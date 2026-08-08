# Managed Object Context CRUD

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.core-data.managed-object-context-crud
artifact_type: knowledge
title: Managed Object Context CRUD
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines using NSManagedObjectContext for create/delete/save operations -- inserting via NSEntityDescription.insertNewObject(forEntityName:into:) or the generated init(context:), delete(_:), save() and its throwing/error behavior, perform(_:)/performAndWait(_:) thread confinement, and a basic parent-child context relationship via parent.
domain: Core Data
tags:
  - core-data
  - nsmanagedobjectcontext
  - crud
  - perform
  - parent-context
references:
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext
  - https://developer.apple.com/documentation/coredata/nsentitydescription/insertnewobject(forentityname:into:)
  - https://developer.apple.com/documentation/coredata/nsmanagedobject/init(context:)
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/insert(_:)
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/delete(_:)
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/save()
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/perform(_:)
  - https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/parent
depends_on:
  - knowledge.core-data.persistent-container-setup
related:
  - knowledge.core-data.model-definition
  - knowledge.core-data.fetching-with-nsfetchrequest
last_updated: 2026-08-08
```

## Intent

This contract governs using an `NSManagedObjectContext` — obtained from `persistent-container-setup`'s container as `viewContext` or a manually created context — to insert, delete, and save managed objects defined per `model-definition`, to confine that work to the context's own queue, and to set up a basic parent-child context relationship. It does not cover reading/fetching, which `fetching-with-nsfetchrequest` governs.

## Scope

### Included

- Inserting via `NSEntityDescription.insertNewObject(forEntityName:into:)` or a generated subclass's `init(context:)` convenience initializer
- `delete(_:)`
- `save()`, its throwing behavior, and checking `hasChanges` first
- `perform(_:)`/`performAndWait(_:)` for thread confinement
- A basic parent-child context relationship via the `parent` property

### Excluded

- `NSFetchRequest`/`context.fetch(_:)` and `@FetchRequest` — see `fetching-with-nsfetchrequest`
- Creating the `NSPersistentContainer`/store a context belongs to — see `persistent-container-setup`
- `NSDeleteRule` cascade/nullify/deny/no-action behavior during `delete(_:)` — see `relationships-and-delete-rules`
- Concurrency patterns beyond one parent and one child context — out of scope for v1

## Rules

### Rule 1

Agents creating a new managed object MUST register it with a context via `NSEntityDescription.insertNewObject(forEntityName:into:)` or a generated subclass's `init(context:)`, and MUST NOT instantiate a managed object with a bare initializer and expect it to be tracked. Per Apple's documentation, `insertNewObject(forEntityName:into:)` "Creates, configures, and returns... a new, autoreleased, fully configured instance" that already "has its entity description set and is inserted... into `context`"; the generated `init(context:)` "Initializes a managed object subclass and inserts it into the specified managed object context."

### Rule 2

Agents removing a managed object MUST call `context.delete(_:)`, and MUST NOT assume the removal happens immediately and independently of the context's save cycle. Per Apple's documentation, `delete(_:)` "Specifies an object that should be removed from its persistent store when changes are committed... If `object` has not yet been saved to a persistent store, it is simply removed from the receiver."

### Rule 3

Agents MUST check `context.hasChanges` before calling `save()` and MUST handle the error `save() throws` can raise rather than force-trying it. Apple's documentation instructs: "Always verify that the context has uncommitted changes (using the `hasChanges` property) before invoking the save: method. Otherwise, Core Data may perform unnecessary work," and notes that multiple validation failures surface as an `NSError` whose `userInfo` dictionary carries the `NSDetailedErrors` key.

### Rule 4

Agents operating on a queue-confined context MUST wrap context work in `perform(_:)` (asynchronous, returns immediately) or `performAndWait(_:)` (synchronous, blocks until the block finishes) rather than calling context methods directly from an arbitrary thread. Per Apple's documentation: "`perform(_:)` and `performAndWait(_:)` ensure the block operations execute on the correct queue for the context. The `perform(_:)` method returns immediately... With the `performAndWait(_:)` method, the context still executes the block methods on its own thread, but the method doesn't return until the block completes." Code already running on the main thread against a main-queue context is the one documented exception that may call the context directly.

### Rule 5

Agents needing a lightweight child context MUST set its `parent` to an existing context rather than expecting it to reach a persistent store coordinator on its own, and MUST remember that saving a child only commits changes "one store up" to its parent, not to the persistent store, until that parent is also saved. Per Apple's documentation: "If a context's parent store is another managed object context, fetch and save operations are mediated by the parent context instead of a coordinator... a parent does not pull changes from children before it saves. You must save a child context if you want ultimately to commit the changes."

## Compliant Example

```swift
import CoreData

func addTask(title: String, context: NSManagedObjectContext) {
    context.perform { // Rule 4
        let task = Task(context: context) // Rule 1
        task.title = title
        guard context.hasChanges else { return } // Rule 3
        do { try context.save() } catch { print("Failed to save: \(error)") } // Rule 3
    }
}

func removeTask(_ task: Task, context: NSManagedObjectContext) {
    context.perform { // Rule 4
        context.delete(task) // Rule 2
        if context.hasChanges { try? context.save() } // Rule 3
    }
}

func makeEditingChildContext(of parent: NSManagedObjectContext) -> NSManagedObjectContext {
    let child = NSManagedObjectContext(concurrencyType: .mainQueueConcurrencyType)
    child.parent = parent // Rule 5: child of an existing context, not the store coordinator
    return child
}
```

## Non-Compliant Example

```swift
import CoreData

func addTask(title: String, context: NSManagedObjectContext) {
    let task = Task() // violates Rule 1 -- bare initializer, never inserted into context
    task.title = title

    try! context.save() // violates Rule 3 -- force-tries save(), never checks hasChanges
    // Runs directly on whatever thread called this, not inside perform(_:) -- violates Rule 4.
}

func removeTask(_ task: Task) {
    task.isComplete = true // violates Rule 2 -- never calls context.delete(_:) at all
}

func makeEditingChildContext() -> NSManagedObjectContext {
    let child = NSManagedObjectContext(concurrencyType: .mainQueueConcurrencyType)
    // Never sets `parent` -- violates Rule 5; any later save() has nowhere to commit to.
    return child
}
```
Never inserts a new instance before expecting it persisted (Rule 1), never calls `delete(_:)` to remove an object (Rule 2), force-tries `save()` without checking `hasChanges` (Rule 3), runs context work outside `perform(_:)` (Rule 4), and creates a child context with no `parent` set (Rule 5).

## Dependencies

Depends on `persistent-container-setup` for the `NSManagedObjectContext` this contract operates on, and on `model-definition` for the managed object instances being inserted, deleted, or saved.

## References

- [Apple Developer — NSManagedObjectContext](https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext)
- [Apple Developer — insertNewObject(forEntityName:into:)](https://developer.apple.com/documentation/coredata/nsentitydescription/insertnewobject(forentityname:into:))
- [Apple Developer — init(context:)](https://developer.apple.com/documentation/coredata/nsmanagedobject/init(context:))
- [Apple Developer — delete(_:)](https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/delete(_:))
- [Apple Developer — save()](https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/save())
- [Apple Developer — perform(_:)](https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/perform(_:))
- [Apple Developer — parent](https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/parent)
