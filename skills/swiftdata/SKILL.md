---
name: swiftdata
description: Route SwiftData implementation tasks to the correct Knowledge Contracts -- declaring persistent model classes with @Model/@Attribute/@Relationship/@Transient, creating and injecting a ModelContainer/ModelConfiguration via .modelContainer, ModelContext CRUD (insert/delete/save/autosave/undo), fetching with @Query or FetchDescriptor+context.fetch(_:), and @Relationship(deleteRule:) referential integrity. Use when writing @Model class RemoteImage { ... }, @Attribute(.unique), @Relationship(deleteRule:inverse:), @Transient, ModelContainer(for:configurations:), ModelConfiguration(isStoredInMemoryOnly:), .modelContainer(for:)/.modelContainer(_:), @Environment(\.modelContext), context.insert(_:)/delete(_:)/save(), context.autosaveEnabled, context.undoManager, @Query(filter:sort:order:), #Predicate, FetchDescriptor<Model>(predicate:sortBy:), context.fetch(_:), or choosing .cascade/.nullify/.deny/.noAction delete rules. v1 is SwiftData only -- no CloudKit sync (ModelConfiguration(cloudKitDatabase:)), no SchemaMigrationPlan/VersionedSchema migration, no Core Data interop (NSManagedObjectContext/NSFetchRequest are a separate domain), no #Index/#Unique macros beyond basic @Attribute(.unique), and no widget-extension/App-Group container sharing specifics. Triggers on SwiftData, @Model, @Attribute, @Relationship, @Transient, ModelContainer, ModelConfiguration, ModelContext, modelContainer, modelContext, @Query, FetchDescriptor, #Predicate, deleteRule, cascade delete.
id: skill.swiftdata.foundations
title: SwiftData — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: SwiftData
routes: [knowledge.swiftdata.model-definition, knowledge.swiftdata.model-container-setup, knowledge.swiftdata.model-context-crud, knowledge.swiftdata.querying-with-query-and-fetchdescriptor, knowledge.swiftdata.relationships-and-cascade-delete]
related: []
last_updated: 2026-08-08
---

# SwiftData — Foundations Skill

## Purpose

Route SwiftData implementation tasks to the minimum required SwiftData
Knowledge Contracts. v1 scope is declaring `@Model` classes and their
attributes/relationships, setting up and injecting a `ModelContainer`,
performing CRUD through a `ModelContext`, fetching with `@Query` or
`FetchDescriptor`, and delete-rule/referential-integrity behavior on
relationships -- not CloudKit sync, not schema migration, not Core Data
interop, and not the `#Index`/`#Unique` macros beyond a basic mention.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/swiftdata/.

-   Annotating a class with `@Model`; customizing a property with `@Attribute` (e.g. `.unique`) or `@Transient`; declaring a `@Relationship` property and its `inverse:`; or asking what SwiftData auto-synthesizes (`Identifiable`/`Hashable`/`Observable`, not `Codable`) -> model-definition.md
-   Setting up `.modelContainer(for:)`/`.modelContainer(_:)`; configuring `ModelConfiguration` (`isStoredInMemoryOnly`, `allowsSave`); creating a `ModelContainer(for:configurations:)` manually for previews/tests/non-SwiftUI code; or wiring `@Environment(\.modelContext)` -> model-container-setup.md
-   Calling `context.insert(_:)`/`delete(_:)`/`save()`; deciding whether `autosaveEnabled` makes an explicit `save()` unnecessary; choosing `mainContext` vs. a manually created secondary `ModelContext`; or enabling undo via `context.undoManager` -> model-context-crud.md
-   Fetching with `@Query` (`filter:`/`sort:`/`order:`/`animation:`) in a SwiftUI view; building a `#Predicate`; or fetching outside a view with `FetchDescriptor<Model>` + `context.fetch(_:)` -> querying-with-query-and-fetchdescriptor.md
-   Choosing a `@Relationship(deleteRule:)` value (`.cascade`/`.nullify`/`.deny`/`.noAction`); reasoning about what happens to related models on delete; or diagnosing a one-directional relationship missing its `inverse:` -> relationships-and-cascade-delete.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/swiftdata/ — do not guess or fall back to general
knowledge. CloudKit sync integration (`ModelConfiguration(cloudKitDatabase:)`)
is out of scope entirely -- not built as a contract here. Schema migration
(`SchemaMigrationPlan`, `VersionedSchema`, lightweight vs. custom migration)
is out of scope entirely -- not yet built. Core Data interop or migration
(`NSManagedObjectContext`, `NSFetchRequest`) belongs to a separate Core
Data domain, not this one -- do not answer Core Data questions from
SwiftData contracts or fabricate a shared API surface. The `#Index`/
`#Unique` freestanding macros beyond the basic `@Attribute(.unique)` case,
and SwiftData in widget extensions or App Group container sharing, are
out of scope entirely -- report the boundary rather than fabricate
behavior.
