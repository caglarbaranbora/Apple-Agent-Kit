# Custom Accessibility Actions

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.custom-accessibility-actions
artifact_type: knowledge
title: Custom Accessibility Actions
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of .accessibilityAction() (SwiftUI) and UIAccessibilityCustomAction (UIKit) to give VoiceOver users a reachable alternative to gesture-only interactions like swipe-to-delete or drag-to-reorder.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - actions
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction
depends_on: []
related:
  - knowledge.accessibility.full-keyboard-access-and-focus
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent exposes gesture-only
interactions (swipe-to-delete, drag-to-reorder, long-press) to VoiceOver
via `.accessibilityAction()` (SwiftUI) or `UIAccessibilityCustomAction`
(UIKit), since VoiceOver intercepts standard touch gestures for its own
navigation.

## Scope

### Included

-   `.accessibilityAction(named:_:)` for named custom actions
-   `UIAccessibilityCustomAction`/`accessibilityCustomActions`
-   `.accessibilityAction(.magicTap)` for a screen's primary action
-   Action naming

### Excluded

-   Moving VoiceOver/keyboard focus itself — see `full-keyboard-access-and-focus`

## Rules

### Rule 1

Agents MUST provide an `.accessibilityAction()` (or
`UIAccessibilityCustomAction`) equivalent for any interaction reachable
only through a gesture VoiceOver intercepts (swipe-to-delete on a list
row, drag-to-reorder, long-press context menus) — without one, VoiceOver
users cannot perform that action at all.

### Rule 2

Agents MUST give each custom action a clear, verb-based name ("Delete",
"Move up") describing the action, not the gesture it replaces ("Swipe
left").

### Rule 3

Agents SHOULD implement `.accessibilityAction(.magicTap)` for a screen's
single most common action (e.g. play/pause on a media player) so a
two-finger double-tap performs it without navigating to a specific
element first.

### Rule 4

Agents MUST NOT rely on multi-finger or complex custom gestures
(pinch, multi-finger swipe) as the only way to trigger a feature without
also exposing a custom action or standard control, since VoiceOver
remaps most multi-finger gestures to its own navigation.

## Compliant Example

```swift
RowView(item: item)
    .accessibilityAction(named: "Delete") {
        delete(item)
    }
    .accessibilityAction(named: "Move Up") {
        moveUp(item)
    }
```
Swipe-to-delete and drag-to-reorder both get named VoiceOver-reachable equivalents. (Rules 1, 2)

## Non-Compliant Example

```swift
RowView(item: item)
    .swipeActions {
        Button("Delete", role: .destructive) { delete(item) }
    }
```
`.swipeActions` alone is reachable by touch but not guaranteed to surface to VoiceOver as an activatable action without an explicit `.accessibilityAction()`; a VoiceOver user swiping through the list has no way to trigger the delete. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityAction(named:_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:))
-   [Apple Developer — UIAccessibilityCustomAction](https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction)
