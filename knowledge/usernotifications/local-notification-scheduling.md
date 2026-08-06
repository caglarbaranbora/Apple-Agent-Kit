# Local Notification Scheduling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.usernotifications.local-notification-scheduling
type: knowledge
title: Local Notification Scheduling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct construction and scheduling of local notifications via UNMutableNotificationContent, UNNotificationRequest, UNTimeIntervalNotificationTrigger, UNCalendarNotificationTrigger, and UNUserNotificationCenter.add.
domain: UserNotifications
tags:
  - usernotifications
  - unnotificationrequest
  - local-notifications
references:
  - https://developer.apple.com/documentation/usernotifications/unmutablenotificationcontent
  - https://developer.apple.com/documentation/usernotifications/unnotificationrequest
  - https://developer.apple.com/documentation/usernotifications/untimeintervalnotificationtrigger
  - https://developer.apple.com/documentation/usernotifications/uncalendarnotificationtrigger
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/add(_:withcompletionhandler:)
depends_on: []
related:
  - knowledge.usernotifications.authorization-request
  - knowledge.usernotifications.managing-pending-delivered-and-badge
  - knowledge.usernotifications.notification-actions-and-categories
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent constructs and schedules a
local notification: building `UNMutableNotificationContent`, choosing a
stable `UNNotificationRequest` identifier, configuring
`UNTimeIntervalNotificationTrigger` or `UNCalendarNotificationTrigger`
within their documented constraints, and calling
`UNUserNotificationCenter.add` correctly, so requests fire as intended and
can be individually managed later.

## Scope

### Included

-   `UNMutableNotificationContent` construction (title, body, sound, badge, categoryIdentifier, userInfo, threadIdentifier)
-   `UNNotificationRequest` identifier semantics for later targeting/replacement
-   `UNTimeIntervalNotificationTrigger` interval and `repeats` constraints
-   `UNCalendarNotificationTrigger` `dateComponents`/`repeats` configuration
-   `UNUserNotificationCenter.add(_:withCompletionHandler:)` call mechanics, threading, and error handling

### Excluded

-   Requesting authorization before scheduling — see `authorization-request.md`
-   Assigning `UNNotificationAction`/`UNNotificationCategory` content — see `notification-actions-and-categories.md`
-   Removing/inspecting pending requests after scheduling — see `managing-pending-delivered-and-badge.md`
-   `UNLocationNotificationTrigger` (CoreLocation-dependent triggers) — deferred, out of v1 scope
-   Remote/push notification payload construction — see `remote-push-registration.md` and APNs server-side docs (out of scope)

## Rules

### Rule 1

Agents MUST give every `UNNotificationRequest` a stable, unique
`identifier` chosen deliberately (not a fresh random value per call when
the intent is to update an existing request) — per Apple, "You can use
this identifier to cancel the request if it's still pending," and
scheduling a new request with an identifier matching a currently pending
one replaces that pending request rather than creating a duplicate.
Random per-call identifiers make later targeted removal impossible.

### Rule 2

Agents MUST NOT set `timeInterval` to zero or a negative value on
`UNTimeIntervalNotificationTrigger` — Apple's documentation states "This
value must be greater than zero" — and MUST use `timeInterval >= 60` when
`repeats` is `true`, since "If [repeats] is true, the value in the
timeInterval parameter must be 60 seconds or greater."

### Rule 3

Agents MUST explicitly remove a repeating `UNTimeIntervalNotificationTrigger`
request when it's no longer needed — per Apple: "If you specify `true`
for the `repeats` parameter, you must explicitly remove the notification
request to stop the delivery of the associated notification" — via
`removePendingNotificationRequests(withIdentifiers:)` (see
`managing-pending-delivered-and-badge.md`).

### Rule 4

Agents MUST treat `add(_:withCompletionHandler:)`'s completion handler as
possibly running on a background thread ("This block may be executed on
a background thread") and MUST check the handler's `Error?` parameter —
scheduling failures (e.g., malformed content) surface only there, not as
a thrown error at the call site.

### Rule 5

Agents MUST NOT pass a `nil` trigger when a delayed delivery is intended
— per Apple, "If the request does not contain a trigger object, the
notification is delivered right away." A `nil` trigger is only correct
when immediate delivery is the actual intent.

## Compliant Example

```swift
func scheduleReminder(id: String, after seconds: TimeInterval) {
    let content = UNMutableNotificationContent()
    content.title = "Reminder"
    content.body = "Check your task."
    content.sound = .default

    let trigger = UNTimeIntervalNotificationTrigger(timeInterval: max(seconds, 1), repeats: false)
    let request = UNNotificationRequest(identifier: id, content: content, trigger: trigger)

    UNUserNotificationCenter.current().add(request) { error in
        if let error { logSchedulingFailure(error) } // Rule 4
    }
}
```
Uses a stable caller-supplied `identifier` (Rule 1), a positive `timeInterval` (Rule 2), and checks the completion handler's error (Rule 4).

## Non-Compliant Example

```swift
func scheduleReminder(after seconds: TimeInterval) {
    let content = UNMutableNotificationContent()
    content.body = "Check your task."

    let trigger = UNTimeIntervalNotificationTrigger(timeInterval: seconds, repeats: true) // May be < 60s.
    let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)

    UNUserNotificationCenter.current().add(request) { _ in } // Error ignored.
}
```
Uses a random identifier that prevents later removal (Rule 1), a repeating trigger that may be under 60 seconds (Rule 2), never removes the repeating request (Rule 3), and discards the completion handler's error (Rule 4).

## Dependencies

None.

## References

-   [Apple Developer — UNMutableNotificationContent](https://developer.apple.com/documentation/usernotifications/unmutablenotificationcontent)
-   [Apple Developer — UNNotificationRequest](https://developer.apple.com/documentation/usernotifications/unnotificationrequest)
-   [Apple Developer — UNTimeIntervalNotificationTrigger](https://developer.apple.com/documentation/usernotifications/untimeintervalnotificationtrigger)
-   [Apple Developer — UNCalendarNotificationTrigger](https://developer.apple.com/documentation/usernotifications/uncalendarnotificationtrigger)
-   [Apple Developer — add(_:withCompletionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/add(_:withcompletionhandler:))
