# App Tracking Transparency

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.app-tracking-transparency
artifact_type: reference
title: App Tracking Transparency
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's AppTrackingTransparency and AdSupport framework documentation, scoped to this domain's v1.
domain: App Tracking Transparency
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/apptrackingtransparency
https://developer.apple.com/documentation/adsupport

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
