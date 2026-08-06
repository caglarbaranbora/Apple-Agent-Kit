# Authorization and Access Levels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.eventkit.authorization-and-access-levels
type: knowledge
title: Authorization and Access Levels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines checking EKAuthorizationStatus, requesting the correct iOS 17+ access level (requestFullAccessToEvents(completion:)/requestWriteOnlyAccessToEvents(completion:)/requestFullAccessToReminders(completion:)) or the legacy requestAccess(to:completion:), and declaring the matching Info.plist usage-description key.
domain: EventKit
tags:
  - eventkit
  - ekeventstore
  - ekauthorizationstatus
  - authorization
  - info-plist
references:
  - https://developer.apple.com/documentation/eventkit/ekauthorizationstatus
  - https://developer.apple.com/documentation/eventkit/ekeventstore/requestfullaccesstoevents(completion:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/requestwriteonlyaccesstoevents(completion:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/requestfullaccesstoreminders(completion:)
  - https://developer.apple.com/documentation/eventkit/ekeventstore/requestaccess(to:completion:)
  - https://developer.apple.com/documentation/eventkit/accessing-the-event-store
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarsfullaccessusagedescription
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarswriteonlyaccessusagedescription
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsremindersfullaccessusagedescription
depends_on: []
related: []
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent checks and requests EventKit authorization: reading `EKAuthorizationStatus`, choosing the correct iOS 17+ request method for the access level and entity type actually needed, falling back to the legacy API only when the deployment target requires it, and declaring the Info.plist key that matches the request being made.

## Scope

### Included

-   Reading `EKEventStore.authorizationStatus(for:)` and branching on `EKAuthorizationStatus` (`.notDetermined`, `.restricted`, `.denied`, `.fullAccess`, `.writeOnly`)
-   Choosing `requestFullAccessToEvents(completion:)` vs. `requestWriteOnlyAccessToEvents(completion:)` for events, and `requestFullAccessToReminders(completion:)` for reminders (there is no write-only reminders variant)
-   The legacy, iOS 17-deprecated `requestAccess(to:completion:)` and when an agent still needs it (deployment target below iOS 17/macOS 14)
-   Declaring the Info.plist usage-description key matching the request made, and the consequence of declaring the wrong one

### Excluded

-   Creating, saving, or fetching `EKEvent`/`EKReminder` objects once access is granted — see `event-crud-and-fetch-predicates` / `reminder-crud-and-fetch`
-   Presenting `EKEventEditViewController`/`EKEventViewController`, including the case where doing so avoids needing calendar access at all — see `recurrence-rules-and-eventkitui-handoff`
-   `EKSource` / multi-account calendar-source management, CalDAV/Exchange specifics, `EKEventStoreChanged` notifications, and EventKit inside a widget extension (that consideration belongs to `widgetkit`)

## Rules

### Rule 1

Agents MUST check `EKAuthorizationStatus` before assuming access, and MUST treat `.fullAccess` and `.writeOnly` as distinct, non-interchangeable grants rather than a single "authorized" state. Per Apple's documentation, `EKAuthorizationStatus` is "The current authorization status for a specific entity type," with cases including `.fullAccess`, `.writeOnly`, `.denied`, `.notDetermined`, and `.restricted`; the pre-iOS-17 `.authorized` case is listed separately under "Deprecated values."

### Rule 2

Agents targeting iOS 17/macOS 14 or later MUST request the minimum access level the feature needs: `requestWriteOnlyAccessToEvents(completion:)` when the app only creates events, `requestFullAccessToEvents(completion:)` when it must also read/edit/delete them, and `requestFullAccessToReminders(completion:)` for reminders. Per Apple's documentation, write-only access "lets your app create new events but doesn't let it read any events or other calendar information, including events your app created," and with write-only access "a request for a list of calendars returns a single virtual calendar" while "requests for events on the virtual calendar return no results."

### Rule 3

Agents MUST use the legacy `requestAccess(to:completion:)` only for deployment targets below iOS 17/macOS 14, and MUST NOT treat it as the primary API on a codebase whose deployment target already supports the split methods. Per Apple's own platform metadata for this symbol, it is deprecated starting at iOS 17.0/iPadOS 17.0/Mac Catalyst 17.0/macOS 14.0, with the message "Use -requestFullAccessToEventsWithCompletion:, -requestWriteOnlyAccessToEventsWithCompletion:, or -requestFullAccessToRemindersWithCompletion:".

### Rule 4

