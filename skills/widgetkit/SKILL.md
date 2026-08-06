---
name: widgetkit
description: Route WidgetKit implementation tasks to the correct Knowledge Contracts -- widget declaration and families, timeline provider and entries, widget interactivity and deep links, and timeline reloading and refresh budget. Use when conforming to Widget, WidgetBundle, or WidgetConfiguration, choosing StaticConfiguration or AppIntentConfiguration, declaring supportedFamilies or reading widgetFamily, applying containerBackground, implementing TimelineProvider (placeholder, getSnapshot, getTimeline), building a Timeline of TimelineEntry values, choosing a TimelineReloadPolicy, wiring widgetURL, Link, Button(intent:), or Toggle(_:isOn:intent:), or calling WidgetCenter.reloadTimelines/reloadAllTimelines. v1 is home-screen/Lock-Screen widgets only -- no Live Activities/ActivityKit, no watchOS complications as a distinct surface, no Control Widgets (iOS 18 Controls/ControlWidget), no StandBy-specific layout. Triggers on WidgetKit, Widget, WidgetBundle, WidgetConfiguration, StaticConfiguration, AppIntentConfiguration, supportedFamilies, widgetFamily, containerBackground, TimelineProvider, TimelineEntry, Timeline, TimelineReloadPolicy, placeholder, getSnapshot, getTimeline, widgetURL, Link, Button(intent:), WidgetCenter, reloadTimelines, reloadAllTimelines.
id: skill.widgetkit.foundations
title: WidgetKit — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: WidgetKit
routes: [knowledge.widgetkit.widget-declaration-and-families, knowledge.widgetkit.timeline-provider-and-entries, knowledge.widgetkit.widget-interactivity-and-deep-links, knowledge.widgetkit.timeline-reloading-and-refresh-budget]
related: [knowledge.app-intents.intent-results-and-widget-hookup]
last_updated: 2026-08-06
---

# WidgetKit — Foundations Skill

## Purpose

Route WidgetKit implementation tasks to the minimum required WidgetKit
Knowledge Contracts. v1 scope is home-screen and Lock-Screen widgets
built with `Widget`/`WidgetConfiguration` and `TimelineProvider` only —
no Live Activities, no watchOS complications as a distinct surface, no
Control Widgets, no StandBy-specific layout.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/widgetkit/.

-   Conforming to `Widget`, `WidgetBundle`, or `WidgetConfiguration`; choosing `StaticConfiguration`/`AppIntentConfiguration`; declaring `supportedFamilies` or reading `@Environment(\.widgetFamily)`; applying `.containerBackground(for: .widget)`; or the `kind` string's stability -> widget-declaration-and-families.md
-   Implementing `TimelineProvider`'s `placeholder(in:)`, `getSnapshot(in:completion:)`, or `getTimeline(in:completion:)`; building a `Timeline` of `TimelineEntry` values; or choosing a `TimelineReloadPolicy` -> timeline-provider-and-entries.md
-   Wiring `widgetURL(_:)`, `Link`, `Button(intent:)`, or `Toggle(_:isOn:intent:)` into a widget's view -> widget-interactivity-and-deep-links.md
-   Calling `WidgetCenter.shared.reloadTimelines(ofKind:)`/`reloadAllTimelines()`, or reasoning about the refresh budget -> timeline-reloading-and-refresh-budget.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/widgetkit/ — do not guess or fall back to general
knowledge. Live Activities and `ActivityKit`, watchOS complications as a
distinct surface, Control Widgets (iOS 18 `Controls`/`ControlWidget`),
and StandBy-specific layout are deferred to future scope, not yet built
— report that explicitly rather than answering from general knowledge
(see docs/architecture/domain-map.md). Authoring an `AppIntent` itself —
its parameters, `perform()` body, and any entities it exposes — is
owned by `app-intents` (`knowledge.app-intents.intent-results-and-widget-hookup`),
not this one; this Skill only routes to wiring an already-authored
intent into a widget's tap target. Scheduling the background work that produces new
widget data (e.g. a `BGAppRefreshTask`) is owned by the future
`backgroundtasks` domain, not this one; this Skill only routes to the
`reloadTimelines`/`reloadAllTimelines` call site once new data has
already landed.
