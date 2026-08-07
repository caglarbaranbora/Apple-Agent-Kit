# Symbol Weight and Scale

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-weight-and-scale
artifact_type: knowledge
title: Symbol Weight and Scale
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of fontWeight/imageScale in SwiftUI and UIImage.SymbolConfiguration(pointSize:weight:scale:) in UIKit to size and weight-match SF Symbols against adjacent content.
domain: SF Symbols
tags:
  - sf-symbols
  - weight
  - scale
references:
  - https://developer.apple.com/documentation/swiftui/view/imagescale(_:)
  - https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class/init(pointsize:weight:scale:)
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.sf-symbols.rendering-modes
  - knowledge.sf-symbols.symbol-color-and-tinting
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent sizes and weight-matches an
SF Symbol relative to adjacent text or a control's Dynamic Type size,
using scale and weight APIs rather than resizing the rendered image
directly, so the glyph stays crisp and visually consistent.

## Scope

### Included

-   `.imageScale(_:)` and `.fontWeight(_:)` in SwiftUI
-   `UIImage.SymbolConfiguration(pointSize:weight:scale:)` in UIKit
-   Matching symbol weight to adjacent text weight

### Excluded

-   Rendering mode and color — see `rendering-modes`, `symbol-color-and-tinting`
-   Dynamic Type text-sizing mechanics unrelated to symbols specifically

## Rules

### Rule 1

Agents MUST set `.imageScale(_:)` (SwiftUI) or
`UIImage.SymbolConfiguration(scale:)` (UIKit) to resize a symbol rather
than resizing its containing frame directly — frame-resizing stretches
or distorts the glyph, while scale re-renders it at the correct weight
for that size.

### Rule 2

Agents SHOULD match a symbol's `.fontWeight(_:)` to the weight of
adjacent text (e.g. both `.semibold`) so the symbol doesn't read as
visually heavier or lighter than the label next to it.

### Rule 3

Agents MUST supply `pointSize`, `weight`, and `scale` together in a
single `UIImage.SymbolConfiguration(pointSize:weight:scale:)` call when
precise UIKit sizing matters, rather than chaining several
single-parameter configurations — combining separately constructed
configurations can produce an unpredictable merged result depending on
application order.

### Rule 4

Agents MUST NOT apply a `.font(_:)` modifier to control a symbol's point
size when that symbol sits inside a control (e.g. `Label`) that also
derives its size from Dynamic Type — the explicit size can fight the
control's automatic Dynamic Type scaling. Use `.imageScale(_:)` instead.

## Compliant Example

```swift
HStack {
    Image(systemName: "bolt.fill")
        .imageScale(.medium)
        .fontWeight(.semibold)
    Text("Fast Charging")
        .fontWeight(.semibold)
}

// UIKit
let config = UIImage.SymbolConfiguration(pointSize: 20, weight: .semibold, scale: .medium)
imageView.preferredSymbolConfiguration = config
```
Symbol and text weight explicitly matched; UIKit sizing set in one combined configuration call. (Rules 2, 3)

## Non-Compliant Example

```swift
imageView.image = UIImage(systemName: "bolt.fill")
imageView.frame.size = CGSize(width: 40, height: 40)
```
Resizing the image view's frame directly instead of using a scale configuration — stretches the glyph rather than re-rendering it at the correct weight. (Rule 1)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — weight/scale apply to a symbol already resolved by name.

## References

-   [Apple Developer — imageScale(_:)](https://developer.apple.com/documentation/swiftui/view/imagescale(_:))
-   [Apple Developer — SymbolConfiguration(pointSize:weight:scale:)](https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class/init(pointsize:weight:scale:))
