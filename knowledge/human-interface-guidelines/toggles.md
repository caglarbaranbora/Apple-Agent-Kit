# Toggles

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.toggles
artifact_type: knowledge
title: Toggles
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for using switch-style toggles on iOS/iPadOS, including state legibility and list-row vs. standalone usage.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - toggles
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/toggles
depends_on: []
related:
  - knowledge.style-guide.input-controls
  - knowledge.human-interface-guidelines.color
last_updated: 2026-08-08
```

## Intent

This contract defines when an AI coding agent should use a toggle on
iOS/iPadOS, how its on/off state must be legible, and the difference
between the in-row switch style and a standalone toggle-behaving
button.

## Scope

### Included

-   Toggle vs. other selection controls (picker, list) decision
-   On/off state legibility beyond color alone
-   Switch style restricted to list rows
-   Standalone toggle-behaving button conventions
-   Accent color changes and contrast

### Excluded

-   SwiftUI `Toggle`/UIKit `UISwitch` implementation — see `swiftui`/`uikit` domains
-   Toggle/label copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST use a toggle only to represent a pair of opposing states
(such as on/off) that affect content or a view's state — not for
choosing among a list of items, which should use a picker or list
instead.

### Rule 2

Agents MUST make a toggle's on/off states visually distinguishable
through more than color alone (such as fill, shape, or inner-detail
changes), since not everyone can perceive color differences.

### Rule 3

Agents MUST use the switch style only within a list row, relying on
the row's own content to supply context rather than adding a redundant
label.

### Rule 4

Agents SHOULD use a button that behaves like a toggle — rather than a
switch control — for toggle-like state outside of a list row, and MUST
NOT pair that button with an explanatory text label, since its icon
and appearance changes alone communicate purpose.

### Rule 5

Agents SHOULD change a switch's default accent color only when
necessary, and only to a color that still provides sufficient contrast
against the off state.

### Rule 6

Agents MUST clearly identify what setting, view, or content a toggle
affects, either via surrounding context or an explicit label.

## Compliant Example

-   ✓ A list-row switch for "Wi-Fi" relies on the row's own label; no redundant caption is added beside the switch. (Rule 3)
-   ✓ A toggle's on state changes both fill color and an internal checkmark, not color alone. (Rule 2)

## Non-Compliant Example

-   ✗ A filter toggle button outside a list row includes an explanatory text label next to its icon. (Rule 4)
-   ✗ A toggle communicates on/off using only a color change with no shape/fill difference. (Rule 2)
-   ✗ A toggle is used to let someone pick one of four options. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles)
