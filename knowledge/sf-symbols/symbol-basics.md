# Symbol Basics

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-basics
artifact_type: knowledge
title: Symbol Basics
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of Image(systemName:) and UIImage(systemName:) to render a system SF Symbol, including safe existence-checking and OS-version availability guarding.
domain: SF Symbols
tags:
  - sf-symbols
  - symbol-basics
  - image
references:
  - https://developer.apple.com/documentation/swiftui/image/init(systemname:)
  - https://developer.apple.com/documentation/uikit/uiimage/init(systemname:)
depends_on: []
related:
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.sf-symbols.custom-symbol-usage
  - knowledge.sf-symbols.rendering-modes
  - knowledge.sf-symbols.symbol-color-and-tinting
  - knowledge.sf-symbols.symbol-variants
  - knowledge.sf-symbols.symbol-weight-and-scale
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent renders a system SF Symbol
by name and guards against the two ways that name lookup can silently
fail — an invalid name and a name not yet available on the app's minimum
supported OS version — so a broken icon doesn't ship unnoticed.

## Scope

### Included

-   `Image(systemName:)` (SwiftUI) and `UIImage(systemName:)` (UIKit)
-   Existence-checking a symbol name before shipping it
-   OS-version availability guarding for newer symbol names

### Excluded

-   Rendering mode, variant, weight/scale, and color configuration — see
    `rendering-modes`, `symbol-variants`, `symbol-weight-and-scale`,
    `symbol-color-and-tinting`
-   Custom (non-system) symbol usage — see `custom-symbol-usage`

## Rules

### Rule 1

Agents MUST use `Image(systemName:)` / `UIImage(systemName:)` for any
icon that has an SF Symbol equivalent, rather than bundling a custom icon
asset — the system symbol gets automatic weight/scale/rendering-mode
adaptation and Dynamic Type behavior for free.

### Rule 2

Agents MUST verify a system symbol name resolves before shipping it
(`UIImage(systemName: "name") != nil`, or confirm in the SF Symbols app)
— an invalid or unavailable name resolves to `nil` / no image, not a
crash, so the failure is silent unless explicitly checked.

### Rule 3

Agents SHOULD guard symbol names introduced after the app's minimum
deployment target with `if #available(...)`, providing an older
fallback symbol name — a symbol that doesn't exist yet on an older OS
returns `nil` the same as a typo'd name, with no automatic fallback.

### Rule 4

Agents MUST NOT force-unwrap `UIImage(systemName:)` (`!`) in production
code — an unrecognized or unavailable name crashes the app at runtime
instead of failing safely to a placeholder or logged warning.

## Compliant Example

```swift
func statusImage(named name: String) -> UIImage {
    guard let image = UIImage(systemName: name) else {
        assertionFailure("Missing SF Symbol: \(name)")
        return UIImage(systemName: "questionmark.circle") ?? UIImage()
    }
    return image
}

struct StarRating: View {
    var body: some View {
        Image(systemName: "star.fill")
    }
}
```
Existence-checked with a safe fallback instead of force-unwrapping; direct SwiftUI use of a known-valid literal name. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
let icon = UIImage(systemName: "start.fill")!
imageView.image = icon
```
Typo'd symbol name (`start.fill` instead of `star.fill`) force-unwrapped — crashes at runtime instead of failing safely. (Rules 2, 4)

## Dependencies

None.

## References

-   [Apple Developer — Image(systemName:)](https://developer.apple.com/documentation/swiftui/image/init(systemname:))
-   [Apple Developer — UIImage(systemName:)](https://developer.apple.com/documentation/uikit/uiimage/init(systemname:))
