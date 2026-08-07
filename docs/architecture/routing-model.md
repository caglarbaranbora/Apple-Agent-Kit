# Routing Model

Status: Approved
Version: 1.0.0

## Purpose

Define how an agent is routed deterministically to the minimum set of artifacts a task
requires.

## Routing Principles

- Route before retrieval.
- Retrieve the minimum sufficient context.
- Never load unrelated knowledge.
- Routing decisions must be deterministic.
- Skills are responsible for routing, not reasoning.

## The Three Stages

Routing happens in three stages, each owned by a different layer.

### Stage 1 — The Routing Index selects one entry point

`skills/index.md` is the repository's single Routing Index. It holds two tables.

1. Match the task against the **Workflows** table first. A match loads that Workflow,
   which names its Skills in order.
2. Otherwise match the **Skills** table and load exactly one Skill.

A Workflow is never auto-discovered — Claude Code has no workflow primitive, so a
Workflow absent from this table is unreachable.

### Stage 2 — The Skill selects Knowledge Contracts

Each Skill's `## Routing` section maps task shape to Knowledge Contract ids. Routing is
explicit and ordered; a Contract listed in `routes:` but absent from `## Routing` is
unreachable and is a validation failure.

A Skill never routes to another Skill.

### Stage 3 — Each Contract pulls its own dependencies

Every Knowledge Contract carries a `## Dependencies` section and a `depends_on` field.
Transitive resolution lives here, in the Knowledge layer — not in the Skill layer.

This is why `## Dependencies` is a required section: it is the only mechanism by which
a Contract's prerequisites are loaded.

## Routing Inputs

A Skill may use:

- The user's task
- Artifact metadata
- Domain
- Explicit dependencies (`depends_on`)

A Skill MUST NOT use:

- Directory traversal
- Similarity search without metadata constraints
- Entire repository scans

`tags` is **not** a routing input. It is search and Obsidian metadata. Routing is keyed
on the Routing Index's trigger keywords and each Skill's `## Routing` section.

## Resolution Rules

1. Routing Index match — Workflow before Skill.
2. The selected Skill's `## Routing` entry for the task.
3. `depends_on` of every loaded Contract, resolved transitively.
4. Remove duplicates.

`related` is never followed automatically. It is a cross-reference offered to a reader,
not a load instruction.

## Context Budget

Skills return only the artifacts required for successful implementation.

Adding unnecessary artifacts is a routing failure, not a harmless extra.

## Failure

When no Routing Index row matches, or a routed artifact is missing, an agent MUST stop
and report the gap rather than fall back to searching the repository or to general
knowledge. Every Skill states this in its `## Stop Conditions`.

## Validation

- Routing produces deterministic output for identical input.
- Every routed id exists and appears in the Skill's `## Routing`.
- Every Workflow in `workflows/` has a Routing Index row.
- `depends_on` resolution is acyclic.

Enforced by `scripts/validate_repo.py`; see ../validation-model.md [[validation-model]].
