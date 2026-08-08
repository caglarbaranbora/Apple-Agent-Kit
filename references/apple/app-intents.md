# App Intents

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.app-intents
artifact_type: reference
title: App Intents
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's App Intents documentation, scoped to this domain's v1.
domain: App Intents
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/appintents
https://developer.apple.com/documentation/appintents/getting-started-with-the-app-intents-framework
https://developer.apple.com/documentation/appintents/appintent
https://developer.apple.com/documentation/appintents/adding-parameters-to-an-app-intent
https://developer.apple.com/documentation/appintents/intentparameter
https://developer.apple.com/documentation/appintents/appenum
https://developer.apple.com/documentation/appintents/parametersummary
https://developer.apple.com/documentation/appintents/defining-app-entities-for-your-custom-data-types
https://developer.apple.com/documentation/appintents/appentity
https://developer.apple.com/documentation/appintents/entityquery
https://developer.apple.com/documentation/appintents/entitystringquery
https://developer.apple.com/documentation/appintents/displayrepresentation
https://developer.apple.com/documentation/appintents/appshortcutsprovider
https://developer.apple.com/documentation/appintents/appshortcut
https://developer.apple.com/design/human-interface-guidelines/app-shortcuts
https://developer.apple.com/documentation/appintents/intentresult
https://developer.apple.com/documentation/appintents/returnsvalue
https://developer.apple.com/documentation/appintents/providesdialog
https://developer.apple.com/documentation/appintents/opensintent
https://developer.apple.com/documentation/appintents/liveactivityintent

## Purpose

Reference index for Apple's App Intents documentation, scoped to this domain's v1: declaring an app-specific action by conforming to the `AppIntent` protocol (`static var title: LocalizedStringResource`, `static var description: IntentDescription?`, `func perform() async throws -> Self.PerformResult`); declaring its inputs with the `@Parameter` property wrapper (documented under the symbol name `IntentParameter`), including optional-vs-required parameters, `AppEnum`-conforming custom enums for closed sets of values, and `parameterSummary`/`ParameterSummary` for the Shortcuts-app editor row; exposing app data via `AppEntity` conformance, an `EntityQuery` (or `EntityStringQuery` for free-text search) assigned to `defaultQuery`, `DisplayRepresentation` for how an entity reads aloud or on-screen, and system-driven disambiguation when a query resolves to more than one match; publishing `AppShortcut`s through a single `AppShortcutsProvider` conformance's `appShortcuts` static property, phrase-authoring rules (each phrase must include `\(.applicationName)`), and `updateAppShortcutParameters()`; and the `IntentResult` result-builder surface (`ReturnsValue`, `ProvidesDialog`, `OpensIntent`) returned from `perform()`.

Out of scope for v1: legacy `SiriKit` donation-based intents (`INIntent`, `NSUserActivity` donation); custom Siri vocabulary and `AppShortcutOptionsCollection`/negative-phrase authoring beyond basic phrase rules; Interactive Snippets and other visual intent-response UI customization beyond `ProvidesDialog`; Spotlight indexing/pinning of entities (`CSSearchableItem`, `IndexedEntity`); `LiveActivityIntent` as a distinct topic (it exists — an intent that starts, pauses, or modifies a Live Activity — but its specifics are deferred); and wiring an already-authored `AppIntent` into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)`, or anything inside a widget extension's `TimelineProvider`/`Timeline`, both owned by the `widgetkit` domain (see `knowledge/widgetkit/widget-interactivity-and-deep-links.md`) — this domain only covers authoring the intent itself.

## Primary Topics

- App intent declaration and parameters
- App entities and queries
- App Shortcuts and Siri phrases
- Intent results and widget hookup

## Used By

- knowledge/app-intents/app-intent-declaration-and-parameters.md ([[knowledge/app-intents/app-intent-declaration-and-parameters]])
- knowledge/app-intents/app-entities-and-queries.md ([[knowledge/app-intents/app-entities-and-queries]])
- knowledge/app-intents/app-shortcuts-and-siri-phrases.md ([[knowledge/app-intents/app-shortcuts-and-siri-phrases]])
- knowledge/app-intents/intent-results-and-widget-hookup.md ([[knowledge/app-intents/intent-results-and-widget-hookup]])
