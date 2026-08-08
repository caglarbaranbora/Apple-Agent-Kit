# Searching

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.searching
artifact_type: knowledge
title: Searching
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines design rules for in-app search placement, scope, and suggestions, and for making app content discoverable through systemwide Spotlight search on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - searching
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/searching
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent places and structures
search on iOS/iPadOS: where the search field lives, how scope is
communicated, what suggestions to offer, and how app content should
participate in systemwide Spotlight search.

## Scope

### Included

-   Placement and prominence of an in-app search field
-   Single vs. per-section (local) search locations
-   Communicating current search scope
-   Recent searches and predictive suggestions
-   Search-history privacy
-   Making app content indexable by systemwide Spotlight search

### Excluded

-   Search field/result implementation code
-   Search suggestion copy/wording — see `style-guide`
-   Core Spotlight indexing API implementation

## Rules

### Rule 1

Agents MUST give search a primary, prominent position (e.g., a
toolbar search field or a dedicated tab) when search is important to
the app's purpose.

### Rule 2

Agents SHOULD consolidate app-wide search into a single, clearly
identified location; a local, section-scoped search that acts as a
filter on the current view is acceptable for apps with clearly
distinct sections.

### Rule 3

Agents MUST clearly communicate the current scope of a search —
through placeholder text, a scope bar, or a title — so people know
what they're searching.

### Rule 4

Agents SHOULD personalize search with recent searches shown before
typing and predictive suggestions, completions, or corrections shown
while typing.

### Rule 5

Agents MUST provide a way to clear search history if search history
is displayed, since people may not want it visible to others.

### Rule 6

Agents SHOULD make the app's content indexable by Spotlight, with
descriptive metadata, so people can find it systemwide without
opening the app first.

## Compliant Example

-   ✓ A notes app puts a search field in its bottom toolbar alongside other primary actions. (Rule 1)
-   ✓ A mail app's search always shows which mailbox is currently being searched. (Rule 3)
-   ✓ A music app shows recent searches before typing and narrows suggestions as the person types. (Rule 4)

## Non-Compliant Example

-   ✗ Search is buried two menus deep in an app where finding content is a primary task. (Rule 1)
-   ✗ A search field gives no indication of whether it's searching the whole app or just the current folder. (Rule 3)
-   ✗ Search history is shown with no way to clear it. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Searching](https://developer.apple.com/design/human-interface-guidelines/searching)
