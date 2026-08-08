# SF Symbols (Design)

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.sf-symbols
artifact_type: knowledge
title: SF Symbols (Design)
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when and how to choose, compose, and style SF Symbols within an iOS/iPadOS design — rendering modes, weights/scales, and variants.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - sf-symbols
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/sf-symbols
depends_on: []
related:
  - knowledge.human-interface-guidelines.icons
  - knowledge.human-interface-guidelines.app-icons
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.sf-symbols.rendering-modes
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent selects and styles SF
Symbols within an iOS/iPadOS design — rendering mode, weight/scale
matching, and fill vs. outline variant choice. It covers the design
angle; API-level rendering/animation implementation belongs to the
dedicated `sf-symbols` domain (see docs/architecture/domain-map.md
Cross-Domain Notes).

## Scope

### Included

-   Rendering-mode selection (monochrome/hierarchical/palette/multicolor)
-   System color usage with symbols for automatic adaptation
-   Weight/scale matching with adjacent text
-   Fill vs. outline variant selection by context
-   Custom-symbol restrictions (no Apple product replicas)
-   Accessibility labeling for custom symbols

### Excluded

-   API-level rendering/animation implementation — see the `sf-symbols` domain
-   General interface-icon consistency rules unrelated to SF Symbols specifically — see `icons`

## Rules

### Rule 1

Agents SHOULD choose a rendering mode (monochrome, hierarchical,
palette, multicolor) based on the symbol's meaning and context, and
verify legibility at the actual display size rather than assuming the
automatic setting is always correct.

### Rule 2

Agents MUST use system-provided colors with symbols so they adapt
automatically to accessibility settings and Dark Mode.

### Rule 3

Agents SHOULD match a symbol's weight to adjacent text weight, and use
scale (small/medium/large) to adjust emphasis without breaking that
weight match.

### Rule 4

Agents SHOULD choose the fill variant for higher-emphasis contexts
(selected tab bar items, swipe actions) and the outline variant when
the symbol appears alongside text in lists or toolbars.

### Rule 5

Agents MUST NOT customize or modify a symbol that SF Symbols already
marks as representing an Apple product or feature. The prohibition on
replicating Apple hardware is surface-scoped rather than general:
`icons` Rule 6 covers interface icons, and `app-icons` Rule 4 covers
the app icon.

### Rule 6

Agents MUST provide an accessibility label for any custom symbol, same
as for a custom interface icon (see `icons` Rule 4).

## Compliant Example

-   ✓ A tab bar uses filled SF Symbol variants for the selected state and outline variants for unselected, all tinted with the system accent color. (Rules 2, 4)

## Non-Compliant Example

-   ✗ A custom symbol hard-codes a non-adaptive color that doesn't respond to Dark Mode. (Rule 2)
-   ✗ A toolbar's SF Symbol uses a Bold weight next to adjacent text set in Regular weight, breaking the intended weight match. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)
