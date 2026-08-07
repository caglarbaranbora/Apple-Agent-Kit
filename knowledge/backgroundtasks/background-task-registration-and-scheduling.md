# Background Task Registration and Scheduling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.backgroundtasks.background-task-registration-and-scheduling
artifact_type: knowledge
title: Background Task Registration and Scheduling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines registering a task identifier with BGTaskScheduler.shared.register(forTaskWithIdentifier:using:launchHandler:) before the app finishes launching, declaring every identifier in Info.plist under BGTaskSchedulerPermittedIdentifiers, submitting a BGAppRefreshTaskRequest/BGProcessingTaskRequest via submit(_:), and treating earliestBeginDate as a hint, not a guarantee.
domain: BackgroundTasks
tags:
  - backgroundtasks
  - bgtaskscheduler
  - bgapprefreshtaskrequest
  - bgprocessingtaskrequest
  - register
references:
  - https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler
  - https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/register(fortaskwithidentifier:using:launchhandler:)
  - https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/submit(_:)
  - https://developer.apple.com/documentation/backgroundtasks/bgtaskrequest/earliestbegindate
  - https://developer.apple.com/documentation/bundleresources/information-property-list/bgtaskschedulerpermittedidentifiers
  - https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app
depends_on: []
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent makes a background task known to the system and asks the system to run it later: registering a task identifier with `BGTaskScheduler.shared.register(forTaskWithIdentifier:using:launchHandler:)` before the app finishes launching, declaring that identifier in Info.plist, choosing the right `BGTaskRequest` subclass, submitting it with `submit(_:)`, and reasoning correctly about `earliestBeginDate`.

## Scope

### Included

-   Calling `BGTaskScheduler.shared.register(forTaskWithIdentifier:using:launchHandler:)` before the app finishes launching (app delegate `application(_:didFinishLaunchingWithOptions:)` or `App` init)
-   Declaring every identifier the app will submit in Info.plist under `BGTaskSchedulerPermittedIdentifiers`
-   Choosing between `BGAppRefreshTaskRequest` (short, opportunistic refresh) and `BGProcessingTaskRequest` (longer-running, deferrable maintenance work)
-   Submitting a request with `BGTaskScheduler.shared.submit(_:)`
-   Treating `earliestBeginDate` as a hint, not a guarantee
-   Cancelling a request that's no longer needed with `cancel(taskRequestWithIdentifier:)`/`cancelAllTaskRequests()`

### Excluded

-   The `launchHandler`'s `BGTask`, `expirationHandler`, and `setTaskCompleted(success:)` — see `task-execution-and-expiration-handling`
-   `BGProcessingTaskRequest`'s `requiresNetworkConnectivity`/`requiresExternalPower` constraints — see `processing-task-constraints-and-conditions`
-   Scheduling a refresh specifically to feed a widget and the WidgetKit reload hand-off — see `background-refresh-and-widget-timeline-hookup`
-   `BGContinuedProcessingTask` (foreground-initiated work that can continue in the background) — newer API surface, deferred
-   Legacy Background Fetch (`UIApplication.setMinimumBackgroundFetchInterval`, `application(_:performFetchWithCompletionHandler:)`) — pre-iOS 13, superseded by this framework
-   Other background modes unrelated to `BGTaskScheduler` (background audio, background location, VoIP push/`PushKit`), `URLSession` background transfer configuration (owned by `networking`), and push-triggered background processing (`content-available` APNs payloads)

## Rules

### Rule 1

Agents MUST call `BGTaskScheduler.shared.register(forTaskWithIdentifier:using:launchHandler:)` for every task identifier before the app finishes launching, not lazily on first use. Per Apple's documentation, "Registration of all launch handlers must be complete before the end of `applicationDidFinishLaunching(_:)`," and Apple's guide states "Register all of the tasks before the end of the app launch sequence."

### Rule 2

Agents MUST add every identifier the app will register or submit to the Info.plist array `BGTaskSchedulerPermittedIdentifiers`, and MUST NOT expect `register`/`submit` to succeed for an undeclared identifier. Per Apple's documentation, `register(forTaskWithIdentifier:using:launchHandler:)` "Returns `false` if the identifier isn't included in the `BGTaskSchedulerPermittedIdentifiers` `Info.plist`," and "Every identifier in the `BGTaskSchedulerPermittedIdentifiers` requires a handler."

