# Artifact Lifecycle

Status: Approved
Version: 1.0.0

## Purpose

Define the lifecycle and state transitions for all repository artifacts.

## Scope

This lifecycle governs every artifact in the repository:

- Knowledge Contracts, Skills, References, Workflows, and the Entry
- Governance documents under `docs/`, `schemas/`, and `templates/`

Governance documents are artifacts. A specification that defines a frozen rule while
sitting in `Draft` has frozen nothing.

Three document classes are **outside** this lifecycle, because they record history
rather than state live rules:

- Design records and plans under `docs/superpowers/`
- Validation reports under `validation/`
- `README.md`'s `Status:` line, which reports product release maturity, not artifact
  state

## Lifecycle

    Draft → Approved → Deprecated → Archived

There is no `Review` state. Review happens in the pull request.

## States

### Draft

- Initial authoring.
- May change without compatibility guarantees.

### Approved

- Accepted as the current canonical artifact.
- Changes require review.
- Breaking architectural changes require an RFC.

### Deprecated

- Scheduled for replacement.
- New artifacts must not depend on it.
- Still present, so existing references resolve.

### Archived

- Retained for historical reference only.
- Must not be referenced by new artifacts.

## Allowed Transitions

- Draft → Approved
- Approved → Draft (reopened for revision)
- Approved → Deprecated
- Deprecated → Archived

## Versioning

- Draft changes MAY update patch versions.
- Approval establishes a stable version — `1.0.0` for a first approval, per
  naming-conventions.md [[naming-conventions]].
- Breaking architectural changes MUST increment the major version.
- Approval does not freeze an artifact. An Approved artifact that turns out to be wrong
  takes a normal version bump; that is what the lifecycle is for.

## Approval Gate

An artifact may be marked Approved only when:

- Validation Levels 1-3 pass. These are mechanical; see validation-model.md
  [[validation-model]].
- The Level 4-5 review checklist is complete. These are semantic and are checked by
  reading, not by a script.
- Review feedback is resolved.

## Validation

Validators MUST reject:

- Invalid state transitions.
- Approved artifacts with unresolved Level 1-3 failures.
- References to Archived artifacts.
- Any `status:` value outside the four states above.
