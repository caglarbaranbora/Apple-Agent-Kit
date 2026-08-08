# Vertical Slice #0002 — Interactive Widget

Date: 2026-08-08

## Objective

Exercise the Workflow layer end to end. Phase 4 built Workflows, the Entry, and the
Routing Index; no slice had run against any of them. This slice is the first.

## Scope

Task:

> Add a widget that shows today's tasks and lets the user check one off without
> opening the app.

Chosen because it is the smallest task that requires a Workflow rather than a Skill:
it spans the widget surface, the intent behind the interaction, and the timeline that
has to reflect the result.

## Procedure

`AGENTS.md`'s Startup Procedure, followed literally and without repository search.

1. Read `AGENTS.md`, then `README.md`.
2. Resolve the task in `skills/index.md`, Workflows table first.
3. Load only what the matched artifact names.
4. Load each loaded Contract's declared `depends_on`.

## Expected Routing

    skills/index.md — Workflows table
      row: "add a widget, configurable widget, interactive widget, keep a widget up to date"
        ↓
    workflows/add-widget/WORKFLOW.md
        ↓
    1. skill.widgetkit.foundations       (always)
    2. skill.app-intents.foundations     (conditional — interactive, so required)
    3. skill.backgroundtasks.foundations (conditional — not required, see below)

## Observed Routing

The Workflows table matched on the first row tried. `WORKFLOW.md`'s Skill Sequence
made step 3 decidable from step 1: the check-off is user-initiated inside the widget
and the data lives in a container the extension can already read, so the condition
step 3 states — "the timeline needs data the widget extension cannot fetch itself" —
does not hold. Step 3 was correctly not loaded.

Contracts loaded, via each Skill's own Routing section:

| Contract | Loaded because |
|---|---|
| `knowledge.widgetkit.widget-declaration-and-families` | the `Widget` and its families |
| `knowledge.widgetkit.timeline-provider-and-entries` | today's tasks as timeline entries |
| `knowledge.widgetkit.widget-interactivity-and-deep-links` | the check-off control |
| `knowledge.widgetkit.timeline-reloading-and-refresh-budget` | reflecting the check-off |
| `knowledge.app-intents.intent-results-and-widget-hookup` | authoring the toggle's intent |
| `knowledge.app-intents.app-intent-declaration-and-parameters` | `depends_on` of the above |

Six Contracts of 326. No Contract was loaded that the task did not need, and no
`related` edge was followed — including the four reciprocal `related` edges between
the two domains, which named exactly the Contracts already loaded and would have been
harmless to follow and wrong to require.

## Results

| Level 5 check | Result |
|---|---|
| Routing succeeds from task to Knowledge without repository search | **PASS** |
| The routed Knowledge is sufficient to complete the task | **FAIL** — see F-002-01 |
| Context is minimized | **PASS** — 6 of 326, no unnecessary load |
| Architecture behaves as specified | **PASS** |

## Result

Overall Status: **PASS WITH ONE BLOCKING FINDING**

The Workflow layer behaves as designed on its first exercise: the Workflows table is
matched before the Skills table, a conditional step is decided by an earlier step
rather than by the agent guessing, and the two domains hand off through their Excluded
lists without either restating the other. What the slice found is a rule that exists
in neither domain because each Excluded list pushes it to the other.

See FINDINGS.md.
