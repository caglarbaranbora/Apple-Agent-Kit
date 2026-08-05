# Accessibility Element Grouping

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-element-grouping
type: knowledge
title: Accessibility Element Grouping
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of .accessibilityElement(children:) (SwiftUI) and isAccessibilityElement/accessibilityElements (UIKit) to control whether a composite view is one VoiceOver stop or several.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - grouping
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement
depends_on: []
related:
  - knowledge.accessibility.accessibility-hidden-decorative
  - knowledge.accessibility.voiceover-navigation-order
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent controls whether a
composite view (icon + title + subtitle row, a card containing an
embedded button) becomes one VoiceOver stop or several, using
`.accessibilityElement(children:)` in SwiftUI and `isAccessibilityElement`/
`accessibilityElements` in UIKit.

## Scope

### Included

-   `.accessibilityElement(children: .combine)` for merging static composite content
-   `.accessibilityElement(children: .contain)` for grouping without merging interactive children
-   `.accessibilityElement(children: .ignore)` with an explicit label
-   UIKit `isAccessibilityElement` and container `accessibilityElements`

### Excluded

-   The order elements are read in — see `voiceover-navigation-order`
-   Hiding purely decorative content — see `accessibility-hidden-decorative`

## Rules

### Rule 1

Agents MUST group a row of purely static, related content (icon +
title + subtitle with no independently interactive children) with
`.accessibilityElement(children: .combine)` so VoiceOver announces it as
one stop instead of three separate swipes.

### Rule 2

Agents MUST use `.accessibilityElement(children: .contain)` — not
`.combine` — when a composite view contains a child that must remain
independently activatable (e.g. a card with body text plus an embedded
button), so the button stays individually reachable while the group
still scopes rotor/frame navigation.

### Rule 3

Agents MUST supply an explicit `.accessibilityLabel()` when using
`.accessibilityElement(children: .ignore)` — `.ignore` hides all child
content from the accessibility tree, so without a label the element
becomes an unannounced blank stop.

### Rule 4

Agents MUST set `isAccessibilityElement = false` on a UIKit container
`UIView` that exists only to lay out already-accessible subviews, so
VoiceOver does not create a duplicate, uninformative stop for the empty
container itself.

### Rule 5

Agents SHOULD populate a UIKit container's `accessibilityElements` array
to scope a composite view to exactly the children that should be
individually exposed — any subview not listed in the array is excluded
from VoiceOver entirely, which is UIKit's equivalent of SwiftUI's
`.combine`/`.contain` grouping choice. Setting the array's *order* (as
opposed to its membership) is covered by `voiceover-navigation-order`.

## Compliant Example

```swift
HStack {
    Image(systemName: "person.crop.circle")
    VStack(alignment: .leading) {
        Text(user.name)
        Text(user.email)
    }
}
.accessibilityElement(children: .combine)
```
Icon, name, and email announce as one combined VoiceOver stop. (Rule 1)

## Non-Compliant Example

```swift
HStack {
    Image(systemName: "person.crop.circle")
    VStack(alignment: .leading) {
        Text(user.name)
        Text(user.email)
    }
}
```
No grouping: VoiceOver treats the icon, name, and email as three separate stops a user must swipe through individually to understand one logical row. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityElement(children:)](https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:))
-   [Apple Developer — UIAccessibility isAccessibilityElement](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement)
