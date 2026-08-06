# BackgroundTasks

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/backgroundtasks
https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler
https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/register(fortaskwithidentifier:using:launchhandler:)
https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/submit(_:)
https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/cancel(taskrequestwithidentifier:)
https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/cancelalltaskrequests()
https://developer.apple.com/documentation/backgroundtasks/bgtaskrequest
https://developer.apple.com/documentation/backgroundtasks/bgtaskrequest/earliestbegindate
https://developer.apple.com/documentation/backgroundtasks/bgapprefreshtaskrequest
https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest
https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest/requiresnetworkconnectivity
https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest/requiresexternalpower
https://developer.apple.com/documentation/backgroundtasks/bgtask
https://developer.apple.com/documentation/backgroundtasks/bgtask/expirationhandler
https://developer.apple.com/documentation/backgroundtasks/bgtask/settaskcompleted(success:)
https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app
https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app
https://developer.apple.com/documentation/bundleresources/information-property-list/bgtaskschedulerpermittedidentifiers

## Purpose

Reference index for Apple's BackgroundTasks documentation, scoped to this domain's v1: registering a task identifier before the app finishes launching with `BGTaskScheduler.shared.register(forTaskWithIdentifier:using:launchHandler:)`, declaring every identifier the app will submit in Info.plist under `BGTaskSchedulerPermittedIdentifiers`, submitting and cancelling requests with `submit(_:)`/`cancel(taskRequestWithIdentifier:)`/`cancelAllTaskRequests()`, choosing between the two `BGTaskRequest` subclasses `BGAppRefreshTaskRequest` (short, opportunistic refresh) and `BGProcessingTaskRequest` (longer-running maintenance work), treating `earliestBeginDate` as a hint rather than a guarantee; the `launchHandler`'s `BGTask` (cast to the concrete `BGAppRefreshTask`/`BGProcessingTask` subclass), `expirationHandler`, and calling `setTaskCompleted(success:)` exactly once, including re-submitting a request for the next occurrence when work should repeat; `BGProcessingTaskRequest`'s `requiresNetworkConnectivity`/`requiresExternalPower` constraints; and the hand-off point where background-refreshed data feeds a widget via WidgetKit's `reloadTimelines`/`reloadAllTimelines`.

Out of scope for v1: `BGContinuedProcessingTask` (foreground-initiated work that can continue running in the background — newer API surface, deferred); legacy Background Fetch (`UIApplication.setMinimumBackgroundFetchInterval`, `application(_:performFetchWithCompletionHandler:)` — pre-iOS 13, superseded by this framework); other background modes unrelated to `BGTaskScheduler` (background audio, background location, VoIP push, `PushKit`); `URLSession` background transfer configuration (`URLSessionConfiguration.background`, owned by the `networking` domain); push-notification-triggered background processing (`content-available` APNs payloads); and actually calling `WidgetCenter.shared.reloadTimelines(ofKind:)`/`reloadAllTimelines()` once new data has landed — owned by the `widgetkit` domain (see `knowledge/widgetkit/timeline-reloading-and-refresh-budget.md`).

## Primary Topics

- Background task registration and scheduling
- Task execution and expiration handling
- Processing task constraints and conditions
- Background refresh and widget timeline hookup

## Used By

- knowledge/backgroundtasks/background-task-registration-and-scheduling.md ([[knowledge/backgroundtasks/background-task-registration-and-scheduling]])
- knowledge/backgroundtasks/task-execution-and-expiration-handling.md ([[knowledge/backgroundtasks/task-execution-and-expiration-handling]])
- knowledge/backgroundtasks/processing-task-constraints-and-conditions.md ([[knowledge/backgroundtasks/processing-task-constraints-and-conditions]])
- knowledge/backgroundtasks/background-refresh-and-widget-timeline-hookup.md ([[knowledge/backgroundtasks/background-refresh-and-widget-timeline-hookup]])
