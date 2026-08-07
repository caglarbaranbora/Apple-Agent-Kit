# Add Widget

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: workflow.add-widget
artifact_type: workflow
title: Add Widget
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Composes the widget surface, its user-configurable and interactive intents, and the background work that keeps its timeline fresh.
skills:
  - skill.widgetkit.foundations
  - skill.app-intents.foundations
  - skill.backgroundtasks.foundations
related: []
last_updated: 2026-08-07
```

## Purpose

Add a home-screen or lock-screen widget that is configurable, interactive, and kept up
to date. Three frameworks meet here, and `domain-map.md` has already resolved their
boundaries — this Workflow states the order in which they are applied.

## Scope

### Included

- Widget declaration, families, and timeline provider
- User configuration and in-widget interaction via App Intents
- Scheduled background refresh feeding the timeline

### Excluded

- Live Activities and ActivityKit — not built
- The host app's own UI — `skill.swiftui.foundations` or `skill.uikit.foundations`
- Push-driven widget reloads — `skill.usernotifications.foundations`

## Trigger Conditions

The task asks to add or change a widget whose content is configurable, interactive, or
refreshed on a schedule. A read-only static widget needs `skill.widgetkit.foundations`
alone and does not enter this Workflow.

Triggers: add a widget, configurable widget, interactive widget, widget refresh, keep
the widget up to date.

## Skill Sequence

1. `skill.widgetkit.foundations` — the widget itself: `Widget`, supported families,
   `TimelineProvider`, and the reload policy. The reload policy chosen here decides
   whether step 3 is needed at all.
2. `skill.app-intents.foundations` — only when the widget is user-configurable
   (`AppIntentConfiguration`) or interactive (`Button(intent:)`). The intent types are
   defined here and referenced back by the configuration declared in step 1.
3. `skill.backgroundtasks.foundations` — only when the timeline needs data the widget
   extension cannot fetch itself, requiring the host app to refresh it via
   `BGAppRefreshTask` and then call `WidgetCenter.reloadTimelines`.

Step 1 is always required. Steps 2 and 3 are conditional, and step 1 determines which.

## Exit Conditions

Complete when the widget builds and:

- Every supported family renders with a placeholder, a snapshot, and a timeline.
- Any configuration or interaction intent resolves without the host app being launched.
- Timeline reloads are requested by a policy or an explicit `WidgetCenter` call, never
  assumed to happen on their own.

Stop and report if any Skill reports an unresolved dependency, naming the Skill and the
missing Contract.
