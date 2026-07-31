# Accessibility Hidden and Decorative Elements

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-hidden-decorative
type: knowledge
title: Accessibility Hidden and Decorative Elements
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of .accessibilityHidden(true) (SwiftUI) and isAccessibilityElement = false (UIKit) to exclude purely decorative or duplicate content from VoiceOver, without hiding elements that carry unique information.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - decorative
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.accessibility.accessibility-labels
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent excludes purely decorative
or duplicate content from the accessibility tree with
`.accessibilityHidden(true)` (SwiftUI) or `isAccessibilityElement = false`
(UIKit), so VoiceOver skips visual noise without ever hiding an element
that carries unique information.

## Scope

### Included

-   Hiding purely decorative images/shapes/backgrounds
-   Hiding duplicate elements that repeat already-announced information
-   Hiding a decorative sublayer without hiding its interactive parent

### Excluded

-   Providing a label instead of hiding informative content — see `accessibility-labels`

## Rules

### Rule 1

Agents MUST hide purely decorative images, background shapes, and
illustrations with `.accessibilityHidden(true)` (SwiftUI) or
`isAccessibilityElement = false` (UIKit) so VoiceOver doesn't stop on
content that conveys no information.

### Rule 2

Agents MUST NOT hide an image or icon that conveys unique information
(an icon-only button, a status illustration with no accompanying text) —
give it a label per `accessibility-labels` instead of hiding it.

### Rule 3

Agents MUST hide only the decorative sublayer of a control, not the
interactive control itself, when a button's background image or icon is
decorative but the button as a whole must remain accessible — apply
`.accessibilityHidden(true)` (SwiftUI) or `isAccessibilityElement = false`
(UIKit) to the decorative image/icon subview, never to its tappable
parent (`Button`/`UIButton`/`UIControl`).

### Rule 4

Agents SHOULD hide a decorative element that visually duplicates
information already announced elsewhere — via `.accessibilityHidden(true)`
(SwiftUI) or `isAccessibilityElement = false` (UIKit) — such as a
disclosure chevron next to a row that already carries the
`.isButton`/navigation trait, to avoid a redundant, uninformative stop.

## Compliant Example

```swift
ZStack {
    Image("hero-background")
        .accessibilityHidden(true)
    Text("Welcome back")
        .font(.largeTitle)
}
```
The decorative background image is hidden; the informative title text remains. (Rule 1)

## Non-Compliant Example

```swift
Button {
    openDetail()
} label: {
    HStack {
        Text(item.title)
        Image(systemName: "chevron.right")
    }
}
.accessibilityHidden(true)
```
Hiding the entire button (including its title text) instead of just the decorative chevron makes the whole row unreachable by VoiceOver. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityHidden(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:))
-   [Apple Developer — UIAccessibility isAccessibilityElement](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement)
