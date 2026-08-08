---
name: core-location
description: Route Core Location implementation tasks to the correct Knowledge Contracts -- authorization and usage strings, location updates and delivery, accuracy and precise location, and background monitoring with location-triggered launches. Use when reading CLAuthorizationStatus or authorizationStatus, calling requestWhenInUseAuthorization()/requestAlwaysAuthorization(), declaring NSLocationWhenInUseUsageDescription/NSLocationAlwaysAndWhenInUseUsageDescription/NSLocationTemporaryUsageDescriptionDictionary, iterating CLLocationUpdate.liveUpdates or implementing locationManager(_:didUpdateLocations:), setting desiredAccuracy or handling CLAccuracyAuthorization.reducedAccuracy, or enabling allowsBackgroundLocationUpdates, startMonitoringSignificantLocationChanges(), and CLMonitor condition monitoring. v1 is location access and delivery only -- no CLGeocoder forward/reverse geocoding, no beacon ranging, no heading or CLVisit, and no map display (that belongs to a future mapkit domain, not yet built). Triggers on Core Location, CLLocationManager, CLLocationUpdate, CLAuthorizationStatus, CLAccuracyAuthorization, CLMonitor, CLCircularGeographicCondition, desiredAccuracy, allowsBackgroundLocationUpdates, significant location change, geofence, region monitoring, location permission, precise location.
id: skill.core-location.foundations
title: Core Location — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Core Location
routes: [knowledge.core-location.authorization-and-usage-strings, knowledge.core-location.location-updates-and-delivery, knowledge.core-location.accuracy-and-precise-location, knowledge.core-location.background-monitoring-and-launches]
related: []
last_updated: 2026-08-09
---

# Core Location — Foundations Skill

## Purpose

Route Core Location implementation tasks to the minimum required Core
Location Knowledge Contracts. v1 scope is obtaining location access and
receiving location: authorization levels and their Information Property
List keys, the two delivery mechanisms, requested versus granted
accuracy, and running outside the foreground — not geocoding, not
beacons, not heading or visits, and not drawing a location on a map.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/core-location/.

-   Reading `authorizationStatus`/`CLAuthorizationStatus`; calling `requestWhenInUseAuthorization()`/`requestAlwaysAuthorization()`; handling `locationManagerDidChangeAuthorization(_:)`; or declaring `NSLocationWhenInUseUsageDescription`/`NSLocationAlwaysAndWhenInUseUsageDescription` -> authorization-and-usage-strings.md
-   Iterating `CLLocationUpdate.liveUpdates(_:)`; calling `startUpdatingLocation()`/`stopUpdatingLocation()`; implementing `locationManager(_:didUpdateLocations:)`/`locationManager(_:didFailWithError:)`; or reading a fix's `timestamp` -> location-updates-and-delivery.md
-   Setting `desiredAccuracy`; branching on `accuracyAuthorization`/`CLAccuracyAuthorization`; or calling `requestTemporaryFullAccuracyAuthorization(withPurposeKey:)` with its `NSLocationTemporaryUsageDescriptionDictionary` entry -> accuracy-and-precise-location.md
-   Setting `allowsBackgroundLocationUpdates` with `UIBackgroundModes`; calling `startMonitoringSignificantLocationChanges()`; building a geofence with `CLMonitor`/`CLCircularGeographicCondition`; or handling a location-triggered relaunch -> background-monitoring-and-launches.md

Never load more than the contracts relevant to the specific question.
For how a usage-description string should be *worded*, route to
`skill.app-store-review-guidelines.submission`. For whether to show a
pre-permission screen and what it says, route to
`skill.human-interface-guidelines.foundations`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/core-location/ — do not guess or fall back to
general knowledge. `CLGeocoder` forward and reverse geocoding, beacon
ranging (`CLBeacon`, `CLBeaconIdentityCondition`), heading
(`CLHeading`), visit monitoring (`CLVisit`), and `LocationButton` are
out of scope entirely (see docs/architecture/domain-map.md). The
deprecated `startMonitoring(for:)` region API is not covered; condition
monitoring is `CLMonitor`'s.

Displaying a location on a map belongs to a future map-rendering
domain, not yet built — report that boundary explicitly rather than
answering from general knowledge.

Scheduling background work with `BGTaskScheduler` is `backgroundtasks`'
job. The one place the two meet — whether a movement-triggered feature
should use a scheduled task at all — is answered by
background-monitoring-and-launches.md here, which owns that decision;
everything else about `BGTask` belongs to that Skill.
