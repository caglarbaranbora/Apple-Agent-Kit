# Environment Values

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.environment-values
type: knowledge
title: Environment Values
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of @Environment for dependency injection of shared app state and custom environment values, instead of manually threading dependencies through view initializers.
domain: SwiftUI
tags:
  - swiftui
  - state
  - environment
references:
  - https://developer.apple.com/documentation/swiftui/environment
  - https://developer.apple.com/documentation/swiftui/environmentkey
depends_on: []
related:
  - knowledge.swiftui.observable-macro
  - knowledge.swiftui.state-and-binding
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent injects shared or
cross-cutting values (custom values, or an `@Observable` model many
descendants need) using SwiftUI's environment, instead of manually
threading dependencies through every intermediate view's initializer.

## Scope

### Included

-   `@Environment` reads for custom and built-in environment values
-   Defining custom environment values (`EnvironmentKey`, or the `@Entry` macro)
-   Injecting an `@Observable` model with `.environment(_:)`
-   When environment injection is overkill

### Excluded

-   `@Observable` model definition itself — see `observable-macro`
-   Local `@State`/`@Binding` — see `state-and-binding`

## Rules

### Rule 1

Agents MUST use `@Environment` to read a value injected via
`.environment(_:)` (custom `@Observable` models) or a built-in
environment key (e.g., `\.dismiss`, `\.colorScheme`), rather than
passing the same dependency through every intermediate view's
initializer.

### Rule 2

Agents MUST define custom environment values as a type conforming to
`EnvironmentKey` (or, using Xcode 16's `@Entry` macro) with an explicit
default value, not force-unwrap a missing environment value at the read
site.

### Rule 3

Agents MUST inject an `@Observable` model into the environment with
`.environment(model)` — not `.environmentObject(model)`, which is the
`ObservableObject`-specific API — to stay consistent with the
`@Observable` convention.

### Rule 4

Agents MUST NOT overuse `@Environment` for values that are only needed
by one or two direct children — a plain stored-property parameter
remains simpler and more explicit for shallow dependency passing.

### Rule 5

Agents SHOULD scope the `.environment(_:)` injection call site to the
smallest subtree that actually needs the value, not always the app
root, so previews and tests can override it with a narrower substitute.

## Compliant Example

```swift
@Observable
final class SessionModel {
    var user: User?
}

RootView()
    .environment(SessionModel())

struct ProfileView: View {
    @Environment(SessionModel.self) private var session
    var body: some View {
        Text(session.user?.name ?? "Guest")
    }
}
```
`@Observable` model injected once, read via `@Environment` without prop-drilling. (Rules 1, 3)

## Non-Compliant Example

```swift
struct RootView: View {
    let session: SessionModel
    var body: some View {
        MiddleView(session: session)
    }
}

struct MiddleView: View {
    let session: SessionModel
    var body: some View {
        ProfileView(session: session)
    }
}
```
`session` threaded manually through `MiddleView`, which never uses it itself, just to reach `ProfileView`. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Environment](https://developer.apple.com/documentation/swiftui/environment)
-   [Apple Developer — EnvironmentKey](https://developer.apple.com/documentation/swiftui/environmentkey)
