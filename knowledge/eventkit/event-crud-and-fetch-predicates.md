# Event CRUD and Fetch Predicates

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.eventkit.event-crud-and-fetch-predicates
artifact_type: knowledge
title: Event CRUD and Fetch Predicates
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines creating an EKEvent(eventStore:), setting its required title/startDate/endDate/calendar fields, saving/removing it with EKEventStore.save(_:span:commit:)/remove(_:span:commit:), and building/running fetch predicates with predicateForEvents(withStart:end:calendars:) + events(matching:).
domain: EventKit
tags:
  - eventkit
  - ekevent
  - ekeventstore
  - predicateforevents
  - fetch
references:
  - https://developer.apple.com/documentation/eventkit/ekevent/init(eventstore:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/save(_:span:commit:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/predicateforevents(withstart:end:calendars:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/events(matching:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/defaultcalendarfornewevents
depends_on:
  - knowledge.eventkit.authorization-and-access-levels
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent creates, persists, and fetches `EKEvent` objects once authorization from `authorization-and-access-levels` is in place: constructing an event, setting the fields the store requires before it will save, choosing a destination calendar, saving/removing with the correct `span`, and building/running a date-bounded fetch predicate correctly.

## Scope

### Included

-   Creating an event with `EKEvent(eventStore:)`
-   Setting `title`, `startDate`, `endDate`, and `calendar` before calling `save`
-   Choosing a calendar via `eventStore.defaultCalendarForNewEvents` or an explicit `EKCalendar`
-   Saving with `EKEventStore.save(_:span:commit:)` and removing with `remove(_:span:commit:)`, including `EKSpan.thisEvent` for non-recurring events
-   Building `predicateForEvents(withStart:end:calendars:)` and running it with `events(matching:)`, including the four-year span cap and main-thread cost

### Excluded

-   Requesting/checking authorization — see `authorization-and-access-levels`
-   `EKReminder` creation, saving, and the async-only `fetchReminders(matching:completion:)` — see `reminder-crud-and-fetch`
-   `EKRecurrenceRule`/`EKRecurrenceEnd` construction and the `EKSpan.futureEvents` case they make meaningful, plus the `EKEventEditViewController`/`EKEventViewController` hand-off — see `recurrence-rules-and-eventkitui-handoff`
-   `EKSource` / multi-account calendar-source management as its own topic

## Rules

### Rule 1

Agents MUST construct a new event with `EKEvent(eventStore:)` against the same `EKEventStore` instance the app uses for saving, and MUST set `title`, `startDate`, `endDate`, and `calendar` before calling `save`. This is reasoned framework behavior rather than a literal single Apple quote: Apple's `EKError.Code` enumeration ships dedicated cases `.noCalendar`, `.noStartDate`, and `.noEndDate`, confirming the store validates exactly these fields and throws rather than silently accepting an incomplete event.

### Rule 2

Agents MUST choose a destination calendar explicitly — either `eventStore.defaultCalendarForNewEvents` or a specific `EKCalendar` the app resolved — rather than leaving `calendar` unset. Per Apple's documentation on write-only access, "When your app creates an event, EventKit saves it to a calendar that's chosen by the person using your app" only in the write-only case; under full access the app itself is responsible for the choice, and an event with no calendar throws `EKError.Code.noCalendar` on save.

### Rule 3

Agents MUST call `EKEventStore.save(_:span:commit:)` to persist an event and `remove(_:span:commit:)` to delete it, and for a non-recurring event MUST pass `EKSpan.thisEvent`. Per Apple's documentation, `save(_:span:commit:)` "raises an exception if it's passed an event from another event store," and "when saving an event, it's updated in the Calendar database... if the event has been deleted from the database, it's recreated as a new event."

### Rule 4

Agents MUST build fetch predicates with `predicateForEvents(withStart:end:calendars:)` rather than filtering `events(matching:)` results by date after the fact, and MUST account for its four-year cap. Per Apple's documentation, "for performance reasons, this method matches only those events within a four-year time span. If the date range between `startDate` and `endDate` is greater than four years, it's shortened to the first four years."

### Rule 5

Agents MUST NOT call `events(matching:)` on the main thread for predicates covering large date ranges without first confirming the cost is acceptable, because the call is synchronous and blocking. Per Apple's documentation, "`events(matching:)` is synchronous. For asynchronous behavior, run the method on another thread with `dispatch_async` or `Operation`." Agents MUST also call `eventStore.commit()` first if they need results to include events saved with `commit: false`, since "only committed events are included in the results."

## Compliant Example

```swift
import EventKit

func createEvent(in store: EKEventStore, title: String, start: Date, end: Date) throws {
    let event = EKEvent(eventStore: store) // Rule 1
    event.title = title
    event.startDate = start
    event.endDate = end
    event.calendar = store.defaultCalendarForNewEvents // Rule 2

    try store.save(event, span: .thisEvent, commit: true) // Rule 3
}

func upcomingEvents(in store: EKEventStore, from start: Date, to end: Date) -> [EKEvent] {
    let predicate = store.predicateForEvents(withStart: start, end: end, calendars: nil) // Rule 4
    // Called off the main thread by the caller for large ranges (Rule 5).
    return store.events(matching: predicate)
}
```

## Non-Compliant Example

```swift
import EventKit

func createEvent(in store: EKEventStore, title: String) {
    let event = EKEvent(eventStore: store)
    event.title = title
    // startDate, endDate, and calendar never set -- violates Rule 1 and Rule 2;
    // save will throw EKError.Code.noStartDate/.noEndDate/.noCalendar.
    try? store.save(event, span: .thisEvent, commit: true)
}

func allEventsEver(in store: EKEventStore) -> [EKEvent] {
    let farPast = Date.distantPast
    let farFuture = Date.distantFuture
    // Multi-decade range on the main thread, ignoring the four-year cap and the
    // synchronous/blocking nature of events(matching:) -- violates Rule 4 and Rule 5.
    let predicate = store.predicateForEvents(withStart: farPast, end: farFuture, calendars: nil)
    return store.events(matching: predicate)
}
```
Never sets the fields `save` requires (Rule 1, Rule 2), and runs an unbounded predicate synchronously on the caller's thread without acknowledging the four-year cap or the blocking cost (Rule 4, Rule 5).

## Dependencies

-   `knowledge.eventkit.authorization-and-access-levels` — this contract assumes the app already holds the event access level (`.fullAccess` or `.writeOnly`) its calls require.

## References

-   [Apple Developer — EKEvent.init(eventStore:)](https://developer.apple.com/documentation/eventkit/ekevent/init(eventstore:))
-   [Apple Developer — save(_:span:commit:)](https://developer.apple.com/documentation/eventkit/ekeventstore/save(_:span:commit:))
-   [Apple Developer — predicateForEvents(withStart:end:calendars:)](https://developer.apple.com/documentation/eventkit/ekeventstore/predicateforevents(withstart:end:calendars:))
-   [Apple Developer — events(matching:)](https://developer.apple.com/documentation/eventkit/ekeventstore/events(matching:))
-   [Apple Developer — defaultCalendarForNewEvents](https://developer.apple.com/documentation/eventkit/ekeventstore/defaultcalendarfornewevents)
