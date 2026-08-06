# Animation Modifiers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.animation-modifiers
type: knowledge
title: Animation Modifiers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of implicit (.animation(_:value:)) and explicit (withAnimation) animation triggers, standard timing curves, and the iOS 17+ completion-callback overload.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/view/animation(_:value:)
  - https://developer.apple.com/documentation/swiftui/withanimation(_:_:)
  - https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:)
depends_on: []
related:
  - knowledge.swiftui.transitions
  - knowledge.human-interface-guidelines.motion
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent triggers SwiftUI animations correctly: scoping implicit animation to a specific value, wrapping synchronous state changes in `withAnimation`, choosing timing curves, and detecting completion without a guessed-duration workaround.

## Scope

### Included

- `.animation(_:value:)` value-scoped implicit animation
- `withAnimation(_:_:)` explicit animation of synchronous state changes
- Standard `Animation` timing curves (`.easeInOut`, `.linear`, `.spring(response:dampingFraction:blendDuration:)`, convenience spring presets)
- iOS 17+ `withAnimation(_:completionCriteria:_:completion:)` completion-callback overload

### Excluded

- View insertion/removal transition animation — see `transitions.md`
- Per-frame custom interpolation — see `animatable-values.md`
- Multi-phase/keyframe animation — see `phase-and-keyframe-animators.md`
- Design-level guidance on when/why to animate — see `knowledge.human-interface-guidelines.motion`

## Rules

### Rule 1

Agents MUST NOT use the deprecated `.animation(_:)` modifier (no `value:` parameter). It animates on any upstream state change, producing unpredictable results — use `.animation(_:value:)` scoped to a specific value, or `withAnimation` around the mutation.

### Rule 2

Agents MUST scope `.animation(_:value:)` to the exact value whose change should animate, not an unrelated or overly broad value.

### Rule 3

Agents MUST perform the state mutation to be animated synchronously inside the `withAnimation` closure — a mutation after an `await` does not animate.

### Rule 4

Agents SHOULD trigger `withAnimation` at the single call site that changes state, rather than scattering `.animation(_:value:)` across multiple views when several properties must animate together.

### Rule 5

Agents MUST use the iOS 17+ `withAnimation(_:completionCriteria:_:completion:)` overload to run code after animation completes. Agents MUST NOT use `DispatchQueue.main.asyncAfter` with a guessed duration.

### Rule 6

Agents SHOULD choose `.logicallyComplete` completion criteria for callbacks that fire once the animation's target state is reached (e.g., re-enabling buttons), and reserve `.removed` for cases requiring full render completion.

## Compliant Example

```swift
struct ExpandableCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("Card")
            if isExpanded {
                Text("Extra detail")
            }
        }
        .animation(.easeInOut, value: isExpanded)
        .onTapGesture {
            withAnimation(.spring(response: 0.4, dampingFraction: 0.8), completionCriteria: .logicallyComplete) {
                isExpanded.toggle()
            } completion: {
                print("Card animation reached target state")
            }
        }
    }
}
```

Value-scoped `.animation(_:value:)`, explicit `withAnimation` with completion callback. (Rules 1, 2, 5, 6)

## Non-Compliant Example

```swift
struct ExpandableCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("Card")
            if isExpanded {
                Text("Extra detail")
            }
        }
        .animation(.easeInOut) // deprecated, no value:
        .onTapGesture {
            isExpanded.toggle()
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                print("guessed animation is done")
            }
        }
    }
}
```

Deprecated `.animation(_:)` and guessed-duration workaround instead of completion callback. (Rules 1, 5)

## Dependencies

None.

## References

- [Apple Developer — animation(_:value:)](https://developer.apple.com/documentation/swiftui/view/animation(_:value:))
- [Apple Developer — withAnimation(_:_:)](https://developer.apple.com/documentation/swiftui/withanimation(_:_:))
- [Apple Developer — withAnimation(_:completionCriteria:_:completion:)](https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:))
