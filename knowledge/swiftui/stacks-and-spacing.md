# Stacks and Spacing

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.swiftui.stacks-and-spacing
artifact_type: knowledge
title: Stacks and Spacing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of VStack/HStack/ZStack, Spacer, alignment, and the spacing parameter for arranging views — the code-implementation angle, distinct from human-interface-guidelines' visual-design angle on layout.
domain: SwiftUI
tags:
  - swiftui
  - layout
references:
  - https://developer.apple.com/documentation/swiftui/vstack
  - https://developer.apple.com/documentation/swiftui/hstack
  - https://developer.apple.com/documentation/swiftui/zstack
depends_on: []
related:
  - knowledge.swiftui.safe-area
  - knowledge.swiftui.lazy-grids
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent arranges views with
`VStack`/`HStack`/`ZStack`, `Spacer`, alignment, and the `spacing:`
parameter — the SwiftUI code-implementation angle. Whether a given
spacing/alignment choice is HIG-compliant is a separate, visual-design
question owned by `human-interface-guidelines`'s `layout.md` (see
docs/architecture/domain-map.md Cross-Domain Notes).

## Scope

### Included

-   Choosing the correct stack axis
-   `Spacer()` vs fixed-size gaps
-   Stack `alignment:` and `spacing:` parameters

### Excluded

-   Whether a layout is HIG-compliant (visual-design angle) — see `human-interface-guidelines`'s `layout.md`
-   Safe-area edge handling — see `safe-area`
-   Lazy/grid layout for large data sets — see `lazy-grids`

## Rules

### Rule 1

Agents MUST choose the stack axis (`VStack` for vertical, `HStack` for
horizontal) that matches the intended layout direction rather than
faking linear layout with a `ZStack` and manual offsets.

### Rule 2

Agents MUST use `Spacer()` (optionally with `minLength:`) to distribute
remaining space, not a hard-coded `Spacer().frame(height:)`-style
magic-number gap meant to push content.

### Rule 3

Agents MUST NOT use `Spacer(minLength: 0)` when the intent is a fixed
gap between two elements — use `.padding()` or a sized `Color.clear`
spacer for a deliberate fixed gap instead.

### Rule 4

Agents SHOULD set a stack's `alignment:` parameter explicitly when the
default (`.center`) doesn't match the design, instead of nesting extra
`HStack { content; Spacer() }` wrappers to fake leading alignment.

### Rule 5

Agents SHOULD use the stack initializer's `spacing:` parameter for
uniform gaps between all children rather than adding `.padding(.bottom:)`
to each child individually.

## Compliant Example

```swift
VStack(alignment: .leading, spacing: 12) {
    Text("Title")
    Text("Subtitle")
}
```
Explicit alignment and uniform spacing via the initializer. (Rules 4, 5)

## Non-Compliant Example

```swift
VStack {
    Text("Title")
    Spacer().frame(height: 12)
    Text("Subtitle")
}
```
A `Spacer` constrained to a fixed height is really just a magic-number gap; `.padding()` or `spacing:` expresses the same intent directly. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — VStack](https://developer.apple.com/documentation/swiftui/vstack)
-   [Apple Developer — HStack](https://developer.apple.com/documentation/swiftui/hstack)
-   [Apple Developer — ZStack](https://developer.apple.com/documentation/swiftui/zstack)
