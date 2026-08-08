# Querying With @Query and FetchDescriptor

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.swiftdata.querying-with-query-and-fetchdescriptor
artifact_type: knowledge
title: Querying With @Query and FetchDescriptor
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines fetching SwiftData models -- the @Query property wrapper for SwiftUI views (filter via #Predicate, sort:, order:, animation:) versus imperative fetching with FetchDescriptor<Model> plus context.fetch(_:) outside view context, and when to use which.
domain: SwiftData
tags:
  - swiftdata
  - query
  - fetchdescriptor
  - predicate
  - fetching
references:
  - https://developer.apple.com/documentation/swiftdata/query
  - https://developer.apple.com/documentation/swiftdata/fetchdescriptor
  - https://developer.apple.com/documentation/swiftdata/modelcontext
  - https://developer.apple.com/documentation/foundation/predicate
  - https://developer.apple.com/documentation/swiftdata/filtering-and-sorting-persistent-data
  - https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches
depends_on:
  - knowledge.swiftdata.model-definition
  - knowledge.swiftdata.model-container-setup
related:
  - knowledge.swiftdata.model-context-crud
last_updated: 2026-08-08
```

## Intent

This contract governs reading persisted `@Model` data (see `model-definition`) back out of SwiftData: the `@Query` property wrapper for SwiftUI views, and the imperative `FetchDescriptor` + `context.fetch(_:)` pair for use outside a view's body (services, background tasks, previews-setup code). Both require a `ModelContainer`/`ModelContext` already set up per `model-container-setup`.

## Scope

### Included

- `@Query` initializers taking `filter:`, `sort:`, `order:`, and `animation:`
- `#Predicate` for building a type-safe `Predicate<Model>` used by both `@Query` and `FetchDescriptor`
- `FetchDescriptor<T>(predicate:sortBy:)` and its `fetchLimit`/`fetchOffset` configuration
- `ModelContext.fetch(_:)` for executing a `FetchDescriptor` outside a view
- Choosing `@Query` vs. `FetchDescriptor`/`fetch(_:)` based on whether code runs inside a SwiftUI view

### Excluded

- Creating the `ModelContainer`/`ModelContext` a query or fetch runs against — see `model-container-setup`
- Inserting, deleting, or saving fetched results — see `model-context-crud`
- `@Relationship(deleteRule:)` and how relationships affect fetched object graphs — see `relationships-and-cascade-delete`

## Rules

### Rule 1

Agents fetching data for display inside a SwiftUI view MUST use `@Query` rather than manually calling `context.fetch(_:)` in the view's body. Per Apple's documentation, `Query` is "A type that fetches models using the specified criteria, and manages those models so they remain in sync with the underlying data" — it is declared `@MainActor @preconcurrency struct Query<Element, Result> where Element : PersistentModel`, and the `@Model` macro's `Observable` conformance is what lets SwiftUI refresh the view automatically as the underlying data changes.

### Rule 2

Agents filtering a `@Query` or `FetchDescriptor` MUST express the filter as a `Predicate<Model>` built with the `#Predicate` macro, not by fetching everything and filtering in Swift afterward. Per Apple's documentation' worked example, a predicate is built as `#Predicate<Quake> { quake in (searchText.isEmpty || quake.location.name.contains(searchText)) && (quake.time > start && quake.time < end) }` and then passed as `Query(filter: predicate, sort: \.magnitude, order: .reverse)` or `FetchDescriptor<T>(predicate: predicate, sortBy: ...)`.

### Rule 3

Agents needing sorted results MUST use the `sort:`/`order:` parameters on `@Query` (e.g. `@Query(sort: \.startDate, order: .reverse)`) or the `sortBy:` parameter on `FetchDescriptor` (`sortBy: [SortDescriptor<T>]`), and MUST NOT sort an already-fetched array in Swift when a descriptor-level sort would do. Per Apple's documentation, `FetchDescriptor.init(predicate:sortBy:)` is declared `init(predicate: Predicate<T>? = nil, sortBy: [SortDescriptor<T>] = [])`, and a `@Query` filter/sort initializer is declared `init<Value>(filter: Predicate<Element>? = nil, sort keyPath: KeyPath<Element, Value?>, order: SortOrder = .forward, animation: Animation) where Result == [Element], Value : Comparable`.

### Rule 4

Agents fetching outside a SwiftUI view's body — in a service type, a background task, or setup code for a preview — MUST use `FetchDescriptor<T>` together with `context.fetch(_:)`, and MUST NOT declare a `@Query` property on a non-View type. Per Apple's documentation, "Outside of a view, or if you're not using SwiftUI, use one of the two fetch methods on `ModelContext`. Each method expects an instance of `FetchDescriptor` containing a predicate and a sort order." `fetch(_:)` is declared `func fetch<T>(_ descriptor: FetchDescriptor<T>) throws -> [T] where T : PersistentModel` and returns "an array of typed models that match the criteria of the specified fetch descriptor," throwing rather than returning an `Observable`-backed live result.

### Rule 5

Agents MUST treat `context.fetch(_:)` results as a one-time snapshot rather than as data that stays synchronized with the store, since only `@Query` provides that live-update behavior. This is reasoned synthesis: `Query`'s documented behavior explicitly "manages those models so they remain in sync with the underlying data," while `fetch(_:)`'s documented behavior is only to return "an array of typed models that match the criteria" at the moment it's called — nothing in `ModelContext.fetch(_:)`'s documentation claims the returned array updates itself afterward.

## Compliant Example

```swift
import SwiftUI
import SwiftData

struct TripListView: View {
    @Query(sort: \Trip.startDate, order: .reverse) private var trips: [Trip] // Rule 1, Rule 3

    var body: some View {
        List(trips) { trip in Text(trip.name) }
    }
}

struct TripImportService {
    func upcomingTrips(context: ModelContext, after date: Date) throws -> [Trip] {
        let predicate = #Predicate<Trip> { $0.startDate > date } // Rule 2
        var descriptor = FetchDescriptor<Trip>(
            predicate: predicate,
            sortBy: [SortDescriptor(\Trip.startDate)] // Rule 3
        )
        descriptor.fetchLimit = 50
        return try context.fetch(descriptor) // Rule 4, Rule 5: one-time snapshot
    }
}
```

## Non-Compliant Example

```swift
import SwiftUI
import SwiftData

struct TripImportService {
    @Query private var trips: [Trip] // violates Rule 4 -- @Query used on a non-View type

    func upcomingTrips(context: ModelContext, after date: Date) throws -> [Trip] {
        // Fetches everything, then filters/sorts manually in Swift instead of
        // a #Predicate + sortBy descriptor -- violates Rule 2 and Rule 3.
        let all = try context.fetch(FetchDescriptor<Trip>())
        let filtered = all.filter { $0.startDate > date }.sorted { $0.startDate > $1.startDate }
        return filtered
    }
}

struct TripListView: View {
    var context: ModelContext
    var trips: [Trip] = []

    var body: some View {
        // Calls context.fetch(_:) directly in the view body instead of @Query,
        // so the list never updates when the store changes -- violates Rule 1 and Rule 5.
        List(try! context.fetch(FetchDescriptor<Trip>())) { trip in Text(trip.name) }
    }
}
```
Declares `@Query` on a non-View service type (Rule 4), fetches everything and filters/sorts in Swift instead of a predicate and sort descriptor (Rule 2, Rule 3), and fetches directly inside a view body instead of `@Query`, losing live updates (Rule 1, Rule 5).

## Dependencies

Depends on `model-definition` for the `@Model` types being queried, and on `model-container-setup` for the `ModelContainer`/`ModelContext` the query or fetch runs against.

## References

- [Apple Developer — Query](https://developer.apple.com/documentation/swiftdata/query)
- [Apple Developer — FetchDescriptor](https://developer.apple.com/documentation/swiftdata/fetchdescriptor)
- [Apple Developer — ModelContext](https://developer.apple.com/documentation/swiftdata/modelcontext)
- [Apple Developer — Predicate](https://developer.apple.com/documentation/foundation/predicate)
- [Apple Developer — Filtering and sorting persistent data](https://developer.apple.com/documentation/swiftdata/filtering-and-sorting-persistent-data)
- [Apple Developer — Preserving your app's model data across launches](https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches)
