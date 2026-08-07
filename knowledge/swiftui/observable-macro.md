# Observable Macro

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.observable-macro
artifact_type: knowledge
title: Observable Macro
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of the @Observable macro (iOS 17+) for reference-type model objects, as the default replacement for ObservableObject/@Published in new code.
domain: SwiftUI
tags:
  - swiftui
  - state
  - observation
references:
  - https://developer.apple.com/documentation/observation/observable()
  - https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app
depends_on: []
related:
  - knowledge.swiftui.state-and-binding
  - knowledge.swiftui.environment-values
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent models reference-type
(class) app state for SwiftUI observation, using the `@Observable`
macro (iOS 17+) as the default for new code instead of
`ObservableObject`/`@Published`.

## Scope

### Included

-   `@Observable` as the default for new iOS 17+ reference-type models
-   Ownership with `@State` instead of `@StateObject`
-   Passing an `@Observable` model to children without a property wrapper
-   Not mixing `@Observable` and `ObservableObject` on one type

### Excluded

-   `@State`/`@Binding` for local value-type state — see `state-and-binding`
-   `@Environment` injection of an `@Observable` model — see `environment-values`

## Rules

### Rule 1

Agents MUST mark reference-type (class) model objects that a SwiftUI
view observes with the `@Observable` macro rather than conforming to
`ObservableObject` with individual `@Published` properties, for new code
targeting iOS 17+.

### Rule 2

Agents MUST hold an `@Observable` model that a view creates and owns
with `@State` (not `@StateObject`, which is specific to
`ObservableObject`) — `@State` correctly manages the lifetime of
`@Observable` reference types.

### Rule 3

Agents MUST pass an `@Observable` model down to child views as a plain
stored property (no property wrapper needed) when the child only reads
or observes it — `@Observable`'s tracking works automatically via
property access inside `body`.

### Rule 4

Agents MUST NOT mix `@Observable` and `ObservableObject`/`@Published` on
the same type — pick one observation mechanism per type.

### Rule 5

Agents SHOULD use `@Environment` (not a manually threaded stored
property through every intermediate view) to inject an `@Observable`
model that many descendant views need, avoiding prop-drilling.

## Compliant Example

```swift
@Observable
final class CartModel {
    var items: [Item] = []
}

struct CartView: View {
    @State private var model = CartModel()
    var body: some View {
        CartList(model: model)
    }
}

struct CartList: View {
    var model: CartModel
    var body: some View {
        List(model.items) { item in Text(item.name) }
    }
}
```
`@Observable` model owned via `@State`, passed to a child as a plain property. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
final class CartModel: ObservableObject {
    @Published var items: [Item] = []
}

struct CartView: View {
    @StateObject private var model = CartModel()
    var body: some View {
        CartList(model: model)
    }
}

struct CartList: View {
    @ObservedObject var model: CartModel
    var body: some View {
        List(model.items) { item in Text(item.name) }
    }
}
```
Legacy `ObservableObject`/`@Published`/`@StateObject`/`@ObservedObject` pattern for new iOS 17+ code, where `@Observable` is the recommended default. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Observable()](https://developer.apple.com/documentation/observation/observable())
-   [Apple Developer — Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app)
