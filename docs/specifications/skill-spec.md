# Skill Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the normative specification for every Skill in Apple Agent Kit.

A Skill routes a task to the minimum set of Knowledge Contracts it needs. It holds no
domain knowledge and no orchestration.

For a Skill's lifecycle — when one is created, how it grows, when it splits, how it is
retired — see skill-management.md [[skill-management]].

## Goals

- Deterministic routing
- Zero domain knowledge
- Minimal token consumption

## Location

    skills/<domain>[-<facet>]/SKILL.md

Always flat. Never nested. Claude Code derives a Skill's invocable name from its
directory name, so `skills/<domain>/<facet>/SKILL.md` would not be discoverable as
`/<domain>-<facet>`. No nested Skill exists in this repository.

Metadata is real YAML frontmatter — `---` at byte offset 0, before any other content —
not a fenced code block under a heading. This is what the Claude Code skill loader
parses for `name` and `description`.

Future Codex-specific behavior, if added, lives at `skills/<domain>/agents/openai.yaml`.
No such file exists yet; this is a reserved convention, not a requirement.

## Identity

The id is `skill.<domain>.<facet>`.

The facet is derivable from the directory name by stripping the domain prefix, and the
two MUST agree: `skills/swiftui-interaction/` carries `skill.swiftui.interaction`.

`foundations` is the default facet for a domain's primary Skill. It is not mandatory —
a more descriptive facet is valid where it reads better, as in `skill.style-guide.writing`
and `skill.app-store-review-guidelines.submission`. Ids are immutable
(../../schemas/metadata.schema.md [[metadata.schema]]), so an existing facet is never
renamed for consistency alone.

## Required Metadata

Common base: `id`, `artifact_type`, `title`, `version`, `status`, `last_updated`

Skill extension: `domain`, `name`, `description`, `routes`, `related`

`artifact_type` is `skill`.

## Required Sections

1. Purpose
2. Routing
3. Stop Conditions

An optional `Review Output Format` section (severity table plus verdict) may be added
by any Skill whose task includes auditing existing text or code against the domain's
rules, rather than only routing implementation guidance.

## Rules

- A Skill MUST NOT contain implementation guidance.
- A Skill MUST NOT duplicate Knowledge Contracts.
- A Skill routes Knowledge Contracts only. A Skill never routes to another Skill —
  composing Skills is a Workflow's job, see workflow-spec.md [[workflow-spec]].
- A Skill's `related` MAY name another Skill; its `depends_on` may not.
- A Skill should load the minimum required artifacts.
- Every id in `routes` MUST exist and MUST also appear in `## Routing`. A routed
  Contract with no routing line is unreachable.

## Splitting

A domain gets one Skill by default. It gets more on **topical coherence**: when its
Knowledge divides into task families that a single `## Routing` section cannot
discriminate cleanly.

Size is not the trigger. The 80-line cap below is a hard ceiling that has never bound —
the largest Skill in this repository is 56 lines. Procedure: skill-management.md.

## Size Limit

A Skill MUST NOT exceed 80 lines. If routing logic does not fit, split by topic —
never raise this limit.

## Routing Rules

- Routing must be explicit.
- Routing order must be deterministic.
- All routed artifacts must exist.
- Missing artifacts must stop execution and be reported.

## Validation Checklist

- Metadata complete and valid against the schema
- Directory layout flat; facet agrees with id
- No implementation knowledge
- Every routed id exists and appears in `## Routing`
- No routing to another Skill
- Minimum artifact set
