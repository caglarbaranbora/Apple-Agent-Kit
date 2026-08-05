# Status and IDFA Access

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-tracking-transparency.status-and-idfa-access
type: knowledge
title: Status and IDFA Access
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct handling of ATTrackingManagerAuthorizationStatus and ASIdentifierManager.advertisingIdentifier, including the zeroed-UUID fallback and the requirement to read both live rather than cache them.
domain: App Tracking Transparency
tags:
  - app-tracking-transparency
  - idfa
  - authorization-status
references:
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/authorizationstatus
  - https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier
depends_on: []
related:
  - knowledge.app-tracking-transparency.authorization-request
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent interprets
`ATTrackingManagerAuthorizationStatus` and accesses
`ASIdentifierManager.advertisingIdentifier` correctly, so tracking-dependent
code paths are gated on the right status value and never rely on a stale
or incorrectly-cached IDFA.

## Scope

### Included

-   `ATTrackingManagerAuthorizationStatus` values (`.notDetermined`, `.restricted`, `.denied`, `.authorized`) and required agent behavior per value
-   `ASIdentifierManager.advertisingIdentifier` and its zeroed-UUID (`00000000-0000-0000-0000-000000000000`) fallback behavior
-   The requirement to read `advertisingIdentifier` live rather than store it
-   The requirement to re-check `trackingAuthorizationStatus` at each point of use rather than caching a value from launch

### Excluded

-   The `requestTrackingAuthorization` call itself — see `authorization-request`
-   App Store Connect privacy-label tracking-use disclosure — see `knowledge.app-store-review-guidelines.privacy-nutrition-label`

## Rules

### Rule 1

Agents MUST gate any tracking-dependent code path (attaching the IDFA to
an ad request, cross-app/cross-site event correlation, sharing data with
a data broker) on `ATTrackingManager.trackingAuthorizationStatus ==
.authorized` specifically — `.notDetermined`, `.restricted`, and
`.denied` all mean tracking-dependent behavior must not run, even though
they are three semantically distinct states (not yet asked, blocked by
a profile/parental control, and explicitly declined by the user,
respectively).

### Rule 2

Agents MUST NOT treat a zeroed `advertisingIdentifier`
(`00000000-0000-0000-0000-000000000000`) as a valid device identifier —
Apple's documentation lists multiple cases that return an all-zero
value, including "if you haven't requested authorization" and "if you've
requested authorization... and the user declines," alongside Simulator,
macOS, and visionOS-compatibility-mode always returning zeros regardless
of status. Code MUST check `trackingAuthorizationStatus == .authorized`
before treating the value as usable, not just check whether it happens
to be non-zero.

### Rule 3

Agents MUST NOT store or cache `advertisingIdentifier` in
`UserDefaults`, a database, or any persisted model — Apple's
documentation states "as a best practice, don't store the advertising
identifier value; access `advertisingIdentifier` instead," since the
user can change authorization in Settings > Privacy > Tracking at any
time without relaunching the app, which would leave a cached value stale
and pointing at a now-revoked identifier.

### Rule 4

Agents MUST re-check `trackingAuthorizationStatus` at each point of use
(e.g. immediately before constructing an ad request) rather than caching
the status from app launch or from the `requestTrackingAuthorization`
completion handler — the same Settings-change-without-relaunch behavior
from Rule 3 applies to the status value itself, not just the identifier.

## Compliant Example

```swift
func idfaForAdRequest() -> String? {
    guard ATTrackingManager.trackingAuthorizationStatus == .authorized else {
        return nil
    }
    return ASIdentifierManager.shared().advertisingIdentifier.uuidString
}
```
Checks live status immediately before reading the identifier, gates strictly on `.authorized`, and never stores the result. (Rules 1, 3, 4)

## Non-Compliant Example

```swift
class AdConfig {
    static let cachedIDFA = ASIdentifierManager.shared().advertisingIdentifier.uuidString // Read once at launch and cached.

    static func attachTrackingID(to request: inout URLRequest) {
        if cachedIDFA != "00000000-0000-0000-0000-000000000000" {
            request.setValue(cachedIDFA, forHTTPHeaderField: "X-Ad-ID")
        }
    }
}
```
Reads and caches the identifier once at launch instead of live at point of use (Rule 3), and checks only whether the string happens to be non-zero instead of checking `trackingAuthorizationStatus == .authorized` (Rule 2) — if the user revokes tracking permission in Settings after launch, this code keeps sending the stale cached identifier.

## Dependencies

None.

## References

-   [Apple Developer — ATTrackingManager.AuthorizationStatus](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/authorizationstatus)
-   [Apple Developer — advertisingIdentifier](https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier)
