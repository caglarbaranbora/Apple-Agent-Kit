# VoiceOver Navigation Order

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.accessibility.voiceover-navigation-order
artifact_type: knowledge
title: VoiceOver Navigation Order
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of accessibilitySortPriority (SwiftUI) and an explicit accessibilityElements order (UIKit) to fix VoiceOver reading order when it diverges from visual/z-order layout.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - navigation-order
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilitycontainer
depends_on: []
related:
  - knowledge.accessibility.accessibility-element-grouping
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent controls VoiceOver's
reading order using `.accessibilitySortPriority()` (SwiftUI) or an
explicit `accessibilityElements` array (UIKit), for layouts where
default visual/z-order traversal produces the wrong reading order.

## Scope

### Included

-   `.accessibilitySortPriority()` for overlapping/`ZStack` layouts
-   UIKit's `accessibilityElements` explicit ordering
-   When default order is already correct (no action needed)

### Excluded

-   Whether elements are merged into one stop — see `accessibility-element-grouping`

## Rules

### Rule 1

Agents MUST set `.accessibilitySortPriority()` explicitly on elements
inside a `ZStack` or other overlapping layout whose intended reading
order doesn't match declaration order — SwiftUI's default reading order
follows visual layout, which is ambiguous for overlapping content.

### Rule 2

Agents MUST NOT rely on default left-to-right, top-to-bottom traversal
for absolutely positioned or manually offset elements where that
traversal would read content out of logical order.

### Rule 3

Agents MUST populate a UIKit container's `accessibilityElements` array
explicitly, in the desired reading order, whenever the default
view-hierarchy order produces an incorrect sequence.

### Rule 4

Agents SHOULD keep sort-priority overrides local and minimal — reorder
only the specific elements that are wrong rather than assigning priority
values across an entire screen, which becomes fragile as the layout
changes.

## Compliant Example

```swift
ZStack {
    BackgroundImage()
        .accessibilityHidden(true)
    VStack {
        Text("Title").accessibilitySortPriority(2)
        Text("Subtitle").accessibilitySortPriority(1)
    }
}
```
Explicit priority guarantees "Title" is read before "Subtitle" regardless of z-order. (Rule 1)

## Non-Compliant Example

```swift
ZStack(alignment: .bottomLeading) {
    Text("Subtitle")
    Text("Title").offset(y: -40)
}
```
No sort priority: VoiceOver's traversal of the overlapping, offset content is unpredictable and may read "Subtitle" before "Title" despite the intended visual hierarchy. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilitySortPriority(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:))
-   [Apple Developer — UIAccessibilityContainer](https://developer.apple.com/documentation/uikit/uiaccessibilitycontainer)
