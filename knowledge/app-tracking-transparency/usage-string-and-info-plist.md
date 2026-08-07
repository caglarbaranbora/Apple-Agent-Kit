# Usage String and Info.plist

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-tracking-transparency.usage-string-and-info-plist
artifact_type: knowledge
title: Usage String and Info.plist
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the required NSUserTrackingUsageDescription Info.plist key and its wording rules, without which requestTrackingAuthorization fails at runtime.
domain: App Tracking Transparency
tags:
  - app-tracking-transparency
  - info-plist
  - nsusertrackingusagedescription
references:
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsusertrackingusagedescription
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)
depends_on: []
related:
  - knowledge.app-tracking-transparency.authorization-request
  - knowledge.app-store-review-guidelines.permission-usage-strings
last_updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent configures the required
`NSUserTrackingUsageDescription` Info.plist key, so a call to
`requestTrackingAuthorization` has task-specific copy and doesn't fail
at runtime.

## Scope

### Included

-   `NSUserTrackingUsageDescription` as a required Info.plist key before calling `requestTrackingAuthorization`
-   Wording rules: specific, explains the actual tracking use, not a generic placeholder

### Excluded

-   General Info.plist permission-usage-string conventions not specific to ATT — see `knowledge.app-store-review-guidelines.permission-usage-strings`
-   The `requestTrackingAuthorization` call mechanics themselves — see `authorization-request`

## Rules

### Rule 1

Agents MUST add an `NSUserTrackingUsageDescription` key with a non-empty
string value to the app's Info.plist before shipping any code path that
calls `requestTrackingAuthorization` — Apple's documentation states that
"to use `requestTrackingAuthorization(completionHandler:)`, the
`NSUserTrackingUsageDescription` key must be in the Information Property
List." Omitting this key is not a degraded-prompt situation; the
authorization request fails outright.

### Rule 2

Agents MUST write `NSUserTrackingUsageDescription`'s value as a
specific, task-grounded sentence describing the actual tracking use
(e.g. "Your data will be used to deliver personalized ads and measure
their effectiveness."), not a generic placeholder like "This app uses
tracking" — the same accuracy standard `permission-usage-strings.md`
applies to other Info.plist usage-description keys applies here.

### Rule 3

Agents MUST NOT write `NSUserTrackingUsageDescription` copy that
implies tracking is required for the app to function, when it is not —
the string should describe what tracking-dependent features (e.g.
personalized ads) do, not pressure the user into granting a permission
that is genuinely optional for the app's core functionality.

## Compliant Example

```xml
<!-- Info.plist -->
<key>NSUserTrackingUsageDescription</key>
<string>Your data will be used to deliver personalized ads and measure their effectiveness.</string>
```
```swift
ATTrackingManager.requestTrackingAuthorization { status in
    Task { @MainActor in
        updateUI(for: status)
    }
}
```
The usage string is specific about what tracking is used for, and the app calls `requestTrackingAuthorization` only after this key is present. (Rules 1, 2)

## Non-Compliant Example

```xml
<!-- Info.plist has no NSUserTrackingUsageDescription entry at all. -->
```
```swift
ATTrackingManager.requestTrackingAuthorization { status in
    updateUI(for: status)
}
```
Missing `NSUserTrackingUsageDescription` causes `requestTrackingAuthorization` to fail the first time this line runs. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — NSUserTrackingUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsusertrackingusagedescription)
-   [Apple Developer — requestTrackingAuthorization(completionHandler:)](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:))
