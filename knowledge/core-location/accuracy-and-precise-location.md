# Accuracy and Precise Location

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.core-location.accuracy-and-precise-location
artifact_type: knowledge
title: Accuracy and Precise Location
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requesting an accuracy with desiredAccuracy, reading the separately granted CLAccuracyAuthorization, and asking for temporary full accuracy with a purpose key rather than treating precision as guaranteed.
domain: Core Location
tags:
  - core-location
  - desiredaccuracy
  - claccuracyauthorization
  - precise-location
  - info-plist
references:
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/desiredaccuracy
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/accuracyauthorization
  - https://developer.apple.com/documentation/corelocation/claccuracyauthorization
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/requesttemporaryfullaccuracyauthorization(withpurposekey:)
  - https://developer.apple.com/documentation/corelocation/kcllocationaccuracyreduced
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationtemporaryusagedescriptiondictionary
depends_on:
  - knowledge.core-location.authorization-and-usage-strings
related: []
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent handles location accuracy as two independent things: the accuracy the app *asks* for, which is a hint the system may not meet, and the accuracy the person *granted*, which the app cannot raise by setting a property.

## Scope

### Included

-   Setting `desiredAccuracy` and choosing among the `kCLLocationAccuracy…` constants
-   Reading `accuracyAuthorization` and branching on `CLAccuracyAuthorization` (`.fullAccuracy`, `.reducedAccuracy`)
-   What a reduced-accuracy grant disables, including region and beacon monitoring
-   `requestTemporaryFullAccuracyAuthorization(withPurposeKey:)` and the `NSLocationTemporaryUsageDescriptionDictionary` entry its purpose key must name
-   The services `desiredAccuracy` does and does not affect

### Excluded

-   Obtaining when-in-use or always authorization, and the `CLAuthorizationStatus` values — see `authorization-and-usage-strings`
-   Starting, reading, and stopping the update stream itself — see `location-updates-and-delivery`
-   Configuring and running condition monitoring or significant-change monitoring — see `background-monitoring-and-launches`, which defers the accuracy precondition below back to this contract rather than restating it
-   Beacon ranging (`CLBeacon`, `CLBeaconIdentityCondition`), which is out of this domain's v1 scope entirely

## Rules

### Rule 1

Agents MUST treat `desiredAccuracy` as a request and MUST NOT write logic that assumes the delivered fix meets it. Per Apple's documentation, "The location service does its best to achieve the requested accuracy; however, apps must be prepared to use less accurate data," and "After you request high-accuracy location data, your app might still get data with a lower accuracy for a period of time... the location service keeps providing the data that's available, even though that data isn't as accurate as your app requested."

### Rule 2

Agents MUST set `desiredAccuracy` to the coarsest constant the feature can work with, and MUST NOT leave it at the default on the assumption that the default is neutral — on iOS it is not. Per Apple's documentation, "To reduce your app's impact on battery life, assign a value to this property that's appropriate for your usage. For example, if you need the current location only within a kilometer, specify `kCLLocationAccuracyKilometer`. More accurate location data also takes more time to become available," and "For iOS, the default value of this property is `kCLLocationAccuracyBest`."

### Rule 3

Agents MUST read `accuracyAuthorization` as a separate grant from the authorization status and MUST NOT try to raise it by assigning to `desiredAccuracy`. Per Apple's documentation, `accuracyAuthorization` is "A value that indicates the level of location accuracy the app has permission to use"; when it is `reducedAccuracy`, "setting `desiredAccuracy` to a value other than `kCLLocationAccuracyReduced` has no effect on the location information, and your app can't use region monitoring or beacon ranging." A feature that depends on either of those MUST branch on this value before starting, not after failing.

### Rule 4

