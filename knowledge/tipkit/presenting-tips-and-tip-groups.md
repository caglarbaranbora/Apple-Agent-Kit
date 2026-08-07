# Presenting Tips and Tip Groups

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.tipkit.presenting-tips-and-tip-groups
artifact_type: knowledge
title: Presenting Tips and Tip Groups
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines presenting a tip with SwiftUI's TipView/popoverTip(_:arrowEdge:action:) vs. UIKit's TipUIView/TipUIPopoverViewController, grouping tips with TipGroup so at most one tip in the group shows at a time, and dismissing a tip programmatically with invalidate(reason:) and Tip.InvalidationReason.
domain: TipKit
tags:
  - tipkit
  - tipview
  - tipuiview
  - tipgroup
  - invalidation
references:
  - https://developer.apple.com/documentation/tipkit/tipview
  - https://developer.apple.com/documentation/tipkit/tipuiview
  - https://developer.apple.com/documentation/tipkit/tipuipopoverviewcontroller
  - https://developer.apple.com/documentation/tipkit/tipgroup
  - https://developer.apple.com/documentation/tipkit/tipgroup/init(_:_:)
  - https://developer.apple.com/documentation/tipkit/tipgroup/priority
  - https://developer.apple.com/documentation/tipkit/tipgroup/currenttip
  - https://developer.apple.com/documentation/tipkit/tip/invalidate(reason:)
  - https://developer.apple.com/documentation/tipkit/tips/invalidationreason
depends_on:
  - knowledge.tipkit.tip-declaration-and-content
related:
  - knowledge.tipkit.tip-options-and-app-configuration
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent presents a tip once it is eligible to display: choosing `TipView`/`popoverTip(_:arrowEdge:action:)` in SwiftUI or `TipUIView`/`TipUIPopoverViewController` in UIKit, coordinating multiple candidate tips with `TipGroup` so only one shows at a time, and dismissing a tip programmatically with `invalidate(reason:)`.

## Scope

### Included

-   `TipView`, a SwiftUI `struct` placed inline near the feature it describes, vs. `popoverTip(_:arrowEdge:action:)`, a view modifier that overlays the tip
-   `TipUIView` and `TipUIPopoverViewController`, the UIKit equivalents (both `@MainActor final class`, not SwiftUI views)
-   `TipGroup`, its `init(_:_:)` builder, its `Priority` (`.firstAvailable` default vs. `.ordered`), and reading `currentTip`
-   `invalidate(reason:)` and the four `Tip.InvalidationReason` cases: `.actionPerformed`, `.displayCountExceeded`, `.displayDurationExceeded`, `.tipClosed`

### Excluded

-   `title`/`message`/`image`/`actions` and the base `Tip` conformance shape — see `tip-declaration-and-content`
-   The `rules`/`#Rule(_:)` display-condition machinery — see `display-rules-and-event-triggers`
-   `Tips.configure(_:)` and per-tip `Tip.Option`s (related, not depended on: presentation assumes configuration already happened) — see `tip-options-and-app-configuration`
-   Authoring a custom `TipViewStyle` beyond the system default — out of scope for this domain's v1

## Rules

### Rule 1

Agents building a SwiftUI screen MUST place `TipView(_:arrowEdge:action:)` inline, next to the feature it describes, and reserve `popoverTip(_:arrowEdge:action:)` for cases where obscuring the underlying UI is acceptable. Per Apple's documentation, `TipView` is "A user interface element that represents an inline tip," and Apple's sample guidance states: "Use this style of tip whenever possible to avoid covering UI elements that people may want to interact with... Use this style of tip view if adjusting the underlying layout is undesirable" for the popover alternative.

### Rule 2

Agents building a UIKit screen MUST use `TipUIView`/`TipUIPopoverViewController`, not attempt to bridge SwiftUI's `TipView` into UIKit. This was verified directly against Apple's TipKit framework symbol index rather than assumed: `TipUIView` is "A user interface element that represents a tip in UIKit applications" and `TipUIPopoverViewController` is "A view controller that displays a popover tip in UIKit applications" — both declared `@MainActor @objc final class`, confirming they are the framework's own dedicated UIKit types, not a SwiftUI wrapper.

### Rule 3

