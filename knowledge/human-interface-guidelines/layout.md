# Layout

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.layout
type: knowledge
title: Layout
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for structuring and adapting iOS/iPadOS interface layout — grouping, hierarchy, safe areas, and adaptability to size/orientation changes.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - layout
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/layout
depends_on: []
related:
  - knowledge.human-interface-guidelines.typography
  - knowledge.human-interface-guidelines.right-to-left
  - knowledge.human-interface-guidelines.materials
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent structures and adapts
iOS/iPadOS interface layout: safe areas, visual hierarchy, grouping,
and responding to device size, orientation, and multitasking changes.

## Scope

### Included

-   Safe-area and system-chrome respect
-   Dynamic Type-driven layout adaptability
-   Reading-order/visual-hierarchy placement
-   Grouping related content with spacing/materials
-   iPad multitasking size adaptability
-   Full-bleed background/content extension

### Excluded

-   RTL-specific mirroring rules — see `right-to-left`
-   Material/blur mechanics used for grouping — see `materials`
-   Typographic hierarchy mechanics — see `typography`

## Rules

### Rule 1

Agents MUST respect system-defined safe areas so content doesn't
collide with device features (Dynamic Island, camera housing) or
system chrome (toolbars, tab bars).

### Rule 2

Agents MUST support Dynamic Type text-size changes without truncating
or breaking the layout of primary content.

### Rule 3

Agents SHOULD place the most important content near the top/leading
edge, respecting reading order (including RTL contexts — see
`right-to-left`).

### Rule 4

Agents SHOULD group related items visually (spacing, separators,
materials) while keeping content and controls clearly distinct.

### Rule 5

Agents MUST test layout at all standard iPad multitasking sizes
(halves, thirds, quadrants) and both iPhone orientations if supported,
ensuring smooth transitions between sizes.

### Rule 6

Agents SHOULD extend backgrounds and scrollable content to the edges
of the display, layering controls (sidebars, tab bars) on top rather
than sharing the same plane as content.

## Compliant Example

-   ✓ Layout adapts from full iPad width down to compact Slide Over width without clipping content. (Rule 5)
-   ✓ Content respects safe areas around the Dynamic Island. (Rule 1)

## Non-Compliant Example

-   ✗ A fixed-width layout clips content in iPad Slide Over. (Rule 5)
-   ✗ Custom UI is drawn underneath the status bar / Dynamic Island. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
