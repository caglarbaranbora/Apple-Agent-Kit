---
name: eventkit
description: Route EventKit implementation tasks to the correct Knowledge Contracts -- authorization and access levels, event CRUD and fetch predicates, reminder CRUD and fetch, and recurrence rules with the EventKitUI hand-off decision. Use when checking EKAuthorizationStatus, calling requestFullAccessToEvents(completion:)/requestWriteOnlyAccessToEvents(completion:)/requestFullAccessToReminders(completion:)/requestAccess(to:completion:), declaring NSCalendarsUsageDescription/NSCalendarsFullAccessUsageDescription/NSCalendarsWriteOnlyAccessUsageDescription/NSRemindersUsageDescription/NSRemindersFullAccessUsageDescription, creating/saving/removing an EKEvent or EKReminder, building predicateForEvents(withStart:end:calendars:)/predicateForReminders(in:), calling events(matching:)/fetchReminders(matching:completion:), constructing EKRecurrenceRule/EKRecurrenceEnd, or deciding between EKEventEditViewController/EKEventViewController and custom UI. v1 is calendar/reminder access through EKEventStore only -- no EKSource/multi-account calendar-source management as its own topic, no CalDAV/Exchange server-specific behavior, no EKEventStoreChanged live-sync notifications, and no EventKit inside a widget extension (that's widgetkit's job). Triggers on EventKit, EventKitUI, EKEventStore, EKEvent, EKReminder, EKCalendar, EKCalendarItem, EKAuthorizationStatus, EKRecurrenceRule, EKRecurrenceEnd, EKEventEditViewController, EKEventViewController.
id: skill.eventkit.foundations
title: EventKit — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: EventKit
routes: [knowledge.eventkit.authorization-and-access-levels, knowledge.eventkit.event-crud-and-fetch-predicates, knowledge.eventkit.reminder-crud-and-fetch, knowledge.eventkit.recurrence-rules-and-eventkitui-handoff]
related: []
last_updated: 2026-08-08
---

# EventKit — Foundations Skill

## Purpose

Route EventKit implementation tasks to the minimum required EventKit
Knowledge Contracts. v1 scope is calendar and reminder access through
`EKEventStore` -- authorization, event/reminder CRUD, fetch predicates,
recurrence rules, and the point where a custom-UI feature should instead
hand off to EventKitUI's prebuilt view controllers -- not multi-account
calendar-source management, not CalDAV/Exchange specifics, not live
external-change syncing, and not EventKit inside a widget extension.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/eventkit/.

-   Checking `EKAuthorizationStatus`; calling `requestFullAccessToEvents(completion:)`/`requestWriteOnlyAccessToEvents(completion:)`/`requestFullAccessToReminders(completion:)`/the legacy `requestAccess(to:completion:)`; or declaring the matching Info.plist usage-description key -> authorization-and-access-levels.md
-   Creating/saving/removing an `EKEvent` (`EKEvent(eventStore:)`, `save(_:span:commit:)`, `remove(_:span:commit:)`); choosing a calendar via `defaultCalendarForNewEvents`; or building/running `predicateForEvents(withStart:end:calendars:)` + `events(matching:)` -> event-crud-and-fetch-predicates.md
-   Creating/saving/removing an `EKReminder` (`EKReminder(eventStore:)`, `save(_:commit:)`, `remove(_:commit:)`); or building/running `predicateForReminders(in:)` + the asynchronous `fetchReminders(matching:completion:)` -> reminder-crud-and-fetch.md
-   Constructing `EKRecurrenceRule`/`EKRecurrenceEnd`; or deciding between `EKEventEditViewController`/`EKEventViewController` (EventKitUI) and custom UI built on the CRUD contracts -> recurrence-rules-and-eventkitui-handoff.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/eventkit/ — do not guess or fall back to general knowledge.
`EKSource` / multi-account calendar-source management as its own deep
topic is out of scope entirely -- mentioned only in passing, where
relevant to choosing a calendar to save to, inside the CRUD contracts;
not planned as a separate contract. CalDAV/Exchange server-specific
behavior is out of scope entirely. The `EKEventStoreChanged` notification
and live external-change syncing are out of scope entirely -- not yet
built (see docs/architecture/domain-map.md). EventKit usage inside a
widget extension is `widgetkit`'s job, not this Skill's -- report that
boundary explicitly rather than routing to a contract here.
