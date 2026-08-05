# Typography

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.typography
type: knowledge
title: Typography
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for typographic choices in iOS/iPadOS interfaces — legibility, hierarchy, system fonts, and Dynamic Type support.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - typography
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/typography
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.layout
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent makes typographic
choices in an iOS/iPadOS interface: legibility, text-style hierarchy,
system vs. custom fonts, and Dynamic Type support.

## Scope

### Included

-   Font-size/weight legibility minimums
-   Use of built-in text styles for hierarchy
-   Typeface-count minimization
-   Custom font accessibility parity with system fonts
-   Dynamic Type layout adaptability
-   Prioritizing which content scales at large accessibility sizes

### Excluded

-   Exact copy wording — see style-guide domain
-   Layout adaptability beyond text — see `layout`
-   Contrast/color rules for text — see `color`, `accessibility`

## Rules

### Rule 1

Agents MUST support Dynamic Type so people can scale visible text via
system text-size settings. Ensuring the surrounding layout doesn't
break or truncate at those larger sizes is covered by `layout` Rule 2.

### Rule 2

Agents SHOULD use built-in text styles (body, headline, etc.) rather
than fixed point sizes, so hierarchy and scaling stay consistent
automatically.

### Rule 3

Agents MUST avoid ultralight/thin font weights for any text that must
stay legible at small sizes; prefer Regular, Medium, Semibold, or Bold.

### Rule 4

Agents SHOULD minimize the number of typefaces used in one interface
to preserve a clear information hierarchy.

### Rule 5

If a custom font is used, agents MUST implement the same Dynamic Type
/ Bold Text accessibility behavior that system fonts provide
automatically.

### Rule 6

Agents SHOULD prioritize which content actually needs to grow at
larger text sizes (e.g., primary content) rather than scaling every
element uniformly.

## Compliant Example

-   ✓ Body text uses the system `body` text style and reflows correctly at the largest accessibility text size. (Rules 1, 2)
-   ✓ A custom display font still responds to Bold Text. (Rule 5)

## Non-Compliant Example

-   ✗ An interface hard-codes a fixed 14pt label that doesn't grow with Dynamic Type. (Rule 1)
-   ✗ A custom font ships without Dynamic Type support and truncates at larger sizes. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
