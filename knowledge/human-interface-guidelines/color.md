# Color

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.color
artifact_type: knowledge
title: Color
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using system and custom color in iOS/iPadOS interfaces — consistency, contrast, semantic meaning, and wide-color support.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - color
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/color
depends_on: []
related:
  - knowledge.human-interface-guidelines.dark-mode
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.materials
last_updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent selects and applies color
in an iOS/iPadOS interface: consistency of meaning, contrast, semantic
system colors, and avoiding color as the sole information channel.

## Scope

### Included

-   Consistent meaning of a given color across the interface
-   Light/dark/increased-contrast variants for custom colors
-   Avoiding hard-coded system color values
-   Semantic meaning of dynamic system colors
-   Color as a non-exclusive information channel
-   iOS/iPadOS background-color hierarchy (system vs. grouped)

### Excluded

-   Dark Mode-specific contrast ratios and base/elevated backgrounds — see `dark-mode`
-   Color-blindness/contrast accessibility minimums — see `accessibility`
-   Liquid Glass material color behavior — see `materials`

## Rules

### Rule 1

Agents MUST use a given color consistently for the same meaning
throughout the interface (don't reuse a status color for decoration
elsewhere).

### Rule 2

Agents MUST supply light, dark, and increased-contrast variants for
any custom color; prefer system-provided dynamic colors, which already
define these variants.

### Rule 3

Agents MUST NOT hard-code system color values — reference them via
platform APIs (e.g., SwiftUI `Color`, UIKit `UIColor`) so they track
OS updates.

### Rule 4

Agents MUST NOT redefine the semantic meaning of a dynamic system
color (e.g., don't use the separator color as body text color).

### Rule 5

Agents MUST NOT rely on color alone to convey information — pair with
text, shape, or icon (see `accessibility` Rule 3).

### Rule 6

Agents SHOULD use the grouped background-color set for grouped table
views, and the system background-color set otherwise, using
primary/secondary/tertiary variants to convey hierarchy.

## Compliant Example

-   ✓ A custom brand color ships with light, dark, and increased-contrast variants. (Rule 2)
-   ✓ A status indicator uses color plus an icon together. (Rule 5)

## Non-Compliant Example

-   ✗ A `UIColor` value is hard-coded as a hex literal in code. (Rule 3)
-   ✗ The system separator color is reused as a body text color. (Rule 4)
-   ✗ Success/failure is shown via a colored dot with no accompanying icon or text. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)
