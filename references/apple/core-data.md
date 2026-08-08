# Core Data

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: reference.apple.core-data
artifact_type: reference
title: Core Data
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's Core Data documentation, scoped to this domain's v1.
domain: Core Data
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/coredata
https://developer.apple.com/documentation/coredata/configuring-relationships
https://developer.apple.com/documentation/coredata/generating-code
https://developer.apple.com/documentation/coredata/nsdeleterule
https://developer.apple.com/documentation/coredata/nsentitydescription
https://developer.apple.com/documentation/coredata/nsentitydescription/insertnewobject(forentityname:into:)
https://developer.apple.com/documentation/coredata/nsfetchrequest
https://developer.apple.com/documentation/coredata/nsmanagedobject
https://developer.apple.com/documentation/coredata/nsmanagedobject/init(context:)
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/delete(_:)
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/fetch(_:)-4xeoz
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/insert(_:)
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/parent
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/perform(_:)
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/performandwait(_:)-ypye
https://developer.apple.com/documentation/coredata/nsmanagedobjectcontext/save()
https://developer.apple.com/documentation/coredata/nspersistentcontainer
https://developer.apple.com/documentation/coredata/nspersistentcontainer/init(name:)
https://developer.apple.com/documentation/coredata/nspersistentcontainer/loadpersistentstores(completionhandler:)
https://developer.apple.com/documentation/coredata/nspersistentcontainer/viewcontext
https://developer.apple.com/documentation/coredata/nspersistentstoredescription
https://developer.apple.com/documentation/coredata/nsrelationshipdescription
https://developer.apple.com/documentation/coredata/nsrelationshipdescription/deleterule
https://developer.apple.com/documentation/coredata/nsrelationshipdescription/inverserelationship
https://developer.apple.com/documentation/foundation/nspredicate
https://developer.apple.com/documentation/foundation/nssortdescriptor
https://developer.apple.com/documentation/swiftui/fetchrequest

## Purpose

Reference index for Apple's Core Data documentation, scoped to this domain's v1: declaring `NSManagedObject` subclasses and configuring them through the `.xcdatamodeld` model editor's three code-generation modes (Class Definition / Manual/None / Category+Extension) plus `@NSManaged` property declarations; standing up a Core Data stack with `NSPersistentContainer`, `loadPersistentStores(completionHandler:)`, `viewContext`, and `NSPersistentStoreDescription` for per-store configuration; performing CRUD through `NSManagedObjectContext` (`NSEntityDescription.insertNewObject(forEntityName:into:)`/the generated `init(context:)`, `delete(_:)`, `save()`, `perform(_:)`/`performAndWait(_:)` thread confinement, and a basic parent-child context relationship via `parent`); fetching with `NSFetchRequest<T>`, `NSPredicate`, `NSSortDescriptor`, and SwiftUI's `@FetchRequest` property wrapper; and configuring relationships and referential integrity with `NSDeleteRule` (`.cascadeDeleteRule`/`.nullifyDeleteRule`/`.denyDeleteRule`/`.noActionDeleteRule`) and inverse relationships via `NSRelationshipDescription`. Core Data is Apple's older, Objective-C-rooted persistence framework for non-SwiftUI and legacy codebases; it is a distinct framework from SwiftData (`@Model`, `ModelContainer`, `ModelContext`), which is its own separate domain not documented here.

Out of scope for v1: `NSPersistentCloudKitContainer`/CloudKit sync; lightweight and mapping-model migration (`NSMigrationManager`, versioned/mapping models); `NSFetchedResultsController` (UIKit-specific, deferred to a future increment); multi-context concurrency patterns beyond a basic parent-child relationship; and any Core Data-to-SwiftData interop.

## Primary Topics

- `NSManagedObject` subclassing, `.xcdatamodeld` Codegen modes (Class Definition / Manual/None / Category+Extension), and `@NSManaged` properties
- `NSPersistentContainer`, `loadPersistentStores(completionHandler:)`, `viewContext`, and `NSPersistentStoreDescription` store configuration
- `NSManagedObjectContext` CRUD, `perform(_:)`/`performAndWait(_:)` thread confinement, and a basic parent-child context relationship
- `NSFetchRequest<T>` with `NSPredicate`/`NSSortDescriptor`, `context.fetch(_:)`, and SwiftUI's `@FetchRequest`
- `NSDeleteRule` cases and inverse relationships via `NSRelationshipDescription`

## Used By

- knowledge/core-data/model-definition.md ([[knowledge/core-data/model-definition]])
- knowledge/core-data/persistent-container-setup.md ([[knowledge/core-data/persistent-container-setup]])
- knowledge/core-data/managed-object-context-crud.md ([[knowledge/core-data/managed-object-context-crud]])
- knowledge/core-data/fetching-with-nsfetchrequest.md ([[knowledge/core-data/fetching-with-nsfetchrequest]])
- knowledge/core-data/relationships-and-delete-rules.md ([[knowledge/core-data/relationships-and-delete-rules]])
- skills/core-data/SKILL.md ([[skills/core-data/SKILL]])
