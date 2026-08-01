# Symbol Color and Tinting

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-color-and-tinting
type: knowledge
title: Symbol Color and Tinting
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the code-level mechanics of coloring an SF Symbol with foregroundStyle in SwiftUI and tintColor in UIKit, matched to the active rendering mode.
domain: SF Symbols
tags:
  - sf-symbols
  - color
  - tinting
references:
  - https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:)
  - https://developer.apple.com/documentation/uikit/uiview/tintcolor
depends_on:
  - knowledge.sf-symbols.rendering-modes
related:
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-01
```

## Intent

This contract defines the code-level mechanics of applying color to an SF
Symbol — `.foregroundStyle(_:_:_:)` in SwiftUI, `tintColor` in UIKit —
matched correctly to the symbol's active rendering mode, so a color
override actually takes visible effect instead of being silently ignored
by an incompatible mode.

## Scope

### Included

-   `.foregroundStyle(_:_:_:)` argument count matched to rendering mode
-   `UIImageView.tintColor` inheritance and system color usage
-   Why `.multicolor` rendering ignores foreground color overrides

### Excluded

-   Which specific color to choose for a given design context — a design
    decision owned by `human-interface-guidelines`'s `sf-symbols.md`
-   Selecting the rendering mode itself — see `rendering-modes`

## Rules

### Rule 1

Agents MUST supply exactly as many colors to `.foregroundStyle(_:_:_:)`
as the active rendering mode expects — one for monochrome/hierarchical's
base color, up to three for `.palette` (one per layer) — supplying fewer
leaves the remaining layers at their default color, and supplying more is
ignored.

### Rule 2

Agents MUST use `UIImageView.tintColor` (inherited from the view
hierarchy when left unset) for monochrome/hierarchical UIKit symbols,
rather than baking a fixed color into the image itself — `tintColor`
responds to view-hierarchy overrides and system appearance changes
automatically.

### Rule 3

Agents MUST NOT set `.foregroundStyle` or `tintColor` expecting it to
recolor a `.multicolor`-rendered symbol's built-in colors — multicolor
rendering uses the symbol's authored palette and ignores foreground color
overrides for its multicolor layers.

### Rule 4

Agents SHOULD use system colors (`Color.primary`/`.secondary`,
`UIColor.label`/`.secondaryLabel`) rather than fixed RGB values so a
symbol's tint adapts automatically to Dark Mode and increased-contrast
settings — deciding *which* system color fits a given context remains a
design decision owned by `human-interface-guidelines`'s `sf-symbols.md`.

## Compliant Example

```swift
Image(systemName: "flag.fill")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.white, .red)
```
Two colors supplied for a two-layer palette symbol, matching the rendering mode's expected color count. (Rule 1)

## Non-Compliant Example

```swift
let imageView = UIImageView(image: multicolorFlagSymbol)
imageView.tintColor = .red
```
`tintColor` set on a `.multicolor`-rendered symbol — has no visible effect because multicolor rendering ignores tint/foreground overrides for its authored layer colors. (Rule 3)

## Dependencies

- `knowledge.sf-symbols.rendering-modes` — color application depends on the active rendering mode.

## References

-   [Apple Developer — foregroundStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:))
-   [Apple Developer — UIView.tintColor](https://developer.apple.com/documentation/uikit/uiview/tintcolor)
