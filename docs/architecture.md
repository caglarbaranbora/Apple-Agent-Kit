# Architecture

Status: Approved
Version: 1.0.0

## Purpose

Define the architecture of Apple Agent Kit.

## Layers

1. **References**
   - External authoritative sources (Apple documentation).
   - Index of authority, not a source of rules.

2. **Knowledge Contracts**
   - Atomic implementation rules.
   - No orchestration.
   - No duplicated knowledge.

3. **Skills**
   - Dispatchers only.
   - Route a task to the minimum required Knowledge.
   - Never route to another Skill.

4. **Workflows**
   - Compose multiple Skills into end-to-end task execution.
   - No implementation rules of their own.

Four layers. `templates/` and `scripts/` are authoring and tooling directories, not
layers — nothing depends on them at runtime.

## Artifact Types

`knowledge`, `skill`, `reference`, `workflow`, `entry`, `template`, `spec`

`entry` is the plugin entry point (`skills/apple-agent-kit/SKILL.md`): the artifact
Claude Code discovers first, which points an agent at the Routing Index. It is not a
Skill and routes no Knowledge.

## Repository Structure

    docs/  knowledge/  skills/  workflows/  references/
    schemas/  templates/  scripts/  tests/  validation/  rfcs/

## Dependency Rules

These govern `depends_on`, the binding dependency edge. `related` is a non-binding
cross-reference and is outside them; `routes` is a Skill's load instruction and is a
separate category. See ../schemas/metadata.schema.md [[metadata.schema]].

**Allowed**

- Workflow → Skill
- Skill → Knowledge Contract
- Knowledge Contract → Knowledge Contract
- Knowledge Contract → Reference

**Forbidden**

- Knowledge → Skill
- Knowledge → Workflow
- Skill → Skill
- Skill → Reference
- Workflow → Knowledge (direct)
- Circular dependencies

A Skill's `related` may name another Skill, and 32 of 32 Skills do. That is not a
dependency and is not covered by the ban above.

## Architecture Principles

- Architecture changes require an RFC.
- Skills never own domain knowledge.
- Knowledge is atomic and reusable.
- Routing is deterministic.
- Dependencies are explicit.
- Context must be minimized.
- Repository is AI-agent optimized.

## Artifact Lifecycle

    Draft → Approved → Deprecated → Archived

See artifact-lifecycle.md [[artifact-lifecycle]].

## Validation

Five levels, defined in validation-model.md [[validation-model]]. Levels 1-3 are
mechanical and enforced by `scripts/`. Levels 4-5 are semantic and enforced by review.

## Exit Criteria

- Layer responsibilities are frozen.
- Dependency rules are frozen.
- Repository layout is frozen.
- Routing model is defined.
- Metadata schema references this architecture.
