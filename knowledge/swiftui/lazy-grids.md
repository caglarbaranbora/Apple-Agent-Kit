# Lazy Grids

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.lazy-grids
type: knowledge
title: Lazy Grids
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when to use LazyVGrid/LazyHGrid and LazyVStack/LazyHStack instead of eager stacks or List, for large or dynamic content inside a ScrollView.
domain: SwiftUI
tags:
  - swiftui
  - layout
  - performance
references:
  - https://developer.apple.com/documentation/swiftui/lazyvgrid
  - https://developer.apple.com/documentation/swiftui/lazyvstack
depends_on: []
related:
  - knowledge.swiftui.stacks-and-spacing
  - knowledge.swiftui.geometry-reader-anti-pattern
updated: 2026-08-01
```

## Intent

This contract defines when an AI coding agent must use lazy containers
(`LazyVStack`/`LazyHStack`, `LazyVGrid`/`LazyHGrid`) instead of eager
stacks or a `ScrollView`-wrapped `List`, for correctness and
performance with large or dynamic data.

## Scope

### Included

-   `LazyVStack`/`LazyHStack` vs `VStack`/`HStack` in a `ScrollView`
-   `LazyVGrid`/`LazyHGrid` with `GridItem` specs
-   `List` vs `ScrollView` + lazy stack trade-off
-   `GridItem` sizing strategies

### Excluded

-   Stack alignment/spacing fundamentals — see `stacks-and-spacing`

## Rules

### Rule 1

Agents MUST use `LazyVStack`/`LazyHStack` (not `VStack`/`HStack`) inside
a `ScrollView` when rendering a data-driven list of unbounded or large
size — non-lazy stacks instantiate every child view immediately.

### Rule 2

Agents MUST use `LazyVGrid`/`LazyHGrid` with `GridItem` column/row specs
for grid layouts of dynamic collections, rather than manually chunking
data into rows of `HStack`s inside a `VStack`.

### Rule 3

Agents MUST NOT wrap a `List` inside a `ScrollView` — `List` is already
scrollable, and nesting causes scroll-gesture conflicts.

### Rule 4

Agents SHOULD prefer `List` over `LazyVStack` in a `ScrollView` when
default list styling (swipe actions, section headers, platform chrome)
is acceptable — `List` already includes lazy loading.

### Rule 5

Agents SHOULD size `GridItem` with `.adaptive(minimum:)` for content
that should reflow its column count by available width, and
`.fixed(_:)`/`.flexible()` when a specific fixed or proportional column
count is required.

## Compliant Example

```swift
ScrollView {
    LazyVGrid(columns: [GridItem(.adaptive(minimum: 120))], spacing: 16) {
        ForEach(items) { item in
            ItemCell(item: item)
        }
    }
}
```
Lazy grid with adaptive columns for a dynamic collection. (Rules 2, 5)

## Non-Compliant Example

```swift
ScrollView {
    VStack {
        ForEach(items) { item in
            ItemCell(item: item)
        }
    }
}
```
Eager `VStack` inside `ScrollView` builds every row immediately, regardless of visibility. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid)
-   [Apple Developer — LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack)
