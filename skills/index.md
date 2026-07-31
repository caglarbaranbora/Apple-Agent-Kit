# Skills Index

Status: Draft
Version: 0.1.0

## Purpose
Maps implementation tasks to the correct Skill.

## Discovery Rules

| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/SKILL.md |
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/SKILL.md |
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |

## Resolution Rules

1. Match the most specific task.
2. Load exactly one primary Skill.
3. The Skill routes Knowledge Contracts.
4. If no Skill matches, stop and report a missing Skill.
