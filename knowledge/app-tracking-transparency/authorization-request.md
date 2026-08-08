# Authorization Request

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-tracking-transparency.authorization-request
artifact_type: knowledge
title: Authorization Request
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of ATTrackingManager.requestTrackingAuthorization -- one-time-only semantics, the .active-state requirement, and pre-call status checks.
domain: App Tracking Transparency
tags:
  - app-tracking-transparency
  - attrackingmanager
  - authorization
references:
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)
depends_on: []
related:
  - knowledge.app-tracking-transparency.status-and-idfa-access
  - knowledge.app-tracking-transparency.usage-string-and-info-plist
  - knowledge.human-interface-guidelines.privacy
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent calls
`ATTrackingManager.requestTrackingAuthorization` correctly: understanding
its one-time-only semantics, the conditions under which it will and won't
display a prompt, and checking status before calling it again, so the
app never issues a redundant or silently-ignored authorization request.

## Scope

### Included

-   `ATTrackingManager.requestTrackingAuthorization(completionHandler:)` call mechanics
-   One-time-only semantics: the system remembers the user's decision and doesn't re-prompt unless the app is uninstalled and reinstalled
-   The `UIApplicationState.active` requirement for the prompt to display
-   Pending-prompt, concurrent-call, and app-extension edge cases
-   Checking `trackingAuthorizationStatus == .notDetermined` before calling again
-   Dispatching the completion handler's UI work back to the main queue

### Excluded

-   Custom pre-permission screen design, request timing/UX judgment, purpose-string design conventions — see `knowledge.human-interface-guidelines.privacy`
-   Interpreting the resulting `ATTrackingManagerAuthorizationStatus` value and gating IDFA access on it — see `status-and-idfa-access`
-   The `NSUserTrackingUsageDescription` Info.plist key itself — see `usage-string-and-info-plist`

## Rules

### Rule 1

Agents MUST call `requestTrackingAuthorization` at most once per
authorization decision — Apple's documentation states it "is a one-time
request to authorize or deny access to app-related data that can be used
for tracking the user or the device. The system remembers the user's
choice and doesn't prompt again unless a user uninstalls and then
reinstalls the app on the device." Calling it again after a decision has
been made does not re-prompt; it simply invokes the completion handler
with the existing status.

### Rule 2

Agents MUST check `ATTrackingManager.trackingAuthorizationStatus ==
.notDetermined` before calling `requestTrackingAuthorization` again in
any code path that might run more than once (e.g. a settings screen with
a "Manage Tracking" button, or a feature entry point reached multiple
times per session) — calling it when status is already
`.authorized`/`.denied`/`.restricted` wastes a call for no effect, since
Rule 1 guarantees no new prompt appears.

### Rule 3

Agents MUST NOT assume `requestTrackingAuthorization` will display a
prompt in every call — per Apple's documentation, "calls to the API only
prompt when the application state is `UIApplicationStateActive`. The
authorization prompt doesn't display if another permission request is
pending user confirmation... and calls to the API through an app
extension don't prompt." Code that calls this from a background task, a
notification-response handler before the app becomes active, or an app
extension must not assume a completion handler result means the user was
actually shown anything.

### Rule 4

Agents MUST dispatch UI updates inside `requestTrackingAuthorization`'s
completion handler back to the main queue — the completion handler is
not guaranteed to run on the main thread, and any UI mutation (enabling
a feature, updating a label) triggered directly from it must be wrapped
in `DispatchQueue.main.async` or use the `async` `Task { @MainActor in
... }` pattern.

## Compliant Example

```swift
func requestTrackingIfNeeded() {
    guard ATTrackingManager.trackingAuthorizationStatus == .notDetermined else {
        return // Already decided -- see status-and-idfa-access.md for handling existing status.
    }

    ATTrackingManager.requestTrackingAuthorization { status in
        Task { @MainActor in
            updateUI(for: status)
        }
    }
}
```
Checks `.notDetermined` before calling (Rule 2), and dispatches the resulting UI update back to the main actor (Rule 4). (Rules 2, 4)

## Non-Compliant Example

```swift
func showTrackingPromptOnEveryLaunch() {
    ATTrackingManager.requestTrackingAuthorization { status in
        updateUI(for: status) // Called directly from the completion handler -- not guaranteed to be on the main thread.
    }
}
// Called unconditionally from applicationDidBecomeActive every launch.
```
Calls `requestTrackingAuthorization` unconditionally on every launch without checking status first (wasted call once a decision exists, Rule 2), and updates UI directly from the completion handler without dispatching to the main queue (Rule 4).

## Dependencies

None.

## References

-   [Apple Developer — ATTrackingManager](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager)
-   [Apple Developer — requestTrackingAuthorization(completionHandler:)](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:))
