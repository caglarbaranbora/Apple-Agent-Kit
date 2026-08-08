# Navigation Controller

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.uikit.navigation-controller
artifact_type: knowledge
title: Navigation Controller
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of UINavigationController push/pop navigation and navigationItem configuration for a stack-based UIKit screen flow.
domain: UIKit
tags:
  - uikit
  - navigation
  - navigation-controller
references:
  - https://developer.apple.com/documentation/uikit/uinavigationcontroller
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/navigationitem
depends_on: []
related:
  - knowledge.uikit.tab-bar-controller
  - knowledge.uikit.modal-presentation
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent pushes and pops screens
onto a `UINavigationController` stack and configures each screen's
`navigationItem`, so back navigation and bar content behave correctly
without manual view controller stacking.

## Scope

### Included

-   `pushViewController(_:animated:)`/`popViewController(animated:)`/`popToRootViewController(animated:)`
-   `navigationItem.title`, `backButtonTitle`, `leftBarButtonItem`/`rightBarButtonItem`

### Excluded

-   Modal present/dismiss — see `modal-presentation`
-   `UITabBarController` — see `tab-bar-controller`

## Rules

### Rule 1

Agents MUST push a new screen onto an existing `UINavigationController`
stack with `navigationController?.pushViewController(_:animated:)`
rather than presenting it modally, whenever the new screen is a
drill-down/detail continuation of the current stack — pushing preserves
the back-stack and the standard back-swipe gesture; modal presentation
does not.

### Rule 2

Agents MUST set `navigationItem.title` (or a custom `titleView`) on each
pushed view controller rather than on the navigation controller itself —
`UINavigationController` displays whichever pushed view controller's own
`navigationItem` is currently on top; setting a title on the navigation
controller has no per-screen effect.

### Rule 3

Agents SHOULD set `navigationItem.backButtonTitle` when the previous
screen's title is too long or unsuitable as a back-button label — the
default back button title is the *previous* screen's `title`, which can
be visually cramped.

### Rule 4

Agents MUST NOT call `popViewController(animated:)` from a view
controller that is not currently the top of the navigation stack —
popping from a non-top controller is undefined/no-op behavior; pop is
only valid from the currently visible screen.

## Compliant Example

```swift
final class InboxViewController: UIViewController {
    func showDetail(for message: Message) {
        let detailVC = MessageDetailViewController(message: message)
        detailVC.navigationItem.title = message.subject
        navigationController?.pushViewController(detailVC, animated: true)
    }
}
```
Push (not modal present) for a drill-down detail screen; title set on the pushed controller's own `navigationItem`. (Rules 1, 2)

## Non-Compliant Example

```swift
final class InboxViewController: UIViewController {
    func showDetail(for message: Message) {
        let detailVC = MessageDetailViewController(message: message)
        title = message.subject
        present(detailVC, animated: true)
    }
}
```
Modal `present` used for a drill-down continuation (loses the back-swipe/back-stack), and the title is set on the wrong view controller (`self`, not `detailVC`). (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — UINavigationController](https://developer.apple.com/documentation/uikit/uinavigationcontroller)
-   [Apple Developer — navigationItem](https://developer.apple.com/documentation/uikit/uiviewcontroller/navigationitem)
