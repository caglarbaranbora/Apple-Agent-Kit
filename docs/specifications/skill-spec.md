# Skill Specification

Status: Draft
Version: 0.1.0

## Purpose

Defines the normative specification for every Skill in Apple Agent Kit.

## Goals

- Deterministic routing
- Zero domain knowledge
- Minimal token consumption
- Reusable orchestration layer

## Required Metadata

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
2. Triggers
3. Routing
4. Stop Conditions

## Rules

- A Skill MUST NOT contain implementation guidance.
- A Skill MUST NOT duplicate Knowledge Contracts.
- A Skill routes Knowledge Contracts only.
- A Skill should load the minimum required artifacts.
- A Skill should resolve exactly one primary task.

## Size Limit

A Skill MUST NOT exceed 60 lines. If routing logic does not fit, split into multiple Skill files — never raise this limit.

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
