# Skills Index

Status: Draft
Version: 0.1.0

## Purpose
Maps implementation tasks to the correct Skill.

## Discovery Rules

| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/login.md |

## Resolution Rules

1. Match the most specific task.
2. Load exactly one primary Skill.
3. The Skill routes Knowledge Contracts.
4. If no Skill matches, stop and report a missing Skill.
