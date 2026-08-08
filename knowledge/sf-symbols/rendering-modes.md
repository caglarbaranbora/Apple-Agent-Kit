# Rendering Modes

Status: Draft Version: 0.2.0

## Metadata

``` yaml
id: knowledge.sf-symbols.rendering-modes
artifact_type: knowledge
title: Rendering Modes
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of SF Symbols rendering modes (monochrome, hierarchical, palette, multicolor) via symbolRenderingMode in SwiftUI and UIImage.SymbolConfiguration in UIKit.
domain: SF Symbols
tags:
  - sf-symbols
  - rendering-modes
  - symbolrenderingmode
references:
  - https://developer.apple.com/documentation/swiftui/symbolrenderingmode
  - https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.sf-symbols.symbol-color-and-tinting
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent selects and applies one of
the four SF Symbols rendering modes — monochrome, hierarchical, palette,
multicolor — in code, so a symbol's layered structure renders the way its
design intends instead of defaulting to whatever automatic mode picks.

## Scope

### Included

-   `.symbolRenderingMode(_:)` in SwiftUI
-   `UIImage.SymbolConfiguration` rendering-mode equivalents in UIKit
-   Matching a rendering mode to a symbol's layered/multicolor capability

### Excluded

-   Which specific colors to apply — see `symbol-color-and-tinting`
-   Which rendering mode best expresses a given design meaning — a design
    decision owned by `human-interface-guidelines`'s `sf-symbols.md`

## Rules

### Rule 1

Agents MUST set an explicit `.symbolRenderingMode(_:)` (SwiftUI) or a
`UIImage.SymbolConfiguration` with a matching mode (UIKit) rather than
relying on the automatic default when a symbol's layered structure
carries meaning (e.g. a palette-colored status icon) — automatic mode may
not select the layered rendering that conveys per-part color.

### Rule 2

Agents MUST pair `.multicolor` rendering only with a symbol whose SF
Symbols definition is authored as multicolor-capable — applying
`.multicolor` to a plain monochrome-only symbol has no visible effect
beyond default rendering.

### Rule 3

Agents MUST pair `.palette` rendering with explicit per-layer colors
(`.foregroundStyle(_:_:_:)` in SwiftUI, `UIImage.SymbolConfiguration(paletteColors:)`
in UIKit) — palette mode with no explicit colors supplied falls back to
default coloring, which may not match design intent.

### Rule 4

Agents SHOULD prefer `.hierarchical` over manually recoloring layers with
`.palette` when a single-color symbol just needs depth (e.g. a filled
shape with a brighter accent on one part) — hierarchical derives shades
from one base color automatically, without specifying per-layer colors.

## Compliant Example

```swift
struct StatusBadge: View {
    var body: some View {
        Image(systemName: "checkmark.seal.fill")
            .symbolRenderingMode(.hierarchical)
            .foregroundStyle(.green)
    }
}

// UIKit
let config = UIImage.SymbolConfiguration(hierarchicalColor: .systemGreen)
let imageView = UIImageView(image: UIImage(systemName: "checkmark.seal.fill"))
imageView.preferredSymbolConfiguration = config
```
Explicit hierarchical mode with one base color, applied consistently in both frameworks. (Rules 1, 4)

## Non-Compliant Example

```swift
Image(systemName: "star.fill")
    .symbolRenderingMode(.multicolor)
```
`star.fill` has no multicolor-authored definition, so `.multicolor` here renders identically to the default — no visible effect, misleading to a reader expecting distinct layer colors. (Rule 2)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — rendering modes apply to a symbol already resolved by name.

## References

-   [Apple Developer — SymbolRenderingMode](https://developer.apple.com/documentation/swiftui/symbolrenderingmode)
-   [Apple Developer — UIImage.SymbolConfiguration](https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class)
