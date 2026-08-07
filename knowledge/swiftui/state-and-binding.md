# State and Binding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.state-and-binding
artifact_type: knowledge
title: State and Binding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct ownership of local view state with @State versus propagating a parent-owned value for read/write access to a child with @Binding.
domain: SwiftUI
tags:
  - swiftui
  - state
references:
  - https://developer.apple.com/documentation/swiftui/state
  - https://developer.apple.com/documentation/swiftui/binding
depends_on: []
related:
  - knowledge.swiftui.observable-macro
  - knowledge.swiftui.environment-values
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent chooses between `@State`
(local, view-owned, value-type data) and `@Binding` (read/write access
to a value owned by a parent), avoiding duplicated or unsynchronized
sources of truth.

## Scope

### Included

-   `@State` ownership rules
-   `@Binding` for child mutation of parent-owned values
-   Avoiding duplicated state
-   Mutating bindings only through the normal update cycle

### Excluded

-   Reference-type observable models — see `observable-macro`
-   Environment-injected shared state — see `environment-values`

## Rules

### Rule 1

Agents MUST mark local, view-owned, mutable value-type data with
`@State`, declared `private` since it belongs to that view instance
only.

### Rule 2

Agents MUST use `@Binding` (not a plain parameter plus callback pair,
and not a duplicated `@State`) when a child view needs to read and
mutate a value owned by a parent or ancestor.

### Rule 3

Agents MUST NOT declare `@State` for a value that is actually owned by a
parent and merely passed down for display — that creates two
independent sources of truth that drift out of sync.

### Rule 4

Agents MUST NOT mutate a `@Binding`'s wrapped value outside SwiftUI's
normal update cycle (e.g., during `init`) — mutate only through normal
event handlers such as button actions or `onChange`.

### Rule 5

Agents SHOULD initialize `@State` with a default value at declaration,
overriding via a custom `init` parameter only when the initial value
genuinely depends on injected data, treated as a one-time seed rather
than a live sync point with the caller.

## Compliant Example

```swift
struct ParentView: View {
    @State private var isOn = false
    var body: some View {
        ToggleRow(isOn: $isOn)
    }
}

struct ToggleRow: View {
    @Binding var isOn: Bool
    var body: some View {
        Toggle("Enabled", isOn: $isOn)
    }
}
```
`@State` owned by the parent, propagated for mutation via `@Binding`. (Rules 1, 2)

## Non-Compliant Example

```swift
struct ToggleRow: View {
    var isOn: Bool
    var body: some View {
        Toggle("Enabled", isOn: .constant(isOn))
    }
}
```
A plain `Bool` parameter wrapped in `.constant()` cannot propagate changes back to the parent. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — State](https://developer.apple.com/documentation/swiftui/state)
-   [Apple Developer — Binding](https://developer.apple.com/documentation/swiftui/binding)
