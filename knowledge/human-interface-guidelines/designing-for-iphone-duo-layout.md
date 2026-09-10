# Designing for iPhone Duo — Dynamic Layouts

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.designing-for-iphone-duo-layout
artifact_type: knowledge
title: Designing for iPhone Duo — Dynamic Layouts
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines how an AI coding agent builds adaptive layout for iPhone Duo — resizable layout fundamentals, split views, arrangement views (split/overlay), fold behavior, and full-screen game layout.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - designing-for-iphone-duo
  - foldable
  - layout
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo
depends_on:
  - knowledge.human-interface-guidelines.designing-for-iphone-duo-anatomy
related:
  - knowledge.human-interface-guidelines.designing-for-iphone-duo-vertical-controls
  - knowledge.human-interface-guidelines.layout
last_updated: 2026-09-10
```

## Intent

This contract defines how an AI coding agent builds a layout that adapts across iPhone Duo's displays, poses, and fold states: resizable layout fundamentals, split views, the new arrangement-view container, fold behavior, and the full-screen exception for games. It assumes the hardware model in `designing-for-iphone-duo-anatomy` (displays, poses, reserved regions).

## Scope

### Included

-   Resizable-layout fundamentals (size classes, layout margins, safe area insets; avoiding fixed widths)
-   Cross-display consistency and hierarchy depth
-   Split-view fold adaptation
-   Arrangement views: split vs. overlay, and keeping navigation outside them
-   Fold-transition behavior (adapt, don't rearrange)
-   Game full-screen/aspect-ratio guidance under pose changes

### Excluded

-   Device anatomy, poses, and reserved-region definitions — see `designing-for-iphone-duo-anatomy`
-   Toolbar/tab bar vertical-axis placement — see `designing-for-iphone-duo-vertical-controls`
-   `NavigationSplitView`/`UISplitViewController` and reserved-region API implementation — see `swiftui`/`uikit` domains
-   General (non-Duo) iOS/iPadOS layout rules — see `human-interface-guidelines/layout`

## Rules

### Rule 1

Agents MUST build layouts that resize using size classes, layout margins, and safe area insets, and MUST avoid fixed widths or any display-specific dependency, since the app can appear at many sizes across displays, poses, and Split View multitasking. "Use size classes, layout margins, and safe area insets to lay out controls and content. Avoid fixed widths and display-specific dependencies."

### Rule 2

Agents MUST keep functionality and element state identical across displays, preserving the app's information hierarchy; agents MAY show one additional hierarchy level on the larger inner display when it suits the content (e.g., list-only when closed, list-and-detail side by side when open). "Keep functionality and the state of elements the same between displays... show an additional level of hierarchy on the larger inner display if it makes sense for your content."

### Rule 3

Agents MUST use a standard adaptive layout container (e.g., a split view) rather than a hand-rolled one so width and margins adjust to the fold automatically; in a grid layout, agents SHOULD prefer an even column count so content divides cleanly across the fold. "Prefer a layout container that adapts automatically, like the split view in Notes that adjusts the width of each pane to stay clearly visible as the device folds. In a grid-style layout, prefer an even number of columns so content divides cleanly."

### Rule 4

Agents MUST NOT make extreme layout changes as the device folds — move only what's necessary to keep elements visible and tappable, since controls that disappear or shift dramatically are harder to find and track. "Avoid extreme layout changes as people fold the device... favor small adjustments over rearrangement."

### Rule 5

Agents SHOULD choose a split arrangement (primary/secondary views divided into two areas, splitting horizontally when wider-than-tall and vertically when taller-than-wide) for a layout that already resembles a side-by-side or stacked stack, and an overlay arrangement (views layered on top of one another, separating to each side only while partially folded) for a layout that already resembles a layered stack. Agents MUST keep navigation containers outside an arrangement view, since an arrangement view lays out content but does not handle navigation. "A layout that places two views side by side or one above the other... translates directly to a split arrangement. A layout that layers one view over another... translates to an overlay arrangement... place navigation containers... around it rather than within it."

### Rule 6

For games, agents SHOULD prefer changing the aspect ratio over letterboxing or pillarboxing as the device pose changes, and SHOULD keep text and control sizes consistent while resizing; if letterboxing or pillarboxing can't be avoided, agents SHOULD add artwork to the padding area to preserve a full-screen feel. "Prefer changing the aspect ratio over letterboxing or pillarboxing in games; if you can't avoid letterboxing or pillarboxing, add artwork to the padding area to help the experience feel full screen."

## Compliant Example

-   ✓ A split view's pane widths and margins adjust automatically as the device folds, instead of the app recomputing pixel widths itself. (Rule 3)
-   ✓ An HStack-shaped two-pane screen is expressed as a split arrangement, with its navigation stack wrapped around it rather than placed inside it. (Rule 5)

## Non-Compliant Example

-   ✗ A fixed-pixel-width panel clips or overlaps content as the display size changes. (Rule 1)
-   ✗ Buttons jump to entirely new positions and an unrelated section collapses the moment the device is folded halfway. (Rule 4)

## Dependencies

-   `knowledge.human-interface-guidelines.designing-for-iphone-duo-anatomy` — reserved regions and device poses this contract's rules assume.

## References

-   [Apple HIG — Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
