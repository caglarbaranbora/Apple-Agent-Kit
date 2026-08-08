# Recurrence Rules and EventKitUI Hand-off

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.eventkit.recurrence-rules-and-eventkitui-handoff
artifact_type: knowledge
title: Recurrence Rules and EventKitUI Hand-off
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines constructing EKRecurrenceRule/EKRecurrenceEnd (frequency, interval, date-based vs. count-based end) and deciding when to hand off to EventKitUI's EKEventEditViewController/EKEventViewController instead of building custom recurrence-editing UI on top of the CRUD APIs.
domain: EventKit
tags:
  - eventkit
  - eventkitui
  - ekrecurrencerule
  - ekrecurrenceend
  - ekeventeditviewcontroller
references:
  - https://developer.apple.com/documentation/eventkit/ekrecurrencerule
  - https://developer.apple.com/documentation/eventkit/ekrecurrencerule/init(recurrencewith:interval:end:)
  - https://developer.apple.com/documentation/eventkit/ekrecurrenceend
  - https://developer.apple.com/documentation/eventkit/accessing-the-event-store
  - https://developer.apple.com/documentation/eventkitui/ekeventeditviewcontroller
  - https://developer.apple.com/documentation/eventkitui/ekeventviewcontroller
depends_on:
  - knowledge.eventkit.event-crud-and-fetch-predicates
related:
  - knowledge.uikit.swiftui-view-representable
  - knowledge.eventkit.reminder-crud-and-fetch
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent constructs an `EKRecurrenceRule`/`EKRecurrenceEnd` and, separately, when to stop building custom event/reminder UI on top of the CRUD contracts and hand off to Apple's prebuilt EventKitUI view controllers instead. Both events and reminders can recur — recurrence lives on the shared `EKCalendarItem` superclass — so this contract depends primarily on the event CRUD contract but applies to either.

## Scope

### Included

-   Constructing `EKRecurrenceRule` with `init(recurrenceWith:interval:end:)` (`frequency`, `interval`, optional `end`)
-   Choosing `EKRecurrenceEnd`: date-based (`init(end:)` / `endDate`) vs. count-based (`init(occurrenceCount:)` / `occurrenceCount`), or `nil` for an indefinite recurrence
-   Attaching a rule with `addRecurrenceRule(_:)` (inherited by both `EKEvent` and `EKReminder` via `EKCalendarItem`)
-   Deciding between `EKEventEditViewController`/`EKEventViewController` (EventKitUI) and custom UI built on the `event-crud-and-fetch-predicates`/`reminder-crud-and-fetch` APIs

### Excluded

-   Requesting/checking authorization — see `authorization-and-access-levels`
-   The base create/save/remove/fetch calls themselves — see `event-crud-and-fetch-predicates` and `reminder-crud-and-fetch`
-   `EKSource` / multi-account calendar-source management, CalDAV/Exchange specifics, `EKEventStoreChanged` live syncing, and EventKit inside a widget extension (that boundary belongs to `widgetkit`)

## Rules

### Rule 1

Agents MUST construct a recurrence rule with `EKRecurrenceRule.init(recurrenceWith:interval:end:)`, supplying an `EKRecurrenceFrequency` (`.daily`, `.weekly`, `.monthly`, `.yearly`), a positive `interval`, and an optional `EKRecurrenceEnd`. Per Apple's documentation, this initializer returns "the initialized recurrence rule, or `nil` if invalid values are provided," and `EKRecurrenceRule`'s overview states "recurrence rules can have an end, represented by an `EKRecurrenceEnd` object. The end can be based on a specific date or a maximum number of occurrences."

### Rule 2

Agents MUST choose `EKRecurrenceEnd.init(end:)` for a date-bounded recurrence, `init(occurrenceCount:)` for a count-bounded one, and MUST pass `nil` rather than a synthesized far-future date for an indefinite recurrence. Per Apple's documentation, "the recurrence end can be specified by a date (date-based) or by a maximum count of occurrences (count-based). An event that is intended to continue indefinitely should have its `EKRecurrenceEnd` set to `nil`."

### Rule 3

Agents adding a recurrence rule to a reminder MUST also set a due date, since a recurring reminder without one is invalid. This is reasoned framework behavior rather than a literal Apple-documentation quote: Apple's `EKError.Code` enumeration ships the dedicated case `.recurringReminderRequiresDueDate`, confirming the store validates this combination and rejects it rather than silently accepting a recurring reminder with no due date.

### Rule 4