### Rule 3

Agents MUST choose `BGAppRefreshTaskRequest` for short-duration, opportunistic content refresh and `BGProcessingTaskRequest` for longer-running maintenance work, and MUST NOT use one where the other's contract applies. Per Apple's documentation, "`BGAppRefreshTask` is for short-duration tasks that expect quick results, such as downloading a stock quote. `BGProcessingTask` is for tasks that might be time-consuming, such as downloading a large file or synchronizing data."

### Rule 4

Agents MUST submit a previously registered task's request with `BGTaskScheduler.shared.submit(_:)`, and MUST account for the framework's queue limits rather than submitting unboundedly. Per Apple's documentation, `submit(_:)` will "Submit a previously registered background task for execution," "Submitting a task request for an unexecuted task that's already in the queue replaces the previous task request," and "There can be a total of 1 refresh task and 10 processing tasks scheduled at any time. Trying to schedule more tasks returns `BGTaskScheduler.Error.Code.tooManyPendingTaskRequests`."

### Rule 5

Agents MUST treat `earliestBeginDate` as a lower bound the system may exceed by an unknown amount, not an expected or scheduled run time, and MUST NOT build logic that assumes the task runs at or near that date. Per Apple's documentation, "Setting the property indicates that the background task shouldn't start any earlier than this date. However, the system doesn't guarantee launching the task at the specified date, but only that it won't begin sooner," and "Specify `nil` for no start delay."

### Rule 6

Agents MUST cancel a pending request with `cancel(taskRequestWithIdentifier:)` (or all pending requests with `cancelAllTaskRequests()`) when the work it represents is no longer needed, rather than leaving a stale request queued. Per Apple's documentation, `cancel(taskRequestWithIdentifier:)` will "Cancel a previously scheduled task request," and `cancelAllTaskRequests()` will "Cancel all scheduled task requests."

## Compliant Example

```swift
// App delegate: register before launch finishes (Rule 1).
func application(_ application: UIApplication,
                  didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    BGTaskScheduler.shared.register(forTaskWithIdentifier: "com.example.app.refresh", using: nil) { task in
        self.handleAppRefresh(task: task as! BGAppRefreshTask)
    }
    return true
}

// Declared in Info.plist under BGTaskSchedulerPermittedIdentifiers: ["com.example.app.refresh"] (Rule 2).

func scheduleAppRefresh() {
    let request = BGAppRefreshTaskRequest(identifier: "com.example.app.refresh") // Rule 3: short refresh.
    request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // hint, not a guarantee (Rule 5).
    do {
        try BGTaskScheduler.shared.submit(request) // Rule 4.
    } catch {
        print("Could not schedule app refresh: \(error)")
    }
}
```

## Non-Compliant Example

```swift
func refreshButtonTapped() {
    // Registers on demand, long after launch has finished -- violates Rule 1.
    BGTaskScheduler.shared.register(forTaskWithIdentifier: "com.example.app.refresh", using: nil) { task in
        self.handleAppRefresh(task: task as! BGAppRefreshTask)
    }
    let request = BGAppRefreshTaskRequest(identifier: "com.example.app.refresh")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 60)
    try? BGTaskScheduler.shared.submit(request)
    // Assumes the task runs in exactly 60 seconds and blocks on that assumption -- violates Rule 5.
}
```
Registers the identifier in response to a user action instead of before the app finishes launching (Rule 1), and treats `earliestBeginDate` as a scheduled run time rather than a hint (Rule 5). The identifier is also never confirmed against `BGTaskSchedulerPermittedIdentifiers` (Rule 2).

## Dependencies

None within this domain — this is the foundational contract other BackgroundTasks Knowledge Contracts build on.

## References

-   [Apple Developer — BGTaskScheduler](https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler)
-   [Apple Developer — register(forTaskWithIdentifier:using:launchHandler:)](https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/register(fortaskwithidentifier:using:launchhandler:))
-   [Apple Developer — submit(_:)](https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler/submit(_:))
-   [Apple Developer — earliestBeginDate](https://developer.apple.com/documentation/backgroundtasks/bgtaskrequest/earliestbegindate)
-   [Apple Developer — BGTaskSchedulerPermittedIdentifiers](https://developer.apple.com/documentation/bundleresources/information-property-list/bgtaskschedulerpermittedidentifiers)
-   [Apple Developer — Using background tasks to update your app](https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app)
