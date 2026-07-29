# Artifact Lifecycle

Status: Draft Version: 0.1.0

## Purpose

Define the lifecycle and state transitions for all repository artifacts.

## Lifecycle

Draft → Review → Approved → Deprecated → Archived

## States

### Draft

-   Initial authoring.
-   May change without compatibility guarantees.

### Review

-   Under technical review.
-   Blocking issues must be resolved before approval.

### Approved

-   Accepted as the current canonical artifact.
-   Changes require review.
-   Breaking changes require an RFC if architectural.

### Deprecated

-   Scheduled for replacement.
-   New artifacts should not depend on it.

### Archived

-   Retained for historical reference only.
-   Must not be referenced by new artifacts.

## Allowed Transitions

-   Draft → Review
-   Review → Approved
-   Approved → Deprecated
-   Deprecated → Archived
-   Review → Draft (requested revisions)

## Versioning

-   Draft changes MAY update patch versions.
-   Approval SHOULD establish a stable version.
-   Breaking architectural changes MUST increment the major version.

## Approval Requirements

An artifact may be marked Approved only if:

-   Metadata is valid.
-   Dependencies resolve successfully.
-   Links validate successfully.
-   Required references exist.
-   Review feedback is resolved.

## Validation

Validators MUST reject:

-   Invalid state transitions.
-   Approved artifacts with unresolved validation errors.
-   References to Archived artifacts.
