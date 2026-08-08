# Accessibility Traits

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-traits
artifact_type: knowledge
title: Accessibility Traits
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of accessibilityTraits (SwiftUI .accessibilityAddTraits()/.accessibilityRemoveTraits(), UIKit accessibilityTraits) so VoiceOver announces an element's role and state correctly.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - traits
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilitytraits
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.accessibility.accessibility-labels
  - knowledge.accessibility.accessibility-value-and-hint
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent assigns
`accessibilityTraits` (SwiftUI `.accessibilityAddTraits()`/
`.accessibilityRemoveTraits()`, UIKit `accessibilityTraits`) so VoiceOver
announces an element's role (button, header, selected) correctly,
especially for custom controls built from non-semantic base views.

## Scope

### Included

-   Assigning role traits (`.isButton`, `.isHeader`, `.isImage`) to custom controls
-   Toggling `.isSelected` with selection state
-   `.updatesFrequently` for continuously changing values
-   Avoiding conflicting trait combinations

### Excluded

-   Label wording itself — see `accessibility-labels`
-   Value/hint content — see `accessibility-value-and-hint`

## Rules

### Rule 1

Agents MUST add the matching role trait (e.g. `.isButton`) when building
a custom interactive control from a non-semantic base view (a `Text` or
`Image` wrapped in `.onTapGesture`, or a plain UIKit `UIView` with a tap
gesture recognizer) — without it, VoiceOver announces the element with no
role at all.

### Rule 2

Agents MUST add `.isHeader` to a view acting as a section/screen heading
that isn't a native heading-styled control, so VoiceOver's headings
rotor can navigate to it.

### Rule 3

Agents MUST toggle `.isSelected` (`.accessibilityAddTraits(.isSelected)`/
`.accessibilityRemoveTraits(.isSelected)` in SwiftUI, the `.selected`
trait in UIKit) to match live selection state, rather than encoding
selection only in the visible label or value.

### Rule 4

Agents MUST NOT combine traits that describe conflicting roles on the
same element (e.g. `.isButton` and `.isStaticText` together) — pick the
trait set that matches the element's actual interactive behavior.

### Rule 5

Agents SHOULD add `.updatesFrequently` to elements whose value changes
continuously (live progress, a running timer) so VoiceOver throttles
re-announcements instead of interrupting speech on every update.

## Compliant Example

```swift
Text("Chapter 1")
    .font(.title2)
    .accessibilityAddTraits(.isHeader)

Image(systemName: "checkmark.circle")
    .onTapGesture { toggleDone() }
    .accessibilityLabel("Mark done")
    .accessibilityAddTraits(isDone ? [.isButton, .isSelected] : .isButton)
```
Explicit header trait for a non-native heading; selection trait toggled with state. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
Text("Chapter 1")
    .font(.title2)

Image(systemName: "checkmark.circle")
    .onTapGesture { toggleDone() }
    .accessibilityLabel("Mark done")
```
No `.isHeader` trait, so the headings rotor skips "Chapter 1"; no `.isButton` trait, so VoiceOver announces the tappable checkmark with no role at all. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityAddTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:))
-   [Apple Developer — UIAccessibilityTraits](https://developer.apple.com/documentation/uikit/uiaccessibilitytraits)
