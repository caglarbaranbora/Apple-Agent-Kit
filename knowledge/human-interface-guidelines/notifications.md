# Notifications

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.notifications
artifact_type: knowledge
title: Notifications
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for notification content, timing, foreground handling, actions, and badging on iOS/iPadOS — not the UserNotifications API.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - notifications
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/notifications
depends_on: []
related:
  - knowledge.human-interface-guidelines.privacy
  - knowledge.human-interface-guidelines.feedback
  - knowledge.human-interface-guidelines.sf-symbols
last_updated: 2026-08-06
```

## Intent

This contract defines the design-level rules an AI coding agent
applies when designing notification content and behavior on
iOS/iPadOS: what a notification should say, when to avoid sending
one, how to behave while the app is foregrounded, and how to use
actions and badges. It does not cover `UNUserNotificationCenter`,
`UNAuthorizationOptions`, or any UserNotifications framework API,
which belong to a future dedicated `usernotifications` domain.

## Scope

### Included

-   Notification content structure (title, body, fallback preview text)
-   When to send vs. withhold a notification
-   Foreground-app notification handling
-   Notification action design (count, labels, destructiveness, icons)
-   Badge usage conventions
-   Consent timing (design-level: request before sending, at an appropriate point)

### Excluded

-   `UNUserNotificationCenter`/`UNAuthorizationOptions` implementation — future `usernotifications` domain
-   Notification and action copy/wording specifics — see `style-guide`
-   Permission purpose-string wording and system-alert mechanics — see `privacy`
-   Interface-icon rendering mechanics for action icons — see `sf-symbols`
-   watchOS-specific short-look/long-look/double-tap patterns (out of scope for this iOS/iPadOS contract)

## Rules

### Rule 1

Agents MUST obtain consent before sending notifications and MUST NOT
design a flow that sends notifications prior to that consent (see
`privacy` for permission-request timing and wording).

### Rule 2

Agents MUST write concise, informative notification content: a short,
title-case title with no ending punctuation (or no title, letting the
system show the app name), and succinct sentence-case body text as a
complete sentence, without manually truncating it.

### Rule 3

Agents MUST provide generically descriptive fallback body text (e.g.,
"Friend request," "New comment") for when the person has hidden
notification previews in Settings, without revealing sensitive
details.

### Rule 4

Agents MUST NOT send multiple notifications for the same event, MUST
NOT instruct people to perform an in-app task via notification text
(offer a notification action instead when feasible), and MUST NOT
include sensitive, personal, or confidential information in
notification content.

### Rule 5

Agents MUST use an alert, not a notification, to display an error
message (see `feedback`).

### Rule 6

Agents MUST handle notifications gracefully when the app is
foregrounded by not displaying the notification UI, instead
reflecting the update unobtrusively within the interface (e.g.,
incrementing a badge or inserting new data into the current view).

### Rule 7

Agents SHOULD provide notification actions only for beneficial,
time-saving tasks (up to four), MUST NOT provide an action that
merely opens the app, and SHOULD prefer nondestructive actions,
giving people enough context before any destructive one.

### Rule 8

Agents MUST use a badge (the numbered oval on the app icon) only to
represent the count of unread notifications, keep it current as
notifications are addressed, and MUST NOT rely on badging as the
only way to communicate essential information.

## Compliant Example

-   ✓ A messaging app's notification shows the sender's name and a one-line message preview, with no manual truncation. (Rule 2)
-   ✓ When the app is open and a new message arrives in the currently viewed conversation, no notification is shown — the message simply appears in the list. (Rule 6)
-   ✓ A calendar-event notification offers a "Snooze" action button instead of telling people to open the app and dismiss the alarm. (Rule 4, 7)

## Non-Compliant Example

-   ✗ The app sends a separate notification every few minutes for the same unread message. (Rule 4)
-   ✗ A notification's body reads "Open the app and update your payment method," instructing an in-app task. (Rule 4)
-   ✗ An error is shown as a notification banner instead of an in-app alert. (Rule 5)
-   ✗ The badge count shows the number of items in a shopping cart instead of unread notifications. (Rule 8)

## Dependencies

None.

## References

-   [Apple HIG — Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications)
