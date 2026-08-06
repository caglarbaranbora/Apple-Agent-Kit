# Gesture Composition

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.gesture-composition
type: knowledge
title: Gesture Composition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of Gesture.simultaneously/sequenced/exclusively combinators and the .gesture/.highPriorityGesture/.simultaneousGesture view modifier priority semantics.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/gesture/simultaneously(with:)
  - https://developer.apple.com/documentation/swiftui/gesture/sequenced(before:)
  - https://developer.apple.com/documentation/swiftui/gesture/exclusively(before:)
  - https://developer.apple.com/documentation/swiftui/view/gesture(_:including:)
  - https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:)
  - https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:)
depends_on: []
related:
  - knowledge.swiftui.gesture-state
  - knowledge.swiftui.drag-gesture
updated: 2026-08-06
```

## Intent

Defines how agents combine gestures via `Gesture` combinators or
prioritize parent/child gesture recognition using view modifiers.

## Scope

### Included

-   `Gesture.simultaneously(with:)`, `.sequenced(before:)`,
    `.exclusively(before:)`
-   `.gesture(_:)`, `.highPriorityGesture(_:)`, `.simultaneousGesture(_:)`
    view modifiers and their precedence differences

### Excluded

-   Individual gesture types — see per-gesture Knowledge Contracts

## Rules

### Rule 1

Agents MUST use `.sequenced(before:)` (not `.simultaneously(with:)`)
when the second gesture should only begin recognizing after the first
gesture succeeds — for example, long-press-then-drag.

### Rule 2

Agents MUST use `.exclusively(before:)` when exactly one of two
gestures should win, with the first-listed gesture taking precedence.
Agents MUST NOT use `.simultaneously(with:)` when both gestures firing
together would produce conflicting behavior.

### Rule 3

Agents MUST choose the correct view modifier for parent/child gesture
conflicts: `.gesture(_:)` gives a view's children's own gestures
higher precedence than this one; `.highPriorityGesture(_:)` gives this
gesture precedence over the view's children's gestures, suppressing
them; `.simultaneousGesture(_:)` lets both this gesture and a child's
own gesture fire together.

### Rule 4

Agents MUST NOT default to `.highPriorityGesture` just to "make a
gesture work" without confirming child views don't also need their own
gesture to fire — it explicitly suppresses child gesture recognition.

### Rule 5

Agents SHOULD compose gestures via the `Gesture` protocol's
`.simultaneously`/`.sequenced`/`.exclusively` combinators into a single
composed gesture passed to one `.gesture(_:)` call, rather than
stacking multiple independent `.gesture(_:)` modifiers on the same
view — independent modifiers do not share recognition state.

## Compliant Example

```swift
struct LongPressThenDragView: View {
    @State private var isReady = false
    @State private var offset: CGSize = .zero

    var body: some View {
        Circle()
            .fill(isReady ? Color.green : Color.gray)
            .frame(width: 60, height: 60)
            .offset(offset)
            .gesture(
                LongPressGesture(minimumDuration: 0.3)
                    .onEnded { _ in isReady = true }
                    .sequenced(before: DragGesture())
                    .onEnded { value in
                        if case .second(true, let drag?) = value {
                            offset = drag.translation
                        }
                        isReady = false
                    }
            )
    }
}
```
`.sequenced(before:)` so the drag only recognizes after the long press
succeeds — a single composed gesture on one `.gesture(_:)` call.
(Rules 1, 5)

## Non-Compliant Example

```swift
struct ButtonWithBackgroundTap: View {
    var body: some View {
        VStack {
            Button("Tap me") { print("button tapped") }
        }
        .highPriorityGesture(
            TapGesture().onEnded { print("background tapped") }
        )
    }
}
```
`.highPriorityGesture` on the container suppresses the `Button`'s own
tap recognition entirely — the button never fires. Should have used
`.simultaneousGesture` (if both should fire) or reconsidered whether a
background tap gesture belongs on a container that also has a
tappable child. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — Gesture.simultaneously(with:)](https://developer.apple.com/documentation/swiftui/gesture/simultaneously(with:))
-   [Apple Developer — Gesture.sequenced(before:)](https://developer.apple.com/documentation/swiftui/gesture/sequenced(before:))
-   [Apple Developer — Gesture.exclusively(before:)](https://developer.apple.com/documentation/swiftui/gesture/exclusively(before:))
-   [Apple Developer — gesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:including:))
-   [Apple Developer — highPriorityGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:))
-   [Apple Developer — simultaneousGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:))
