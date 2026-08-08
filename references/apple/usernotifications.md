# UserNotifications

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.usernotifications
artifact_type: reference
title: UserNotifications
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's UserNotifications framework documentation, scoped to this domain's v1.
domain: UserNotifications
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/uikit/uiapplication/registerforremotenotifications()
https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didfailtoregisterforremotenotificationswitherror:)
https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didregisterforremotenotificationswithdevicetoken:)
https://developer.apple.com/documentation/usernotifications
https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns
https://developer.apple.com/documentation/usernotifications/unauthorizationoptions
https://developer.apple.com/documentation/usernotifications/uncalendarnotificationtrigger
https://developer.apple.com/documentation/usernotifications/unmutablenotificationcontent
https://developer.apple.com/documentation/usernotifications/unnotificationaction
https://developer.apple.com/documentation/usernotifications/unnotificationcategory
https://developer.apple.com/documentation/usernotifications/unnotificationpresentationoptions
https://developer.apple.com/documentation/usernotifications/unnotificationrequest
https://developer.apple.com/documentation/usernotifications/unnotificationsettings
https://developer.apple.com/documentation/usernotifications/untextinputnotificationaction
https://developer.apple.com/documentation/usernotifications/untimeintervalnotificationtrigger
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/add(_:withcompletionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getdeliverednotifications(completionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getnotificationsettings(completionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/getpendingnotificationrequests(completionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/removedeliverednotifications(withidentifiers:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/removependingnotificationrequests(withidentifiers:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/requestauthorization(options:completionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/setbadgecount(_:withcompletionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/setnotificationcategories(_:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate
https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate/usernotificationcenter(_:didreceive:withcompletionhandler:)
https://developer.apple.com/documentation/usernotifications/unusernotificationcenterdelegate/usernotificationcenter(_:willpresent:withcompletionhandler:)

## Purpose

Reference index for Apple's UserNotifications framework documentation,
scoped to this domain's v1: notification authorization
(`UNUserNotificationCenter.requestAuthorization`, `UNAuthorizationOptions`,
`getNotificationSettings`, provisional authorization), local notification
scheduling (`UNMutableNotificationContent`, `UNNotificationRequest`,
`UNTimeIntervalNotificationTrigger`, `UNCalendarNotificationTrigger`),
client-side remote push registration (`registerForRemoteNotifications`
and its app-delegate callbacks — device token handling only, not APNs
server-side payload construction), `UNUserNotificationCenterDelegate`
handling (`willPresent`, `didReceive`), notification actions and
categories (`UNNotificationAction`, `UNTextInputNotificationAction`,
`UNNotificationCategory`), and managing pending/delivered requests plus
badge count. `UNNotificationServiceExtension`/`UNNotificationContentExtension`
rich-media extensions, critical-alert entitlement specifics,
location-based triggers (`UNLocationNotificationTrigger`), APNs
server-side payload construction, ActivityKit/Live Activities, and
watchOS-specific notification interfaces are out of scope for v1.
Notification *design* (content wording, timing judgment, foreground UX,
action/badge conventions) is owned by `human-interface-guidelines`.

## Primary Topics

- Authorization request mechanics and status handling
- Local notification content, triggers, and scheduling
- Remote push client-side registration and device token handling
- Notification delegate setup and foreground/response handling
- Notification actions and categories
- Managing pending/delivered requests and badge count

## Used By

- knowledge/usernotifications/authorization-request.md ([[knowledge/usernotifications/authorization-request]])
- knowledge/usernotifications/local-notification-scheduling.md ([[knowledge/usernotifications/local-notification-scheduling]])
- knowledge/usernotifications/remote-push-registration.md ([[knowledge/usernotifications/remote-push-registration]])
- knowledge/usernotifications/notification-delegate-handling.md ([[knowledge/usernotifications/notification-delegate-handling]])
- knowledge/usernotifications/notification-actions-and-categories.md ([[knowledge/usernotifications/notification-actions-and-categories]])
- knowledge/usernotifications/managing-pending-delivered-and-badge.md ([[knowledge/usernotifications/managing-pending-delivered-and-badge]])
