# Validation Model

Status: Draft Version: 0.1.0

## Purpose

Define the validation requirements that every artifact and architectural
change must satisfy before approval.

## Validation Levels

### Level 1 --- Structural

Checks:

-   Metadata schema compliance
-   Naming convention compliance
-   Valid lifecycle state
-   Required fields present

Size limits:

-   Knowledge Contract: 150 lines (see docs/specifications/knowledge-spec.md)
-   Skill: 60 lines (see docs/specifications/skill-spec.md)
-   Reference: 80 lines (no dedicated spec doc; limit defined here)

Blocking: Yes

------------------------------------------------------------------------

### Level 2 --- Repository Integrity

Checks:

-   Relative links resolve
-   Artifact IDs are unique
-   Dependency graph is acyclic
-   No orphaned required artifacts

Blocking: Yes

------------------------------------------------------------------------

### Level 3 --- Architectural

Checks:

-   Layer responsibilities respected
-   Dependency rules respected
-   Routing rules respected
-   No forbidden cross-layer references

Blocking: Yes

------------------------------------------------------------------------

### Level 4 --- Domain

Checks:

-   Knowledge contracts are atomic
-   No duplicated rules
-   References point to authoritative sources
-   Skills contain no domain knowledge

Blocking: Yes

------------------------------------------------------------------------

### Level 5 --- Vertical Slice

Checks:

-   End-to-end routing succeeds
-   Required knowledge is sufficient
-   Context is minimized
-   Architecture behaves as specified

Blocking: Required before architecture approval.

## Validation Outcomes

PASS

Artifact satisfies all validation levels.

FAIL

Artifact cannot progress to Approved.

WARNING

Non-blocking recommendation. Does not prevent approval.

## Validator Responsibilities

A validator MUST report:

-   Validation level
-   Rule violated
-   Artifact ID
-   Suggested remediation

## Approval Gate

An artifact may be approved only if:

-   All blocking validations pass.
-   No critical architectural violations exist.
-   Required reviews are complete.
