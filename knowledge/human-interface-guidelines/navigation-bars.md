# Navigation Bars

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.navigation-bars
artifact_type: knowledge
title: Navigation Bars
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for the iOS/iPadOS top navigation bar — titles, back/close controls, and leading/trailing item placement.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - navigation-bars
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/toolbars
depends_on: []
related:
  - knowledge.human-interface-guidelines.tab-bars
  - knowledge.style-guide.navigation-controls
  - knowledge.human-interface-guidelines.layout
last_updated: 2026-08-06
```

## Intent

Apple has merged its former standalone "Navigation Bars" page into the
"Toolbars" HIG page (the `navigation-bars` URL now redirects there; the
page states "In iOS, a navigation-specific toolbar is sometimes called
a navigation bar"). This contract scopes strictly to that
navigation-specific subset for iOS/iPadOS: screen titles, back/close
controls, and leading/center/trailing item placement — not general
toolbar action-button guidance.

## Scope

### Included

-   Screen/window title conventions
-   Standard Back/Close control usage
-   Large title behavior on scroll (iOS)
-   Leading/trailing edge content placement
-   Combining a navigation bar with a tab bar (iPadOS)

### Excluded

-   General toolbar action-item selection/grouping (non-navigation) — out of scope for this contract
-   SwiftUI `NavigationStack`/UIKit `UINavigationController` implementation — see `swiftui`/`uikit` domains
-   Title copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST give each screen a concise, useful title — not the app's
own name — so people can confirm their location and distinguish
between windows.

### Rule 2

Agents MUST use the standard Back and Close symbols and behavior for
hierarchical and modal dismissal respectively, without replacing them
with custom "Back"/"Close" text labels.

### Rule 3

Agents SHOULD use a large title on iOS that automatically transitions
to a standard/compact title as content scrolls, and back again at the
top, to reinforce location during scrolling.

### Rule 4

Agents MUST reserve the leading edge of the navigation bar for
back/sidebar navigation controls and the title, and reserve the
trailing edge for the primary action and any controls that must stay
available regardless of window width.

### Rule 5

Agents SHOULD move less-essential actions into a More menu rather than
crowding the visible bar, prioritizing only the most important actions
for direct placement.

### Rule 6

Agents SHOULD apply a single prominent (tinted) style to one key
trailing action (such as Done or Submit) rather than tinting multiple
bar items, to keep a clear focal point.

### Rule 7

Agents SHOULD allow a navigation bar to share horizontal space with a
tab bar on iPadOS when navigating between a few top-level areas while
keeping full width available for content.

## Compliant Example

-   ✓ A detail screen's title is a short noun phrase describing content, not the app's name. (Rule 1)
-   ✓ The Back button uses the standard chevron symbol with no "Back" text label. (Rule 2)
-   ✓ On iPadOS, a compact top bar combines navigation controls and a tab bar in the same row without crowding. (Rule 7)

## Non-Compliant Example

-   ✗ Every screen's title bar reads the app's own name. (Rule 1)
-   ✗ A custom "Back" text button replaces the system back control. (Rule 2)
-   ✗ Six equally weighted actions are crammed into the trailing edge with no More menu. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) (the former `navigation-bars` URL now redirects here)
