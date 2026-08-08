# Background Monitoring and Launches

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.core-location.background-monitoring-and-launches
artifact_type: knowledge
title: Background Monitoring and Launches
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines running location outside the foreground -- allowsBackgroundLocationUpdates with its required UIBackgroundModes value, significant-change and CLMonitor condition monitoring, and the relaunches they produce instead of a scheduled background task.
domain: Core Location
tags:
  - core-location
  - background
  - clmonitor
  - significant-location-change
  - uibackgroundmodes
references:
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/allowsbackgroundlocationupdates
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/startmonitoringsignificantlocationchanges()
  - https://developer.apple.com/documentation/corelocation/monitoring-the-user-s-proximity-to-geographic-regions
  - https://developer.apple.com/documentation/corelocation/clmonitor-2r51v
  - https://developer.apple.com/documentation/corelocation/clcirculargeographiccondition
  - https://developer.apple.com/documentation/bundleresources/information-property-list/uibackgroundmodes
depends_on:
  - knowledge.core-location.authorization-and-usage-strings
  - knowledge.core-location.accuracy-and-precise-location
related:
  - knowledge.backgroundtasks.background-task-registration-and-scheduling
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent runs location work while the app is not in the foreground: enabling background delivery without the configuration mistake that terminates the app, choosing between continuous updates and the two monitoring services, and handling the relaunch each monitoring service produces.

## Scope

### Included

-   `allowsBackgroundLocationUpdates` and the `UIBackgroundModes` `location` value it requires
-   `startMonitoringSignificantLocationChanges()`, its relaunch behavior, and its documented event cadence
-   `CLMonitor` with `CLCircularGeographicCondition`, the per-app condition limit, and recreating a monitor after relaunch
-   Choosing a monitoring service instead of a scheduled background task

### Excluded

-   Obtaining Always authorization, without which none of this runs — see `authorization-and-usage-strings`
-   Whether the granted accuracy permits region monitoring at all — see `accuracy-and-precise-location` Rule 3, which owns that precondition; this contract states none of its own accuracy rules
-   Foreground delivery mechanics and stopping a stream — see `location-updates-and-delivery`
-   `BGTaskScheduler` registration, scheduling, and expiration handling — see `knowledge.backgroundtasks.background-task-registration-and-scheduling`; Rule 4 below owns only the choice *between* that mechanism and this one
-   Visit monitoring (`CLVisit`) and beacon monitoring, out of this domain's v1 scope entirely

## Rules

### Rule 1

Agents MUST add the `UIBackgroundModes` key with the `location` value to the app's Information Property List before setting `allowsBackgroundLocationUpdates` to `true`, and MUST NOT treat the missing key as a degraded-delivery case. Per Apple's documentation, "Apps that receive location updates when running in the background must include the `UIBackgroundModes` key (with the `location` value) in their app's `Info.plist` file," and "Setting the value to `true` but omitting the `UIBackgroundModes` key and `location` value in your app's `Info.plist` file is a fatal error that terminates the app."

### Rule 2

Agents MUST restart the service after a location-triggered relaunch rather than assuming delivery resumes. Per Apple's documentation on significant-change monitoring, "If you start this service and your app is subsequently terminated, the system automatically relaunches the app into the background if a new event arrives," with `UIApplication.LaunchOptionsKey.location` present in the launch options, and "Upon relaunch, you must still configure a location manager object and call this method to continue receiving location events." The equivalent for condition monitoring is to rebuild the monitor under its original name: "When the app relaunches, recreate the monitor with the same identifier."

### Rule 3

Agents MUST budget conditions against the documented per-app ceiling and MUST NOT register one condition per item in an unbounded list. Per Apple's documentation, "To ensure that all apps can participate in condition monitoring, Core Location prevents any single app from monitoring more than 20 conditions of any type simultaneously. Prioritize what you want to monitor to based on this restriction." Apple also notes that "monitoring can only occur after the user unlocks the device after a reboot," so a monitor is not a guarantee of coverage from the moment of registration.

### Rule 4

