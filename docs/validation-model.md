# Validation Model

Status: Approved
Version: 1.1.0

## Purpose

Define the validation requirements every artifact and architectural change must
satisfy before approval, and name what enforces each one.

A level with no named enforcement is an aspiration, not a gate.

## Validation Levels

### Level 1 — Structural

Per file.

Checks:

- Metadata schema compliance — required fields for the artifact's type
- Enum values valid — `artifact_type` and `status`
- Version format valid (semantic version)
- Required sections present
- Size limit respected
- `artifact_type` agrees with the artifact's location

Size limits:

| Artifact | Limit |
|---|---|
| Knowledge Contract | 150 lines |
| Skill | 80 lines |
| Workflow | 80 lines |
| Reference | 98 lines |

Enforced by: `scripts/validate_artifact.py`

```bash
python3 scripts/validate_artifact.py <path> --type knowledge   # one file
python3 scripts/validate_artifact.py . --all                   # every artifact
```

`--all` takes each file's type from its own `artifact_type` rather than from its
location, which is the only way `skills/apple-agent-kit/SKILL.md` is validated as the
entry point rather than as a Skill.

Blocking: Yes

------------------------------------------------------------------------

### Level 2 — Repository Integrity

Repository-wide.

Checks:

- Artifact ids are unique
- Ids agree with paths, and `domain` agrees with the directory
- Every metadata edge (`depends_on`, `related`, `routes`) resolves
- Every wiki link and relative path resolves
- Prose that names a `domain`, `skill`, or `workflow` names one that exists — a
  hand-off written in prose routes an agent exactly as far as one written in an
  edge field, so it is held to the same standard
- A Reference's `## Used By` lists every Contract that cites one of its `## Source`
  URLs — matched by URL, never by directory name, because Reference-to-Knowledge is
  many-to-many; see architecture/linking-model.md [[linking-model]]
- Every URL a Contract cites is indexed by some Reference's `## Source`. This is the
  forward half of the edge above, and without it that check is vacuous on any URL no
  Reference lists: it walks indexed URLs, so an unindexed one resolves to an empty
  list and is never examined at all
- No orphaned artifacts
- `skills/index.md` agrees with `skills/` and `workflows/` in both directions

Enforced by: `scripts/validate_repo.py`

```bash
python3 scripts/validate_repo.py .
```

Blocking: Yes

------------------------------------------------------------------------

### Level 3 — Architectural

Repository-wide.

Checks:

- Layer responsibilities respected
- Dependency direction rules respected, per architecture/dependency-graph.md
  [[dependency-graph]]
- `depends_on` graph is acyclic
- Routing rules respected — every routed id appears in the Skill's `## Routing`; no
  Skill routes to a Skill; every Workflow has a Routing Index row
- Every Workflow names at least two Skills — composing Skills is what a Workflow is for
- Scope statements use the vocabulary specifications/skill-spec.md [[skill-spec]]
  defines, and describe reality: a Skill may not call a domain that exists `future`
  or `unbuilt`, which would send an agent to general knowledge past Contracts that
  answer the question. The reality half also applies to a Reference's `## Purpose`,
  which states the same boundaries — the marker vocabulary itself stays a Skill rule,
  since a Reference has no `## Stop Conditions` to carry it
- No forbidden cross-layer references

Enforced by: `scripts/validate_repo.py`

Blocking: Yes

------------------------------------------------------------------------

Levels 1-3 are covered by `tests/test_validate_artifact.py` and
`tests/test_validate_repo.py`. Each test builds a fixture and breaks exactly one
thing, so a check that stops working fails a test rather than going quiet:

```bash
python3 -m unittest discover tests/
```

------------------------------------------------------------------------

### Level 4 — Domain

Semantic. Checked by reading, in review. No script can decide these, and a heuristic
implementation would produce noise that gets silenced.

Checks:

- Knowledge Contracts are atomic — one responsibility each
- No duplicated rules across contracts
- References point to authoritative sources, and each citation is specific enough to
  authorize the rule it backs. **URL shape does not prove specificity** — a hub page
  and a real framework landing page can sit at the same path depth.
- Skills contain no domain knowledge
- Excluded sections record real boundaries rather than assumed ones

Enforced by: review checklist

Blocking: Yes

------------------------------------------------------------------------

### Level 5 — Vertical Slice

End-to-end exercise, run against a real task rather than a file.

Checks:

- Routing succeeds from task to Knowledge without repository search
- The routed Knowledge is sufficient to complete the task
- Context is minimized — no artifact was loaded that the task did not need
- Architecture behaves as specified

Enforced by: review, recorded under `validation/slices/`

Blocking: Required before architecture approval.

## Validation Outcomes

**PASS** — the artifact satisfies the level.

**FAIL** — the artifact cannot progress to Approved.

**WARNING** — non-blocking recommendation. Does not prevent approval.

## Validator Responsibilities

A validator MUST report:

- Validation level
- Rule violated
- Artifact id or path
- Suggested remediation

## Approval Gate

An artifact may be approved only when:

- Levels 1-3 pass mechanically.
- The Level 4-5 checklist is complete.
- No critical architectural violations exist.
- Required reviews are complete.

See artifact-lifecycle.md [[artifact-lifecycle]].
