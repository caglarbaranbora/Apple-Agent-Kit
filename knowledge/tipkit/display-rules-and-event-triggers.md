# Display Rules and Event Triggers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.tipkit.display-rules-and-event-triggers
artifact_type: knowledge
title: Display Rules and Event Triggers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the #Rule(_:) macro for declaring parameter-bound and event-bound display conditions on a Tip's rules property, donating app-usage events with Tips.Event and sendDonation(), and the AND combination of every rule on a tip.
domain: TipKit
tags:
  - tipkit
  - rule-macro
  - tips-parameter
  - tips-event
  - display-rules
references:
  - https://developer.apple.com/documentation/tipkit/tip/rules
  - https://developer.apple.com/documentation/tipkit/tips/rule
  - https://developer.apple.com/documentation/tipkit/tips/parameter
  - https://developer.apple.com/documentation/tipkit/tips/event
  - https://developer.apple.com/documentation/tipkit/tips/event/senddonation(_:)
  - https://developer.apple.com/documentation/tipkit/tips/event/donate()
  - https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit
depends_on:
  - knowledge.tipkit.tip-declaration-and-content
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent restricts *when* a tip is eligible to display: writing the `rules: [Self.Rule]` property with the `#Rule(_:)` macro over either a `Tips.Parameter`-wrapped state variable or a donated `Tips.Event`, and understanding that every rule attached to a tip must be true simultaneously (AND) before the tip becomes eligible.

## Scope

### Included

-   The `#Rule(_:)` macro — the real, verified API surface for declaring a display condition; it is a freestanding Swift macro, not a `Tip.rule(_:)` method
-   Binding a rule to app state with `@Tips.Parameter` (referenced via its `$`-prefixed projected value inside `#Rule(_:)`)
-   Binding a rule to a user action with `Tips.Event` (declared as a `static let`, donated with `sendDonation(_:)` or the async `donate()`, referenced directly — no `$` — inside `#Rule(_:)`)
-   The AND combination of every entry in a tip's `rules` array

### Excluded

-   `title`/`message`/`image`/`actions` and the base `Tip` conformance shape — see `tip-declaration-and-content`
-   `Tips.configure(_:)`, datastore/display-frequency configuration, and per-tip `Tip.Option`s (`MaxDisplayCount`, `MaxDisplayDuration`, `IgnoresDisplayFrequency`) — see `tip-options-and-app-configuration`
-   Presenting the tip and invalidating it once its rules pass — see `presenting-tips-and-tip-groups`

## Rules

### Rule 1

Agents MUST declare a rule with the `#Rule(_:)` macro inside the `rules` property, not by hand-writing conditional logic elsewhere or calling a nonexistent `Tip.rule(_:)` method. This was verified directly against Apple's TipKit sample code rather than assumed: every rule example in Apple's *Highlighting app features with TipKit* sample uses the literal syntax `#Rule(Self.$isLoggedIn) { $0 == true }` / `#Rule(Self.enteredView) { $0.donations.count >= 3 }` inside `var rules: [Rule] { ... }` — confirming `#Rule` is a real freestanding macro, and the brief's alternative hypothesis of a `Tip.rule(_:)` instance method does not exist in the framework.

### Rule 2

Agents binding a rule to app state MUST declare a `static` property wrapped in `@Tips.Parameter` and reference its projected value (`$propertyName`) as the macro's argument. Per Apple's documentation, `Tips.Parameter` is "A type that monitors the state of its wrapped value to reevaluate any dependent tip rules when the value changes"; Apple's sample declares `@Parameter static var isLoggedIn: Bool = false` and writes the rule as `#Rule(Self.$isLoggedIn) { $0 == true }`.

### Rule 3

