# Dependency Graph

Status: Approved
Version: 1.0.0

## Purpose

Defines dependency rules between artifact types.

## Scope

Both tables below govern **`depends_on` only** — the binding dependency edge.

Two other fields express relationships and are **not** covered here:

- `related` — non-binding cross-reference. No direction constraint. Its target must
  exist. A Skill's `related` may name another Skill, and 32 of 32 Skills do.
- `routes` — a Skill's Knowledge load instruction. Every id must exist, but this is
  not a dependency edge.

See ../../schemas/metadata.schema.md [[metadata.schema]].

## Allowed Dependencies

| From | To |
|---|---|
| Reference | — |
| Knowledge | Reference |
| Knowledge | Knowledge |
| Skill | Knowledge |
| Workflow | Skill |

## Forbidden Dependencies

| From | Forbidden |
|---|---|
| Reference | Knowledge, Skill, Workflow |
| Knowledge | Skill, Workflow |
| Skill | Skill, Reference |
| Workflow | Knowledge |

`Entry` has no dependencies. It points an agent at the Routing Index and carries no
`depends_on`, `routes`, or `related`.

## Rules

- Dependency direction is one-way.
- Circular dependencies are prohibited.
- Cross-domain dependencies must be explicit.
- Every dependency must resolve to an existing artifact.

## Validation

Enforced by `scripts/validate_repo.py` as Validation Level 3; see
../validation-model.md [[validation-model]].

- DAG verification over `depends_on`
- Broken link detection across all three relationship fields
- Orphan artifact detection
- Direction-rule enforcement against the tables above
