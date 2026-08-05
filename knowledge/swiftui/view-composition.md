# View Composition

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.view-composition
type: knowledge
title: View Composition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to break SwiftUI UI into small, single-responsibility views using ViewBuilder and extracted view types instead of monolithic body implementations.
domain: SwiftUI
tags:
  - swiftui
  - views
  - composition
references:
  - https://developer.apple.com/documentation/swiftui/view
depends_on: []
related:
  - knowledge.swiftui.modifier-order
  - knowledge.swiftui.view-identity
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent structures SwiftUI view
code: extracting focused subviews, keeping `body` declarative, and
choosing between computed properties, `@ViewBuilder` helpers, and
extracted view structs.

## Scope

### Included

-   When to extract a subview vs. keep inline
-   `@ViewBuilder` usage for conditional view-returning helpers
-   Keeping `body` free of non-trivial logic
-   Computed property vs. extracted `View` struct trade-off

### Excluded

-   Stable identity for extracted/repeated views in collections — see `view-identity`
-   Order of modifiers applied to a composed view — see `modifier-order`

## Rules

### Rule 1

Agents MUST extract a subview (or `@ViewBuilder` helper) when `body`
mixes multiple independent concerns (e.g., header + list + footer)
instead of writing one large `body`.

### Rule 2

Agents MUST NOT place non-trivial business logic (parsing, formatting
chains, network calls) inside `body` — compute values in properties or
methods outside `body`, keeping `body` declarative.

### Rule 3

Agents SHOULD use `@ViewBuilder` for helper functions or computed
properties that conditionally return different view content, instead of
type-erasing with `AnyView` by default.

### Rule 4

Agents SHOULD extract a private `View` struct (not a computed property)
when the subview needs its own `@State` or is reused across multiple
parents — a computed property recomputes on every access and cannot
hold state.

## Compliant Example

```swift
struct ProfileScreen: View {
    let profile: Profile

    var body: some View {
        VStack {
            ProfileHeader(profile: profile)
            ProfileDetailsList(profile: profile)
        }
    }
}

private struct ProfileHeader: View {
    let profile: Profile
    var body: some View {
        Text(profile.name).font(.title)
    }
}
```
Small, single-responsibility views composed together. (Rules 1, 4)

## Non-Compliant Example

```swift
struct ProfileScreen: View {
    let profile: Profile
    var body: some View {
        VStack {
            Text(profile.name).font(.title)
            Text(profile.bio.trimmingCharacters(in: .whitespaces).uppercased())
            ForEach(profile.posts) { post in
                // dozens more lines of unrelated list-rendering logic
                Text(post.title)
            }
        }
    }
}
```
One monolithic `body` mixing header formatting logic and list rendering. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — View](https://developer.apple.com/documentation/swiftui/view)
