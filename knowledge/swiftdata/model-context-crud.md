# Model Context CRUD

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.swiftdata.model-context-crud
artifact_type: knowledge
title: Model Context CRUD
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines using a SwiftData ModelContext for create/delete/save operations -- insert(_:), delete(_:), save(), when autosaveEnabled makes an explicit save() unnecessary versus when it's required, mainContext vs. creating a background/secondary ModelContext, and undo support via context.undoManager.
domain: SwiftData
tags:
  - swiftdata
  - modelcontext
  - crud
  - autosave
  - undo
references:
  - https://developer.apple.com/documentation/swiftdata/modelcontext
  - https://developer.apple.com/documentation/swiftdata/modelcontainer/maincontext
  - https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches
  - https://developer.apple.com/documentation/swiftdata/deleting-persistent-data-from-your-app
  - https://developer.apple.com/documentation/swiftdata/reverting-data-changes-using-the-undo-manager
depends_on:
  - knowledge.swiftdata.model-container-setup
related:
  - knowledge.swiftdata.model-definition
last_updated: 2026-08-08
```

## Intent

This contract governs using a `ModelContext` — obtained from `model-container-setup`'s container, either as `@Environment(\.modelContext)`, `container.mainContext`, or a manually created secondary context — to insert, delete, and save `@Model` instances (see `model-definition`), and to enable undo. It does not cover reading/fetching, which `querying-with-query-and-fetchdescriptor` governs.

## Scope

### Included

- `insert(_:)` and `delete(_:)` to register pending changes with a context
- `save()`, and when it's required versus when `autosaveEnabled` makes it optional
- `mainContext` (the container's main-actor-bound context) vs. `ModelContext(_:)` for a manually created secondary context
- `undoManager` for enabling undo/redo support on a context
- `hasChanges` for checking whether a context has unsaved state

### Excluded

- `FetchDescriptor`/`context.fetch(_:)` and `@Query` — see `querying-with-query-and-fetchdescriptor`
- Creating the `ModelContainer` a context belongs to — see `model-container-setup`
- `@Relationship(deleteRule:)` cascade/nullify/deny/noAction behavior during `delete(_:)` — see `relationships-and-cascade-delete`

## Rules

### Rule 1

Agents MUST call `context.insert(_:)` to register a new model instance with a context before it can be persisted, and MUST NOT assume merely initializing a `@Model` instance persists it. Per Apple's documentation, `insert(_:)` is declared `func insert<T>(_ model: T) where T : PersistentModel` and "Registers the specified model with the context so it can include the model in the next save operation." A model holds a temporary identifier until the context's first successful save of it.

### Rule 2

Agents MUST call `context.delete(_:)` to remove a model, and MUST NOT assume the removal is immediate and independent of the context's save cycle. Per Apple's documentation, `delete(_:)` is declared `func delete<T>(_ model: T) where T : PersistentModel` and "Removes the specified model from the persistent storage during the next save operation" — "If the model is new and in an unsaved state, the context simply discards it."

### Rule 3

Agents MUST check a context's `autosaveEnabled` value before deciding whether an explicit `save()` call is required, rather than always calling `save()` defensively or always omitting it. Per Apple's documentation, `autosaveEnabled` "indicates whether the context should automatically save any pending changes when certain events occur" and "SwiftData automatically sets this property to `true` for the model container's `mainContext`" while "the default value is `false`" otherwise — so a context obtained via `@Environment(\.modelContext)` or `container.mainContext` autosaves, but a context created manually with `ModelContext(_:)` does not unless the agent sets `autosaveEnabled = true` or calls `save()` explicitly.

### Rule 4

Agents needing a context that is not bound to the main actor (e.g., for off-main-thread batch import or export work) MUST create one with `ModelContext(_:)` against the app's existing `ModelContainer`, rather than reusing `mainContext` on a background queue. Per Apple's documentation, `init(_ container: ModelContainer)` "Creates a context that belongs to the specified model container," and separately, `mainContext` is declared `@MainActor var mainContext: ModelContext { get }` — a main-actor-bound property that is not meant for background-thread use.

### Rule 5

Agents adding undo support MUST assign an `UndoManager` to `context.undoManager` and SHOULD temporarily set it back to `nil` before large batch operations. Per Apple's documentation, "Assign an instance of `UndoManager` to this property to enable undo support for the context... If the context does use an undo manager, improve performance by temporarily setting this property to `nil` when performing expensive operations, such as importing large numbers of models." The default value is `nil`.

## Compliant Example

```swift
import SwiftData

struct TripStore {
    let mainContext: ModelContext // e.g. container.mainContext

    func addTrip(name: String) {
        let trip = Trip(name: name)
        mainContext.insert(trip) // Rule 1
        // mainContext.autosaveEnabled is true by default -- no explicit save() required (Rule 3)
    }

    func removeTrip(_ trip: Trip) throws {
        mainContext.delete(trip) // Rule 2
        try mainContext.save()   // explicit save for immediate persistence
    }

    func importManyTrips(_ names: [String], container: ModelContainer) throws {
        let backgroundContext = ModelContext(container) // Rule 4: secondary context
        backgroundContext.undoManager = nil              // Rule 5: disabled for a large batch
        for name in names { backgroundContext.insert(Trip(name: name)) }
        try backgroundContext.save() // Rule 3: this context does not autosave
    }
}
```

## Non-Compliant Example

```swift
import SwiftData

func addAndImport(names: [String], mainContext: ModelContext, container: ModelContainer) {
    for name in names {
        let trip = Trip(name: name)
        // Never calls mainContext.insert(trip) -- violates Rule 1.
    }

    // Reuses the main-actor mainContext for a large background import
    // instead of a secondary ModelContext(container) -- violates Rule 4.
    for name in names {
        mainContext.delete(Trip(name: name)) // deleting an unsaved, never-inserted instance -- violates Rule 2
    }
    // Assumes autosave always happens and never checks autosaveEnabled or calls save() -- violates Rule 3.
    // Never assigns undoManager, then still expects undo to work -- violates Rule 5.
}
```
Never inserts new instances before expecting them persisted (Rule 1), deletes instances that were never registered (Rule 2), assumes autosave without checking `autosaveEnabled` (Rule 3), reuses the main-actor context for background batch work instead of a secondary context (Rule 4), and expects undo without assigning `undoManager` (Rule 5).

## Dependencies

Depends on `model-container-setup` for the `ModelContainer`/`ModelContext` this contract operates on, and on `model-definition` for the `@Model` instances being inserted, deleted, or saved.

## References

- [Apple Developer — ModelContext](https://developer.apple.com/documentation/swiftdata/modelcontext)
- [Apple Developer — ModelContainer.mainContext](https://developer.apple.com/documentation/swiftdata/modelcontainer/maincontext)
- [Apple Developer — Preserving your app's model data across launches](https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches)
- [Apple Developer — Deleting persistent data from your app](https://developer.apple.com/documentation/swiftdata/deleting-persistent-data-from-your-app)
- [Apple Developer — Reverting data changes using the undo manager](https://developer.apple.com/documentation/swiftdata/reverting-data-changes-using-the-undo-manager)
