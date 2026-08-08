# Dynamic Type API

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.accessibility.dynamic-type-api
artifact_type: knowledge
title: Dynamic Type API
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of @ScaledMetric (SwiftUI) and UIFontMetrics (UIKit) to scale custom spacing/sizing with Dynamic Type, and text-style-based fonts instead of fixed point sizes — the API-implementation half of HIG's Dynamic Type requirement.
domain: Accessibility
tags:
  - accessibility
  - dynamic-type
references:
  - https://developer.apple.com/documentation/swiftui/scaledmetric
  - https://developer.apple.com/documentation/uikit/uifontmetrics
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent implements Dynamic Type
support at the API level — `@ScaledMetric` (SwiftUI) and
`UIFontMetrics.scaledFont(for:)` (UIKit) for custom numeric
spacing/sizing, and text-style-based fonts instead of fixed point sizes —
implementing the requirement HIG's `accessibility.md` Rule 1 sets at the
design level (text must scale to at least 200% without loss of content).

## Scope

### Included

-   `@ScaledMetric` for custom spacing/icon-size constants
-   `UIFontMetrics.scaledFont(for:)` and `adjustsFontForContentSizeCategory`
-   Text-style fonts (`.font(.body)`, `UIFont.preferredFont(forTextStyle:)`) vs fixed point sizes
-   Capping unconstrained scaling where it breaks layout

### Excluded

-   Layout not breaking/truncating at large sizes — owned by `human-interface-guidelines`'s `accessibility.md`/`layout.md`

## Rules

### Rule 1

Agents MUST use `@ScaledMetric` (SwiftUI) or
`UIFontMetrics(forTextStyle:).scaledFont(for:)` (UIKit) for any custom
fixed-point spacing or sizing value that is visually tied to text (icon
size next to a label, padding around a text block), instead of a
hardcoded constant that ignores the user's text-size setting.

### Rule 2

Agents MUST use Dynamic Type text styles (`.font(.body)`,
`.font(.headline)` in SwiftUI; `UIFont.preferredFont(forTextStyle:)` in
UIKit) for body and label text, not a fixed pixel/point size
(`.font(.system(size: 14))`, `UIFont(name:size:)`), so text scales with
the user's preferred content size category.

### Rule 3

Agents MUST set `adjustsFontForContentSizeCategory = true` on any UIKit
`UILabel`/`UIButton`/`UITextField` configured with
`UIFont.preferredFont(forTextStyle:)`, so the control's font updates live
when the user changes their preferred text size in Settings.

### Rule 4

Agents SHOULD cap unconstrained `@ScaledMetric`/Dynamic Type growth with
`.dynamicTypeSize(...upTo:)` on the specific view where uncapped scaling
would break the layout, rather than disabling Dynamic Type support
entirely for that screen.

## Compliant Example

```swift
struct BadgeView: View {
    @ScaledMetric private var iconSize: CGFloat = 16

    var body: some View {
        Label("New", systemImage: "bell.fill")
            .font(.subheadline)
            .imageScale(.small)
            .frame(width: iconSize, height: iconSize)
    }
}
```
Icon size scales alongside the text via `@ScaledMetric`, and the label uses a Dynamic Type text style. (Rules 1, 2)

## Non-Compliant Example

```swift
struct BadgeView: View {
    var body: some View {
        Label("New", systemImage: "bell.fill")
            .font(.system(size: 12))
            .frame(width: 16, height: 16)
    }
}
```
Fixed point font size and hardcoded icon frame ignore the user's Dynamic Type setting entirely. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — ScaledMetric](https://developer.apple.com/documentation/swiftui/scaledmetric)
-   [Apple Developer — UIFontMetrics](https://developer.apple.com/documentation/uikit/uifontmetrics)
