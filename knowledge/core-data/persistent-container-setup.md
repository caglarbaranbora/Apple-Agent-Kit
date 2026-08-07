# Persistent Container Setup

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.core-data.persistent-container-setup
artifact_type: knowledge
title: Persistent Container Setup
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines standing up a Core Data stack with NSPersistentContainer -- constructing it with init(name:), loading stores with loadPersistentStores(completionHandler:) and handling its error, reading the main-queue viewContext, and configuring an individual store via NSPersistentStoreDescription/persistentStoreDescriptions before loading.
domain: Core Data
tags:
  - core-data
  - nspersistentcontainer
  - loadpersistentstores
  - viewcontext
  - nspersistentstoredescription
references:
  - https://developer.apple.com/documentation/coredata/nspersistentcontainer
  - https://developer.apple.com/documentation/coredata/nspersistentcontainer/init(name:)
  - https://developer.apple.com/documentation/coredata/nspersistentcontainer/loadpersistentstores(completionhandler:)
  - https://developer.apple.com/documentation/coredata/nspersistentcontainer/viewcontext
  - https://developer.apple.com/documentation/coredata/nspersistentstoredescription
  - https://developer.apple.com/documentation/swiftui/fetchrequest
depends_on:
  - knowledge.core-data.model-definition
related:
  - knowledge.core-data.managed-object-context-crud
last_updated: 2026-08-06
```

## Intent

This contract governs creating a Core Data stack for entities defined per `model-definition` and making its main-queue context available to the rest of the app: `NSPersistentContainer(name:)`, `loadPersistentStores(completionHandler:)` and its error handling, `viewContext`, and `NSPersistentStoreDescription` for configuring an individual store before it loads. Once a context is available, `managed-object-context-crud` governs using it.

## Scope

### Included

- `NSPersistentContainer(name:)` and how the name resolves to both the store's file name and the `NSManagedObjectModel` to use
- `loadPersistentStores(completionHandler:)` and inspecting its `(NSPersistentStoreDescription, Error?)` completion arguments
- `viewContext`, the container's main-queue-associated context
- `NSPersistentStoreDescription` and `persistentStoreDescriptions` for per-store configuration (e.g. `url`, `setOption(_:forKey:)`) set before loading
- Injecting `viewContext` into a SwiftUI environment via `.environment(\.managedObjectContext, container.viewContext)`

### Excluded

- CRUD once a context exists — see `managed-object-context-crud`
- `NSPersistentCloudKitContainer`/CloudKit sync — out of scope for v1
- Lightweight/mapping-model migration — out of scope for v1
- `NSFetchRequest`/fetching — see `fetching-with-nsfetchrequest`

## Rules

### Rule 1

Agents standing up a Core Data stack SHOULD create one `NSPersistentContainer(name:)` rather than assembling `NSManagedObjectModel`/`NSPersistentStoreCoordinator`/`NSManagedObjectContext` by hand, since the container "simplifies the creation and management of the Core Data stack ... by handling the creation of the managed object model, persistent store coordinator, and the managed object context." Per `init(name:)`'s documentation, "the provided name value is used to name the persistent store and is used to look up the name of the `NSManagedObjectModel` object to be used with the `NSPersistentContainer` object."

### Rule 2

Agents MUST call `loadPersistentStores(completionHandler:)` after constructing the container and before using `viewContext`, and MUST check the completion handler's `Error?` argument rather than assuming the store always loads. Per Apple's documentation: "Once the persistent container has been initialized, you need to execute `loadPersistentStores(completionHandler:)` to instruct the container to load the persistent stores... If there is an error in the loading of the persistent stores, the `NSError` value will be populated." Only once the handler fires is "the stack ... fully initialized and ... ready for use."

### Rule 3

Agents needing to customize a store's location or behavior (e.g. an in-memory store for tests/previews) MUST configure `persistentStoreDescriptions` before calling `loadPersistentStores(completionHandler:)`, since Apple's documentation states: "If you will be configuring custom persistent store descriptions, you must set this property before calling `loadPersistentStores(completionHandler:)`." Per-store options are set with `NSPersistentStoreDescription.setOption(_:forKey:)`, not by mutating the container's model afterward.

### Rule 4

Agents reading or writing on the main thread/UI layer SHOULD use the container's `viewContext` rather than constructing a separate main-queue context, since `viewContext` "contains a reference to the `NSManagedObjectContext` that is created and owned by the persistent container which is associated with the main queue of the application" and "is created automatically as part of the initialization of the persistent container."

### Rule 5

Agents building a SwiftUI app MUST inject the container's context into the environment with `.environment(\.managedObjectContext, container.viewContext)` so that `@FetchRequest` and `@Environment(\.managedObjectContext)` can resolve it in descendant views, mirroring Apple's documented pattern: "the fetch request and its results use the managed object context stored in the environment," set for example with `ContentView().environment(\.managedObjectContext, QuakesProvider.shared.container.viewContext)`.

## Compliant Example

```swift
import CoreData
import SwiftUI

final class PersistenceController {
    static let shared = PersistenceController()
    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "TaskModel") // Rule 1
        if inMemory {
            let description = NSPersistentStoreDescription(url: URL(fileURLWithPath: "/dev/null"))
            container.persistentStoreDescriptions = [description] // Rule 3: set before loading
        }
        container.loadPersistentStores { _, error in // Rule 2
            if let error { fatalError("Failed to load store: \(error)") }
        }
    }
}

@main
struct TasksApp: App {
    let persistence = PersistenceController.shared
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistence.container.viewContext) // Rule 4, 5
        }
    }
}
```

## Non-Compliant Example

```swift
import CoreData
import SwiftUI

final class PersistenceController {
    let container = NSPersistentContainer(name: "TaskModel")
    // init() never calls loadPersistentStores(completionHandler:) -- violates Rule 2.

    func addSampleData() {
        let context = container.viewContext // used against a possibly-unloaded store
        try? context.save() // the (never-called) completion handler's error goes unchecked
    }
}

struct ContentView: View {
    // Never injects .environment(\.managedObjectContext, ...) above this view --
    // violates Rule 5. @FetchRequest below has no context to resolve.
    @FetchRequest(sortDescriptors: []) private var tasks: FetchedResults<NSManagedObject>
    var body: some View { Text("Tasks") }
}
```
Never calls `loadPersistentStores(completionHandler:)` before using `viewContext` (Rule 2), and never injects the context into the SwiftUI environment for `@FetchRequest` to find (Rule 5).

## Dependencies

Depends on `model-definition` for the entities the container's `NSManagedObjectModel` is built from.

## References

- [Apple Developer — NSPersistentContainer](https://developer.apple.com/documentation/coredata/nspersistentcontainer)
- [Apple Developer — init(name:)](https://developer.apple.com/documentation/coredata/nspersistentcontainer/init(name:))
- [Apple Developer — loadPersistentStores(completionHandler:)](https://developer.apple.com/documentation/coredata/nspersistentcontainer/loadpersistentstores(completionhandler:))
- [Apple Developer — viewContext](https://developer.apple.com/documentation/coredata/nspersistentcontainer/viewcontext)
- [Apple Developer — NSPersistentStoreDescription](https://developer.apple.com/documentation/coredata/nspersistentstoredescription)
- [Apple Developer — FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest)
