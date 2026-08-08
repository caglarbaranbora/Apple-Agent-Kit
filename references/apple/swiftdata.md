# SwiftData

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.swiftdata
artifact_type: reference
title: SwiftData
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's SwiftData documentation, scoped to this domain's v1.
domain: SwiftData
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/foundation/predicate
https://developer.apple.com/documentation/swiftdata
https://developer.apple.com/documentation/swiftdata/attribute(_:originalname:hashmodifier:)
https://developer.apple.com/documentation/swiftdata/defining-data-relationships-with-enumerations-and-model-classes
https://developer.apple.com/documentation/swiftdata/deleting-persistent-data-from-your-app
https://developer.apple.com/documentation/swiftdata/fetchdescriptor
https://developer.apple.com/documentation/swiftdata/filtering-and-sorting-persistent-data
https://developer.apple.com/documentation/swiftdata/model()
https://developer.apple.com/documentation/swiftdata/modelconfiguration
https://developer.apple.com/documentation/swiftdata/modelcontainer
https://developer.apple.com/documentation/swiftdata/modelcontainer/maincontext
https://developer.apple.com/documentation/swiftdata/modelcontext
https://developer.apple.com/documentation/swiftdata/persistentmodel
https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches
https://developer.apple.com/documentation/swiftdata/query
https://developer.apple.com/documentation/swiftdata/relationship(_:deleterule:minimummodelcount:maximummodelcount:originalname:inverse:hashmodifier:)
https://developer.apple.com/documentation/swiftdata/reverting-data-changes-using-the-undo-manager
https://developer.apple.com/documentation/swiftdata/schema/relationship/deleterule-swift.enum
https://developer.apple.com/documentation/swiftdata/transient()
https://developer.apple.com/documentation/swiftui/environmentvalues/modelcontext
https://developer.apple.com/documentation/swiftui/view/modelcontainer(_:)
https://developer.apple.com/documentation/swiftui/view/modelcontainer(for:inmemory:isautosaveenabled:isundoenabled:onsetup:)

## Purpose

Reference index for Apple's SwiftData documentation, scoped to this domain's v1: declaring persistent model classes with the `@Model` macro plus `@Attribute`, `@Relationship`, and `@Transient`; creating and injecting a `ModelContainer` via SwiftUI's `.modelContainer(for:)`/`.modelContainer(_:)` modifiers or a manual `ModelContainer(for:configurations:)` initializer, and configuring storage with `ModelConfiguration`; performing CRUD through `ModelContext` (`insert(_:)`, `delete(_:)`, `save()`, `autosaveEnabled`, `undoManager`); fetching declaratively in SwiftUI with `@Query` (`#Predicate`, `sort:`, `order:`) versus imperatively with `FetchDescriptor`/`context.fetch(_:)`; and controlling referential integrity on delete with `@Relationship(deleteRule:)`. SwiftData is Apple's modern, SwiftUI-native persistence framework; it is a distinct framework from Core Data (`NSManagedObjectContext`, `NSFetchRequest`), which is its own separate domain not documented here.

Out of scope for v1: CloudKit sync integration (`ModelConfiguration(cloudKitDatabase:)`, `groupContainer`); `SchemaMigrationPlan`/`VersionedSchema` and lightweight vs. custom migration; the Core Data interop/migration path; the `#Index`/`#Unique` macros beyond the basic `@Attribute(.unique)` mention; and SwiftData in widget extensions or App Group container sharing.

## Primary Topics

- `@Model`, `@Attribute`, `@Relationship`, `@Transient`, and what SwiftData auto-synthesizes on a model class
- `ModelContainer`/`ModelConfiguration` creation and SwiftUI injection via `.modelContainer`
- `ModelContext` CRUD, autosave behavior, and undo support
- `@Query` versus `FetchDescriptor` + `context.fetch(_:)` for reading persisted data
- `@Relationship(deleteRule:)` and inverse relationships for referential integrity

## Used By

- knowledge/swiftdata/model-definition.md ([[knowledge/swiftdata/model-definition]])
- knowledge/swiftdata/model-container-setup.md ([[knowledge/swiftdata/model-container-setup]])
- knowledge/swiftdata/model-context-crud.md ([[knowledge/swiftdata/model-context-crud]])
- knowledge/swiftdata/querying-with-query-and-fetchdescriptor.md ([[knowledge/swiftdata/querying-with-query-and-fetchdescriptor]])
- knowledge/swiftdata/relationships-and-cascade-delete.md ([[knowledge/swiftdata/relationships-and-cascade-delete]])
- skills/swiftdata/SKILL.md ([[skills/swiftdata/SKILL]])
