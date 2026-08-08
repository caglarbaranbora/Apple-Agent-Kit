# Location Updates and Delivery

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.core-location.location-updates-and-delivery
artifact_type: knowledge
title: Location Updates and Delivery
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines choosing one delivery mechanism -- the CLLocationUpdate.liveUpdates async sequence or the CLLocationManagerDelegate pair -- and starting, reading, and stopping location updates without mixing the two.
domain: Core Location
tags:
  - core-location
  - cllocationupdate
  - cllocationmanager
  - cllocationmanagerdelegate
  - location-updates
references:
  - https://developer.apple.com/documentation/corelocation/cllocationupdate
  - https://developer.apple.com/documentation/corelocation/cllocationupdate/liveupdates(_:)
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/startupdatinglocation()
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/stopupdatinglocation()
  - https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate/locationmanager(_:didupdatelocations:)
  - https://developer.apple.com/documentation/corelocation/cllocation
depends_on:
  - knowledge.core-location.authorization-and-usage-strings
related: []
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent receives location from Core Location once access is granted: picking exactly one of the two delivery mechanisms Apple ships, reading authorization and diagnostic state from whichever one it picked, and stopping delivery when the feature is done with it.

## Scope

### Included

-   `CLLocationUpdate.liveUpdates(_:)` and iterating the `CLLocationUpdate.Updates` async sequence
-   Reading `CLLocationUpdate`'s `location` and its diagnostic properties (`authorizationDenied`, `authorizationDeniedGlobally`, `insufficientlyInUse`, `authorizationRequestInProgress`, `accuracyLimited`)
-   `startUpdatingLocation()`/`stopUpdatingLocation()` with `locationManager(_:didUpdateLocations:)` and `locationManager(_:didFailWithError:)`
-   The restart semantics of calling `startUpdatingLocation()` more than once
-   Reading `CLLocation`'s `timestamp` before trusting a delivered fix

### Excluded

-   Obtaining authorization in the first place, and the status values themselves — see `authorization-and-usage-strings`
-   `desiredAccuracy` and what a reduced-accuracy grant does to delivery — see `accuracy-and-precise-location`
-   Continuing delivery while the app is backgrounded or terminated, the `UIBackgroundModes` `location` value, and significant-change or condition monitoring — see `background-monitoring-and-launches`
-   `CLGeocoder`, heading (`CLHeading`), and visits (`CLVisit`), which are out of this domain's v1 scope entirely

## Rules

### Rule 1

Agents MUST choose one delivery mechanism per feature and MUST NOT run `CLLocationUpdate.liveUpdates(_:)` and a `CLLocationManagerDelegate` against the same feature at once. The two are alternative front ends to the same service: `liveUpdates(_:)` "Tells Core Location to start delivering the location updates it produces for the configuration you specify" and returns an async sequence, while `startUpdatingLocation()` "Starts the generation of updates that report the user's current location" and delivers them "by calling its `locationManager(_:didUpdateLocations:)` method." Running both doubles the request for the same data and splits the feature's state across two owners.

### Rule 2

Agents using the async sequence MUST read authorization and diagnostic state from the delivered `CLLocationUpdate` rather than reaching for a separate `CLLocationManager` to answer the same question. `CLLocationUpdate` is "A structure that contains the location information the framework delivers with each update" and carries `authorizationDenied`, `authorizationDeniedGlobally`, `insufficientlyInUse`, `authorizationRequestInProgress`, and `accuracyLimited` alongside `location`, which is documented as "The user's location, if available" — so an update with no `location` is a state to branch on, not an error to ignore.

### Rule 3

Agents using the delegate MUST implement the failure callback alongside the success one. Per Apple's documentation, "In addition to your delegate object implementing the `locationManager(_:didUpdateLocations:)` method, it should also implement the `locationManager(_:didFailWithError:)` method to respond to potential errors." A delegate with only the success method silently reports nothing when location is unavailable.

### Rule 4

