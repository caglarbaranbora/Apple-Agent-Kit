# Interactive Transitions

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.interactive-transitions
artifact_type: knowledge
title: Interactive Transitions
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the gesture-driven view controller transition — that it requires an animator object as well as an interaction controller, that the interaction controller must be vended only while a gesture is actually driving because a non-interactive dismissal otherwise stalls mid-transition, the mapping from gesture states to update(_:)/finish()/cancel(), the completeTransition(_:) call still owed on top of finish or cancel, and the super call every UIPercentDrivenInteractiveTransition override must begin with.
domain: UIKit
tags:
  - uikit
  - transitions
  - gestures
  - interaction
references:
  - https://developer.apple.com/documentation/uikit/uipercentdriveninteractivetransition
  - https://developer.apple.com/documentation/uikit/uiviewcontrollerinteractivetransitioning
  - https://developer.apple.com/documentation/uikit/uiviewcontrolleranimatedtransitioning
  - https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/completetransition(_:)
depends_on:
  - knowledge.uikit.custom-view-controller-transitions
  - knowledge.uikit.gesture-recognizers
related:
  - knowledge.uikit.gesture-recognizer-coordination
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent puts a gesture in control of a
view controller transition. Its central claim is that an interaction
controller is a promise to finish or cancel: once UIKit is handed one it
stops driving the transition and waits, so the failure mode is not a bad
animation but a screen frozen half-presented.

## Scope

### Included

-   Pairing an interaction controller with an animator, and when to vend it
-   Mapping gesture state to `update(_:)`, `finish()`, `cancel()`
-   Completion obligations and subclassing

### Excluded

-   The animator object itself — see `custom-view-controller-transitions`
-   Attaching and handling the driving gesture — see `gesture-recognizers`

## Rules

### Rule 1

Agents MUST provide an animator object alongside the interaction controller.
Per Apple's documentation: "To support an interactive view controller
transition, you must also provide a transition animator delegate… The
transition delegate and the transition animator can, if you wish, be defined
within a single custom class, but the class must adopt both protocols." The
interaction controller supplies timing only; it animates nothing.

### Rule 2

Agents MUST return the interaction controller from
`interactionControllerForDismissal(using:)` only while a gesture is actually
driving, and `nil` otherwise. Returning it unconditionally makes a
button-triggered dismissal interactive with nothing to advance it: UIKit
waits for a `finish()` or `cancel()` that no gesture will send. A stored
`isInteractive` flag set on `.began` and cleared on the gesture's terminal
state is the usual form.

### Rule 3

Agents MUST map the gesture's states onto the three progress calls. Per
Apple's documentation: "As user events arrive that would affect the progress
of a transition, call the `update(_:)`, `cancel()`, and `finish()` methods
to reflect the current progress. For example, you might call these methods
from a gesture recognizer to reflect how much of the gesture is completed."
`.changed` maps to `update(_:)`; `.ended` maps to `finish()` or `cancel()`
by threshold; `.cancelled` maps to `cancel()`.

### Rule 4

Agents MUST still call `completeTransition(_:)` from the animator. Per
Apple's documentation: "For interactive animations, you must call this
method in addition to the `finishInteractiveTransition()` or
`cancelInteractiveTransition()` method." Finishing reports the gesture's
outcome, completing reports that the animation stopped; UIKit needs both.

### Rule 5

Agents MUST begin every override in a `UIPercentDrivenInteractiveTransition`
subclass with a `super` call. Per Apple's documentation: "You can subclass
`UIPercentDrivenInteractiveTransition`, but if you do so you must start each
of your method overrides with a call to the `super` implementation of the
method."

## Compliant Example

```swift
final class DismissInteractor: UIPercentDrivenInteractiveTransition {
    private(set) var isInteractive = false                            // Rule 2
    @objc func handle(_ pan: UIPanGestureRecognizer, in vc: UIViewController) {
        let progress = pan.translation(in: vc.view).y / vc.view.bounds.height
        switch pan.state {                                            // Rule 3
        case .began:   isInteractive = true; vc.dismiss(animated: true)
        case .changed: update(progress)
        case .ended:   isInteractive = false; progress > 0.4 ? finish() : cancel()
        case .cancelled: isInteractive = false; cancel()
        default: break
        }
    }
}

func interactionControllerForDismissal(using a: UIViewControllerAnimatedTransitioning)
    -> UIViewControllerInteractiveTransitioning? {
    interactor.isInteractive ? interactor : nil                       // Rule 2
}
```

## Non-Compliant Example

```swift
func interactionControllerForDismissal(using a: UIViewControllerAnimatedTransitioning)
    -> UIViewControllerInteractiveTransitioning? { interactor }

@objc func handle(_ pan: UIPanGestureRecognizer) {
    interactor.update(pan.translation(in: view).y / view.bounds.height)
}
```
Every dismissal is interactive, including the close button's (Rule 2). The
handler never branches on state, so `finish()` and `cancel()` are never
called and the screen is left half-dismissed and unresponsive (Rule 3).

## Dependencies

- `custom-view-controller-transitions` -- it owns the animator object, the
  container, and `completeTransition(_:)`; this one owns only the timing.
- `gesture-recognizers` -- it owns the recognizer whose states Rule 3 maps.

## References

-   [Apple Developer — UIPercentDrivenInteractiveTransition](https://developer.apple.com/documentation/uikit/uipercentdriveninteractivetransition)
-   [Apple Developer — UIViewControllerInteractiveTransitioning](https://developer.apple.com/documentation/uikit/uiviewcontrollerinteractivetransitioning)
-   [Apple Developer — UIViewControllerAnimatedTransitioning](https://developer.apple.com/documentation/uikit/uiviewcontrolleranimatedtransitioning)
-   [Apple Developer — completeTransition(_:)](https://developer.apple.com/documentation/uikit/uiviewcontrollercontexttransitioning/completetransition(_:))
