# Modifier Order

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.modifier-order
artifact_type: knowledge
title: Modifier Order
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines that SwiftUI view modifiers apply in the order written, each wrapping the view in a new view, and that order changes the rendered result.
domain: SwiftUI
tags:
  - swiftui
  - views
  - modifiers
references:
  - https://developer.apple.com/documentation/swiftui/viewmodifier
depends_on: []
related:
  - knowledge.swiftui.stacks-and-spacing
  - knowledge.swiftui.view-composition
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent orders chained view
modifiers (`.padding()`, `.background()`, `.frame()`, `.clipShape()`,
etc.) so the rendered result matches intent, since each modifier wraps
the view rather than mutating it in place.

## Scope

### Included

-   `.padding()` vs `.background()` ordering
-   `.frame()` vs `.background()` ordering
-   Non-commutativity of sizing/appearance modifiers
-   `.clipShape()`/`.overlay()` ordering for matching borders

### Excluded

-   Which stack/alignment to use — see `stacks-and-spacing`
-   View decomposition itself — see `view-composition`

## Rules

### Rule 1

Agents MUST apply `.background()` after `.padding()` when the
background is meant to cover the padded area — `.background()` only
fills the view's bounds at the point it's applied in the chain.

### Rule 2

Agents MUST apply `.frame()` before `.background()` when the background
should fill the frame's size — a `.background()` applied before
`.frame()` only fills the pre-frame size.

### Rule 3

Agents MUST NOT assume modifier order is commutative — `.padding()`
followed by `.frame(width:)` adds padding inside a fixed frame, while
`.frame(width:)` followed by `.padding()` adds padding outside the
frame, growing the total size.

### Rule 4

Agents SHOULD apply `.clipShape()` after `.frame()` and before
`.overlay()` when adding a border stroke that must match the clip
shape's edge.

## Compliant Example

```swift
Text("Hello")
    .padding()
    .background(Color.blue)
    .clipShape(RoundedRectangle(cornerRadius: 8))
```
Padding is applied first, so the background fills the padded area. (Rule 1)

## Non-Compliant Example

```swift
Text("Hello")
    .background(Color.blue)
    .padding()
```
Background applied before padding only colors the text's own bounds; the padding area around it stays uncolored. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — ViewModifier](https://developer.apple.com/documentation/swiftui/viewmodifier)
