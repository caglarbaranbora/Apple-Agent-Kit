# Linking Model

Status: Draft Version: 0.1.0

## Purpose

Define how artifacts reference each other throughout the repository.

## Goals

-   Deterministic navigation
-   Stable references
-   Low maintenance
-   Obsidian compatibility
-   Tool-agnostic parsing

## Link Types

### Relative Path (Canonical)

Use relative Markdown paths as the canonical linking mechanism.

Example:

``` md
See: ../knowledge/authentication/sign-in.md
```

### Wiki Link (Optional)

Wiki links MAY be included for Obsidian convenience.

Example:

``` md
[[knowledge/authentication/sign-in]]
```

Wiki links MUST mirror the canonical relative path.

## Rules

-   Relative paths are the source of truth.
-   Wiki links are optional and must never be the only reference.
-   Never reference artifacts by title alone.
-   Prefer linking by file rather than directory.
-   Broken links are validation failures.

## Resolution Order

1.  Relative path
2.  Wiki link
3.  Artifact ID (metadata lookup)

## Cross-Layer Linking

Allowed:

-   Skill → Knowledge
-   Workflow → Skill
-   Specification → Any specification
-   Knowledge → Reference

Forbidden:

-   Knowledge → Workflow
-   Knowledge → Skill
-   Circular navigation used as dependency

## Validation

A repository validator MUST report:

-   Missing targets
-   Broken relative paths
-   Invalid wiki links
-   Duplicate artifact IDs
-   Orphaned artifacts
