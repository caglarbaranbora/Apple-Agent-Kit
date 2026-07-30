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

**Compact table format (20+ terms):** when a contract governs many
short, independent term-level rules (e.g. a glossary-derived terminology
list) and prose `### Rule N` subsections would exceed the line cap before
covering them all, use a markdown table instead: columns `| Term |
Correct Form | Notes |`, with 1-2 short prose paragraphs above the table
stating any rule that applies across the whole table. Cite table rows as
`(Rule N)` in row order for cross-referencing from the Example sections.
Only the two contract shapes below are valid — don't invent a third:
prose `### Rule N` (default, for contracts with few enough rules that
each earns its own explanation), or this compact table (for term-mapping
contracts where explaining each term at prose length wouldn't fit the cap).

### Compliant Example

Provide a minimal example that follows every rule. When a contract has
multiple numbered rules, use one bullet per rule: `-   ✓ <example> (Rule N)`.
For compact-table contracts, a representative subset (6-8 rows) is enough —
don't try to illustrate every row.

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
