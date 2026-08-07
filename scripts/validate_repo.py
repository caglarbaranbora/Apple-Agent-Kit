#!/usr/bin/env python3
"""Levels 2-3 validation for the Apple Agent Kit repository.

Level 1 is per-file and lives in validate_artifact.py. This script is
repository-wide: it checks the things no single file can know about itself --
that its id is unique, that its edges land somewhere, that the graph they form
is acyclic and points the right way, and that the Routing Index agrees with
what is on disk.

Authority for everything in this file:
  docs/validation-model.md                  -- what Levels 2 and 3 cover
  docs/architecture/dependency-graph.md     -- the direction tables
  docs/architecture/linking-model.md        -- the three link conventions
  docs/architecture/routing-model.md        -- the three routing stages
  schemas/metadata.schema.md                -- field names and per-type extensions

A disagreement between this file and those documents is a release-blocking
defect, not a preference.
"""
import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Rules, transcribed from the documents named above.
# ---------------------------------------------------------------------------

# docs/architecture/dependency-graph.md, "Allowed Dependencies". Governs
# `depends_on` only -- `related` has no direction constraint and `routes` is a
# load instruction rather than a dependency.
ALLOWED_DEPENDENCIES = {
    ("knowledge", "reference"),
    ("knowledge", "knowledge"),
    ("skill", "knowledge"),
    ("workflow", "skill"),
}

EDGE_FIELDS = ("depends_on", "related", "routes")

# Directories under the repository root that hold artifacts. Everything else
# (docs/, templates/, validation/, scripts/) is not an artifact.
ARTIFACT_GLOBS = {
    "knowledge": "knowledge/*/*.md",
    "skill": "skills/*/SKILL.md",
    "reference": "references/apple/*.md",
    "workflow": "workflows/*/WORKFLOW.md",
}

ROUTING_INDEX = "skills/index.md"


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


class Finding:
    """A validation failure.

    docs/validation-model.md requires a validator to report the level, the rule
    violated, the artifact, and a suggested remediation. All four are mandatory
    here so that no check can be written that reports less.
    """

    def __init__(self, level, rule, artifact, message, remediation):
        self.level = level
        self.rule = rule
        self.artifact = artifact
        self.message = message
        self.remediation = remediation

    def __str__(self):
        return (
            f"L{self.level} {self.rule}: {self.artifact}\n"
            f"    {self.message}\n"
            f"    fix: {self.remediation}"
        )


# ---------------------------------------------------------------------------
# Metadata parsing
#
# Deliberately dependency-free, matching validate_artifact.py. It parses the
# subset of YAML the schema actually uses: scalars, inline lists, block lists.
# ---------------------------------------------------------------------------


def extract_metadata_block(text):
    """Frontmatter at offset 0 (skill/entry) or a fenced block (everything else)."""
    match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r"```\s*ya?ml\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else ""


def parse_metadata(block):
    fields = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):(.*)$", line)
        if not match:
            i += 1
            continue
        key, rest = match.group(1), match.group(2).strip()
        if rest.startswith("["):
            inner = rest[1:].rsplit("]", 1)[0]
            fields[key] = [v.strip() for v in inner.split(",") if v.strip()]
        elif rest:
            fields[key] = rest
        else:
            items = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s+-\s*", lines[j]):
                items.append(re.sub(r"^\s+-\s*", "", lines[j]).strip())
                j += 1
            fields[key] = items
            i = j - 1
        i += 1
    return fields


def get_list(meta, key):
    value = meta.get(key)
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def section(text, heading):
    """The body of a `## Heading` section, up to the next `## ` or EOF."""
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    return match.group(1) if match else ""


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


class Artifact:
    def __init__(self, path, root):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        self.text = path.read_text()
        self.meta = parse_metadata(extract_metadata_block(self.text))
        self.id = self.meta.get("id")
        self.artifact_type = self.meta.get("artifact_type")
        self.domain = self.meta.get("domain")

    def __repr__(self):
        return f"<Artifact {self.id or self.rel}>"