Agents MUST declare the Info.plist usage-description key matching the access being requested, and MUST NOT rely on the wrong key or omit it. Per Apple's documentation, "On iOS 17 and later, to access a person's calendar events or reminders, you need to include descriptions for: `NSCalendarsWriteOnlyAccessUsageDescription` or `NSCalendarsFullAccessUsageDescription`, depending on the level of access to events your app needs... `NSRemindersFullAccessUsageDescription`, if your app needs access to reminders." For apps supporting iOS 10 through iOS 16, Apple's documentation states the legacy `NSCalendarsUsageDescription`/`NSRemindersUsageDescription` keys are required "as a fallback if your app runs on iOS 17 or later and doesn't include descriptions for" the newer keys; Apple's key-reference page confirms `NSCalendarsUsageDescription` is deprecated starting at iOS 17.0 (macOS 14.0, watchOS 10.0).

### Rule 5

Agents MUST treat a missing usage-description key as a launch-time crash risk, not merely a denied-permission path, and MUST NOT ship a build that calls an access-requesting method without the corresponding key present. This is reasoned framework behavior rather than a literal EventKit-documentation quote: iOS terminates apps that touch privacy-gated data without a matching `Info.plist` key, surfacing the well-known runtime message "This app has crashed because it attempted to access privacy-sensitive data without a usage description. The app's Info.plist must contain an `NS<Resource>UsageDescription` key..." — the same TCC-enforced mechanism that applies to every usage-description-gated framework, EventKit included.

## Compliant Example

```swift
import EventKit

let store = EKEventStore()

func requestEventAccess(writeOnly: Bool, completion: @escaping (Bool) -> Void) {
    let status = EKEventStore.authorizationStatus(for: .event) // Rule 1
    switch status {
    case .fullAccess:
        completion(true)
    case .writeOnly:
        completion(writeOnly) // write-only grant can't satisfy a full-access need
    case .notDetermined:
        if writeOnly {
            store.requestWriteOnlyAccessToEvents { granted, _ in completion(granted) } // Rule 2
        } else {
            store.requestFullAccessToEvents { granted, _ in completion(granted) } // Rule 2
        }
    case .denied, .restricted:
        completion(false)
    @unknown default:
        completion(false)
    }
}
// Info.plist declares NSCalendarsFullAccessUsageDescription and
// NSCalendarsWriteOnlyAccessUsageDescription for an iOS 17+ deployment target (Rule 4).
```

## Non-Compliant Example

```swift
import EventKit

let store = EKEventStore()

func addEvent() {
    // No authorization-status check before touching the store -- violates Rule 1.
    store.requestAccess(to: .event) { granted, _ in
        // Uses the deprecated legacy API unconditionally on an iOS 17+ target,
        // instead of requestFullAccessToEvents/requestWriteOnlyAccessToEvents --
        // violates Rule 3.
        guard granted else { return }
        // Info.plist declares only the legacy NSCalendarsUsageDescription key,
        // not NSCalendarsFullAccessUsageDescription/NSCalendarsWriteOnlyAccessUsageDescription
        // -- violates Rule 4, and risks the launch-time crash in Rule 5.
    }
}
```
Never reads `EKAuthorizationStatus` before requesting (Rule 1), calls the iOS-17-deprecated `requestAccess(to:completion:)` as the primary path on a modern target (Rule 3), and pairs it with only the legacy Info.plist key (Rule 4), risking a crash rather than a clean denial (Rule 5).

## Dependencies

None within this domain — this is the foundational contract every other EventKit Knowledge Contract assumes access has already been granted correctly.

## References

-   [Apple Developer — EKAuthorizationStatus](https://developer.apple.com/documentation/eventkit/ekauthorizationstatus)
-   [Apple Developer — requestFullAccessToEvents(completion:)](https://developer.apple.com/documentation/eventkit/ekeventstore/requestfullaccesstoevents(completion:))
-   [Apple Developer — requestWriteOnlyAccessToEvents(completion:)](https://developer.apple.com/documentation/eventkit/ekeventstore/requestwriteonlyaccesstoevents(completion:))
-   [Apple Developer — requestFullAccessToReminders(completion:)](https://developer.apple.com/documentation/eventkit/ekeventstore/requestfullaccesstoreminders(completion:))
-   [Apple Developer — requestAccess(to:completion:)](https://developer.apple.com/documentation/eventkit/ekeventstore/requestaccess(to:completion:))
-   [Apple Developer — Accessing the event store](https://developer.apple.com/documentation/eventkit/accessing-the-event-store)
-   [Apple Developer — NSCalendarsFullAccessUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarsfullaccessusagedescription)
-   [Apple Developer — NSCalendarsWriteOnlyAccessUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarswriteonlyaccessusagedescription)
-   [Apple Developer — NSRemindersFullAccessUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsremindersfullaccessusagedescription)
