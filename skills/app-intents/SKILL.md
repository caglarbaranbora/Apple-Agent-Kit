---
name: app-intents
description: Route App Intents implementation tasks to the correct Knowledge Contracts -- app intent declaration and parameters, app entities and queries, App Shortcuts and Siri phrases, and intent results. Use when conforming to AppIntent, declaring @Parameter, AppEnum, or parameterSummary, conforming to AppEntity or EntityQuery/EntityStringQuery, implementing displayRepresentation, conforming to AppShortcutsProvider or building an AppShortcut, authoring Siri phrases, or returning IntentResult/ReturnsValue/ProvidesDialog/OpensIntent from perform(). v1 is intent authoring only -- no legacy SiriKit (INIntent, NSUserActivity donation), no custom Siri vocabulary beyond basic phrase authoring, no Interactive Snippets, no Spotlight indexing of entities, no LiveActivityIntent specifics, and no wiring an already-authored intent into a widget's Button(intent:)/Toggle(_:isOn:intent:) -- that's widgetkit's job. Triggers on AppIntent, @Parameter, IntentParameter, AppEnum, ParameterSummary, AppEntity, EntityQuery, EntityStringQuery, DisplayRepresentation, AppShortcutsProvider, AppShortcut, applicationName, IntentResult, ReturnsValue, ProvidesDialog, OpensIntent, perform().
id: skill.app-intents.foundations
title: App Intents — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: App Intents
routes: [knowledge.app-intents.app-intent-declaration-and-parameters, knowledge.app-intents.app-entities-and-queries, knowledge.app-intents.app-shortcuts-and-siri-phrases, knowledge.app-intents.intent-results-and-widget-hookup]
related: [knowledge.widgetkit.widget-interactivity-and-deep-links]
last_updated: 2026-08-06
---

# App Intents — Foundations Skill

## Purpose

Route App Intents implementation tasks to the minimum required App
Intents Knowledge Contracts. v1 scope is authoring an `AppIntent` itself
-- its declaration, parameters, entities, Siri Shortcuts surface, and
result -- not legacy `SiriKit`, not custom Siri vocabulary beyond basic
phrase rules, not Interactive Snippets, not Spotlight indexing of
entities, and not `LiveActivityIntent` specifics.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-intents/.

-   Conforming to `AppIntent`; declaring `title`/`description`/`perform()`; declaring inputs with `@Parameter`/`IntentParameter`; restricting a parameter with an `AppEnum`; or implementing `parameterSummary`/`ParameterSummary` -> app-intent-declaration-and-parameters.md
-   Conforming to `AppEntity`; providing an `EntityQuery`/`EntityStringQuery` and assigning `defaultQuery`; implementing `displayRepresentation`; or reasoning about disambiguation when a query returns multiple matches -> app-entities-and-queries.md
-   Conforming to `AppShortcutsProvider`; building an `AppShortcut` (`shortTitle`, `systemImageName`); authoring Siri phrases (`\(.applicationName)`); or calling `updateAppShortcutParameters()` -> app-shortcuts-and-siri-phrases.md
-   Returning `IntentResult` from `perform()`; composing `ReturnsValue`/`ProvidesDialog`/`OpensIntent`; or authoring the `perform()` body of an intent destined for a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)` -> intent-results-and-widget-hookup.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-intents/ — do not guess or fall back to
general knowledge. Legacy `SiriKit` donation-based intents (`INIntent`,
`NSUserActivity` donation) are out of scope entirely -- superseded by
App Intents, not planned as a separate domain; report that explicitly.
Custom Siri vocabulary/`AppShortcutOptionsCollection` beyond basic
phrase authoring, Interactive Snippets and other visual intent-response
UI beyond `ProvidesDialog`, Spotlight indexing of entities, and
`LiveActivityIntent`'s specifics are deferred, not yet built (see
docs/architecture/domain-map.md). Wiring an already-authored `AppIntent`
into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)`, or anything
inside a widget extension's `TimelineProvider`/`Timeline`, is owned by
the `widgetkit` domain (`knowledge.widgetkit.widget-interactivity-and-deep-links`)
-- this Skill only routes to authoring the intent itself: its
declaration, parameters, entities, Shortcuts surface, and result.
