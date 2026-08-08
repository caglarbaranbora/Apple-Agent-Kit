# Relationships and Cascade Delete

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.swiftdata.relationships-and-cascade-delete
artifact_type: knowledge
title: Relationships and Cascade Delete
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines @Relationship(deleteRule:) semantics -- .cascade, .nullify (default), .deny, .noAction -- what each does when the owning object is deleted, the inverse-relationship requirement for SwiftData to maintain referential integrity, and the common mistake of declaring a relationship on only one side without linking it as the other's inverse.
domain: SwiftData
tags:
  - swiftdata
  - relationship
  - deleterule
  - cascade
  - referential-integrity
references:
  - https://developer.apple.com/documentation/swiftdata/relationship(_:deleterule:minimummodelcount:maximummodelcount:originalname:inverse:hashmodifier:)
  - https://developer.apple.com/documentation/swiftdata/schema/relationship/deleterule-swift.enum
  - https://developer.apple.com/documentation/swiftdata/defining-data-relationships-with-enumerations-and-model-classes
  - https://developer.apple.com/documentation/swiftdata/deleting-persistent-data-from-your-app
depends_on:
  - knowledge.swiftdata.model-definition
related:
  - knowledge.swiftdata.model-context-crud
last_updated: 2026-08-08
```

## Intent

This contract governs `@Relationship`'s `deleteRule:` parameter and the inverse-relationship requirement introduced in `model-definition`: what each of the four delete rules does to related models when the owning model is deleted from a `ModelContext` (`model-context-crud`), and why a relationship declared on only one side, without an `inverse:` link, is a common and dangerous mistake.

## Scope

### Included

- The four `Schema.Relationship.DeleteRule` cases: `.cascade`, `.nullify` (default), `.deny`, `.noAction`
- What each rule does to related model instances when the owning instance is deleted via `context.delete(_:)`
- Why `inverse:` is required for SwiftData to treat two declared properties as one relationship rather than two independent ones
- The common mistake of declaring `@Relationship` on both sides (or neither side) instead of one owning side with `inverse:`

### Excluded

- Declaring the relationship property itself (`@Relationship(inverse:)` syntax, to-one vs. to-many shape) — see `model-definition`
- `insert(_:)`/`delete(_:)`/`save()` mechanics on `ModelContext` — see `model-context-crud`
- Schema versioning/migration of relationship shape changes — out of scope for v1

## Rules

### Rule 1

Agents choosing `.cascade` MUST expect every related model to be deleted along with the owning model, with no further cleanup required. Per Apple's documentation, `Schema.Relationship.DeleteRule.cascade` is "A rule that deletes any related models" — e.g., deleting an `AnimalCategory` whose `animals` relationship uses `.cascade` also deletes every `Animal` in that category.

### Rule 2

Agents relying on the default delete rule MUST know it is `.nullify`, not `.cascade` or `.deny`, and MUST expect related models to survive with their reference to the deleted model cleared rather than being deleted themselves. Per Apple's documentation, `Schema.Relationship.DeleteRule.nullify` is "A rule that nullifies the related model's reference to the deleted model," and the `deleteRule` parameter's "default value is `nullify`" — so `@Relationship(inverse: \Animal.category) var animals = [Animal]()`, with no explicit `deleteRule`, sets each animal's `category` to `nil` when its category is deleted rather than deleting the animal.

### Rule 3

Agents choosing `.deny` MUST handle the resulting failure at delete time rather than assuming the delete always succeeds. Per Apple's documentation, `Schema.Relationship.DeleteRule.deny` is "A rule that prevents the deletion of a model because it contains one or more references to other models" — agents SHOULD use this when related data must be explicitly reassigned or removed by the app before the owning model can be deleted at all.

### Rule 4

Agents choosing `.noAction` MUST manually delete or nullify the related models themselves elsewhere, and MUST NOT treat `.noAction` as equivalent to `.nullify`. Per Apple's documentation, `Schema.Relationship.DeleteRule.noAction` is "A rule that doesn't make changes to any related models," and Apple explicitly warns: "Ensure that you take the appropriate action on any related models when using this delete rule, such as deleting them or nullifying their references to the deleted model. Otherwise, your data will be in an inconsistent state and may reference models that don't exist."

### Rule 5

Agents declaring a two-model relationship MUST designate exactly one side as the owner with `@Relationship(inverse:)` pointing at a plain (or independently-annotated) property on the other model, and MUST NOT declare the relationship on both sides with no `inverse:` linking them, nor on neither side. This is reasoned synthesis built on the documented pattern in `defining-data-relationships-with-enumerations-and-model-classes`, where only `AnimalCategory.animals` carries `@Relationship(deleteRule:inverse:)` and `Animal.category` is left as a plain `var category: AnimalCategory?` — `inverse:` is the only documented mechanism that tells SwiftData two properties describe one bidirectional relationship rather than two unrelated ones, which matters directly for which side's `deleteRule` (Rules 1-4) actually governs the delete.

## Compliant Example

```swift
import SwiftData

@Model
final class AnimalCategory {
    @Attribute(.unique) var name: String
    @Relationship(deleteRule: .cascade, inverse: \Animal.category) // Rule 1, Rule 5
    var animals = [Animal]()

    init(name: String) { self.name = name }
}

@Model
final class Animal {
    var name: String
    var category: AnimalCategory? // Rule 5: inverse side, no separate @Relationship needed

    init(name: String) { self.name = name }
}

// Deleting a category cascades and removes every Animal referencing it (Rule 1).
// If deleteRule had been omitted, the default .nullify would instead set
// each animal's `category` to nil (Rule 2) rather than deleting them.
```

## Non-Compliant Example

```swift
import SwiftData

@Model
final class AnimalCategory {
    @Attribute(.unique) var name: String
    @Relationship(deleteRule: .noAction) var animals = [Animal]() // Rule 4 risk: no inverse cleanup planned
    // No `inverse:` argument at all -- violates Rule 5.

    init(name: String) { self.name = name }
}

@Model
final class Animal {
    var name: String
    @Relationship var category: AnimalCategory? // Also independently annotated, still with no inverse -- violates Rule 5
    // Nothing in the app ever nullifies or deletes `category` after a category is
    // deleted with .noAction -- violates Rule 4's explicit warning.

    init(name: String) { self.name = name }
}
```
Declares `@Relationship` on both sides with no `inverse:` linking them into one relationship (Rule 5), and pairs `.noAction` with no code that cleans up the dangling reference afterward, exactly the inconsistent state Apple's documentation warns `.noAction` can produce (Rule 4).

## Dependencies

Depends on `model-definition` for the `@Relationship` property declarations this contract's `deleteRule:` values and inverse requirement apply to.

## References

- [Apple Developer — Relationship(...)](https://developer.apple.com/documentation/swiftdata/relationship(_:deleterule:minimummodelcount:maximummodelcount:originalname:inverse:hashmodifier:))
- [Apple Developer — Schema.Relationship.DeleteRule](https://developer.apple.com/documentation/swiftdata/schema/relationship/deleterule-swift.enum)
- [Apple Developer — Defining data relationships with enumerations and model classes](https://developer.apple.com/documentation/swiftdata/defining-data-relationships-with-enumerations-and-model-classes)
- [Apple Developer — Deleting persistent data from your app](https://developer.apple.com/documentation/swiftdata/deleting-persistent-data-from-your-app)
