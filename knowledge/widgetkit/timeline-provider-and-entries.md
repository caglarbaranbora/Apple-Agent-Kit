# Timeline Provider and Entries

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.widgetkit.timeline-provider-and-entries
artifact_type: knowledge
title: Timeline Provider and Entries
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines implementing TimelineProvider's placeholder(in:), getSnapshot(in:completion:), and getTimeline(in:completion:), building a Timeline of TimelineEntry values with real future dates, and choosing a TimelineReloadPolicy.
domain: WidgetKit
tags:
  - widgetkit
  - timelineprovider
  - timelineentry
  - timeline
  - timelinereloadpolicy
references:
  - https://developer.apple.com/documentation/widgetkit/timelineprovider
  - https://developer.apple.com/documentation/widgetkit/timelineprovidercontext
  - https://developer.apple.com/documentation/widgetkit/timelineentry
  - https://developer.apple.com/documentation/widgetkit/timeline
  - https://developer.apple.com/documentation/widgetkit/timelinereloadpolicy
depends_on:
  - knowledge.widgetkit.widget-declaration-and-families
related:
  - knowledge.widgetkit.timeline-reloading-and-refresh-budget
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent implements a `TimelineProvider` — its three required methods, the `TimelineEntry` values it produces, and the `TimelineReloadPolicy` it chooses — the mechanism WidgetKit uses to decide what a widget shows and when to show it, applied uniformly whether the provider backs a `StaticConfiguration` or an `AppIntentConfiguration`.

## Scope

### Included

-   `placeholder(in:)` — synchronous, fast, no I/O
-   `getSnapshot(in:completion:)` — fast transient/gallery preview, `context.isPreview` handling
-   `getTimeline(in:completion:)` — real future-dated `TimelineEntry` values
-   Choosing a `TimelineReloadPolicy` (`.atEnd`, `.after(_:)`, `.never`)
-   The `TimelineEntry` protocol's `date: Date` requirement and entry content shape

### Excluded

-   Declaring the `Widget`/`WidgetConfiguration` that owns this provider — see `widget-declaration-and-families`
-   `widgetURL`/`Link`/`Button(intent:)`/`Toggle(_:isOn:intent:)` interactivity — see `widget-interactivity-and-deep-links`
-   `WidgetCenter.reloadTimelines`/`reloadAllTimelines` and the refresh budget — see `timeline-reloading-and-refresh-budget`
-   `AppIntentTimelineProvider`'s intent-specific parameter handling — owned by the `app-intents` domain

## Rules

### Rule 1

Agents MUST implement `placeholder(in:)` (`func placeholder(in: Self.Context) -> Self.Entry`) to return synchronously and fast, with no network or disk I/O. Per Apple's documentation, "WidgetKit calls `placeholder(in:)` to request an entry representing the widget's placeholder configuration," and this is what renders while the widget appears in the gallery before real data loads — any blocking work here delays that render.

### Rule 2

Agents MUST implement `getSnapshot(in:completion:)` (`func getSnapshot(in: Self.Context, completion: (Self.Entry) -> Void)`) to also return quickly, using cached or local data rather than a fresh network fetch. Per Apple's documentation, "WidgetKit calls `getSnapshot(in:completion:)` when the widget appears in transient situations," and "if `context.isPreview` is `true`, the widget appears in the widget gallery" — in that case call the completion "as quickly as possible, perhaps supplying sample data if it could take more than a few seconds to fetch or calculate the widget's current state." Agents MUST branch on `context.isPreview` rather than always attempting a real fetch.

### Rule 3

Agents MUST implement `getTimeline(in:completion:)` (`func getTimeline(in: Self.Context, completion: (Timeline<Self.Entry>) -> Void)`) to build a `Timeline` of one or more `TimelineEntry` values with real, distinct future dates — not every entry stamped `Date()`. Each entry's `date` is the point at which WidgetKit switches the displayed content to that entry; a timeline that never advances past "now" gives WidgetKit nothing to schedule against.

### Rule 4