Agents MUST request temporary full accuracy only at the moment a feature needs it, and MUST pass a `purposeKey` that names a real entry in the app's `NSLocationTemporaryUsageDescriptionDictionary`. Per Apple's documentation, the parameter is "A key in the `NSLocationTemporaryUsageDescriptionDictionary` dictionary of the app's `Info.plist` file. The value for this key is an app-provided string that describes the reason for accessing location data with full accuracy" — so the dictionary carries one entry per distinct reason, and a key with no matching entry has no string to show. Apple notes the same dictionary is "A collection of messages that explain why the app is requesting temporary access to their location," which is what makes a per-feature key meaningful rather than decorative.

### Rule 5

Agents MUST NOT tune `desiredAccuracy` in the expectation that it changes significant-change delivery. Per Apple's documentation, this property "effects only the standard location services, not for monitoring significant location changes." Accuracy is a lever on one service only; reaching for it to make a background service more precise changes nothing and costs battery in the foreground one.

## Compliant Example

```swift
import CoreLocation
func configure(_ manager: CLLocationManager) async {
    // Rule 2: a delivery-radius feature needs a kilometre, not the iOS default.
    manager.desiredAccuracy = kCLLocationAccuracyKilometer
    // Rule 3: the grant is read, never assumed, and never "raised" by assignment.
    if manager.accuracyAuthorization == .reducedAccuracy {
        // Rule 4: asked here, where the feature needs it -- not at launch.
        manager.requestTemporaryFullAccuracyAuthorization(
            withPurposeKey: "PreciseDropOffPin" // an NSLocationTemporary… entry
        )
    }
}
func isUsable(_ location: CLLocation) -> Bool {
    location.horizontalAccuracy >= 0 // Rule 1: the delivered fix may be coarser
}
```

## Non-Compliant Example

```swift
import CoreLocation
func configure(_ manager: CLLocationManager) {
    manager.desiredAccuracy = kCLLocationAccuracyBestForNavigation // Rule 2
    // Assumes assignment grants precision, so reduced-accuracy users silently get
    // nothing usable and region monitoring is started anyway -- violates Rule 3.
    manager.startMonitoringSignificantLocationChanges()
    // Tuned in the belief it sharpens the significant-change service -- Rule 5.
    manager.desiredAccuracy = kCLLocationAccuracyBest
    // Requested at launch with a key that isn't in the Info.plist dictionary,
    // so there is no message to show -- violates Rule 4.
    manager.requestTemporaryFullAccuracyAuthorization(withPurposeKey: "default")
}
func pin(_ location: CLLocation) -> CLLocation { location } // trusts it -- Rule 1
```
Requests navigation-grade accuracy a delivery feature never needed (Rule 2), treats the assignment as if it granted precision (Rule 3), tunes a property that does not affect the service it started (Rule 5), passes a purpose key with no dictionary entry behind it (Rule 4), and consumes the fix as exact (Rule 1).

## Dependencies

-   `knowledge.core-location.authorization-and-usage-strings` — accuracy authorization is a second grant layered on the authorization status that contract obtains; neither is readable before the other exists.

## References

-   [Apple Developer — desiredAccuracy](https://developer.apple.com/documentation/corelocation/cllocationmanager/desiredaccuracy)
-   [Apple Developer — accuracyAuthorization](https://developer.apple.com/documentation/corelocation/cllocationmanager/accuracyauthorization)
-   [Apple Developer — CLAccuracyAuthorization](https://developer.apple.com/documentation/corelocation/claccuracyauthorization)
-   [Apple Developer — requestTemporaryFullAccuracyAuthorization(withPurposeKey:)](https://developer.apple.com/documentation/corelocation/cllocationmanager/requesttemporaryfullaccuracyauthorization(withpurposekey:))
-   [Apple Developer — kCLLocationAccuracyReduced](https://developer.apple.com/documentation/corelocation/kcllocationaccuracyreduced)
-   [Apple Developer — NSLocationTemporaryUsageDescriptionDictionary](https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationtemporaryusagedescriptiondictionary)
