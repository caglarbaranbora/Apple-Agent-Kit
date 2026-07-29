# Workflow Specification

Status: Draft
Version: 0.1.0

## Purpose

Defines the normative specification for every Workflow in Apple Agent Kit.

## Goals

- Compose multiple Skills into a deterministic execution flow.
- Keep orchestration separate from implementation knowledge.
- Minimize loaded artifacts through explicit routing.

## Required Metadata

- id
- title
- version
- status
- artifact_type: workflow
- skills
- related
- last_updated

## Required Sections

1. Purpose
2. Scope
3. Trigger Conditions
4. Skill Sequence
5. Exit Conditions

## Rules

- A Workflow MUST NOT contain implementation guidance.
- A Workflow MUST NOT contain Apple-specific rules.
- A Workflow orchestrates Skills only.
- Skills remain the single source of routing to Knowledge Contracts.
- A Workflow may invoke one or more Skills.
- Workflows should be reusable across projects.

## Composition Rules

- Skills execute in the declared order.
- Each Skill is independently responsible for Knowledge routing.
- A Workflow must stop if any Skill reports an unresolved dependency.
- Workflows must not bypass Skills to load Knowledge directly.

## Validation Checklist

- Metadata complete
- Skills exist
- Skill order deterministic
- No direct Knowledge routing
- Exit conditions defined
