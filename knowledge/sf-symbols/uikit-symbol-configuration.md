# UIKit Symbol Configuration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.uikit-symbol-configuration
type: knowledge
title: UIKit Symbol Configuration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines composing and applying UIImage.SymbolConfiguration objects in UIKit — withConfiguration(_:), preferredSymbolConfiguration, and combining configurations with applying(_:).
domain: SF Symbols
tags:
  - sf-symbols
  - uikit
  - symbolconfiguration
references:
  - https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration
  - https://developer.apple.com/documentation/uikit/uiimage/withconfiguration(_:)
  - https://developer.apple.com/documentation/uikit/uiimageview/preferredsymbolconfiguration
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.sf-symbols.rendering-modes
  - knowledge.sf-symbols.symbol-weight-and-scale
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent composes and applies
`UIImage.SymbolConfiguration` objects in UIKit — setting a reusable
configuration on a `UIImageView`, updating an existing image's
configuration without re-fetching it by name, and combining
configuration aspects built separately — so symbol styling in UIKit stays
consistent and correctly applied.

## Scope

### Included

-   `UIImageView.preferredSymbolConfiguration`
-   `UIImage.withConfiguration(_:)`
-   Combining `UIImage.SymbolConfiguration` values with `.applying(_:)`

### Excluded

-   What each configuration parameter should be set to (weight, scale,
    rendering mode) — see `rendering-modes`, `symbol-weight-and-scale`
-   SwiftUI equivalents — SwiftUI uses view modifiers, not this object,
    see `rendering-modes` and `symbol-weight-and-scale`

## Rules

### Rule 1

Agents MUST set `UIImageView.preferredSymbolConfiguration` rather than
pre-configuring each individual `UIImage` when the same image view will
display different symbol names over its lifetime — the view applies the
stored configuration to every symbol image assigned afterward, so
weight/scale/rendering-mode logic isn't repeated per assignment.

### Rule 2

Agents MUST use `UIImage.withConfiguration(_:)` to get a differently
configured version of an already-resolved symbol image, rather than
calling `UIImage(systemName:)` again with a new configuration — reusing
the resolved image avoids a redundant name lookup.

### Rule 3

Agents SHOULD compose configuration aspects that come from separate
sources (e.g. a size configuration from one place, a color configuration
from another) with `UIImage.SymbolConfiguration.applying(_:)` rather than
one large combined initializer call — this keeps each aspect's origin
clear and combinable independently.

### Rule 4

Agents MUST NOT assume `withConfiguration(_:)` mutates its receiver — it
returns a new `UIImage`; discarding the return value and expecting the
original image or an image view's current image to have changed is a
no-op bug.

## Compliant Example

```swift
let sizeConfig = UIImage.SymbolConfiguration(pointSize: 20, weight: .semibold)
let colorConfig = UIImage.SymbolConfiguration(hierarchicalColor: .systemBlue)
let combined = sizeConfig.applying(colorConfig)

imageView.preferredSymbolConfiguration = combined
imageView.image = UIImage(systemName: "star.fill")
```
Two independently built configurations combined via `applying(_:)`, then set once on the image view so every later symbol assignment inherits it. (Rules 1, 3)

## Non-Compliant Example

```swift
let image = UIImage(systemName: "star.fill")!
image.withConfiguration(UIImage.SymbolConfiguration(pointSize: 30, weight: .bold))
imageView.image = image
```
The return value of `withConfiguration(_:)` is discarded — `image` and the assigned `imageView.image` remain unconfigured, so the intended size/weight change never takes effect. (Rule 4)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — configuration applies to a symbol already resolved by name.

## References

-   [Apple Developer — UIImage.SymbolConfiguration](https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration)
-   [Apple Developer — withConfiguration(_:)](https://developer.apple.com/documentation/uikit/uiimage/withconfiguration(_:))
-   [Apple Developer — preferredSymbolConfiguration](https://developer.apple.com/documentation/uikit/uiimageview/preferredsymbolconfiguration)
