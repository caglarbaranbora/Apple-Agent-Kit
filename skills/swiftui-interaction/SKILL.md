---
name: swiftui-interaction
description: Route SwiftUI Animation and Gesture implementation tasks to the correct Knowledge Contracts — implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, and GestureState. Use when writing or reviewing SwiftUI animation code, building custom transitions, implementing drag/pinch/rotate interactions, or combining multiple gestures on a view. This is implementation-code guidance (iOS 17+), not visual design — for when/why to animate or which gesture to use, see human-interface-guidelines. Triggers on withAnimation, .animation, AnyTransition, matchedGeometryEffect, Animatable, animatableData, PhaseAnimator, KeyframeAnimator, TapGesture, LongPressGesture, DragGesture, MagnifyGesture, RotateGesture, MagnificationGesture, RotationGesture, GestureState, simultaneously, sequenced, exclusively, highPriorityGesture, simultaneousGesture.
id: skill.swiftui.interaction
title: SwiftUI — Interaction (Animation & Gestures)
version: 1.0.0
status: Approved
artifact_type: skill
domain: SwiftUI
routes: [knowledge.swiftui.animation-modifiers, knowledge.swiftui.transitions, knowledge.swiftui.matched-geometry-effect, knowledge.swiftui.animatable-values, knowledge.swiftui.phase-and-keyframe-animators, knowledge.swiftui.tap-and-long-press-gestures, knowledge.swiftui.drag-gesture, knowledge.swiftui.magnification-and-rotation-gestures, knowledge.swiftui.gesture-composition, knowledge.swiftui.gesture-state]
related:
  - skill.swiftui.foundations
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-08
---

# SwiftUI — Interaction Skill

## Purpose

Route SwiftUI Animation and Gesture implementation-code tasks to the
minimum required Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/swiftui/.

-   Animation start/state -> animation-modifiers.md
-   View transitions -> transitions.md, matched-geometry-effect.md
-   Custom animatable values -> animatable-values.md
-   Multi-phase/keyframe animation -> phase-and-keyframe-animators.md
-   Tap/long-press -> tap-and-long-press-gestures.md
-   Drag -> drag-gesture.md
-   Pinch/rotate -> magnification-and-rotation-gestures.md
-   Combining gestures -> gesture-composition.md, gesture-state.md

Never load more than the contracts relevant to the specific question.
For Foundations topics (view/navigation/layout/state), route to
`skill.swiftui.foundations` instead. For visual/UX design questions
(when/why to animate, which gesture to use), route to
`skill.human-interface-guidelines.foundations` or
`skill.human-interface-guidelines.components`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/swiftui/ — do not guess or fall back to general
knowledge.

-   Previews and custom `Layout` protocol conformances — Excluded
-   Legacy `ObservableObject`/`NavigationView` migration — Deferred
-   `UIGestureRecognizer` and Core Animation — owned by `uikit`, in its
    `uikit-interaction` skill
-   Accessibility APIs — owned by `accessibility`
