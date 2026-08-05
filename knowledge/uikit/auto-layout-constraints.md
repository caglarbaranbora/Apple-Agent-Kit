# Auto Layout Constraints

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.auto-layout-constraints
type: knowledge
title: Auto Layout Constraints
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of NSLayoutConstraint and layout anchors, plus translatesAutoresizingMaskIntoConstraints, to position views programmatically without ambiguous or conflicting layout.
domain: UIKit
tags:
  - uikit
  - auto-layout
  - constraints
references:
  - https://developer.apple.com/documentation/uikit/nslayoutconstraint
  - https://developer.apple.com/documentation/uikit/nslayoutanchor
  - https://developer.apple.com/documentation/uikit/uiview/translatesautoresizingmaskintoconstraints
depends_on: []
related:
  - knowledge.uikit.safe-area-and-layout-guides
  - knowledge.uikit.auto-layout-stack-views
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent authors programmatic Auto
Layout with anchors so views position correctly across size classes
without ambiguous or conflicting constraints.

## Scope

### Included

-   Setting `translatesAutoresizingMaskIntoConstraints = false` on programmatically added views
-   Anchor-based constraint creation and `NSLayoutConstraint.activate`
-   Avoiding ambiguous or unsatisfiable constraints

### Excluded

-   `UIStackView` — see `auto-layout-stack-views`
-   Safe area / layout margin guides — see `safe-area-and-layout-guides`

## Rules

### Rule 1

Agents MUST set `translatesAutoresizingMaskIntoConstraints = false` on
every view added programmatically before applying Auto Layout
constraints to it — leaving the default `true` makes the system generate
an autoresizing-mask-derived constraint that conflicts with explicit
constraints.

### Rule 2

Agents MUST use layout anchors (`leadingAnchor`, `topAnchor`,
`widthAnchor`, `centerXAnchor`, etc.) with
`NSLayoutConstraint.activate([...])` rather than the older
`NSLayoutConstraint(item:attribute:relatedBy:toItem:attribute:multiplier:constant:)`
initializer — anchors are type-safe (can't accidentally constrain a
horizontal anchor to a vertical one) and read closer to the resulting
layout.

### Rule 3

Agents MUST batch-activate a view's full constraint set in one
`NSLayoutConstraint.activate([...])` call rather than setting
`.isActive = true` on each constraint individually — batching lets Auto
Layout resolve the whole set together instead of potentially hitting a
transient ambiguous state between individual activations.

### Rule 4

Agents MUST give every added view a complete constraint set (position
plus size, whether explicit or derived from content/intrinsic size) — a
view with only, say, a leading and top anchor has an ambiguous width and
height, and Auto Layout will place it at zero size or log an ambiguity
warning.

## Compliant Example

```swift
let avatarImageView = UIImageView()
avatarImageView.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(avatarImageView)

NSLayoutConstraint.activate([
    avatarImageView.topAnchor.constraint(equalTo: view.topAnchor, constant: 16),
    avatarImageView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    avatarImageView.widthAnchor.constraint(equalToConstant: 44),
    avatarImageView.heightAnchor.constraint(equalToConstant: 44),
])
```
Autoresizing mask disabled, anchors batch-activated, full position and size constraint set. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
let avatarImageView = UIImageView()
view.addSubview(avatarImageView)

avatarImageView.topAnchor.constraint(equalTo: view.topAnchor, constant: 16).isActive = true
avatarImageView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16).isActive = true
```
`translatesAutoresizingMaskIntoConstraints` left `true` (conflicts with the explicit constraints), constraints activated individually via `.isActive = true` instead of batched, and no width/height, leaving the image view's size ambiguous. (Rules 1, 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — NSLayoutConstraint](https://developer.apple.com/documentation/uikit/nslayoutconstraint)
-   [Apple Developer — NSLayoutAnchor](https://developer.apple.com/documentation/uikit/nslayoutanchor)
-   [Apple Developer — translatesAutoresizingMaskIntoConstraints](https://developer.apple.com/documentation/uikit/uiview/translatesautoresizingmaskintoconstraints)
