# Glossary

Status: Draft Version: 0.1.0

## Knowledge Contract

**Definition:** Atomic, enforceable rules for one problem. **Is:**
Implementation contract. **Is not:** Human documentation.

## Skill

**Definition:** Dispatcher that routes an agent to the required
knowledge. **Is:** Task entrypoint. **Is not:** Business logic or
documentation.

## Dispatcher

**Definition:** Component that selects required knowledge. **Is:**
Router. **Is not:** Knowledge source.

## Workflow

**Definition:** Multi-step composition of skills. **Is:** Process. **Is
not:** Single task.

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

**Definition:** Rules describing required relationships. **Is:**
Execution dependency. **Is not:** Documentation links.

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
