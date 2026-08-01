# Custom Symbol Usage

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.custom-symbol-usage
type: knowledge
title: Custom Symbol Usage
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to reference an already-authored custom symbol asset in code so it renders with the same rendering-mode/weight/scale/tinting behavior as a system SF Symbol. Excludes authoring the symbol artwork itself.
domain: SF Symbols
tags:
  - sf-symbols
  - custom-symbol
  - asset-catalog
references:
  - https://developer.apple.com/documentation/swiftui/image/init(_:bundle:)
  - https://developer.apple.com/documentation/uikit/uiimage/init(named:)
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.sf-symbols.rendering-modes
  - knowledge.sf-symbols.symbol-weight-and-scale
  - knowledge.sf-symbols.symbol-color-and-tinting
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent references a custom symbol
that has already been added to the asset catalog as a Symbol Image
template, so it behaves identically to a system SF Symbol at the API
level. It covers usage only — authoring the symbol's artwork (Symbol
Composer, `.svg` preparation) is a design/asset-pipeline task outside
this contract's scope.

## Scope

### Included

-   Referencing a custom symbol by asset name (`Image("name")`,
    `UIImage(named:)`)
-   Confirming the asset is configured as a Symbol Image template, not a
    static bitmap
-   Applying the same rendering/variant/weight/color rules that apply to
    system symbols

### Excluded

-   Symbol Composer workflow, `.svg` export/preparation, or any other
    artwork-authoring step
-   Adding the asset to the asset catalog in Xcode (a project-configuration
    step, not a code-implementation rule)

## Rules

### Rule 1

Agents MUST reference a custom symbol added to the asset catalog by its
asset name via `Image("customName")` (SwiftUI) or `UIImage(named:
"customName")` (UIKit) — the same call pattern as any other named image
asset, with no symbol-specific initializer required.

### Rule 2

Agents MUST confirm the custom symbol asset is configured as a "Symbol
Image" template (not a static bitmap) before relying on
rendering-mode/weight/scale/tinting modifiers on it — those modifiers
only affect template-rendered images; a plain bitmap asset ignores them
silently, with no error.

### Rule 3

Agents MUST apply the same rendering-mode, weight/scale, and tinting
rules that apply to system symbols (see `rendering-modes`,
`symbol-weight-and-scale`, `symbol-color-and-tinting`) to a correctly
configured custom symbol — a template-configured custom symbol behaves
identically to a system symbol at the API level once imported.

### Rule 4

Agents MUST NOT author, edit, or export a custom symbol's artwork (Symbol
Composer workflow, `.svg` preparation) as part of an implementation task
— that is a design/asset-pipeline task outside this contract's scope;
implementation only consumes an already-prepared symbol asset.

## Compliant Example

```swift
Image("app.custom.badge")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.blue)
```
A custom symbol referenced by asset name and styled with the same rendering-mode API used for system symbols, because the asset is configured as a Symbol Image template. (Rules 1, 3)

## Non-Compliant Example

```swift
Image("app.custom.badge")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.white, .blue)
```
Applied to an asset that was imported as a plain bitmap (not a Symbol Image template) — the rendering-mode and multi-color foreground styling have no effect, producing an unstyled flat image with no error to indicate why. (Rule 2)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — custom symbols are referenced by name the same way system symbols are.

## References

-   [Apple Developer — Image(_:bundle:)](https://developer.apple.com/documentation/swiftui/image/init(_:bundle:))
-   [Apple Developer — UIImage(named:)](https://developer.apple.com/documentation/uikit/uiimage/init(named:))