def load_artifacts(root):
    """Every artifact in the repository, plus the files that claim to be one.

    An artifact's type comes from its `artifact_type` field, not from where it
    sits: `skills/apple-agent-kit/SKILL.md` is the entry point, not a Skill, and
    only its metadata says so.
    """
    artifacts = []
    seen = set()
    for glob in ARTIFACT_GLOBS.values():
        for path in sorted(root.glob(glob)):
            if path.name == "README.md" or path in seen:
                continue
            seen.add(path)
            artifacts.append(Artifact(path, root))
    return artifacts


# ---------------------------------------------------------------------------
# Level 2 -- Repository Integrity
# ---------------------------------------------------------------------------


def check_ids_unique(artifacts, root):
    findings = []
    by_id = {}
    for artifact in artifacts:
        if artifact.id is None:
            findings.append(
                Finding(
                    2,
                    "id-present",
                    artifact.rel,
                    "no `id` field; the artifact cannot be referenced by any edge",
                    "add an `id` following schemas/metadata.schema.md",
                )
            )
            continue
        by_id.setdefault(artifact.id, []).append(artifact.rel)
    for artifact_id, paths in sorted(by_id.items()):
        if len(paths) > 1:
            findings.append(
                Finding(
                    2,
                    "id-unique",
                    artifact_id,
                    "id claimed by " + ", ".join(paths),
                    "ids are immutable and global; rename all but one",
                )
            )
    return findings


def expected_id(artifact):
    """The id a file's location implies, or None where location does not fix it.

    Knowledge and Reference ids are fully determined by the path. A Skill's is
    not: `skills/human-interface-guidelines-components/` holds
    `skill.human-interface-guidelines.components`, so the directory encodes
    `<domain>` or `<domain>-<facet>` and only the domain segment is checkable.
    """
    if artifact.artifact_type == "knowledge":
        return f"knowledge.{artifact.path.parent.name}.{artifact.path.stem}"
    if artifact.artifact_type == "reference":
        return f"reference.apple.{artifact.path.stem}"
    return None


def check_id_matches_path(artifacts, root):
    findings = []
    for artifact in artifacts:
        if artifact.id is None:
            continue
        want = expected_id(artifact)
        if want is not None:
            if artifact.id != want:
                findings.append(
                    Finding(
                        2,
                        "id-path",
                        artifact.rel,
                        f"id is `{artifact.id}` but its location implies `{want}`",
                        "move the file or change the id so the two agree",
                    )
                )
            continue
        if artifact.artifact_type in ("skill", "workflow", "entry"):
            parts = artifact.id.split(".")
            if parts[0] != artifact.artifact_type:
                findings.append(
                    Finding(
                        2,
                        "id-path",
                        artifact.rel,
                        f"id `{artifact.id}` does not start with "
                        f"`{artifact.artifact_type}.`",
                        "an id's first segment is its artifact type",
                    )
                )
            elif artifact.artifact_type == "skill":
                directory = artifact.path.parent.name
                domain_segment = parts[1] if len(parts) > 2 else ""
                if directory != domain_segment and not directory.startswith(
                    domain_segment + "-"
                ):
                    findings.append(
                        Finding(
                            2,
                            "id-path",
                            artifact.rel,
                            f"id `{artifact.id}` has domain segment "
                            f"`{domain_segment}`, which does not match directory "
                            f"`{directory}`",
                            "a Skill directory is `<domain>` or `<domain>-<facet>`; "
                            "see docs/specifications/skill-spec.md",
                        )
                    )
    return findings


def check_domain_matches_directory(artifacts, root):
    """`domain` must agree with the directory -- see CLAUDE.md.

    Compared after slugifying, because the field carries the domain's proper
    name (`Style Guide`) while the directory carries its slug (`style-guide`).
    Workflows and the entry point are not domain-scoped and are skipped.
    """
    findings = []
    for artifact in artifacts:
        if artifact.artifact_type in ("workflow", "entry") or artifact.domain is None:
            continue
        if artifact.artifact_type == "reference":
            actual = artifact.path.stem
        else:
            actual = artifact.path.parent.name
        declared = slugify(artifact.domain)
        if declared == actual:
            continue
        if artifact.artifact_type == "skill" and actual.startswith(declared + "-"):
            continue  # a facet directory, e.g. swiftui-interaction
        findings.append(
            Finding(
                2,
                "domain-path",
                artifact.rel,
                f"declares `domain: {artifact.domain}` but sits in `{actual}`",
                "move the artifact into its domain, or correct the field",
            )
        )
    return findings


