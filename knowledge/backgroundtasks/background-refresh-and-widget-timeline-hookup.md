# Background Refresh and Widget Timeline Hookup

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.backgroundtasks.background-refresh-and-widget-timeline-hookup
artifact_type: knowledge
title: Background Refresh and Widget Timeline Hookup
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines scheduling a BGAppRefreshTaskRequest to refresh data a widget depends on, and the boundary that once the task's handler has fetched/updated that data, calling WidgetCenter.shared.reloadTimelines(ofKind:)/reloadAllTimelines() to trigger the widget refresh is widgetkit's territory.
domain: BackgroundTasks
tags:
  - backgroundtasks
  - widgetkit
  - bgapprefreshtaskrequest
  - widgetcenter
references:
  - https://developer.apple.com/documentation/backgroundtasks/bgapprefreshtaskrequest
  - https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/register(fortaskwithidentifier:using:launchhandler:)
  - https://developer.apple.com/documentation/backgroundtasks/bgtask/settaskcompleted(success:)
  - https://developer.apple.com/documentation/widgetkit/widgetcenter/reloadtimelines(ofkind:)
depends_on:
  - knowledge.backgroundtasks.background-task-registration-and-scheduling
  - knowledge.backgroundtasks.task-execution-and-expiration-handling
related:
  - knowledge.widgetkit.timeline-reloading-and-refresh-budget
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent schedules a `BGAppRefreshTaskRequest` specifically to refresh data a widget depends on, and closes a seam `widgetkit`'s `knowledge.widgetkit.timeline-reloading-and-refresh-budget` proactively deferred: this contract owns getting the background task registered, submitted, and run so fresh data actually lands; the moment that data has landed, calling `WidgetCenter.shared.reloadTimelines(ofKind:)`/`reloadAllTimelines()` — and everything about the refresh budget governing that call — belongs to `widgetkit`, not here.

## Scope

### Included

-   Scheduling a `BGAppRefreshTaskRequest` whose purpose is producing fresh data for a widget
-   The launch handler fetching/persisting that data before signaling completion
-   Re-submitting the next refresh request per `task-execution-and-expiration-handling`, applied to this widget-refresh use case
-   The exact hand-off point: the single call site where the handler, having landed new data, invokes WidgetKit's reload API

### Excluded

-   Everything about `WidgetCenter.reloadTimelines(ofKind:)`/`reloadAllTimelines()` beyond calling it — the refresh budget, its best-effort nature, and preferring future-dated timeline entries over frequent reloads are `widgetkit`'s rules (`knowledge.widgetkit.timeline-reloading-and-refresh-budget`), not restated here
-   Building the `TimelineProvider`/`Timeline`/`TimelineEntry` values the widget renders — `widgetkit`'s `timeline-provider-and-entries`
-   General registration/submission/`earliestBeginDate` mechanics and general `launchHandler`/`expirationHandler`/`setTaskCompleted(success:)` mechanics — see `background-task-registration-and-scheduling` and `task-execution-and-expiration-handling`; this contract applies them to the widget-refresh case, it doesn't re-derive them

## Rules

### Rule 1

Agents scheduling a background refresh for widget data MUST use `BGAppRefreshTaskRequest`, not `BGProcessingTaskRequest`, since keeping widget content current is the short, opportunistic refresh case, not deferrable heavy maintenance. Per Apple's documentation, `BGAppRefreshTaskRequest` is "A request to launch your app in the background to execute a short refresh task" — register and submit it per `background-task-registration-and-scheduling`'s Rules 1–5, scoped to this identifier.

### Rule 2

Agents MUST have the task's launch handler fetch and persist the widget's underlying data *before* calling WidgetKit's reload API, and MUST treat that reload call as the last step of this task's work, not a step this contract governs the mechanics of. Once new data has landed, `knowledge.widgetkit.timeline-reloading-and-refresh-budget`'s own Rule 1 already requires calling `reloadTimelines`/`reloadAllTimelines` "when data changes" — this contract's job ends at making that data change happen; agents MUST NOT restate or re-derive WidgetKit's refresh-budget reasoning here.

