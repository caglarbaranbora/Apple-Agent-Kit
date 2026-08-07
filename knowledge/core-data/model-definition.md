# Model Definition

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.core-data.model-definition
artifact_type: knowledge
title: Model Definition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines subclassing NSManagedObject for a Core Data entity, the three .xcdatamodeld Codegen modes (Class Definition / Manual/None / Category+Extension) and when to use each, and declaring persisted attributes/relationships with @NSManaged rather than ordinary stored properties.
domain: Core Data
tags:
  - core-data
  - nsmanagedobject
  - codegen
  - nsmanaged
  - nsentitydescription
references:
  - https://developer.apple.com/documentation/coredata/nsmanagedobject
  - https://developer.apple.com/documentation/coredata/nsentitydescription
  - https://developer.apple.com/documentation/coredata/generating-code
depends_on: []
related:
  - knowledge.core-data.relationships-and-delete-rules
last_updated: 2026-08-06
```

## Intent

This contract governs turning a Core Data entity into a usable Swift type: the `.xcdatamodeld` model editor's Codegen setting (Class Definition / Category+Extension / Manual/None) and what each mode generates or expects the agent to maintain, plus declaring an entity's persisted attributes and relationships with `@NSManaged`. Delete-rule and inverse-relationship semantics are governed separately by `relationships-and-delete-rules`; this contract covers only the class/property-declaration layer.

## Scope

### Included

- Entities in the `.xcdatamodeld` model editor mapping to `NSManagedObject` subclasses, backed at runtime by `NSEntityDescription`
- The three Codegen modes: Class Definition, Category/Extension, Manual/None, and when to choose each
- `@NSManaged` property declarations for attributes and relationships
- What Xcode's generated code does and does not synthesize (e.g. `Identifiable`, not `Codable`/`Hashable`)

### Excluded

- `NSPersistentContainer`/store setup — see `persistent-container-setup`
- Inserting, deleting, or saving instances — see `managed-object-context-crud`
- `NSDeleteRule` and inverse-relationship configuration — see `relationships-and-delete-rules`
- `NSFetchRequest`/fetching — see `fetching-with-nsfetchrequest`

## Rules

### Rule 1

Agents defining a Core Data entity MUST create or edit it in the `.xcdatamodeld` model editor (or, for a programmatically built model, via `NSEntityDescription`), and MUST NOT expect a hand-written `NSManagedObject` subclass alone to define an entity's schema. Per Apple's documentation, entities are "to managed objects what `Class` is to `id`," and "as a minimum, an entity description requires: A name. The class name of the corresponding managed object."

### Rule 2

Agents choosing a Codegen mode MUST select "Class Definition" when no custom logic on the class is needed, since Xcode regenerates both the class file and the properties file automatically as part of the build and "these files regenerate whenever the related entity changes in the data model." Agents needing custom methods or business logic on the class MUST choose "Category/Extension" instead, which generates only the properties file and leaves the class file for the agent to create once (Editor > Create NSManagedObject Subclass) and maintain manually thereafter.

### Rule 3

Agents choosing "Manual/None" MUST create and maintain both the class file and the properties file themselves, including every `@NSManaged` declaration, since with this option "Core Data doesn't generate any files to support your managed object. You create and maintain your class, including its properties, manually." Agents SHOULD reserve Manual/None for cases needing full control (e.g. altered access modifiers) beyond what Category/Extension's class/properties split already allows.

### Rule 4

Agents declaring a persisted attribute or relationship property on a Category/Extension or Manual/None managed object subclass MUST mark it `@NSManaged`, not an ordinary stored property with a default value, because Core Data supplies that property's storage and accessor implementation at runtime rather than through normal Swift storage. Apple's own generated properties file demonstrates this directly: `@NSManaged public var name: String?` and `@NSManaged public var shoppingItems: NSSet?`.

### Rule 5

Agents MUST NOT assume `Codable` or `Hashable` conformance is synthesized for an `NSManagedObject` subclass the way SwiftData's `@Model` macro synthesizes protocol conformances. Apple's own Class Definition/Category+Extension code sample adds only `extension Store: Identifiable {}` automatically — no other conformance appears in that generated output — so agents needing `Codable` or `Hashable` must add those conformances explicitly.

## Compliant Example

```swift
// Codegen: Category/Extension (Rule 2) -- class file is hand-maintained for custom logic.
import CoreData

@objc(Task)
public class Task: NSManagedObject {
    func markComplete() { // Rule 2: custom logic is why Category/Extension was chosen
        isComplete = true
        completedAt = Date()
    }
}

// Task+CoreDataProperties.swift -- regenerated automatically by Xcode's build process.
extension Task {
    @nonobjc public class func fetchRequest() -> NSFetchRequest<Task> {
        NSFetchRequest<Task>(entityName: "Task")
    }

    @NSManaged public var title: String?         // Rule 4: @NSManaged, not a stored property
    @NSManaged public var isComplete: Bool
    @NSManaged public var completedAt: Date?
}

extension Task: Identifiable {} // Rule 5: the one conformance Xcode adds automatically
```

## Non-Compliant Example

```swift
import CoreData

// Codegen set to Manual/None, but the properties file was never created/maintained -- violates Rule 3.
@objc(Task)
public class Task: NSManagedObject {
    var title: String = ""       // violates Rule 4 -- ordinary stored property, not @NSManaged
    var isComplete: Bool = false // Core Data has no storage/accessor for this at runtime
    // No .xcdatamodeld entity backs these properties at all -- violates Rule 1.
}

extension Task: Codable {} // violates Rule 5 -- assumes a conformance Core Data never synthesizes
```
Declares Manual/None codegen without maintaining the required properties file (Rule 3), uses ordinary stored properties instead of `@NSManaged` (Rule 4), defines a class with no backing entity description (Rule 1), and assumes a `Codable` conformance Core Data does not synthesize (Rule 5).

## Dependencies

None within this domain — this is the foundational contract every other Core Data Knowledge Contract assumes when referring to "the managed object subclass."

## References

- [Apple Developer — NSManagedObject](https://developer.apple.com/documentation/coredata/nsmanagedobject)
- [Apple Developer — NSEntityDescription](https://developer.apple.com/documentation/coredata/nsentitydescription)
- [Apple Developer — Generating code](https://developer.apple.com/documentation/coredata/generating-code)