def check_edges_resolve(artifacts, root):
    findings = []
    known = {a.id for a in artifacts if a.id}
    for artifact in artifacts:
        for field in EDGE_FIELDS:
            for target in get_list(artifact.meta, field):
                if target not in known:
                    findings.append(
                        Finding(
                            2,
                            "edge-resolves",
                            artifact.rel,
                            f"`{field}` names `{target}`, which no artifact declares",
                            "correct the id, or add the artifact it names",
                        )
                    )
    return findings


def check_wiki_links_resolve(artifacts, root):
    """A Reference's `## Used By` links resolve -- linking-model.md convention 2."""
    findings = []
    for artifact in artifacts:
        if artifact.artifact_type != "reference":
            continue
        for target in re.findall(
            r"\[\[([^\]]+)\]\]", section(artifact.text, "## Used By")
        ):
            if not (root / (target + ".md")).exists():
                findings.append(
                    Finding(
                        2,
                        "wiki-link-resolves",
                        artifact.rel,
                        f"`## Used By` links [[{target}]], which does not exist",
                        "correct the path, or drop the entry if the citation is gone",
                    )
                )
    return findings


def check_used_by_is_complete(artifacts, root):
    """`## Used By` is the reverse index of the Knowledge layer's citations.

    A Contract cites Apple URLs in `references:`; the Reference that indexes
    those URLs must list the Contract back. This is checked by URL, never by
    directory name -- Reference-to-Knowledge is many-to-many, and a
    directory-derived check reports false positives on the three
    human-interface-guidelines References and on cross-domain citations of
    style-guide. See docs/architecture/linking-model.md.
    """
    findings = []
    references = [a for a in artifacts if a.artifact_type == "reference"]
    sources = {}
    for reference in references:
        for url in re.findall(r"https?://\S+", section(reference.text, "## Source")):
            sources.setdefault(url.rstrip(".,);"), []).append(reference)

    for artifact in artifacts:
        if artifact.artifact_type != "knowledge":
            continue
        wiki_target = artifact.rel[:-3]  # drop ".md"
        cited = set()
        for url in get_list(artifact.meta, "references"):
            for reference in sources.get(url.rstrip(".,);"), []):
                cited.add(reference)
        for reference in sorted(cited, key=lambda r: r.rel):
            used_by = section(reference.text, "## Used By")
            if f"[[{wiki_target}]]" not in used_by:
                findings.append(
                    Finding(
                        2,
                        "used-by-complete",
                        reference.rel,
                        f"indexes a URL cited by `{artifact.id}` but does not "
                        f"list it under `## Used By`",
                        f"add `- [[{wiki_target}]]` to `## Used By`",
                    )
                )
    return findings


def check_prose_paths_resolve(artifacts, root):
    """Relative links in prose resolve -- linking-model.md convention 3.

    Two things make a naive implementation report ~50 false positives on this
    repository, and both are handled here rather than by lowering the bar:

    * `npx/README.md` is a byte-for-byte mirror of the root README, published to
      npm. Its links are written against the repository root, which is where
      they resolve for a reader on GitHub. They are resolved that way here.
    * A Markdown link is `[text](target)`, but so is the localization syntax
      `^[…](inflect: true)`. A target containing whitespace is not a path.

    Code spans and fenced blocks are stripped first: a link inside them is a
    format example, not a link. CLAUDE.md documents the README's Skill-bullet
    shape that way.

    `docs/superpowers/` is excluded: design records and plans are dated
    snapshots of past decisions, not maintained documents.
    """
    findings = []
    root_relative = {"npx/README.md"}
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel.startswith((".git/", ".claude/", "node_modules/", "docs/superpowers/")):
            continue
        base = root if rel in root_relative else path.parent
        prose = re.sub(r"```.*?```", "", path.read_text(), flags=re.DOTALL)
        prose = re.sub(r"`[^`\n]*`", "", prose)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if re.search(r"\s", target):
                continue  # not a path; see the docstring
            resolved = (base / target.split("#")[0]).resolve()
            if not resolved.exists():
                findings.append(
                    Finding(
                        2,
                        "prose-path-resolves",
                        rel,
                        f"links `{target}`, which does not resolve",
                        "correct the path; a link that does not resolve is a "
                        "broken link in every renderer",
                    )
                )
    return findings


