# Relationships and Delete Rules

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.core-data.relationships-and-delete-rules
artifact_type: knowledge
title: Relationships and Delete Rules
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines NSDeleteRule's four cases -- cascadeDeleteRule, nullifyDeleteRule (default), denyDeleteRule, noActionDeleteRule -- what each does when the owning managed object is deleted, the requirement that every relationship have an inverse, and how relationships are configured in the .xcdatamodeld model editor or programmatically via NSRelationshipDescription.
domain: Core Data
tags:
  - core-data
  - nsdeleterule
  - nsrelationshipdescription
  - inverse-relationship
  - referential-integrity
references:
  - https://developer.apple.com/documentation/coredata/nsdeleterule
  - https://developer.apple.com/documentation/coredata/nsrelationshipdescription
  - https://developer.apple.com/documentation/coredata/nsrelationshipdescription/deleterule
  - https://developer.apple.com/documentation/coredata/nsrelationshipdescription/inverserelationship
  - https://developer.apple.com/documentation/coredata/configuring-relationships
depends_on:
  - knowledge.core-data.model-definition
related:
  - knowledge.core-data.managed-object-context-crud
last_updated: 2026-08-06
```

## Intent

This contract governs `NSDeleteRule` and the inverse-relationship requirement for relationships declared per `model-definition`: what each of the four delete rules does to related objects when the owning object is deleted from an `NSManagedObjectContext` (`managed-object-context-crud`), and how a relationship's delete rule and inverse are configured — in the `.xcdatamodeld` model editor, or programmatically via `NSRelationshipDescription`.

## Scope

### Included

- The four `NSDeleteRule` cases: `.cascadeDeleteRule`, `.nullifyDeleteRule` (default), `.denyDeleteRule`, `.noActionDeleteRule`
- What each rule does to related objects when the owning object is deleted via `context.delete(_:)`
- The requirement that every relationship have an inverse relationship on the destination entity
- Configuring a relationship's delete rule and inverse in the model editor's graph/table style, or programmatically via `NSRelationshipDescription.deleteRule`/`inverseRelationship`

### Excluded

- Declaring the relationship as an `@NSManaged` property on the class — see `model-definition`
- `delete(_:)`/`save()` mechanics on `NSManagedObjectContext` — see `managed-object-context-crud`
- Migration of relationship shape changes across model versions — out of scope for v1

## Rules

### Rule 1

Agents choosing the Cascade delete rule (`.cascadeDeleteRule` in code; "Cascade" in the model editor) MUST expect every related object reachable through that relationship to be deleted along with the owning object. Per Apple's documentation, `NSDeleteRule.cascadeDeleteRule` is "A rule that deletes the referenced managed objects," and the model editor's own guidance frames it from the owning ("source") side: "Select Cascade to delete the source object instance, and with it, all of the destination object instances."

### Rule 2

Agents relying on the default delete rule MUST know it is Nullify (`.nullifyDeleteRule` in code), not Cascade or Deny, and MUST expect related objects to survive with their reference to the deleted object cleared rather than being deleted themselves. Per Apple's documentation, `NSRelationshipDescription.deleteRule`'s "default value is `nullifyDeleteRule`," and `NSDeleteRule.nullifyDeleteRule` is "A rule that nullifies the inverse relationship of the referenced managed objects."

### Rule 3

Agents choosing Deny (`.denyDeleteRule`) MUST handle the resulting failure at delete/save time rather than assuming the delete always succeeds. Per Apple's documentation, `denyDeleteRule` "prevents the deletion of the owning managed object if the relationship has references to other objects" — agents SHOULD use this when related data must be explicitly reassigned or removed before the owning object can be deleted at all.

### Rule 4

Agents choosing No Action (`.noActionDeleteRule`) MUST manually delete or nullify the related objects themselves elsewhere, and MUST NOT treat it as equivalent to Nullify. Per Apple's documentation, `noActionDeleteRule` is "A rule that prevents modification of the referenced managed objects," and Apple explicitly warns: "If you use this delete rule, make sure you delete any referenced managed objects or nullify their inverse relationships. Otherwise, those objects will reference an object that doesn't exist, and your persistent store will be in an inconsistent state."

### Rule 5

Agents configuring a relationship — in the `.xcdatamodeld` graph/table editor or programmatically via `NSRelationshipDescription` — MUST give it an inverse relationship on the destination entity, and MUST NOT leave a relationship one-directional. Per Apple's documentation, "You must also configure every relationship with an inverse relationship," and programmatically this is the `inverseRelationship` property: "The inverse relationship is the description of the current relationship from the destination entity's perspective." Control-dragging between two entities in the graph editor creates both sides of the pair in one step; in the table editor, each side must be configured individually.

## Compliant Example

```swift
// In the .xcdatamodeld graph editor, control-drag between Department and Employee to
// create both sides of the relationship at once, then set each side's delete rule
// and inverse in the Data Model inspector (Rule 5).
// Department.employees -> destination Employee, delete rule: Cascade      (Rule 1)
// Employee.department   -> destination Department, delete rule: Nullify   (Rule 2, default)

