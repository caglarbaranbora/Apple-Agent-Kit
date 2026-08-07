# Transitions

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.transitions
artifact_type: knowledge
title: Transitions
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of AnyTransition and .transition(_:) for view insertion/removal animation tied to view-identity changes.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/view/transition(_:)
  - https://developer.apple.com/documentation/swiftui/anytransition
depends_on: []
related:
  - knowledge.swiftui.animation-modifiers
  - knowledge.swiftui.view-identity
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent animates view insertion/removal using `AnyTransition` and `.transition(_:)`, and prevents the common mistake of applying a transition without an animation to trigger it.

## Scope

### Included

- `.transition(_:)` modifier
- `AnyTransition` statics: `.opacity`, `.slide`, `.move(edge:)`, `.scale`, `.asymmetric(insertion:removal:)`, `.combined(with:)`
- Pairing transitions with `withAnimation`/`.animation(_:value:)` and view-identity changes

### Excluded

- Shared-element transitions between co-present views — see `matched-geometry-effect.md`
- Custom per-frame interpolation — see `animatable-values.md`

## Rules

### Rule 1

Agents MUST pair `.transition(_:)` with a `withAnimation` call (or ancestor `.animation(_:value:)`) around the state change that inserts/removes the view. `.transition` only declares how a view animates in/out — it doesn't trigger the animation.

### Rule 2

Agents MUST apply `.transition(_:)` to a view whose presence in the hierarchy is conditionally toggled (an `if` branch or `ForEach` membership changing) — applying it to a view that never leaves has no visible effect.

### Rule 3

Agents SHOULD use `.asymmetric(insertion:removal:)` when appearing/disappearing should differ visually (e.g., slide in from edge, fade out in place).

### Rule 4

Agents SHOULD use `.combined(with:)` to layer multiple transitions (e.g., `.opacity.combined(with: .scale)`) rather than adding wrapper views to fake a combined effect.

### Rule 5

Agents MUST NOT rely on `.transition(_:)` to animate a view remaining present but changing an internal property (position, size, color) without identity change — use `.animation(_:value:)`/`withAnimation` directly instead.

## Compliant Example

```swift
struct ToastView: View {
    @State private var showToast = false

    var body: some View {
        VStack {
            Button("Show") {
                withAnimation(.easeInOut) {
                    showToast = true
                }
            }
            if showToast {
                Text("Saved")
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
    }
}
```

`.transition` paired with `withAnimation`, applied to conditionally present view, combining transitions. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
struct ToastView: View {
    @State private var showToast = false

    var body: some View {
        VStack {
            Button("Show") {
                showToast = true // no withAnimation
            }
            if showToast {
                Text("Saved")
                    .transition(.opacity)
            }
        }
    }
}
```

Transition declared but the state change isn't wrapped in
`withAnimation`, so the toast appears instantly instead of fading in.
(Rule 1)

## Dependencies

None.

## References

- [Apple Developer — transition(_:)](https://developer.apple.com/documentation/swiftui/view/transition(_:))
- [Apple Developer — AnyTransition](https://developer.apple.com/documentation/swiftui/anytransition)
