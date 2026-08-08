# Processing Task Constraints and Conditions

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.backgroundtasks.processing-task-constraints-and-conditions
artifact_type: knowledge
title: Processing Task Constraints and Conditions
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines BGProcessingTaskRequest's requiresNetworkConnectivity and requiresExternalPower flags, when to choose BGProcessingTaskRequest over BGAppRefreshTaskRequest, and why these constraints make prompt execution less likely, not more.
domain: BackgroundTasks
tags:
  - backgroundtasks
  - bgprocessingtaskrequest
  - requiresnetworkconnectivity
  - requiresexternalpower
references:
  - https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest
  - https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest/requiresnetworkconnectivity
  - https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest/requiresexternalpower
  - https://developer.apple.com/documentation/backgroundtasks/bgapprefreshtaskrequest
  - https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app
depends_on:
  - knowledge.backgroundtasks.background-task-registration-and-scheduling
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines the two execution-condition flags an AI coding agent can set on a `BGProcessingTaskRequest` — `requiresNetworkConnectivity` and `requiresExternalPower` — when to reach for `BGProcessingTaskRequest` instead of `BGAppRefreshTaskRequest` in the first place, and why adding these constraints makes the system less likely to run the task soon, not more likely.

## Scope

### Included

-   `BGProcessingTaskRequest.requiresNetworkConnectivity`
-   `BGProcessingTaskRequest.requiresExternalPower`
-   Choosing `BGProcessingTaskRequest` over `BGAppRefreshTaskRequest` for heavy, deferrable maintenance work
-   The practical reality that constrained requests wait longer for a matching opportunity, not less

### Excluded

-   Registering, submitting, and `earliestBeginDate` mechanics shared by both request types — see `background-task-registration-and-scheduling`
-   The `launchHandler`/`expirationHandler`/`setTaskCompleted(success:)` execution contract, which applies identically to `BGProcessingTask` — see `task-execution-and-expiration-handling`
-   `BGHealthResearchTaskRequest` and other request subclasses outside `BGAppRefreshTaskRequest`/`BGProcessingTaskRequest` — not part of this domain's v1

## Rules

### Rule 1

Agents MUST set `requiresNetworkConnectivity = true` on a `BGProcessingTaskRequest` only when the task's work genuinely needs network access, and MUST NOT set it reflexively on every processing request. Per Apple's documentation, `requiresNetworkConnectivity` is "A Boolean specifying if the processing task requires network connectivity."

### Rule 2

Agents MUST set `requiresExternalPower = true` on a `BGProcessingTaskRequest` only when the task's work genuinely needs the device connected to power (e.g. sustained heavy computation), and MUST NOT set it for work that can run on battery. Per Apple's documentation, `requiresExternalPower` is "A Boolean specifying if the processing task requires a device connected to power."

### Rule 3

Agents MUST choose `BGProcessingTaskRequest` for heavy, deferrable maintenance work (e.g. database maintenance, on-device model training) and `BGAppRefreshTaskRequest` for quick, opportunistic content refresh, rather than treating the two as interchangeable. Per Apple's documentation, "To preserve battery life and performance, you can schedule background tasks for periods of low activity, such as overnight when the device charges. Use this approach when your app manages heavy workloads, such as training machine learning models or performing database maintenance. Schedule these types of background tasks using `BGProcessingTask`." By contrast, `BGAppRefreshTaskRequest` is for cases where "your app may require short bursts of background time to perform content refresh or other work" and "provides your app up to 30 seconds of background runtime."

### Rule 4

Agents MUST treat `requiresNetworkConnectivity`/`requiresExternalPower` as constraints that narrow the set of moments the system considers eligible to run the task, and therefore MUST NOT assume that submitting a `BGProcessingTaskRequest` with these flags set makes the system run it any sooner than an unconstrained request — if anything, agents should expect it to wait longer for a moment (e.g. overnight while charging) that satisfies every condition simultaneously. This is reasoned framework behavior rather than a literal Apple quote: Apple's guidance frames `BGProcessingTask` work as something scheduled for "periods of low activity, such as overnight when the device charges," and "the system decides the best time to launch your background task" in every case — adding conditions can only shrink that set of acceptable times, not expand it.

## Compliant Example

```swift
func scheduleDatabaseMaintenance() {
    let request = BGProcessingTaskRequest(identifier: "com.example.app.db-maintenance") // Rule 3: heavy, deferrable work.
    request.requiresNetworkConnectivity = false // Rule 1: this task doesn't touch the network.
    request.requiresExternalPower = true        // Rule 2: sustained CPU work, require power.
    request.earliestBeginDate = Date(timeIntervalSinceNow: 60 * 60) // No later than an hour out.
    do {
        try BGTaskScheduler.shared.submit(request)
        // Rule 4: expect this to run overnight while charging, not imminently.
    } catch {
        print("Could not schedule database maintenance: \(error)")
    }
}
```
Uses `BGProcessingTaskRequest` for heavy maintenance work rather than `BGAppRefreshTaskRequest` (Rule 3), sets only the constraint the work actually needs (Rule 2, with Rule 1 left `false` deliberately), and the surrounding comment reflects the realistic expectation that this runs later, not sooner (Rule 4).

## Non-Compliant Example

```swift
func scheduleDatabaseMaintenance() {
    let request = BGAppRefreshTaskRequest(identifier: "com.example.app.db-maintenance")
    // Uses the short-refresh request type for heavy, minutes-long work -- violates Rule 3.

    request.earliestBeginDate = Date(timeIntervalSinceNow: 5 * 60)
    try? BGTaskScheduler.shared.submit(request)
    // Comment elsewhere in the codebase: "Runs almost immediately since we
    // required power and network -- should finish within a few minutes."
    // Wrong: adding constraints narrows eligible run times, it doesn't
    // speed anything up -- violates Rule 4.
}
```
Uses `BGAppRefreshTaskRequest` for maintenance work that belongs on `BGProcessingTaskRequest` (Rule 3), and assumes that constraints make the system run the task sooner rather than narrowing the eligible window (Rule 4).

## Dependencies

-   `knowledge.backgroundtasks.background-task-registration-and-scheduling` — `BGProcessingTaskRequest` is one of the two request subclasses that contract's registration/submission rules already cover; this contract only adds the request-specific constraint flags.

## References

-   [Apple Developer — BGProcessingTaskRequest](https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest)
-   [Apple Developer — requiresNetworkConnectivity](https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest/requiresnetworkconnectivity)
-   [Apple Developer — requiresExternalPower](https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest/requiresexternalpower)
-   [Apple Developer — BGAppRefreshTaskRequest](https://developer.apple.com/documentation/backgroundtasks/bgapprefreshtaskrequest)
-   [Apple Developer — Choosing Background Strategies for Your App](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app)
