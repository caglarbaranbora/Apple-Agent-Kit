# Widget Declaration and Families

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.widgetkit.widget-declaration-and-families
artifact_type: knowledge
title: Widget Declaration and Families
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines declaring a widget via the Widget protocol and a WidgetConfiguration, bundling multiple widgets with WidgetBundle, declaring supportedFamilies and adapting per widgetFamily, the containerBackground(for:) requirement, and kind-string stability.
domain: WidgetKit
tags:
  - widgetkit
  - widget
  - widgetbundle
  - widgetconfiguration
  - widgetfamily
references:
  - https://developer.apple.com/documentation/swiftui/widget
  - https://developer.apple.com/documentation/swiftui/widgetbundle
  - https://developer.apple.com/documentation/widgetkit/staticconfiguration
  - https://developer.apple.com/documentation/swiftui/widgetconfiguration/supportedfamilies(_:)
  - https://developer.apple.com/documentation/swiftui/environmentvalues/widgetfamily
  - https://developer.apple.com/documentation/swiftui/view/containerbackground(for:alignment:content:)
  - https://developer.apple.com/documentation/widgetkit/widgetinfo
depends_on: []
related:
  - knowledge.widgetkit.timeline-provider-and-entries
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent declares a single widget's type and shape — conforming to `Widget`, choosing a `WidgetConfiguration`, bundling multiple widgets, declaring the families it supports, adapting its view per family, and backgrounding its root view — the structural entry point into WidgetKit, before any timeline or interactivity concern applies.

## Scope

### Included

-   Declaring a widget by conforming to `Widget` with `body: some WidgetConfiguration`, choosing `StaticConfiguration` or `AppIntentConfiguration`
-   Bundling multiple widgets via `WidgetBundle`
-   Declaring `supportedFamilies` and adapting the view via `@Environment(\.widgetFamily)`
-   Backgrounding the root view via `.containerBackground(for: .widget)`
-   The stability requirement on a widget's `kind` string

### Excluded

-   `TimelineProvider` implementation and `TimelineEntry` shape — see `timeline-provider-and-entries`
-   `widgetURL`/`Link`/`Button(intent:)`/`Toggle(_:isOn:intent:)` interactivity — see `widget-interactivity-and-deep-links`
-   `WidgetCenter` reloads and the refresh budget — see `timeline-reloading-and-refresh-budget`
-   Live Activities (`ActivityKit`), watchOS complications, Control Widgets, StandBy — out of v1 scope; `AppIntent` authoring for `AppIntentConfiguration` — owned by the `app-intents` domain

## Rules

### Rule 1

Agents MUST declare a widget by conforming to the `Widget` protocol (`@MainActor @preconcurrency protocol Widget`) and providing a `body` of `some WidgetConfiguration` — either `StaticConfiguration` (no user-configurable options) or `AppIntentConfiguration` (configurable via an `AppIntent`) — and MUST NOT try to produce a widget by subclassing a view controller or any other non-`Widget` type. Mark the widget's type with `@main` so the compiler-generated `main()` entry point runs it.

### Rule 2

Agents MUST bundle multiple widgets from one extension by conforming to `WidgetBundle` (`@MainActor @preconcurrency protocol WidgetBundle`) and marking that bundle type `@main`, per Apple's documentation: "To support multiple types of widgets, add the `@main` attribute to a structure that conforms to `WidgetBundle`." Agents MUST NOT mark more than one `Widget` type `@main` in the same extension target.

### Rule 3

Agents MUST declare `supportedFamilies` explicitly via the `.supportedFamilies(_:)` modifier rather than relying on an implicit default, and MUST make the widget's view read `@Environment(\.widgetFamily)` — "Use this value to retrieve the widget size that the user chose for a widget" — and branch its layout per case. Agents MUST NOT write a single fixed layout that assumes one family; a widget can be placed in any family it declares support for.

### Rule 4

Agents MUST apply `.containerBackground(for: .widget) { ... }` to a widget's root view rather than a plain `.background(_:)`/color fill. Per Apple's documentation this modifier "differs from the `background` modifier by automatically filling an entire parent container," and the paired `containerBackgroundRemovable(_:)` modifier note states plainly this behavior "has no effect on operating system versions prior to iOS 17, watchOS 10, or macOS 14" — so a plain background bypasses the system's tinting and removable-background handling on iOS 17+.

### Rule 5

Agents MUST treat a widget's `kind` string (the `kind:` argument to `StaticConfiguration`/`AppIntentConfiguration`'s initializer) as a stable, unique identifier and MUST NOT change it once the widget has shipped. Per Apple's documentation, `kind` is "the string specified during creation of the widget's configuration," and that same string is how `WidgetInfo.kind` identifies a user's already-placed widget and how `WidgetCenter.reloadTimelines(ofKind:)` targets it — changing the string severs that identity link for widgets users have already added.

## Compliant Example

```swift
struct GameStatusWidget: Widget {
    let kind: String = "com.mygame.game-status" // Never changed after shipping.

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: GameStatusProvider()) { entry in
            GameStatusView(entry: entry)
        }
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct GameStatusView: View {
    @Environment(\.widgetFamily) var family
    var entry: GameStatusEntry

    var body: some View {
        Group {
            switch family {
            case .systemSmall: GameTurnSummary(entry.status)
            default: GameStatusDetail(entry.status)
            }
        }
        .containerBackground(for: .widget) { Color.gameBackground }
    }
}

@main
struct GameWidgets: WidgetBundle {
    var body: some Widget { GameStatusWidget() }
}
```
Conforms to `Widget` with a `StaticConfiguration` body (Rule 1), bundles via `WidgetBundle` under one `@main` (Rule 2), declares families and branches on `widgetFamily` (Rule 3), and backgrounds the root view with `containerBackground(for:)` (Rule 4). (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
@main
struct GameStatusWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "widget-\(UUID())", provider: GameStatusProvider()) { entry in
            GameStatusView(entry: entry)
                .background(Color.gameBackground) // Ignores system tinting/removable background.
        }
    }
}

@main // A second @main widget in the same extension.
struct GameLeaderboardWidget: Widget {
    var body: some WidgetConfiguration {
        // No supportedFamilies, no widgetFamily branching.
        StaticConfiguration(kind: "leaderboard", provider: LeaderboardProvider()) { LeaderboardView(entry: $0) }
    }
}
```
Generates a new `kind` on every launch instead of a stable string (Rule 5), declares two separate `@main` widgets instead of one `WidgetBundle` (Rule 2), uses `.background(_:)` instead of `.containerBackground(for:)` (Rule 4), and never declares or adapts to `supportedFamilies`/`widgetFamily` (Rule 3).

## Dependencies

None.

## References

-   [Apple Developer — Widget](https://developer.apple.com/documentation/swiftui/widget)
-   [Apple Developer — WidgetBundle](https://developer.apple.com/documentation/swiftui/widgetbundle)
-   [Apple Developer — StaticConfiguration](https://developer.apple.com/documentation/widgetkit/staticconfiguration)
-   [Apple Developer — WidgetConfiguration.supportedFamilies(_:)](https://developer.apple.com/documentation/swiftui/widgetconfiguration/supportedfamilies(_:))
-   [Apple Developer — EnvironmentValues.widgetFamily](https://developer.apple.com/documentation/swiftui/environmentvalues/widgetfamily)
-   [Apple Developer — View.containerBackground(for:alignment:content:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(for:alignment:content:))
-   [Apple Developer — WidgetInfo.kind](https://developer.apple.com/documentation/widgetkit/widgetinfo)
