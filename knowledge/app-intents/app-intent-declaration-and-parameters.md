# App Intent Declaration and Parameters

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-intents.app-intent-declaration-and-parameters
type: knowledge
title: App Intent Declaration and Parameters
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines AppIntent protocol conformance (title, description, perform()), declaring inputs with the @Parameter property wrapper (IntentParameter), AppEnum-conforming custom enums, and parameterSummary for the Shortcuts-app editor.
domain: App Intents
tags:
  - app-intents
  - appintent
  - parameter
  - appenum
  - parametersummary
references:
  - https://developer.apple.com/documentation/appintents/appintent
  - https://developer.apple.com/documentation/appintents/adding-parameters-to-an-app-intent
  - https://developer.apple.com/documentation/appintents/intentparameter
  - https://developer.apple.com/documentation/appintents/appenum
  - https://developer.apple.com/documentation/appintents/parametersummary
depends_on: []
related: []
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent declares an app-specific action: conforming to `AppIntent` with `title`/`description`/`perform()`, declaring its inputs with the `@Parameter` property wrapper, restricting a parameter to a closed set of values with an `AppEnum`-conforming custom enum, and describing the intent's parameters to the Shortcuts-app editor via `parameterSummary`.

## Scope

### Included

-   `AppIntent` protocol conformance: `static var title: LocalizedStringResource`, `static var description: IntentDescription?`, `func perform() async throws -> Self.PerformResult`
-   The `@Parameter` property wrapper (documented under the symbol name `IntentParameter`) for declaring required and optional inputs
-   `AppEnum`-conforming custom enums for closed, discoverable sets of parameter values
-   `static var parameterSummary: Self.SummaryContent` and the `ParameterSummary` result builder (`Summary`, `Switch`, `Case`, `When`)

### Excluded

-   `AppEntity`/`EntityQuery` — see `app-entities-and-queries`
-   `AppShortcutsProvider`/`AppShortcut` — see `app-shortcuts-and-siri-phrases`
-   `IntentResult` variants (`ReturnsValue`, `ProvidesDialog`, `OpensIntent`) — see `intent-results-and-widget-hookup`
-   Legacy `SiriKit` donation-based intents (`INIntent`, `NSUserActivity` donation) — superseded by App Intents, not planned as a separate domain
-   Wiring an already-authored intent into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)` — that is `widgetkit`'s territory (`knowledge.widgetkit.widget-interactivity-and-deep-links`)

## Rules

### Rule 1

Agents MUST conform to `AppIntent` (`protocol AppIntent : PersistentlyIdentifiable, _SupportsAppDependencies, Sendable`) and implement `static var title: LocalizedStringResource` and `func perform() async throws -> Self.PerformResult`. Per Apple's documentation, `title` is "A short, localized, human-readable string that conveys the app intent's action," and each app intent needs "the following minimum set of behaviors: It performs an action in its `perform()` method... It declares any required or optional parameters it needs to perform the action. It provides a localized title and other descriptive information that Siri, the Shortcuts app, and other system features can display." Agents SHOULD also implement `static var description: IntentDescription?` — Apple's documentation defines it as "A localized string that describes what the app intent does."

### Rule 2

Agents MUST declare an intent's inputs by decorating a stored property with the `@Parameter` property wrapper, and MUST use a non-optional property type for a required parameter versus an `Optional` type for one the system may leave unset. Per Apple's documentation (`IntentParameter`, the symbol backing `@Parameter`), "When you implement an `AppIntent` type, declare its parameters using the `@Parameter` property wrapper," and "If you define a variable as a non-optional type, the system knows the parameter is required and, when necessary, requests a value. Conversely, if you define a variable as an optional type, the system assumes the parameter is optional and doesn't request a value." For an optional parameter the intent still needs, agents MUST use the wrapper's projected value to request one: `throw $date.requestValue("What date would you like to use?")`.

### Rule 3

Agents MUST restrict a parameter to a closed, known set of values by giving it a type that conforms to `AppEnum` (`protocol AppEnum : AppValue, StaticDisplayRepresentable, RawRepresentable where Self.RawValue : LosslessStringConvertible`), and MUST NOT model such a value as a bare `String`/`Int` when the framework can present it as a picker. Per Apple's documentation, "when defining an app enum, make sure your type adheres to the following rules: The type inherits from the `AppEnum` type. Its storage type is `RawRepresentable`... The type also conforms to the `CaseDisplayRepresentable` protocol" — agents MUST supply case-level display strings, not just raw values, so the system can present each option.

### Rule 4

Agents MUST implement `static var parameterSummary: some ParameterSummary` whenever the intent declares one or more parameters, using the `Summary(_:)` result builder with key-path interpolation (e.g. `Summary("Get information on \(\.$trail)")`), and MUST use `Switch`/`Case`/`When`/`DefaultCase` rather than free-form string concatenation when the summary needs to vary by an already-chosen value. Per Apple's documentation, "a parameter summary is a visual, textual outline of your app intent that the Shortcuts app displays in the shortcut editor... Write the content using localized natural language and, where applicable, substitute words that represent parameters with the key paths to those parameters," and "the shortcut editor substitutes each key path with the corresponding parameter's title and enables a person to set the value by tapping it."

## Compliant Example

```swift
enum TrailDifficulty: String, AppEnum {
    case easy, moderate, difficult

