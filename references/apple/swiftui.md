# SwiftUI

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.swiftui
artifact_type: reference
title: SwiftUI
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's SwiftUI framework documentation, implementation-conventions scope (Views, Navigation, Layout, State management,.
domain: SwiftUI
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/swiftui

## Purpose

Reference index for Apple's SwiftUI framework documentation,
implementation-conventions scope (Views, Navigation, Layout, State
management, Animation, Gestures), targeting iOS 17+ APIs. Visual/UX
design guidance for what a screen should look like is owned by
`human-interface-guidelines`, not this domain — see
docs/architecture/domain-map.md Cross-Domain Notes. Previews and custom
`Layout` protocol conformances are out of scope for this pass.

## Primary Topics

- View composition and ViewBuilder
- View identity (ForEach/List, Identifiable)
- Modifier order and view wrapping
- NavigationStack and NavigationPath
- NavigationSplitView
- Stacks and spacing (VStack/HStack/ZStack)
- Safe area (safeAreaInset, ignoresSafeArea)
- Lazy grids and lazy stacks
- GeometryReader
- State and Binding
- The Observable macro
- Environment values
- Implicit/explicit animation and timing curves
- View transitions
- matchedGeometryEffect
- The Animatable protocol
- PhaseAnimator and KeyframeAnimator
- Tap and long-press gestures
- Drag gesture
- Magnification and rotation gestures
- Gesture composition
- GestureState

## Used By

- knowledge/swiftui/view-composition.md ([[knowledge/swiftui/view-composition]])
- knowledge/swiftui/view-identity.md ([[knowledge/swiftui/view-identity]])
- knowledge/swiftui/modifier-order.md ([[knowledge/swiftui/modifier-order]])
- knowledge/swiftui/navigation-stack.md ([[knowledge/swiftui/navigation-stack]])
- knowledge/swiftui/navigation-split-view.md ([[knowledge/swiftui/navigation-split-view]])
- knowledge/swiftui/stacks-and-spacing.md ([[knowledge/swiftui/stacks-and-spacing]])
- knowledge/swiftui/safe-area.md ([[knowledge/swiftui/safe-area]])
- knowledge/swiftui/lazy-grids.md ([[knowledge/swiftui/lazy-grids]])
- knowledge/swiftui/geometry-reader-anti-pattern.md ([[knowledge/swiftui/geometry-reader-anti-pattern]])
- knowledge/swiftui/state-and-binding.md ([[knowledge/swiftui/state-and-binding]])
- knowledge/swiftui/observable-macro.md ([[knowledge/swiftui/observable-macro]])
- knowledge/swiftui/environment-values.md ([[knowledge/swiftui/environment-values]])
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
