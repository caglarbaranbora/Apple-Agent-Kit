# Core Location

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.core-location
artifact_type: reference
title: Core Location
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's Core Location documentation, scoped to this domain's v1.
domain: Core Location
last_updated: 2026-08-09
```

## Source

https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationalwaysandwheninuseusagedescription
https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationtemporaryusagedescriptiondictionary
https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationwheninuseusagedescription
https://developer.apple.com/documentation/bundleresources/information-property-list/uibackgroundmodes
https://developer.apple.com/documentation/corelocation
https://developer.apple.com/documentation/corelocation/claccuracyauthorization
https://developer.apple.com/documentation/corelocation/clauthorizationstatus
https://developer.apple.com/documentation/corelocation/clcirculargeographiccondition
https://developer.apple.com/documentation/corelocation/cllocation
https://developer.apple.com/documentation/corelocation/cllocationmanager
https://developer.apple.com/documentation/corelocation/cllocationmanager/accuracyauthorization
https://developer.apple.com/documentation/corelocation/cllocationmanager/allowsbackgroundlocationupdates
https://developer.apple.com/documentation/corelocation/cllocationmanager/authorizationstatus-swift.property
https://developer.apple.com/documentation/corelocation/cllocationmanager/desiredaccuracy
https://developer.apple.com/documentation/corelocation/cllocationmanager/requestalwaysauthorization()
https://developer.apple.com/documentation/corelocation/cllocationmanager/requesttemporaryfullaccuracyauthorization(withpurposekey:)
https://developer.apple.com/documentation/corelocation/cllocationmanager/requestwheninuseauthorization()
https://developer.apple.com/documentation/corelocation/cllocationmanager/startmonitoringsignificantlocationchanges()
https://developer.apple.com/documentation/corelocation/cllocationmanager/startupdatinglocation()
https://developer.apple.com/documentation/corelocation/cllocationmanager/stopupdatinglocation()
https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate/locationmanager(_:didupdatelocations:)
https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate/locationmanagerdidchangeauthorization(_:)
https://developer.apple.com/documentation/corelocation/cllocationupdate
https://developer.apple.com/documentation/corelocation/cllocationupdate/liveupdates(_:)
https://developer.apple.com/documentation/corelocation/clmonitor-2r51v
https://developer.apple.com/documentation/corelocation/clmonitor-2r51v/circulargeographiccondition
https://developer.apple.com/documentation/corelocation/kcllocationaccuracyreduced
https://developer.apple.com/documentation/corelocation/monitoring-the-user-s-proximity-to-geographic-regions
https://developer.apple.com/documentation/corelocation/requesting-authorization-to-use-location-services

## Purpose

Reference index for Apple's Core Location documentation, scoped to this domain's v1: requesting authorization through `CLLocationManager` (`CLAuthorizationStatus`, the `authorizationStatus` property, `locationManagerDidChangeAuthorization(_:)`, and the ordering constraint between `requestWhenInUseAuthorization()` and `requestAlwaysAuthorization()` that produces the two-prompt Provisional Always flow); declaring the matching Information Property List keys (`NSLocationWhenInUseUsageDescription`, `NSLocationAlwaysAndWhenInUseUsageDescription`, `NSLocationTemporaryUsageDescriptionDictionary`); receiving updates through either `CLLocationUpdate.liveUpdates(_:)` or the `CLLocationManagerDelegate` pair `startUpdatingLocation()`/`locationManager(_:didUpdateLocations:)`; requesting accuracy (`desiredAccuracy`, `kCLLocationAccuracyReduced`) and handling the reduced-accuracy grant (`accuracyAuthorization`, `CLAccuracyAuthorization`, `requestTemporaryFullAccuracyAuthorization(withPurposeKey:)`); and running without the app in the foreground — `allowsBackgroundLocationUpdates` with the `UIBackgroundModes` `location` value, `startMonitoringSignificantLocationChanges()`, and condition monitoring with `CLMonitor`/`CLCircularGeographicCondition`, including the relaunches each of those produces.

Out of scope for v1: `CLGeocoder` forward and reverse geocoding; beacon ranging (`CLBeacon`, `CLBeaconIdentityCondition`) and iBeacon; heading and course (`CLHeading`, `startUpdatingHeading()`); visit monitoring (`CLVisit`); `CLLocationButton`/`LocationButton` as a UI component; the deprecated `startMonitoring(for:)` region API superseded by `CLMonitor`; and displaying a location on a map, which belongs to a future map-rendering domain rather than this one.

## Primary Topics

- Authorization levels, the two-prompt Always flow, and usage-description keys
- Location delivery: the `CLLocationUpdate` async sequence and the delegate path
- Requested accuracy versus granted accuracy authorization
- Background monitoring, condition monitoring, and location-triggered launches

## Used By

- knowledge/core-location/authorization-and-usage-strings.md ([[knowledge/core-location/authorization-and-usage-strings]])
- knowledge/core-location/location-updates-and-delivery.md ([[knowledge/core-location/location-updates-and-delivery]])
- knowledge/core-location/accuracy-and-precise-location.md ([[knowledge/core-location/accuracy-and-precise-location]])
- knowledge/core-location/background-monitoring-and-launches.md ([[knowledge/core-location/background-monitoring-and-launches]])
