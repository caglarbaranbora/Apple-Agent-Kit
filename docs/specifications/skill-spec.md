# Skill Specification

Status: Draft
Version: 0.2.0

## Purpose

Defines the normative specification for every Skill in Apple Agent Kit.

## Goals

- Deterministic routing
- Zero domain knowledge
- Minimal token consumption
- Reusable orchestration layer

## Frontmatter Format

Every Skill file is named `SKILL.md` and lives at `skills/<domain>/SKILL.md`
(or `skills/<domain>/<sub-skill>/SKILL.md` if a domain ever needs more than
one skill). Metadata is real YAML frontmatter — `---` at byte offset 0 of
the file, before any other content — not a fenced code block under a
heading. This is what the Claude Code skill loader parses for `name` and
`description`; both are required (see Required Metadata) so the skill is
independently discoverable and explicitly invocable as `/<domain>`.

Future Codex-specific behavior (if added) lives at
`skills/<domain>/agents/openai.yaml`, matching this same per-domain layout.
No such file exists yet — this is a reserved convention, not a current
requirement.

## Required Metadata

- name
- description
- id
- title
- version
- status
- artifact_type: skill
- domain
- routes
- related
- last_updated

## Required Sections

1. Purpose
2. Routing
3. Stop Conditions

An optional `Review Output Format` section (severity table + verdict) may
be added by any Skill whose task includes auditing existing text or code
against the domain's rules, not just routing implementation guidance. It is
not required for Skills that only route implementation Knowledge Contracts.

## Rules

- A Skill MUST NOT contain implementation guidance.
- A Skill MUST NOT duplicate Knowledge Contracts.
- A Skill routes Knowledge Contracts only.
- A Skill should load the minimum required artifacts.
- A Skill should resolve exactly one primary task.

## Size Limit

A Skill MUST NOT exceed 80 lines. If routing logic does not fit, split into multiple Skill files — never raise this limit.

## Routing Rules

- Routing must be explicit.
- Routing order must be deterministic.
- All routed artifacts must exist.
- Missing artifacts must stop execution.

## Validation Checklist

- Metadata complete
- No implementation knowledge
- Routing valid
- No circular routing
- Minimum artifact set