extension Department {
    @NSManaged public var employees: NSSet? // to-many, Cascade
}

extension Employee {
    @NSManaged public var department: Department? // to-one, inverse of `employees`
}

// Deleting a Department cascades and deletes every Employee referencing it (Rule 1).
// Employee.department defaults to Nullify (Rule 2): deleting a single Employee only
// clears that Employee's slot out of the Department's `employees` set.

// The same pair configured programmatically, e.g. when building an NSManagedObjectModel
// in code, mirrors the same rules and the required inverse link (Rule 5):
let employees = NSRelationshipDescription()
employees.name = "employees"
employees.destinationEntity = employeeEntity
employees.deleteRule = .cascadeDeleteRule // Rule 1

let department = NSRelationshipDescription()
department.name = "department"
department.destinationEntity = departmentEntity
department.deleteRule = .nullifyDeleteRule // Rule 2 (also the default)

employees.inverseRelationship = department // Rule 5
department.inverseRelationship = employees // Rule 5
```

## Non-Compliant Example

```swift
// No inverse configured anywhere -- violates Rule 5.
let employees = NSRelationshipDescription()
employees.name = "employees"
employees.destinationEntity = employeeEntity
employees.deleteRule = .noActionDeleteRule // Rule 4 risk: no cleanup plan exists
// employees.inverseRelationship is never set.

extension Employee {
    @NSManaged public var department: Department?
    // Nothing in the app ever nullifies or deletes `department` after a Department is
    // deleted with No Action -- violates Rule 4's explicit warning about an inconsistent
    // store, and this relationship has no configured inverse back to `employees` --
    // violates Rule 5.
}
```
Declares a relationship with no `inverseRelationship` linking the two sides (Rule 5), and pairs `.noActionDeleteRule` with no code that cleans up the dangling reference afterward, exactly the inconsistent-store risk Apple's documentation warns `noActionDeleteRule` can produce (Rule 4).

## Dependencies

Depends on `model-definition` for the managed object properties this contract's `deleteRule` values and inverse requirement apply to.

## References

- [Apple Developer — NSDeleteRule](https://developer.apple.com/documentation/coredata/nsdeleterule)
- [Apple Developer — NSRelationshipDescription](https://developer.apple.com/documentation/coredata/nsrelationshipdescription)
- [Apple Developer — deleteRule](https://developer.apple.com/documentation/coredata/nsrelationshipdescription/deleterule)
- [Apple Developer — inverseRelationship](https://developer.apple.com/documentation/coredata/nsrelationshipdescription/inverserelationship)
- [Apple Developer — Configuring Relationships](https://developer.apple.com/documentation/coredata/configuring-relationships)
