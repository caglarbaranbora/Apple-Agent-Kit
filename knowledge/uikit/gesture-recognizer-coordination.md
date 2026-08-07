# Gesture Recognizer Coordination

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.gesture-recognizer-coordination
artifact_type: knowledge
title: Gesture Recognizer Coordination
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how two gesture recognizers competing for the same touch are resolved — the exclusive-by-default behaviour that makes a custom pan block a scroll view, the asymmetry by which returning true from shouldRecognizeSimultaneouslyWith is guaranteed while returning false is not, require(toFail:) as the ordering tool and the latency it buys with, its documented limit across view hierarchies, and the weak delegate reference that silently reverts every answer to its default.
domain: UIKit
tags:
  - uikit
  - gestures
  - delegate
  - interaction
references:
  - https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate
  - https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate/gesturerecognizer(_:shouldrecognizesimultaneouslywith:)
  - https://developer.apple.com/documentation/uikit/uigesturerecognizer/require(tofail:)
  - https://developer.apple.com/documentation/uikit/uigesturerecognizer/delegate
depends_on:
  - knowledge.uikit.gesture-recognizers
related:
  - knowledge.uikit.interactive-transitions
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent resolves two gesture
recognizers that want the same touch. Its central claim is that the
delegate's two answers are not symmetric: `true` decides the outcome, `false`
only declines to, so code returning `false` to enforce exclusivity is
expressing a preference the system may overrule.

## Scope

### Included

-   Exclusive-by-default recognition and opting a specific pair out of it
-   Ordering one recognizer behind another's failure; its cost, limits, and
    the delegate's ownership requirement

### Excluded

-   Attaching a recognizer and handling its states — see `gesture-recognizers`
-   Driving a transition from a gesture — see `interactive-transitions`
-   `UIScrollView`'s own pan and pinch as scrolling behaviour — Excluded

## Rules

### Rule 1

Agents MUST assume recognition is exclusive unless a delegate opts a pair
in. Per Apple's documentation, the default implementation of
`gestureRecognizer(_:shouldRecognizeSimultaneouslyWith:)` "returns
`false`—no two gestures can be recognized simultaneously." A custom pan
added over a `UIScrollView`'s content therefore stops the scroll rather than
riding alongside it, reported as a scroll view that "stopped working."

### Rule 2

Agents MUST NOT return `false` from that method to enforce exclusivity. Per
Apple's documentation: "returning `true` is guaranteed to allow simultaneous
recognition; returning `false`, on the other hand, is not guaranteed to
prevent simultaneous recognition because the other gesture recognizer's
delegate may return `true`." Exclusivity is expressed with Rule 3's failure
requirement, not with a negative delegate answer.

### Rule 3

Agents MUST use `require(toFail:)` when one recognizer should only act if
another does not — a single tap behind a double tap being the standard case.
Per Apple's documentation the relationship "delays the current gesture
recognizer's transition out of `UIGestureRecognizer.State.possible`": the
single tap fires only after the double-tap window elapses. That latency is
the price of the ordering, not a bug.

### Rule 4

Agents MUST NOT use `require(toFail:)` across view hierarchies or against
recognizers they do not own. Per Apple's documentation it "works fine when
gesture recognizers aren't created elsewhere in the app — or in a framework
— and the set of gesture recognizers remains the same. If you need to set up
failure requirements lazily or in different view hierarchies, use
`gestureRecognizer(_:shouldRequireFailureOf:)`… instead." A navigation
controller's interactive pop is the framework case.

### Rule 5

Agents MUST keep a strong reference to whatever object they assign as
`delegate`. The property is declared `weak var delegate: (any
UIGestureRecognizerDelegate)?`, so a helper created inline at the assignment
is deallocated immediately and every answer reverts to its default — Rule
1's exclusivity returns with no diagnostic.

## Compliant Example

```swift
final class PhotoViewController: UIViewController, UIGestureRecognizerDelegate {
    private lazy var pinch = UIPinchGestureRecognizer(target: self, action: #selector(zoom))
    private lazy var single = UITapGestureRecognizer(target: self, action: #selector(tap))
    private lazy var double = UITapGestureRecognizer(target: self, action: #selector(open))

    override func viewDidLoad() {
        super.viewDidLoad()
        double.numberOfTapsRequired = 2
        single.require(toFail: double)                                // Rule 3
        pinch.delegate = self                                         // Rule 5 — self is owned
        [pinch, single, double].forEach(scrollView.addGestureRecognizer)
    }

    func gestureRecognizer(_ g: UIGestureRecognizer,
                           shouldRecognizeSimultaneouslyWith o: UIGestureRecognizer) -> Bool {
        g === pinch && o === scrollView.panGestureRecognizer          // Rules 1, 2 — one pair
    }
}
```

## Non-Compliant Example

```swift
pinch.delegate = SimultaneousDelegate()

final class SimultaneousDelegate: NSObject, UIGestureRecognizerDelegate {
    func gestureRecognizer(_ g: UIGestureRecognizer,
                           shouldRecognizeSimultaneouslyWith o: UIGestureRecognizer) -> Bool { true }
}
```
The delegate is deallocated on the line that assigns it, so the method is
never called (Rule 5). Had it survived, the unconditional `true` opts every
recognizer into simultaneity with every other — the scroll view's pan, the
interactive pop — instead of naming one pair (Rules 1, 2).

## Dependencies

- `gesture-recognizers` -- it owns attaching a recognizer and reading its
  state; this one owns what happens when two of them collide.

## References

-   [Apple Developer — UIGestureRecognizerDelegate](https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate)
-   [Apple Developer — gestureRecognizer(_:shouldRecognizeSimultaneouslyWith:)](https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate/gesturerecognizer(_:shouldrecognizesimultaneouslywith:))
-   [Apple Developer — require(toFail:)](https://developer.apple.com/documentation/uikit/uigesturerecognizer/require(tofail:))
-   [Apple Developer — UIGestureRecognizer.delegate](https://developer.apple.com/documentation/uikit/uigesturerecognizer/delegate)
