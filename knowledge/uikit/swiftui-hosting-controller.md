# SwiftUI Hosting Controller

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.swiftui-hosting-controller
artifact_type: knowledge
title: SwiftUI Hosting Controller
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how SwiftUI content is embedded in a UIKit hierarchy through UIHostingController — that it is a view controller and must be installed with the containment sequence rather than by adding its view, that content is updated by assigning rootView because the SwiftUI view is a value, that sizingOptions defaults to the empty set so the controller tracks no size change until asked, that safeAreaRegions defaults to all and double-insets content inside a container that already inset it, and that the SwiftUI environment starts at rootView.
domain: UIKit
tags:
  - uikit
  - swiftui
  - interop
  - hosting
references:
  - https://developer.apple.com/documentation/swiftui/uihostingcontroller
  - https://developer.apple.com/documentation/swiftui/uihostingcontroller/rootview
  - https://developer.apple.com/documentation/swiftui/uihostingcontroller/sizingoptions
  - https://developer.apple.com/documentation/swiftui/uihostingcontroller/safearearegions
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:)
depends_on:
  - knowledge.uikit.view-controller-composition
related:
  - knowledge.uikit.swiftui-view-representable
  - knowledge.uikit.safe-area-and-layout-guides
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent puts a SwiftUI view inside a
UIKit screen. Its central claim is that `UIHostingController` is an ordinary
view controller with three defaults an agent must know it is accepting — no
size tracking, full safe-area insetting, a fresh SwiftUI environment — none
of which announce themselves when they are wrong.

## Scope

### Included

-   Installing a hosting controller, and updating its content
-   `sizingOptions` and `safeAreaRegions` defaults; the environment root

### Excluded

-   Wrapping a UIKit view for SwiftUI — see `swiftui-view-representable`;
    the containment sequence — see `view-controller-composition`
-   SwiftUI views, state, and environment values — owned by `swiftui`

## Rules

### Rule 1

Agents MUST install a `UIHostingController` with the child view controller
containment sequence, not by adding its `view` alone. Per Apple's
documentation: "Use the hosting controller like you would any other view
controller, by presenting it or embedding it as a child view controller in
your interface." A bare `addSubview(host.view)` leaves the controller
unretained and outside the hierarchy, so it deallocates and the content
stops updating.

### Rule 2

Agents MUST update embedded content by assigning `rootView`, and MUST NOT
expect a mutated copy of the original SwiftUI view to take effect. Per
Apple's documentation the view is specified "as the root view for this view
controller; you can change that view later using the `rootView` property."
The view is a value the controller holds, so mutating the struct the agent
still references reaches nothing.

### Rule 3

Agents MUST set `sizingOptions` when the surrounding UIKit layout should
follow the SwiftUI content's size. Per Apple's documentation, this property
governs "how the hosting controller tracks changes to the size of its
SwiftUI content", and "the default value is the empty set" — by default no
change is tracked, so a hosted view that grows leaves its container at its
original size.

### Rule 4

Agents MUST set `safeAreaRegions` to exclude what the surrounding UIKit
container already handles. Per Apple's documentation "the default value is
`SafeAreaRegions.all`", and disabling a region is appropriate "when hosting
content that you know should never be affected by the safe area". A host
inside a view already constrained to the safe area insets its content a
second time, which reads as unexplained padding.

### Rule 5

Agents MUST attach every environment value, observable object, and modifier
the SwiftUI hierarchy needs to the view passed as `rootView`. The hosting
controller is where the SwiftUI hierarchy starts; UIKit view controllers
above it hold no environment and contribute none.

## Compliant Example

```swift
final class ProfileViewController: UIViewController {
    private let host = UIHostingController(rootView: ProfileView(model: .placeholder)
                                            .environmentObject(Session.shared))  // Rule 5
    override func viewDidLoad() {
        super.viewDidLoad()
        host.sizingOptions = .intrinsicContentSize                    // Rule 3
        host.safeAreaRegions = []                                     // Rule 4
        addChild(host)                                                // Rule 1
        view.addSubview(host.view)
        host.view.frame = view.bounds
        host.didMove(toParent: self)
    }
    func show(_ model: ProfileModel) {
        host.rootView = ProfileView(model: model)                     // Rule 2
            .environmentObject(Session.shared)
    }
}
```

## Non-Compliant Example

```swift
override func viewDidLoad() {
    var root = ProfileView(model: .placeholder)
    view.addSubview(UIHostingController(rootView: root).view)
    root.model = loadedModel
}
```
The hosting controller is created, its view added, and the controller
released on the same line — nothing retains it and no containment is
established (Rule 1). Mutating the local `root` afterwards changes a value
the controller never saw (Rule 2), nothing sizes the content (Rule 3), and
`Session` is nowhere in the SwiftUI environment (Rule 5).

## Dependencies

- `view-controller-composition` -- it owns the `addChild`/`didMove` sequence
  Rule 1 requires; this one owns only what is special about hosting SwiftUI.

## References

-   [Apple Developer — UIHostingController](https://developer.apple.com/documentation/swiftui/uihostingcontroller)
-   [Apple Developer — rootView](https://developer.apple.com/documentation/swiftui/uihostingcontroller/rootview)
-   [Apple Developer — sizingOptions](https://developer.apple.com/documentation/swiftui/uihostingcontroller/sizingoptions)
-   [Apple Developer — safeAreaRegions](https://developer.apple.com/documentation/swiftui/uihostingcontroller/safearearegions)
-   [Apple Developer — addChild(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:))
