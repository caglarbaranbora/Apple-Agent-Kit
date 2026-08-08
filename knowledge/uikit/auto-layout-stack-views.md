# Auto Layout Stack Views

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.uikit.auto-layout-stack-views
artifact_type: knowledge
title: Auto Layout Stack Views
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of UIStackView (axis, distribution, alignment, spacing) to lay out a linear sequence of views without hand-written inter-view constraints.
domain: UIKit
tags:
  - uikit
  - auto-layout
  - stack-view
references:
  - https://developer.apple.com/documentation/uikit/uistackview
  - https://developer.apple.com/documentation/uikit/uistackview/distribution-swift.property
  - https://developer.apple.com/documentation/uikit/uistackview/alignment-swift.property
depends_on: []
related:
  - knowledge.uikit.auto-layout-constraints
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent uses `UIStackView` to
arrange a linear row or column of views, picking a correct axis,
distribution, alignment, and spacing instead of hand-writing inter-view
constraints for a case `UIStackView` already solves.

## Scope

### Included

-   Axis, distribution, alignment, spacing configuration
-   Nesting stack views for two-dimensional layouts
-   When a stack view is the right tool vs. plain constraints

### Excluded

-   Constraining the stack view itself to its superview — see `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST use `UIStackView` instead of hand-written leading/trailing
constraints between sibling views when laying out a linear (horizontal
or vertical) sequence of views — the stack view manages inter-view
spacing and distribution automatically, avoiding N-1 manually authored
constraints.

### Rule 2

Agents MUST set an explicit `distribution` (`.fill`, `.fillEqually`,
`.fillProportionally`, `.equalSpacing`, `.equalCentering`) rather than
leaving the default — the default `.fill` silently relies on each
arranged subview's content-hugging/compression-resistance priorities,
which is often not the intended layout.

### Rule 3

Agents MUST still constrain the stack view itself to its superview (or
use it as an arranged subview of an outer stack) — `UIStackView` only
manages its own arranged subviews' internal layout, not its own
position, so it needs standard constraints per `auto-layout-constraints`.

### Rule 4

Agents SHOULD nest stack views (a horizontal stack of vertical stacks, or
vice versa) for two-dimensional layouts rather than falling back to raw
constraints, when the layout is still fundamentally row/column-based.

## Compliant Example

```swift
let titleLabel = UILabel()
let subtitleLabel = UILabel()
let textStack = UIStackView(arrangedSubviews: [titleLabel, subtitleLabel])
textStack.axis = .vertical
textStack.distribution = .fill
textStack.alignment = .leading
textStack.spacing = 4
textStack.translatesAutoresizingMaskIntoConstraints = false
```
Explicit axis, distribution, alignment, and spacing on a vertical text stack. (Rules 1, 2)

## Non-Compliant Example

```swift
let titleLabel = UILabel()
let subtitleLabel = UILabel()
view.addSubview(titleLabel)
view.addSubview(subtitleLabel)

NSLayoutConstraint.activate([
    titleLabel.topAnchor.constraint(equalTo: view.topAnchor),
    subtitleLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 4),
])
```
Hand-written inter-view constraint for a plain vertical sequence that `UIStackView` would express in three configuration lines. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — UIStackView](https://developer.apple.com/documentation/uikit/uistackview)
-   [Apple Developer — UIStackView.distribution](https://developer.apple.com/documentation/uikit/uistackview/distribution-swift.property)
-   [Apple Developer — UIStackView.alignment](https://developer.apple.com/documentation/uikit/uistackview/alignment-swift.property)
