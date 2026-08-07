# Tap and Long-Press Gestures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.tap-and-long-press-gestures
artifact_type: knowledge
title: Tap and Long-Press Gestures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of TapGesture, LongPressGesture, and their onTapGesture/onLongPressGesture shorthand modifiers, including count and maximumDistance configuration.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/tapgesture
  - https://developer.apple.com/documentation/swiftui/longpressgesture
  - https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:)
  - https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:)
depends_on: []
related:
  - knowledge.swiftui.gesture-composition
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent implements tap and
long-press interactions in SwiftUI using `TapGesture`, `LongPressGesture`,
and their `.onTapGesture`/`.onLongPressGesture` shorthand modifiers.

## Scope

### Included

-   `TapGesture(count:)` and `.onTapGesture(count:perform:)`
-   `LongPressGesture(minimumDuration:maximumDistance:)` and
    `.onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)`

### Excluded

-   Drag, magnification, and rotation gestures — see `drag-gesture.md`,
    `magnification-and-rotation-gestures.md`
-   Composing these gestures with others — see `gesture-composition.md`

## Rules

### Rule 1

Agents MUST use the `.onTapGesture(count:perform:)` shorthand modifier
for a plain tap action on a view, reserving the standalone
`TapGesture(count:)` gesture value for cases where it must be combined
with other gestures via `.simultaneously`/`.sequenced`/`.exclusively`.

### Rule 2

Agents MUST pass `count:` explicitly (default is `1`) when a double- or
multi-tap is required — SwiftUI does not expose a separate configurable
timing window for multi-tap recognition beyond the `count` value.

### Rule 3

Agents MUST set `maximumDistance` on `LongPressGesture`/
`.onLongPressGesture` deliberately, rather than relying on the
10-point default, when the target is a small control. The gesture
fails outright — it does not partial-recognize — if the touch moves
beyond `maximumDistance` before `minimumDuration` elapses.

### Rule 4

Agents MUST NOT assume `onPressingChanged` only fires on a successful
long press. It fires `true` on press-down and `false` on
release/cancel/failure, so success MUST be detected from the `perform`
closure, not from `onPressingChanged` alone.

### Rule 5

Agents SHOULD prefer `.onLongPressGesture` over composing a raw
`LongPressGesture` with `.updating` gesture state when only a simple
press/hold action is needed, not a value derived from the press.

## Compliant Example

```swift
struct DeletableRow: View {
    @State private var isPressed = false

    var body: some View {
        Text("Swipe or hold to delete")
            .onLongPressGesture(
                minimumDuration: 0.5,
                maximumDistance: 20,
                perform: { deleteRow() },
                onPressingChanged: { pressing in isPressed = pressing }
            )
            .onTapGesture(count: 2) { editRow() }
    }

    func deleteRow() {}
    func editRow() {}
}
```
Explicit `maximumDistance`, success handled in `perform` (not
`onPressingChanged`), explicit `count: 2` for double-tap. (Rules 2, 3, 4)

## Non-Compliant Example

```swift
struct DeletableRow: View {
    var body: some View {
        Text("Swipe or hold to delete")
            .onLongPressGesture(
                perform: { deleteRow() },
                onPressingChanged: { pressing in
                    if pressing { deleteRow() } // fires on press-down too, not just success
                }
            )
    }

    func deleteRow() {}
}
```
Treats `onPressingChanged`'s `true` case as success, so the delete
action fires on press-down instead of after the long-press completes.
(Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — TapGesture](https://developer.apple.com/documentation/swiftui/tapgesture)
-   [Apple Developer — LongPressGesture](https://developer.apple.com/documentation/swiftui/longpressgesture)
-   [Apple Developer — onTapGesture(count:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:))
-   [Apple Developer — onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:))
