# Matched Geometry Effect

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.matched-geometry-effect
type: knowledge
title: Matched Geometry Effect
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of matchedGeometryEffect and @Namespace for shared-element transitions between two co-present views.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)
  - https://developer.apple.com/documentation/swiftui/namespace
depends_on: []
related:
  - knowledge.swiftui.transitions
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent builds shared-element ("hero") transitions with `matchedGeometryEffect`, including the `@Namespace` requirement and the exactly-one-source rule.

## Scope

### Included

- `matchedGeometryEffect(id:in:properties:anchor:isSource:)` signature and usage
- `@Namespace` / `Namespace.ID` requirement
- Exactly-one-`isSource: true`-per-id rule
- Co-presence requirement (both linked views present during transaction)

### Excluded

- Transitions without shared geometry — see `transitions.md`

## Rules

### Rule 1

Agents MUST declare a `@Namespace private var` and pass its `.id` namespace to every `matchedGeometryEffect(id:in:)` call that should link — views in different namespaces never match.

### Rule 2

Agents MUST ensure exactly one view with a given `id` has `isSource: true` at any time the effect is active. Apple's documentation states results are undefined if the count of `isSource: true` views sharing that id isn't exactly one.

### Rule 3

Agents MUST keep both the source view (`isSource: true`) and non-source view (`isSource: false`) co-present in the hierarchy during the animated transaction — `matchedGeometryEffect` interpolates between two views' frames, it doesn't move a single view.

### Rule 4

Agents SHOULD wrap the state change that swaps which id is active in `withAnimation` — the effect participates in the ambient animation transaction like any other animatable property.

### Rule 5

Agents SHOULD scope `properties:` to `.position` or `.size` only (instead of default `.frame`) when just one dimension should morph, to avoid unwanted stretching.

## Compliant Example

```swift
struct HeroTransition: View {
    @Namespace private var animation
    @State private var isExpanded = false

    var body: some View {
        ZStack {
            if !isExpanded {
                RoundedRectangle(cornerRadius: 12)
                    .matchedGeometryEffect(id: "card", in: animation)
                    .frame(width: 80, height: 80)
            } else {
                RoundedRectangle(cornerRadius: 0)
                    .matchedGeometryEffect(id: "card", in: animation)
                    .frame(width: 300, height: 300)
            }
        }
        .onTapGesture {
            withAnimation(.spring()) {
                isExpanded.toggle()
            }
        }
    }
}
```

Single namespace, one matched id, exactly one view per state, wrapped in `withAnimation`. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
struct BrokenHeroTransition: View {
    @Namespace private var animationA
    @Namespace private var animationB // second namespace

    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: 12)
                .matchedGeometryEffect(id: "card", in: animationA)
            RoundedRectangle(cornerRadius: 12)
                .matchedGeometryEffect(id: "card", in: animationB) // never matches
        }
    }
}
```

Two views share same `id` but live in different namespaces — they never link. (Rule 1)

## Dependencies

None.

## References

- [Apple Developer — matchedGeometryEffect(id:in:properties:anchor:isSource:)](https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:))
- [Apple Developer — Namespace](https://developer.apple.com/documentation/swiftui/namespace)
