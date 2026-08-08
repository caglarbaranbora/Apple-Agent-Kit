# Custom View Controller Transitions

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.uikit.custom-view-controller-transitions
artifact_type: knowledge
title: Custom View Controller Transitions
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the non-interactive custom presentation transition — the modalPresentationStyle .custom and weak transitioningDelegate that together arm it, the animator's obligation to add the presented view to the context's containerView because UIKit adds only the presenting one, the completeTransition(_:) call without which UIKit never finishes the presentation, the isAnimated check that must gate the animations, and the protocol's own rule that an animator object must not be interactive.
domain: UIKit
tags:
  - uikit
  - transitions
  - animation
  - presentation
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontrolleranimatedtransitioning
  - https://developer.apple.com/documentation/uikit/uiviewcontrollertransitioningdelegate
  - https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning
  - https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/containerview
  - https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/completetransition(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/transitioningdelegate
depends_on:
  - knowledge.uikit.modal-presentation
related:
  - knowledge.uikit.interactive-transitions
  - knowledge.uikit.uiview-animation
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent replaces a modal presentation's
animation with its own. Its central claim is that the animator is trusted
with two things UIKit will not do for it — putting the presented view into
the container, and declaring the transition over — and that omitting either
produces a stuck screen rather than a wrong animation.

## Scope

### Included

-   Arming a custom transition: `.custom`, `transitioningDelegate`, ownership
-   The animator's container and completion obligations
-   `isAnimated`, and the boundary against interactive transitions

### Excluded

-   Gesture-driven and cancellable transitions — see `interactive-transitions`
-   Presentation styles and dismissal — see `modal-presentation`; animating
    views inside a screen — see `uiview-animation`

## Rules

### Rule 1

Agents MUST set both `modalPresentationStyle = .custom` and
`transitioningDelegate` before presenting. Per Apple's documentation: "set
the presentation style to `UIModalPresentationStyle.custom` and assign your
transitioning delegate to the view controller's `transitioningDelegate`
property." Setting only the delegate leaves the system animation in place,
and the custom animator is never asked for.

### Rule 2

Agents MUST keep a strong reference to the transitioning delegate. It is
declared `weak var transitioningDelegate: (any
UIViewControllerTransitioningDelegate)?`, so a delegate created inline at the
assignment is gone before the presentation begins and the transition
silently reverts to the system's.

### Rule 3

Agents MUST add the presented view controller's view to
`transitionContext.containerView`. Per Apple's documentation: "UIKit sets
this view for you and automatically adds the view of the presenting view
controller to it. The animator object is responsible for adding the view of
the presented view controller." An animator that only sets an `alpha` or a
`transform` animates a view outside the hierarchy, so nothing changes.

### Rule 4

Agents MUST call `completeTransition(_:)` from the animation's completion
block, passing whether it finished. Per Apple's documentation: "You must
call this method after your animations have completed… The best place to
call this method is in the completion block of your animations." Without it
UIKit considers the transition still running: the presented controller gets
no appearance callbacks and the app accepts no further presentations.

### Rule 5

Agents MUST check `transitionContext.isAnimated` before building animations,
and MUST NOT make the animator interactive. Per Apple's documentation:
"always check the value returned by the `isAnimated` method to determine
whether you should create animations at all", and "the animations you create
using this protocol must not be interactive" — that needs a second object,
see `interactive-transitions`.

## Compliant Example

```swift
final class FadeAnimator: NSObject, UIViewControllerAnimatedTransitioning {
    func transitionDuration(using c: UIViewControllerContextTransitioning?) -> TimeInterval { 0.3 }

    func animateTransition(using context: UIViewControllerContextTransitioning) {
        guard let to = context.view(forKey: .to) else { return context.completeTransition(false) }
        context.containerView.addSubview(to)                              // Rule 3
        guard context.isAnimated else { return context.completeTransition(true) }  // Rule 5
        to.alpha = 0
        UIView.animate(withDuration: transitionDuration(using: context),
                       animations: { to.alpha = 1 },
                       completion: { context.completeTransition($0) })    // Rule 4
    }
}
```

## Non-Compliant Example

```swift
detail.transitioningDelegate = FadeTransitioningDelegate()
present(detail, animated: true)

func animateTransition(using context: UIViewControllerContextTransitioning) {
    let to = context.view(forKey: .to)!
    UIView.animate(withDuration: 0.3) { to.alpha = 1 }
}
```
The delegate is deallocated on assignment and `modalPresentationStyle` is
never set to `.custom`, so the system animation runs (Rules 1, 2). Reached,
the animator would fade a view it never added to the container (Rule 3) and
never complete, leaving UIKit mid-presentation (Rule 4).

## Dependencies

- `modal-presentation` -- it owns presenting a view controller and the
  standard styles; this one owns what replaces the animation between them.

## References

-   [Apple Developer — UIViewControllerAnimatedTransitioning](https://developer.apple.com/documentation/uikit/uiviewcontrolleranimatedtransitioning)
-   [Apple Developer — UIViewControllerTransitioningDelegate](https://developer.apple.com/documentation/uikit/uiviewcontrollertransitioningdelegate)
-   [Apple Developer — UIViewControllerContextTransitioning](https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning)
-   [Apple Developer — containerView](https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/containerview)
-   [Apple Developer — completeTransition(_:)](https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/completetransition(_:))
-   [Apple Developer — transitioningDelegate](https://developer.apple.com/documentation/uikit/uiviewcontroller/transitioningdelegate)
