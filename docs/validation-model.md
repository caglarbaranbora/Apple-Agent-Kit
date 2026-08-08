# Validation Model

Status: Approved
Version: 1.3.0

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
- An `Approved` artifact is on a stable version (>= 1.0.0) — artifact-lifecycle.md
  [[artifact-lifecycle]] makes approval establish one, so `Approved 0.1.0` is
  approved in name only
- The prose `Status:`/`Version:` header agrees with the metadata block. Most artifacts
  carry both copies and nothing compared them until 2026-08-08; the promotion pass
  that writes both at once is exactly the edit that can leave them disagreeing.
  Skills have no header — absence is the convention there, not an omission

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
- No edge points at an `Archived` artifact. Archived is "retained for historical
  reference only"; the resolution check above proves an edge lands somewhere, not
  that where it landed is still current — see artifact-lifecycle.md
  [[artifact-lifecycle]]
- `skills/index.md` agrees with `skills/` and `workflows/` in both directions
- No Routing Index keyword names two different Skills. `AGENTS.md` tells an agent to
  "select exactly one Skill", which a keyword in two rows makes unexecutable. The two
  index checks above are about presence — that nothing is missing, that nothing is
  stranded — and ambiguity is a uniqueness property neither of them touches. Added
  after vertical slice #0004 found nine such keywords, every one a boundary
  `architecture/domain-map.md` had already resolved and the Index had not carried

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

A slice record is only evidence for the architecture it was run against. Slice #0001
was superseded on 2026-08-08 rather than merely aged: all five artifacts it tested had
been deleted with the `authentication` domain, so it could not support the approval it
was the only record for. Slices #0002-#0004 replaced it and found three defects — an
unowned rule between two correct Excluded lists, a two-domain task the Routing Index
cannot express, and nine ambiguous routing keywords — none of which Levels 1-4 are
shaped to see, because none of them sees a task.

------------------------------------------------------------------------

### Lifecycle Transitions — deliberately outside the levels

artifact-lifecycle.md [[artifact-lifecycle]] requires validators to reject invalid
state transitions. No working tree can decide that. A transition is a relationship
between two versions of a file, and Levels 1-3 are defined as offline *and*
deterministic — the same tree gives the same answer forever, which is what earns them
the right to block a commit. A check that reads history does not have that property.

It belongs where a transition actually exists: a pull request. This is the second
check outside the levels and it is outside for the same structural reason as the
first — its answer depends on something other than the tree in front of it.

Checks:

- Every `status` change between the base ref and the working tree is one of the four
  transitions artifact-lifecycle.md allows

Enforced by: `scripts/check_transitions.py`, run by `.github/workflows/ci.yml`

```bash
python3 scripts/check_transitions.py .                  # vs origin/main
python3 scripts/check_transitions.py . --base HEAD~1
```

Blocking: On a pull request. Nothing to compare on a push to `main` — the merge has
already happened.

------------------------------------------------------------------------

### Link Freshness — deliberately outside the levels

Repository-wide, and the only check here that leaves the machine.

Levels 1-3 are offline and deterministic: the same working tree gives the same
answer forever, which is exactly what earns them the right to block a commit. This
one asks another organisation's web server a question, so its answer can change
without this repository changing, and a network blip could fail a commit that is
perfectly correct. That is why it is a separate script on a separate schedule
rather than a seventeenth check in `validate_repo.py`.

It closes the half `check_reference_indexes_citations` structurally cannot. That
check proves a cited URL is *indexed*; nothing proved it *resolves*, and the two
are independent — a URL can be indexed by the right Reference, listed under the
right `## Used By`, and still be a 404.

Checks:

- Every cited URL returns a success status
- Every cited URL is the address Apple currently serves. A redirect is a finding,
  not a pass: Apple disambiguates a path whenever a name is both a type and a
  member or an overload set, and the undisambiguated form it redirects from is
  the address that later becomes a 404

Enforced by: `scripts/check_links.py`, run by `.github/workflows/links.yml`

```bash
python3 scripts/check_links.py .                   # every cited URL
python3 scripts/check_links.py . --files a.md b.md # only those files' URLs
```

Blocking: On a pull request, for the files that pull request changed. The weekly
full sweep reports rather than blocks — nothing is merging at 06:00 on a Monday,
and a red cron is a notification, not a gate.

Its first full run, 2026-08-08, found four defects in 739 cited URLs: two 404s and
two redirects, in four domains that had each passed every other level.

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
