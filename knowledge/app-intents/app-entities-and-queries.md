# App Entities and Queries

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-intents.app-entities-and-queries
artifact_type: knowledge
title: App Entities and Queries
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines AppEntity protocol conformance, EntityQuery/EntityStringQuery for locating entities by identifier or string, DisplayRepresentation, defaultQuery wiring, and system-driven disambiguation when a query resolves to multiple matches.
domain: App Intents
tags:
  - app-intents
  - appentity
  - entityquery
  - entitystringquery
  - displayrepresentation
references:
  - https://developer.apple.com/documentation/appintents/defining-app-entities-for-your-custom-data-types
  - https://developer.apple.com/documentation/appintents/appentity
  - https://developer.apple.com/documentation/appintents/entityquery
  - https://developer.apple.com/documentation/appintents/entitystringquery
  - https://developer.apple.com/documentation/appintents/displayrepresentation
depends_on:
  - knowledge.app-intents.app-intent-declaration-and-parameters
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent exposes app data to the system as an `AppEntity`, gives that entity a query type conforming to `EntityQuery` (or `EntityStringQuery` for free-text search) assigned to `defaultQuery`, describes it with `DisplayRepresentation`, and understands what happens when that query resolves to more than one match — an entity used as an `@Parameter` type in a KC1 intent.

## Scope

### Included

-   `AppEntity` protocol conformance: a stable `id`, `@Property`-wrapped data variables, `displayRepresentation`, `static var defaultQuery`
-   `EntityQuery` for identifier-based lookup (`entities(for:)`) and `EntityStringQuery` for string-based search (`entities(matching:)`)
-   `DisplayRepresentation` (title/subtitle/image) for how an entity reads in dialog and on-screen
-   Suggested results via `suggestedEntities()`, and disambiguation when a query returns multiple matches for a parameter

### Excluded

-   Declaring the `AppIntent`/`@Parameter` that consumes the entity — see `app-intent-declaration-and-parameters`
-   `AppShortcut`/`AppShortcutsProvider` — see `app-shortcuts-and-siri-phrases`
-   Spotlight indexing of entities (`IndexedEntity`, `CSSearchableItem`) — out of scope for v1
-   Property-matched queries (`EntityPropertyQuery`) and sort options beyond the identifier/string basics

## Rules

### Rule 1

Agents MUST conform a custom data type to `AppEntity` (`protocol AppEntity : AppValue, DisplayRepresentable, Identifiable where Self == Self.ValueType, Self.ID : EntityIdentifierConvertible, Self.ID : Sendable`) rather than exposing a plain struct as an intent parameter, and MUST give it a stable `id` property, typed as `String`, `Int`, or `UUID` whenever possible. Per Apple's documentation, "an app entity is a type that adopts the `AppEntity` protocol and reflects a portion of your app's data," and "a requirement for all app entities is that they provide a unique identifier to distinguish one instance from another... Set the type of this property to `String`, `Int`, or `UUID` type whenever possible. The App Intents framework contains built-in support for identifying entities using these types."

### Rule 2

Agents MUST provide a query type conforming to `EntityQuery` and assign an instance of it to `static var defaultQuery` on the entity, implementing at minimum `func entities(for identifiers: [Self.Entity.ID]) async throws -> [Self.Entity]`; agents MUST use `EntityStringQuery` (`protocol EntityStringQuery : EntityQuery`, adding `func entities(matching string: String) async throws -> Self.Result`) instead when the entity also needs free-text search. Per Apple's documentation, "to help the system find your app's entities, provide a query type for each entity type you define... The minimal implementation of this protocol requires you to locate or create an entity using only its unique identifier. Use additional protocols to support text- or property-based searches of your entities." Agents MUST NOT leave `defaultQuery` unset — without it, the system has no way to resolve the entity from an identifier or a spoken/typed value.

### Rule 3