Agents binding a rule to a user action MUST declare a `static let` of type `Tips.Event` (via `Event(id:)`), donate to it when the action occurs with `sendDonation(_:)` (completion-handler based) or the `async` `donate()`, and reference the event directly — no `$` prefix — as the macro's argument, inspecting `$0.donations` inside the closure. Per Apple's documentation, `Tips.Event` is "A repeatable user-defined action," and Apple's sample donates with `FoodEventTip.viewedSpecificFood.sendDonation(food)` and rules on it with `#Rule(FoodEventTip.viewedDetailView) { $0.donations.count >= 1 }`.

### Rule 4

Agents MUST treat every rule in a tip's `rules` array as combined with AND, and MUST NOT add a rule expecting OR semantics or expecting the tip to display if only some rules pass. This is a literal Apple quote, not an inference: Apple's own sample documentation states "These rules logically AND together in the rules property of the tip structure," describing a tip with one parameter-based rule and one event-based rule that both must be true before the tip displays.

### Rule 5

Agents MUST NOT assume a tip with an empty or absent `rules` array stays hidden by default. Per Apple's sample documentation, "If you define no rules within a tip content structure, all tips display until dismissed or they exceed the threshold of their display frequency" — omitting `rules` means the tip is eligible immediately, gated only by display-frequency/options behavior, not a safe "never shows" default.

## Compliant Example

```swift
import TipKit

struct FavoriteFeatureTip: Tip {
    // Rule 2: app-state-bound parameter.
    @Parameter
    static var hasSeenFavoritesList: Bool = false

    // Rule 3: user-action-bound event.
    static let openedItemDetail = Event(id: "opened-item-detail")

    var title: Text { Text("Save as a Favorite") }

    var rules: [Rule] {
        // Rule 1 + Rule 4: two rules, combined with AND.
        #Rule(Self.$hasSeenFavoritesList) { $0 == true }
        #Rule(Self.openedItemDetail) { $0.donations.count >= 3 }
    }
}

// Elsewhere, when the tracked interaction happens:
FavoriteFeatureTip.openedItemDetail.sendDonation() // Rule 3
```

## Non-Compliant Example

```swift
import TipKit

struct FavoriteFeatureTip: Tip {
    static let openedItemDetail = Event(id: "opened-item-detail")

    var title: Text { Text("Save as a Favorite") }

    var rules: [Rule] {
        // Violates Rule 3: reads openedItemDetail directly but never donates
        // to it anywhere in the app, so donations.count never advances --
        // the rule silently never passes.
        #Rule(Self.openedItemDetail) { $0.donations.count >= 3 }
    }

    // Assumes this second, unrelated tip only needs ONE of two conditions --
    // violates Rule 4, since TipKit always ANDs every entry in `rules`.
    // (No OR mechanism exists; each condition must be its own #Rule closure
    // returning Bool for that single condition, not a workaround for OR.)
}
```
Reads a `Tips.Event` in a rule but never calls `sendDonation(_:)`/`donate()` anywhere in the app (Rule 3), and assumes rules can express OR semantics rather than TipKit's fixed AND combination (Rule 4).

## Dependencies

-   `knowledge.tipkit.tip-declaration-and-content` — rules are declared on a `Tip`-conforming type that already has `title` and, optionally, `message`/`image`/`actions` defined.

## References

-   [Apple Developer — Tip.rules](https://developer.apple.com/documentation/tipkit/tip/rules)
-   [Apple Developer — Tips.Rule](https://developer.apple.com/documentation/tipkit/tips/rule)
-   [Apple Developer — Tips.Parameter](https://developer.apple.com/documentation/tipkit/tips/parameter)
-   [Apple Developer — Tips.Event](https://developer.apple.com/documentation/tipkit/tips/event)
-   [Apple Developer — Tips.Event.sendDonation(_:)](https://developer.apple.com/documentation/tipkit/tips/event/senddonation(_:))
-   [Apple Developer — Tips.Event.donate()](https://developer.apple.com/documentation/tipkit/tips/event/donate())
-   [Apple Developer — Highlighting app features with TipKit](https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit)
