# Vertical Slice #0003 — Single-Skill Routing

Date: 2026-08-08

## Objective

The positive control for slice #0002. Confirm that a task confined to one domain loads
one Skill and does not enter a Workflow, and measure how small the resulting context
actually is.

## Scope

Task:

> The error message on the upload screen reads "Invalid Entry." Fix it.

Chosen because it names no framework and no API. If routing depended on API-name
matching, this task would fail to route at all.

## Procedure

`AGENTS.md`'s Startup Procedure, followed literally.

## Expected Routing

    skills/index.md — Workflows table: no match
        ↓
    skills/index.md — Skills table
      row: "writing, terminology, capitalization, button label wording, …"
        ↓
    skills/style-guide/SKILL.md

## Observed Routing

The Workflows table was matched first and produced nothing — correct; none of the three
Workflows names a wording-only task. The Skills table matched one row.

`style-guide`'s own Routing section then matched one line — "App state, connectivity,
instructional voice" — loading three Contracts:

| Contract | `depends_on` |
|---|---|
| `knowledge.style-guide.app-state-and-error-terminology` | none |
| `knowledge.style-guide.instructional-voice-and-phrasing` | none |
| `knowledge.style-guide.connectivity-and-media-terminology` | none |

Three Contracts of 326, no dependency fan-out, no Workflow, no second Skill.

## Results

| Level 5 check | Result |
|---|---|
| Routing succeeds from task to Knowledge without repository search | **PASS** |
| The routed Knowledge is sufficient to complete the task | **PARTIAL** — see F-003-01 |
| Context is minimized | **PASS** — 3 of 326 |
| Architecture behaves as specified | **PASS** |

## Result

Overall Status: **PASS WITH ONE ARCHITECTURAL FINDING**

Routing is deterministic and the context is as small as the architecture promises: a
task with no API names in it still routed in two table lookups, which is the property
the Routing Index exists to provide. The finding is about what a single Skill can
answer, not about whether the right Skill was chosen.

See FINDINGS.md.
