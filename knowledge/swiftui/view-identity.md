# View Identity

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.view-identity
type: knowledge
title: View Identity
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to give ForEach/List content stable, correct identity to avoid state loss, animation glitches, and wrong-row bugs after data mutation.
domain: SwiftUI
tags:
  - swiftui
  - views
  - identity
references:
  - https://developer.apple.com/documentation/swiftui/foreach
  - https://developer.apple.com/documentation/swift/identifiable
depends_on: []
related:
  - knowledge.swiftui.state-and-binding
  - knowledge.swiftui.view-composition
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent assigns identity to
`ForEach`/`List` content and understands SwiftUI's structural identity
rules, so that state and animations stay attached to the correct
logical item as data changes.

## Scope

### Included

-   Stable `id`/`Identifiable` requirement for `ForEach`/`List`
-   Index-based identity pitfalls for mutable collections
-   Structural identity (`if`/`switch` branches) and the `.id()` modifier

### Excluded

-   General view decomposition — see `view-composition`
-   `@State` ownership rules themselves — see `state-and-binding`

## Rules

### Rule 1

Agents MUST supply a stable, unique identity for `ForEach`/`List`
content — via `Identifiable` conformance or an explicit `id:` parameter
— that stays attached to the same logical item across re-renders.

### Rule 2

Agents MUST NOT use array index as the identity (`id: \.self` on
`.indices`) for a collection whose order or membership can change
(insert/delete/reorder) — this attaches a row's state/animation to the
wrong item after mutation.

### Rule 3

Agents MUST NOT generate an id inline in `body` (e.g., `UUID()` created
during view evaluation) — this creates a new identity every render,
defeating diffing and causing state loss or flicker.

### Rule 4

Agents SHOULD use the `.id(_:)` modifier deliberately when the intent is
to force a view's identity to reset (e.g., clearing internal `@State`
when navigating to a different item), understanding that changing which
`if`/`switch` branch renders also creates a new identity and resets any
`@State` inside that branch.

## Compliant Example

```swift
struct Item: Identifiable {
    let id: UUID
    var title: String
}

ForEach(items) { item in
    ItemRow(item: item)
}
```
Stable `Identifiable` conformance keeps each row's identity attached to its item. (Rule 1)

## Non-Compliant Example

```swift
ForEach(items.indices, id: \.self) { index in
    ItemRow(item: items[index])
}
```
Index identity: deleting item 0 makes every subsequent row's identity shift, losing per-row state and mis-animating the delete. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — ForEach](https://developer.apple.com/documentation/swiftui/foreach)
-   [Apple Developer — Identifiable](https://developer.apple.com/documentation/swift/identifiable)
