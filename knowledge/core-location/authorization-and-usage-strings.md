# Authorization and Usage Strings

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.core-location.authorization-and-usage-strings
artifact_type: knowledge
title: Authorization and Usage Strings
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines checking CLAuthorizationStatus, requesting when-in-use before always so the two-prompt Provisional Always flow behaves as intended, and declaring the matching Information Property List keys before any request is made.
domain: Core Location
tags:
  - core-location
  - cllocationmanager
  - clauthorizationstatus
  - authorization
  - info-plist
references:
  - https://developer.apple.com/documentation/corelocation/requesting-authorization-to-use-location-services
  - https://developer.apple.com/documentation/corelocation/clauthorizationstatus
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/authorizationstatus-swift.property
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/requestwheninuseauthorization()
  - https://developer.apple.com/documentation/corelocation/cllocationmanager/requestalwaysauthorization()
  - https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate/locationmanagerdidchangeauthorization(_:)
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationwheninuseusagedescription
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationalwaysandwheninuseusagedescription
depends_on: []
related:
  - knowledge.app-store-review-guidelines.permission-usage-strings
  - knowledge.human-interface-guidelines.privacy
  - knowledge.privacy.collected-data-types-declaration
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent obtains Core Location authorization: reading the current status before requesting anything, choosing the smallest access level the feature needs, ordering the when-in-use and always requests so the second prompt reaches the user at all, and declaring the Information Property List keys that must already be present when the request is made.

## Scope

### Included

-   Reading `CLLocationManager.authorizationStatus`, branching on `CLAuthorizationStatus` (`.notDetermined`, `.restricted`, `.denied`, `.authorizedWhenInUse`, `.authorizedAlways`), and handling later changes in `locationManagerDidChangeAuthorization(_:)`
-   Choosing between `requestWhenInUseAuthorization()` and `requestAlwaysAuthorization()`, the ordering between them, and the Provisional Always state with its deferred second prompt
-   Declaring `NSLocationWhenInUseUsageDescription` and `NSLocationAlwaysAndWhenInUseUsageDescription`

### Excluded

-   Whether the granted authorization is full or reduced accuracy, and asking for full accuracy temporarily — see `accuracy-and-precise-location`
-   Starting, receiving, and stopping location updates once authorized — see `location-updates-and-delivery`
-   Background delivery, condition monitoring, and location-triggered launches — see `background-monitoring-and-launches`
-   How a usage-description string is *worded* to survive App Review — see `knowledge.app-store-review-guidelines.permission-usage-strings`
-   Whether and how to show a pre-permission explanation screen before the system prompt, and its copy — see `knowledge.human-interface-guidelines.privacy`
-   Declaring Location as a collected data type in `PrivacyInfo.xcprivacy` — see `knowledge.privacy.collected-data-types-declaration`

## Rules

### Rule 1

Agents MUST check the current authorization status before placing a request, and MUST NOT treat a request call as a way to read it. Per Apple's documentation, "Before you start any location services, check your app's current authorization status and place an authorization request if needed," and a newly configured `CLLocationManager` "reports your app's current authorization status to its delegate's `locationManagerDidChangeAuthorization(_:)` method automatically" — which is where Apple directs an agent to "place an authorization request when the current status is `notDetermined`." Because people "can change your app's authorization status at any time in system settings," an agent MUST handle the status arriving again later rather than reading it once at launch.

### Rule 2

Agents MUST request When in Use unless the feature demonstrably cannot work without background delivery. Per Apple's documentation, When in Use "is the preferred choice, because it has better privacy and battery life implications," while Always authorization should be requested "only when necessary."

### Rule 3

Agents that need Always authorization MUST call `requestWhenInUseAuthorization()` first and `requestAlwaysAuthorization()` only after When in Use is granted, and MUST NOT call `requestAlwaysAuthorization()` from `.notDetermined` as a shortcut. Per Apple's documentation, "To obtain Always authorization, your app must first request When In Use permission followed by requesting Always authorization," and taking the shortcut does not surface an Always prompt: the first prompt shows the *when-in-use* string, "Allow While Using App" grants only "a Provisional Always authorization," and the second prompt "displays when Core Location prepares to deliver an event to your app requiring `authorizedAlways`" — which Apple notes "will typically display... when your app isn't running."

### Rule 4

