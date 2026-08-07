# Accessibility Labels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-labels
artifact_type: knowledge
title: Accessibility Labels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to set accessibilityLabel (SwiftUI .accessibilityLabel(), UIKit accessibilityLabel) so VoiceOver announces a concise, meaningful name for every element that needs one.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - labels
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilitylabel
depends_on: []
related:
  - knowledge.accessibility.accessibility-traits
  - knowledge.accessibility.accessibility-value-and-hint
  - knowledge.human-interface-guidelines.accessibility
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent sets `accessibilityLabel`
(SwiftUI `.accessibilityLabel()`, UIKit `accessibilityLabel`) so VoiceOver
announces a concise, meaningful name for every element that needs one,
implementing the API-level half of the labeling requirement HIG's
`accessibility.md` sets at the design level.

## Scope

### Included

-   When a custom label is required vs. when the default suffices
-   Concise, noun-phrase label wording
-   Avoiding redundant or state-encoding labels

### Excluded

-   Which trait an element should carry — see `accessibility-traits`
-   Communicating dynamic value/state — see `accessibility-value-and-hint`
-   Whether contrast/text-scaling makes a label legible — owned by `human-interface-guidelines`'s `accessibility.md`

## Rules

### Rule 1

Agents MUST set `accessibilityLabel` (`.accessibilityLabel()` in SwiftUI,
`accessibilityLabel` in UIKit) on every interactive or informative
element whose visible content is an icon, image, or symbol with no
adjacent text — VoiceOver has no other source for that element's name.

### Rule 2

Agents MUST NOT set a custom `accessibilityLabel` on an element that
already displays plain, sufficient text (e.g. a `Text`/`UILabel` showing
its own content) unless the visible text is itself insufficient out of
context — a redundant custom label just duplicates or overrides correct
default behavior.

### Rule 3

Agents MUST write labels as concise noun phrases describing what the
element is, without restating its type ("Delete", not "Delete button" or
"Delete icon") — VoiceOver appends the control's role from its trait
automatically.

### Rule 4

Agents MUST NOT encode dynamic state (selected, on/off, count) inside
`accessibilityLabel` — state belongs in `accessibilityValue` or a trait
like `.isSelected`, so the label stays stable while the value updates
independently.

### Rule 5

Agents SHOULD localize accessibility labels through the same
localization pipeline as visible strings, not hardcode English text that
visible UI already localizes.

## Compliant Example

```swift
Button {
    deleteItem()
} label: {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete")
```
Icon-only button gets a concise, stable label; VoiceOver announces "Delete, button." (Rules 1, 3)

## Non-Compliant Example

```swift
Button {
    toggleFavorite()
} label: {
    Image(systemName: isFavorite ? "star.fill" : "star")
}
.accessibilityLabel(isFavorite ? "Favorited star icon, tap to unfavorite" : "Star icon, tap to favorite")
```
Verbose label restates the control type ("icon") and encodes instructions and state that belong in a trait/value, not the label. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:))
-   [Apple Developer — UIAccessibility accessibilityLabel](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilitylabel)
