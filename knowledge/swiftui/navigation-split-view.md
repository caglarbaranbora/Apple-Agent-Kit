# Navigation Split View

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.navigation-split-view
type: knowledge
title: Navigation Split View
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the use of NavigationSplitView for adaptive multi-column sidebar/content/detail navigation.
domain: SwiftUI
tags:
  - swiftui
  - navigation
references:
  - https://developer.apple.com/documentation/swiftui/navigationsplitview
depends_on: []
related:
  - knowledge.swiftui.navigation-stack
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent implements adaptive
multi-column (sidebar/content/detail) navigation using
`NavigationSplitView`, and how it composes with `NavigationStack`.

## Scope

### Included

-   `NavigationSplitView` for sidebar/detail or sidebar/content/detail layouts
-   Selection-state binding across columns
-   Two-column vs three-column initializer choice
-   Composition with `NavigationStack` inside a column

### Excluded

-   Single-column push/pop navigation — see `navigation-stack`

## Rules

### Rule 1

Agents MUST use `NavigationSplitView` (not a manually built `HStack` of
columns) for sidebar–detail layouts that need to adapt between compact
and regular size classes.

### Rule 2

Agents MUST bind a single selection state to drive both the sidebar's
selected row and the detail column's content — not separate,
unsynchronized state per column.

### Rule 3

Agents MUST NOT use `NavigationSplitView` and `NavigationStack` as
siblings for the same navigational concern — nest a `NavigationStack`
inside the detail column only if that column itself needs push/pop
within the selected item.

### Rule 4

Agents SHOULD use the two-column initializer (`sidebar:detail:`) when
there is no distinct middle "content" list, and the three-column
initializer (`sidebar:content:detail:`) only when a genuine middle list
exists.

### Rule 5

Agents SHOULD rely on `NavigationSplitView`'s default adaptive/balanced
column behavior and only override width or style when the default does
not fit the design.

## Compliant Example

```swift
@State private var selection: Item?

NavigationSplitView {
    List(items, selection: $selection) { item in
        Text(item.title)
    }
} detail: {
    if let selection {
        DetailView(item: selection)
    } else {
        Text("Select an item")
    }
}
```
Single selection state drives both sidebar and detail. (Rule 2)

## Non-Compliant Example

```swift
HStack {
    SidebarView(onSelect: { selectedID = $0 })
    DetailView(id: detailID)
}
```
Hand-rolled columns with two unsynchronized selection variables and no adaptive collapsing on compact width. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)
