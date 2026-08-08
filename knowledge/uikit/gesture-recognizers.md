# Gesture Recognizers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.gesture-recognizers
artifact_type: knowledge
title: Gesture Recognizers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how a UIGestureRecognizer is attached to the one view whose hit-tested touches it observes, the isUserInteractionEnabled default that silently disables recognizers on UILabel and UIImageView, the difference between a discrete recognizer that only reports .recognized and a continuous one that must be branched on state, the obligation to treat .cancelled as a terminal state alongside .ended, and the fact that a recognized gesture cancels the view's own touch delivery because the recognizer is not in the responder chain.
domain: UIKit
tags:
  - uikit
  - gestures
  - touch
  - interaction
references:
  - https://developer.apple.com/documentation/uikit/uigesturerecognizer
  - https://developer.apple.com/documentation/uikit/uigesturerecognizer/state-swift.enum
  - https://developer.apple.com/documentation/uikit/uiview/addgesturerecognizer(_:)
  - https://developer.apple.com/documentation/uikit/uipangesturerecognizer
  - https://developer.apple.com/documentation/uikit/uitapgesturerecognizer
depends_on: []
related:
  - knowledge.uikit.gesture-recognizer-coordination
  - knowledge.uikit.view-controller-lifecycle
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent attaches and handles a
`UIGestureRecognizer`. Its central claim is that a recognizer is bound to
exactly one view's hit-tested touches, and that its two most common failures
— attaching it to the wrong view, and reading `state` as though every
recognizer reported every state — both compile, install, and never fire.

## Scope

### Included

-   Attaching a recognizer, and the views on which it silently does nothing
-   Discrete vs. continuous recognizers and the `state` branch each requires
-   Terminal states, coordinate spaces, and the view's own cancelled touches

### Excluded

-   Two recognizers competing for one touch — see
    `gesture-recognizer-coordination`; driving a transition — see
    `interactive-transitions`
-   SwiftUI's `Gesture` types — owned by `swiftui`

## Rules

### Rule 1

Agents MUST attach the recognizer to the view whose touches it should
observe, with `addGestureRecognizer(_:)`. Per Apple's documentation: "A
gesture recognizer operates on touches hit-tested to a specific view and all
of that view's subviews. It thus must be associated with that view."
Attaching to a parent widens the gesture to the whole subtree.

### Rule 2

Agents MUST set `isUserInteractionEnabled = true` when attaching a
recognizer to a `UILabel`, `UIImageView`, or any other view that ships with
it off. The recognizer is added successfully and the handler is never
called, which reads as a broken recognizer rather than a disabled view.

### Rule 3

Agents MUST branch on `state` for a continuous recognizer and MUST NOT do
so for a discrete one. Per Apple's documentation, discrete recognizers
"recognize a discrete event such as a tap or a swipe but don't report
changes within the gesture… discrete gestures don't transition through the
Began and Changed states and they can't fail or be canceled." A `.began`
branch around a `UITapGestureRecognizer` is unreachable; an unbranched pan
handler runs its "gesture finished" logic on every touch move.

### Rule 4

Agents MUST treat `.cancelled` as terminal wherever they treat `.ended` as
terminal. A continuous gesture is cancelled when the system interrupts it —
an incoming call, a competing recognizer winning — and a handler that
commits state only in `.ended` leaves the view stranded mid-drag.

### Rule 5

Agents MUST pass an explicit view to `location(in:)` and `translation(in:)`
rather than assuming a coordinate space. These values are meaningless
without the view they are expressed in; passing the recognizer's own view
where the animated view's superview was meant produces a compounding offset.

## Compliant Example

```swift
final class CardViewController: UIViewController {
    private let card = UIView()

    override func viewDidLoad() {
        super.viewDidLoad()
        card.isUserInteractionEnabled = true                          // Rule 2
        card.addGestureRecognizer(UIPanGestureRecognizer(target: self, // Rule 1
                                                        action: #selector(didPan)))
    }

    @objc private func didPan(_ pan: UIPanGestureRecognizer) {
        switch pan.state {                                            // Rule 3
        case .changed:
            let t = pan.translation(in: card.superview)               // Rule 5
            card.transform = CGAffineTransform(translationX: t.x, y: t.y)
        case .ended, .cancelled:                                      // Rule 4
            UIView.animate(withDuration: 0.2) { self.card.transform = .identity }
        default:
            break
        }
    }
}
```

## Non-Compliant Example

```swift
label.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didTap)))

@objc private func didPan(_ pan: UIPanGestureRecognizer) {
    let t = pan.translation(in: view)
    card.center = CGPoint(x: card.center.x + t.x, y: card.center.y + t.y)
}
```
The tap never fires: `UILabel` ships with `isUserInteractionEnabled` off
(Rule 2). The pan handler runs its move on every state (Rule 3), never
releases on cancellation (Rule 4), and reads translation in the controller's
root view rather than the card's superview (Rule 5).

## Dependencies

None.

## References

-   [Apple Developer — UIGestureRecognizer](https://developer.apple.com/documentation/uikit/uigesturerecognizer)
-   [Apple Developer — UIGestureRecognizer.State](https://developer.apple.com/documentation/uikit/uigesturerecognizer/state-swift.enum)
-   [Apple Developer — addGestureRecognizer(_:)](https://developer.apple.com/documentation/uikit/uiview/addgesturerecognizer(_:))
-   [Apple Developer — UIPanGestureRecognizer](https://developer.apple.com/documentation/uikit/uipangesturerecognizer)
-   [Apple Developer — UITapGestureRecognizer](https://developer.apple.com/documentation/uikit/uitapgesturerecognizer)
