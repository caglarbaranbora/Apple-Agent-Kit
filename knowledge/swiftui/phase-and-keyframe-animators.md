# Phase and Keyframe Animators

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.phase-and-keyframe-animators
type: knowledge
title: Phase and Keyframe Animators
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when to use iOS 17+ PhaseAnimator for discrete repeating/triggered phase cycling versus KeyframeAnimator for independent per-property animation timelines.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/phaseanimator
  - https://developer.apple.com/documentation/swiftui/keyframeanimator
depends_on: []
related:
  - knowledge.swiftui.animation-modifiers
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use `PhaseAnimator` versus `KeyframeAnimator` (both iOS 17+) instead of chaining multiple `withAnimation` calls or using a manual `Timer`, for multi-step or timeline-based animation.

## Scope

### Included

- `PhaseAnimator` — discrete phase cycling, repeating or `trigger`-replayed
- `KeyframeAnimator` — independent per-property timelines (`KeyframeTrack`, `LinearKeyframe`, `CubicKeyframe`, `SpringKeyframe`, `MoveKeyframe`)
- Choosing between `PhaseAnimator`, `KeyframeAnimator`, and plain `withAnimation`

### Excluded

- Single state-change animation — see `animation-modifiers.md`
- View insertion/removal transitions — see `transitions.md`

## Rules

### Rule 1

Agents MUST use `PhaseAnimator` (not a manual `Timer` or recursive `withAnimation` calls) when a view cycles through a fixed sequence of discrete visual phases, either continuously repeating or replayed when a `trigger` value changes.

### Rule 2

Agents MUST use `KeyframeAnimator` (not multiple staggered `withAnimation` calls) when independent properties — scale and rotation — need their own timing curve on a shared timeline; use a separate `KeyframeTrack` per property.

### Rule 3

Agents SHOULD avoid expensive work directly inside a `PhaseAnimator`/`KeyframeAnimator` content closure. Apple's `KeyframeAnimator` documentation states the content closure updates every frame while animating.

### Rule 4

Agents MUST use the iOS 17+ `withAnimation(_:completionCriteria:_:completion:)` overload (see `animation-modifiers.md`) rather than fixed-duration `DispatchQueue.asyncAfter` when code must run after external animation completes.

### Rule 5

Agents SHOULD use the `trigger:` initializer when the phase sequence/keyframe timeline should play exactly once in response to specific event (success checkmark), and reserve non-trigger continuously repeating initializer for looping effects (pulsing indicator).

## Compliant Example

```swift
struct SuccessCheckmark: View {
    enum Phase: CaseIterable {
        case initial, popped, settled
    }
    let trigger: Bool

    var body: some View {
        Image(systemName: "checkmark.circle.fill")
            .phaseAnimator(Phase.allCases, trigger: trigger) { content, phase in
                content
                    .scaleEffect(phase == .popped ? 1.3 : 1.0)
            } animation: { phase in
                switch phase {
                case .initial: .default
                case .popped: .spring(response: 0.3, dampingFraction: 0.5)
                case .settled: .easeOut
                }
            }
    }
}
```

`PhaseAnimator` with `trigger:` initializer plays pop-and-settle sequence once per trigger change. (Rules 1, 5)

## Non-Compliant Example

```swift
struct SuccessCheckmark: View {
    @State private var scale: CGFloat = 1.0

    func animateSequence() {
        withAnimation(.spring(response: 0.3, dampingFraction: 0.5)) {
            scale = 1.3
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            withAnimation(.easeOut) {
                self.scale = 1.0
            }
        }
    }

    var body: some View {
        Image(systemName: "checkmark.circle.fill")
            .scaleEffect(scale)
            .onAppear { animateSequence() }
    }
}
```

Manually chained `withAnimation` calls glued together with guessed `DispatchQueue.asyncAfter` delay instead of `PhaseAnimator`. (Rules 1, 4)

## Dependencies

None.

## References

- [Apple Developer — PhaseAnimator](https://developer.apple.com/documentation/swiftui/phaseanimator)
- [Apple Developer — KeyframeAnimator](https://developer.apple.com/documentation/swiftui/keyframeanimator)