Agents MUST NOT schedule a `BGAppRefreshTask` or `BGProcessingTask` in order to poll the device's location, and MUST use significant-change or condition monitoring instead when the app needs to act on movement while not in the foreground. This is the coupled decision between the two domains, and this contract owns it: Core Location performs the launch itself — the system "automatically relaunches the app into the background if a new event arrives" for significant-change, and "If an iOS app isn't running when a condition is satisfied, the system tries to launch it" for condition monitoring — so choosing a monitoring service *removes* the need for a scheduled task rather than sitting beside it. `knowledge.backgroundtasks.background-task-registration-and-scheduling` owns everything about `BGTaskScheduler` itself; what it cannot state, because the question only exists once location is involved, is that this is the wrong mechanism for this job.

### Rule 5

Agents MUST NOT build a feature on significant-change monitoring that requires updates more often than the service delivers them. Per Apple's documentation, "Apps can expect a notification as soon as the device moves 500 meters or more from its previous notification. It should not expect notifications more frequently than once every five minutes." A feature needing tighter cadence needs continuous updates with `allowsBackgroundLocationUpdates` and the battery cost that carries, and the choice MUST be made deliberately rather than discovered when events arrive late.

## Compliant Example

```swift
import CoreLocation
// Rule 4: movement-triggered work uses Core Location's own launch, not BGTaskScheduler.
func startGeofence(center: CLLocationCoordinate2D) async throws {
    let monitor = await CLMonitor("delivery_monitor") // Rule 2: stable identifier
    // Rule 3: one condition, well under the 20-condition per-app ceiling.
    await monitor.add(CLCircularGeographicCondition(center: center, radius: 200),
                      identifier: "at_drop_off")
    for try await event in await monitor.events where event.state == .satisfied {
        await handleArrival()
    }
}
// Rule 1: Info.plist carries UIBackgroundModes -> location before this is ever set.
func enableContinuousBackgroundUpdates(_ manager: CLLocationManager) {
    manager.allowsBackgroundLocationUpdates = true // Rule 5: chosen, not defaulted to
}
func handleArrival() async { /* act on the crossing */ }
```

## Non-Compliant Example

```swift
import BackgroundTasks
import CoreLocation

func scheduleLocationPoll() {
    // Polls location from a scheduled refresh task instead of letting Core Location
    // launch the app on movement -- violates Rule 4.
    let request = BGAppRefreshTaskRequest(identifier: "com.example.locationPoll")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 60) // also Rule 5's cadence
    try? BGTaskScheduler.shared.submit(request)
}
func enableBackground(_ manager: CLLocationManager) {
    // No UIBackgroundModes location value in Info.plist: this terminates the app
    // rather than degrading delivery -- violates Rule 1.
    manager.allowsBackgroundLocationUpdates = true
    manager.startMonitoringSignificantLocationChanges()
    // Relaunch handling assumes delivery resumes by itself -- violates Rule 2.
}
```
Uses `BGTaskScheduler` for work Core Location launches the app to do (Rule 4), at a cadence the service does not deliver (Rule 5), sets the background flag without the Information Property List value that makes it legal (Rule 1), and never restarts the service after a location-triggered relaunch (Rule 2).

## Dependencies

-   `knowledge.core-location.authorization-and-usage-strings` — every service here requires an authorization level that contract obtains, and condition monitoring requires Always.
-   `knowledge.core-location.accuracy-and-precise-location` — that contract's Rule 3 states whether the granted accuracy permits region monitoring; this one assumes the check was made.

## References

-   [Apple Developer — allowsBackgroundLocationUpdates](https://developer.apple.com/documentation/corelocation/cllocationmanager/allowsbackgroundlocationupdates)
-   [Apple Developer — startMonitoringSignificantLocationChanges()](https://developer.apple.com/documentation/corelocation/cllocationmanager/startmonitoringsignificantlocationchanges())
-   [Apple Developer — Monitoring the user's proximity to geographic regions](https://developer.apple.com/documentation/corelocation/monitoring-the-user-s-proximity-to-geographic-regions)
-   [Apple Developer — CLMonitor](https://developer.apple.com/documentation/corelocation/clmonitor-2r51v)
-   [Apple Developer — CLCircularGeographicCondition](https://developer.apple.com/documentation/corelocation/clcirculargeographiccondition)
-   [Apple Developer — UIBackgroundModes](https://developer.apple.com/documentation/bundleresources/information-property-list/uibackgroundmodes)
