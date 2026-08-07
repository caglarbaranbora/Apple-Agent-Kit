# Tip Options and App Configuration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.tipkit.tip-options-and-app-configuration
artifact_type: knowledge
title: Tip Options and App Configuration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines calling Tips.configure(_:) once at app launch before any tip is evaluated (datastore location, display frequency), and setting per-tip Tip.Option values (MaxDisplayCount, MaxDisplayDuration, IgnoresDisplayFrequency) through a tip's options property.
domain: TipKit
tags:
  - tipkit
  - tips-configure
  - tip-options
  - display-frequency
  - app-launch
references:
  - https://developer.apple.com/documentation/tipkit/tips/configure(_:)
  - https://developer.apple.com/documentation/tipkit/tips/configurationoption/datastorelocation(_:)
  - https://developer.apple.com/documentation/tipkit/tips/configurationoption/displayfrequency(_:)
  - https://developer.apple.com/documentation/tipkit/tip/options
  - https://developer.apple.com/documentation/tipkit/tip/option
  - https://developer.apple.com/documentation/tipkit/tip/maxdisplaycount
  - https://developer.apple.com/documentation/tipkit/tip/maxdisplayduration
  - https://developer.apple.com/documentation/tipkit/tip/ignoresdisplayfrequency
  - https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit
depends_on:
  - knowledge.tipkit.tip-declaration-and-content
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines the two configuration surfaces an AI coding agent must get right for TipKit to work at all: the one-time, app-wide `Tips.configure(_:)` call that loads the tip datastore and sets a default display frequency, and the per-tip `options` property that overrides display-count, display-duration, and display-frequency behavior for an individual tip.

## Scope

### Included

-   Calling `Tips.configure(_:)` exactly once during app initialization, before any tip is evaluated or displayed
-   `Tips.ConfigurationOption.datastoreLocation(_:)` — the on-disk location of the tip datastore
-   `Tips.ConfigurationOption.displayFrequency(_:)` — the app-wide minimum spacing between two *different* tips' first appearances
-   Per-tip `Tip.Option`s set via `options: [any TipOption]`: `MaxDisplayCount`, `MaxDisplayDuration`, `IgnoresDisplayFrequency`

### Excluded

-   `title`/`message`/`image`/`actions` and the base `Tip` conformance shape — see `tip-declaration-and-content`
-   The `rules`/`#Rule(_:)` display-condition machinery — see `display-rules-and-event-triggers`
-   `Tips.ConfigurationOption.cloudKitContainer(_:)` and any cross-device sync of the datastore — out of scope for this domain's v1 (see `references/apple/tipkit.md`'s scope note)
-   Presenting the tip and invalidating it — see `presenting-tips-and-tip-groups`

## Rules

### Rule 1

Agents MUST call `Tips.configure(_:)` once, during app initialization, before any `Tip` is evaluated for display, and MUST NOT call it from a view's `body` or any per-screen code path. Per Apple's documentation, its declaration is `static func configure(_ configuration: [Tips.ConfigurationOption] = []) throws`, and "Call this function during app initialization... The best practice is to call this once per app session, for example, in the `init()` method of your app" (Apple's TipKit sample documentation). It `throws`, so agents MUST handle the error rather than call it with `try!` or ignore it silently.

### Rule 2

Agents needing a non-default on-disk location for the tip datastore MUST pass `Tips.ConfigurationOption.datastoreLocation(_:)` to `configure(_:)`, and MUST NOT assume the default location suits every case (e.g. a shared App Group container for a widget extension). Per Apple's documentation, "By default `.applicationDefault` is used on macOS, iOS, watchOS, and visionOS. On tvOS, `.applicationDefault` is used by default in conjunction with `NSUbiquitousKeyValueStore` to manage tip statuses."

### Rule 3

Agents wanting to change how often *new* tips appear relative to one another MUST pass `Tips.ConfigurationOption.displayFrequency(_:)` to `configure(_:)`, and MUST understand its scope is app-wide spacing between different tips, not a per-tip repeat-display limiter. Per Apple's documentation, "if display frequency is set to `.daily` and your [tip] is displayed, no new tips will be shown for at least 24 hours... Display frequency only applies to tips that have not appeared. Previously displayed tips will still appear if their display [rules] are satisfied." The default value for this option is `.immediate`.

### Rule 4

Agents needing a specific tip to ignore the app-wide display-frequency spacing MUST set `IgnoresDisplayFrequency()` in that tip's `options` property rather than lowering the app-wide `displayFrequency(_:)` for everyone. Per Apple's documentation, "Individual tips can override this behavior by specifying `IgnoresDisplayFrequency` in their `options`" — confirming this is the documented per-tip escape hatch, not a workaround.

### Rule 5

Agents limiting how many times or how long a tip may display MUST use `MaxDisplayCount(_:)` / `MaxDisplayDuration(_:)` in the tip's `options` property, not hand-rolled counters. Per Apple's documentation, `MaxDisplayCount` "specifies the maximum number of times a tip displays before the system automatically invalidates it," and `MaxDisplayDuration` "specifies the maximum amount of time a tip is displayed before it is invalidated" — both are built-in `Tip.Option` (`Tips.MaxDisplayCount`/`Tips.MaxDisplayDuration`) types, set through the `@Tips.OptionsBuilder`-backed `options: [any TipOption]` property.

## Compliant Example

```swift
import SwiftUI
import TipKit

@main
struct MyApp: App {
    init() {
        do {
            // Rule 1: called once, in App.init(), before any tip is shown.
            try Tips.configure([
                .datastoreLocation(.applicationDefault), // Rule 2
                .displayFrequency(.daily)                // Rule 3
            ])
        } catch {
            print("Error initializing TipKit: \(error)")
        }
    }
    var body: some Scene { WindowGroup { ContentView() } }
}

struct FavoriteFeatureTip: Tip {
    var title: Text { Text("Save as a Favorite") }

    var options: [Option] {
        MaxDisplayCount(1)        // Rule 5
        IgnoresDisplayFrequency() // Rule 4
    }
}
```

## Non-Compliant Example

```swift
import SwiftUI
import TipKit

struct ContentView: View {
    var body: some View {
        // Violates Rule 1: configure(_:) called from view code, not once at
        // app launch -- runs (and reloads the datastore) on every appearance.
        VStack { Text("Welcome") }
            .task { try? Tips.configure() } // also swallows the thrown error
    }
}

struct FavoriteFeatureTip: Tip {
    var title: Text { Text("Save as a Favorite") }
    // No MaxDisplayCount/MaxDisplayDuration and no IgnoresDisplayFrequency
    // override -- no per-tip escape hatch, violating Rules 4-5.
}
```
Calls `Tips.configure(_:)` from inside a view's body/`task` instead of once at app launch, and discards its thrown error (Rule 1); declares no display-count/duration or frequency-override options at all (Rules 4-5).

## Dependencies

-   `knowledge.tipkit.tip-declaration-and-content` — `options` is a property on the same `Tip`-conforming type whose `title`/`message`/`image` that contract defines.

## References

-   [Apple Developer — Tips.configure(_:)](https://developer.apple.com/documentation/tipkit/tips/configure(_:))
-   [Apple Developer — Tips.ConfigurationOption.datastoreLocation(_:)](https://developer.apple.com/documentation/tipkit/tips/configurationoption/datastorelocation(_:))
-   [Apple Developer — Tips.ConfigurationOption.displayFrequency(_:)](https://developer.apple.com/documentation/tipkit/tips/configurationoption/displayfrequency(_:))
-   [Apple Developer — Tip.options](https://developer.apple.com/documentation/tipkit/tip/options)
-   [Apple Developer — Tip.Option](https://developer.apple.com/documentation/tipkit/tip/option)
-   [Apple Developer — Tip.MaxDisplayCount](https://developer.apple.com/documentation/tipkit/tip/maxdisplaycount)
-   [Apple Developer — Tip.MaxDisplayDuration](https://developer.apple.com/documentation/tipkit/tip/maxdisplayduration)
-   [Apple Developer — Tip.IgnoresDisplayFrequency](https://developer.apple.com/documentation/tipkit/tip/ignoresdisplayfrequency)
-   [Apple Developer — Highlighting app features with TipKit](https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit)
