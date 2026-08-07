# GeometryReader Anti-Pattern

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.geometry-reader-anti-pattern
artifact_type: knowledge
title: GeometryReader Anti-Pattern
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the pitfalls of GeometryReader's greedy size-filling behavior and when it should and should not be used in a SwiftUI layout tree.
domain: SwiftUI
tags:
  - swiftui
  - layout
  - performance
references:
  - https://developer.apple.com/documentation/swiftui/geometryreader
depends_on: []
related:
  - knowledge.swiftui.lazy-grids
last_updated: 2026-08-01
```

## Intent

This contract defines when an AI coding agent may use `GeometryReader`
and when it must avoid it, since `GeometryReader` always greedily fills
all available space and frequently breaks the intrinsic sizing of
siblings or parents.

## Scope

### Included

-   Why `GeometryReader` breaks intrinsic content sizing
-   Nesting `GeometryReader` inside stacks
-   Scoped alternatives (`.background()`/`.overlay()`, `.frame()`, `.aspectRatio()`)
-   Legitimate direct uses

### Excluded

-   Lazy loading of large data sets — see `lazy-grids`

## Rules

### Rule 1

Agents MUST NOT wrap a view in `GeometryReader` solely to read a size
for a computation unrelated to that view's own layout — `GeometryReader`
greedily fills all available space, which breaks the intrinsic sizing
of the view it wraps.

### Rule 2

Agents MUST NOT nest a `GeometryReader` inside a `VStack`/`HStack`
expecting it to size to its content — it expands to fill the stack's
available cross-axis space instead, distorting sibling layout.

### Rule 3

Agents SHOULD use `.frame(maxWidth:maxHeight:)`, `.aspectRatio()`, or a
size read scoped to `.background()`/`.overlay()` of an already-correctly
laid-out view when only a specific measured value is needed, rather
than placing a `GeometryReader` directly in the layout tree.

### Rule 4

Agents MAY use `GeometryReader` directly in the layout tree only when
the view genuinely needs to size or position itself relative to the
full available space it's given (e.g., a custom paginated carousel), and
the surrounding layout is designed to accommodate a greedy-filling
child.

## Compliant Example

```swift
Text("Title")
    .background(
        GeometryReader { proxy in
            Color.clear.preference(key: SizeKey.self, value: proxy.size)
        }
    )
```
`GeometryReader` scoped to `.background()` reads size without affecting `Text`'s own layout. (Rule 3)

## Non-Compliant Example

```swift
GeometryReader { proxy in
    VStack {
        Text("Title")
        Text("Subtitle")
    }
}
```
The `VStack` now stretches to `GeometryReader`'s full greedy size instead of hugging its content. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — GeometryReader](https://developer.apple.com/documentation/swiftui/geometryreader)
