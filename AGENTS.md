# AGENTS.md

This repository is designed for AI coding agents.

## Startup Procedure

1. Read this file.
2. Read README.md.
3. Resolve the correct Skill.
4. Load only routed Knowledge Contracts.
5. Execute the task.

## Rules

- Do not search the repository randomly.
- Do not load unrelated domains.
- Skills orchestrate.
- Knowledge defines implementation rules.
- Workflows compose multiple Skills.
- References are authoritative sources.
- If a dependency cannot be resolved, stop and report the issue.
- Prefer deterministic routing over semantic search.
- Load the minimum number of artifacts required.

## Layer Order

References
↓
Knowledge
↓
Skills
↓
Workflows

## Forbidden

- Embedding domain knowledge inside Skills.
- Duplicating Knowledge Contracts.
- Ignoring dependency rules.
- Skipping required contracts.

## Expected Behavior

Always explain:
- Which Skill was selected.
- Which Knowledge Contracts were loaded.
- Why each artifact was required.
