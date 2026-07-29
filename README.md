# Apple Agent Kit

Status: Draft
Version: 0.1.0

## Overview

Apple Agent Kit is an open-source, spec-first knowledge system for AI coding agents developing Apple platform applications.

The project transforms official Apple documentation into small, atomic Knowledge Contracts that can be deterministically routed through Skills instead of relying on repository-wide semantic search.

## Goals

- Reduce token usage
- Improve routing accuracy
- Increase implementation consistency
- Preserve traceability to Apple documentation
- Scale to hundreds of reusable Knowledge Contracts

## Architecture

Apple Documentation
↓
References
↓
Knowledge Contracts
↓
Skills
↓
Workflows

## Repository Structure

- docs/
- references/
- knowledge/
- skills/
- workflows/
- templates/
- schemas/
- validation/
- tests/
- scripts/

## Quick Start

1. Read AGENTS.md.
2. Resolve the appropriate Skill.
3. Load only routed Knowledge Contracts.
4. Follow contract rules.
5. Never bypass routing.

## Current Status

- Phase 0 — Complete
- Phase 1 — Complete
- Phase 1.5 — Validation In Progress

## License

TBD
