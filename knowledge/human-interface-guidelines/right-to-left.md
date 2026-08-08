# Right to Left

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.right-to-left
artifact_type: knowledge
title: Right to Left
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for adapting iOS/iPadOS interfaces to right-to-left (RTL) languages such as Arabic and Hebrew — layout mirroring, numerals, and icon flipping.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - right-to-left
  - rtl
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/right-to-left
depends_on: []
related:
  - knowledge.human-interface-guidelines.layout
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.style-guide.international-formatting
  - knowledge.style-guide.international-style
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent adapts an iOS/iPadOS
interface for right-to-left (RTL) languages: layout mirroring, numeral
ordering, and which icons/images flip versus stay fixed.

## Scope

### Included

-   Layout direction mirroring
-   Digit-order preservation within a number
-   Flipping of directional controls
-   Non-flipping of images, logos, universal symbols
-   Interface-icon flip rules (text/motion vs. real-world objects)
-   Paragraph vs. short-text alignment rules

### Excluded

-   General layout/hierarchy rules unrelated to direction — see `layout`
-   General SF Symbols usage (rendering, variants, weight/scale) — see `sf-symbols`; SF Symbols' built-in RTL-variant mechanics specifically is not yet covered by any current contract
-   Locale-specific number/date formatting text rules — see style-guide `international-style`/`international-formatting`

## Rules

### Rule 1

Agents MUST mirror layout direction for RTL languages when not already
using system-provided components that flip automatically.

### Rule 2

Agents MUST NOT reverse the digit order within a specific number
(phone numbers, "541") regardless of language direction.

### Rule 3

Agents MUST flip directional controls (back button, progress bars,
next/previous) to match RTL reading order.

### Rule 4

Agents MUST NOT flip images, logos, or universal symbols (e.g.,
checkmarks) — flipping can change or violate their meaning.

### Rule 5

Agents SHOULD flip interface icons that represent text/reading
direction or forward/backward motion, but MUST NOT flip icons that
depict real-world objects (e.g., a clock) unless directionality is the
point of the icon.

### Rule 6

Agents SHOULD align a paragraph (3+ lines) to match its language, while
short 1–2 line text blocks may follow the current UI context direction.

## Compliant Example

-   ✓ The back button points right in an RTL layout. (Rule 3)
-   ✓ A phone number's digits stay in their original order under RTL. (Rule 2)

## Non-Compliant Example

-   ✗ An app logo is mirrored in an RTL locale. (Rule 4)
-   ✗ A "541" balance is reversed to "145" under RTL. (Rule 2)
-   ✗ The back button still points left in an RTL layout. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Right to Left](https://developer.apple.com/design/human-interface-guidelines/right-to-left)
