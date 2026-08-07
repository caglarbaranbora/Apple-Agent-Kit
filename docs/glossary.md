# Glossary

Status: Approved
Version: 1.0.0

## Knowledge Contract

**Definition:** Atomic, enforceable rules for one problem. **Is:**
Implementation contract. **Is not:** Human documentation.

## Skill

**Definition:** Dispatcher that routes a task to the Knowledge it needs.
**Is:** Knowledge router. **Is not:** Business logic, documentation, or a
router of other Skills.

## Workflow

**Definition:** Multi-step composition of Skills. **Is:** Process
spanning domains. **Is not:** Single task, or a source of rules.

## Entry

**Definition:** The plugin entry point — the artifact Claude Code
discovers first, which points an agent at the Routing Index. **Is:**
Entry point. **Is not:** A Skill, or a router of Knowledge.

## Dispatcher

**Definition:** Component that selects required knowledge. **Is:**
Router. **Is not:** Knowledge source.

## Routing Index

**Definition:** `skills/index.md` — the single table mapping task
keywords to one Workflow or one Skill. **Is:** The only routing entry
point. **Is not:** A search index.

## Routing

**Definition:** Deterministic selection of dependencies. **Is:**
Resolution strategy. **Is not:** Search.

## Vertical Slice

**Definition:** End-to-end architectural validation. **Is:** Validation
exercise. **Is not:** Production implementation.

## Frozen Decision

**Definition:** Architectural decision requiring RFC to change. **Is:**
Stable contract. **Is not:** Temporary preference.

## Metadata Schema

**Definition:** Standard metadata for repository artifacts. **Is:**
Shared structure. **Is not:** Content.

## Linking Model

**Definition:** Rules for connecting artifacts. **Is:** Navigation
model. **Is not:** Dependency model.

## Dependency Model

**Definition:** Rules governing `depends_on`, the binding dependency
edge. **Is:** Execution dependency. **Is not:** `related`, which is a
non-binding cross-reference outside these rules, or `routes`, which is a
Skill's load instruction.

## Reference

**Definition:** Traceable link to an external authoritative source.
**Is:** Source attribution. **Is not:** Knowledge.

## Context Budget

**Definition:** Maximum useful context loaded for a task. **Is:**
Optimization target. **Is not:** Token limit.

## Tier

**Definition:** Priority rank (1, 2, or 3) assigned to a domain,
determining build order across [[domain-map]]. **Is:** Build-order
priority. **Is not:** Dependency relationship or architectural layer.