    static var caseDisplayRepresentations: [TrailDifficulty: DisplayRepresentation] = [
        .easy: "Easy", .moderate: "Moderate", .difficult: "Difficult"
    ]
}

struct GetTrailInfo: AppIntent {
    static var title: LocalizedStringResource = "Get Trail Info"
    static var description: IntentDescription? = IntentDescription("Shows the current conditions for a trail.")

    @Parameter(title: "Trail", description: "The trail to get information on.")
    var trail: TrailEntity

    @Parameter(title: "Minimum Difficulty")
    var minimumDifficulty: TrailDifficulty?

    static var parameterSummary: some ParameterSummary {
        Summary("Get information on \(\.$trail)")
    }

    func perform() async throws -> some IntentResult {
        return .result()
    }
}
```
Conforms to `AppIntent` with `title`, `description`, and `perform()` (Rule 1), declares `trail` (required) and `minimumDifficulty` (optional) with `@Parameter` (Rule 2), restricts difficulty to a closed set via an `AppEnum` with case display representations (Rule 3), and provides a key-path-interpolated `parameterSummary` (Rule 4). (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
struct GetTrailInfo: AppIntent {
    static var title: LocalizedStringResource = "Get Trail Info"

    var trailID: String // No @Parameter -- the system can't discover or resolve this input.
    var minimumDifficulty: String // Free-form string instead of an AppEnum -- no picker, no validation.

    // No parameterSummary -- Shortcuts editor shows only the bare title.

    func perform() async throws -> some IntentResult {
        return .result()
    }
}
```
Declares `trailID`/`minimumDifficulty` as plain stored properties instead of `@Parameter`-wrapped inputs (Rule 2), uses a bare `String` for a value that should be a closed `AppEnum` set (Rule 3), and omits `parameterSummary` entirely (Rule 4).

## Dependencies

None within this domain — this is the foundational contract other App Intents Knowledge Contracts build on.

## References

-   [Apple Developer — AppIntent](https://developer.apple.com/documentation/appintents/appintent)
-   [Apple Developer — Adding parameters to an app intent](https://developer.apple.com/documentation/appintents/adding-parameters-to-an-app-intent)
-   [Apple Developer — IntentParameter (the `@Parameter` property wrapper)](https://developer.apple.com/documentation/appintents/intentparameter)
-   [Apple Developer — AppEnum](https://developer.apple.com/documentation/appintents/appenum)
-   [Apple Developer — ParameterSummary](https://developer.apple.com/documentation/appintents/parametersummary)
