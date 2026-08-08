# FINDINGS — Vertical Slice #0002

Date: 2026-08-08

## Result

Overall Status: PASS WITH ONE BLOCKING FINDING

Routing, context minimization, and the Workflow's conditional sequencing all behaved
as specified. One rule required by the task exists in neither domain.

------------------------------------------------------------------------

### F-002-01 The intent-to-timeline seam is unowned, and the general rule an agent lands on is wrong for it

Status: **Blocking** — fixed in this pull request

Observation:

An interactive widget's timeline reload is not stated anywhere in the kit, and the
rule an agent does reach gives the wrong answer for the interactive case.

`widgetkit`'s `widget-interactivity-and-deep-links` Rule 3 requires `Button(intent:)`
or `Toggle(_:isOn:intent:)`, and its Excluded list defers authoring the intent to
`app-intents`. `app-intents`' `intent-results-and-widget-hookup` Rule 5 requires
`perform()` to be fully implemented, and defers the widget-side wiring back to
`widgetkit`. Both are correct. Neither says what happens after `perform()` returns.

The agent then reaches `timeline-reloading-and-refresh-budget` Rule 1, which is
written for the general case:

> Agents MUST call `WidgetCenter.shared.reloadTimelines(ofKind:)` … whenever the data
> a widget depends on changes outside the provider's own predicted schedule

Checking off a task is such a change, so the rule as written directs the agent to call
`reloadTimelines` from inside `perform()`. Apple documents the opposite:

> When you return from the `perform()` function, the system reloads the widget's
> timeline using its timeline provider.

> Interactions with a toggle or button always guarantee a timeline reload.

The manual call is therefore redundant, and it is spent against the budget Rule 2 of
the same Contract describes as 40–70 reloads per day.

Apple also states an ordering requirement that no Contract carried:

> Make sure any code that's necessary for the timeline update runs before you return
> from `perform()`.

This is a correctness rule, not a refinement. An intent that starts asynchronous work
and returns before it lands renders the *previous* state — which for this task means
the widget shows the task still unchecked immediately after the person checked it.

Source: [Adding interactivity to widgets and Live Activities](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities)

Why no level caught it:

Levels 1–3 are satisfied — both Contracts exist, both ids resolve, both Excluded lists
name a real neighbour, and the `related` edges are reciprocal. Level 4 asks whether
Excluded sections "record real boundaries rather than assumed ones", and both do. The
defect is not that a boundary is wrong; it is that a rule falls in the gap between two
correct boundaries, which only a task crossing that gap can reveal.

Architectural action taken:

The rule is placed on the Contract whose own rule was wrong, not on the Contract that
merely names the control. `timeline-reloading-and-refresh-budget` Rule 1 gains the
carve-out and a new Rule 5 stating the automatic reload — Rule 1 is the rule that gave
the wrong answer, so fixing it anywhere else would have left it standing.
`intent-results-and-widget-hookup` Rule 5 gains the ordering requirement, since the
`perform()` body is that Contract's territory.

`widget-interactivity-and-deep-links` is deliberately left alone. It was the first
candidate — it is where `Button(intent:)` is required — but at 146 lines against the
150-line cap it had no room, and more importantly it owns *wiring* the control, not the
timeline. Both new rules cite Apple's page from a Contract in a different directory
than the one the Reference indexing it lives in, which `reference-spec.md`'s
many-to-many rule permits and `references/apple/widgetkit.md`'s `## Used By` now
records.

No Excluded list changes: the seam is assigned, not redrawn.

------------------------------------------------------------------------

### F-002-02 Reciprocal `related` edges did their job

Status: Passed

Observation:

The four `related` edges between `widgetkit` and `app-intents` all pointed at
Contracts already loaded by routing. `AGENTS.md` forbids following `related`
automatically, and nothing was lost by obeying it — the edges document adjacency for a
reader, and routing did not need them. This is the behaviour `related` is specified to
have, confirmed under a task that crosses the two domains it connects.
