# Routing Model

Status: Draft Version: 0.1.0

## Purpose

Define how Skills deterministically route AI agents to the minimum set
of Knowledge Contracts required to complete a task.

## Routing Principles

-   Route before retrieval.
-   Retrieve the minimum sufficient context.
-   Never load unrelated knowledge.
-   Routing decisions must be deterministic.
-   Skills are responsible for routing, not reasoning.

## Routing Inputs

A Skill may use:

-   User task
-   Artifact metadata
-   Domain
-   Tags
-   Explicit dependencies

A Skill MUST NOT use:

-   Directory traversal
-   Similarity search without metadata constraints
-   Entire repository scans

## Routing Flow

1.  Receive task.
2.  Identify domain.
3.  Select matching Skill.
4.  Resolve required Knowledge Contracts.
5.  Resolve transitive dependencies.
6.  Remove duplicates.
7.  Return ordered artifact list.

## Resolution Rules

Priority:

1.  Explicit dependency (`depends_on`)
2.  Domain match
3.  Tag match
4.  Related artifacts (optional)

## Context Budget

Skills SHOULD return only the artifacts required for successful
implementation.

Adding unnecessary artifacts is considered a routing failure.

## Validation

A routing implementation MUST:

-   Produce deterministic output for identical input.
-   Respect dependency ordering.
-   Avoid circular dependency resolution.
-   Minimize retrieved artifacts.
-   Fail gracefully when required artifacts are missing.
