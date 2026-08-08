# Tip Declaration and Content

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.tipkit.tip-declaration-and-content
artifact_type: knowledge
title: Tip Declaration and Content
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines conforming a struct to the Tip protocol -- the required title (Text) property, optional message (Text?) and image (Image?) properties, and the actions ([Tip.Action]) property for tip-embedded buttons -- as the minimal-conformance shape every other TipKit contract builds on.
domain: TipKit
tags:
  - tipkit
  - tip-protocol
  - tip-action
  - onboarding
  - feature-tips
references:
  - https://developer.apple.com/documentation/tipkit/tip
  - https://developer.apple.com/documentation/tipkit/tip/title
  - https://developer.apple.com/documentation/tipkit/tip/message
  - https://developer.apple.com/documentation/tipkit/tip/image
  - https://developer.apple.com/documentation/tipkit/tip/actions
  - https://developer.apple.com/documentation/tipkit/tip/action
  - https://developer.apple.com/documentation/tipkit/tips/action/init(id:title:perform:)
  - https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent declares a tip's content: conforming a `struct` to the `Tip` protocol, supplying the one required property (`title`), the optional descriptive properties (`message`, `image`), and optional embedded buttons (`actions`). Every other TipKit Knowledge Contract in this domain assumes a `Tip`-conforming type already exists in this shape.

## Scope

### Included

-   Conforming a `struct` (not a class) to the `Tip` protocol
-   The required `title: Text { get }` property
-   The optional `message: Text? { get }` and `image: Image? { get }` properties
-   The optional `actions: [Self.Action] { get }` property, built with `Tip.Action`'s `init(id:title:perform:)` for tip-embedded buttons with their own handler closures

### Excluded

-   The `rules`/`options` properties and everything that drives when a tip is eligible to display — see `display-rules-and-event-triggers` and `tip-options-and-app-configuration`
-   Calling `Tips.configure(_:)` and app-launch setup — see `tip-options-and-app-configuration`
-   Presenting the tip (`TipView`, `TipUIView`, `TipGroup`) and invalidating it — see `presenting-tips-and-tip-groups`

## Rules

### Rule 1

Agents MUST conform a `struct` to the `Tip` protocol, not a `class`. This is reasoned framework behavior rather than a literal Apple-documentation quote for the requirement itself, but it is directly demonstrated in Apple's own TipKit sample: "Each example defines a structure that conforms to the `Tip` protocol, and sets the properties that define the tip content" (Apple's *Highlighting app features with TipKit* sample documentation) — every first-party example, with no exception, is a `struct`.

### Rule 2

Agents MUST implement `title: Text`, the only property `Tip` requires with no default. Per Apple's documentation, `Tip.title` is "A title that names the tip," declared as `var title: Text { get }` with no `?` — omitting it is a protocol-conformance compile error, not a runtime default.

### Rule 3

Agents SHOULD implement `message: Text?` and `image: Image?` only when the tip needs descriptive body text or an accompanying image, and MUST NOT treat either as required. Per Apple's documentation, `message` is "A short description of how to use the tip's feature" and `image` is "The image associated with the tip," both declared with `Text?`/`Image?` return types; a tip with only `title` set is valid and compiles.

### Rule 4

Agents adding buttons to a tip MUST declare them through the `actions: [Self.Action] { get }` property using `Tip.Action`, not through custom view code layered on top of `TipView`. Per Apple's documentation, `Tip.Action` "describes a control associated with a tip," and its `init(id:title:perform:)` initializer is `init(id: String? = nil, title: some StringProtocol, perform handler: @escaping @MainActor @Sendable () -> Void = {})` — each action carries its own `id` (for dispatching inside a `TipView` trailing-closure handler) and optionally its own `perform` handler.

### Rule 5

Agents MUST NOT assume `message`, `image`, or `actions` need an explicit empty-value override when unused — Apple's own minimal sample tip (`InlineTip`) implements only `title`, `message`, and `image`, omitting `actions` entirely and compiling without error, confirming the property carries a usable default when absent.

## Compliant Example

```swift
import SwiftUI
import TipKit

struct FavoriteFeatureTip: Tip {
    var title: Text {
        Text("Save as a Favorite") // Rule 2: the one required property
    }

    var message: Text? {
        Text("Your favorite items always appear at the top of the list.") // Rule 3
    }

    var image: Image? {
        Image(systemName: "star") // Rule 3
    }

    var actions: [Action] {
        Action(id: "learn-more", title: "Learn More") { // Rule 4
            // Handle the button tap, e.g. navigate to a help screen.
        }
    }
}
```

## Non-Compliant Example

```swift
import SwiftUI
import TipKit

// Violates Rule 1: a class, not a struct, conforming to Tip.
final class FavoriteFeatureTip: Tip {
    // Violates Rule 2: `title` is missing entirely -- this does not compile,
    // because `Tip.title` has no default implementation.

    var message: Text? {
        Text("Your favorite items always appear at the top of the list.")
    }
}
```
Conforms with a `class` instead of a `struct` (Rule 1) and omits the one property `Tip` actually requires, `title` (Rule 2).

## Dependencies

None within this domain — this is the foundational contract every other TipKit Knowledge Contract assumes a `Tip`-conforming type already exists in this shape.

## References

-   [Apple Developer — Tip](https://developer.apple.com/documentation/tipkit/tip)
-   [Apple Developer — Tip.title](https://developer.apple.com/documentation/tipkit/tip/title)
-   [Apple Developer — Tip.message](https://developer.apple.com/documentation/tipkit/tip/message)
-   [Apple Developer — Tip.image](https://developer.apple.com/documentation/tipkit/tip/image)
-   [Apple Developer — Tip.actions](https://developer.apple.com/documentation/tipkit/tip/actions)
-   [Apple Developer — Tip.Action](https://developer.apple.com/documentation/tipkit/tip/action)
-   [Apple Developer — Tips.Action.init(id:title:perform:)](https://developer.apple.com/documentation/tipkit/tips/action/init(id:title:perform:))
-   [Apple Developer — Highlighting app features with TipKit](https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit)
