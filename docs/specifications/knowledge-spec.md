# Knowledge Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the normative specification for every Knowledge Contract in Apple Agent Kit.

A Knowledge Contract states enforceable implementation rules for one atomic concept,
traceable to official Apple sources. It is not documentation, not orchestration, and
not routing.

## Goals

- Atomic and reusable
- Deterministic
- Traceable to official Apple references
- Framework-agnostic unless implementation requires otherwise
- Optimized for AI coding agents

## Location

    knowledge/<domain>/<slug>.md

The id is `knowledge.<domain>.<slug>` and MUST agree with the path. `domain` in the
metadata MUST agree with the directory name.

## Required Metadata

Common base (see ../../schemas/metadata.schema.md [[metadata.schema]]):
`id`, `artifact_type`, `title`, `version`, `status`, `last_updated`

Knowledge extension:
`domain`, `owner`, `summary`, `tags`, `depends_on`, `related`, `references`

`artifact_type` is `knowledge`.

## Required Sections

1. Intent
2. Rules
3. Compliant Example
4. Non-Compliant Example
5. Dependencies

`## Dependencies` is required because transitive resolution lives in this layer. A
Skill routes an agent to a Contract; the Contract itself declares what else must be
loaded with it. See ../architecture/routing-model.md [[routing-model]].

A `## Scope` section with `### Included` / `### Excluded` is conventional and strongly
recommended — an Excluded list is how a boundary with another domain is recorded
instead of being silently assumed.

## Rules

- One responsibility per Knowledge Contract.
- Do not embed orchestration logic. Sequencing multiple tasks is a Workflow's job.
- Do not embed Skill routing. A Contract never tells an agent which Contract to load
  next except through `depends_on` and its `## Dependencies` section.
- Do not duplicate rules from another contract. Cross-reference via `related` instead.
- Every rule MUST be traceable to one or more Reference artifacts, and the citation
  MUST be specific enough to authorize that rule.
- Keep contracts concise and normative.

## Dependency Rules

These apply to `depends_on` only. `related` is a non-binding cross-reference and is
outside them.

- Dependencies MUST form a directed acyclic graph.
- Circular dependencies are prohibited.
- Dependencies MUST be explicit and MUST resolve to an existing artifact.
- Knowledge MAY depend on Knowledge. Knowledge MUST NOT depend on a Skill, a
  Workflow, or an Entry.

## Size Limit

A Knowledge Contract MUST NOT exceed 150 lines. If a topic does not fit, split it into
another atomic contract — never raise this limit.

## References

Knowledge Contracts cite files under `references/apple/`. The domain Reference records
where a rule's authority comes from; see reference-spec.md [[reference-spec]].

## Validation Checklist

- Metadata complete and valid against the schema
- Path, id, and `domain` agree
- Atomic scope
- No duplicated rules
- Every rule traceable to a cited Apple source
- Examples included, both compliant and non-compliant
- `depends_on` graph valid and acyclic
