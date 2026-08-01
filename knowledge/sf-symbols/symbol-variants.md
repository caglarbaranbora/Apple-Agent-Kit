# Symbol Variants

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-variants
type: knowledge
title: Symbol Variants
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of SF Symbols variant suffixes (.fill/.circle/.square/.slash) and the symbolVariant(_:) modifier for applying a variant across a view hierarchy.
domain: SF Symbols
tags:
  - sf-symbols
  - symbol-variants
  - symbolvariants
references:
  - https://developer.apple.com/documentation/swiftui/symbolvariants
depends_on:
  - knowledge.sf-symbols.symbol-basics
related: []
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent selects a symbol variant —
fill, circle, square, or slash — either per symbol name or app-wide via
the `.symbolVariant(_:)` environment modifier, so selected/emphasized
states render consistently without duplicating variant logic at every
call site.

## Scope

### Included

-   Variant name suffixes (`.fill`, `.circle`, `.square`, `.slash`)
-   `.symbolVariant(_:)` environment modifier
-   Verifying a requested variant exists for a given base symbol

### Excluded

-   Rendering mode (monochrome/hierarchical/palette/multicolor) — see `rendering-modes`
-   Which variant best expresses selected vs. unselected state as a design choice

## Rules

### Rule 1

Agents MUST use the `.symbolVariant(_:)` modifier to switch a variant
across an entire view hierarchy (e.g. all icons in a toolbar becoming
filled together) rather than string-concatenating suffixes onto
`systemName` at each call site — one environment value stays the single
source of truth instead of scattering the same suffix logic everywhere.

### Rule 2

Agents MUST verify a requested variant suffix actually exists for a
given base symbol name before use — not every SF Symbol ships every
variant; a nonexistent suffixed name resolves to `nil` the same as any
other invalid name (see `symbol-basics` Rule 2).

### Rule 3

Agents SHOULD use the `.fill` variant for selected/active/emphasized
states and the unsuffixed (outline) form for default/unselected states,
matching the convention used throughout system UI (e.g. tab bar
selection).

### Rule 4

Agents MUST NOT combine the `.slash` variant with `.multicolor`
rendering without visually verifying the result — the slash overlay can
visually conflict with a multicolor symbol's authored layer coloring.

## Compliant Example

```swift
struct SelectableIcon: View {
    let isSelected: Bool

    var body: some View {
        Image(systemName: "heart")
            .symbolVariant(isSelected ? .fill : .none)
    }
}
```
A single environment-driven variant toggle instead of building two separate `systemName` strings. (Rules 1, 3)

## Non-Compliant Example

```swift
Image(systemName: isSelected ? "heart.fill" : "heart")
    .symbolVariant(.circle)
```
Manually building the fill/outline suffix in the `systemName` string while also applying `.symbolVariant(.circle)` on top — the two mechanisms compound unpredictably rather than using one consistent variant strategy. (Rule 1)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — variants apply to a symbol already resolved by name.

## References

-   [Apple Developer — SymbolVariants](https://developer.apple.com/documentation/swiftui/symbolvariants)
