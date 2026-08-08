# Accessibility Value and Hint

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-value-and-hint
artifact_type: knowledge
title: Accessibility Value and Hint
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of accessibilityValue for a custom control's current state and accessibilityHint for the outcome of an ambiguous action, in SwiftUI and UIKit.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - value
  - hint
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)
  - https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityvalue
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityhint
depends_on: []
related:
  - knowledge.accessibility.accessibility-labels
  - knowledge.accessibility.accessibility-traits
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent communicates a custom
control's live state via `accessibilityValue` and the outcome of a
non-obvious action via `accessibilityHint`, so VoiceOver users get the
same state and outcome information sighted users get visually.

## Scope

### Included

-   `accessibilityValue` for custom sliders/steppers/segmented controls
-   Keeping value live/computed, not a stale literal
-   `accessibilityHint` for non-obvious action outcomes
-   Avoiding label/value/hint duplication

### Excluded

-   Element naming — see `accessibility-labels`
-   Role/state traits — see `accessibility-traits`

## Rules

### Rule 1

Agents MUST set `accessibilityValue` (SwiftUI `.accessibilityValue()`,
UIKit `accessibilityValue`) on any custom control that carries a value
not conveyed by its label — a custom slider, star rating, or segmented
control needs its current selection/level spoken separately from its
name.

### Rule 2

Agents MUST bind `accessibilityValue` to a computed expression that
reflects the current state, not a literal string captured once — a stale
value announces the wrong state after the control changes.

### Rule 3

Agents SHOULD add `accessibilityHint` (SwiftUI `.accessibilityHint()`,
UIKit `accessibilityHint`) only when the result of activating the
element isn't obvious from its label and trait alone (e.g. "Deletes this
message" on a swipe-triggered action with no visible confirmation).

### Rule 4

Agents MUST NOT restate the label's content inside the hint — the hint
describes the *outcome* of interacting with the element, not what the
element already says it is.

### Rule 5

Agents MUST NOT put information required to use the control only in the
hint — hints are supplementary; anything essential belongs in the label
or value so it's never missed.

## Compliant Example

```swift
Slider(value: $volume, in: 0...100)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume)) percent")
```
Live, computed value reflects the current slider position on every read. (Rules 1, 2)

## Non-Compliant Example

```swift
Slider(value: $volume, in: 0...100)
    .accessibilityLabel("Volume, currently 50 percent")
```
The starting value is baked into the label as a one-time string; it never updates as `volume` changes, and the value's role belongs in `accessibilityValue`, not the label. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:))
-   [Apple Developer — accessibilityHint(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:))
-   [Apple Developer — UIAccessibilityElement accessibilityValue](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityvalue)
-   [Apple Developer — UIAccessibilityElement accessibilityHint](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityhint)
