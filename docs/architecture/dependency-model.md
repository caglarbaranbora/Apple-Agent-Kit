# Dependency Model

Status: Draft Version: 0.1.0

## Purpose

Define valid dependency relationships between repository artifacts and
establish rules for dependency validation.

## Dependency Graph

  Source               Target               Allowed
  -------------------- -------------------- -------------------
  Workflow             Skill                Yes
  Workflow             Template             Yes
  Skill                Knowledge Contract   Yes
  Skill                Template             Yes
  Knowledge Contract   Reference            Yes
  Specification        Specification        Yes
  Knowledge Contract   Knowledge Contract   Yes (if acyclic)
  Template             Template             Yes (if reusable)

## Forbidden Dependencies

  Source               Target
  -------------------- -----------------------------
  Knowledge Contract   Skill
  Knowledge Contract   Workflow
  Reference            Any internal artifact
  Skill                Skill
  Workflow             Knowledge Contract (direct)

## Cycle Rules

The dependency graph MUST remain acyclic.

Allowed: - Cross-reference through `related`

Forbidden: - Cyclic `depends_on` relationships

Example:

A -\> B -\> C

Valid

A -\> B -\> C -\> A

Invalid

## Dependency Types

### depends_on

Required for correct execution.

### related

Informational only.

### references

External authoritative sources.

### provides

Capabilities exposed by the artifact.

## Validation Rules

A validator MUST detect:

-   Circular dependencies
-   Missing dependency targets
-   Invalid dependency types
-   Duplicate IDs
-   Orphaned required artifacts

Validation failure blocks approval.

## Design Principles

-   Dependencies must be explicit.
-   Dependencies must be minimal.
-   Informational links are not dependencies.
-   Routing must not rely on implicit relationships.
