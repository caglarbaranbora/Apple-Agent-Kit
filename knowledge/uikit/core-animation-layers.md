# Core Animation Layers

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.uikit.core-animation-layers
artifact_type: knowledge
title: Core Animation Layers
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the model-versus-presentation-layer split that governs every CALayer animation — that the properties an agent sets are the model tree while presentation() returns the tree onscreen, that an explicit CAAnimation never writes the model so the layer snaps back on completion, why isRemovedOnCompletion and fillMode hide that snap instead of fixing it and leave hit testing on stale geometry, that a CABasicAnimation keyPath is an unchecked string, and that a view-backed layer's delegate belongs to the view.
domain: UIKit
tags:
  - uikit
  - core-animation
  - calayer
  - animation
references:
  - https://developer.apple.com/documentation/quartzcore/calayer
  - https://developer.apple.com/documentation/quartzcore/calayer/presentation()
  - https://developer.apple.com/documentation/quartzcore/cabasicanimation
  - https://developer.apple.com/documentation/quartzcore/caanimation
  - https://developer.apple.com/documentation/quartzcore/camediatiming
  - https://developer.apple.com/documentation/uikit/uiview/layer
depends_on: []
related:
  - knowledge.uikit.uiview-animation
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent animates a `CALayer`. Its
central claim is that a layer has two trees and an explicit animation writes
only one of them: the model layer keeps the value the agent assigned, the
presentation layer carries the value onscreen, and every classic Core
Animation defect — the snap-back, the stale hit test — is that split
showing.

## Scope

### Included

-   The model and presentation trees, and which one to read
-   Explicit `CAAnimation` vs. the underlying property value
-   `keyPath` correctness and a view-backed layer's delegate

### Excluded

-   `UIView.animate` and `UIViewPropertyAnimator` — see `uiview-animation`
-   View controller transition animations — see
    `custom-view-controller-transitions`
-   SwiftUI animation — owned by `swiftui`

## Rules

### Rule 1

Agents MUST read `presentation()` — not the layer itself — when they need
the value a layer currently shows. Per Apple's documentation it "provides a
close approximation of the layer that is currently being displayed onscreen.
While an animation is in progress, you can retrieve this object and use it
to get the current values for those animations." Reading `layer.position`
mid-animation returns the destination, which is why a drag that starts on a
moving view jumps.

### Rule 2

Agents MUST set the animated property to its final value in addition to
adding the `CAAnimation`. Adding an animation does not write the model
layer, so when the animation is removed on completion the layer renders its
unchanged model value and the view snaps back. The property assignment is
the state change; the animation only describes how the change is drawn.

### Rule 3

Agents MUST NOT use `isRemovedOnCompletion = false` with
`fillMode = .forwards` to make an animation appear to stick. That pair keeps
the presentation layer displaying the end value while the model layer still
holds the old one. Per Apple's documentation the presentation tree is
distinct — `hitTest(_:)` on a presentation layer "queries the layer objects
in the presentation tree (not the model tree)" — so ordinary hit testing and
layout keep using the stale geometry, and a control animated this way draws
in its new place and responds in its old one.

### Rule 4

Agents MUST verify that a `CABasicAnimation` `keyPath` names a real
animatable property. The initializer takes a `String` "specifying the key
path of the property to be animated in the render tree", so a typo or a
non-animatable name compiles and runs, producing silence rather than a
diagnostic. Compound paths such as `transform.scale.x` are valid; invented
ones are not.

### Rule 5

Agents MUST NOT assign a delegate to a `UIView`'s backing layer. Per Apple's
documentation: "If the layer object was created by a view, the view
typically assigns itself as the layer's delegate automatically, and you
should not change that relationship." Replacing it breaks the view's own
drawing and implicit-animation behaviour.

## Compliant Example

```swift
func slide(_ layer: CALayer, to end: CGPoint) {
    let start = layer.presentation()?.position ?? layer.position     // Rule 1
    let move = CABasicAnimation(keyPath: "position")                 // Rule 4
    move.fromValue = start
    move.toValue = end
    move.duration = 0.3
    layer.position = end                                             // Rule 2
    layer.add(move, forKey: "slide")
}
```
The model layer is moved, so hit testing, layout and any later read agree
with what is onscreen; the animation only describes the path between them.

## Non-Compliant Example

```swift
let move = CABasicAnimation(keyPath: "layerPosition")
move.toValue = end
move.duration = 0.3
move.fillMode = .forwards
move.isRemovedOnCompletion = false
layer.add(move, forKey: "slide")
```
`layerPosition` is not a property, so nothing animates and nothing reports
it (Rule 4). With the key path corrected, the layer would still never move
in the model tree (Rule 2); the fill/removal pair would hold the end frame
onscreen while taps continued to land at the old position (Rule 3).

## Dependencies

None.

## References

-   [Apple Developer — CALayer](https://developer.apple.com/documentation/quartzcore/calayer)
-   [Apple Developer — presentation()](https://developer.apple.com/documentation/quartzcore/calayer/presentation())
-   [Apple Developer — CABasicAnimation](https://developer.apple.com/documentation/quartzcore/cabasicanimation)
-   [Apple Developer — CAAnimation](https://developer.apple.com/documentation/quartzcore/caanimation)
-   [Apple Developer — CAMediaTiming](https://developer.apple.com/documentation/quartzcore/camediatiming)
-   [Apple Developer — UIView.layer](https://developer.apple.com/documentation/uikit/uiview/layer)
