# EventKit

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/eventkit
https://developer.apple.com/documentation/eventkit/ekeventstore
https://developer.apple.com/documentation/eventkit/ekevent
https://developer.apple.com/documentation/eventkit/ekreminder
https://developer.apple.com/documentation/eventkit/ekcalendaritem
https://developer.apple.com/documentation/eventkit/ekcalendar
https://developer.apple.com/documentation/eventkit/eksource
https://developer.apple.com/documentation/eventkit/ekrecurrencerule
https://developer.apple.com/documentation/eventkit/ekrecurrenceend
https://developer.apple.com/documentation/eventkit/ekauthorizationstatus
https://developer.apple.com/documentation/eventkit/ekspan
https://developer.apple.com/documentation/eventkit/accessing-the-event-store
https://developer.apple.com/documentation/eventkit/ekeventstore/requestfullaccesstoevents(completion:)
https://developer.apple.com/documentation/eventkit/ekeventstore/requestwriteonlyaccesstoevents(completion:)
https://developer.apple.com/documentation/eventkit/ekeventstore/requestfullaccesstoreminders(completion:)
https://developer.apple.com/documentation/eventkit/ekeventstore/requestaccess(to:completion:)
https://developer.apple.com/documentation/eventkit/ekeventstore/predicateforevents(withstart:end:calendars:)
https://developer.apple.com/documentation/eventkit/ekeventstore/predicateforreminders(in:)
https://developer.apple.com/documentation/eventkit/ekeventstore/events(matching:)
https://developer.apple.com/documentation/eventkit/ekeventstore/fetchreminders(matching:completion:)
https://developer.apple.com/documentation/eventkit/ekeventstore/save(_:span:commit:)
https://developer.apple.com/documentation/eventkit/ekeventstore/save(_:commit:)
https://developer.apple.com/documentation/eventkitui/ekeventeditviewcontroller
https://developer.apple.com/documentation/eventkitui/ekeventviewcontroller
https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarsfullaccessusagedescription
https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarswriteonlyaccessusagedescription
https://developer.apple.com/documentation/bundleresources/information-property-list/nsremindersfullaccessusagedescription

## Purpose

Reference index for Apple's EventKit documentation, scoped to this domain's v1: authorizing access through `EKEventStore` (`EKAuthorizationStatus`, the iOS 17+ split between `requestFullAccessToEvents(completion:)`/`requestWriteOnlyAccessToEvents(completion:)`/`requestFullAccessToReminders(completion:)` and the legacy `requestAccess(to:completion:)`); creating, saving, and removing `EKEvent`/`EKReminder` objects (both subclasses of `EKCalendarItem`, which supplies shared `title`, `calendar`, and recurrence-rule properties); choosing a destination `EKCalendar` (including `EKEventStore.defaultCalendarForNewEvents`); building and running fetch predicates (`predicateForEvents(withStart:end:calendars:)` + synchronous `events(matching:)`; `predicateForReminders(in:)` + asynchronous `fetchReminders(matching:completion:)`); constructing `EKRecurrenceRule`/`EKRecurrenceEnd`; and choosing between that custom CRUD surface and Apple's prebuilt `EKEventEditViewController`/`EKEventViewController` (EventKitUI).

Out of scope for v1: `EKSource` and multi-account calendar-source management as their own deep topic (mentioned only where relevant to choosing a calendar to save to); CalDAV/Exchange server-specific behavior; the `EKEventStoreChanged` notification and live external-change syncing; and EventKit usage inside a widget extension, which belongs to the `widgetkit` domain, not this one.

## Primary Topics

- Authorization and access levels (full vs. write-only, events vs. reminders)
- Event creation, persistence, and fetch predicates
- Reminder creation, persistence, and fetch (async-only)
- Recurrence rules and the EventKitUI hand-off decision

## Used By

- knowledge/eventkit/authorization-and-access-levels.md ([[knowledge/eventkit/authorization-and-access-levels]])
- knowledge/eventkit/event-crud-and-fetch-predicates.md ([[knowledge/eventkit/event-crud-and-fetch-predicates]])
- knowledge/eventkit/reminder-crud-and-fetch.md ([[knowledge/eventkit/reminder-crud-and-fetch]])
- knowledge/eventkit/recurrence-rules-and-eventkitui-handoff.md ([[knowledge/eventkit/recurrence-rules-and-eventkitui-handoff]])
