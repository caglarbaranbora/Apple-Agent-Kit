# App Tracking Transparency

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.app-tracking-transparency
artifact_type: reference
title: App Tracking Transparency
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's AppTrackingTransparency and AdSupport framework documentation, scoped to this domain's v1.
domain: App Tracking Transparency
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/adsupport
https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier
https://developer.apple.com/documentation/apptrackingtransparency
https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager
https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/authorizationstatus
https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)
https://developer.apple.com/documentation/bundleresources/information-property-list/nsusertrackingusagedescription

## Purpose

Reference index for Apple's AppTrackingTransparency and AdSupport
framework documentation, scoped to this domain's v1: the tracking
authorization request, authorization status handling, IDFA access, and
the required `NSUserTrackingUsageDescription` Info.plist key. tvOS-specific
behavior, SKAdNetwork, AdServices attribution, custom pre-permission
screen design (owned by `human-interface-guidelines`), and App Store
Connect privacy-label disclosure (owned by `app-store-review-guidelines`)
are out of scope.

## Primary Topics

- Authorization request mechanics
- Authorization status handling
- IDFA access
- Usage string and Info.plist requirement

## Used By

- knowledge/app-tracking-transparency/authorization-request.md ([[knowledge/app-tracking-transparency/authorization-request]])
- knowledge/app-tracking-transparency/status-and-idfa-access.md ([[knowledge/app-tracking-transparency/status-and-idfa-access]])
- knowledge/app-tracking-transparency/usage-string-and-info-plist.md ([[knowledge/app-tracking-transparency/usage-string-and-info-plist]])
