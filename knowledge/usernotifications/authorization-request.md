# Authorization Request

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.usernotifications.authorization-request
artifact_type: knowledge
title: Authorization Request
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of UNUserNotificationCenter.requestAuthorization, UNAuthorizationOptions selection, getNotificationSettings status checks, and provisional authorization.
domain: UserNotifications
tags:
  - usernotifications
  - unusernotificationcenter
  - authorization
references:
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/requestauthorization(options:completionhandler:)
  - https://developer.apple.com/documentation/usernotifications/unauthorizationoptions
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getnotificationsettings(completionhandler:)
  - https://developer.apple.com/documentation/usernotifications/unnotificationsettings
depends_on: []
related:
  - knowledge.usernotifications.remote-push-registration
  - knowledge.usernotifications.local-notification-scheduling
  - knowledge.human-interface-guidelines.notifications
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent requests notification
authorization correctly: selecting `UNAuthorizationOptions` that match
what the app actually uses, checking existing status with
`getNotificationSettings` before deciding whether to prompt, understanding
`requestAuthorization`'s one-time-prompt semantics, and handling
provisional authorization, so the app never issues a redundant request.

## Scope

### Included

-   `UNUserNotificationCenter.requestAuthorization(options:completionHandler:)` call mechanics and one-time-prompt semantics
-   Selecting `UNAuthorizationOptions` (`.alert`, `.sound`, `.badge`, `.provisional`, `.criticalAlert`, `.providesAppNotificationSettings`) that match used features
-   `getNotificationSettings(completionHandler:)` and `UNNotificationSettings.authorizationStatus` as the pre-request check
-   Provisional authorization (`.provisional`) request-time behavior
-   Completion handler threading

### Excluded

-   Deciding when/why to ask and purpose framing — see `knowledge.human-interface-guidelines.notifications`
-   Registering for remote notifications after authorization — see `remote-push-registration.md`
-   Scheduling local notifications — see `local-notification-scheduling.md`
-   The `criticalAlert` entitlement's App Review / provisioning process (the option itself is in scope; the entitlement grant process is not)

## Rules

### Rule 1

Agents MUST treat `requestAuthorization` as effectively one-time per
decision — Apple's documentation states: "The first time your app calls
the method, the system prompts the person to authorize the requested
interactions... Subsequent calls to this method don't prompt the person
again." Code must not assume repeated calls will show additional UI; use
Rule 2 to branch on existing status instead of calling this repeatedly.

### Rule 2

Agents MUST call `getNotificationSettings(completionHandler:)` before
deciding whether to call `requestAuthorization` in any code path that
might run more than once (e.g., a settings screen, a feature entry point
reached repeatedly) — per Apple, use it "to determine the user
interactions and notification-related features that the system
authorizes your app to use," branching on
`UNNotificationSettings.authorizationStatus` rather than calling
`requestAuthorization` unconditionally.

### Rule 3

Agents MUST request only the `UNAuthorizationOptions` the app actually
uses — Apple's documentation states: "Request only the authorization
options that you plan to use." Requesting `.badge` when the app never
badges its icon, or `.criticalAlert` without the entitlement and a
genuine critical-alert use case, is non-compliant.

### Rule 4

Agents MUST NOT perform UI work directly inside `requestAuthorization`'s
or `getNotificationSettings`'s completion handler without dispatching to
the main thread — both documented as "may execute on a background
thread" — any UI mutation must be wrapped in `DispatchQueue.main.async`
or `Task { @MainActor in ... }`.

### Rule 5

Agents MUST treat `.provisional` authorization as its own status, not
equivalent to full `.authorized` — Apple defines it as "the ability to
post noninterrupting notifications provisionally to the Notification
Center," delivered quietly without an alert prompt. Code branching on
authorization status must handle `.provisional` distinctly from
`.authorized`, `.denied`, and `.notDetermined`, not collapse it into a
boolean "granted."

## Compliant Example

```swift
func requestNotificationAuthorizationIfNeeded() {
    UNUserNotificationCenter.current().getNotificationSettings { settings in
        guard settings.authorizationStatus == .notDetermined else {
            return // Already decided -- branch on settings.authorizationStatus instead.
        }
        UNUserNotificationCenter.current().requestAuthorization(
            options: [.alert, .sound, .badge] // Only options this app uses.
        ) { granted, error in
            Task { @MainActor in
                updateUI(granted: granted)
            }
        }
    }
}
```
Checks status first (Rules 1, 2), requests only used options (Rule 3), dispatches UI to main (Rule 4).

## Non-Compliant Example

```swift
func requestNotificationsOnEveryLaunch() {
    UNUserNotificationCenter.current().requestAuthorization(
        options: [.alert, .sound, .badge, .criticalAlert, .providesAppNotificationSettings]
    ) { granted, error in
        updateUI(granted: granted) // Not dispatched to main thread.
    }
}
// Called unconditionally from applicationDidFinishLaunching every launch.
```
Calls `requestAuthorization` unconditionally without checking status (Rules 1, 2), requests unused options like `.criticalAlert` and `.providesAppNotificationSettings` (Rule 3), and updates UI directly from a background-thread completion handler (Rule 4).

## Dependencies

None.

## References

-   [Apple Developer — requestAuthorization(options:completionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/requestauthorization(options:completionhandler:))
-   [Apple Developer — UNAuthorizationOptions](https://developer.apple.com/documentation/usernotifications/unauthorizationoptions)
-   [Apple Developer — getNotificationSettings(completionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getnotificationsettings(completionhandler:))
-   [Apple Developer — UNNotificationSettings](https://developer.apple.com/documentation/usernotifications/unnotificationsettings)
