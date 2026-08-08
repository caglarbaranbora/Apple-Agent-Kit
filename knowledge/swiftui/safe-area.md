# Safe Area

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.swiftui.safe-area
artifact_type: knowledge
title: Safe Area
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of safeAreaInset for persistent chrome versus ignoresSafeArea for edge-to-edge content, and the risks of misapplying either.
domain: SwiftUI
tags:
  - swiftui
  - layout
  - safe-area
references:
  - https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:)
  - https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:)
depends_on: []
related:
  - knowledge.swiftui.stacks-and-spacing
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent handles the safe area:
using `.safeAreaInset(edge:)` for persistent UI chrome that should
reserve space, and `.ignoresSafeArea()` only for content meant to bleed
to the physical screen edge.

## Scope

### Included

-   `.safeAreaInset(edge:)` for chrome that reserves space
-   `.ignoresSafeArea()` scope and edge targeting
-   Risk of covering interactive controls or content

### Excluded

-   General stack/spacing layout — see `stacks-and-spacing`

## Rules

### Rule 1

Agents MUST use `.safeAreaInset(edge:)` to add persistent chrome (e.g.,
a bottom toolbar or input bar) that reserves space and pushes
scrollable content, rather than overlaying it with `.overlay()` and
manually guessed padding.

### Rule 2

Agents MUST use `.ignoresSafeArea()` only for content meant to extend to
the physical screen edge (backgrounds, full-bleed images/media).

### Rule 3

Agents MUST NOT apply `.ignoresSafeArea()` to interactive controls or
primary content that would then sit under the notch, Dynamic Island, or
home indicator.

### Rule 4

Agents MUST NOT apply `.ignoresSafeArea()` to an entire screen's root
view when only a background layer needs edge-to-edge extension — scope
it to the specific background view instead.

### Rule 5

Agents SHOULD specify the `edges:` parameter on `.ignoresSafeArea(edges:)`
(e.g., `.top`) rather than ignoring all edges when only one edge needs
to bleed.

## Compliant Example

```swift
ScrollView {
    content
}
.safeAreaInset(edge: .bottom) {
    InputBar()
}
```
`InputBar` reserves its own space; scroll content never renders underneath it. (Rule 1)

## Non-Compliant Example

```swift
ZStack(alignment: .bottom) {
    ScrollView { content }
    InputBar()
}
```
`InputBar` overlays the scroll content with no reserved space, obscuring the last row. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — safeAreaInset](https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:))
-   [Apple Developer — ignoresSafeArea](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:))