Agents needing to show at most one tip from a prioritized set of candidates MUST group them with `TipGroup(_:_:)` and read `currentTip` rather than manually tracking which tip is "active." Per Apple's documentation, `TipGroup` is "A collection of tips that can be presented one at a time," and `currentTip` "Returns the current tip available for display" as a single optional (`(any Tip)?`), not an array.

### Rule 4

Agents MUST NOT assume `TipGroup`'s default priority is strict array order (`.ordered`) — the verified default is `.firstAvailable`. Per Apple's documentation, `TipGroup.init(_:_:)` is declared `init(_ priority: TipGroup.Priority = .firstAvailable, @Tips.GroupBuilder _ builder: () -> [any Tip])`. Array order still matters under both modes: `.firstAvailable` "Shows the first tip eligible for display" (the first candidate in array order whose own rules currently pass), while `.ordered` "Shows an eligible tip when all of the previous tips have been [invalidated]" (a strict, sequential gate through the array). Agents needing the sequential behavior MUST pass `.ordered` explicitly.

### Rule 5

Agents dismissing a tip after the feature it describes was used MUST call `invalidate(reason:)` with the `Tip.InvalidationReason` case that matches why, and MUST NOT rely only on the person tapping the tip's built-in close button. The four verified cases are `.actionPerformed` ("The user performed the action that the tip describes"), `.displayCountExceeded`, `.displayDurationExceeded`, and `.tipClosed` ("The user explicitly closed the tip view while it was displaying") — `.tipClosed` and the count/duration cases are system-driven, so an agent's own code should pass `.actionPerformed` when the person completes the described action programmatically.

## Compliant Example

```swift
import SwiftUI
import TipKit

struct FeatureScreen: View {
    let favoriteTip = FavoriteFeatureTip()

    var body: some View {
        VStack {
            TipView(favoriteTip, arrowEdge: .bottom) // Rule 1: inline placement
            Button("Favorite") {
                // Rule 5: matches the action the tip describes.
                favoriteTip.invalidate(reason: .actionPerformed)
            }
        }
    }
}

struct OnboardingTipsView: View {
    // Rule 3 + Rule 4: default .firstAvailable priority, array order matters.
    @State var tips = TipGroup {
        WelcomeTip()
        FavoriteFeatureTip()
    }

    var body: some View {
        TipView(tips.currentTip as? WelcomeTip)
        TipView(tips.currentTip as? FavoriteFeatureTip)
    }
}
```

## Non-Compliant Example

```swift
import SwiftUI
import TipKit

struct FeatureScreen: View {
    let favoriteTip = FavoriteFeatureTip()

    var body: some View {
        // Violates Rule 1: popoverTip hides a persistent control instead of
        // an inline TipView. No invalidate(reason:) call when the favorite
        // action completes, either -- violates Rule 5; stays eligible forever.
        Button("Favorite") {}
            .popoverTip(favoriteTip)
    }
}
```
Uses `popoverTip` where an inline `TipView` was the right choice for a control that must stay interactable (Rule 1), and never calls `invalidate(reason:)` when the described action completes (Rule 5).

## Dependencies

-   `knowledge.tipkit.tip-declaration-and-content` — presentation assumes a `Tip`-conforming type with `title` already exists.
-   `knowledge.tipkit.tip-options-and-app-configuration` (related) — presentation assumes `Tips.configure(_:)` already ran; per-tip options there interact with, but don't gate, presentation choices here.

## References

-   [Apple Developer — TipView](https://developer.apple.com/documentation/tipkit/tipview)
-   [Apple Developer — TipUIView](https://developer.apple.com/documentation/tipkit/tipuiview)
-   [Apple Developer — TipUIPopoverViewController](https://developer.apple.com/documentation/tipkit/tipuipopoverviewcontroller)
-   [Apple Developer — TipGroup](https://developer.apple.com/documentation/tipkit/tipgroup)
-   [Apple Developer — TipGroup.init(_:_:)](https://developer.apple.com/documentation/tipkit/tipgroup/init(_:_:))
-   [Apple Developer — TipGroup.Priority](https://developer.apple.com/documentation/tipkit/tipgroup/priority)
-   [Apple Developer — TipGroup.currentTip](https://developer.apple.com/documentation/tipkit/tipgroup/currenttip)
-   [Apple Developer — Tip.invalidate(reason:)](https://developer.apple.com/documentation/tipkit/tip/invalidate(reason:))
-   [Apple Developer — Tips.InvalidationReason](https://developer.apple.com/documentation/tipkit/tips/invalidationreason)
