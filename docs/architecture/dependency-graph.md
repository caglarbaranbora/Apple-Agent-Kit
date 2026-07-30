# Dependency Graph

Status: Draft
Version: 0.1.0

## Purpose

Defines dependency rules between artifact types.

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
| Skill | Reference |
| Workflow | Knowledge |
| Knowledge | Workflow |

## Rules

- Dependency direction is one-way.
- Circular dependencies are prohibited.
- Cross-domain dependencies must be explicit.
- Every dependency must resolve to an existing artifact.

## Validation

- DAG verification
- Broken link detection
- Orphan artifact detection
- Dependency resolution
