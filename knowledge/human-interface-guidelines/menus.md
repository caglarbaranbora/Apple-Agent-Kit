# Menus

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.menus
artifact_type: knowledge
title: Menus
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for menu item availability, ordering/grouping, icon consistency, submenu depth, and iOS/iPadOS menu layout.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - menus
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/menus
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
  - knowledge.human-interface-guidelines.sf-symbols
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent structures menus on
iOS/iPadOS: item availability and clarity, ordering and grouping, icon
consistency, submenu limits, toggled-item state, and menu layout
choice.

## Scope

### Included

-   Unavailable item presentation (dimmed, not hidden)
-   Item label clarity (one item = one action)
-   Ellipsis-style affordance for items needing further input
-   Priority ordering and logical grouping with separators
-   Icon consistency within a group
-   Submenu depth/length limits
-   Toggled-item state representation
-   iOS/iPadOS small/medium/large menu layout choice

### Excluded

-   SwiftUI `Menu`/UIKit `UIMenu` implementation — see `swiftui`/`uikit` domains
-   Menu item copy wording/capitalization — see `style-guide`

## Rules

### Rule 1

Agents MUST show an unavailable menu item in a dimmed/disabled state
rather than hiding it, so the menu itself remains discoverable and
openable even when all its items are unavailable.

### Rule 2

Agents MUST ensure each menu item's label clearly and succinctly
describes exactly one action or state.

### Rule 3

Agents SHOULD visually indicate when choosing a menu item requires
further input before the action completes (such as an
ellipsis-style affordance).

### Rule 4

Agents SHOULD order menu items with the most important/frequently used
items first, and group logically related items together, separated
visually from unrelated groups.

### Rule 5

Agents MUST apply icons consistently within a group — either all items
in a group have an icon or none do.

### Rule 6

Agents SHOULD restrict submenus to a single level of depth and to
roughly five or fewer items, using a submenu instead of indenting
related items.

### Rule 7

Agents on iOS/iPadOS SHOULD choose a menu layout — small (icon row),
medium (icon+label row), or large (default list) — appropriate to how
many high-priority actions the context has, reserving small/medium
layouts for closely related or especially frequent actions.

## Compliant Example

-   ✓ A disabled "Merge Duplicates" menu item appears dimmed rather than being removed from the menu. (Rule 1)
-   ✓ Cut, Copy, and Paste are grouped together and separated from unrelated commands. (Rule 4)
-   ✓ A notes app uses the medium layout for its three most common actions. (Rule 7)

## Non-Compliant Example

-   ✗ A "Sort By" menu item silently disappears instead of appearing dimmed when sorting is unavailable. (Rule 1)
-   ✗ A submenu nests three levels deep to organize export formats. (Rule 6)
-   ✗ Only some items in the Edit group have icons while others in the same group don't. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
