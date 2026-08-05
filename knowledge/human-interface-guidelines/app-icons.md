# App Icons

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.app-icons
type: knowledge
title: App Icons
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design requirements for iOS/iPadOS app icons — layered composition, unmasked shape, simplicity, and light/dark/tinted appearance variants.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - app-icon
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/app-icons
depends_on: []
related:
  - knowledge.human-interface-guidelines.branding
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.icons
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent designs or reviews an
iOS/iPadOS app icon: layer composition, shape/masking, simplicity, and
appearance variants. It is distinct from `icons` (in-UI interface
icons/glyphs) and `branding` (broader brand identity).

## Scope

### Included

-   Layered icon composition (background/foreground layers)
-   Unmasked square layer shape (the system applies corner masking)
-   Simplicity and optical centering
-   Prohibition on replicating Apple hardware
-   Text-in-icon guidance
-   Light/dark/tinted appearance variant consistency

### Excluded

-   In-UI interface icons/glyphs — see `icons`
-   SF Symbols selection/rendering — see `sf-symbols`
-   Broader brand voice/accent color — see `branding`

## Rules

### Rule 1

Agents MUST specify square, unmasked foreground/background layers for
iOS/iPadOS app icons — the system applies corner-radius masking; the
icon source MUST NOT pre-apply rounded corners.

### Rule 2

Agents MUST keep primary icon content optically centered so it isn't
truncated when the system applies masking.

### Rule 3

Agents SHOULD design a simple icon using a minimal number of shapes —
fine detail becomes illegible at small icon sizes.

### Rule 4

Agents MUST NOT depict replicas of Apple hardware products in an app
icon.

### Rule 5

Agents SHOULD avoid nonessential text in an app icon — text doesn't
localize or scale, and is often unreadable at small sizes.

### Rule 6

Agents SHOULD keep the icon's core visual features consistent across
default, dark, and tinted appearance variants rather than swapping
elements between them.

## Compliant Example

-   ✓ Icon uses one simple centered shape, square unmasked layers imported to Icon Composer. (Rules 1, 2, 3)
-   ✓ Dark and tinted variants use the same silhouette as the default icon, just recolored. (Rule 6)

## Non-Compliant Example

-   ✗ Icon source has corners pre-rounded before being handed to the system. (Rule 1)
-   ✗ Icon is packed with fine detail and includes the app's full name as text. (Rules 3, 5)
-   ✗ Dark variant uses an entirely different graphic than the default variant. (Rule 6)

## Dependencies

None.

## References

-   [Apple HIG — App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