def check_no_orphans(artifacts, root):
    """An artifact no route and no dependency reaches is unreachable.

    Reachability differs per layer: a Contract is reached by a Skill's `routes`
    or another Contract's `depends_on`; a Reference by a `## Used By` entry; a
    Skill or Workflow by a Routing Index row (checked separately).
    """
    findings = []
    reached = set()
    for artifact in artifacts:
        reached.update(get_list(artifact.meta, "routes"))
        reached.update(get_list(artifact.meta, "depends_on"))

    for artifact in artifacts:
        if artifact.artifact_type == "knowledge" and artifact.id not in reached:
            findings.append(
                Finding(
                    2,
                    "orphan",
                    artifact.rel,
                    "no Skill routes to it and no Contract depends on it",
                    "add it to the owning Skill's `routes` and `## Routing`, "
                    "or retire it per docs/specifications/skill-management.md",
                )
            )
        if artifact.artifact_type == "reference":
            if not re.search(r"\[\[", section(artifact.text, "## Used By")):
                findings.append(
                    Finding(
                        2,
                        "orphan",
                        artifact.rel,
                        "`## Used By` is empty; no Knowledge Contract cites it",
                        "cite it from a Contract, or retire the Reference",
                    )
                )
    return findings


def check_routing_index_sync(artifacts, root):
    """`skills/index.md` agrees with `skills/` and `workflows/`, both directions."""
    findings = []
    index_path = root / ROUTING_INDEX
    if not index_path.exists():
        return [
            Finding(
                2,
                "index-sync",
                ROUTING_INDEX,
                "the Routing Index does not exist",
                "create it; without it no Skill or Workflow is reachable",
            )
        ]
    index = index_path.read_text()

    on_disk = {
        a.path.parent.name: a
        for a in artifacts
        if a.artifact_type in ("skill", "workflow")
    }
    listed = set(re.findall(r"(?:skills|workflows)/([a-z0-9-]+)/", index))

    for name, artifact in sorted(on_disk.items()):
        if name not in listed:
            findings.append(
                Finding(
                    2,
                    "index-sync",
                    artifact.rel,
                    "not listed in the Routing Index, so nothing can route to it",
                    f"add a row for `{name}` to {ROUTING_INDEX}",
                )
            )
    for name in sorted(listed - set(on_disk)):
        if (root / "skills" / name).exists() or (root / "workflows" / name).exists():
            continue
        findings.append(
            Finding(
                2,
                "index-sync",
                ROUTING_INDEX,
                f"lists `{name}`, which is not on disk",
                "remove the row, or restore the artifact",
            )
        )
    return findings


# ---------------------------------------------------------------------------
# Level 3 -- Architectural
# ---------------------------------------------------------------------------


def check_dependency_direction(artifacts, root):
    findings = []
    types = {a.id: a.artifact_type for a in artifacts if a.id}
    for artifact in artifacts:
        for target in get_list(artifact.meta, "depends_on"):
            target_type = types.get(target)
            if target_type is None:
                continue  # already reported by edge-resolves
            pair = (artifact.artifact_type, target_type)
            if pair not in ALLOWED_DEPENDENCIES:
                findings.append(
                    Finding(
                        3,
                        "dependency-direction",
                        artifact.rel,
                        f"{pair[0]} depends_on {pair[1]} (`{target}`), which the "
                        f"dependency graph forbids",
                        "see docs/architecture/dependency-graph.md; a non-binding "
                        "link belongs in `related`",
                    )
                )
    return findings