Agents MUST implement `var displayRepresentation: DisplayRepresentation { get }` on every `AppEntity` and MUST include enough information (at minimum a `title`) for the system to speak or show the entity in a dialog. Per Apple's documentation, `DisplayRepresentation` "provides the displayable version of your entity, and offers a title, subtitle, and image the system can incorporate into dialogs" — during a Siri conversation "the system might describe the contents of the entity verbally to someone," and it can only do so from what `displayRepresentation` supplies.

### Rule 4

Agents MUST implement `func suggestedEntities() async throws -> Self.Result` on the query when the parameter benefits from an initial, pre-filtered list rather than an empty picker, and agents MUST NOT assume they need to build their own disambiguation UI when a query legitimately returns more than one entity for a request — the system presents the returned set as a picker using each entity's `displayRepresentation` and lets the person choose. Per Apple's documentation, `suggestedEntities()` "returns the initial results to display when the system presents options backed by this query," and system features like Siri "use your queries to try and resolve conversational requests automatically" — disambiguation among multiple query results is the system's responsibility once the query and `displayRepresentation` are correctly implemented, not something the intent's `perform()` needs to handle itself.

## Compliant Example

```swift
struct TrailEntity: AppEntity {
    var id: Trail.ID
    var currentConditions: String

    @Property(title: "Name")
    var name: String

    @Property(title: "Region")
    var regionDescription: String

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(name)", subtitle: "\(regionDescription)")
    }

    static let defaultQuery = TrailEntityQuery()

    init(trail: Trail) {
        self.id = trail.id
        self.currentConditions = trail.currentConditions
        self.name = trail.name
        self.regionDescription = trail.regionDescription
    }
}

struct TrailEntityQuery: EntityQuery {
    @Dependency
    var trailManager: TrailDataManager

    func entities(for identifiers: [TrailEntity.ID]) async throws -> [TrailEntity] {
        trailManager.trails(with: identifiers).map { TrailEntity(trail: $0) }
    }

    func suggestedEntities() async throws -> [TrailEntity] {
        trailManager.nearbyTrails().map { TrailEntity(trail: $0) }
    }
}
```
`TrailEntity` conforms to `AppEntity` with a stable `id` (Rule 1), assigns a query to `defaultQuery` implementing `entities(for:)` (Rule 2), implements `displayRepresentation` with a title and subtitle (Rule 3), and the query implements `suggestedEntities()` for an initial pre-filtered list, leaving multi-match disambiguation to the system (Rule 4). (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
struct TrailEntity: AppEntity {
    var id: String
    var name: String
    var regionDescription: String

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "Trail") // No per-instance detail -- every trail reads identically.
    }

    // No defaultQuery -- the system has no way to resolve this entity from an identifier or search term.

    func findMatchingTrails(named: String) -> [TrailEntity] { [] } // Hand-rolled search the framework can't call.
}
```
Omits `defaultQuery` entirely instead of providing an `EntityQuery`/`EntityStringQuery` (Rule 2), gives every instance the same static `displayRepresentation` title instead of interpolating the entity's own data (Rule 3), and adds an ad hoc search method instead of `entities(matching:)` that the framework can actually invoke (Rule 2).

## Dependencies

-   `knowledge.app-intents.app-intent-declaration-and-parameters` — an `AppEntity` is typically declared so it can be used as an `@Parameter` type on an `AppIntent`; this contract does not redefine parameter declaration itself.

## References

-   [Apple Developer — Defining app entities for your custom data types](https://developer.apple.com/documentation/appintents/defining-app-entities-for-your-custom-data-types)
-   [Apple Developer — AppEntity](https://developer.apple.com/documentation/appintents/appentity)
-   [Apple Developer — EntityQuery](https://developer.apple.com/documentation/appintents/entityquery)
-   [Apple Developer — EntityStringQuery](https://developer.apple.com/documentation/appintents/entitystringquery)
-   [Apple Developer — DisplayRepresentation](https://developer.apple.com/documentation/appintents/displayrepresentation)
