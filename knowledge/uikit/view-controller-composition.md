# View Controller Composition

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.view-controller-composition
type: knowledge
title: View Controller Composition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the child view controller container pattern — addChild(_:), view hierarchy insertion, and didMove(toParent:)/willMove(toParent:) — for embedding one view controller's content inside another.
domain: UIKit
tags:
  - uikit
  - view-controller
  - composition
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/didmove(toparent:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/willmove(toparent:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/removefromparent()
depends_on: []
related:
  - knowledge.uikit.navigation-controller
  - knowledge.uikit.tab-bar-controller
  - knowledge.uikit.view-controller-lifecycle
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent embeds a child view
controller's view inside a parent so both view controllers' lifecycles
and event forwarding stay correct, instead of adding a child's view as a
bare subview with no containment relationship.

## Scope

### Included

-   `addChild(_:)` + view hierarchy insertion + `didMove(toParent:)` sequence
-   Removing a child view controller (`willMove(toParent: nil)` + `removeFromParent()`)

### Excluded

-   `UINavigationController`/`UITabBarController` (system containers) — see `navigation-controller`, `tab-bar-controller`

## Rules

### Rule 1

Agents MUST call `addChild(_:)` on the parent before adding the child's
`view` as a subview — adding the view first without registering
containment breaks the child's `parent`/`didMove` lifecycle callbacks and
any layout-guide/trait propagation the system provides to properly
contained children.

### Rule 2

Agents MUST call `child.didMove(toParent: self)` immediately after adding
the child's view to the parent's view hierarchy — this is Apple's
documented completion step of the containment sequence; skipping it
leaves the child view controller unaware it's now installed.

### Rule 3

Agents MUST call `child.willMove(toParent: nil)` before removing a
child's view from the hierarchy, and `child.removeFromParent()` after —
in that order — so the child gets a chance to react before removal and
the parent-child relationship is torn down cleanly afterward.

### Rule 4

Agents MUST set the child's view `frame` (or constraints) explicitly
after insertion — a child view controller's view has no inherent size or
position in the parent; forgetting this produces a zero-frame or
misplaced child view.

## Compliant Example

```swift
final class DashboardViewController: UIViewController {
    private let summaryVC = SummaryViewController()

    override func viewDidLoad() {
        super.viewDidLoad()
        addChild(summaryVC)
        view.addSubview(summaryVC.view)
        summaryVC.view.frame = view.bounds
        summaryVC.didMove(toParent: self)
    }

    func removeSummary() {
        summaryVC.willMove(toParent: nil)
        summaryVC.view.removeFromSuperview()
        summaryVC.removeFromParent()
    }
}
```
Full four-step containment sequence on install; correctly ordered teardown on removal. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
final class DashboardViewController: UIViewController {
    private let summaryVC = SummaryViewController()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(summaryVC.view)
    }
}
```
The child's view is added directly without `addChild(_:)` or `didMove(toParent:)` — `summaryVC.parent` stays `nil` and the child never receives correct containment callbacks. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — addChild(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:))
-   [Apple Developer — didMove(toParent:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/didmove(toparent:))
-   [Apple Developer — willMove(toParent:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/willmove(toparent:))
-   [Apple Developer — removeFromParent()](https://developer.apple.com/documentation/uikit/uiviewcontroller/removefromparent())
