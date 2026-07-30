# Pointer and Click Terminology

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.pointer-and-click-terminology
type: knowledge
title: Pointer and Click Terminology
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct verbs and nouns for pointer, mouse, and click-based interactions, for the secondary pointer-support surface on iPad and Mac Catalyst.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - pointer
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.touch-gesture-verbs
  - knowledge.style-guide.ui-action-verbs
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent describes pointer, mouse, and
click-based interactions — click, click and drag, click and hold, double
click, right-click, mouse, and cursor — in UI text and documentation for
Apple platforms. It exists so an agent doesn't default to desktop-borrowed
"click on"/"right-click" phrasing when writing for touch-first surfaces
that also support a pointer, such as iPad with trackpad/mouse support or
Mac Catalyst apps.

## Scope

### Included

-   Core click verbs: click, click on, click and drag, click and hold, click in
-   Click-count verbs: double click, double press
-   Platform-specific secondary-click term: right-click
-   Pointer hardware/element nouns: mouse, cursor

### Excluded

-   Touchscreen gesture verbs (tap, swipe, pinch, drag, etc.) (see `touch-gesture-verbs`)
-   The pointer itself as an onscreen element, and "insertion point" (not in this glossary excerpt)

## Rules

### Rule 1

Agents MUST use click to describe positioning the pointer over an onscreen
element and briefly pressing and releasing the mouse or trackpad. Agents
MUST NOT say "click the mouse" or "click the trackpad" to mean this action;
use press and release instead.

### Rule 2

Agents MUST NOT use click on. Use click instead.

### Rule 3

Agents MUST NOT use click and drag. An item is either clicked or dragged,
never both in one verb.

### Rule 4

Agents MUST use click and hold only for positioning the pointer on an item
and pressing the mouse or trackpad until something happens (e.g. rewind by
holding a button). Agents MUST NOT use click and hold for pressing deeper
on a Force Touch trackpad; use force click for that.

### Rule 5

Agents MUST use click in only for windows or screen areas (e.g. an image);
use click alone for onscreen elements such as icons and buttons.

### Rule 6

Agents MUST hyphenate double click by part of speech: double click (n.),
double-click (v.), double-clicking (n., v.).

### Rule 7

Agents MUST use double press only for quickly pressing twice on the stem
of some AirPods models. Agents MUST NOT use double press for pressing a
mechanical button (Home button, side button, top button, Digital Crown)
twice; use double-click for that instead.

### Rule 8

Agents MUST use right-click only for Windows content, to describe clicking
the secondary (usually right) mouse button. Agents MUST use Control-click
instead when documenting the equivalent action on Mac.

### Rule 9

Agents SHOULD avoid referring to the mouse when possible, switching
emphasis to the onscreen action (clicking, dragging, selecting, choosing)
instead. Agents MUST NOT pluralize mouse as "mouses"; use mouse devices or
mice.

### Rule 10

Agents MUST NOT use cursor to describe the macOS or iOS interface; use
insertion point or pointer depending on context. Cursor MAY be used when
describing the VoiceOver interface or other contexts where it's the
platform's own term.

## Compliant Example

-   ✓ "Click the Mail icon in the Dock." (Rule 1)
-   ✓ "Drag the icon to the Trash." not "Click and drag the icon" (Rule 3)
-   ✓ "Click and hold the Next button to fast-forward." (Rule 4)
-   ✓ "Click in the image to place the insertion point." (Rule 5)
-   ✓ "You open a folder by double-clicking it." (Rule 6)
-   ✓ "Double-press the stem to skip to the next track." (Rule 7)
-   ✓ "Windows: Right-click the app icon." / "Mac: Control-click the app icon." (Rule 8)
-   ✓ "Apple offers several types of mouse devices." (Rule 9)
-   ✓ "Use insertion point or pointer" instead of cursor for macOS/iOS text (Rule 10)

## Non-Compliant Example

-   ✗ "Click on the Mail icon in the Dock." (Rule 2)
-   ✗ "Click and drag the icon to the Trash." (Rule 3)
-   ✗ "Click and hold the trackpad to force click." (Rule 4)
-   ✗ "Click the image to place the insertion point." meaning click in (Rule 5)
-   ✗ "To view your open apps, double-press the Home button." (Rule 7)
-   ✗ "Right-click the app icon to open a shortcut menu." written for Mac (Rule 8)
-   ✗ "Connect several mouses to your Mac." (Rule 9)
-   ✗ "Move the cursor to the top of the screen." describing macOS (Rule 10)

## Dependencies

None.

## References

-   [Apple Style Guide — click; click and drag; click and hold; click in; click on (p. 51)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — cursor (p. 61)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — double click (n.), double-click (v.), double-clicking (n., v.) (p. 72)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — double press (n.), double-press (v.), double-pressing (n., v.) (p. 73)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — mouse (p. 145)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — right-click (v.) (p. 177)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
