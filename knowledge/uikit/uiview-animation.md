# UIView Animation

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.uiview-animation
artifact_type: knowledge
title: UIView Animation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the view-level animation APIs — the UIViewPropertyAnimator that runs nothing until startAnimation() is called, the requirement to set final values on animatable properties rather than deltas, the Auto Layout rule that a constrained view is animated by changing constraint constants and calling layoutIfNeeded inside the block rather than by animating frame, the disabling of user interaction on views under animation, and the interruptibility that decides between UIView.animate and a property animator.
domain: UIKit
tags:
  - uikit
  - animation
  - uiview
  - auto-layout
references:
  - https://developer.apple.com/documentation/uikit/uiview/animate(withduration:animations:)
  - https://developer.apple.com/documentation/uikit/uiviewpropertyanimator
  - https://developer.apple.com/documentation/uikit/uiviewanimating/startanimation()
  - https://developer.apple.com/documentation/uikit/uiview/layoutifneeded()
  - https://developer.apple.com/documentation/uikit/nslayoutconstraint/constant
depends_on: []
related:
  - knowledge.uikit.core-animation-layers
  - knowledge.uikit.auto-layout-constraints
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent animates a `UIView`. Its
central claim is that the two most common failures are silent in opposite
directions: a property animator that is never started does nothing at all,
and a `frame` animation on a constrained view plays correctly and is then
undone by the next layout pass.

## Scope

### Included

-   Starting a `UIViewPropertyAnimator`, and choosing it over `UIView.animate`
-   Final values, animatable properties, and animating Auto Layout
-   User interaction during an animation

### Excluded

-   `CALayer` and explicit `CAAnimation` — see `core-animation-layers`
-   View controller transitions — see `custom-view-controller-transitions`
-   Which constraints to write in the first place — see
    `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST call `startAnimation()` on a `UIViewPropertyAnimator` built with
an initializer. Per Apple's documentation: "If you create your animator
using one of the standard initialization methods, you must explicitly start
your animations by calling the `startAnimation()` method. If you want to
start the animations immediately after the creation of your animator, use
the `runningPropertyAnimator(withDuration:delay:options:animations:completion:)`
method instead of the standard initializers." An unstarted animator is a
live object holding an unrun block, so nothing is logged.

### Rule 2

Agents MUST assign final values to animatable properties inside the block.
Per Apple's documentation: "In your animation blocks, set the value of an
animatable property to the final value you want reflected by that view", and
the animator "operates on animatable properties of views, such as the
`frame`, `center`, `alpha`, and `transform` properties." A non-animatable
property changed in the block — `isHidden`, a label's `text` — takes effect
at once, so it appears to have no animation rather than an unsupported one.

### Rule 3

Agents MUST animate a constrained view by changing constraint `constant`
values before the block and calling `layoutIfNeeded()` inside it, and MUST
NOT animate its `frame`. Auto Layout recomputes frames on the next layout
pass, so a frame animation on a constrained view completes and is then
reverted — the animation is seen, the result is not.

### Rule 4

Agents MUST pass `.allowUserInteraction` when a view must stay tappable
mid-animation. Per Apple's documentation: "During an animation, user
interactions are temporarily disabled for the views being animated." A tap
during a long fade is discarded, which reads as an unresponsive control
rather than a suppressed one.

### Rule 5

Agents MUST use `UIViewPropertyAnimator` rather than `UIView.animate` when
the animation must be paused, reversed, or scrubbed. Only the animator
exposes `fractionComplete`, `isReversed`, and `pauseAnimation()`; an
interactive gesture driving a `UIView.animate` call has nothing to drive,
which is why such code re-runs the whole animation on every gesture update.

## Compliant Example

```swift
final class PanelViewController: UIViewController {
    private var heightConstraint: NSLayoutConstraint!
    private var animator: UIViewPropertyAnimator?

    func expand() {
        heightConstraint.constant = 320                              // Rule 3
        let a = UIViewPropertyAnimator(duration: 0.35, dampingRatio: 0.8) {
            self.view.layoutIfNeeded()                               // Rule 3
            self.panel.alpha = 1                                     // Rule 2
        }
        a.startAnimation()                                           // Rule 1
        animator = a                                                 // Rule 5
    }
}
```

## Non-Compliant Example

```swift
func expand() {
    UIViewPropertyAnimator(duration: 0.35, curve: .easeOut) {
        self.panel.frame.size.height = 320
        self.panel.isHidden = false
    }
}
```
The animator is created and discarded without `startAnimation()`, so no
frame is ever drawn (Rule 1). Started, it would animate `frame` on a view
Auto Layout owns and lose the change at the next pass (Rule 3), and
`isHidden` would flip instantly rather than animate (Rule 2).

## Dependencies

None.

## References

-   [Apple Developer — animate(withDuration:animations:)](https://developer.apple.com/documentation/uikit/uiview/animate(withduration:animations:))
-   [Apple Developer — UIViewPropertyAnimator](https://developer.apple.com/documentation/uikit/uiviewpropertyanimator)
-   [Apple Developer — startAnimation()](https://developer.apple.com/documentation/uikit/uiviewanimating/startanimation())
-   [Apple Developer — layoutIfNeeded()](https://developer.apple.com/documentation/uikit/uiview/layoutifneeded())
-   [Apple Developer — NSLayoutConstraint.constant](https://developer.apple.com/documentation/uikit/nslayoutconstraint/constant)