Agents building a feature that only needs the person to create, edit, or view a calendar event through a standard, modal, Calendar-app-like interface MUST default to `EKEventEditViewController`/`EKEventViewController` (EventKitUI) rather than building that UI from scratch on top of `event-crud-and-fetch-predicates`. Per Apple's documentation, `EKEventEditViewController` "provides a way for users to add new events, as well as edit or delete events from their calendar," including recurrence editing, and on iOS 17+ "EventKitUI presents chooser and editor UI outside of your app's process... Your app can use EventKitUI without requesting write-only or full calendar access... If your app needs to present UI for creating and editing calendar events, consider using EventKitUI instead of requesting full access to calendar data."

### Rule 5

Agents MUST reserve custom UI built on the CRUD contracts for cases EventKitUI cannot serve: embedded/inline event creation that must not feel like leaving the app, or a UI shape EventKitUI's fixed view controllers don't offer. Choosing custom UI over EventKitUI trades away the benefit described in Rule 4 (faster to ship, automatically matches system Calendar conventions, EventKitUI's own recurrence-editing UI, and — critically — no calendar-access request or Info.plist key at all) for full control over presentation.

### Rule 6

Agents MUST treat EventKitUI as UIKit-only when choosing how to present it from SwiftUI, and MUST bridge it with `UIViewControllerRepresentable` rather than assuming a native SwiftUI view exists. How that wrapper is written is `knowledge.uikit.swiftui-view-representable` Rule 5 — this contract states only that EventKitUI needs one, and defines no wrapping mechanics of its own. This was verified directly against Apple's EventKitUI framework-overview page rather than assumed from general knowledge: its declared "Calendar Views"/"Calendar Edits" symbols are `EKEventViewController`/`EKEventEditViewController`, both declared as `class` (`UIViewController` subclasses), and Apple's own overview text introduces them as "the view controllers you'll use on iOS" — no SwiftUI `View`-conforming wrapper appears in the framework's symbol index as of this verification.

## Compliant Example

```swift
import EventKit
import EventKitUI

func makeWeeklyRule(untilOccurrences count: Int) -> EKRecurrenceRule {
    let end = EKRecurrenceEnd(occurrenceCount: count) // Rule 2: count-based end
    return EKRecurrenceRule(recurrenceWith: .weekly, interval: 1, end: end)! // Rule 1
}

func presentEventCreation(from viewController: UIViewController, store: EKEventStore) {
    // Rule 4: hand off to EventKitUI instead of a hand-built create/edit form;
    // on iOS 17+ this needs no calendar-access request at all.
    let editController = EKEventEditViewController()
    editController.eventStore = store
    viewController.present(editController, animated: true)
}
```

## Non-Compliant Example

```swift
import EventKit

func makeIndefiniteWeeklyRule() -> EKRecurrenceRule {
    // Synthesizes a "forever" end date instead of passing nil -- violates Rule 2.
    let fakeForeverEnd = EKRecurrenceEnd(end: Date(timeIntervalSinceNow: 100 * 365 * 24 * 60 * 60))
    return EKRecurrenceRule(recurrenceWith: .weekly, interval: 1, end: fakeForeverEnd)!
}

func addRecurringReminder(in store: EKEventStore, calendar: EKCalendar) throws {
    let reminder = EKReminder(eventStore: store)
    reminder.title = "Take out trash"
    reminder.calendar = calendar
    reminder.addRecurrenceRule(EKRecurrenceRule(recurrenceWith: .weekly, interval: 1, end: nil)!)
    // dueDateComponents never set on a recurring reminder -- violates Rule 3;
    // save throws EKError.Code.recurringReminderRequiresDueDate.
    try store.save(reminder, commit: true)
}
```
Fakes an indefinite recurrence with a hundred-year end date instead of `nil` (Rule 2), and attaches a recurrence rule to a reminder with no due date (Rule 3).

## Dependencies

-   `knowledge.eventkit.event-crud-and-fetch-predicates` — recurrence rules attach to an `EKEvent` created and saved per that contract's rules.
-   `knowledge.eventkit.reminder-crud-and-fetch` (related) — the same recurrence API applies to `EKReminder` via the shared `EKCalendarItem` superclass.

## References

-   [Apple Developer — EKRecurrenceRule](https://developer.apple.com/documentation/eventkit/ekrecurrencerule)
-   [Apple Developer — EKRecurrenceRule.init(recurrenceWith:interval:end:)](https://developer.apple.com/documentation/eventkit/ekrecurrencerule/init(recurrencewith:interval:end:))
-   [Apple Developer — EKRecurrenceEnd](https://developer.apple.com/documentation/eventkit/ekrecurrenceend)
-   [Apple Developer — Accessing the event store](https://developer.apple.com/documentation/eventkit/accessing-the-event-store)
-   [Apple Developer — EKEventEditViewController](https://developer.apple.com/documentation/eventkitui/ekeventeditviewcontroller)
-   [Apple Developer — EKEventViewController](https://developer.apple.com/documentation/eventkitui/ekeventviewcontroller)
