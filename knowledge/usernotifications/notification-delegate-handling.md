# Notification Delegate Handling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.usernotifications.notification-delegate-handling
artifact_type: knowledge
title: Notification Delegate Handling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct UNUserNotificationCenterDelegate setup timing, foreground presentation via willPresent, and response handling via didReceive.
domain: UserNotifications
tags:
  - usernotifications
  - unusernotificationcenterdelegate
  - delegate
references:
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate/usernotificationcenter(_:willpresent:withcompletionhandler:)
  - https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate/usernotificationcenter(_:didreceive:withcompletionhandler:)
  - https://developer.apple.com/documentation/usernotifications/unnotificationpresentationoptions
depends_on: []
related:
  - knowledge.usernotifications.authorization-request
  - knowledge.usernotifications.remote-push-registration
  - knowledge.usernotifications.notification-actions-and-categories
  - knowledge.human-interface-guidelines.notifications
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent sets up
`UNUserNotificationCenterDelegate` correctly: assigning the delegate
early enough to not miss launch-time interactions, implementing
`willPresent` to choose foreground presentation, and implementing
`didReceive` to process the response and always call its completion
handler. It does not define notification content or badge UX — see
`knowledge.human-interface-guidelines.notifications` for that layer.

## Scope

### Included

-   Assigning an object to `UNUserNotificationCenter.current().delegate`
-   `willPresent(_:withCompletionHandler:)` and `UNNotificationPresentationOptions` selection
-   `didReceive(_:withCompletionHandler:)` — action identifier and completion handler discipline
-   Consequences of not implementing either delegate method

### Excluded

-   Notification content wording, timing judgment, badge UX — see `knowledge.human-interface-guidelines.notifications`
-   Defining `UNNotificationAction`/`UNNotificationCategory` — see `notification-actions-and-categories.md`; requesting authorization/registering for remote notifications — see `authorization-request.md`, `remote-push-registration.md`
-   `UNNotificationServiceExtension`/`UNNotificationContentExtension` (rich media extension delegates) — deferred, out of v1 scope

## Rules

### Rule 1

Agents MUST assign the delegate synchronously within
`application(_:didFinishLaunchingWithOptions:)`, before it returns — per
Apple's `UNUserNotificationCenter` documentation: "Always assign an
object to the delegate property before performing any tasks that might
interact with that delegate." A cold launch triggered by tapping a
notification can invoke delegate methods immediately, so a lazily
assigned delegate can miss that launch's response.

### Rule 2

Agents MUST implement `willPresent(_:withCompletionHandler:)` and always
call back with an explicit `UNNotificationPresentationOptions` value if
foreground presentation is needed — per Apple: "If your delegate does
not implement this method, the system behaves as if you had passed the
`[]` option," meaning no alert, sound, or list entry appears at all for
foreground-delivered notifications otherwise.

### Rule 3

Agents MUST always invoke `completionHandler` in both `willPresent` and
`didReceive`, exactly once, even on early-return/error branches — Apple:
"Always execute this block at some point during your implementation of
this method" (`willPresent`) and "You must execute this block ... to let
the system know that you are done" (`didReceive`). Omitting the call
leaves the system waiting and can delay subsequent handling.

### Rule 4

Agents MUST branch on `response.actionIdentifier` inside `didReceive`
(including the system-defined `UNNotificationDefaultActionIdentifier` for
a tap and `UNNotificationDismissActionIdentifier` for a dismissal) rather
than applying one behavior to every response — per Apple: "Match the
value in the [actionIdentifier] property of the response object to one
of your app's actions or a system-defined action."

### Rule 5

Agents MUST implement `didReceive` if the app registers any custom
`UNNotificationAction` — per Apple: "If you do not implement this
method, your app never responds to custom actions." A category with
actions but no `didReceive` silently drops every action tap.

## Compliant Example

```swift
class NotificationDelegate: NSObject, UNUserNotificationCenterDelegate {
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                 willPresent notification: UNNotification,
                                 withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .sound, .list]) // Explicit options -- Rule 2.
    }
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                 didReceive response: UNNotificationResponse,
                                 withCompletionHandler completionHandler: @escaping () -> Void) {
        switch response.actionIdentifier { // Rule 4.
        case "SNOOZE": snoozeReminder(response.notification)
        default: break
        }
        completionHandler() // Rule 3.
    }
} // Assigned in didFinishLaunchingWithOptions before returning -- Rule 1.
```

## Non-Compliant Example

```swift
class NotificationDelegate: NSObject, UNUserNotificationCenterDelegate {
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                 didReceive response: UNNotificationResponse,
                                 withCompletionHandler completionHandler: @escaping () -> Void) {
        openScreen(for: response) // Ignores actionIdentifier; never calls completionHandler.
    }
    // willPresent not implemented at all.
}
// Delegate assigned inside a view controller's viewDidLoad, long after launch.
```
Omits `willPresent` entirely, so foreground notifications show nothing (Rule 2); never calls `completionHandler` in `didReceive` (Rule 3); ignores `actionIdentifier` (Rule 4); and assigns the delegate too late to catch a launch-time response (Rule 1).

## Dependencies

None.

## References

-   [Apple Developer — UNUserNotificationCenterDelegate](https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate)
-   [Apple Developer — willPresent(_:withCompletionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate/usernotificationcenter(_:willpresent:withcompletionhandler:))
-   [Apple Developer — didReceive(_:withCompletionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate/usernotificationcenter(_:didreceive:withcompletionhandler:))
-   [Apple Developer — UNNotificationPresentationOptions](https://developer.apple.com/documentation/usernotifications/unnotificationpresentationoptions)
