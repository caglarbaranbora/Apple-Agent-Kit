# Workflows

Status: Draft
Version: 0.2.0

## Purpose

A Workflow composes multiple Skills into one deterministic task. It exists because a
real task — shipping an app, building a sign-in screen — spans domains, while a Skill
deliberately does not.

Composing Skills is a Workflow's job. A Skill never routes to another Skill.

## Contents

| Workflow | Shape | Skills |
|---|---|---|
| [authentication](authentication/WORKFLOW.md) | Fan-out across five domains | style-guide → accessibility → authenticationservices → local-authentication → security |
| [app-store-submission](app-store-submission/WORKFLOW.md) | Sequential and gated | app-store-review-guidelines → privacy → xcode |
| [add-widget](add-widget/WORKFLOW.md) | Three resolved hand-offs | widgetkit → app-intents → backgroundtasks |

The three shapes are deliberate. A Workflow spec fitted to one example would not have
survived the other two.

## Rules

- No domain knowledge, and no Apple-specific rules.
- Compose Skills only. A Workflow MUST NOT route Knowledge Contracts directly.
- At least two Skills. One Skill is a Skill.
- Skills load Knowledge Contracts; Knowledge defines implementation rules.

## Entry

A Workflow is never auto-discovered — Claude Code has no workflow primitive, and
nothing loads `WORKFLOW.md` on its own. Agents reach one through the Workflows table in
[../skills/index.md](../skills/index.md), the repository's single Routing Index, which
is matched ahead of the Skills table. A Workflow absent from that table is unreachable.

Normative shape: [../docs/specifications/workflow-spec.md](../docs/specifications/workflow-spec.md).
