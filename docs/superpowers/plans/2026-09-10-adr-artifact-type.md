# ADR Artifact Type Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a sixth, fully validated artifact type, `adr` (Architecture Decision
Record), give it a spec and validator support matching the repo's other five types,
and prove the whole pipeline end-to-end with one real ADR (`style-guide`, the
simplest domain) plus the matching `domain-map.md` link.

**Architecture:** `adr` joins `knowledge`/`skill`/`reference`/`workflow`/`entry` in
`schemas/metadata.schema.md`'s type enum, gets its own
`docs/specifications/adr-spec.md`, and is checked at Level 1 by
`scripts/validate_artifact.py --type adr` (required sections, 150-line cap,
metadata fields) and at Level 2 by a new `scripts/validate_repo.py` check that
`docs/architecture/domain-map.md`'s `ADR` column links resolve, and that every
`docs/adr/*.md` file is linked from exactly one row — bidirectional, mirroring the
existing `check_no_orphans`/`check_wiki_links_resolve` shape.

**Tech Stack:** Python 3 stdlib only (`re`, `pathlib`, `argparse`), `unittest`. No
new dependencies — matches every existing script and test in `scripts/`/`tests/`.

**Scope of this plan:** Infrastructure (schema, spec, both validators, their tests)
plus exactly one real ADR, proving the pipeline works on real content. It does
**not** migrate the other ~30 domains out of `domain-map.md`'s "Completed:"
paragraph, and does **not** touch `## Cross-Domain Notes`. Both are explicitly
out of scope per `docs/superpowers/specs/2026-09-10-adr-artifact-type-design.md`'s
Non-goals, and the bulk migration is large enough to be its own follow-up plan (see
the handoff note at the end of this document, which gives that plan everything it
needs: the full domain → ADR-number mapping).

---

### Task 1: Schema — add `adr` to the type enum

**Files:**
- Modify: `schemas/metadata.schema.md`

- [ ] **Step 1: Add the `adr` per-type extension row**

In `schemas/metadata.schema.md`, find the "Per-type extension" table (currently
5 rows: `knowledge`, `skill`, `reference`, `workflow`, `entry`) and add a row after
`entry`:

```
| `adr` | `domain`, `related` |
```

- [ ] **Step 2: Add `adr` to the `artifact_type` enum**

Find:

```
### `artifact_type`

`knowledge`, `skill`, `reference`, `workflow`, `entry`, `template`, `spec`
```

Replace with:

```
### `artifact_type`

`knowledge`, `skill`, `reference`, `workflow`, `entry`, `template`, `spec`, `adr`
```

- [ ] **Step 3: Verify by eye**

No test suite covers this file directly — `tests/test_validate_artifact.py`'s
`TestMetadataSchema` tests exercise `validate_artifact.py`'s own copies of these
tables (updated in Task 7), not this markdown file. Confirm the two edits above are
the only change: `git diff schemas/metadata.schema.md` should show exactly a
one-line enum addition and a one-row table addition.

- [ ] **Step 4: Commit**

```bash
git add schemas/metadata.schema.md
git commit -m "docs: add adr to the metadata schema's artifact_type enum"
```

---

### Task 2: `docs/specifications/adr-spec.md`

**Files:**
- Create: `docs/specifications/adr-spec.md`

- [ ] **Step 1: Write the spec, matching `knowledge-spec.md`'s shape**

