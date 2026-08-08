# Tab Bars

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.tab-bars
artifact_type: knowledge
title: Tab Bars
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for using a tab bar for top-level app navigation on iOS/iPadOS, including visibility, tab count, and labeling.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - tab-bars
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/tab-bars
depends_on: []
related:
  - knowledge.human-interface-guidelines.navigation-bars
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.style-guide.navigation-controls
last_updated: 2026-08-08
```

## Intent

This contract defines when an AI coding agent should use a tab bar on
iOS/iPadOS, how many tabs to show, and conventions for visibility,
labeling, and badges, so top-level navigation stays predictable.

## Scope

### Included

-   Tab bar vs. toolbar (navigation vs. action) decision
-   Tab bar visibility persistence
-   Tab count and overflow guidance
-   Tab labeling and SF Symbols icon usage
-   Badge usage
-   iPadOS sidebar-convertible tab bar

### Excluded

-   SwiftUI `TabView`/UIKit `UITabBarController` implementation — see `swiftui`/`uikit` domains
-   Tab label copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST use a tab bar for top-level navigation between sections,
not for actions that operate on the current view's content — use a
toolbar instead for those.

### Rule 2

Agents MUST keep the tab bar visible as people move between top-level
sections; hiding it (other than a temporary modal covering it) causes
people to lose track of where they are in the app.

### Rule 3

Agents MUST NOT disable or hide a tab bar button when its section's
content is unavailable — the tab MUST remain reachable, with the empty
state explained within that section.

### Rule 4

Agents SHOULD choose the smallest number of tabs that adequately
covers the app's top-level sections, since fewer tabs are easier to
navigate; consider a sidebar-convertible tab bar on iPadOS for complex
hierarchies.

### Rule 5

Agents SHOULD include a short (ideally one-word) label beneath or
beside each tab's icon to aid navigation, and prefer SF Symbols so
icons adapt automatically between compact and regular layouts.

### Rule 6

Agents SHOULD avoid relying on an overflow ("More") tab where
possible — content behind it is harder to discover — by prioritizing
which tabs are visible instead of overloading the bar.

### Rule 7

Agents SHOULD reserve badges for genuinely critical, attention-worthy
information rather than routine updates, to preserve their meaning.

## Compliant Example

-   ✓ Five or fewer top-level sections are represented in the tab bar with SF Symbols icons and one-word labels. (Rule 4, Rule 5)
-   ✓ An empty "Downloads" tab remains selectable and explains why it's empty instead of being disabled. (Rule 3)

## Non-Compliant Example

-   ✗ The tab bar disappears when navigating into a section, leaving no persistent orientation cue. (Rule 2)
-   ✗ A tab is grayed out and untappable because its content is currently empty. (Rule 3)
-   ✗ Eight top-level tabs push several items into a "More" overflow list by default. (Rule 6)

## Dependencies

None.

## References

-   [Apple HIG — Tab Bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
