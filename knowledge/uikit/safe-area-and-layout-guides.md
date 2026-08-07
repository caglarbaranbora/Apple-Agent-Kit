# Safe Area and Layout Guides

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.safe-area-and-layout-guides
artifact_type: knowledge
title: Safe Area and Layout Guides
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of safeAreaLayoutGuide and layoutMarginsGuide to anchor content clear of system chrome and respect consistent view margins.
domain: UIKit
tags:
  - uikit
  - auto-layout
  - safe-area
references:
  - https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide
  - https://developer.apple.com/documentation/uikit/uiview/layoutmarginsguide
depends_on: []
related:
  - knowledge.uikit.auto-layout-constraints
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent anchors content to
`safeAreaLayoutGuide`/`layoutMarginsGuide` instead of a view's raw edges,
so content stays clear of system chrome and respects consistent margins.

## Scope

### Included

-   Constraining to `safeAreaLayoutGuide` anchors instead of view edge anchors
-   `layoutMarginsGuide` for consistent inset content
-   When to intentionally extend content under the safe area (backgrounds)

### Excluded

-   General anchor-based constraint mechanics — see `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST anchor top-level content (navigation bars, primary text,
interactive controls) to `view.safeAreaLayoutGuide` anchors, not
`view.topAnchor`/`view.bottomAnchor` directly — anchoring to the raw view
edge places content under the status bar, notch/Dynamic Island, or home
indicator on devices where those obstruct the edge.

### Rule 2

Agents MUST NOT apply `safeAreaLayoutGuide` to background or decorative
views meant to fill the entire screen (a full-bleed background image or
color) — constrain those to `view`'s edges directly so they extend under
the status bar/home indicator area as visually intended.

### Rule 3

Agents SHOULD use `view.layoutMarginsGuide` instead of hand-picked
constant insets when a screen's content should respect the system's
standard content margins — this keeps horizontal insets consistent with
other UIKit screens and adapts automatically to size class and device.

### Rule 4

Agents MUST re-verify safe area insets after rotation or size class
changes for any manual (non-constraint) frame math involving
`safeAreaInsets` — these values change with device orientation and
windowing, and stale cached values misplace content.

## Compliant Example

```swift
let scrollView = UIScrollView()
scrollView.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(scrollView)

NSLayoutConstraint.activate([
    scrollView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
    scrollView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor),
    scrollView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor),
    scrollView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
])
```
Content scroll view anchored to the safe area guide, clear of the notch and home indicator. (Rule 1)

## Non-Compliant Example

```swift
let scrollView = UIScrollView()
view.addSubview(scrollView)
NSLayoutConstraint.activate([
    scrollView.topAnchor.constraint(equalTo: view.topAnchor),
    scrollView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
])
```
Anchored to the view's raw top/bottom edges — on notched devices the first row of content renders under the status bar or Dynamic Island. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — safeAreaLayoutGuide](https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide)
-   [Apple Developer — layoutMarginsGuide](https://developer.apple.com/documentation/uikit/uiview/layoutmarginsguide)