Agents MUST treat the Always request as single-use and MUST NOT retry it to recover from a decision. Per Apple's documentation, "Core Location limits calls to `requestAlwaysAuthorization()`. After your app calls this method, further calls have no effect," and the request is valid only from `.notDetermined` or `.authorizedWhenInUse`. A feature that needs Always after a denial MUST route the person to Settings rather than re-prompting.

### Rule 5

Agents MUST add every usage-description key the app's requests require before shipping any code path that requests authorization, and MUST NOT treat a missing key as a degraded prompt. Per Apple's documentation, "Add all usage description keys to your app's Information Property List before you make any authorization requests. Authorization requests fail immediately if the required keys aren't present." Apple further states that "You must include a usage description string for When in Use access. If your app supports Always access, provide an additional string explaining why you want the elevated privileges" — so an Always-capable app declares `NSLocationWhenInUseUsageDescription` *and* `NSLocationAlwaysAndWhenInUseUsageDescription`, the latter being, per its key reference, "required if your iOS app uses APIs that access the user's location information at all times."

### Rule 6

This contract defines *which* key each request requires and *when* it must exist. It defines no rule about how that string is written: the accuracy and specificity every usage-description string must meet is `knowledge.app-store-review-guidelines.permission-usage-strings`, and an agent MUST apply that contract's wording rules to these keys rather than inventing a Core Location-specific wording standard here.

## Compliant Example

```swift
import CoreLocation
final class LocationAuthorization: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    // Rule 2: true only for a feature that cannot work in the foreground alone.
    private let needsBackgroundDelivery = false

    override init() {
        super.init()
        manager.delegate = self // Rule 1: status arrives via the delegate
    }
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization() // Rule 3: always the first step
        case .authorizedWhenInUse where needsBackgroundDelivery:
            manager.requestAlwaysAuthorization() // Rule 3: only after when-in-use
        case .denied, .restricted:
            openSettings() // Rule 4: never re-prompt
        default: break
        }
    }
    private func openSettings() { /* deep-link to Settings */ }
}
// Info.plist declares NSLocationWhenInUseUsageDescription and, because this app can
// ask for Always, NSLocationAlwaysAndWhenInUseUsageDescription (Rule 5).
```

## Non-Compliant Example

```swift
import CoreLocation
let manager = CLLocationManager()

func startTracking() {
    // Never reads authorizationStatus first (Rule 1), and requests Always straight
    // from .notDetermined: the person sees the when-in-use string, grants Provisional
    // Always, and the real prompt is deferred to a moment when the app isn't running
    // (Rule 3). Info.plist declares only the Always key, so the request fails
    // immediately rather than prompting at all (Rule 5).
    manager.requestAlwaysAuthorization()
    manager.startUpdatingLocation()
}
func retryAfterDenial() {
    manager.requestAlwaysAuthorization() // No effect after the first call -- Rule 4.
}
```
Requests Always without reading the status first (Rule 1), skips the when-in-use step so the Always prompt never reaches the user in-session (Rule 3), retries a single-use request (Rule 4), and ships without the key that request requires (Rule 5).

## Dependencies

None within this domain — this is the foundational contract every other Core Location Knowledge Contract assumes access has already been granted correctly.

## References

-   [Apple Developer — Requesting authorization to use location services](https://developer.apple.com/documentation/corelocation/requesting-authorization-to-use-location-services)
-   [Apple Developer — CLAuthorizationStatus](https://developer.apple.com/documentation/corelocation/clauthorizationstatus)
-   [Apple Developer — CLLocationManager.authorizationStatus](https://developer.apple.com/documentation/corelocation/cllocationmanager/authorizationstatus-swift.property)
-   [Apple Developer — requestWhenInUseAuthorization()](https://developer.apple.com/documentation/corelocation/cllocationmanager/requestwheninuseauthorization())
-   [Apple Developer — requestAlwaysAuthorization()](https://developer.apple.com/documentation/corelocation/cllocationmanager/requestalwaysauthorization())
-   [Apple Developer — locationManagerDidChangeAuthorization(_:)](https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate/locationmanagerdidchangeauthorization(_:))
-   [Apple Developer — NSLocationWhenInUseUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationwheninuseusagedescription)
-   [Apple Developer — NSLocationAlwaysAndWhenInUseUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationalwaysandwheninuseusagedescription)
