# Timeline Reloading and Refresh Budget

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.widgetkit.timeline-reloading-and-refresh-budget
artifact_type: knowledge
title: Timeline Reloading and Refresh Budget
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines calling WidgetCenter.shared.reloadTimelines(ofKind:)/reloadAllTimelines() when data changes, treating the system-managed refresh budget as best-effort, and preferring future-dated timeline entries over frequent reload requests.
domain: WidgetKit
tags:
  - widgetkit
  - widgetcenter
  - reloadtimelines
  - reloadalltimelines
  - refresh-budget
references:
  - https://developer.apple.com/documentation/widgetkit/widgetcenter
  - https://developer.apple.com/documentation/widgetkit/widgetcenter/reloadtimelines(ofkind:)
  - https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date
depends_on:
  - knowledge.widgetkit.timeline-provider-and-entries
related:
  - knowledge.backgroundtasks.background-refresh-and-widget-timeline-hookup
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent tells WidgetKit that a widget's underlying data has changed, and how it must reason about the system-managed refresh budget that governs when that request is actually honored — the mechanism that keeps an already-declared `TimelineProvider` (see `timeline-provider-and-entries`) showing current data between its own scheduled reloads.

## Scope

### Included

-   Calling `WidgetCenter.shared.reloadTimelines(ofKind:)`/`reloadAllTimelines()` when data changes
-   Understanding the refresh budget as a best-effort, system-managed allowance
-   Treating reload calls as requests, not guarantees
-   Preferring future-dated timeline entries over frequent reload calls
-   The hand-off point from a background data update to a reload call

### Excluded

-   Building the `Timeline`/`TimelineEntry` values themselves — see `timeline-provider-and-entries`
-   Declaring the `Widget`/`kind` being reloaded — see `widget-declaration-and-families`
-   Scheduling the background work that produces new data (e.g. `BGAppRefreshTask`) — owned by `backgroundtasks` (see `knowledge.backgroundtasks.background-refresh-and-widget-timeline-hookup`); this contract only covers the `reloadTimelines`/`reloadAllTimelines` call site once new data has already landed

## Rules

### Rule 1

Agents MUST call `WidgetCenter.shared.reloadTimelines(ofKind:)` (or `reloadAllTimelines()` for a `WidgetBundle` with multiple widget kinds) whenever the data a widget depends on changes outside the provider's own predicted schedule — for example, right after the app receives new data. Per Apple's documentation, one way to "keep its content up to date" is to "tell the system to reload all timelines when data changes; for example, when your app receives new data" — the system does not poll app or server state on its own; without this call it has no signal that a reload is warranted.

### Rule 2

Agents MUST treat the refresh budget as a best-effort, system-managed allowance, not a documented hard guarantee, and MUST NOT design a widget that assumes minute-level refresh cadence. Per Apple's documentation, "for a widget the user frequently views, a daily budget typically includes from 40 to 70 refreshes," which "roughly translates to widget reloads every 15 to 60 minutes, but it's common for these intervals to vary due to the many factors involved," and "WidgetKit imposes a minimum amount of time before it reloads a widget" — timeline entries should be spaced "at least about 5 minutes apart."

### Rule 3

Agents MUST treat every `reloadTimelines(ofKind:)`/`reloadAllTimelines()` call as a request whose actual re-invocation timing is system-determined, not a guarantee of immediate execution, and MUST NOT write app logic that assumes the provider runs synchronously right after the call returns. The budget allocation Apple describes is "dynamic and takes many factors into account," including how often the widget is visible and its last reload time — the same call can be honored quickly for one user and deferred for another.

### Rule 4

Agents MUST prefer scheduling a `Timeline` with several future-dated entries (see `timeline-provider-and-entries`) over issuing frequent `reloadTimelines()` calls when future content is predictable, since entries already inside a delivered timeline render on their scheduled dates without consuming the reload budget at all. Reserve `reloadTimelines`/`reloadAllTimelines` for changes the provider could not have predicted in advance. When the new data driving a reload arrives from background work (e.g. a `BGAppRefreshTask` or a push payload), call `reloadTimelines` at the point that data lands — the scheduling of that background work itself is owned by `backgroundtasks` (`knowledge.backgroundtasks.background-refresh-and-widget-timeline-hookup`).

## Compliant Example

```swift
// App target: called once new data has actually landed, not on a timer.
func didReceiveHealingPotion(for characterID: String) {
    store.applyHealingPotion(to: characterID)
    WidgetCenter.shared.reloadTimelines(ofKind: "com.mygame.character-detail")
}

// Provider: predictable recovery is expressed as future-dated entries instead
// of relying on repeated reloads.
struct GameStatusProvider: TimelineProvider {
    func getTimeline(in context: Context, completion: @escaping (Timeline<GameStatusEntry>) -> Void) {
        let now = Date()
        let entries = (0..<4).map { hour in
            GameStatusEntry(date: Calendar.current.date(byAdding: .hour, value: hour, to: now)!,
                             healthPercent: min(100, cachedHealthPercent + hour * 25))
        }
        completion(Timeline(entries: entries, policy: .atEnd))
    }
}
```
Calls `reloadTimelines(ofKind:)` only when an unpredicted event actually lands (Rules 1, 3), and expresses the predictable recovery curve as future-dated entries instead of polling for reloads (Rule 4).

## Non-Compliant Example

```swift
// Polls on a fixed timer and assumes the reload runs immediately every time.
Timer.scheduledTimer(withTimeInterval: 60, repeats: true) { _ in
    WidgetCenter.shared.reloadTimelines(ofKind: "com.mygame.character-detail")
    // Code here assumes the provider has already re-run and shown fresh data.
    updateAppBadge(from: latestKnownHealth)
}

struct GameStatusProvider: TimelineProvider {
    func getTimeline(in context: Context, completion: @escaping (Timeline<GameStatusEntry>) -> Void) {
        // Single "now" entry every time; relies entirely on external reloads.
        completion(Timeline(entries: [GameStatusEntry(date: Date(), healthPercent: cachedHealthPercent)], policy: .never))
    }
}
```
Requests a reload every 60 seconds assuming minute-level cadence, which the budget does not guarantee (Rule 2), treats the reload as if it executes synchronously (Rule 3), and pushes all freshness onto `reloadTimelines` instead of encoding the predictable recovery as future entries (Rule 4).

## Dependencies

-   `knowledge.widgetkit.timeline-provider-and-entries` — the `Timeline`/`TimelineEntry` values a reload causes the provider to regenerate are defined there; this contract only covers the reload call site.

## References

-   [Apple Developer — WidgetCenter](https://developer.apple.com/documentation/widgetkit/widgetcenter)
-   [Apple Developer — WidgetCenter.reloadTimelines(ofKind:)](https://developer.apple.com/documentation/widgetkit/widgetcenter/reloadtimelines(ofkind:))
-   [Apple Developer — Keeping a widget up to date](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date)
