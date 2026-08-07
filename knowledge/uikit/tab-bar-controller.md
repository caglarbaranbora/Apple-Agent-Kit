# Tab Bar Controller

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.tab-bar-controller
artifact_type: knowledge
title: Tab Bar Controller
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UITabBarController and per-view-controller tabBarItem configuration to present sibling top-level screens behind a persistent tab bar.
domain: UIKit
tags:
  - uikit
  - navigation
  - tab-bar
references:
  - https://developer.apple.com/documentation/uikit/uitabbarcontroller
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/tabbaritem
depends_on: []
related:
  - knowledge.uikit.navigation-controller
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent assembles a
`UITabBarController`'s `viewControllers` array and configures each
child's `tabBarItem`, so top-level sibling screens are reachable behind a
persistent tab bar with correct icons and titles.

## Scope

### Included

-   Setting `viewControllers` on a `UITabBarController`
-   `tabBarItem` title/image per child, badge value
-   Embedding a `UINavigationController` per tab

### Excluded

-   Push/pop within a given tab's stack — see `navigation-controller`

## Rules

### Rule 1

Agents MUST set each child view controller's `tabBarItem` (title and
image) before assigning it into the `UITabBarController.viewControllers`
array — `UITabBarController` reads each child's own `tabBarItem` to build
the tab bar; an unset item shows a blank/untitled tab.

### Rule 2

Agents MUST wrap any tab whose content needs its own push/pop navigation
in a `UINavigationController` before adding it to `viewControllers` — the
tab bar controller does not provide stack navigation itself; embedding a
`UINavigationController` per tab is the standard way to get both a
persistent tab bar and per-tab navigation stacks.

### Rule 3

Agents MUST set `UITabBarController.viewControllers` in the exact order
tabs should appear left-to-right — the array order is the display order,
not the badge or selection order.

### Rule 4

Agents SHOULD use `tabBarItem.badgeValue` for a per-tab unread or
notification count instead of embedding a custom badge view —
`badgeValue` is the system-provided mechanism and matches platform
conventions automatically.

## Compliant Example

```swift
let inboxVC = UINavigationController(rootViewController: InboxViewController())
inboxVC.tabBarItem = UITabBarItem(title: "Inbox", image: UIImage(systemName: "tray"), tag: 0)

let settingsVC = UINavigationController(rootViewController: SettingsViewController())
settingsVC.tabBarItem = UITabBarItem(title: "Settings", image: UIImage(systemName: "gear"), tag: 1)

let tabBarController = UITabBarController()
tabBarController.viewControllers = [inboxVC, settingsVC]
```
Each tab wrapped in its own navigation controller with a configured `tabBarItem` before assignment. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
let tabBarController = UITabBarController()
tabBarController.viewControllers = [InboxViewController(), SettingsViewController()]
```
Neither child has a configured `tabBarItem` (both show blank tabs), and neither is wrapped in a navigation controller, so pushing a detail screen from either tab has no stack to push onto. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — UITabBarController](https://developer.apple.com/documentation/uikit/uitabbarcontroller)
-   [Apple Developer — tabBarItem](https://developer.apple.com/documentation/uikit/uiviewcontroller/tabbaritem)
