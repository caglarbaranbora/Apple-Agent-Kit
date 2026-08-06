# Reminder CRUD and Fetch

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.eventkit.reminder-crud-and-fetch
type: knowledge
title: Reminder CRUD and Fetch
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines creating an EKReminder(eventStore:), setting its required title/calendar fields, saving/removing it with EKEventStore.save(_:commit:)/remove(_:commit:) (no span parameter), and fetching reminders only via the asynchronous fetchReminders(matching:completion:) built from predicateForReminders(in:).
domain: EventKit
tags:
  - eventkit
  - ekreminder
  - ekeventstore
  - predicateforreminders
  - fetchreminders
references:
  - https://developer.apple.com/documentation/eventkit/ekreminder/init(eventstore:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/save(_:commit:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/predicateforreminders(in:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/fetchreminders(matching:completion:)
depends_on:
  - knowledge.eventkit.authorization-and-access-levels
related: []
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent creates, persists, and fetches `EKReminder` objects once reminders authorization from `authorization-and-access-levels` is in place: constructing a reminder, setting the fields it requires, saving/removing with the reminder-specific (no `span`) signature, and fetching exclusively through the asynchronous, completion-handler-based API — there is no synchronous reminder fetch.

## Scope

### Included

-   Creating a reminder with `EKReminder(eventStore:)`
-   Setting `title` and `calendar` (both inherited from `EKCalendarItem`, the superclass shared with `EKEvent`) before saving
-   Saving with `EKEventStore.save(_:commit:)` and removing with `remove(_:commit:)` — no `span:` parameter, unlike the event-saving calls
-   Building `predicateForReminders(in:)` and fetching with the asynchronous `fetchReminders(matching:completion:)`

### Excluded

-   Requesting/checking authorization — see `authorization-and-access-levels`
-   `EKEvent` creation, `save(_:span:commit:)`/`remove(_:span:commit:)`, and the synchronous `events(matching:)` — see `event-crud-and-fetch-predicates`
-   `EKRecurrenceRule`/`EKRecurrenceEnd` construction (reminders can carry recurrence rules too, via the shared `EKCalendarItem` API) and the `EKEventEditViewController`/`EKEventViewController` hand-off — see `recurrence-rules-and-eventkitui-handoff`
-   `EKSource` / multi-account calendar-source management as its own topic

## Rules

### Rule 1

Agents MUST construct a new reminder with `EKReminder(eventStore:)` against the same `EKEventStore` used for saving, and MUST set `title` and `calendar` (both defined on the shared `EKCalendarItem` superclass) before calling `save`. Per Apple's documentation, "Use the `EKReminder.init(eventStore:)` method to create a new reminder. Use the properties in the class to get and modify certain information about a reminder," and an unset calendar throws `EKError.Code.noCalendar` on save, exactly as it does for `EKEvent`.

### Rule 2

Agents MUST save a reminder with `EKEventStore.save(_:commit:)` and remove it with `remove(_:commit:)`, and MUST NOT pass a `span:` argument — reminders are not recurring-instance-based the way events are, so the save/remove signatures omit it. Per Apple's documentation, `save(_:commit:)` "raises an exception if `reminder` belongs to another event store," and its declared signature is `func save(_ reminder: EKReminder, commit: Bool) throws` — no `span` parameter, unlike `EKEvent`'s `save(_:span:commit:)`.

### Rule 3

Agents MUST build a reminder fetch predicate with `predicateForReminders(in:)` before fetching, mirroring how `predicateForEvents(withStart:end:calendars:)` is required before an event fetch. Per Apple's documentation, `predicateForReminders(in:)` returns "a predicate to use when calling `fetchReminders(matching:completion:)`."

### Rule 4

Agents MUST fetch reminders only through the asynchronous `fetchReminders(matching:completion:)`, and MUST NOT assume a synchronous reminder-fetch method exists — EventKit provides one for events (`events(matching:)`) but not for reminders. Per Apple's documentation, "this method fetches reminders asynchronously," and its return value "represents the asynchronous fetch request. To cancel a fetch request before it completes, pass this value to `cancelFetchRequest(_:)`." Agents MUST also call `eventStore.commit()` first if uncommitted saves should be visible, since "only committed reminders are included in the results."

## Compliant Example

```swift
import EventKit

func createReminder(in store: EKEventStore, title: String, calendar: EKCalendar) throws {
    let reminder = EKReminder(eventStore: store) // Rule 1
    reminder.title = title
    reminder.calendar = calendar // Rule 1

    try store.save(reminder, commit: true) // Rule 2: no span: parameter
}

func fetchAllReminders(in store: EKEventStore, calendars: [EKCalendar]?, completion: @escaping ([EKReminder]) -> Void) {
    let predicate = store.predicateForReminders(in: calendars) // Rule 3
    _ = store.fetchReminders(matching: predicate) { reminders in // Rule 4: async, no sync alternative
        completion(reminders ?? [])
    }
}
```

## Non-Compliant Example

```swift
import EventKit

func createReminder(in store: EKEventStore, title: String) {
    let reminder = EKReminder(eventStore: store)
    reminder.title = title
    // calendar never set -- violates Rule 1; save throws EKError.Code.noCalendar.
    try? store.save(reminder, span: .thisEvent, commit: true)
    // Passes span:, a parameter save(_:commit:) doesn't have -- violates Rule 2;
    // this line does not compile against the real EKEventStore API.
}

func fetchAllReminders(in store: EKEventStore) -> [EKReminder] {
    let predicate = store.predicateForReminders(in: nil)
    // Assumes a synchronous fetch exists, mirroring events(matching:) -- violates
    // Rule 4; EKEventStore has no such synchronous reminder-fetch method.
    return store.reminders(matching: predicate)
}
```
Never sets `calendar` (Rule 1), invents a `span:` argument that `save(_:commit:)` does not accept (Rule 2), and assumes a synchronous fetch method that does not exist on `EKEventStore` (Rule 4).

## Dependencies

-   `knowledge.eventkit.authorization-and-access-levels` — this contract assumes the app already holds `.fullAccess` for reminders before any of these calls run.

## References

-   [Apple Developer — EKReminder.init(eventStore:)](https://developer.apple.com/documentation/eventkit/ekreminder/init(eventstore:))
-   [Apple Developer — save(_:commit:)](https://developer.apple.com/documentation/eventkit/ekeventstore/save(_:commit:))
-   [Apple Developer — predicateForReminders(in:)](https://developer.apple.com/documentation/eventkit/ekeventstore/predicateforreminders(in:))
-   [Apple Developer — fetchReminders(matching:completion:)](https://developer.apple.com/documentation/eventkit/ekeventstore/fetchreminders(matching:completion:))
