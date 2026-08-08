---
name: core-data
description: Route Core Data implementation tasks to the correct Knowledge Contracts -- subclassing NSManagedObject and choosing an .xcdatamodeld Codegen mode (Class Definition/Manual-None/Category+Extension) with @NSManaged properties, standing up NSPersistentContainer via loadPersistentStores(completionHandler:) and viewContext with NSPersistentStoreDescription store options, NSManagedObjectContext CRUD (insertNewObject(forEntityName:into:)/init(context:), delete(_:), save(), perform(_:)/performAndWait(_:), parent), fetching with NSFetchRequest<T>/NSPredicate/NSSortDescriptor/context.fetch(_:)/@FetchRequest, and NSDeleteRule referential integrity. Use when writing @NSManaged public var, NSEntityDescription.insertNewObject(forEntityName:into:), Task(context:), NSPersistentContainer(name:), container.loadPersistentStores { }, container.viewContext, NSPersistentStoreDescription, context.insert(_:)/delete(_:)/save(), context.perform { }/performAndWait { }, context.parent, NSFetchRequest<Item>(entityName:), NSPredicate(format:), NSSortDescriptor(keyPath:ascending:), @FetchRequest(sortDescriptors:)/@FetchRequest(fetchRequest:), or choosing .cascadeDeleteRule/.nullifyDeleteRule/.denyDeleteRule/.noActionDeleteRule and inverseRelationship. v1 is Core Data only -- no NSPersistentCloudKitContainer/CloudKit sync, no lightweight or mapping-model migration (NSMigrationManager, versioned/mapping models), no NSFetchedResultsController, no multi-context concurrency beyond a basic parent-child relationship, and no SwiftData interop (@Model/ModelContainer/ModelContext are a separate domain). Triggers on Core Data, NSManagedObject, NSManagedObjectContext, NSPersistentContainer, NSPersistentStoreDescription, NSEntityDescription, NSFetchRequest, NSPredicate, NSSortDescriptor, @FetchRequest, FetchedResults, NSRelationshipDescription, NSDeleteRule, viewContext, xcdatamodeld, Codegen, @NSManaged.
id: skill.core-data.foundations
title: Core Data — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: Core Data
routes: [knowledge.core-data.model-definition, knowledge.core-data.persistent-container-setup, knowledge.core-data.managed-object-context-crud, knowledge.core-data.fetching-with-nsfetchrequest, knowledge.core-data.relationships-and-delete-rules]
related: []
last_updated: 2026-08-08
---

# Core Data — Foundations Skill

## Purpose

Route Core Data implementation tasks to the minimum required Core Data
Knowledge Contracts. v1 scope is subclassing `NSManagedObject` and choosing
an `.xcdatamodeld` Codegen mode with `@NSManaged` properties, standing up
and loading an `NSPersistentContainer`, performing CRUD through an
`NSManagedObjectContext` with basic thread confinement and a basic
parent-child context relationship, fetching with `NSFetchRequest`/
`@FetchRequest`, and `NSDeleteRule`/inverse-relationship referential
integrity -- not CloudKit sync, not migration, not
`NSFetchedResultsController`, not advanced multi-context concurrency, and
not SwiftData interop.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/core-data/.

-   Subclassing `NSManagedObject`; choosing a Codegen mode (Class
    Definition/Category+Extension/Manual-None); declaring `@NSManaged`
    attribute or relationship properties; or asking what Xcode's generated
    code does and doesn't synthesize -> model-definition.md
-   Constructing `NSPersistentContainer(name:)`; calling
    `loadPersistentStores(completionHandler:)` and handling its error;
    reading `viewContext`; configuring a store via
    `NSPersistentStoreDescription`/`persistentStoreDescriptions`; or
    injecting a context with `.environment(\.managedObjectContext, ...)`
    -> persistent-container-setup.md
-   Inserting via `NSEntityDescription.insertNewObject(forEntityName:into:)`
    or a generated `init(context:)`; calling `delete(_:)`/`save()`;
    checking `hasChanges`; wrapping work in `perform(_:)`/
    `performAndWait(_:)`; or setting up a basic parent-child context via
    `parent` -> managed-object-context-crud.md
-   Building an `NSFetchRequest<T>` with a `predicate`/`sortDescriptors`;
    calling `context.fetch(_:)`; or declaring `@FetchRequest` in a SwiftUI
    view -> fetching-with-nsfetchrequest.md
-   Choosing an `NSDeleteRule` value (`.cascadeDeleteRule`/
    `.nullifyDeleteRule`/`.denyDeleteRule`/`.noActionDeleteRule`);
    reasoning about what happens to related objects on delete; or
    diagnosing a relationship missing its `inverseRelationship` ->
    relationships-and-delete-rules.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/core-data/ — do not guess or fall back to general knowledge.

-   `NSPersistentCloudKitContainer`/CloudKit sync — Deferred
-   Lightweight and mapping-model migration (`NSMigrationManager`,
    versioned/mapping models) — Deferred
-   `NSFetchedResultsController` — Deferred; do not fabricate its behavior
    from `fetching-with-nsfetchrequest`
-   Multi-context concurrency beyond one parent-child relationship — Deferred
-   SwiftData interop or migration (`@Model`, `ModelContainer`,
    `ModelContext`) — owned by `swiftdata`; do not answer SwiftData questions
    from Core Data contracts or fabricate a shared API surface
