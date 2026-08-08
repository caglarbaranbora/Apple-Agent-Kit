# Fetching With NSFetchRequest

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.core-data.fetching-with-nsfetchrequest
artifact_type: knowledge
title: Fetching With NSFetchRequest
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines fetching managed objects with NSFetchRequest<T> -- filtering with NSPredicate, sorting with NSSortDescriptor, executing via context.fetch(_:), and SwiftUI's @FetchRequest property wrapper as the SwiftUI-side convenience over the same request.
domain: Core Data
tags:
  - core-data
  - nsfetchrequest
  - nspredicate
  - nssortdescriptor
  - fetchrequest
references:
  - https://developer.apple.com/documentation/coredata/nsfetchrequest
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/fetch(_:)-4xeoz
  - https://developer.apple.com/documentation/foundation/nspredicate
  - https://developer.apple.com/documentation/foundation/nssortdescriptor
  - https://developer.apple.com/documentation/swiftui/fetchrequest
depends_on:
  - knowledge.core-data.model-definition
  - knowledge.core-data.persistent-container-setup
related:
  - knowledge.core-data.managed-object-context-crud
last_updated: 2026-08-08
```

## Intent

This contract governs reading managed objects defined per `model-definition` back out of Core Data: building an `NSFetchRequest<T>` with an `NSPredicate` filter and `NSSortDescriptor` sort order and executing it with `context.fetch(_:)`, and the SwiftUI-side `@FetchRequest` property wrapper that wraps the same mechanics for a view. Both require a context already set up per `persistent-container-setup`.

## Scope

### Included

- `NSFetchRequest<T>` construction, typically via a generated subclass's `fetchRequest()` class method or `NSFetchRequest<T>(entityName:)`
- `NSPredicate` assigned to a request's `predicate` property, including format-string predicates
- `NSSortDescriptor` assigned to a request's `sortDescriptors` property, including the type-safe `init(keyPath:ascending:)`
- `NSManagedObjectContext.fetch(_:)` for executing a request
- SwiftUI's `@FetchRequest` property wrapper, declared with `sortDescriptors:`/`predicate:` or from an already-configured `NSFetchRequest`

### Excluded

- `NSFetchedResultsController` — out of scope for v1 (UIKit-specific, deferred to a future increment)
- Inserting, deleting, or saving fetched results — see `managed-object-context-crud`
- Relationship-aware prefetching and how delete rules affect a fetched object graph — see `relationships-and-delete-rules`

## Rules

### Rule 1

Agents fetching managed objects outside a SwiftUI view MUST build an `NSFetchRequest<T>` and execute it with `context.fetch(_:)` rather than loading every instance and filtering in Swift. Per Apple's documentation, `NSFetchRequest` "collects the criteria needed to select and optionally to sort a group of... managed objects," and the generic overload on `NSManagedObjectContext`, declared `func fetch<T>(_ request: NSFetchRequest<T>) throws -> [T]`, "Returns an array of objects that meet the criteria of the specified fetch request."

### Rule 2

Agents filtering a fetch MUST assign an `NSPredicate` to the request's `predicate` property rather than fetching unfiltered results and filtering afterward, since "If the fetch request has no predicate, then all instances of the specified entity are retrieved." Predicates are commonly built from a format string, per Apple's own `NSFetchRequest` documentation example: `request.predicate = NSPredicate(format: "isChecked = false")`.

### Rule 3

Agents needing ordered results MUST assign an array of `NSSortDescriptor` to the request's `sortDescriptors` property rather than sorting the fetched array in Swift afterward, since `NSSortDescriptor` exists to "specify... the order of objects that return from a Core Data fetch request." Apple's own example builds one with the type-safe key-path initializer: `NSSortDescriptor(keyPath: \ShoppingItem.name, ascending: true)`, declared `init<Root, Value>(keyPath: KeyPath<Root, Value>, ascending: Bool)`.

### Rule 4

Agents fetching for display inside a SwiftUI view MUST use the `@FetchRequest` property wrapper, declared `private`, rather than calling `context.fetch(_:)` directly in the view's body. Per Apple's documentation, `@FetchRequest` "retrieves entities from a Core Data persistent store," and can be declared either with inferred criteria — `@FetchRequest(sortDescriptors: [SortDescriptor(\.time, order: .reverse)]) private var quakes: FetchedResults<Quake>` — or from an already-configured `NSFetchRequest` — `@FetchRequest(fetchRequest: request) private var items: FetchedResults<ShoppingItem>`. Apple's documentation adds: "Always declare properties that have a fetch request wrapper as private. This lets the compiler help you avoid accidentally setting the property from the memberwise initializer of the enclosing view."

### Rule 5

Agents using `@FetchRequest` MUST ensure a managed object context has been injected into the SwiftUI environment (see `persistent-container-setup`'s `.environment(\.managedObjectContext, container.viewContext)`), since "the fetch request and its results use the managed object context stored in the environment."

## Compliant Example

```swift
import CoreData
import SwiftUI

// Outside a view -- Rule 1, Rule 2, Rule 3
func incompleteTasks(context: NSManagedObjectContext) throws -> [Task] {
    let request = Task.fetchRequest()
    request.predicate = NSPredicate(format: "isComplete == NO") // Rule 2
    request.sortDescriptors = [NSSortDescriptor(keyPath: \Task.title, ascending: true)] // Rule 3
    return try context.fetch(request) // Rule 1
}

struct TaskListView: View {
    @FetchRequest( // Rule 4, Rule 5
        sortDescriptors: [SortDescriptor(\Task.title, order: .forward)]
    ) private var tasks: FetchedResults<Task>

    var body: some View {
        List(tasks) { task in Text(task.title ?? "") }
    }
}
```

## Non-Compliant Example

```swift
import CoreData
import SwiftUI

func incompleteTasks(context: NSManagedObjectContext) throws -> [Task] {
    // Fetches everything, then filters/sorts in Swift instead of predicate/sortDescriptors --
    // violates Rule 2 and Rule 3.
    let all = try context.fetch(Task.fetchRequest())
    return all.filter { $0.isComplete == false }.sorted { ($0.title ?? "") < ($1.title ?? "") }
}

struct TaskListView: View {
    var context: NSManagedObjectContext

    var body: some View {
        // Fetches directly inside the view body instead of @FetchRequest, so the list
        // never updates when the store changes -- violates Rule 4.
        List(try! context.fetch(Task.fetchRequest())) { task in Text(task.title ?? "") }
    }
}
```
Fetches everything and filters/sorts in Swift instead of a predicate and sort descriptors (Rule 2, Rule 3), and fetches directly inside a view body instead of `@FetchRequest`, losing live updates (Rule 4).

## Dependencies

Depends on `model-definition` for the managed object types being fetched, and on `persistent-container-setup` for the context a fetch runs against.

## References

- [Apple Developer — NSFetchRequest](https://developer.apple.com/documentation/coredata/nsfetchrequest)
- [Apple Developer — fetch(_:)](https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/fetch(_:)-4xeoz)
- [Apple Developer — NSPredicate](https://developer.apple.com/documentation/foundation/nspredicate)
- [Apple Developer — NSSortDescriptor](https://developer.apple.com/documentation/foundation/nssortdescriptor)
- [Apple Developer — FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest)
