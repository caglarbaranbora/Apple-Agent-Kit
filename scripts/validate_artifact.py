#!/usr/bin/env python3
"""Level 1 (Structural) validation for Apple Agent Kit artifacts.

Authority for everything in this file:
  schemas/metadata.schema.md          -- field names and per-type extensions
  docs/specifications/*-spec.md       -- required sections and size limits
  docs/validation-model.md            -- what Level 1 covers

A disagreement between this file and those documents is a release-blocking
defect, not a preference. Levels 2-3 (repository-wide) live in validate_repo.py.
"""
import argparse
import re
import sys
from pathlib import Path

ARTIFACT_TYPES = ["knowledge", "skill", "reference", "workflow", "entry"]

# docs/artifact-lifecycle.md, "States". `Review` is deliberately absent.
STATUSES = ["Draft", "Approved", "Deprecated", "Archived"]

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

LINE_CAPS = {"knowledge": 150, "skill": 80, "reference": 98, "workflow": 80}

# Where each type lives, for the "artifact_type agrees with its location" check.
# A type absent here is not location-constrained.
TYPE_LOCATIONS = {
    "knowledge": "knowledge",
    "skill": "skills",
    "reference": "references",
    "workflow": "workflows",
    "entry": "skills",
}

REQUIRED_SECTIONS = {
    "knowledge": [
        "## Intent",
        "## Rules",
        "## Compliant Example",
        "## Non-Compliant Example",
        "## Dependencies",
    ],
    "skill": ["## Purpose", "## Routing", "## Stop Conditions"],
    "reference": ["## Source", "## Purpose", "## Primary Topics", "## Used By"],
    "workflow": [
        "## Purpose",
        "## Scope",
        "## Trigger Conditions",
        "## Skill Sequence",
        "## Exit Conditions",
    ],
}

# Required of every artifact type.
BASE_METADATA_FIELDS = [
    "id",
    "artifact_type",
    "title",
    "version",
    "status",
    "last_updated",
]

# Added per type. `domain` is an extension rather than a base field because a
# workflow spans domains by definition and an entry belongs to none.
METADATA_EXTENSIONS = {
    "knowledge": [
        "domain",
        "owner",
        "summary",
        "tags",
        "depends_on",
        "related",
        "references",
    ],
    "skill": ["domain", "name", "description", "routes", "related"],
    "reference": ["domain", "owner", "summary"],
    "workflow": ["skills", "related"],
    "entry": ["name", "description"],
}


def required_metadata_fields(artifact_type):
    return BASE_METADATA_FIELDS + METADATA_EXTENSIONS.get(artifact_type, [])


