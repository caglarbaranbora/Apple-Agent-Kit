# View Controller Lifecycle

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.view-controller-lifecycle
artifact_type: knowledge
title: View Controller Lifecycle
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct placement of setup and teardown work across UIViewController's viewDidLoad, viewWillAppear, viewDidAppear, viewWillDisappear, and viewDidDisappear.
domain: UIKit
tags:
  - uikit
  - view-controller
  - lifecycle
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidload()
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwillappear(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidappear(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwilldisappear(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdiddisappear(_:)
depends_on: []
related:
  - knowledge.uikit.auto-layout-constraints
  - knowledge.uikit.view-controller-composition
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent places one-time setup work,
per-appearance refresh work, animation-dependent work, and cleanup work
across `UIViewController`'s lifecycle methods, so view controllers don't
duplicate work or start/stop resources at the wrong time.

## Scope

### Included

-   One-time view hierarchy/constraint setup in `viewDidLoad()`
-   State refresh that must happen every appearance in `viewWillAppear(_:)`
-   Starting animations/timers/live updates in `viewDidAppear(_:)`
-   Pausing/stopping work in `viewWillDisappear(_:)`/`viewDidDisappear(_:)`

### Excluded

-   Child view controller add/remove — see `view-controller-composition`
-   Auto Layout constraint authoring — see `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST perform one-time view hierarchy construction and constraint
setup in `viewDidLoad()`, not in `viewWillAppear(_:)` — `viewDidLoad()`
runs exactly once per view controller instance; repeating it in an appear
method wastes work and can duplicate subviews on every appearance.

### Rule 2

Agents MUST refresh data-dependent UI state (a value that may have
changed while this screen was off-screen) in `viewWillAppear(_:)`, not
`viewDidLoad()` — `viewDidLoad()` only runs once, so state changed by
another screen would never be reflected on return.

### Rule 3

Agents MUST start animations, timers, or other work that requires the
view to already be in the window hierarchy in `viewDidAppear(_:)`, never
in `viewWillAppear(_:)` — the view isn't guaranteed to be in the window
yet at `viewWillAppear`, so animations timed against it can be dropped or
glitch.

### Rule 4

Agents MUST stop timers, remove notification observers, and pause
ongoing work started in `viewDidAppear(_:)` inside `viewWillDisappear(_:)`
(or `viewDidDisappear(_:)`) — leaving them running after the view leaves
the screen wastes resources and can update UI that's no longer visible.

### Rule 5

Agents MUST call the corresponding `super` lifecycle method first, before
doing any subclass work in the override — per Apple's documented override
contract, so the base class's own setup runs before the subclass depends
on it.

## Compliant Example

```swift
final class ProfileViewController: UIViewController {
    private let nameLabel = UILabel()
    private var refreshTimer: Timer?

    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(nameLabel)
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        nameLabel.text = currentUser.name
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        refreshTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.reloadStatus()
        }
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        refreshTimer?.invalidate()
        refreshTimer = nil
    }
}
```
One-time setup in `viewDidLoad`, per-appearance refresh in `viewWillAppear`, timer started only once visible and stopped on disappearance. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
final class ProfileViewController: UIViewController {
    private let nameLabel = UILabel()

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        view.addSubview(nameLabel)
        nameLabel.text = currentUser.name
    }
}
```
Subview construction runs on every appearance instead of once, duplicating the label into the view hierarchy on a second visit. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — viewDidLoad()](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidload())
-   [Apple Developer — viewWillAppear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwillappear(_:))
-   [Apple Developer — viewDidAppear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidappear(_:))
-   [Apple Developer — viewWillDisappear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwilldisappear(_:))
-   [Apple Developer — viewDidDisappear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdiddisappear(_:))
