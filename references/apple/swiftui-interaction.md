# SwiftUI — Interaction

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.swiftui-interaction
artifact_type: reference
title: SwiftUI — Interaction
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for the Apple SwiftUI documentation behind skill.swiftui.interaction -- implicit and explicit animation, timing curves, view transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator and KeyframeAnimator, tap/long-press/drag/magnification/rotation gestures, gesture composition, and GestureState.
domain: SwiftUI — Interaction
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/swiftui
https://developer.apple.com/documentation/swiftui/animatable
https://developer.apple.com/documentation/swiftui/animatablepair
https://developer.apple.com/documentation/swiftui/anytransition
https://developer.apple.com/documentation/swiftui/draggesture
https://developer.apple.com/documentation/swiftui/draggesture/value
https://developer.apple.com/documentation/swiftui/gesture/exclusively(before:)
https://developer.apple.com/documentation/swiftui/gesture/sequenced(before:)
https://developer.apple.com/documentation/swiftui/gesture/simultaneously(with:)
https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:)
https://developer.apple.com/documentation/swiftui/gesturestate
https://developer.apple.com/documentation/swiftui/keyframeanimator
https://developer.apple.com/documentation/swiftui/longpressgesture
https://developer.apple.com/documentation/swiftui/magnificationgesture
https://developer.apple.com/documentation/swiftui/magnifygesture
https://developer.apple.com/documentation/swiftui/namespace
https://developer.apple.com/documentation/swiftui/phaseanimator
https://developer.apple.com/documentation/swiftui/rotategesture
https://developer.apple.com/documentation/swiftui/rotationgesture
https://developer.apple.com/documentation/swiftui/tapgesture
https://developer.apple.com/documentation/swiftui/view/animation(_:value:)
https://developer.apple.com/documentation/swiftui/view/gesture(_:including:)
https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:)
https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)
https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:)
https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:)
https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:)
https://developer.apple.com/documentation/swiftui/view/transition(_:)
https://developer.apple.com/documentation/swiftui/withanimation(_:_:)
https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:)

## Purpose

Reference index for the Apple SwiftUI documentation behind `skill.swiftui.interaction` — animation and gestures, targeting iOS 17+ APIs. Views, navigation, layout, and state-management sources are indexed by `references/apple/swiftui.md` ([[references/apple/swiftui]]), which backs `skill.swiftui.foundations`. The two Skills were split on topical coherence before their References were; this file completes that split, which `docs/specifications/reference-spec.md` requires ("One Reference per Skill-scoped domain").

Both the pre-iOS-17 and iOS-17+ spellings of the magnification and rotation gestures are indexed, because the older `MagnificationGesture`/`RotationGesture` are what existing code contains and the deprecation is what an agent must recognise.

## Primary Topics

- Animation: implicit `.animation(_:value:)`, explicit `withAnimation`, and completion criteria
- Transitions: `AnyTransition` and `.transition(_:)`
- Geometry matching: `matchedGeometryEffect` and the `Namespace` it requires
- Custom animatable values: the `Animatable` protocol and `AnimatablePair`
- Multi-step animation: `PhaseAnimator` and `KeyframeAnimator`
- Gestures: tap, long-press, drag, magnification, and rotation, in both their current and deprecated spellings
- Gesture composition: `simultaneously`, `sequenced`, `exclusively`, `highPriorityGesture`, `simultaneousGesture`
- Transient gesture state: `GestureState` and `updating(_:body:)`

## Used By

- knowledge/swiftui/animation-modifiers.md ([[knowledge/swiftui/animation-modifiers]])
- knowledge/swiftui/transitions.md ([[knowledge/swiftui/transitions]])
- knowledge/swiftui/matched-geometry-effect.md ([[knowledge/swiftui/matched-geometry-effect]])
- knowledge/swiftui/animatable-values.md ([[knowledge/swiftui/animatable-values]])
- knowledge/swiftui/phase-and-keyframe-animators.md ([[knowledge/swiftui/phase-and-keyframe-animators]])
- knowledge/swiftui/tap-and-long-press-gestures.md ([[knowledge/swiftui/tap-and-long-press-gestures]])
- knowledge/swiftui/drag-gesture.md ([[knowledge/swiftui/drag-gesture]])
- knowledge/swiftui/magnification-and-rotation-gestures.md ([[knowledge/swiftui/magnification-and-rotation-gestures]])
- knowledge/swiftui/gesture-composition.md ([[knowledge/swiftui/gesture-composition]])
- knowledge/swiftui/gesture-state.md ([[knowledge/swiftui/gesture-state]])
