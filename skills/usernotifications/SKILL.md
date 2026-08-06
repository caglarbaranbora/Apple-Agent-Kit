---
name: usernotifications
description: Route UserNotifications framework implementation tasks to the correct Knowledge Contracts -- authorization, local notification scheduling, remote push registration, delegate handling, actions/categories, and managing pending/delivered requests plus badge count. Use when calling UNUserNotificationCenter, requestAuthorization, UNAuthorizationOptions, getNotificationSettings, UNMutableNotificationContent, UNNotificationRequest, UNTimeIntervalNotificationTrigger, UNCalendarNotificationTrigger, registerForRemoteNotifications, didRegisterForRemoteNotificationsWithDeviceToken, UNUserNotificationCenterDelegate, willPresent, didReceive, UNNotificationAction, UNTextInputNotificationAction, UNNotificationCategory, setNotificationCategories, removePendingNotificationRequests, removeDeliveredNotifications, or badge count / setBadgeCount. v1 is client-side UserNotifications + UIKit push-registration API only -- no rich media extensions, critical alerts, location triggers, APNs server payloads, Live Activities, or watchOS.
id: skill.usernotifications.foundations
title: UserNotifications — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: UserNotifications
routes: [knowledge.usernotifications.authorization-request, knowledge.usernotifications.local-notification-scheduling, knowledge.usernotifications.remote-push-registration, knowledge.usernotifications.notification-delegate-handling, knowledge.usernotifications.notification-actions-and-categories, knowledge.usernotifications.managing-pending-delivered-and-badge]
related: [skill.human-interface-guidelines.foundations]
last_updated: 2026-08-06
---

# UserNotifications — Foundations Skill

## Purpose

Route UserNotifications framework implementation tasks to the minimum
required UserNotifications Knowledge Contracts. v1 scope is client-side
API implementation only: authorization, local scheduling, push
registration, delegate handling, actions/categories, and
pending/delivered/badge management.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/usernotifications/.

-   Calling requestAuthorization, UNAuthorizationOptions, or getNotificationSettings -> authorization-request.md
-   Building UNMutableNotificationContent/UNNotificationRequest or configuring a trigger -> local-notification-scheduling.md
-   Calling registerForRemoteNotifications or handling its device-token callbacks -> remote-push-registration.md
-   Setting UNUserNotificationCenterDelegate, willPresent, or didReceive -> notification-delegate-handling.md
-   Defining UNNotificationAction/UNTextInputNotificationAction/UNNotificationCategory or setNotificationCategories -> notification-actions-and-categories.md
-   Removing/inspecting pending or delivered requests, or setting badge count -> managing-pending-delivered-and-badge.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/usernotifications/ — do not guess or fall back to
general knowledge. `UNNotificationServiceExtension`/`UNNotificationContentExtension`
rich-media extensions, critical-alert entitlement specifics,
location-based triggers (`UNLocationNotificationTrigger`), APNs
server-side payload construction, ActivityKit/Live Activities, and
watchOS-specific notification interfaces are deferred/unbuilt scope —
report that explicitly rather than answering from general knowledge (see
docs/architecture/domain-map.md). Notification *design* questions
(content wording, timing judgment, foreground UX, badge conventions) are
owned by the `human-interface-guidelines` Skill, not this one.
