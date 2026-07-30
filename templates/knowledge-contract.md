# Knowledge Contract Template

Status: Draft Version: 0.1.0

## Purpose

Defines the canonical structure for every Knowledge Contract in Apple
Agent Kit.

## Required Structure

### Metadata

Every contract MUST include:

``` yaml
id:
type: knowledge
title:
version:
status:
owner:
summary:
domain:
tags:
references:
depends_on:
related:
updated:
```

### Intent

Describe the single implementation problem this contract governs.

### Scope

Define what is included and explicitly excluded.

### Rules

Normative requirements using MUST, SHOULD and MAY.

Rules MUST: - Be atomic. - Be testable. - Avoid implementation unrelated
to the contract.

### Compliant Example

Provide a minimal example that follows every rule. When a contract has
multiple numbered rules, use one bullet per rule: `-   ✓ <example> (Rule N)`.

### Non-Compliant Example

Provide a minimal example that violates one or more rules and explain
why. When a contract has multiple numbered rules, use one bullet per rule:
`-   ✗ <example> (Rule N)`.

### Dependencies

List only required Knowledge Contracts. If none, write a plain `None.` —
no bullet.

### References

Reference authoritative Apple documentation.

## Authoring Rules

-   One contract solves one problem.
-   No duplicated rules.
-   No orchestration logic.
-   No workflow descriptions.
-   No skill behavior.
-   Optimize for AI agents.
-   Prefer concise, normative language.
-   Use official Apple terminology.

## Validation

A Knowledge Contract is valid only if all required sections are present.
