# Intent Results and Widget Hookup

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-intents.intent-results-and-widget-hookup
artifact_type: knowledge
title: Intent Results and Widget Hookup
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the IntentResult protocol and its ReturnsValue/ProvidesDialog/OpensIntent variants returned from perform(), and closes the seam with widgetkit -- this is where an AppIntent used in a widget's Button(intent:)/Toggle(_:isOn:intent:) actually gets authored.
domain: App Intents
tags:
  - app-intents
  - intentresult
  - returnsvalue
  - providesdialog
  - opensintent
references:
  - https://developer.apple.com/documentation/appintents/intentresult
  - https://developer.apple.com/documentation/appintents/returnsvalue
  - https://developer.apple.com/documentation/appintents/providesdialog
  - https://developer.apple.com/documentation/appintents/opensintent
depends_on:
  - knowledge.app-intents.app-intent-declaration-and-parameters
related:
  - knowledge.widgetkit.widget-interactivity-and-deep-links
last_updated: 2026-08-06
```

## Intent

This contract defines what an `AppIntent`'s `perform()` returns: the `IntentResult` protocol and its composable variants `ReturnsValue<Value>`, `ProvidesDialog`, and `OpensIntent`, built with the static `.result(...)` factory methods. It also closes a seam with the `widgetkit` domain: `knowledge.widgetkit.widget-interactivity-and-deep-links` already covers wiring an *already-authored* `AppIntent` into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)` — this contract is where that intent's `perform()` body, parameters, and result actually get authored.

## Scope

### Included

-   `IntentResult` and the `.result()` family of static factory methods
-   `ReturnsValue<Value>` for delivering a value back to the caller
-   `ProvidesDialog` for delivering spoken/displayed dialog back to the caller
-   `OpensIntent` for delivering a follow-up intent the system should run next
-   Authoring the `perform()` body, parameters, and result type of an `AppIntent` that a widget will later reference via `Button(intent:)`/`Toggle(_:isOn:intent:)`

### Excluded

-   Wiring an already-authored `AppIntent` into `Button(intent:)`/`Toggle(_:isOn:intent:)` inside a widget's view, or anything inside a widget extension's `TimelineProvider`/`Timeline` — owned by `widgetkit` (`knowledge.widgetkit.widget-interactivity-and-deep-links`)
-   Interactive Snippets and other visual intent-response UI customization beyond `ProvidesDialog` (e.g. `ShowsSnippetView`)
-   `LiveActivityIntent` as a distinct topic — it exists (an intent that starts, pauses, or modifies a Live Activity) but its specifics are deferred
-   Declaring the intent's own parameters — see `app-intent-declaration-and-parameters`

## Rules

### Rule 1

Agents MUST return a type conforming to `IntentResult` from `perform()` — typically written as an opaque `some IntentResult` (and composed protocols) rather than a concrete type — and MUST build it with one of the `IntentResult` static `.result(...)` factory methods rather than constructing a result type by hand. Per Apple's documentation, `IntentResult` is "A type that contains the result of performing an action, and includes optional information to deliver back to the initiator," and `AppIntent.perform()` is declared as `func perform() async throws -> Self.PerformResult` where `associatedtype PerformResult : IntentResult`. An intent with nothing to report back MUST use the bare `.result()` case.

### Rule 2

Agents MUST compose the `perform()` return type with `ReturnsValue<Value>` (`protocol ReturnsValue<Value> : IntentResult`) and call `.result(value:)` whenever the intent has a value the caller needs — e.g. so a widget's `Button(intent:)` action can read back the state it just toggled — and MUST NOT stash the value somewhere else for the caller to poll. Per Apple's documentation, `ReturnsValue` is "The result of performing an action that delivers a value back to the initiator."

### Rule 3

Agents MUST compose the `perform()` return type with `ProvidesDialog` (`protocol ProvidesDialog : IntentResult where Self.Dialog == IntentDialog`) and call `.result(dialog:)`/`.result(value:dialog:)` whenever Siri or another voice-first surface needs something to say back, and MUST NOT rely on `ReturnsValue` alone to communicate outcome to a spoken interaction — `ReturnsValue` carries data, not something speakable. Per Apple's documentation, `ProvidesDialog` is "The result of performing an action that delivers a dialog back to the initiator of the action."

### Rule 4

Agents MUST compose the `perform()` return type with `OpensIntent` (`protocol OpensIntent : IntentResult`) and call `.result(opensIntent:)` when completing the current intent should hand off to a specific follow-up `AppIntent`, rather than having `perform()` try to invoke that follow-up intent's logic directly inline. Per Apple's documentation, `OpensIntent` is "The result of performing an action that delivers an app intent back to the initiator of the action."

### Rule 5

Agents authoring an `AppIntent` that a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)` will bind to MUST fully implement that intent's `perform()`, parameters, and result here, per Rules 1–4, and MUST treat the widget-side wiring itself as out of scope for this contract — that binding step is `knowledge.widgetkit.widget-interactivity-and-deep-links`'s territory. Agents MUST NOT leave `perform()` as a stub on the assumption that the widget domain will "finish" the intent; a widget's `Button`/`Toggle` only invokes an intent that already runs correctly on its own.

## Compliant Example

```swift
struct ToggleTodoIntent: AppIntent {
    static var title: LocalizedStringResource = "Toggle Todo"

    @Parameter(title: "Todo ID")
    var id: Todo.ID

    @Dependency
    var todoStore: TodoStore

    func perform() async throws -> some IntentResult & ReturnsValue<Bool> & ProvidesDialog {
        let isComplete = try await todoStore.toggleCompletion(for: id)
        let dialog = IntentDialog(isComplete ? "Marked complete." : "Marked incomplete.")
        return .result(value: isComplete, dialog: dialog)
    }
}
```
`perform()` returns `some IntentResult` composed with `ReturnsValue<Bool>` and `ProvidesDialog` (Rules 1, 2, 3), built via `.result(value:dialog:)`; this is the fully authored intent a widget's `Toggle(_:isOn:intent:)` can later bind to unchanged (Rule 5). (Rules 1, 2, 3, 5)

## Non-Compliant Example

```swift
struct ToggleTodoIntent: AppIntent {
    static var title: LocalizedStringResource = "Toggle Todo"

    @Parameter(title: "Todo ID")
    var id: Todo.ID

    func perform() async throws -> some IntentResult {
        // TODO: finish this once it's wired into the widget button.
        return .result()
    }
}
```
Leaves `perform()` as a stub that never toggles anything, on the mistaken assumption that wiring the intent into a widget's `Button`/`Toggle` will "complete" it (Rule 5), and returns a bare `.result()` even though callers need the toggled value back, so it should compose `ReturnsValue<Bool>` (Rule 2).

## Dependencies

-   `knowledge.app-intents.app-intent-declaration-and-parameters` — the `perform()` this contract governs belongs to an `AppIntent` declared per that contract's rules.
-   `knowledge.widgetkit.widget-interactivity-and-deep-links` — covers wiring this contract's already-authored intent into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)`; not restated here.

## References

-   [Apple Developer — IntentResult](https://developer.apple.com/documentation/appintents/intentresult)
-   [Apple Developer — ReturnsValue](https://developer.apple.com/documentation/appintents/returnsvalue)
-   [Apple Developer — ProvidesDialog](https://developer.apple.com/documentation/appintents/providesdialog)
-   [Apple Developer — OpensIntent](https://developer.apple.com/documentation/appintents/opensintent)
