# Drag Gesture

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.swiftui.drag-gesture
artifact_type: knowledge
title: Drag Gesture
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of DragGesture, its Value properties, and the choice between .updating and .onChanged/.onEnded for handling drag state.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/draggesture
  - https://developer.apple.com/documentation/swiftui/draggesture/value
  - https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:)
depends_on: []
related:
  - knowledge.swiftui.gesture-state
  - knowledge.swiftui.gesture-composition
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent implements drag
interactions with `DragGesture`: which initializer overload to use,
which `Value` properties to read, and `.updating` vs.
`.onChanged`/`.onEnded`.

## Scope

### Included

-   `DragGesture(minimumDistance:coordinateSpace:)`, both the current
    and deprecated initializer overloads
-   `DragGesture.Value` properties: `translation`, `location`,
    `predictedEndLocation`, `startLocation`
-   `.updating($gestureState)` vs. `.onChanged`/`.onEnded`

### Excluded

-   The `@GestureState` property wrapper's general mechanics (this file
    covers drag-specific usage only) — see `gesture-state.md`
-   Composing drag with other gestures — see `gesture-composition.md`

## Rules

### Rule 1

Agents MUST use the current `DragGesture(minimumDistance:coordinateSpace:)`
overload (`CoordinateSpaceProtocol`: `.local`, `.global`, `.named(_:)`)
for iOS 17+ targets. The older overload taking a `CoordinateSpace` enum
is deprecated — Apple's note reads "Use overload that accepts a
CoordinateSpaceProtocol instead." Only use the deprecated overload
below iOS 17.

### Rule 2

Agents MUST read `translation` for movement relative to where the drag
began, and `location`/`predictedEndLocation` for absolute/projected
positions — MUST NOT compute translation manually from raw touch deltas.

### Rule 3

Agents MUST use `.updating($gestureState)` with `@GestureState` for
transient drag state that should auto-reset when the drag ends or is
cancelled by the system (e.g., an interrupting alert).

### Rule 4

Agents MUST use `.onChanged`/`.onEnded` with a plain `@State` when the
value must persist after the gesture ends (e.g., a committed offset).
`@GestureState` is already reset by the time `.onEnded` runs.

### Rule 5

Agents SHOULD set `minimumDistance` above `0` on a view that also
recognizes a tap gesture, to avoid eating taps.

## Compliant Example

```swift
struct DraggableCard: View {
    @GestureState private var dragTranslation: CGSize = .zero
    @State private var committedOffset: CGSize = .zero

    var body: some View {
        Color.blue
            .frame(width: 100, height: 100)
            .offset(x: committedOffset.width + dragTranslation.width,
                    y: committedOffset.height + dragTranslation.height)
            .gesture(
                DragGesture(minimumDistance: 10, coordinateSpace: .local)
                    .updating($dragTranslation) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        committedOffset.width += value.translation.width
                        committedOffset.height += value.translation.height
                    }
            )
    }
}
```
Modern `CoordinateSpaceProtocol` overload, `@GestureState` for
transient translation (auto-resets), plain `@State` commits the final
value in `.onEnded`. (Rules 1, 3, 4)

## Non-Compliant Example

```swift
struct DraggableCard: View {
    @GestureState private var dragTranslation: CGSize = .zero

    var body: some View {
        Color.blue
            .frame(width: 100, height: 100)
            .offset(dragTranslation)
            .gesture(
                DragGesture(minimumDistance: 10, coordinateSpace: .local)
                    .updating($dragTranslation) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        // @GestureState already reset to .zero here
                        print("final offset: \(dragTranslation)")
                    }
            )
    }
}
```
Reads `dragTranslation` in `.onEnded` expecting the in-progress value,
but it has already reset — the card snaps back. (Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — DragGesture](https://developer.apple.com/documentation/swiftui/draggesture)
-   [Apple Developer — DragGesture.Value](https://developer.apple.com/documentation/swiftui/draggesture/value)
-   [Apple Developer — Gesture.updating(_:body:)](https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:))
