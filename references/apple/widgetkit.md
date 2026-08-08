# WidgetKit

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.widgetkit
artifact_type: reference
title: WidgetKit
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's WidgetKit documentation, scoped to this domain's v1.
domain: WidgetKit
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/swiftui/button/init(_:intent:)
https://developer.apple.com/documentation/swiftui/containerbackgroundplacement
https://developer.apple.com/documentation/swiftui/environmentvalues/widgetfamily
https://developer.apple.com/documentation/swiftui/link
https://developer.apple.com/documentation/swiftui/toggle/init(_:ison:intent:)
https://developer.apple.com/documentation/swiftui/view/containerbackground(for:alignment:content:)
https://developer.apple.com/documentation/swiftui/view/widgeturl(_:)
https://developer.apple.com/documentation/swiftui/widget
https://developer.apple.com/documentation/swiftui/widgetbundle
https://developer.apple.com/documentation/swiftui/widgetconfiguration
https://developer.apple.com/documentation/swiftui/widgetconfiguration/supportedfamilies(_:)
https://developer.apple.com/documentation/widgetkit
https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities
https://developer.apple.com/documentation/widgetkit/appintentconfiguration
https://developer.apple.com/documentation/widgetkit/creating-a-widget-extension
https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date
https://developer.apple.com/documentation/widgetkit/linking-to-specific-app-scenes-from-your-widget-or-live-activity
https://developer.apple.com/documentation/widgetkit/staticconfiguration
https://developer.apple.com/documentation/widgetkit/timeline
https://developer.apple.com/documentation/widgetkit/timelineentry
https://developer.apple.com/documentation/widgetkit/timelineprovider
https://developer.apple.com/documentation/widgetkit/timelineprovidercontext
https://developer.apple.com/documentation/widgetkit/timelinereloadpolicy
https://developer.apple.com/documentation/widgetkit/widgetcenter
https://developer.apple.com/documentation/widgetkit/widgetcenter/reloadtimelines(ofkind:)
https://developer.apple.com/documentation/widgetkit/widgetinfo

## Purpose

Reference index for Apple's WidgetKit documentation, scoped to this domain's v1: declaring a widget by conforming to the `Widget` protocol with a `body` of `some WidgetConfiguration` (`StaticConfiguration` or `AppIntentConfiguration`); bundling multiple widgets via `WidgetBundle`; declaring `supportedFamilies` and adapting per family via `@Environment(\.widgetFamily)`; the `.containerBackground(for: .widget)` requirement for a widget's root view; the stability requirement on a widget's `kind` string; the `TimelineProvider` triad of `placeholder(in:)`, `getSnapshot(in:completion:)`, and `getTimeline(in:completion:)`; building a `Timeline` of `TimelineEntry` values with a `TimelineReloadPolicy`; whole-widget navigation via `widgetURL(_:)` and per-region navigation via `Link`; wiring an already-authored `AppIntent` into `Button(intent:)`/`Toggle(_:isOn:intent:)` for in-place interactivity; and telling the system to re-invoke a provider via `WidgetCenter.shared.reloadTimelines(ofKind:)`/`reloadAllTimelines()`, including the system-managed, best-effort refresh budget that governs how often that request is actually honored.

Out of scope for v1: Live Activities and the `ActivityKit` framework; watchOS complications as a distinct surface (the shared WidgetKit/SwiftUI rendering pipeline is in scope only insofar as `Widget`/`WidgetConfiguration` apply — complication-specific families and the Smart Stack relevance API are not); Control Widgets (iOS 18 `Controls`/`ControlWidget`); StandBy-specific layout guidance; WidgetKit push notifications; server-side data-fetching mechanics inside a widget extension. Authoring the `AppIntent` itself — its parameters, `perform()` body, and any `AppEntity`/`AppEnumeration` types it exposes — is owned by `app-intents`; this domain only covers wiring an already-authored intent into a widget's `Button`/`Toggle`. There is no existing widget-design content in `swiftui` or `human-interface-guidelines` to hand off to or overlap with — widget-specific layout, font, and interaction guidance lives entirely in this domain for now. Scheduling the background work that produces new widget data (e.g. a `BGAppRefreshTask`) is owned by `backgroundtasks`; this domain only covers the `reloadTimelines`/`reloadAllTimelines` call site once new data has already landed.

## Primary Topics

- Widget declaration, families, and bundling
- Timeline providers and timeline entries
- Widget interactivity and deep links
- Timeline reloading and the refresh budget

## Used By

- knowledge/widgetkit/widget-declaration-and-families.md ([[knowledge/widgetkit/widget-declaration-and-families]])
- knowledge/widgetkit/timeline-provider-and-entries.md ([[knowledge/widgetkit/timeline-provider-and-entries]])
- knowledge/widgetkit/widget-interactivity-and-deep-links.md ([[knowledge/widgetkit/widget-interactivity-and-deep-links]])
- knowledge/widgetkit/timeline-reloading-and-refresh-budget.md ([[knowledge/widgetkit/timeline-reloading-and-refresh-budget]])
- knowledge/backgroundtasks/background-refresh-and-widget-timeline-hookup.md ([[knowledge/backgroundtasks/background-refresh-and-widget-timeline-hookup]])
- knowledge/app-intents/intent-results-and-widget-hookup.md ([[knowledge/app-intents/intent-results-and-widget-hookup]])
