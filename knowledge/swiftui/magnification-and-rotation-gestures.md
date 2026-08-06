# Magnification and Rotation Gestures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.magnification-and-rotation-gestures
type: knowledge
title: Magnification and Rotation Gestures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the iOS 17+ MagnifyGesture and RotateGesture, and when the deprecated MagnificationGesture/RotationGesture are still required.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/magnifygesture
  - https://developer.apple.com/documentation/swiftui/rotategesture
  - https://developer.apple.com/documentation/swiftui/magnificationgesture
  - https://developer.apple.com/documentation/swiftui/rotationgesture
depends_on: []
related:
  - knowledge.swiftui.gesture-composition
updated: 2026-08-06
```

## Intent

Defines how agents implement pinch-to-zoom and rotation using
`MagnifyGesture`/`RotateGesture`, and flags the deprecated
`MagnificationGesture`/`RotationGesture` types.

## Scope

### Included

-   `MagnifyGesture` (`minimumScaleDelta`, `Value.magnification`)
-   `RotateGesture` (`minimumAngleDelta`, `Value.rotation`)
-   The deprecated `MagnificationGesture`/`RotationGesture` as a
    pre-iOS-17 fallback only

### Excluded

-   Drag and tap gestures — see `drag-gesture.md`,
    `tap-and-long-press-gestures.md`
-   Composing these with other gestures — see `gesture-composition.md`

## Rules

### Rule 1

Agents MUST use `MagnifyGesture` (not the deprecated
`MagnificationGesture`) and `RotateGesture` (not the deprecated
`RotationGesture`) for iOS 17+ deployment targets. Apple's
documentation marks both older gesture types deprecated with explicit
replacement notes: "Use MagnifyGesture instead" and "Use RotateGesture
instead."

### Rule 2

Agents MUST only use `MagnificationGesture`/`RotationGesture` when the
deployment target is below iOS 17 — `MagnifyGesture`/`RotateGesture`
require iOS 17+/macOS 14+.

### Rule 3

Agents MUST read pinch scale from `MagnifyGesture.Value.magnification`
and rotation from `RotateGesture.Value.rotation` (an `Angle`). Agents
MUST NOT assume these property names are interchangeable with the
deprecated types' value properties in generically-typed code — the
underlying value container types differ.

### Rule 4

Agents SHOULD set `minimumScaleDelta`/`minimumAngleDelta` above the
default when the view also recognizes a drag or tap gesture, to reduce
accidental multi-gesture conflicts from small incidental finger
movement during a pinch or rotate.

### Rule 5

Agents SHOULD compose `MagnifyGesture` and `RotateGesture` with
`.simultaneously(with:)` (see `gesture-composition.md`) when a view
must support pinch-to-zoom and rotate at the same time, rather than
nesting two separate `.gesture(...)` modifiers.

## Compliant Example

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0
    @State private var angle: Angle = .zero

    var body: some View {
        Image("photo")
            .scaleEffect(scale)
            .rotationEffect(angle)
            .gesture(
                MagnifyGesture()
                    .simultaneously(with: RotateGesture())
                    .onChanged { value in
                        if let magnify = value.first {
                            scale = magnify.magnification
                        }
                        if let rotate = value.second {
                            angle = rotate.rotation
                        }
                    }
            )
    }
}
```
Current `MagnifyGesture`/`RotateGesture` composed with
`.simultaneously(with:)`, reading `.magnification`/`.rotation` from
each gesture's `Value`. (Rules 1, 3, 5)

## Non-Compliant Example

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Image("photo")
            .scaleEffect(scale)
            .gesture(
                MagnificationGesture() // deprecated on iOS 17+ targets
                    .onChanged { value in
                        scale = value
                    }
            )
    }
}
```
Uses the deprecated `MagnificationGesture` on a project targeting
iOS 17+ instead of `MagnifyGesture`. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — MagnifyGesture](https://developer.apple.com/documentation/swiftui/magnifygesture)
-   [Apple Developer — RotateGesture](https://developer.apple.com/documentation/swiftui/rotategesture)
-   [Apple Developer — MagnificationGesture (deprecated)](https://developer.apple.com/documentation/swiftui/magnificationgesture)
-   [Apple Developer — RotationGesture (deprecated)](https://developer.apple.com/documentation/swiftui/rotationgesture)
