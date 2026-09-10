# Designing for iPhone Duo — Vertical Controls

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.designing-for-iphone-duo-vertical-controls
artifact_type: knowledge
title: Designing for iPhone Duo — Vertical Controls
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for toolbars, tab bars, and navigation controls placed on iPhone Duo's vertical axis — ordering, visibility priority, grouping, labeling, overflow compression, and Split View multitasking placement.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - designing-for-iphone-duo
  - foldable
  - toolbars
  - tab-bars
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo
depends_on:
  - knowledge.human-interface-guidelines.designing-for-iphone-duo-anatomy
related:
  - knowledge.human-interface-guidelines.designing-for-iphone-duo-layout
  - knowledge.human-interface-guidelines.tab-bars
  - knowledge.human-interface-guidelines.navigation-bars
last_updated: 2026-09-10
```

## Intent

This contract defines how an AI coding agent places and orders toolbars, tab bars, and navigation controls on iPhone Duo, where the system moves them to the vertical (side) axis to preserve vertical space for content. It extends, rather than replaces, the general `tab-bars`/`navigation-bars` contracts — those still govern when to use a tab bar or toolbar at all.

## Scope

### Included

-   When controls move to the vertical axis vs. stay horizontal
-   Vertical toolbar item ordering and grouping
-   Visibility priority and overflow behavior
-   Title/symbol requirements for vertical-axis items
-   Toolbar-vs-tab-bar compression choice under space pressure
-   Control placement when two apps share the inner display (Split View)

### Excluded

-   Device anatomy, poses, and reserved regions (the outer camera region controls align to) — see `designing-for-iphone-duo-anatomy`
-   General tab bar vs. toolbar usage rules — see `human-interface-guidelines/tab-bars` and `/navigation-bars`
-   `ToolbarItemVisibilityPriority`/`ToolbarItemGroup`/`UIBarButtonItemGroup` implementation — see `swiftui`/`uikit` domains

## Rules

### Rule 1

Agents MUST let the system place toolbars, tab bars, and navigation controls on the vertical axis by default — whenever the outer display is active and whenever the inner display is in landscape — and MUST NOT override the default bar placement; the sole exception is the inner display in portrait, which has enough vertical space to keep standard horizontal bars. "In general, don't override the default bar placement... The exception is the inner display in portrait, which has enough vertical space to keep standard horizontal bars."

### Rule 2

Agents MUST order vertical-axis toolbar items with primary navigation controls (Back, Close) at the top of the axis, followed by prominent actions (Done), and MUST preserve each item's original grouping from the horizontal bars, relying on the system-provided vertical space between top-origin and bottom-origin groups to keep them distinct. "Reserve the top of the vertical axis for primary navigation controls, like Back or Close, followed by prominent actions, like Done... Keep remaining toolbar items in their original groupings."

### Rule 3

Agents SHOULD assign a visibility priority to items and groups that need to appear earlier than the default bottom-to-top overflow order, prioritizing frequently used actions (e.g., Compose, New Note) and items that convey status (e.g., badges) so they stay visible longest. "Items overflow from bottom to top by default. Assign each item a visibility priority to change that order... Preserve frequently used actions first... and keep controls that convey important status... visible longer."

### Rule 4

Agents MUST group related toolbar items using a group construct (`ToolbarItemGroup`/`UIBarButtonItemGroup`) instead of adding manual spacing between them, since groups space themselves and adapt automatically as available space changes. "Groups you create with ToolbarItemGroup (SwiftUI) or UIBarButtonItemGroup (UIKit) provide space between items and other groups automatically... avoid adding fixed spacing yourself."

### Rule 5

Agents MUST give every toolbar item that isn't text-only both a title and a symbol — the title is used in overflow menus and expanded forms even when the item normally shows only a symbol — and SHOULD keep text-labeled buttons to a minimum, since labels with text stay confined to a horizontal bar. "Provide both a title and a symbol for each toolbar item that isn't text-only... Keep text-based buttons to a minimum... prefer a symbol wherever one works."

### Rule 6

When space is limited, agents MUST choose the compression strategy that matches the experience: for navigation-focused experiences, move toolbar items into the overflow menu and keep the tab bar and primary destinations accessible (the default behavior); for task-oriented experiences, minimize the tab bar to preserve the toolbar actions central to completing the task. Any app-specific overflow menu MUST be merged into the system overflow menu, reserving the ellipsis symbol for overflow. "In navigation-focused experiences, move toolbar items into the overflow menu... In task-oriented experiences, minimize the tab bar... If your app has its own overflow menu, move those actions into the system menu."

### Rule 7

When two apps share the inner display under Split View multitasking, agents MUST keep each app's controls along its own outer edge and MUST use safe areas so neither app's controls cover its own or the other app's content. "When two apps share the inner display with Split View multitasking, each one places controls along its outer edge... Use safe areas to make sure controls don't cover your content, including controls on the opposite edge."

## Compliant Example

-   ✓ A detail screen's Back button sits at the top of the vertical toolbar, Done directly below it, with remaining actions grouped exactly as they were in the horizontal bar. (Rule 2)
-   ✓ A task-oriented editor minimizes its tab bar under space pressure to keep its toolbar actions available. (Rule 6)

## Non-Compliant Example

-   ✗ The app forces its toolbar to stay horizontal on the outer display, contradicting the system default. (Rule 1)
-   ✗ In Split View, the right-hand app's controls sit on its left edge, colliding with the left-hand app's content. (Rule 7)

## Dependencies

-   `knowledge.human-interface-guidelines.designing-for-iphone-duo-anatomy` — the outer camera region vertical-axis controls stay aligned to.

## References

-   [Apple HIG — Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
