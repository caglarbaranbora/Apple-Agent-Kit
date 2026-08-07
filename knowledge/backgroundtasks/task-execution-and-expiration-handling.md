# Task Execution and Expiration Handling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.backgroundtasks.task-execution-and-expiration-handling
artifact_type: knowledge
title: Task Execution and Expiration Handling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines handling the BGTask delivered to a launchHandler (casting to BGAppRefreshTask/BGProcessingTask), setting task.expirationHandler to cancel in-flight work, calling task.setTaskCompleted(success:) exactly once, and re-submitting a request for the next occurrence when work should repeat.
domain: BackgroundTasks
tags:
  - backgroundtasks
  - bgtask
  - expirationhandler
  - settaskcompleted
references:
  - https://developer.apple.com/documentation/backgroundtasks/bgtask
  - https://developer.apple.com/documentation/backgroundtasks/bgtask/expirationhandler
  - https://developer.apple.com/documentation/backgroundtasks/bgtask/settaskcompleted(success:)
  - https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app
depends_on:
  - knowledge.backgroundtasks.background-task-registration-and-scheduling
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines what an AI coding agent does inside a registered task's `launchHandler`: reading the delivered `BGTask` as its concrete subclass, guarding against the system revoking time mid-work with `expirationHandler`, reporting completion exactly once with `setTaskCompleted(success:)`, and re-submitting a new request when the work should recur — the system does not reschedule a task on its own.

## Scope

### Included

-   The `launchHandler` closure receiving a `BGTask`, cast to `BGAppRefreshTask`/`BGProcessingTask` to match the request submitted
-   Setting `task.expirationHandler` to cancel in-flight work when the system revokes remaining time
-   Calling `task.setTaskCompleted(success:)` exactly once, reflecting whether the work actually succeeded
-   Re-submitting a new request for the task's next occurrence before/while completing, when the work should repeat

### Excluded

-   Registering the identifier and submitting the initial request — see `background-task-registration-and-scheduling`
-   `BGProcessingTaskRequest`'s `requiresNetworkConnectivity`/`requiresExternalPower` constraints — see `processing-task-constraints-and-conditions`
-   Calling `WidgetCenter.shared.reloadTimelines`/`reloadAllTimelines` after this task's data lands — see `background-refresh-and-widget-timeline-hookup`
-   `BGContinuedProcessingTask` — a task your app executes in the foreground rather than one the system runs on your app's behalf in the background; newer API surface, deferred

## Rules

### Rule 1

Agents MUST cast the `BGTask` delivered to a `launchHandler` to the concrete subclass matching the request that was submitted for that identifier (`BGAppRefreshTask` for a `BGAppRefreshTaskRequest`, `BGProcessingTask` for a `BGProcessingTaskRequest`) before reading any subclass-specific state. Per Apple's documentation, `BGTask` is "An abstract class for the framework's tasks," and `register(forTaskWithIdentifier:using:launchHandler:)` delivers it typed only as `BGTask` (`launchHandler: (BGTask) -> Void`); Apple's sample code performs this cast directly: `self.handleAppRefresh(task: task as! BGAppRefreshTask)`.

### Rule 2

Agents MUST assign `task.expirationHandler` before starting the task's work, and that handler MUST cancel or otherwise stop the in-flight work rather than leaving it running unattended. Per Apple's documentation, `expirationHandler` is "A handler called shortly before the task's background time expires," and "Not setting an expiration handler results in the system marking your task as complete and unsuccessful instead of sending a warning." Agents MUST also ensure the handler's own work "complete[s] before the allocated time," since "the time allocated by the system for expiration handlers doesn't vary with the number of background tasks."

### Rule 3

Agents MUST call `task.setTaskCompleted(success:)` exactly once per task invocation, after the work finishes (whether it succeeded or failed), and MUST NOT omit the call or call it more than once. Per Apple's documentation, `setTaskCompleted(success:)` "Informs the background task scheduler that the task is complete," and "Not calling `setTaskCompleted(success:)` before the time for the task expires may result in the system killing your app."

### Rule 4

Agents whose task should recur MUST submit a new request for the task's next occurrence themselves — the system does not automatically create a follow-up request once one has run. Apple's own sample code demonstrates this pattern by resubmitting inside the launch handler, before doing any of the task's actual work: `handleAppRefresh(task:)` opens with `// Schedule a new refresh task.` followed by a call to `scheduleAppRefresh()`, ahead of running the refresh operation itself.

## Compliant Example

```swift
func handleAppRefresh(task: BGAppRefreshTask) {
    // Rule 4: re-submit for the next occurrence before doing this run's work.
    scheduleAppRefresh()

    let operation = RefreshAppContentsOperation()

    // Rule 2: cancel in-flight work if the system revokes time.
    task.expirationHandler = {
        operation.cancel()
    }

    // Rule 3: report completion exactly once, success reflects outcome.
    operation.completionBlock = {
        task.setTaskCompleted(success: !operation.isCancelled)
    }

    operationQueue.addOperation(operation)
}
```
Casts to `BGAppRefreshTask` at the registration call site (Rule 1), sets `expirationHandler` before starting work (Rule 2), calls `setTaskCompleted(success:)` exactly once from the operation's completion (Rule 3), and re-submits the next request up front (Rule 4).

## Non-Compliant Example

```swift
func handleAppRefresh(task: BGAppRefreshTask) {
    let operation = RefreshAppContentsOperation()
    // No expirationHandler -- violates Rule 2; the system marks the task
    // complete and unsuccessful with no chance to cancel cleanly.

    operationQueue.addOperation(operation)
    task.setTaskCompleted(success: true) // Called immediately, before the
                                          // operation finishes -- violates Rule 3.
    // No re-submission for the next occurrence -- violates Rule 4; this
    // task never runs again.
}
```
Omits `expirationHandler` entirely (Rule 2), calls `setTaskCompleted(success:)` before the work actually completes and hardcodes `true` regardless of outcome (Rule 3), and never re-submits a request for the next occurrence (Rule 4).

## Dependencies

-   `knowledge.backgroundtasks.background-task-registration-and-scheduling` — the `BGTask` this contract governs is delivered to the `launchHandler` registered per that contract's rules, for a request submitted per those rules.

## References

-   [Apple Developer — BGTask](https://developer.apple.com/documentation/backgroundtasks/bgtask)
-   [Apple Developer — expirationHandler](https://developer.apple.com/documentation/backgroundtasks/bgtask/expirationhandler)
-   [Apple Developer — setTaskCompleted(success:)](https://developer.apple.com/documentation/backgroundtasks/bgtask/settaskcompleted(success:))
-   [Apple Developer — Using background tasks to update your app](https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app)
