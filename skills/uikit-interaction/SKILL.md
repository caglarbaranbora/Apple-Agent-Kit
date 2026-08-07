---
name: uikit-interaction
description: Route UIKit interaction, animation, transition, and SwiftUI-interop implementation tasks to the correct Knowledge Contracts — gesture recognizers and their coordination, Core Animation layers, UIView and property-animator animation, custom and interactive view controller transitions, and the UIViewRepresentable/UIHostingController boundary. Use when writing or reviewing code that adds a gesture to a UIKit view, animates a view or layer, replaces a modal presentation's animation, drives a dismissal from a pan, wraps a UIKit view for SwiftUI, or embeds a SwiftUI view in a UIKit screen. Screen scaffolding (lifecycle, Auto Layout, navigation, diffable lists) is out of scope here — see the uikit skill. Triggers on UIGestureRecognizer, UIPanGestureRecognizer, UITapGestureRecognizer, addGestureRecognizer, UIGestureRecognizerDelegate, shouldRecognizeSimultaneouslyWith, require(toFail:), CALayer, CABasicAnimation, presentation layer, isRemovedOnCompletion, fillMode, UIView.animate, UIViewPropertyAnimator, startAnimation, layoutIfNeeded, UIViewControllerAnimatedTransitioning, UIViewControllerTransitioningDelegate, transitioningDelegate, containerView, completeTransition, UIPercentDrivenInteractiveTransition, interactionControllerForDismissal, UIViewRepresentable, UIViewControllerRepresentable, makeCoordinator, updateUIView, UIHostingController, rootView, sizingOptions, safeAreaRegions.
id: skill.uikit.interaction
title: UIKit — Interaction (Gestures, Animation, Transitions, Interop)
version: 0.1.0
status: Draft
artifact_type: skill
domain: UIKit
routes: [knowledge.uikit.gesture-recognizers, knowledge.uikit.gesture-recognizer-coordination, knowledge.uikit.core-animation-layers, knowledge.uikit.uiview-animation, knowledge.uikit.custom-view-controller-transitions, knowledge.uikit.interactive-transitions, knowledge.uikit.swiftui-view-representable, knowledge.uikit.swiftui-hosting-controller]
related:
  - skill.uikit.foundations
  - skill.swiftui.foundations
  - skill.swiftui.interaction
last_updated: 2026-08-08
---

# UIKit — Interaction Skill

## Purpose

Route the UIKit tasks that act on a screen that already exists — touch
handling, animation, the transition between two screens, and the boundary
where UIKit and SwiftUI meet — to the minimum required UIKit Knowledge
Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/uikit/.

-   Touch -> gesture-recognizers.md (attaching, state, coordinate spaces), gesture-recognizer-coordination.md (delegate, simultaneous recognition, require(toFail:))
-   Animation -> uiview-animation.md (UIView.animate, UIViewPropertyAnimator, animating constraints), core-animation-layers.md (CALayer, CABasicAnimation, presentation vs model layer)
-   Transitions -> custom-view-controller-transitions.md (animator object, containerView, completeTransition), interactive-transitions.md (UIPercentDrivenInteractiveTransition, gesture-driven dismissal)
-   SwiftUI interop -> swiftui-view-representable.md (UIViewRepresentable, Coordinator), swiftui-hosting-controller.md (UIHostingController, sizingOptions, safeAreaRegions)

Never load more than the contracts relevant to the specific question.
For view controller lifecycle, Auto Layout, navigation, and diffable
lists, route to `skill.uikit.foundations` instead. For animation and
gestures written in SwiftUI rather than UIKit, route to
`skill.swiftui.interaction` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/uikit/ — do not guess or fall back to general
knowledge.

-   When to animate, and which gesture a control should use — owned by
    `human-interface-guidelines`
-   Accessibility of a custom gesture or an animation preference such as
    Reduce Motion — owned by `accessibility`
-   `UIViewPropertyAnimator` as a scroll-linked scrubbing engine, Metal or
    `CAEmitterLayer` effects, and `UIKit Dynamics` — Excluded
-   Storyboard segues and `IBAction`-driven transitions — Excluded