```markdown
# ADR Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the normative specification for every Architecture Decision Record (ADR)
in Apple Agent Kit.

An ADR records *why* one domain's scope was set where it was, and when it later
changed — separately from `docs/architecture/domain-map.md`, which records only
*what* the current scope is. It is a governance document, not domain content: it
carries no implementation rules and is never routed to by a Skill.

## When an ADR Is Warranted

For a *new* decision (as opposed to the initial migration this spec accompanies),
use `mattpocock/skills`' three-part test, cited in
`docs/research/2026-09-mattpocock-skills-architecture.md` §5-6:

- **Hard to reverse.**
- **Surprising without context** — a later reader would otherwise ask "why is it
  like this?"
- **The result of a real trade-off**, not a default choice with no alternative
  seriously considered.

A decision that fails all three stays as ordinary prose in the relevant Knowledge
Contract, Skill, or `domain-map.md` row instead of getting its own ADR.

## Location

    docs/adr/<NNNN>-<domain-slug>-scope.md

`NNNN` is a zero-padded, sequential, four-digit number, assigned once per domain
and never reused or renumbered. The id is `adr.<NNNN>` and MUST agree with the
number in the filename — a validator checks the two agree, the same pattern
`knowledge-spec.md` uses for id/path agreement.

## Required Metadata

Common base (see `../../schemas/metadata.schema.md` [[metadata.schema]]):
`id`, `artifact_type`, `title`, `version`, `status`, `last_updated`

ADR extension: `domain` (the domain name exactly as it appears in
`domain-map.md`'s `Domain` column), `related` (non-binding; used to point at the
ADR that supersedes this one, when `status` is `Deprecated`)

`artifact_type` is `adr`.

## Required Sections

1. `## Context` — why the decision was needed
2. `## Decision` — what was decided (the domain's initial scope)
3. `## Consequences` — what the decision affected: which files, which other
   domains, what it ruled out
4. `## Verification Log` — dated bullets. A later scope change (an expansion, a
   closed gap) is a new dated bullet here, **not** a rewrite of `## Decision`'s
   original text and **not** a new ADR — one ADR persists for the domain's whole
   life (see Granularity below)

## Granularity

One ADR per domain, for the life of that domain. When scope changes later
(an expansion, a closed gap, a retirement), append a dated bullet to
`## Consequences`/`## Verification Log` rather than opening a new ADR file. This
mirrors how `domain-map.md`'s prose already appended "expanded 2026-08-08 to add
X" before this spec existed — this changes *where* that sentence lives, not its
shape.

## Status Semantics

Reuses the four states `../artifact-lifecycle.md` [[artifact-lifecycle]] already
defines — no ADR-specific vocabulary:

- **Approved** — this decision currently governs the domain's scope.
- **Deprecated** — a later ADR supersedes this one. Name the superseding ADR via
  `related:`.
- **Archived** — the domain itself is retired (e.g. `authentication`). Matches
  `domain-map.md`'s "Retired" status for that row.
- **Draft** — being authored; not yet a settled record.

## Rules

- One domain per ADR (see Granularity). Do not describe more than one domain's
  scope in a single ADR — that is what `## Cross-Domain Notes` is for, and ADRs do
  not currently cover that section (see the design's Non-goals; a future ADR
  variant or distinct artifact type may).
- `## Decision`/`## Consequences` content MUST be traceable to what
  `domain-map.md`'s current row for that domain says it owns, not asserted fresh.
  Where `domain-map.md` itself has no elaborating prose for the domain (a real
  case — some domains were never narrated in detail there), `## Context` MUST say
  so explicitly rather than inventing a rationale, and MAY instead cite that
  domain's own `docs/superpowers/specs/*-design.md` if one exists.
- Do not embed implementation rules. An ADR is never a Knowledge Contract in
  disguise — if a rule belongs in a Contract, it goes there, not here.
- `## Verification Log` entries are append-only. Do not edit or remove an earlier
  entry to "clean up" the record; a wrong entry gets a new dated entry that
  corrects it, the same way `domain-map.md`'s own history is never quietly
  rewritten.

## Size Limit

An ADR MUST NOT exceed 150 lines, the same cap as a Knowledge Contract. An ADR
that grows past it during `## Verification Log` accretion is a signal the domain
has enough independent decision history to warrant a closer look — not, by
itself, an automatic trigger to split it.

## References

Cite `domain-map.md`'s row for the domain, and that domain's own
`docs/superpowers/specs/*-design.md` where one exists.

## Validation Checklist

- Metadata complete and valid against the schema
- Filename number and `id`'s `<NNNN>` agree
- Exactly one domain described
- All four required sections present
- `## Decision`/`## Consequences` traceable to `domain-map.md`'s current row (or
  the domain's own design spec, where `domain-map.md` itself is silent)
- `status` is one of the four lifecycle states, with `Deprecated`/`Archived`
  semantics as defined above
```

- [ ] **Step 2: Commit**

```bash
git add docs/specifications/adr-spec.md
git commit -m "docs: add adr-spec.md, the ADR artifact type specification"
```

---

### Task 3: Register the 150-line cap in `docs/validation-model.md`

**Files:**
- Modify: `docs/validation-model.md`

- [ ] **Step 1: Add a row to the Level 1 size-limits table**

Find:

```
| Artifact | Limit |
|---|---|
| Knowledge Contract | 150 lines |
| Skill | 80 lines |
| Workflow | 80 lines |
| Reference | 98 lines |
```

Replace with:

```
| Artifact | Limit |
|---|---|
| Knowledge Contract | 150 lines |
| Skill | 80 lines |
| Workflow | 80 lines |
| Reference | 98 lines |
| ADR | 150 lines |
```

- [ ] **Step 2: Commit**

```bash
git add docs/validation-model.md
git commit -m "docs: register the ADR size limit in the validation model"
```

---

### Task 4: Register `adr-spec.md` in `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add a row to "The normative specs" table**

Find:

```
| Artifact | Spec |
|---|---|
| Knowledge Contract | `docs/specifications/knowledge-spec.md` |
| Skill | `docs/specifications/skill-spec.md` |
| Reference | `docs/specifications/reference-spec.md` |
| Workflow | `docs/specifications/workflow-spec.md` |
| Metadata fields (all types) | `schemas/metadata.schema.md` |
```

Replace with:

```
| Artifact | Spec |
|---|---|
| Knowledge Contract | `docs/specifications/knowledge-spec.md` |
| Skill | `docs/specifications/skill-spec.md` |
| Reference | `docs/specifications/reference-spec.md` |
| Workflow | `docs/specifications/workflow-spec.md` |
| Architecture Decision Record | `docs/specifications/adr-spec.md` |
| Metadata fields (all types) | `schemas/metadata.schema.md` |
```

Note: this does **not** touch the "Layer order (do not violate)" section above it
in `CLAUDE.md`. An ADR is a governance/decision record, not a fifth
content-pipeline layer alongside References → Knowledge → Skills → Workflows — it
is never routed to by a Skill and carries no domain implementation rules (see
`adr-spec.md`'s Rules). This is deliberate and matches how `template`/`spec`
already sit in the `artifact_type` enum without being pipeline layers either.

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: register adr-spec.md in CLAUDE.md's normative specs table"
```

---

### Task 5: `validate_artifact.py` — write the failing tests first

**Files:**
- Modify: `tests/test_validate_artifact.py`

- [ ] **Step 1: Add a valid ADR fixture and a test class**

Add this near the top of `tests/test_validate_artifact.py`, after `VALID_KNOWLEDGE`
(and before `class TestValidateKnowledge`):

````python
VALID_ADR = """# ADR-0001: Example Domain Scope

## Metadata

```yaml
id: adr.0001
artifact_type: adr
title: Example Domain Scope
version: 1.0.0
status: Approved
domain: Example
related: []
last_updated: 2026-09-10
```

## Context

Why the Example domain's scope was set where it was.

## Decision

Example domain covers X, Y, Z.

## Consequences

Affects `knowledge/example/`.

## Verification Log

- 2026-09-10: initial scope recorded.
"""
````

Then add, after `class TestValidateKnowledge`'s closing (before
`class TestValidateSkill` or wherever the next class begins — insert it as its own
new class anywhere after `TestValidateKnowledge`):

```python
class TestValidateAdr(unittest.TestCase):
    def test_valid_adr_has_no_errors(self):
        errors = validate_artifact.validate_text(VALID_ADR, "adr")
        self.assertEqual(errors, [])

    def test_line_cap_is_150(self):
        text = VALID_ADR + ("\nextra line\n" * 150)
        errors = validate_artifact.validate_text(text, "adr")
        self.assertTrue(any("line cap" in e for e in errors))
        self.assertTrue(any("> 150" in e for e in errors))

    def test_missing_context_section_is_rejected(self):
        text = VALID_ADR.replace("## Context", "## Renamed")
        errors = validate_artifact.validate_text(text, "adr")
        self.assertIn("missing required section: ## Context", errors)

    def test_missing_verification_log_section_is_rejected(self):
        text = VALID_ADR.replace("## Verification Log", "## Renamed")
        errors = validate_artifact.validate_text(text, "adr")
        self.assertIn("missing required section: ## Verification Log", errors)

    def test_missing_domain_field_is_rejected(self):
        text = VALID_ADR.replace("domain: Example\n", "")
        errors = validate_artifact.validate_text(text, "adr")
        self.assertTrue(any("domain" in e for e in errors))

    def test_adr_under_docs_adr_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "docs" / "adr" / "0001-example-scope.md"
            path.parent.mkdir(parents=True)
            path.write_text(VALID_ADR)
            errors = validate_artifact.validate_file(path, "adr")
        self.assertEqual(errors, [])

    def test_adr_under_knowledge_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "knowledge" / "example" / "misfiled.md"
            path.parent.mkdir(parents=True)
            path.write_text(VALID_ADR)
            errors = validate_artifact.validate_file(path, "adr")
        self.assertTrue(any("belongs under `docs/adr/`" in e for e in errors), errors)
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `python3 -m unittest tests.test_validate_artifact.TestValidateAdr -v`

Expected: every test errors or fails — `validate_text` doesn't know `"adr"` yet, so
`LINE_CAPS.get("adr")` is `None` (no line-cap error ever fires),
`REQUIRED_SECTIONS.get("adr", [])` is `[]` (no missing-section error ever fires),
and `required_metadata_fields("adr")` omits `domain` (no missing-field error
fires) — so `test_valid_adr_has_no_errors` is the one that currently passes by
accident, and every other new test fails because the check it exercises does not
yet exist for `"adr"`.

---

### Task 6: `validate_artifact.py` — implement `adr` support

**Files:**
- Modify: `scripts/validate_artifact.py:17,24,28-34,36-53,67-81`

- [ ] **Step 1: Add `"adr"` to `ARTIFACT_TYPES`**

Change (line 17):

```python
ARTIFACT_TYPES = ["knowledge", "skill", "reference", "workflow", "entry"]
```

to:

```python
ARTIFACT_TYPES = ["knowledge", "skill", "reference", "workflow", "entry", "adr"]
```

- [ ] **Step 2: Add the ADR line cap**

Change (line 24):

```python
LINE_CAPS = {"knowledge": 150, "skill": 80, "reference": 98, "workflow": 80}
```

to:

```python
LINE_CAPS = {"knowledge": 150, "skill": 80, "reference": 98, "workflow": 80, "adr": 150}
```

- [ ] **Step 3: Add the ADR location constraint**

Change (lines 28-34):

```python
TYPE_LOCATIONS = {
    "knowledge": "knowledge",
    "skill": "skills",
    "reference": "references",
    "workflow": "workflows",
    "entry": "skills",
}
```

to:

```python
TYPE_LOCATIONS = {
    "knowledge": "knowledge",
    "skill": "skills",
    "reference": "references",
    "workflow": "workflows",
    "entry": "skills",
    "adr": "adr",
}
```

(`"adr"` here is the directory name `docs/adr/` ends with — the check in
`validate_file` matches on `path.resolve().parts`, so it is comparing directory
*names*, the same way `"knowledge"` matches `knowledge/` and `"references"`
matches `references/apple/`.)

- [ ] **Step 4: Add the required sections**

Change (lines 36-53) by adding an `"adr"` key to `REQUIRED_SECTIONS`:

```python
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
    "adr": [
        "## Context",
        "## Decision",
        "## Consequences",
        "## Verification Log",
    ],
}
```

- [ ] **Step 5: Add the metadata extension**

Change (lines 67-81) by adding an `"adr"` key to `METADATA_EXTENSIONS`:

```python
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
    "adr": ["domain", "related"],
}
```

- [ ] **Step 6: Add `docs/adr/*.md` to the artifacts the `--all` walker discovers**

Change `iter_artifacts` (around line 232):

```python
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
```

to:

```python
def iter_artifacts(root):
    root = Path(root)
    globs = [
        "knowledge/*/*.md",
        "skills/*/SKILL.md",
        "references/apple/*.md",
        "workflows/*/WORKFLOW.md",
        "docs/adr/*.md",
    ]
    for glob in globs:
        for path in sorted(root.glob(glob)):
            if path.name != "README.md":
                yield path
```

- [ ] **Step 7: Run the tests to verify they pass**

Run: `python3 -m unittest tests.test_validate_artifact.TestValidateAdr -v`

Expected: `OK` — all 7 tests pass.

- [ ] **Step 8: Run the full `validate_artifact.py` test suite**

Run: `python3 -m unittest tests.test_validate_artifact -v`

Expected: `OK`, all tests pass (no existing test broke — `ARTIFACT_TYPES`,
`LINE_CAPS`, etc. only gained a key, nothing already there changed shape).

- [ ] **Step 9: Commit**

```bash
git add scripts/validate_artifact.py tests/test_validate_artifact.py
git commit -m "feat: add adr artifact type support to validate_artifact.py"
```

---

### Task 7: `validate_repo.py` — write the failing tests first

**Files:**
- Modify: `tests/test_validate_repo.py`

- [ ] **Step 1: Add an ADR fixture constant**

Add near the top of `tests/test_validate_repo.py`, after the `KNOWLEDGE` constant:

````python
ADR = """# ADR-0001: Example Domain Scope

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: adr.0001
artifact_type: adr
title: Example Domain Scope
version: 1.0.0
status: Approved
domain: Example
related: []
last_updated: 2026-09-10
```

## Context

Why.

## Decision

What.

## Consequences

Affects nothing in this fixture.

## Verification Log

- 2026-09-10: initial scope recorded.
"""
````

- [ ] **Step 2: Add a test class exercising the new bidirectional check**

Add, after `class TestFixtureIsValid(RepoTestCase)`:

```python
class TestAdrLinks(RepoTestCase):
    DOMAIN_MAP = (
        "# Domain Map\n\n"
        "| Domain | Slug | Initial Scope | Owns | ADR |\n"
        "|---|---|---|---|---|\n"
        "| Example | example | Example scope | Example owns | "
        "[ADR-0001](../adr/0001-example-scope.md) |\n"
    )

    def test_resolving_link_with_matching_file_has_no_findings(self):
        self.repo.write("docs/architecture/domain-map.md", self.DOMAIN_MAP)
        self.repo.write("docs/adr/0001-example-scope.md", ADR)
        self.assertNotIn("domain-map-adr-link", self.repo.rules())

    def test_broken_link_is_reported(self):
        self.repo.write(
            "docs/architecture/domain-map.md",
            self.DOMAIN_MAP.replace("0001-example-scope.md", "0001-missing.md"),
        )
        self.assertRule("domain-map-adr-link")

    def test_orphan_adr_file_is_reported(self):
        self.repo.write("docs/architecture/domain-map.md", self.DOMAIN_MAP)
        self.repo.write("docs/adr/0001-example-scope.md", ADR)
        self.repo.write(
            "docs/adr/0002-orphan-scope.md",
            ADR.replace("adr.0001", "adr.0002").replace("Example Domain Scope", "Orphan Scope"),
        )
        self.assertRule("domain-map-adr-link")

    def test_no_domain_map_file_has_no_findings(self):
        # RepoFixture's base fixture (see class RepoFixture above) has no
        # docs/architecture/domain-map.md at all -- the check must no-op
        # rather than error when the file the ADR column lives in is absent.
        self.assertNotIn("domain-map-adr-link", self.repo.rules())
```

- [ ] **Step 3: Add a test proving `check_domain_matches_directory` skips `adr`**

Add to the same new class:

```python
    def test_domain_field_is_not_checked_against_directory(self):
        # ADRs live flat in docs/adr/, never in a domain-named subdirectory,
        # unlike knowledge/skill/reference -- the domain-directory check must
        # skip this type the same way it already skips workflow/entry.
        self.repo.write("docs/adr/0001-example-scope.md", ADR)
        self.assertNotIn("domain-path", self.repo.rules())
```

- [ ] **Step 4: Run the new tests to verify they fail**

Run: `python3 -m unittest tests.test_validate_repo.TestAdrLinks -v`

Expected: failures. `ARTIFACT_GLOBS` does not yet include `"adr"`, so
`load_artifacts` never sees `docs/adr/*.md` files at all — the new check function
does not exist yet (an `AttributeError`/`NameError`-shaped failure at collection
or the test simply cannot find `"domain-map-adr-link"` among findings because
nothing ever produces it), and `test_domain_field_is_not_checked_against_directory`
currently passes vacuously (the file is never loaded, so `check_domain_matches_directory`
never sees it either) — that one test will need re-checking after Task 8 rather
than trusted as "already green".

---

### Task 8: `validate_repo.py` — implement `adr` support

**Files:**
- Modify: `scripts/validate_repo.py:43-48,217-229,284-313,1099-1118`

- [ ] **Step 1: Add the ADR glob**

Change `ARTIFACT_GLOBS` (around line 43):

```python
ARTIFACT_GLOBS = {
    "knowledge": "knowledge/*/*.md",
    "skill": "skills/*/SKILL.md",
    "reference": "references/apple/*.md",
    "workflow": "workflows/*/WORKFLOW.md",
}
```

to:

```python
ARTIFACT_GLOBS = {
    "knowledge": "knowledge/*/*.md",
    "skill": "skills/*/SKILL.md",
    "reference": "references/apple/*.md",
    "workflow": "workflows/*/WORKFLOW.md",
    "adr": "docs/adr/*.md",
}
```

- [ ] **Step 2: Teach `expected_id` the ADR id/path shape**

Change `expected_id` (around line 217):

```python
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
```

to:

```python
def expected_id(artifact):
    """The id a file's location implies, or None where location does not fix it.

    Knowledge and Reference ids are fully determined by the path. A Skill's is
    not: `skills/human-interface-guidelines-components/` holds
    `skill.human-interface-guidelines.components`, so the directory encodes
    `<domain>` or `<domain>-<facet>` and only the domain segment is checkable.
    An ADR's filename leads with its zero-padded number
    (`0001-style-guide-scope.md`), which is the whole of its id (`adr.0001`).
    """
    if artifact.artifact_type == "knowledge":
        return f"knowledge.{artifact.path.parent.name}.{artifact.path.stem}"
    if artifact.artifact_type == "reference":
        return f"reference.apple.{artifact.path.stem}"
    if artifact.artifact_type == "adr":
        match = re.match(r"(\d+)-", artifact.path.stem)
        return f"adr.{match.group(1)}" if match else None
    return None
```

- [ ] **Step 3: Skip `adr` in `check_domain_matches_directory`**

Change (around line 284):

```python
    for artifact in artifacts:
        if artifact.artifact_type in ("workflow", "entry") or artifact.domain is None:
            continue
```

to:

```python
    for artifact in artifacts:
        if artifact.artifact_type in ("workflow", "entry", "adr") or artifact.domain is None:
            continue
```

(ADRs live flat in `docs/adr/`, never in a domain-named subdirectory — the same
reason `workflow`/`entry` are already skipped here. The docstring above this
function already says "Workflows and the entry point are not domain-scoped and
are skipped"; leave that sentence as-is, since amending it to also name `adr` is
optional prose polish, not required by any test.)

- [ ] **Step 4: Add the new bidirectional check function**

Add this function anywhere after `check_no_orphans` (a natural neighbor — both are
"reachable from somewhere" checks) and before the `CHECKS` list:

```python
def check_domain_map_adr_links(artifacts, root):
    """`domain-map.md`'s ADR column agrees with `docs/adr/`, both directions.

    Mirrors `check_wiki_links_resolve`/`check_no_orphans`'s shape for the `adr`
    type: a `domain-map.md` row's `[ADR-NNNN](...)` link must resolve to a real
    file, and every `docs/adr/*.md` file must be the target of exactly one such
    link. See `docs/specifications/adr-spec.md`.

    No-ops when `domain-map.md` doesn't exist. During incremental migration (see
    `docs/superpowers/plans/2026-09-10-adr-artifact-type.md`), only the ADRs
    that already have a matching table link are checked for orphanhood -- a
    `docs/adr/*.md` file created in the same commit as its table row stays
    green throughout, the same discipline
    `docs/specifications/skill-management.md` already requires when adding a
    Knowledge Contract to an existing Skill.
    """
    findings = []
    path = root / "docs" / "architecture" / "domain-map.md"
    if not path.exists():
        return findings
    text = path.read_text()

    linked = set()
    for match in re.finditer(r"\[ADR-\d+\]\(([^)]+)\)", text):
        target = (path.parent / match.group(1)).resolve()
        if not target.exists():
            findings.append(
                Finding(
                    2,
                    "domain-map-adr-link",
                    "docs/architecture/domain-map.md",
                    f"links `{match.group(1)}`, which does not exist",
                    "correct the path, or add the missing ADR",
                )
            )
            continue
        linked.add(target)

    adr_dir = root / "docs" / "adr"
    adr_files = {p.resolve() for p in adr_dir.glob("*.md")} if adr_dir.exists() else set()
    for orphan in sorted(adr_files - linked):
        findings.append(
            Finding(
                2,
                "domain-map-adr-link",
                orphan.relative_to(root).as_posix(),
                "no domain-map.md row links to this ADR",
                "add an `[ADR-NNNN](../adr/...)` link in the domain's table row",
            )
        )
    return findings
```

- [ ] **Step 5: Register the check**

Change `CHECKS` (around line 1099) to add the new function:

```python
CHECKS = [
    check_ids_unique,
    check_id_matches_path,
    check_domain_matches_directory,
    check_edges_resolve,
    check_no_edges_to_archived,
    check_wiki_links_resolve,
    check_prose_paths_resolve,
    check_prose_domain_mentions_resolve,
    check_used_by_is_complete,
    check_reference_indexes_citations,
    check_no_orphans,
    check_routing_index_sync,
    check_routing_keywords_unambiguous,
    check_dependency_direction,
    check_dependency_graph_is_acyclic,
    check_routing_coverage,
    check_workflows_compose_skills,
    check_scope_vocabulary,
    check_domain_map_adr_links,
]
```

- [ ] **Step 6: Run the new tests to verify they pass**

Run: `python3 -m unittest tests.test_validate_repo.TestAdrLinks -v`

Expected: `OK` — all 5 tests pass.

- [ ] **Step 7: Run the full `validate_repo.py` test suite**

Run: `python3 -m unittest tests.test_validate_repo -v`

Expected: `OK`. In particular re-check `TestFixtureIsValid.test_clean_repository_has_no_findings`
still passes — the base `RepoFixture` has no `docs/architecture/domain-map.md`,
so `check_domain_map_adr_links` must return `[]` for it (Step 4's `if not
path.exists(): return findings` handles this).

- [ ] **Step 8: Commit**

```bash
git add scripts/validate_repo.py tests/test_validate_repo.py
git commit -m "feat: add adr artifact type support to validate_repo.py"
```

---

### Task 9: Author `docs/adr/0001-style-guide-scope.md` — the first real ADR

**Files:**
- Create: `docs/adr/0001-style-guide-scope.md`

This is the worked example that proves the pipeline on real content, using
`style-guide` (Tier 1, the repository's first and simplest domain) as the subject.
Its `domain-map.md` row (Tier 1 table) reads exactly:

```
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style | UI copy wording, capitalization rules, punctuation, inclusive writing |
```

Its "Completed:" paragraph mention is minimal — literally just `` `style-guide`
(Tier 1) `` with no elaborating clause, unlike most later domains. Per
`adr-spec.md`'s Rules ("Where `domain-map.md` itself has no elaborating prose...
`## Context` MUST say so explicitly... and MAY instead cite that domain's own
design spec"), this ADR draws its `## Context` from that absence plus
`docs/superpowers/specs/2026-07-30-style-guide-domain-design.md`, which exists and
covers the domain's founding design.

- [ ] **Step 1: Read the cited design spec**

Run: `cat docs/superpowers/specs/2026-07-30-style-guide-domain-design.md` (or open
it) to pull its actual stated goal/scope for the `## Context` and `## Decision`
sections below — do not paraphrase from memory; quote or closely summarize what
that file actually says.

- [ ] **Step 2: Create `docs/adr/` and write the ADR**

````markdown
# ADR-0001: Apple Style Guide Domain Scope

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: adr.0001
artifact_type: adr
title: Apple Style Guide Domain Scope
version: 1.0.0
status: Approved
domain: Apple Style Guide
related: []
last_updated: 2026-09-10
```

## Context

`style-guide` was the repository's first domain (Tier 1) and predates the habit,
visible in later `domain-map.md` entries, of narrating each domain's founding
rationale inline: the "Completed:" paragraph's own mention of it is just
`` `style-guide` (Tier 1) ``, with no elaborating clause. The domain's actual
founding rationale lives in its own design spec,
`docs/superpowers/specs/2026-07-30-style-guide-domain-design.md`, written before
`domain-map.md`'s narrative-paragraph convention existed. [Fill in: one or two
sentences summarizing that design spec's stated goal, quoting or closely
paraphrasing it — see Step 1.]

## Decision

Scope `style-guide` to terminology, capitalization, punctuation, and writing style
— UI copy wording, capitalization rules, punctuation, and inclusive writing —
exactly as `domain-map.md`'s Tier 1 table row states today:

> Apple Style Guide | style-guide | Terminology, capitalization, punctuation,
> writing style | UI copy wording, capitalization rules, punctuation, inclusive
> writing

## Consequences

- Established the pattern every later Foundations-adjacent domain follows: UI
  *wording* is `style-guide`'s angle, UI *visual design* is
  `human-interface-guidelines`'s — see `domain-map.md`'s Cross-Domain Notes for
  the specific angle-split entries this enabled later (out of scope for this ADR
  to restate; cited there, not duplicated here per `adr-spec.md`'s no-duplication
  rule).
- No other domain existed yet at authoring time, so no boundary was contested at
  the time this scope was set.

## Verification Log

- 2026-09-10: initial scope recorded, migrated out of `domain-map.md`'s
  "Completed:" paragraph into this ADR per
  `docs/superpowers/specs/2026-09-10-adr-artifact-type-design.md`. No scope
  change — a format migration only.
````

Fill in the one bracketed placeholder in `## Context` from what Step 1's file
actually says before saving — this is the one piece of this task's content that
depends on reading a file this plan cannot inline (the design spec is dated
2026-07-30 and belongs to a different domain's history).

- [ ] **Step 3: Validate the new file alone**

Run: `python3 scripts/validate_artifact.py docs/adr/0001-style-guide-scope.md --type adr`

Expected: `PASS: docs/adr/0001-style-guide-scope.md`

---

### Task 10: Link ADR-0001 from `domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md:36`

- [ ] **Step 1: Add the ADR column to the style-guide row only**

This deliberately makes the Tier 1 table temporarily ragged (one 5-cell row among
ten 4-cell rows) — expected and acceptable for this plan's scope. Squaring up
every other row with its own ADR column is the follow-up plan's job (see the
handoff note at the end of this document); doing it here for one row without the
other 30 ADRs to link would mean inventing 29 empty cells with nothing real to put
in them, which is exactly the placeholder pattern this process avoids.

Change (line 36):

```
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style | UI copy wording, capitalization rules, punctuation, inclusive writing |
```

to:

```
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style | UI copy wording, capitalization rules, punctuation, inclusive writing | [ADR-0001](../adr/0001-style-guide-scope.md) |
```

- [ ] **Step 2: Commit**

```bash
git add docs/adr/0001-style-guide-scope.md docs/architecture/domain-map.md
git commit -m "docs: author ADR-0001 (style-guide) and link it from domain-map.md"
```

---

### Task 11: Full validation pass

**Files:** none (verification only)

- [ ] **Step 1: Level 1, every artifact**

Run: `python3 scripts/validate_artifact.py . --all`

Expected: the last line reads `N/N artifacts pass Level 1` where `N` is one more
than before this plan started (ADR-0001 is now a validated artifact).

- [ ] **Step 2: Levels 2-3, repository-wide**

Run: `python3 scripts/validate_repo.py .`

Expected: `PASS`, and the check count on the first line reads `19 checks` (was 18
— `check_domain_map_adr_links` is now registered).

- [ ] **Step 3: Lifecycle transitions**

Run: `python3 scripts/check_transitions.py .`

Expected: `PASS`. ADR-0001 is a new file going straight to `status: Approved`
with `version: 1.0.0` — same pattern every other artifact in this repository uses
on first authoring (see e.g. any Tier 2 Knowledge Contract's first commit), which
`check_transitions.py` accepts for files that don't exist on the base ref.

- [ ] **Step 4: Link freshness**

`docs/adr/0001-style-guide-scope.md` cites no external URL (its `## References`
section was deliberately omitted from this ADR's content since `adr-spec.md`
doesn't require one the way `knowledge-spec.md` does — an ADR cites
`domain-map.md`/a design spec, not an Apple documentation page). No
`check_links.py` run is needed for this file.

- [ ] **Step 5: Full unit test suite**

Run: `python3 -m unittest discover tests/ -v`

Expected: `OK`, every test passes, including all the new ones from Tasks 5 and 7.

---

### Task 12: `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add an entry under `[Unreleased]`**

```markdown
## [Unreleased]
### Added
- **New `adr` artifact type — Architecture Decision Records.** `docs/adr/`, validated like the other five artifact types (`docs/specifications/adr-spec.md`, `scripts/validate_artifact.py --type adr`, and a new `scripts/validate_repo.py` check that `domain-map.md`'s `ADR` column links agree with `docs/adr/`, both directions). Exists to stop `domain-map.md`'s "Completed:" paragraph from growing forever as one un-editable run-on sentence — see `docs/superpowers/specs/2026-09-10-adr-artifact-type-design.md` for the full design, informed by researching why the `mattpocock/skills` repo's own skill/agent system holds up (`docs/research/2026-09-mattpocock-skills-architecture.md`).
  - `ADR-0001` (`style-guide`) is the first real instance, proving the pipeline end-to-end. The other ~30 domains' scope history remains in `domain-map.md`'s paragraph for now — migrating them, and squaring up every Tier table's `ADR` column, is a follow-up plan. `## Cross-Domain Notes` is explicitly out of scope for this artifact type; see the design's Non-goals.
```

If `## [Unreleased]` already has content from other in-flight work on this branch,
add this as an additional bullet under its existing `### Added` heading rather
than duplicating the heading.

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: changelog entry for the new adr artifact type"
```

---

## Self-Review Notes

**Spec coverage** — every decision (D1-D7) in
`docs/superpowers/specs/2026-09-10-adr-artifact-type-design.md` maps to a task
here: D1 (phasing) is this plan's stated scope; D2 (location/validation rigor) is
Tasks 1-2, 5-8; D3 (template) is Task 2 and the fixture in Tasks 5/7; D4
(granularity) is stated in `adr-spec.md`'s Granularity section (Task 2) and
demonstrated by ADR-0001's `## Verification Log` shape (Task 9); D5
(`domain-map.md` structural change) is Task 10, deliberately partial per its own
note; D6 (numbering) is honored by ADR-0001 being `0001`; D7 (status reuse) is
`adr-spec.md`'s Status Semantics section. The full ~30-domain numbering scheme for
the follow-up plan is in the handoff note below rather than repeated per-task.

**Placeholder scan** — the only bracketed placeholder in this entire plan is the
one sentence in Task 9 that depends on reading
`docs/superpowers/specs/2026-07-30-style-guide-domain-design.md` fresh (a file
this plan cannot inline verbatim without risking a stale quote); Task 9 Step 1
exists specifically to resolve it before the file is saved, and Step 2's ADR body
is otherwise fully written out. No other task contains "TBD", "similar to Task
N", or an unshown code block.

**Type consistency** — `check_domain_map_adr_links`'s rule string
(`"domain-map-adr-link"`) is used identically in Task 8's implementation and
Task 7's tests. The ADR metadata shape (`id`, `artifact_type`, `title`, `version`,
`status`, `domain`, `related`, `last_updated`) is identical across the schema
table (Task 1), the spec (Task 2), the `validate_artifact.py` fixture (Task 5),
the `validate_repo.py` fixture (Task 7), and the real `ADR-0001` file (Task 9).

---

## Handoff note for the follow-up plan (bulk migration)

Not part of this plan's execution — recorded here so the next plan doesn't have
to re-derive it. Per design doc D6, numbering follows `domain-map.md`'s own
current row order: Tier 1 table, then Tier 2 table, then the two built Tier 3
pilots, then the retired `authentication` row last.

| # | Domain | Slug | Tier |
|---|---|---|---|
| 0001 | Apple Style Guide | style-guide | 1 (done, this plan) |
| 0002 | Human Interface Guidelines | human-interface-guidelines | 1 |
| 0003 | App Store Review Guidelines | app-store-review-guidelines | 1 |
| 0004 | SwiftUI | swiftui | 1 |
| 0005 | UIKit | uikit | 1 |
| 0006 | Accessibility | accessibility | 1 |
| 0007 | SF Symbols | sf-symbols | 1 |
| 0008 | Xcode | xcode | 1 |
| 0009 | Networking | networking | 1 |
| 0010 | Local Authentication | local-authentication | 1 |
| 0011 | App Tracking Transparency | app-tracking-transparency | 1 |
| 0012 | App Intents | app-intents | 2 |
| 0013 | WidgetKit | widgetkit | 2 |
| 0014 | UserNotifications | usernotifications | 2 |
| 0015 | BackgroundTasks | backgroundtasks | 2 |
| 0016 | Foundation | foundation | 2 |
| 0017 | Localization | localization | 2 |
| 0018 | Privacy | privacy | 2 |
| 0019 | AuthenticationServices | authenticationservices | 2 |
| 0020 | StoreKit | storekit | 2 |
| 0021 | Core Data | core-data | 2 |
| 0022 | SwiftData | swiftdata | 2 |
| 0023 | PassKit | passkit | 2 |
| 0024 | TipKit | tipkit | 2 |
| 0025 | Combine | combine | 2 |
| 0026 | EventKit | eventkit | 2 |
| 0027 | Testing | testing | 2 |
| 0028 | Security | security | 2 |
| 0029 | Photos | photos | 3 (built pilot) |
| 0030 | Core Location | core-location | 3 (built pilot) |
| 0031 | Authentication | authentication | Existing/Unscheduled, **Archived** (retired 2026-08-07) |

That plan's tasks should, per domain: extract the domain's clause from
`domain-map.md`'s "Completed:" paragraph (read it fresh — do not trust a cached
quote, since Tasks 1-11 of *this* plan do not modify that paragraph's text for any
domain but `style-guide`), write `docs/adr/<NNNN>-<slug>-scope.md`, and add that
row's `ADR` column link in the same commit — the discipline
`check_domain_map_adr_links` (Task 8) is built to require going forward. Once all
31 rows carry a real link, the paragraph itself can be deleted in full and
replaced with the one-sentence pointer the design doc's D5 specifies. Domain #31
(`authentication`) is the one `status: Archived` instance — its ADR's `## Decision`
should record what it originally covered and its `## Consequences`/
`## Verification Log` should record the 2026-08-07 retirement, matching how the
"Existing / Unscheduled Domains" table already treats it as a row that stays on
record rather than being erased.
