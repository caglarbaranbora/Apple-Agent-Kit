# Workflow Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the normative specification for every Workflow in Apple Agent Kit.

A Workflow composes multiple Skills into one deterministic task. It exists because a
real task — shipping an app, building a sign-in screen — spans domains, while a Skill
deliberately does not.

## Goals

- Compose multiple Skills into a deterministic execution order.
- Keep orchestration separate from implementation knowledge.
- Minimize loaded artifacts through explicit routing.

## Location

    workflows/<slug>/WORKFLOW.md

The id is `workflow.<slug>`. The slug names the task, not a domain — a Workflow that
maps one-to-one onto a single domain should be a Skill instead.

## Entry

A Workflow is never auto-discovered. Claude Code has no workflow primitive; nothing
loads `WORKFLOW.md` on its own.

An agent reaches a Workflow through the Workflows table in `skills/index.md`, which is
the repository's single Routing Index. Matching happens there first: if the task
matches a Workflow trigger, that Workflow is loaded and names its Skills in order;
otherwise exactly one Skill is loaded. See ../architecture/routing-model.md
[[routing-model]].

A Workflow that is not listed in `skills/index.md` is unreachable.

## Required Metadata

Common base (see ../../schemas/metadata.schema.md [[metadata.schema]]):
`id`, `artifact_type`, `title`, `version`, `status`, `last_updated`

Workflow extension: `skills`, `related`

`artifact_type` is `workflow`. There is no `domain` field — a Workflow spans domains by
definition, which is what distinguishes it from a Skill.

`skills` is the ordered list of Skill ids this Workflow composes.

## Required Sections

1. Purpose
2. Scope
3. Trigger Conditions
4. Skill Sequence
5. Exit Conditions

## Rules

- A Workflow MUST NOT contain implementation guidance.
- A Workflow MUST NOT contain Apple-specific rules.
- A Workflow orchestrates Skills only. It MUST NOT route Knowledge Contracts directly —
  Skills remain the single source of Knowledge routing.
- A Workflow MUST name at least two Skills. One Skill is a Skill.
- Every id in `skills` MUST exist and MUST appear in `## Skill Sequence`.

## Composition Rules

- Skills execute in the declared order.
- Each Skill is independently responsible for its own Knowledge routing.
- A Workflow must stop if any Skill reports an unresolved dependency.
- `## Exit Conditions` states what must hold for the Workflow to be complete, and what
  to report when it is not.

## Size Limit

A Workflow MUST NOT exceed 80 lines, matching Skills. A Workflow is pure routing; if
the sequence does not fit, the task is too broad to be one Workflow.

## Validation Checklist

- Metadata complete and valid against the schema
- All five sections present, in order
- Every id in `skills` exists and appears in `## Skill Sequence`
- At least two Skills named
- Listed in the Workflows table of `skills/index.md`
- No direct Knowledge routing
- Exit conditions defined