Agents MUST choose a `TimelineReloadPolicy` (`.atEnd`, `.after(_:)`, or `.never`) that matches how predictable the widget's future content is, and MUST NOT default to `.never` out of convenience. `.atEnd` requests a new timeline once the last entry's date passes; `.after(_:)` requests one at a specific future date even if entries remain; `.never` stops WidgetKit from asking for a new timeline at all until the app explicitly reloads via `WidgetCenter` — appropriate only when nothing will change until an external signal arrives.

### Rule 5

Agents MUST make custom `TimelineEntry` types (conforming to the protocol's `date: Date` requirement) carry only the data the view needs to render that entry, and MUST NOT have the widget's view perform further async fetches — the view renders from an already-archived entry in a separate process, so any data the entry doesn't already carry simply isn't available at render time.

## Compliant Example

```swift
struct GameStatusEntry: TimelineEntry {
    let date: Date
    let healthPercent: Int // Everything the view needs; no further fetching.
}

struct GameStatusProvider: TimelineProvider {
    func placeholder(in context: Context) -> GameStatusEntry {
        GameStatusEntry(date: Date(), healthPercent: 100) // Synchronous, no I/O.
    }

    func getSnapshot(in context: Context, completion: @escaping (GameStatusEntry) -> Void) {
        if context.isPreview {
            completion(GameStatusEntry(date: Date(), healthPercent: 100)) // Fast sample data.
            return
        }
        completion(GameStatusEntry(date: Date(), healthPercent: cachedHealthPercent))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<GameStatusEntry>) -> Void) {
        let now = Date()
        let entries = (0..<4).map { hour in
            GameStatusEntry(date: Calendar.current.date(byAdding: .hour, value: hour, to: now)!,
                             healthPercent: min(100, cachedHealthPercent + hour * 25))
        }
        completion(Timeline(entries: entries, policy: .atEnd)) // Predictable recovery -> atEnd.
    }
}
```
Returns fast/synchronous placeholder data with no I/O (Rule 1), branches on `context.isPreview` in the snapshot (Rule 2), builds real future-dated entries (Rule 3), picks `.atEnd` because the recovery schedule is fully known (Rule 4), and carries only `healthPercent` on the entry (Rule 5). (Rules 1, 2, 3, 4, 5)

## Non-Compliant Example

```swift
struct GameStatusProvider: TimelineProvider {
    func placeholder(in context: Context) -> GameStatusEntry {
        let health = try! fetchHealthSynchronously() // Blocking network I/O.
        return GameStatusEntry(date: Date(), healthPercent: health)
    }

    func getSnapshot(in context: Context, completion: @escaping (GameStatusEntry) -> Void) {
        Task {
            let health = await fetchHealthFromServer() // Always a fresh fetch, ignores isPreview.
            completion(GameStatusEntry(date: Date(), healthPercent: health))
        }
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<GameStatusEntry>) -> Void) {
        let entry = GameStatusEntry(date: Date(), healthPercent: 50) // Single entry, stamped "now."
        completion(Timeline(entries: [entry], policy: .never)) // Blocks all future updates.
    }
}
```
Blocks on synchronous I/O in `placeholder(in:)` (Rule 1), always fetches fresh data in `getSnapshot` regardless of `context.isPreview` (Rule 2), builds a timeline with only a "now" entry (Rule 3), and defaults to `.never` even though health changes predictably over time (Rule 4).

## Dependencies

-   `knowledge.widgetkit.widget-declaration-and-families` — the `TimelineProvider` implemented here is the `provider:` argument to the `StaticConfiguration`/`AppIntentConfiguration` declared there.

## References

-   [Apple Developer — TimelineProvider](https://developer.apple.com/documentation/widgetkit/timelineprovider)
-   [Apple Developer — TimelineProviderContext](https://developer.apple.com/documentation/widgetkit/timelineprovidercontext)
-   [Apple Developer — TimelineEntry](https://developer.apple.com/documentation/widgetkit/timelineentry)
-   [Apple Developer — Timeline](https://developer.apple.com/documentation/widgetkit/timeline)
-   [Apple Developer — TimelineReloadPolicy](https://developer.apple.com/documentation/widgetkit/timelinereloadpolicy)
