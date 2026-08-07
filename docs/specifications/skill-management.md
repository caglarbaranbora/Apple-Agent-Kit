# Skill Management Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the lifecycle of a Skill: when one is created, how it is identified, what must
change when it grows, when it splits, and how it is retired.

skill-spec.md [[skill-spec]] defines a Skill's shape. This document defines its change
procedure.

## When a Skill Is Created

A domain gets exactly one Skill by default.

A domain gets more than one Skill on **topical coherence**: when its Knowledge divides
into task families that a single `## Routing` section cannot discriminate cleanly.

Size is not the trigger. The 80-line cap is a hard ceiling, and no Skill in this
repository has approached it — the largest is 56 lines while routing 12 Contracts, and
`style-guide` routes 25 Contracts in 44 lines.

Precedent:

- `human-interface-guidelines` splits three ways because Apple's own guidelines split
  three ways (Foundations, Components, Patterns), and one routing table cannot separate
  "check this screen's layout" from "which control do I use here".
- `swiftui` splits two ways because static composition and interaction are distinct
  task families reached by different tasks.

## Identity and Layout

Layout is always flat:

    skills/<domain>[-<facet>]/SKILL.md

Never nested. Claude Code derives the invocable Skill name from the directory name, so
a nested layout would not be discoverable.

The id is `skill.<domain>.<facet>`. The facet is derivable from the directory name by
stripping the domain prefix, and a validator checks the two agree.

`foundations` is the default facet for a domain's primary Skill. It is not mandatory —
`writing` and `submission` are valid where they describe the Skill better. Ids are
immutable (../../schemas/metadata.schema.md [[metadata.schema]]), so an existing facet
name is never changed for consistency alone.

## Adding a Knowledge Contract to an Existing Skill

Every one of these changes in the same commit:

1. The Knowledge Contract file itself.
2. The Skill's `routes:` list.
3. The Skill's `## Routing` section. A routed Contract with no routing line is
   unreachable.
4. The domain's Reference: add the Contract to `## Used By`, and add any new Apple
   source to `## Source`.
5. `skills/index.md`: add trigger keywords if the Contract introduces terms the
   existing row does not cover.
6. `docs/architecture/domain-map.md`: extend the domain's scope cell.
7. `CHANGELOG.md`.
8. `README.md` only when a Skill or domain is added — not for a Contract.

Items 2-5 are machine-checkable and are enforced by `scripts/validate_repo.py`.
Items 6-8 are prose and belong to the Level 4 review checklist
(../validation-model.md [[validation-model]]).

## Splitting a Skill

1. Confirm the trigger is topical, not size.
2. Create `skills/<domain>-<facet>/SKILL.md`.
3. Move the relevant ids out of the original Skill's `routes:` and `## Routing`.
   Knowledge Contracts do not move — `knowledge/<domain>/` stays one directory.
4. Give the new Skill its own Reference if its sources differ; otherwise both Skills
   may draw on the domain Reference.
5. Add a row to `skills/index.md` and partition the trigger keywords so the two rows do
   not collide.
6. Update `README.md`, `domain-map.md`, and `CHANGELOG.md`.

## Retiring a Skill

Retirement is the correct outcome when a Skill's Knowledge is owned by other domains
and its own value was routing rather than knowledge.

1. Set each retired Knowledge Contract's `status:` to `Deprecated`, then remove it once
   nothing references it. Never delete a Contract another artifact still names.
2. Relocate any Contract that belongs to another domain, correcting its `domain:` field
   and id. The id changes because the artifact is replaced, not renamed.
3. Remove the Skill's row from `skills/index.md`.
4. Resolve every `related:` reference to the retired Skill's id.
5. Record the retirement in `domain-map.md`. A retired domain stays in the record with
   its disposition; it is not erased.
6. If the routing value survives the Knowledge, replace the Skill with a Workflow.

## Relationship to Workflows

A Skill routes to Knowledge Contracts. It never routes to another Skill.

When a task genuinely spans domains, that is a Workflow, and the Workflow names the
Skills in order. A "Skill that dispatches to Skills" is a Workflow written in the wrong
layer.

`authentication` is the worked example. Its Knowledge was owned by `style-guide`
(sign-in terminology, button labels) and `accessibility` (form accessibility), and its
own foundational Contract encoded routing rules rather than implementation rules. The
Knowledge retires; the routing value becomes `workflows/authentication/`.

## Validation Checklist

- Directory layout flat; facet agrees with id
- Every routed id exists and appears in `## Routing`
- `skills/index.md` row present; trigger keywords do not collide with another row
- Reference `## Used By` complete
- No Skill routes to a Skill
- A retired Skill leaves no dangling `related:` reference
