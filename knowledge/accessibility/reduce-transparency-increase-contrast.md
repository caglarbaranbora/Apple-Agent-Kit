# Reduce Transparency and Increase Contrast

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.reduce-transparency-increase-contrast
type: knowledge
title: Reduce Transparency and Increase Contrast
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines checking accessibilityReduceTransparency/colorSchemeContrast (SwiftUI) and UIAccessibility.isReduceTransparencyEnabled/isDarkerSystemColorsEnabled (UIKit) to replace translucent materials and fixed low-contrast colors when these settings are on.
domain: Accessibility
tags:
  - accessibility
  - contrast
  - transparency
references:
  - https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency
  - https://developer.apple.com/documentation/uikit/uiaccessibility/isreducetransparencyenabled
  - https://developer.apple.com/documentation/uikit/uiaccessibility/isdarkersystemcolorsenabled
depends_on: []
related:
  - knowledge.accessibility.reduce-motion
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent responds to the Reduce
Transparency and Increase Contrast settings — replacing translucent
materials with opaque backgrounds and preferring system colors (which
auto-adjust) over fixed custom colors — implementing at the API level
the contrast requirement HIG's `accessibility.md` Rule 2 sets at the
design level.

## Scope

### Included

-   `accessibilityReduceTransparency`/`isReduceTransparencyEnabled`
-   `colorSchemeContrast`/`isDarkerSystemColorsEnabled`
-   Preferring system colors over fixed custom colors
-   Custom-drawn content (Core Graphics/Canvas) not adapting automatically

### Excluded

-   Motion/animation settings — see `reduce-motion`
-   The 4.5:1 contrast ratio requirement itself — owned by `human-interface-guidelines`'s `accessibility.md`

## Rules

### Rule 1

Agents MUST replace translucent materials (`.ultraThinMaterial`,
`.regularMaterial`, a blurred `UIVisualEffectView`) with an opaque
background when `accessibilityReduceTransparency` (SwiftUI) or
`UIAccessibility.isReduceTransparencyEnabled` (UIKit) is true.

### Rule 2

Agents MUST check `colorSchemeContrast == .increased` (SwiftUI) or
`UIAccessibility.isDarkerSystemColorsEnabled` (UIKit) and prefer
system-provided colors for text/borders/dividers, which automatically
increase contrast under this setting, rather than fixed custom colors
that don't respond to it.

### Rule 3

Agents SHOULD avoid adding bespoke contrast-boosting logic on top of
system colors/materials — system colors and materials already respond
to Reduce Transparency and Increase Contrast automatically, so custom
overrides are only needed for custom-drawn content.

### Rule 4

Agents MUST NOT ignore these settings for custom-drawn content (Core
Graphics, `Canvas`, `CAShapeLayer`) that doesn't automatically adapt —
read the settings directly and adjust fill/stroke colors and opacity in
the drawing code.

## Compliant Example

```swift
@Environment(\.accessibilityReduceTransparency) private var reduceTransparency

var body: some View {
    ToolbarContent()
        .background(reduceTransparency ? AnyShapeStyle(Color(.systemBackground)) : AnyShapeStyle(.ultraThinMaterial))
}
```
Falls back to an opaque system background instead of a translucent material. (Rule 1)

## Non-Compliant Example

```swift
var body: some View {
    ToolbarContent()
        .background(.ultraThinMaterial)
}
```
Translucent material is applied unconditionally, ignoring the user's Reduce Transparency setting. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityReduceTransparency](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency)
-   [Apple Developer — UIAccessibility isReduceTransparencyEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/isreducetransparencyenabled)
-   [Apple Developer — UIAccessibility isDarkerSystemColorsEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/isdarkersystemcolorsenabled)
