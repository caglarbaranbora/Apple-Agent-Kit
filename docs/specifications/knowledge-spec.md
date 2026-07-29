# Knowledge Specification

Status: Draft
Version: 0.1.0

## Purpose

Defines the normative specification for every Knowledge Contract in Apple Agent Kit.

## Goals

- Atomic and reusable
- Deterministic
- Traceable to official Apple references
- Framework-agnostic unless implementation requires otherwise
- Optimized for AI coding agents

## Required Metadata

- id
- title
- version
- status
- artifact_type: knowledge
- domain
- depends_on
- related
- references
- last_updated

## Required Sections

1. Intent
2. Rules
3. Compliant Example
4. Non-compliant Example

## Rules

- One responsibility per Knowledge Contract.
- Do not embed workflow logic.
- Do not embed Skill routing.
- Do not duplicate rules from another contract.
- Every rule must be traceable to one or more Reference artifacts.
- Keep contracts concise and normative.

## Dependency Rules

- Dependencies must form a directed acyclic graph.
- Circular dependencies are prohibited.
- Dependencies must be explicit.

## References

Knowledge Contracts reference files under:

references/apple/

## Validation Checklist

- Metadata complete
- Atomic scope
- No duplicated rules
- References present
- Examples included
- Dependency graph valid
