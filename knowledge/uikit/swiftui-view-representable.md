# SwiftUI View Representable

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.uikit.swiftui-view-representable
artifact_type: knowledge
title: SwiftUI View Representable
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines how a UIKit view is wrapped for a SwiftUI hierarchy — the layout properties SwiftUI owns and an agent must never assign, the Coordinator that is the only supported route for delegate and target-action messages back into SwiftUI, the documented ordering that makeCoordinator runs before makeUIView so delegates are read from the context rather than constructed, the idempotence updateUIView must have because it runs on every state change, and the choice of UIViewControllerRepresentable when the wrapped type is a view controller.
domain: UIKit
tags:
  - uikit
  - swiftui
  - interop
  - representable
references:
  - https://developer.apple.com/documentation/swiftui/uiviewrepresentable
  - https://developer.apple.com/documentation/swiftui/uiviewcontrollerrepresentable
  - https://developer.apple.com/documentation/swiftui/uiviewrepresentablecontext
  - https://developer.apple.com/documentation/swiftui/uiviewrepresentable/makecoordinator()
  - https://developer.apple.com/documentation/swiftui/uiviewrepresentable/updateuiview(_:context:)
depends_on: []
related:
  - knowledge.uikit.swiftui-hosting-controller
  - knowledge.uikit.view-controller-composition
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent exposes a UIKit view to
SwiftUI. Its central claim is that the representable is a description, not
an owner: SwiftUI decides the view's geometry and calls the update method
whenever it likes, so code that sets a frame or holds state in the struct
fights the system rather than configuring it.

## Scope

### Included

-   The layout properties SwiftUI owns, and the view-controller variant
-   `Coordinator` creation and ordering; `updateUIView` idempotence

### Excluded

-   Embedding SwiftUI inside UIKit — see `swiftui-hosting-controller`;
    containment itself — see `view-controller-composition`
-   SwiftUI views, state, and layout — owned by `swiftui`

## Rules

### Rule 1

Agents MUST NOT assign the wrapped view's layout properties. Per Apple's
documentation: "SwiftUI fully controls the layout of the UIKit view's
`center`, `bounds`, `frame`, and `transform` properties. Don't directly set
these layout-related properties on the view managed by a
`UIViewRepresentable` instance from your own code because that conflicts
with SwiftUI and results in undefined behavior." Sizing is expressed with
SwiftUI modifiers, or with hugging and compression-resistance priorities.

### Rule 2

Agents MUST route delegate and target-action messages through a
`Coordinator`. Per Apple's documentation: "The system doesn't automatically
communicate changes occurring within your view to other parts of your
SwiftUI interface… you must provide a `Coordinator` instance to facilitate
those interactions. For example, you use a coordinator to forward
target-action and delegate messages from your view to any SwiftUI views."
The struct itself cannot serve: it is a value recreated on every render.

### Rule 3

Agents MUST read the coordinator from `context.coordinator` inside
`makeUIView(context:)` rather than constructing one there. Per Apple's
documentation of `makeCoordinator()`: "SwiftUI calls this method before
calling the `makeUIView(context:)` method." One built inside `makeUIView` is
unowned by SwiftUI and deallocates, taking the delegate with it.

### Rule 4

Agents MUST make `updateUIView(_:context:)` idempotent. It runs on every
change SwiftUI propagates, so allocating subviews or reassigning delegates
there accumulates them silently. Its job is to apply current values to a
view that exists; everything created once belongs in `makeUIView`.

### Rule 5

Agents MUST use `UIViewControllerRepresentable` when the wrapped type is a
`UIViewController`, and MUST NOT wrap its `view` in a
`UIViewRepresentable`. A bare `view` leaves the controller outside the
containment hierarchy, so it gets no appearance callbacks and no trait
propagation — what `view-controller-composition` describes for `addSubview`.

## Compliant Example

```swift
struct SearchField: UIViewRepresentable {
    @Binding var text: String
    func makeCoordinator() -> Coordinator { Coordinator(text: $text) }   // Rule 3

    func makeUIView(context: Context) -> UISearchBar {
        let bar = UISearchBar()
        bar.delegate = context.coordinator                               // Rules 2, 3
        return bar
    }
    func updateUIView(_ bar: UISearchBar, context: Context) {
        bar.text = text                                                  // Rule 4
    }
    final class Coordinator: NSObject, UISearchBarDelegate {
        @Binding private var text: String
        init(text: Binding<String>) { _text = text }
        func searchBar(_ b: UISearchBar, textDidChange t: String) { text = t }
    }
}
```

## Non-Compliant Example

```swift
struct SearchField: UIViewRepresentable {
    func makeUIView(context: Context) -> UISearchBar { UISearchBar() }

    func updateUIView(_ bar: UISearchBar, context: Context) {
        bar.frame = CGRect(x: 0, y: 0, width: 320, height: 44)
        bar.delegate = SearchDelegate()
    }
}
```
The frame assignment conflicts with SwiftUI's layout and is undefined
behaviour (Rule 1). The delegate is a fresh object per update, deallocated
at once and re-created on every state change (Rules 2, 4), with no
coordinator to hold it (Rule 3).

## Dependencies

None.

## References

-   [Apple Developer — UIViewRepresentable](https://developer.apple.com/documentation/swiftui/uiviewrepresentable)
-   [Apple Developer — UIViewControllerRepresentable](https://developer.apple.com/documentation/swiftui/uiviewcontrollerrepresentable)
-   [Apple Developer — UIViewRepresentableContext](https://developer.apple.com/documentation/swiftui/uiviewrepresentablecontext)
-   [Apple Developer — makeCoordinator()](https://developer.apple.com/documentation/swiftui/uiviewrepresentable/makecoordinator())
-   [Apple Developer — updateUIView(_:context:)](https://developer.apple.com/documentation/swiftui/uiviewrepresentable/updateuiview(_:context:))
