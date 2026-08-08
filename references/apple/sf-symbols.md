# SF Symbols

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.sf-symbols
artifact_type: reference
title: SF Symbols
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's SF Symbols API documentation, scoped to this domain's v1.
domain: SF Symbols
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/swiftui/image/init(_:bundle:)
https://developer.apple.com/documentation/swiftui/image/init(systemname:)
https://developer.apple.com/documentation/swiftui/image/init(systemname:variablevalue:)
https://developer.apple.com/documentation/swiftui/symbolrenderingmode
https://developer.apple.com/documentation/swiftui/symbolvariants
https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:)
https://developer.apple.com/documentation/swiftui/view/imagescale(_:)
https://developer.apple.com/documentation/uikit/configuring-and-displaying-symbol-images-in-your-ui
https://developer.apple.com/documentation/uikit/uiimage/init(named:)
https://developer.apple.com/documentation/uikit/uiimage/init(systemname:)
https://developer.apple.com/documentation/uikit/uiimage/init(systemname:variablevalue:configuration:)
https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class
https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class/init(pointsize:weight:scale:)
https://developer.apple.com/documentation/uikit/uiimage/withconfiguration(_:)
https://developer.apple.com/documentation/uikit/uiimageview/preferredsymbolconfiguration
https://developer.apple.com/documentation/uikit/uiview/tintcolor

## Purpose

Reference index for Apple's SF Symbols API documentation, scoped to this
domain's v1: core rendering (`Image(systemName:)`/`UIImage(systemName:)`),
rendering modes (monochrome, hierarchical, palette, multicolor), symbol
variants (fill/circle/square/slash), variable value symbols, weight/scale
configuration, color/tinting mechanics, custom symbol usage, and UIKit
`SymbolConfiguration` object composition — across SwiftUI and UIKit.
Symbol effects/animations (`SymbolEffect`, iOS 17+) and Symbol Composer /
custom symbol authoring are **Excluded**, matching
`skills/sf-symbols/SKILL.md` — this file called them deferred until
2026-08-08, which promised a pass the Skill had already ruled out.
Design-level symbol
*selection* (which symbol fits a meaning, fill vs. outline as a design
choice) is owned by the `human-interface-guidelines` domain's
`sf-symbols.md` Knowledge Contract, not this one — see
docs/architecture/domain-map.md Cross-Domain Notes.

## Primary Topics

- Symbol basics
- Rendering modes
- Symbol variants
- Variable value symbols
- Symbol weight and scale
- Symbol color and tinting
- Custom symbol usage
- UIKit symbol configuration

## Used By

- knowledge/sf-symbols/symbol-basics.md ([[knowledge/sf-symbols/symbol-basics]])
- knowledge/sf-symbols/rendering-modes.md ([[knowledge/sf-symbols/rendering-modes]])
- knowledge/sf-symbols/symbol-variants.md ([[knowledge/sf-symbols/symbol-variants]])
- knowledge/sf-symbols/variable-value-symbols.md ([[knowledge/sf-symbols/variable-value-symbols]])
- knowledge/sf-symbols/symbol-weight-and-scale.md ([[knowledge/sf-symbols/symbol-weight-and-scale]])
- knowledge/sf-symbols/symbol-color-and-tinting.md ([[knowledge/sf-symbols/symbol-color-and-tinting]])
- knowledge/sf-symbols/custom-symbol-usage.md ([[knowledge/sf-symbols/custom-symbol-usage]])
- knowledge/sf-symbols/uikit-symbol-configuration.md ([[knowledge/sf-symbols/uikit-symbol-configuration]])
