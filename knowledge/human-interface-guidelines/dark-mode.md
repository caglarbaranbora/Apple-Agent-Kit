# Dark Mode

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.dark-mode
type: knowledge
title: Dark Mode
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requirements for supporting the systemwide Dark Mode appearance setting on iOS/iPadOS, including contrast minimums and background-color layering.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - dark-mode
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/dark-mode
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.materials
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent supports the systemwide
Dark Mode appearance setting on iOS/iPadOS: mandatory systemwide
adherence, contrast minimums in both appearances, and iOS/iPadOS's
base/elevated background-color layering.

## Scope

### Included

-   Prohibition on app-specific appearance overrides
-   Legibility in both Light and Dark, including Increase Contrast / Reduce Transparency
-   Minimum contrast ratios in both appearances
-   iOS/iPadOS base/elevated background-color layering
-   Icon/image adaptation across appearances

### Excluded

-   General color-consistency rules — see `color`
-   Material/vibrancy mechanics — see `materials`
-   Non-color-related accessibility rules — see `accessibility`

## Rules

### Rule 1

Agents MUST NOT offer an app-specific appearance override that ignores
the systemwide Light/Dark/Auto setting.

### Rule 2

Agents MUST ensure content remains legible in both Light and Dark
appearance, including with Increase Contrast and Reduce Transparency
turned on.

### Rule 3

Agents MUST maintain at least a 4.5:1 contrast ratio between
foreground and background in both appearances, targeting 7:1 for small
custom text.

### Rule 4

Agents SHOULD use semantic/dynamic colors (e.g., `label`,
`secondaryLabel`) that adapt automatically rather than defining
separate hard-coded light/dark palettes.

### Rule 5

Agents SHOULD prefer system background colors (base/elevated) on
iOS/iPadOS so the system can convey correct depth between layered
interfaces (popovers, sheets).

### Rule 6

Agents SHOULD use SF Symbols and vibrancy for icons so they adapt
automatically between appearances, rather than shipping separate
light/dark icon assets unless a design genuinely requires it.

## Compliant Example

-   ✓ App uses `Color(.label)` / system background colors and renders correctly when the system switches Light→Dark automatically. (Rules 1, 4)

## Non-Compliant Example

-   ✗ App ships its own in-app Light/Dark toggle that ignores the system setting. (Rule 1)
-   ✗ A white content-background image glows against the surrounding Dark Mode context because it wasn't adjusted. (Rule 2)

## Dependencies

None.

## References

-   [Apple HIG — Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)