def check_dependency_graph_is_acyclic(artifacts, root):
    graph = {
        a.id: [t for t in get_list(a.meta, "depends_on")] for a in artifacts if a.id
    }
    findings = []
    WHITE, GREY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def visit(node, stack):
        color[node] = GREY
        for target in graph.get(node, []):
            if target not in color:
                continue
            if color[target] == GREY:
                cycle = stack[stack.index(target):] + [target]
                findings.append(
                    Finding(
                        3,
                        "dependency-acyclic",
                        node,
                        "cycle: " + " -> ".join(cycle),
                        "break the cycle; `depends_on` must form a DAG so that "
                        "transitive resolution terminates",
                    )
                )
            elif color[target] == WHITE:
                visit(target, stack + [target])
        color[node] = BLACK

    for node in sorted(graph):
        if color[node] == WHITE:
            visit(node, [node])
    return findings


def check_routing_coverage(artifacts, root):
    """Routing Stage 2 -- routing-model.md.

    Every id in `routes:` must appear in the Skill's `## Routing` section, and no
    Skill may route to a Skill. `## Routing` names Contracts by filename rather
    than by id, so the check is on the id's final segment plus the `.md`
    extension: a bare substring test would let `something-else.md` satisfy a
    route to `thing`.
    """
    findings = []
    for artifact in artifacts:
        if artifact.artifact_type != "skill":
            continue
        routing = section(artifact.text, "## Routing")
        for target in get_list(artifact.meta, "routes"):
            if target.startswith("skill."):
                findings.append(
                    Finding(
                        3,
                        "no-skill-to-skill",
                        artifact.rel,
                        f"routes to `{target}`, another Skill",
                        "a Skill routes only to Knowledge; composing Skills is a "
                        "Workflow's job",
                    )
                )
                continue
            slug = target.split(".")[-1]
            if not re.search(rf"(?<![\w-]){re.escape(slug)}\.md\b", routing):
                findings.append(
                    Finding(
                        3,
                        "routing-coverage",
                        artifact.rel,
                        f"`routes` names `{target}` but `## Routing` never "
                        f"mentions it, so no task can reach it",
                        f"add a `## Routing` line ending in `-> {slug}.md`, or "
                        f"drop the id from `routes`",
                    )
                )
    return findings


def check_workflows_compose_skills(artifacts, root):
    """A Workflow exists to compose Skills -- workflow-spec.md requires two."""
    findings = []
    for artifact in artifacts:
        if artifact.artifact_type != "workflow":
            continue
        skills = get_list(artifact.meta, "skills")
        if len(skills) < 2:
            findings.append(
                Finding(
                    3,
                    "workflow-composes",
                    artifact.rel,
                    f"names {len(skills)} Skill(s); a Workflow exists to compose "
                    f"several",
                    "name at least two Skills, or make this a Skill instead; see "
                    "docs/specifications/workflow-spec.md",
                )
            )
    return findings


CHECKS = [
    check_ids_unique,
    check_id_matches_path,
    check_domain_matches_directory,
    check_edges_resolve,
    check_wiki_links_resolve,
    check_prose_paths_resolve,
    check_used_by_is_complete,
    check_no_orphans,
    check_routing_index_sync,
    check_dependency_direction,
    check_dependency_graph_is_acyclic,
    check_routing_coverage,
    check_workflows_compose_skills,
]


def validate_repo(root):
    artifacts = load_artifacts(Path(root))
    findings = []
    for check in CHECKS:
        findings.extend(check(artifacts, Path(root)))
    return artifacts, findings


def main():
    parser = argparse.ArgumentParser(
        description="Validate the repository (Levels 2-3)."
    )
    parser.add_argument(
        "root", nargs="?", default=".", help="Repository root (default: .)"
    )
    args = parser.parse_args()

    artifacts, findings = validate_repo(args.root)
    print(f"{len(artifacts)} artifacts, {len(CHECKS)} checks")

    if not findings:
        print("PASS")
        sys.exit(0)

    for finding in sorted(findings, key=lambda f: (f.level, f.rule, f.artifact)):
        print(finding)
    print(f"\nFAIL: {len(findings)} finding(s)")
    sys.exit(1)


if __name__ == "__main__":
    main()
