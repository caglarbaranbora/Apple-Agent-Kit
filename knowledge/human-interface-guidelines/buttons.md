# Buttons

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.buttons
artifact_type: knowledge
title: Buttons
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for button hit targets, press states, prominence, role assignment, and content on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - buttons
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/buttons
depends_on: []
related:
  - knowledge.style-guide.general-button-labels
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.human-interface-guidelines.color
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent sizes, styles, and assigns
semantic roles to buttons on iOS/iPadOS so their function, prominence,
and destructive/primary status are visually unambiguous.

## Scope

### Included

-   Minimum hit-target sizing
-   Press/highlight state requirements
-   Prominent-style usage and limits
-   Style vs. size for distinguishing preferred choices
-   Role assignment (normal, primary, cancel, destructive)
-   Icon vs. text content selection
-   Inline activity indicator for delayed actions

### Excluded

-   SwiftUI `Button`/UIKit `UIButton` implementation — see `swiftui`/`uikit` domains
-   Exact button label wording/capitalization — see `style-guide`
-   Symbol rendering/configuration API — see `sf-symbols` domain

## Rules

### Rule 1

Agents MUST provide a hit region of at least 44x44 pt for every
button, with enough surrounding space to visually distinguish it from
neighboring content and controls.

### Rule 2

Agents MUST provide a distinct press/highlighted state for any custom
button so it doesn't feel unresponsive to input.

### Rule 3

Agents SHOULD reserve a prominent (accent-colored/filled) style for
the single most likely action in a view, keeping prominent buttons to
one or two per view.

### Rule 4

Agents MUST use style — not size — to distinguish the preferred option
among a set of same-purpose buttons; buttons that form a coherent set
of choices MUST share the same size.

### Rule 5

Agents MUST NOT assign the primary/default role to a button that
performs a destructive action, even when that action is the most
likely choice.

### Rule 6

Agents SHOULD associate familiar system actions with familiar SF
Symbols icons, and use a short, verb-first text label when a label
communicates the action more clearly than an icon alone.

### Rule 7

Agents SHOULD configure a button to show an inline activity indicator
(optionally with an updated label) when its action doesn't complete
instantly, rather than leaving the button static during the delay.

## Compliant Example

-   ✓ A destructive "Delete Account" button uses the destructive/normal role, not primary, even though it's the likely next step in that flow. (Rule 5)
-   ✓ A "Checkout" button switches to an inline spinner plus a "Checking Out…" label during a network delay. (Rule 7)
-   ✓ Two same-purpose buttons share identical size; the preferred one is differentiated only by a prominent style. (Rule 4)

## Non-Compliant Example

-   ✗ A 30x30 pt icon button has no surrounding padding, making it hard to tap accurately. (Rule 1)
-   ✗ A destructive "Erase All Content" button is styled and assigned as the primary/default button. (Rule 5)
-   ✗ Three buttons in the same view all use the prominent, accent-colored style. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
