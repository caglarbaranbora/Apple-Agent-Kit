# AGENTS.md

This repository is designed for AI coding agents.

## Startup Procedure

1. Read this file.
2. Read README.md.
3. Resolve the task in `skills/index.md`, the Routing Index. Match the Workflows table
   first; a match names the Skills to run in order. Otherwise match the Skills table
   and select exactly one Skill.
4. Load only the Knowledge Contracts that Skill routes to.
5. Load each loaded Contract's own declared dependencies.
6. Execute the task.

## Rules

- Do not search the repository randomly.
- Do not load unrelated domains.
- Skills route to Knowledge Contracts. A Skill never routes to another Skill.
- Workflows compose multiple Skills. Composing Skills is a Workflow's job, never a
  Skill's.
- Knowledge defines implementation rules.
- References are authoritative sources.
- A Knowledge Contract's `## Dependencies` section is binding — load what it names.
- `related` is a cross-reference, not a load instruction. Do not follow it
  automatically.
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
- Falling back to general knowledge when a Skill's Stop Conditions say to report a gap.

## Expected Behavior

Always explain:

- Which Workflow was selected, if any.
- Which Skill was selected.
- Which Knowledge Contracts were loaded.
- Why each artifact was required.
