# Undo and Redo

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.undo-and-redo
type: knowledge
title: Undo and Redo
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for predictable, discoverable undo and redo behavior on iOS/iPadOS, including standard gesture and alert conventions.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - undo-and-redo
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/undo-and-redo
depends_on: []
related:
  - knowledge.human-interface-guidelines.feedback
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent designs undo and redo on
iOS/iPadOS so people can predict and see the outcome of reversing
their actions, using standard system-supported triggers rather than
redefined gestures or unlimited custom UI.

## Scope

### Included

-   Making undo/redo outcomes predictable (descriptive labels)
-   Surfacing the visible result of an undo/redo
-   Undo depth (how many actions back people can go)
-   Batch/revert-all options
-   Standard iOS/iPadOS undo/redo triggers (shake-to-undo alert, three-finger swipe, keyboard shortcut)
-   When dedicated undo/redo buttons are appropriate

### Excluded

-   Undo/redo implementation code (undo manager, command stack)
-   Undo/redo alert and menu-item copy wording — see `style-guide`
-   macOS Edit-menu placement and keyboard-shortcut conventions (out of scope for this iOS/iPadOS contract)
-   Toolbar button icon rendering mechanics — see `sf-symbols`

## Rules

### Rule 1

Agents MUST help people predict the outcome of an undo or redo action
— for example, a descriptive shake-to-undo alert or a menu item that
names the action (e.g., "Undo Typing") — rather than a bare,
unqualified "Undo"/"Redo" label.

### Rule 2

Agents MUST make the result of an undo or redo visible, scrolling to
or otherwise surfacing off-screen content so people can see that the
action took effect.

### Rule 3

Agents SHOULD NOT impose an artificial limit on the number of
sequential undo/redo actions; support undoing back through every
action taken since the last logical checkpoint (e.g., opening or
saving a document).

### Rule 4

Agents SHOULD consider offering a way to revert a batch of related
changes at once, or all changes since the last open/save, when that
fits the task.

### Rule 5

Agents MUST NOT redefine the standard iOS/iPadOS undo/redo gestures
(three-finger swipe, shake-to-undo) for a different purpose.

### Rule 6

Agents SHOULD rely on system-supported undo/redo triggers
(shake-to-undo alert, three-finger swipe, a hardware keyboard
shortcut on iPad) rather than adding dedicated undo/redo buttons; if
buttons are necessary, use the standard system-provided symbols in a
toolbar.

## Compliant Example

-   ✓ Shaking the device on iPhone shows an alert reading "Undo Typing" with Undo and Cancel options. (Rule 1)
-   ✓ Undoing the deletion of an off-screen paragraph scrolls the document to show the restored text. (Rule 2)
-   ✓ A drawing app lets people undo every stroke back to when the canvas was opened, with no fixed step limit. (Rule 3)

## Non-Compliant Example

-   ✗ The undo alert reads only "Undo" with no indication of what will be reversed. (Rule 1)
-   ✗ Undo is capped at the last 5 actions regardless of how many changes were made. (Rule 3)
-   ✗ The three-finger swipe gesture is repurposed for page navigation instead of undo/redo. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Undo and Redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)
