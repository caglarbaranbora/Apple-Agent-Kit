# App Shortcuts and Siri Phrases

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-intents.app-shortcuts-and-siri-phrases
artifact_type: knowledge
title: App Shortcuts and Siri Phrases
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the AppShortcutsProvider protocol's appShortcuts static property, the AppShortcut struct (phrase, shortTitle, systemImageName), phrase-authoring rules (must include applicationName, must be unambiguous, up to 10 per app), the one-AppShortcutsProvider-per-app constraint, and updateAppShortcutParameters().
domain: App Intents
tags:
  - app-intents
  - appshortcutsprovider
  - appshortcut
  - siri-phrases
  - shortcuts
references:
  - https://developer.apple.com/documentation/appintents/appshortcutsprovider
  - https://developer.apple.com/documentation/appintents/appshortcut
  - https://developer.apple.com/design/human-interface-guidelines/app-shortcuts
depends_on:
  - knowledge.app-intents.app-intent-declaration-and-parameters
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent publishes an already-declared `AppIntent` to Siri and the Shortcuts app: implementing `AppShortcutsProvider`'s `appShortcuts` static property, constructing each `AppShortcut` with a phrase, `shortTitle`, and `systemImageName`, following phrase-authoring rules so Siri can reliably match what someone says, and keeping stored shortcut parameters current with `updateAppShortcutParameters()`.

## Scope

### Included

-   `AppShortcutsProvider` conformance and its `@AppShortcutsBuilder static var appShortcuts: [AppShortcut]` requirement
-   The `AppShortcut` struct: `init(intent:phrases:shortTitle:systemImageName:)`
-   Phrase-authoring rules: every phrase must include `\(.applicationName)`, must be phrasable without ambiguity, up to 10 App Shortcuts per app
-   The one-`AppShortcutsProvider`-conformance-per-app constraint
-   `AppShortcutsProvider.updateAppShortcutParameters()`

### Excluded

-   Custom Siri vocabulary and `NegativeAppShortcutPhrase`/`AppShortcutOptionsCollection` beyond basic phrase authoring
-   Declaring the underlying `AppIntent`, its parameters, or `perform()` — see `app-intent-declaration-and-parameters`
-   `AppEntity`/`EntityQuery` that a shortcut's intent may reference — see `app-entities-and-queries`
-   Legacy `SiriKit` donation-based intents (`INIntent`, `NSUserActivity` donation) — superseded by App Intents

## Rules

### Rule 1

Agents MUST implement `AppShortcutsProvider` with exactly one conforming type per app target, exposing `@AppShortcutsBuilder static var appShortcuts: [AppShortcut]`, and MUST NOT declare a second conformer. Per Apple's documentation, "to provide App Shortcuts for your app intents, create a type that conforms to the `AppShortcutsProvider` protocol. In your type, create an `AppShortcut` type for each of your app intents. The compiler extracts your code and makes it available to the Shortcuts app and the rest of the system" — the framework's build-time extraction of `appShortcuts` is keyed to a single provider type per app, so agents MUST consolidate all of an app's shortcuts into one `AppShortcutsProvider` rather than spreading them across several.

### Rule 2

Agents MUST construct each `AppShortcut` with `init(intent:phrases:shortTitle:systemImageName:)`, supplying a `LocalizedStringResource` for `shortTitle` (not `title`) and a system symbol name for `systemImageName`, and MUST keep the app to at most 10 `AppShortcut`s. Per Apple's documentation, this initializer "Initializes an App Shortcut with phrases that run the app intent, a title, and an image," with the signature `init<Intent>(intent: Intent, phrases: [AppShortcutPhrase<Intent>], shortTitle: LocalizedStringResource, systemImageName: String)`. Per Apple's Human Interface Guidelines, "Each app can include up to 10 App Shortcuts."

### Rule 3

Agents MUST include `\(.applicationName)` in every phrase passed to an `AppShortcut`, and MUST write phrases that are short and unambiguous rather than layering multiple parameters into one spoken sentence. Per Apple's documentation, a phrase example reads `"Open Favorites in \(.applicationName)"`, and per Apple's Human Interface Guidelines, "Provide brief, memorable activation phrases and natural variants. Because an App Shortcut phrase (or a variant you define) is what people say to run an App Shortcut with Siri, it's important to keep it brief to make it easier to remember. You have to include your app name, but you can be creative with it." The guidelines also warn: "Keep voice interactions simple. If your phrase feels too complicated when you say it aloud, it's probably too difficult to remember or say correctly" — citing a phrase with two parameters as an example of one that's too complicated. Agents MUST NOT author a phrase with more than one parameter placeholder for this reason.

### Rule 4

Agents MUST call `AppShortcutsProvider.updateAppShortcutParameters()` after a runtime event that changes which parameter values the system should have pre-resolved for a shortcut (e.g. new data becoming available), rather than assuming stored shortcuts refresh automatically. Per Apple's documentation, `AppShortcutsProvider` declares `static func updateAppShortcutParameters()` under "Updating stored parameters" — it exists precisely because the system caches resolved parameter values for a shortcut and needs an explicit signal to re-resolve them.

## Compliant Example

```swift
struct OpenFavorites: AppIntent {
    static var title: LocalizedStringResource = "Open Favorites"

    func perform() async throws -> some IntentResult {
        return .result()
    }
}

struct TrailsShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: OpenFavorites(),
            phrases: [
                "Open Favorites in \(.applicationName)",
                "Show my favorite trails in \(.applicationName)"
            ],
            shortTitle: "Open Favorites",
            systemImageName: "star.circle"
        )
    }
}
```
Exactly one `AppShortcutsProvider` conformer for the app (Rule 1), the `AppShortcut` is built with `shortTitle`/`systemImageName` (Rule 2), and both phrases include `\(.applicationName)` and stay short with a single implicit subject, no parameter placeholder (Rule 3). (Rules 1, 2, 3)

## Non-Compliant Example

```swift
struct TrailsShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: OpenFavorites(),
            phrases: ["Open my favorites"], // Missing \(.applicationName) -- Siri can't disambiguate the target app.
            shortTitle: "Open Favorites",
            systemImageName: "star.circle"
        )
    }
}

struct SearchShortcuts: AppShortcutsProvider { // A second conformer -- violates the one-per-app constraint.
    static var appShortcuts: [AppShortcut] {
        AppShortcut(intent: SearchTrails(), phrases: ["Search trails in \(.applicationName) for \(\.$region) near \(\.$activity)"],
                    shortTitle: "Search", systemImageName: "magnifyingglass")
    }
}
```
Omits `\(.applicationName)` from a phrase (Rule 3), declares a second `AppShortcutsProvider` conformer in the same app instead of consolidating into one (Rule 1), and stacks two parameter placeholders into a single spoken phrase instead of keeping it simple (Rule 3).

## Dependencies

-   `knowledge.app-intents.app-intent-declaration-and-parameters` — an `AppShortcut` always wraps an already-declared `AppIntent`; this contract does not redefine intent declaration itself.

## References

-   [Apple Developer — AppShortcutsProvider](https://developer.apple.com/documentation/appintents/appshortcutsprovider)
-   [Apple Developer — AppShortcut](https://developer.apple.com/documentation/appintents/appshortcut)
-   [Apple Human Interface Guidelines — App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)
