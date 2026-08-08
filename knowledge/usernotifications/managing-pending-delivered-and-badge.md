# Managing Pending, Delivered, and Badge

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.usernotifications.managing-pending-delivered-and-badge
artifact_type: knowledge
title: Managing Pending, Delivered, and Badge
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of removePendingNotificationRequests, removeDeliveredNotifications, getPendingNotificationRequests, getDeliveredNotifications, and badge-count APIs.
domain: UserNotifications
tags:
  - usernotifications
  - unusernotificationcenter
  - badge
references:
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/removependingnotificationrequests(withidentifiers:)
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/removedeliverednotifications(withidentifiers:)
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getpendingnotificationrequests(completionhandler:)
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getdeliverednotifications(completionhandler:)
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/setbadgecount(_:withcompletionhandler:)
depends_on: []
related:
  - knowledge.usernotifications.local-notification-scheduling
  - knowledge.human-interface-guidelines.notifications
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent inspects and cleans up
pending/delivered local notifications, and sets the app icon's badge
count, using the correct API for the deployment target. It does not
define when a badge should be shown or what it should represent as a
UX decision — see `knowledge.human-interface-guidelines.notifications`.

## Scope

### Included

-   `getPendingNotificationRequests(completionHandler:)` / `getDeliveredNotifications(completionHandler:)`
-   `removePendingNotificationRequests(withIdentifiers:)` / `removeDeliveredNotifications(withIdentifiers:)`
-   `UNUserNotificationCenter.setBadgeCount(_:withCompletionHandler:)` (iOS 16+) vs. legacy `UIApplication.shared.applicationIconBadgeNumber` (deprecated iOS 17)
-   Identifier-array targeting semantics for the remove methods

### Excluded

-   What the badge count should represent and when to clear it as a UX decision — see `knowledge.human-interface-guidelines.notifications`
-   Constructing the `UNNotificationRequest`/identifier scheme itself — see `local-notification-scheduling.md`
-   Remote-notification-driven badge updates via the APNs payload's `badge` key — server-side, out of v1 scope

## Rules

### Rule 1

Agents MUST pass identifiers to `removePendingNotificationRequests` and
`removeDeliveredNotifications` that match the `identifier` used when the
request was created — both methods "ignore" identifiers that don't
correspond to a currently pending or displayed item (per Apple: a
non-repeating request whose trigger has already fired is ignored by the
pending-removal call; notifications not currently in Notification Center
are ignored by the delivered-removal call). Passing stale or guessed
identifiers silently does nothing rather than erroring.

### Rule 2

Agents MUST treat `getPendingNotificationRequests` and
`getDeliveredNotifications` completion handlers as running on a
background thread — both are documented as possibly executing "on a
background thread" — and MUST dispatch any resulting UI update to the
main thread rather than mutating UI directly inside the handler.

### Rule 3

Agents targeting iOS 16 or later MUST use
`UNUserNotificationCenter.setBadgeCount(_:withCompletionHandler:)` (or
its `async throws` overload) to set the badge, not
`UIApplication.shared.applicationIconBadgeNumber` — Apple deprecated
`applicationIconBadgeNumber` as of iOS 17, and `setBadgeCount` has been
available since iOS 16.0/macOS 13.0. `applicationIconBadgeNumber` remains
the only option for code that must also run on iOS versions below 16.

### Rule 4

Agents MUST check the `Error?` passed to `setBadgeCount`'s completion
handler (or catch the thrown error on the `async throws` overload) — per
Apple: "If the update fails, the system provides an error that contains
additional information about the failure." A badge-count update that
silently fails leaves the icon showing a stale count with no indication
to the app.

### Rule 5

Agents MUST NOT assume `getPendingNotificationRequests` reflects
notifications already delivered, or that `getDeliveredNotifications`
reflects notifications still pending — a request moves from the pending
set to the delivered set once its trigger fires and the system presents
it; code that needs the full picture (e.g., a "clear all" feature) must
query and clear both sets, not just one.

## Compliant Example

```swift
func clearAllReminderNotifications() {
    let center = UNUserNotificationCenter.current()
    center.getPendingNotificationRequests { requests in
        let ids = requests.map(\.identifier)
        center.removePendingNotificationRequests(withIdentifiers: ids) // Rule 1.
    }
    center.getDeliveredNotifications { notifications in
        let ids = notifications.map { $0.request.identifier }
        center.removeDeliveredNotifications(withIdentifiers: ids) // Rule 5: both sets.
    }
    center.setBadgeCount(0) { error in
        if let error { logBadgeFailure(error) } // Rule 4.
    }
}
```

## Non-Compliant Example

```swift
func clearBadgeOnly() {
    UIApplication.shared.applicationIconBadgeNumber = 0 // Deprecated on iOS 17+ targets -- Rule 3.
    // Pending requests never queried or removed; delivered notifications untouched -- Rule 5.
}
```

## Dependencies

None.

## References

-   [Apple Developer — removePendingNotificationRequests(withIdentifiers:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/removependingnotificationrequests(withidentifiers:))
-   [Apple Developer — removeDeliveredNotifications(withIdentifiers:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/removedeliverednotifications(withidentifiers:))
-   [Apple Developer — setBadgeCount(_:withCompletionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/setbadgecount(_:withcompletionhandler:))
-   [Apple Developer — applicationIconBadgeNumber](https://developer.apple.com/documentation/uikit/uiapplication/applicationiconbadgenumber)
