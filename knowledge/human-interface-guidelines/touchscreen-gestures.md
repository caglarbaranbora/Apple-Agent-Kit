# Touchscreen Gestures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.touchscreen-gestures
type: knowledge
title: Touchscreen Gestures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using standard vs. custom touch gestures on iOS/iPadOS, including alternate-input and feedback requirements.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - touchscreen-gestures
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/gestures
depends_on: []
related:
  - knowledge.style-guide.touch-gesture-verbs
  - knowledge.accessibility.full-keyboard-access-and-focus
updated: 2026-08-06
```

## Intent

Apple renamed this page from "Touchscreen gestures" to "Gestures" (the
`touchscreen-gestures` URL now redirects there) when it broadened scope
to cover indirect/direct input across platforms. This contract keeps
the original filename per the touch-focused scope requested, and
restricts its Rules to the iOS/iPadOS touchscreen subset: when to use
standard vs. custom gestures, feedback, and alternate-input
availability.

## Scope

### Included

-   Alternate-input availability for gesture-driven actions
-   Standard gesture consistency (don't repurpose or reinvent)
-   In-progress gesture feedback
-   Unavailable-gesture communication
-   Custom gesture design criteria
-   iOS/iPadOS standard system gestures (three-finger swipe/pinch, four-finger swipe)

### Excluded

-   `UIGestureRecognizer`/SwiftUI gesture modifier implementation — see `swiftui`/`uikit` domains
-   VoiceOver/Switch Control gesture mechanics — see `accessibility` domain
-   Gesture-verb copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST offer more than one way to perform any given task — a
specific gesture MUST NOT be the only way to accomplish something.

### Rule 2

Agents MUST respond to standard gestures (tap, swipe, drag,
touch-and-hold, pinch/zoom) consistently with their system-wide
meaning, MUST NOT repurpose a standard gesture to perform an
app-unique action, and MUST NOT invent a custom gesture to perform a
standard action such as activating a button or scrolling.

### Rule 3

Agents MUST provide immediate, responsive feedback while a gesture is
in progress so people can predict its result.

### Rule 4

Agents MUST clearly indicate when a gesture isn't currently available,
rather than leaving the interaction silently unresponsive.

### Rule 5

Agents SHOULD add a custom gesture only for a frequent, specialized
task not covered by standard gestures, and only when it is
discoverable, easy to perform, distinct from other gestures, and not
the only way to perform an important action.

### Rule 6

Agents SHOULD use a custom/shortcut gesture only as a supplement to —
never a replacement for — the standard tappable control it accelerates.

### Rule 7

Agents MUST support the standard iOS three-finger swipe (undo/redo)
and three-finger pinch (copy/paste) system gestures without conflict,
and on iPadOS MUST avoid conflicting with the four-finger swipe
app-switching gesture.

## Compliant Example

-   ✓ A drawing app adds a custom two-finger tap to undo, but a visible Undo button and the standard three-finger swipe still work. (Rule 6)
-   ✓ Dragging a locked item shows a resistance animation instead of silently doing nothing. (Rule 4)

## Non-Compliant Example

-   ✗ Swiping right on a list item performs a unique, app-specific action instead of the expected reveal-actions behavior. (Rule 2)
-   ✗ A key action is reachable only via a custom three-finger rotate gesture with no button alternative. (Rule 1, Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) (the former `touchscreen-gestures` URL now redirects here)
