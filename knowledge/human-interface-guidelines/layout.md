# Layout

Status: Approved Version: 1.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.layout
artifact_type: knowledge
title: Layout
version: 1.1.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for structuring and adapting iOS/iPadOS interface layout — grouping, hierarchy, safe areas, size-class-based adaptability, and Liquid Glass control differentiation.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - layout
  - size-classes
  - liquid-glass
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/layout
depends_on: []
related:
  - knowledge.human-interface-guidelines.typography
  - knowledge.human-interface-guidelines.right-to-left
  - knowledge.human-interface-guidelines.materials
last_updated: 2026-09-10
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
-   Full-bleed background/content extension, including the background
    extension effect
-   Liquid Glass as the mechanism for differentiating controls from content
-   Size-class-based (not device-type/orientation-based) layout decisions

### Excluded

-   RTL-specific mirroring rules — see `right-to-left`
-   Material/blur mechanics used for grouping — see `materials`
-   Typographic hierarchy mechanics — see `typography`
-   macOS/tvOS/visionOS/watchOS platform-specific layout specifics — this
    contract is iOS/iPadOS-scoped, per `docs/architecture/domain-map.md`

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

### Rule 7

Agents SHOULD use the Liquid Glass material, not a solid or
semi-opaque background color, to visually differentiate controls from
content, and SHOULD use a scroll edge effect to elevate controls above
scrolling content. When a full-bleed background image would otherwise
be covered by an adjacent component (a sidebar or inspector), agents
SHOULD use a background extension effect (`backgroundExtensionEffect()`
/ `UIBackgroundExtensionView`) to mirror the image beneath it rather
than letting the image end abruptly at the component's edge. "Take
advantage of the Liquid Glass material... to provide a distinct
appearance for your controls... use a scroll edge effect to visually
elevate controls above content... you can use a background extension
effect to flip and blur the image, mirroring it beneath adjacent
components."

### Rule 8

Agents MUST determine layout from the current horizontal and vertical
size class (each compact or regular), not from device type or
orientation, since size class reflects the space actually available
and device idiom does not; agents MUST design for every size-class
combination the app can reach (including via multitasking or window
resizing), and MUST keep functionality — only how much of it is
visible onscreen — the same as size classes change. "Determine layout
based on size classes, not device type or orientation... Consider all
possible combinations of size classes... Don't change your app's
functionality based on the space it occupies."

## Compliant Example

-   ✓ Layout adapts from full iPad width down to compact Slide Over width without clipping content. (Rule 5)
-   ✓ Content respects safe areas around the Dynamic Island. (Rule 1)
-   ✓ A screen switches from a tab bar to a sidebar in a regular-width size class while keeping every feature reachable in compact width too. (Rule 8)

## Non-Compliant Example

-   ✗ A fixed-width layout clips content in iPad Slide Over. (Rule 5)
-   ✗ Custom UI is drawn underneath the status bar / Dynamic Island. (Rule 1)
-   ✗ A layout branches on `UIDevice.current.userInterfaceIdiom` / device orientation instead of the current size class. (Rule 8)

## Dependencies

None.

## References

-   [Apple HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
