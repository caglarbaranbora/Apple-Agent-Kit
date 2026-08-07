# Metadata Schema

Status: Approved
Version: 1.0.0

## Purpose

Define the metadata contract for every repository artifact. This file is the
field-level authority: where a specification and this schema disagree about a field
name or whether a field is required, this file is wrong or that specification is —
they are never both right, and the disagreement is a release-blocking defect.

## Structure

Metadata is a common base plus a per-type extension. A type never redefines a base
field; it only adds.

### Common base

Required for every artifact type.

| Field | Description |
|---|---|
| `id` | Globally unique artifact identifier. Immutable. |
| `artifact_type` | One of the values in the type enum below. |
| `title` | Human-readable title. |
| `version` | Semantic version. |
| `status` | One of the values in the status enum below. |
| `last_updated` | ISO date the artifact last changed. |

### Per-type extension

| Type | Adds |
|---|---|
| `knowledge` | `domain`, `owner`, `summary`, `tags`, `depends_on`, `related`, `references` |
| `skill` | `domain`, `name`, `description`, `routes`, `related` |
| `reference` | `domain`, `owner`, `summary` |
| `workflow` | `skills`, `related` |
| `entry` | `name`, `description` |

`domain` is an extension field, not a base field, because two artifact types are not
domain-scoped. A `workflow` spans domains by definition — that is what makes it a
workflow rather than a skill. The `entry` artifact is the plugin's single entry point
and belongs to no domain.

`name` and `description` are what the Claude Code skill loader reads from YAML
frontmatter, which is why `skill` and `entry` carry them and the other types do not.

## Enums

### `artifact_type`

`knowledge`, `skill`, `reference`, `workflow`, `entry`, `template`, `spec`

### `status`

`Draft`, `Approved`, `Deprecated`, `Archived`

See ../docs/artifact-lifecycle.md [[artifact-lifecycle]] for the transitions between
them. There is no `Review` state — review happens in the pull request.

## Field semantics

Three fields express relationships between artifacts, and they are not
interchangeable. Confusing them makes every dependency rule unenforceable.

| Field | Meaning | Subject to graph rules |
|---|---|---|
| `depends_on` | The binding dependency edge. A depends_on B means A is incomplete without B. | **Yes** — direction bans, acyclicity, and resolution all apply here and only here. |
| `related` | Non-binding cross-reference. Points at adjacent material without requiring it. | No direction constraint. The target must exist. |
| `routes` | A Skill's load instruction: the Knowledge Contracts it directs an agent to. | Every id must exist. Not a dependency edge. |

A Skill's `related` may name another Skill. A Skill's `depends_on` may not — see
../docs/architecture/dependency-graph.md [[dependency-graph]].

`tags` is search and Obsidian metadata. It is **not** a routing input; see
../docs/architecture/routing-model.md [[routing-model]].

## Example

``` yaml
id: knowledge.localization.localized-string-apis
artifact_type: knowledge
title: Localized String APIs
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines which localized-string API to call and what each one resolves.
domain: Localization
tags:
  - localization
  - strings
references:
  - https://developer.apple.com/documentation/foundation/string/init(localized:table:bundle:locale:comment:)
depends_on:
  - knowledge.localization.string-catalogs-and-extraction
related:
  - knowledge.localization.plural-and-device-variations
last_updated: 2026-08-07
```

## Rules

- Every artifact MUST include the common base plus its type's extension.
- IDs MUST be immutable. An id is never changed for consistency or aesthetics; a
  renamed artifact keeps its id or is retired and replaced.
- Status changes MUST establish a version consistent with
  ../docs/artifact-lifecycle.md [[artifact-lifecycle]].
- `references` MUST point to official Apple sources.
- `depends_on` MUST remain acyclic.
- Unknown fields are permitted but unenforced. A field no specification requires
  carries no guarantee.