def extract_metadata_block(text, artifact_type=None):
    if artifact_type in ("skill", "entry"):
        # Real Claude Code skills need frontmatter at byte offset 0 -- a
        # fenced ```yaml block anywhere in the body (the knowledge/reference
        # convention) is not something the skill loader parses.
        match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
        return match.group(1) if match else ""
    match = re.search(r"```\s*ya?ml\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else ""


def validate_text(text, artifact_type):
    errors = []
    cap = LINE_CAPS.get(artifact_type)
    line_count = len(text.splitlines())
    if cap is not None and line_count > cap:
        errors.append(f"exceeds {artifact_type} line cap: {line_count} > {cap}")

    for heading in REQUIRED_SECTIONS.get(artifact_type, []):
        if not re.search(rf"^{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"missing required section: {heading}")

    block = extract_metadata_block(text, artifact_type)
    if not block:
        errors.append("missing metadata YAML block")
        return errors

    for field in required_metadata_fields(artifact_type):
        if not re.search(rf"^{field}:", block, re.MULTILINE):
            errors.append(f"missing required metadata field: {field}")

    declared_type = scalar(block, "artifact_type")
    if declared_type is not None and declared_type != artifact_type:
        errors.append(
            f"artifact_type is `{declared_type}` but the file was validated "
            f"as `{artifact_type}`"
        )
    elif declared_type is not None and declared_type not in ARTIFACT_TYPES:
        errors.append(f"unknown artifact_type: {declared_type}")

    status = scalar(block, "status")
    if status is not None and status not in STATUSES:
        errors.append(f"unknown status: {status} (expected one of {', '.join(STATUSES)})")

    version = scalar(block, "version")
    if version is not None and not SEMVER.match(version):
        errors.append(f"version is not a semantic version: {version}")

    # docs/artifact-lifecycle.md, "Versioning": "Approval establishes a stable
    # version -- 1.0.0 for a first approval". An Approved artifact still on a
    # 0.x version is Approved in name only.
    if status == "Approved" and version is not None and SEMVER.match(version):
        if int(version.split(".")[0]) < 1:
            errors.append(
                f"status is Approved but version is {version}; approval "
                f"establishes a stable version (>= 1.0.0)"
            )

    # The prose header duplicates two metadata fields in every artifact that
    # has one. Nothing compared them until Phase 6, and the promotion pass is
    # exactly the edit that writes both -- so it is exactly the edit that can
    # leave them disagreeing.
    errors.extend(header_disagreements(text, status, version))

    return errors


# `Status: Draft` on its own line, or `Status: Draft Version: 0.1.0` on one
# line. Skills carry neither: their frontmatter is the only copy.
HEADER = re.compile(
    r"^Status:[ \t]+(?P<status>\S+)(?:[ \t]+Version:[ \t]+(?P<version>\S+))?[ \t]*$",
    re.MULTILINE,
)


def header_disagreements(text, status, version):
    """The prose `Status:`/`Version:` header agrees with the metadata block."""
    match = HEADER.search(text)
    if match is None:
        return []

    errors = []
    if status is not None and match.group("status") != status:
        errors.append(
            f"prose header says `Status: {match.group('status')}` but metadata "
            f"says `status: {status}`"
        )

    header_version = match.group("version")
    if header_version is None:
        # A `Version:` on its own line, which several documents use.
        line = re.search(r"^Version:[ \t]+(\S+)[ \t]*$", text, re.MULTILINE)
        header_version = line.group(1) if line else None

    if header_version is not None and version is not None and header_version != version:
        errors.append(
            f"prose header says `Version: {header_version}` but metadata "
            f"says `version: {version}`"
        )
    return errors


def scalar(block, field):
    match = re.search(rf"^{field}:\s*(.*)$", block, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip() or None


def validate_file(path, artifact_type):
    path = Path(path)
    errors = validate_text(path.read_text(), artifact_type)

    # Location agreement needs the path, so it cannot live in validate_text.
    # Only files already inside the artifact tree are checked -- a fixture in a
    # temporary directory is in none of these roots and is not being misfiled.
    expected = TYPE_LOCATIONS.get(artifact_type)
    parts = set(path.resolve().parts)
    roots = parts & set(TYPE_LOCATIONS.values())
    if expected is not None and roots and expected not in roots:
        errors.append(
            f"a `{artifact_type}` artifact belongs under `{expected}/`, "
            f"but this file is under `{sorted(roots)[0]}/`"
        )
    return errors


def declared_type(path):
    """The `artifact_type` a file claims, or None.

    Used by `--all`, where a file's type comes from its metadata rather than a
    flag: `skills/apple-agent-kit/SKILL.md` sits among the Skills but is the
    entry point, and only its metadata says so.
    """
    text = Path(path).read_text()
    for candidate in ("skill", "knowledge"):  # both metadata block shapes
        block = extract_metadata_block(text, candidate)
        if block:
            return scalar(block, "artifact_type")
    return None


def iter_artifacts(root):
    root = Path(root)
    globs = [
        "knowledge/*/*.md",
        "skills/*/SKILL.md",
        "references/apple/*.md",
        "workflows/*/WORKFLOW.md",
    ]
    for glob in globs:
        for path in sorted(root.glob(glob)):
            if path.name != "README.md":
                yield path


def validate_all(root):
    """Level 1 across every artifact. Returns (checked, {path: errors})."""
    failures = {}
    checked = 0
    for path in iter_artifacts(root):
        artifact_type = declared_type(path)
        checked += 1
        if artifact_type is None:
            failures[path] = ["no `artifact_type`; cannot determine how to validate"]
            continue
        if artifact_type not in ARTIFACT_TYPES:
            failures[path] = [f"unknown artifact_type: {artifact_type}"]
            continue
        errors = validate_file(path, artifact_type)
        if errors:
            failures[path] = errors
    return checked, failures


def main():
    parser = argparse.ArgumentParser(
        description="Validate an Apple Agent Kit artifact (Level 1 - Structural)."
    )
    parser.add_argument(
        "path", help="Path to the artifact markdown file, or to the repository with --all"
    )
    parser.add_argument("--type", choices=ARTIFACT_TYPES, help="Artifact type")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate every artifact under PATH, taking each type from its metadata",
    )
    args = parser.parse_args()

    if args.all:
        checked, failures = validate_all(args.path)
        for path, errors in sorted(failures.items()):
            print(f"FAIL: {path}")
            for e in errors:
                print(f"  - {e}")
        print(f"\n{checked - len(failures)}/{checked} artifacts pass Level 1")
        sys.exit(1 if failures else 0)

    if not args.type:
        parser.error("--type is required unless --all is given")

    errors = validate_file(args.path, args.type)
    if errors:
        print(f"FAIL: {args.path}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"PASS: {args.path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
