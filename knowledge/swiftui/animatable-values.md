# Animatable Values

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.animatable-values
artifact_type: knowledge
title: Animatable Values
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when and how to conform a custom Shape or View to Animatable using animatableData and AnimatablePair for per-frame interpolation.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/animatable
  - https://developer.apple.com/documentation/swiftui/animatablepair
depends_on: []
related:
  - knowledge.swiftui.animation-modifiers
last_updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should conform a custom `Shape` or `View` to `Animatable`, and how to combine multiple animatable properties with `AnimatablePair`, as distinct from relying on built-in `.animation(_:value:)`.

## Scope

### Included

- The `Animatable` protocol and `animatableData` requirement
- `AnimatablePair` for combining two (or, nested, more) animatable values
- When custom interpolation is needed vs. when built-in modifier handles it

### Excluded

- Triggering built-in animatable modifiers — see `animation-modifiers.md`
- Multi-phase/keyframe animation — see `phase-and-keyframe-animators.md`

## Rules

### Rule 1

Agents MUST conform a custom `Shape` or `View` to `Animatable` (implementing `animatableData`) when it needs SwiftUI to interpolate a custom internal parameter (corner radius, progress fraction, path-defining value) frame-by-frame during animation — a plain stored property is not interpolated.

### Rule 2

Agents MUST back `animatableData` with a type conforming to `VectorArithmetic` — a custom struct without arithmetic operations cannot be interpolated.

### Rule 3

Agents MUST use `AnimatablePair` (nesting `AnimatablePair<A, AnimatablePair<B, C>>` for three+ values) to combine multiple independently animatable properties into single `animatableData` when they move together as one visual change. Don't animate each such property separately with unsynchronized `.animation(_:value:)`.

### Rule 4

Agents MUST NOT reach for custom `Animatable` conformance to animate a value that a built-in modifier (`.animation(_:value:)`, `.offset`, `.scaleEffect`) already animates correctly — custom conformance is only for custom-drawn `Shape`/`View` internals.

## Compliant Example

```swift
struct ProgressArc: Shape {
    var progress: Double // 0...1

    var animatableData: Double {
        get { progress }
        set { progress = newValue }
    }

    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.addArc(
            center: CGPoint(x: rect.midX, y: rect.midY),
            radius: rect.width / 2,
            startAngle: .degrees(-90),
            endAngle: .degrees(-90 + 360 * progress),
            clockwise: false
        )
        return path
    }
}
```

Custom `Shape` conforms to `Animatable` so `.animation(.linear, value: progress)` interpolates arc frame-by-frame. (Rules 1, 2)

## Non-Compliant Example

```swift
struct ProgressArc: Shape {
    var progress: Double // 0...1, not Animatable

    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.addArc(
            center: CGPoint(x: rect.midX, y: rect.midY),
            radius: rect.width / 2,
            startAngle: .degrees(-90),
            endAngle: .degrees(-90 + 360 * progress),
            clockwise: false
        )
        return path
    }
}
```

No `Animatable` conformance — wrapping in `.animation(_:value:)` snaps instantly between progress values instead of interpolating. (Rule 1)

## Dependencies

None.

## References

- [Apple Developer — Animatable](https://developer.apple.com/documentation/swiftui/animatable)
- [Apple Developer — AnimatablePair](https://developer.apple.com/documentation/swiftui/animatablepair)
