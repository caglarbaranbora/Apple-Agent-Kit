# Gesture State

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.gesture-state
type: knowledge
title: Gesture State
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the @GestureState property wrapper and .updating(_:body:), including its automatic reset semantics on gesture end or cancellation.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/gesturestate
  - https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:)
depends_on: []
related:
  - knowledge.swiftui.drag-gesture
updated: 2026-08-06
```

## Intent

Defines how agents use `@GestureState` and `.updating(_:body:)` for
transient gesture-scoped state that automatically resets, distinct from
persistent `@State` that requires manual reset logic.

## Scope

### Included

-   `@GestureState` property wrapper declaration
-   `.updating(_:body:)` gesture modifier
-   Automatic reset on gesture end or system cancellation

### Excluded

-   Gesture-specific usage walkthroughs (drag, magnify, rotate) — see
    per-gesture Knowledge Contracts, which use `@GestureState` in context

## Rules

### Rule 1

Agents MUST declare transient, gesture-scoped state with
`@GestureState` (not a plain `@State`) when the value should
automatically reset once the gesture ends or is cancelled. Apple's
documentation states it "resets the state to its initial value when
the user or the system ends or cancels the gesture."

### Rule 2

Agents MUST attach a `@GestureState` value to a gesture via
`.updating(_:body:)`, whose `body` closure's first parameter is the
gesture's own `Value` type (for example, `DragGesture.Value`), not the
`GestureState`'s wrapped type. Agents MUST NOT confuse the two when
writing the closure signature.

### Rule 3

Agents MUST copy any `@GestureState` value that must survive past
gesture completion into a separate, persistent `@State` inside the
gesture's `.onEnded` closure before the reset happens. Agents MUST NOT
attempt to read a `@GestureState` value inside `.onEnded` expecting the
in-progress value — it is already reset by then.

### Rule 4

Agents SHOULD prefer `@GestureState` over manually resetting a plain
`@State` in every gesture's `onEnded`/cancellation path, since
`@GestureState` also resets automatically on system-initiated
cancellation (an interrupting alert, for example), which manual
`onEnded`-only reset code does not cover.

## Compliant Example

```swift
struct PressableButton: View {
    @GestureState private var isPressing = false

    var body: some View {
        Text("Hold")
            .padding()
            .background(isPressing ? Color.gray : Color.blue)
            .gesture(
                LongPressGesture(minimumDuration: .infinity)
                    .updating($isPressing) { _, state, _ in
                        state = true
                    }
            )
    }
}
```
`@GestureState` tied to `.updating` — `isPressing` automatically
resets to `false` if the press is released or cancelled, with no
manual reset code. (Rules 1, 4)

## Non-Compliant Example

```swift
struct DraggableCard: View {
    @GestureState private var dragOffset: CGSize = .zero

    var body: some View {
        Color.blue
            .frame(width: 100, height: 100)
            .offset(dragOffset)
            .gesture(
                DragGesture()
                    .updating($dragOffset) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { _ in
                        // dragOffset already reset to .zero here — this print
                        // never shows the dropped position
                        print("dropped at \(dragOffset)")
                    }
            )
    }
}
```
Reads `dragOffset` inside `.onEnded`, but `@GestureState` has already
reset it to `.zero` by the time the closure runs. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — GestureState](https://developer.apple.com/documentation/swiftui/gesturestate)
-   [Apple Developer — Gesture.updating(_:body:)](https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:))
