# Architecture

Status: Draft Version: 0.1.0

## Purpose

Define the immutable architecture of Apple Agent Kit.

## Layers

1.  References

-   External authoritative sources (Apple documentation).

2.  Knowledge Contracts

-   Atomic implementation rules.
-   No orchestration.
-   No duplicated knowledge.

3.  Skills

-   Dispatchers only.
-   Route tasks to the minimum required knowledge.

4.  Workflows

-   Compose multiple skills into end-to-end task execution.

5.  Templates

-   Reusable output formats and scaffolds.

## Repository Structure

docs/ knowledge/ skills/ workflows/ templates/ references/ schemas/
validation/ rfcs/

## Dependency Rules

Allowed: - Workflow -\> Skill - Skill -\> Knowledge Contract - Knowledge
Contract -\> Reference - Skill -\> Template

Forbidden: - Knowledge -\> Skill - Knowledge -\> Workflow - Skill -\>
Skill - Workflow -\> Knowledge (direct) - Circular dependencies

## Architecture Principles

-   Architecture changes require RFC.
-   Skills never own domain knowledge.
-   Knowledge is atomic and reusable.
-   Routing is deterministic.
-   Dependencies are explicit.
-   Context must be minimized.
-   Repository is AI-agent optimized.

## Artifact Lifecycle

Draft -\> Approved -\> Deprecated -\> Archived

## Validation

Architecture must pass a Vertical Slice before formal specification.

## Exit Criteria

-   Layer responsibilities are frozen.
-   Dependency rules are frozen.
-   Repository layout is frozen.
-   Routing model is defined.
-   Metadata schema references this architecture.