### Rule 3

Agents MUST call `task.setTaskCompleted(success:)` only after the widget's data fetch (and the resulting reload call) has actually finished, with `success` reflecting whether fresh data landed, and MUST re-submit the next `BGAppRefreshTaskRequest` per `task-execution-and-expiration-handling`'s Rule 4 so the widget continues to receive refresh opportunities — a one-off refresh that isn't re-scheduled leaves the widget stale after its first update.

### Rule 4

Agents MUST NOT call `WidgetCenter.shared.reloadTimelines(ofKind:)`/`reloadAllTimelines()` speculatively before the data fetch completes, and MUST NOT skip the call after data has landed on the assumption that WidgetKit will notice the change on its own — WidgetKit has no independent signal that app or server data changed; this contract's entire reason for existing is to make sure that signal gets sent once, at the right moment.

## Compliant Example

```swift
func handleWidgetDataRefresh(task: BGAppRefreshTask) {
    scheduleWidgetDataRefresh() // Rule 3: re-submit for the next occurrence.

    let operation = FetchWidgetDataOperation()
    task.expirationHandler = {
        operation.cancel()
    }
    operation.completionBlock = {
        if !operation.isCancelled {
            // Rule 2: reload only after new data has actually landed; the
            // budget/timing behind this call is widgetkit's territory.
            WidgetCenter.shared.reloadTimelines(ofKind: "com.example.app.status-widget")
        }
        task.setTaskCompleted(success: !operation.isCancelled) // Rule 3.
    }
    operationQueue.addOperation(operation)
}
```
Uses `BGAppRefreshTaskRequest`/`BGAppRefreshTask` for the widget-refresh case (Rule 1), calls `reloadTimelines(ofKind:)` only once the fetch operation has actually produced new data (Rules 2, 4), and reports completion while re-scheduling the next refresh (Rule 3).

## Non-Compliant Example

```swift
func handleWidgetDataRefresh(task: BGAppRefreshTask) {
    let operation = FetchWidgetDataOperation()
    // Reloads immediately, before the fetch has run -- violates Rules 2 and 4.
    WidgetCenter.shared.reloadTimelines(ofKind: "com.example.app.status-widget")

    operation.completionBlock = {
        task.setTaskCompleted(success: true)
    }
    operationQueue.addOperation(operation)
    // Never re-submits a request for the next refresh -- violates Rule 3;
    // the widget goes stale after this one update.
}
```
Calls `reloadTimelines(ofKind:)` before the data fetch has produced anything new (Rules 2, 4), and never re-submits the next `BGAppRefreshTaskRequest` (Rule 3), so the widget stops receiving fresh data after the first run.

## Dependencies

-   `knowledge.backgroundtasks.background-task-registration-and-scheduling` — registers and submits the `BGAppRefreshTaskRequest` this contract schedules.
-   `knowledge.backgroundtasks.task-execution-and-expiration-handling` — governs the general `expirationHandler`/`setTaskCompleted(success:)`/re-submission mechanics this contract applies to the widget-refresh case.
-   `knowledge.widgetkit.timeline-reloading-and-refresh-budget` — owns the `reloadTimelines`/`reloadAllTimelines` call this contract's handler makes once new data has landed, and every rule about the refresh budget governing it; not restated here.

## References

-   [Apple Developer — BGAppRefreshTaskRequest](https://developer.apple.com/documentation/backgroundtasks/bgapprefreshtaskrequest)
-   [Apple Developer — register(forTaskWithIdentifier:using:launchHandler:)](https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/register(fortaskwithidentifier:using:launchhandler:))
-   [Apple Developer — setTaskCompleted(success:)](https://developer.apple.com/documentation/backgroundtasks/bgtask/settaskcompleted(success:))
-   [Apple Developer — WidgetCenter.reloadTimelines(ofKind:)](https://developer.apple.com/documentation/widgetkit/widgetcenter/reloadtimelines(ofkind:))
