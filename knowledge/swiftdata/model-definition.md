# Model Definition

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.swiftdata.model-definition
artifact_type: knowledge
title: Model Definition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines turning a Swift class into a persistent SwiftData model with the @Model macro, customizing individual properties with @Attribute (e.g. .unique) and @Relationship (inverse:), excluding a property from persistence with @Transient, and the auto-synthesized conformances and structural constraints (class, not struct; noncomputed stored properties only) that follow.
domain: SwiftData
tags:
  - swiftdata
  - model
  - attribute
  - relationship
  - transient
references:
  - https://developer.apple.com/documentation/swiftdata/model()
  - https://developer.apple.com/documentation/swiftdata/persistentmodel
  - https://developer.apple.com/documentation/swiftdata/attribute(_:originalname:hashmodifier:)
  - https://developer.apple.com/documentation/swiftdata/relationship(_:deleterule:minimummodelcount:maximummodelcount:originalname:inverse:hashmodifier:)
  - https://developer.apple.com/documentation/swiftdata/transient()
  - https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches
depends_on: []
related:
  - knowledge.swiftdata.relationships-and-cascade-delete
last_updated: 2026-08-06
```

## Intent

This contract governs turning a Swift class into a SwiftData-managed model and customizing individual stored properties on it: applying `@Model`, refining an attribute with `@Attribute`, declaring a relationship's inverse and shape with `@Relationship`, and excluding a property from persistence with `@Transient`. Delete-rule semantics for relationships are governed separately by `relationships-and-cascade-delete`; this contract covers only declaring a relationship property and its `inverse:`.

## Scope

### Included

- Annotating a class with `@Model` to make it persistable
- `@Attribute(_:originalName:hashModifier:)`, most commonly `@Attribute(.unique)`
- `@Relationship(_:deleteRule:minimumModelCount:maximumModelCount:originalName:inverse:hashModifier:)` for declaring to-one/to-many relationship properties and their `inverse:` key path
- `@Transient` for stored properties SwiftData must not persist
- What `@Model` auto-synthesizes, and the structural constraints it implies on the class

### Excluded

- `deleteRule:` semantics (`.cascade`/`.nullify`/`.deny`/`.noAction`) and referential-integrity consequences — see `relationships-and-cascade-delete`
- `ModelContainer`/`ModelConfiguration` setup — see `model-container-setup`
- `#Index`/`#Unique` freestanding macros beyond the basic `@Attribute(.unique)` case — out of scope for v1
- CloudKit sync, schema versioning/migration (`SchemaMigrationPlan`, `VersionedSchema`) — out of scope for v1

## Rules

### Rule 1

Agents MUST apply `@Model` to a `class`, not a `struct` or `enum`, when defining a persistent model. Per Apple's documentation, the macro is declared as `@attached(member, conformances: Observable, PersistentModel, Sendable, ...) macro Model()`, and `PersistentModel` is declared as `protocol PersistentModel : AnyObject, Observable, Hashable, Identifiable, SendableMetatype` — the `AnyObject` requirement means only a reference type (a class) can conform.

### Rule 2

Agents MUST NOT hand-write `Identifiable`, `Hashable`, or `Observable` conformance on a `@Model` class, and MUST NOT assume `Codable` conformance is also synthesized. Per Apple's documentation, `@Model` "converts a Swift class into a stored model that's managed by SwiftData" and "the macro expands to provide conformance to the `PersistentModel` and `Observable` protocols" — `PersistentModel` itself already requires `Hashable` and `Identifiable`, so those are covered, but `Codable` is a separate protocol the macro does not add; agents SHOULD add it explicitly if a model needs to be encoded/decoded.

### Rule 3

Agents SHOULD rely on SwiftData's default per-property behavior and only reach for `@Attribute` when that default is insufficient — most commonly `@Attribute(.unique)` to enforce a uniqueness constraint. Per Apple's documentation, "The framework's default behavior for managing a model class's stored properties is suitable for most use cases. However, if you need to alter the persistence behavior of a particular property, annotate it with the `@Attribute` macro" — e.g., `@Attribute(.unique) var sourceURL: URL`.

### Rule 4

Agents declaring a relationship property MUST supply an `inverse:` key path pointing at the corresponding property on the related model, and MUST NOT declare the same logical relationship independently on both sides without one designating the other as its `inverse`. This is reasoned synthesis: Apple's own relationship example annotates only the owning side, `@Relationship(deleteRule: .cascade, inverse: \Animal.category) var animals = [Animal]()`, against a plain, unannotated `var category: AnimalCategory?` on `Animal` — `inverse:` is what links the two into one relationship SwiftData can maintain, per the documented behavior in `defining-data-relationships-with-enumerations-and-model-classes`.

### Rule 5

Agents MUST provide a default value for any `@Transient` property whose type is not `Optional`, and MUST NOT expect `@Transient` properties to survive a fetch that materializes a fresh instance. Per Apple's documentation, "Unless the type of the annotated property is an optional, the `@Transient` macro requires you to provide a default value. This constraint enables SwiftData to successfully materialize instances of the enclosing model class when running fetches."

## Compliant Example

```swift
import SwiftData

@Model
final class Category {
    @Attribute(.unique) var name: String                       // Rule 3
    @Relationship(deleteRule: .cascade, inverse: \Item.category) // Rule 4
    var items = [Item]()

    init(name: String) { self.name = name }
} // Rule 1: class, not struct

@Model
final class Item {
    var title: String
    var category: Category?          // Rule 4: inverse side, no re-declaration
    @Transient var isSelectedInUI = false // Rule 5: default value provided

    init(title: String) { self.title = title }
}
// Rule 2: no hand-written Identifiable/Hashable/Observable conformance
```

## Non-Compliant Example

```swift
import SwiftData

@Model
struct Category { // violates Rule 1 -- @Model requires a class (AnyObject)
    @Attribute(.unique) var name: String
}

@Model
final class Item: Identifiable, Hashable { // violates Rule 2 -- redundant, already synthesized
    var title: String
    @Relationship(inverse: \Category.items) var category: Category?
    @Relationship var relatedItems = [Item]() // violates Rule 4 -- no inverse, not linked to any other property
    @Transient var cachedThumbnail: Data // violates Rule 5 -- non-optional @Transient with no default value

    init(title: String) { self.title = title }
}
```
Declares `@Model` on a struct (Rule 1), re-declares conformances SwiftData already synthesizes (Rule 2), leaves a relationship without an `inverse:` link (Rule 4), and gives a non-optional `@Transient` property no default value (Rule 5).

## Dependencies

None within this domain — this is the foundational contract every other SwiftData Knowledge Contract assumes when referring to "the model class."

## References

- [Apple Developer — Model()](https://developer.apple.com/documentation/swiftdata/model())
- [Apple Developer — PersistentModel](https://developer.apple.com/documentation/swiftdata/persistentmodel)
- [Apple Developer — Attribute(_:originalName:hashModifier:)](https://developer.apple.com/documentation/swiftdata/attribute(_:originalname:hashmodifier:))
- [Apple Developer — Relationship(...)](https://developer.apple.com/documentation/swiftdata/relationship(_:deleterule:minimummodelcount:maximummodelcount:originalname:inverse:hashmodifier:))
- [Apple Developer — Transient()](https://developer.apple.com/documentation/swiftdata/transient())
- [Apple Developer — Preserving your app's model data across launches](https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches)