Agents MUST NOT call `startUpdatingLocation()` again as a way to force a fresh fix. Per Apple's documentation, "Calling this method several times in succession does not automatically result in new events being generated. Calling `stopUpdatingLocation()` in between, however, does cause a new initial event to be sent the next time you call this method." An agent that needs a new initial event MUST stop first.

### Rule 5

Agents MUST stop delivery when the feature no longer needs it — `stopUpdatingLocation()` for the delegate path, cancelling the iterating `Task` for the async sequence — and MUST NOT leave a stream running for the lifetime of the app because the screen that started it might return. Core Location keeps the hardware working for as long as updates are requested; Apple's own guidance on `desiredAccuracy` frames continuous location as a cost to be sized against need ("To reduce your app's impact on battery life, assign a value to this property that's appropriate for your usage"), and a stream nobody reads is that cost with no benefit.

### Rule 6

Agents MUST check a delivered fix's `timestamp` before acting on it rather than treating the first delivery as current. Core Location's documented behavior is to deliver what it already has while it works toward a better answer — Apple states for the significant-change service that "The first event to be delivered is usually the most recently cached location event (if any)... Obtaining a current location fix may take several additional seconds, so be sure to check the timestamps on the location events in your delegate method." The same caching applies to the standard service, whose initial fix "may take several seconds" to obtain.

## Compliant Example

```swift
import CoreLocation
// Async-sequence path (Rule 1: this feature uses only this mechanism).
func trackWhileVisible() async throws {
    for try await update in CLLocationUpdate.liveUpdates() {
        if update.authorizationDenied || update.authorizationDeniedGlobally {
            break // Rule 2: the update itself reports authorization state
        }
        guard let location = update.location else { continue } // Rule 2
        guard location.timestamp.timeIntervalSinceNow > -30 else { continue } // Rule 6
        render(location)
    }
    // Rule 5: cancelling the enclosing Task ends delivery; nothing keeps running.
}
func render(_ location: CLLocation) { /* update the UI */ }
```

## Non-Compliant Example

```swift
import CoreLocation
final class Tracker: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    private var stream: Task<Void, Error>?

    func start() {
        manager.delegate = self
        manager.startUpdatingLocation()
        // A second mechanism for the same feature -- violates Rule 1.
        stream = Task { for try await _ in CLLocationUpdate.liveUpdates() {} }
        manager.startUpdatingLocation() // No new event; needed a stop -- Rule 4.
    }
    // No locationManager(_:didFailWithError:) -- violates Rule 3.
    func locationManager(_ m: CLLocationManager, didUpdateLocations l: [CLLocation]) {
        render(l.last!) // Acts on a possibly cached fix, unread timestamp -- Rule 6.
    }
    // Nothing ever calls stopUpdatingLocation() or cancels stream -- violates Rule 5.
    func render(_ location: CLLocation) { }
}
```
Runs both delivery mechanisms for one feature (Rule 1), implements no failure callback (Rule 3), restarts instead of stopping first (Rule 4), never stops (Rule 5), and trusts the first fix without reading its `timestamp` (Rule 6).

## Dependencies

-   `knowledge.core-location.authorization-and-usage-strings` — delivery begins only after authorization is granted; this contract assumes that contract's rules were followed first.

## References

-   [Apple Developer — CLLocationUpdate](https://developer.apple.com/documentation/corelocation/cllocationupdate)
-   [Apple Developer — liveUpdates(_:)](https://developer.apple.com/documentation/corelocation/cllocationupdate/liveupdates(_:))
-   [Apple Developer — startUpdatingLocation()](https://developer.apple.com/documentation/corelocation/cllocationmanager/startupdatinglocation())
-   [Apple Developer — stopUpdatingLocation()](https://developer.apple.com/documentation/corelocation/cllocationmanager/stopupdatinglocation())
-   [Apple Developer — locationManager(_:didUpdateLocations:)](https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate/locationmanager(_:didupdatelocations:))
-   [Apple Developer — CLLocation](https://developer.apple.com/documentation/corelocation/cllocation)
