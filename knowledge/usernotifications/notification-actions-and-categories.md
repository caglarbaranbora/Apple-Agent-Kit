# Notification Actions and Categories

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.usernotifications.notification-actions-and-categories
artifact_type: knowledge
title: Notification Actions and Categories
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct definition and registration of UNNotificationAction, UNTextInputNotificationAction, and UNNotificationCategory via setNotificationCategories.
domain: UserNotifications
tags:
  - usernotifications
  - unnotificationaction
  - unnotificationcategory
references:
  - https://developer.apple.com/documentation/usernotifications/unnotificationaction
  - https://developer.apple.com/documentation/usernotifications/untextinputnotificationaction
  - https://developer.apple.com/documentation/usernotifications/unnotificationcategory
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/setnotificationcategories(_:)
depends_on: []
related:
  - knowledge.usernotifications.local-notification-scheduling
  - knowledge.usernotifications.notification-delegate-handling
  - knowledge.human-interface-guidelines.notifications
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent defines `UNNotificationAction`
and `UNTextInputNotificationAction` objects, groups them into
`UNNotificationCategory` objects, and registers those categories via
`setNotificationCategories(_:)`, so actionable notifications present the
correct buttons and remain wired to content correctly. It does not define
how many actions to offer or their labeling/destructiveness judgment —
see `knowledge.human-interface-guidelines.notifications` for that layer.

## Scope

### Included

-   `UNNotificationAction`/`UNTextInputNotificationAction` construction
-   `UNNotificationCategory` construction and its `identifier`
-   `setNotificationCategories(_:)` registration timing and replace-all semantics
-   Linking a category to content via `UNMutableNotificationContent.categoryIdentifier`
-   Action-count display limits

### Excluded

-   Action count, labeling, destructiveness, and icon design judgment — see `knowledge.human-interface-guidelines.notifications`
-   Handling the selected action once tapped (`didReceive`) — see `notification-delegate-handling.md`
-   Building the `UNMutableNotificationContent` itself — see `local-notification-scheduling.md`
-   Custom notification UI via `UNNotificationContentExtension` — deferred, out of v1 scope

## Rules

### Rule 1

Agents MUST register all of an app's notification categories in a single
`setNotificationCategories(_:)` call, typically at launch — per Apple:
"This method registers all of your categories at once, replacing any
previously registered categories with the new ones... Typically, you
call this method only once." Calling it multiple times with partial sets
across the app's lifetime silently drops previously registered categories
not included in the latest call.

### Rule 2

Agents MUST assign a unique, stable `identifier` to each
`UNNotificationCategory` and set the matching value on
`UNMutableNotificationContent.categoryIdentifier` for any content meant
to use it — per Apple: "the system looks in the notification payload for
one of the identifier strings from your category objects. If it finds
one, it adds user-selectable buttons for each action." A content object
with no matching `categoryIdentifier`, or a typo'd one, displays no
actions.

### Rule 3

Agents MUST account for the system's action display limits when designing
a category's action list — per Apple: "When the system has unlimited
space, the system displays up to 10 actions. When the system has limited
space, the system displays at most two actions." Code that assumes all
registered actions are always visible must instead order actions by
priority, since only the first ones may render in constrained contexts.

### Rule 4

Agents MUST call `setNotificationCategories(_:)` before any notification
using those categories can be scheduled or received with working actions
— since action buttons render from the payload's `categoryIdentifier`
matched against currently registered categories, registering categories
after scheduling (or not at app launch) risks a notification arriving
with no matching registered category yet.

### Rule 5

Agents MUST use `UNTextInputNotificationAction`, not a plain
`UNNotificationAction`, when the action needs a free-text or dictated
reply — per Apple: "the system displays controls for the user to enter
or dictate the text content. That text is then included in the response
object," available via `UNTextInputNotificationResponse.userText` in
`didReceive`, not on a plain response.

## Compliant Example

```swift
let reply = UNTextInputNotificationAction(identifier: "REPLY", title: "Reply", options: [])
let snooze = UNNotificationAction(identifier: "SNOOZE", title: "Snooze", options: [])
let category = UNNotificationCategory(identifier: "MEETING", actions: [reply, snooze],
                                       intentIdentifiers: [], options: [])

UNUserNotificationCenter.current().setNotificationCategories([category]) // All categories, once, at launch.

let content = UNMutableNotificationContent()
content.categoryIdentifier = "MEETING" // Matches the registered category -- Rule 2.
```

## Non-Compliant Example

```swift
func addSnoozeCategory() {
    let snooze = UNNotificationCategory(identifier: "SNOOZE_ONLY",
                                         actions: [UNNotificationAction(identifier: "SNOOZE", title: "Snooze", options: [])],
                                         intentIdentifiers: [], options: [])
    UNUserNotificationCenter.current().setNotificationCategories([snooze]) // Called again later, dropping other categories -- Rule 1.
}
// content.categoryIdentifier left unset elsewhere, so no actions ever appear -- Rule 2.
```

## Dependencies

None.

## References

-   [Apple Developer — UNNotificationAction](https://developer.apple.com/documentation/usernotifications/unnotificationaction)
-   [Apple Developer — UNTextInputNotificationAction](https://developer.apple.com/documentation/usernotifications/untextinputnotificationaction)
-   [Apple Developer — UNNotificationCategory](https://developer.apple.com/documentation/usernotifications/unnotificationcategory)
-   [Apple Developer — setNotificationCategories(_:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/setnotificationcategories(_:))
