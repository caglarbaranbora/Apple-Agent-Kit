---
name: backgroundtasks
description: Route BackgroundTasks implementation tasks to the correct Knowledge Contracts -- background task registration and scheduling, task execution and expiration handling, processing task constraints and conditions, and background refresh and widget timeline hookup. Use when registering a task identifier with BGTaskScheduler.register(forTaskWithIdentifier:using:launchHandler:), declaring BGTaskSchedulerPermittedIdentifiers, submitting a BGAppRefreshTaskRequest/BGProcessingTaskRequest, reading earliestBeginDate, handling a BGTask/BGAppRefreshTask/BGProcessingTask in a launch handler, setting expirationHandler, calling setTaskCompleted(success:), setting requiresNetworkConnectivity/requiresExternalPower, or scheduling background refresh that feeds a widget. v1 is BGTaskScheduler-based scheduling and execution only -- no BGContinuedProcessingTask, no legacy Background Fetch (setMinimumBackgroundFetchInterval, performFetchWithCompletionHandler), no unrelated background modes (background audio, background location, VoIP/PushKit), and no URLSession background transfer configuration -- that's networking's job. Triggers on BackgroundTasks, BGTaskScheduler, BGTask, BGTaskRequest, BGAppRefreshTaskRequest, BGProcessingTaskRequest, BGAppRefreshTask, BGProcessingTask, launchHandler, expirationHandler, setTaskCompleted, requiresNetworkConnectivity, requiresExternalPower, earliestBeginDate, BGTaskSchedulerPermittedIdentifiers.
id: skill.backgroundtasks.foundations
title: BackgroundTasks — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: BackgroundTasks
routes: [knowledge.backgroundtasks.background-task-registration-and-scheduling, knowledge.backgroundtasks.task-execution-and-expiration-handling, knowledge.backgroundtasks.processing-task-constraints-and-conditions, knowledge.backgroundtasks.background-refresh-and-widget-timeline-hookup]
related: [knowledge.widgetkit.timeline-reloading-and-refresh-budget]
last_updated: 2026-08-06
---

# BackgroundTasks — Foundations Skill

## Purpose

Route BackgroundTasks implementation tasks to the minimum required
BackgroundTasks Knowledge Contracts. v1 scope is scheduling and running
deferred background work through `BGTaskScheduler` -- registration,
submission, execution, expiration handling, processing constraints, and
the hand-off point where background-refreshed data reaches a widget --
not `BGContinuedProcessingTask`, not legacy Background Fetch, not
unrelated background modes, and not `URLSession` background transfer.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/backgroundtasks/.

-   Registering a task identifier with `BGTaskScheduler.shared.register(forTaskWithIdentifier:using:launchHandler:)`; declaring `BGTaskSchedulerPermittedIdentifiers`; choosing `BGAppRefreshTaskRequest` vs `BGProcessingTaskRequest`; submitting with `submit(_:)`; or reasoning about `earliestBeginDate` -> background-task-registration-and-scheduling.md
-   Handling the `BGTask` delivered to a `launchHandler` (casting to `BGAppRefreshTask`/`BGProcessingTask`); setting `expirationHandler`; calling `setTaskCompleted(success:)`; or re-submitting a request for the next occurrence -> task-execution-and-expiration-handling.md
-   Setting `BGProcessingTaskRequest.requiresNetworkConnectivity`/`requiresExternalPower`; or deciding whether work belongs on `BGProcessingTaskRequest` versus `BGAppRefreshTaskRequest` -> processing-task-constraints-and-conditions.md
-   Scheduling a `BGAppRefreshTaskRequest` to refresh data a widget depends on, up through the point new data has landed -> background-refresh-and-widget-timeline-hookup.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/backgroundtasks/ — do not guess or fall back to
general knowledge. `BGContinuedProcessingTask` (foreground-initiated work
that can continue in the background) is out of scope entirely -- newer
API surface, deferred, not yet built (see docs/architecture/domain-map.md).
Legacy Background Fetch (`UIApplication.setMinimumBackgroundFetchInterval`,
`application(_:performFetchWithCompletionHandler:)`) is out of scope --
superseded by this framework, not planned as a separate domain; report
that explicitly. Other background modes unrelated to `BGTaskScheduler`
(background audio, background location, VoIP push/`PushKit`) are out of
scope entirely. `URLSession` background transfer configuration
(`URLSessionConfiguration.background`) is `networking`'s job, not this
Skill's. Actually calling `WidgetCenter.shared.reloadTimelines(ofKind:)`/
`reloadAllTimelines()`, and every rule about the refresh budget governing
that call, is `widgetkit`'s job (`knowledge.widgetkit.timeline-reloading-and-refresh-budget`)
-- this Skill only routes to getting the background task registered,
submitted, and run so fresh data exists for that call to reload.
