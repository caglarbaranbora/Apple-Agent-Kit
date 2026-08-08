# UIKit — Interaction

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.uikit-interaction
artifact_type: reference
title: UIKit — Interaction
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for the Apple documentation behind skill.uikit.interaction -- gesture recognizers and their coordination, Core Animation layers, UIView and property-animator animation, custom and interactive view controller transitions, and UIKit-SwiftUI interop through UIViewRepresentable and UIHostingController.
domain: UIKit — Interaction
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/quartzcore/caanimation
https://developer.apple.com/documentation/quartzcore/cabasicanimation
https://developer.apple.com/documentation/quartzcore/calayer
https://developer.apple.com/documentation/quartzcore/calayer/presentation()
https://developer.apple.com/documentation/quartzcore/camediatiming
https://developer.apple.com/documentation/swiftui/uihostingcontroller
https://developer.apple.com/documentation/swiftui/uihostingcontroller/rootview
https://developer.apple.com/documentation/swiftui/uihostingcontroller/safearearegions
https://developer.apple.com/documentation/swiftui/uihostingcontroller/sizingoptions
https://developer.apple.com/documentation/swiftui/uiviewcontrollerrepresentable
https://developer.apple.com/documentation/swiftui/uiviewrepresentable
https://developer.apple.com/documentation/swiftui/uiviewrepresentable/makecoordinator()
https://developer.apple.com/documentation/swiftui/uiviewrepresentable/updateuiview(_:context:)
https://developer.apple.com/documentation/swiftui/uiviewrepresentablecontext
https://developer.apple.com/documentation/uikit/nslayoutconstraint/constant
https://developer.apple.com/documentation/uikit/uigesturerecognizer
https://developer.apple.com/documentation/uikit/uigesturerecognizer/delegate
https://developer.apple.com/documentation/uikit/uigesturerecognizer/require(tofail:)
https://developer.apple.com/documentation/uikit/uigesturerecognizer/state-swift.enum
https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate
https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate/gesturerecognizer(_:shouldrecognizesimultaneouslywith:)
https://developer.apple.com/documentation/uikit/uipangesturerecognizer
https://developer.apple.com/documentation/uikit/uipercentdriveninteractivetransition
https://developer.apple.com/documentation/uikit/uitapgesturerecognizer
https://developer.apple.com/documentation/uikit/uiview/addgesturerecognizer(_:)
https://developer.apple.com/documentation/uikit/uiview/animate(withduration:animations:)
https://developer.apple.com/documentation/uikit/uiview/layer
https://developer.apple.com/documentation/uikit/uiview/layoutifneeded()
https://developer.apple.com/documentation/uikit/uiviewanimating/startanimation()
https://developer.apple.com/documentation/uikit/uiviewcontroller/transitioningdelegate
https://developer.apple.com/documentation/uikit/uiviewcontrolleranimatedtransitioning
https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning
https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/completetransition(_:)
https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/containerview
https://developer.apple.com/documentation/uikit/uiviewcontrollerinteractivetransitioning
https://developer.apple.com/documentation/uikit/uiviewcontrollertransitioningdelegate
https://developer.apple.com/documentation/uikit/uiviewpropertyanimator

## Purpose

Reference index for the Apple documentation behind
`skill.uikit.interaction` — what a UIKit screen does once it exists:
responds to touch, animates, transitions between screens, and hosts or is
hosted by SwiftUI. Screen scaffolding (view controller lifecycle and
composition, Auto Layout, navigation, diffable table and collection views)
is indexed separately by `reference.apple.uikit`, whose 34 sources reached
the 98-line cap; splitting the Skill in two was the only way to index this
surface without raising it, per reference-spec.md.

Core Animation lives in QuartzCore and the interop protocols live in
SwiftUI, so this Reference indexes three frameworks: they are the sources
one Skill routes to, not one framework's documentation.

## Primary Topics

- Gesture recognition: `UIGestureRecognizer`, its state machine and delegate
- Recognizer coordination: simultaneous recognition, failure requirements
- Core Animation: `CALayer`, `CABasicAnimation`, the presentation tree
- View animation: `UIView.animate`, `UIViewPropertyAnimator`
- Custom transitions: animator objects, the transitioning context
- Interactive transitions: `UIPercentDrivenInteractiveTransition`
- SwiftUI interop: `UIViewRepresentable`, `UIHostingController`

## Used By

- knowledge/uikit/gesture-recognizers.md ([[knowledge/uikit/gesture-recognizers]])
- knowledge/uikit/gesture-recognizer-coordination.md ([[knowledge/uikit/gesture-recognizer-coordination]])
- knowledge/uikit/core-animation-layers.md ([[knowledge/uikit/core-animation-layers]])
- knowledge/uikit/uiview-animation.md ([[knowledge/uikit/uiview-animation]])
- knowledge/uikit/custom-view-controller-transitions.md ([[knowledge/uikit/custom-view-controller-transitions]])
- knowledge/uikit/interactive-transitions.md ([[knowledge/uikit/interactive-transitions]])
- knowledge/uikit/swiftui-view-representable.md ([[knowledge/uikit/swiftui-view-representable]])
- knowledge/uikit/swiftui-hosting-controller.md ([[knowledge/uikit/swiftui-hosting-controller]])
