# Navigation Stack

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.navigation-stack
type: knowledge
title: Navigation Stack
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the use of NavigationStack and NavigationPath for stack-based push/pop navigation, including programmatic and deep-link navigation.
domain: SwiftUI
tags:
  - swiftui
  - navigation
references:
  - https://developer.apple.com/documentation/swiftui/navigationstack
  - https://developer.apple.com/documentation/swiftui/navigationpath
depends_on: []
related:
  - knowledge.swiftui.navigation-split-view
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent implements stack-based
(push/pop) navigation in SwiftUI using `NavigationStack` and
`NavigationPath`, including programmatic and deep-link navigation.

## Scope

### Included

-   `NavigationStack` as the stack-based navigation container
-   `NavigationPath`-driven programmatic navigation
-   `.navigationDestination(for:)` type-keyed destinations
-   Nesting restrictions

### Excluded

-   Multi-column sidebar/detail navigation — see `navigation-split-view`
-   Legacy `NavigationView` migration guidance — out of scope for v1

## Rules

### Rule 1

Agents MUST use `NavigationStack` (not the deprecated `NavigationView`)
as the root container for stack-based push/pop navigation.

### Rule 2

Agents MUST drive programmatic navigation through a bound
`NavigationPath` (or a typed `[Value]` path) rather than wiring manual
boolean `isActive` flags per destination.

### Rule 3

Agents MUST declare destinations with `.navigationDestination(for:)`
keyed by the pushed data type, not by manually toggling per-destination
view state.

### Rule 4

Agents MUST NOT nest a `NavigationStack` inside another
`NavigationStack` within the same navigation hierarchy — nested stacks
produce ambiguous back-stack behavior.

### Rule 5

Agents SHOULD keep the `NavigationPath` state at the point in the view
hierarchy that owns the navigation flow (e.g., a `@State` on the
stack's root), so a deep link can push directly by appending to the
path.

## Compliant Example

```swift
@State private var path = NavigationPath()

NavigationStack(path: $path) {
    RootView()
        .navigationDestination(for: Item.self) { item in
            DetailView(item: item)
        }
}
```
Programmatic push via `NavigationPath`, type-keyed destination. (Rules 2, 3)

## Non-Compliant Example

```swift
NavigationView {
    NavigationLink(destination: DetailView(), isActive: $showDetail) {
        EmptyView()
    }
}
```
Deprecated `NavigationView` with a manual `isActive` boolean per destination. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)
-   [Apple Developer — NavigationPath](https://developer.apple.com/documentation/swiftui/navigationpath)
