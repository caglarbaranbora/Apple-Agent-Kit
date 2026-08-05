# Sheets

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.sheets
type: knowledge
title: Sheets
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for presenting, sizing, and dismissing sheets on iOS/iPadOS, including detents, grabbers, and button placement.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - sheets
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/sheets
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.human-interface-guidelines.materials
  - knowledge.human-interface-guidelines.alerts
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent presents, sizes, and
dismisses sheets on iOS/iPadOS: single-sheet stacking, dismissal
buttons, detents/grabbers, and when a sheet is the right surface versus
a full-screen presentation.

## Scope

### Included

-   Single-sheet-at-a-time stacking rule
-   Cancel/Done/Back button placement and pairing
-   Swipe-to-dismiss and unsaved-changes confirmation
-   Detents, grabber, and progressive disclosure
-   Page/form sheet presentation style on iPadOS
-   Sheet vs. full-screen presentation for scoped vs. prolonged tasks

### Excluded

-   SwiftUI `.sheet`/UIKit presentation-controller implementation — see `swiftui`/`uikit` domains
-   Sheet button copy wording — see `style-guide`
-   Blur/material rendering mechanics — see `materials`

## Rules

### Rule 1

Agents MUST display only one sheet at a time from the main interface;
if an action inside a sheet needs to present another sheet, the first
MUST be dismissed before the second appears.

### Rule 2

Agents MUST pair a Done button with a Cancel (or Back) button rather
than relying on Done alone as the only way to leave the sheet, and
MUST NOT show Cancel, Done, and Back together at once.

### Rule 3

Agents MUST support swipe-to-dismiss on an iOS/iPadOS sheet, and MUST
present a confirmation (such as an action sheet) if dismissing would
discard unsaved changes.

### Rule 4

Agents MUST place the Cancel/Close button on the leading edge and the
Done button on the trailing edge of a single-view sheet's top toolbar.

### Rule 5

Agents SHOULD include a grabber on a resizable sheet and support the
medium detent for progressive disclosure, unless the sheet's content
is only useful at full height.

### Rule 6

Agents SHOULD prefer the page or form sheet presentation style on
iPadOS for a consistent, centered, default-sized sheet rather than a
custom size.

### Rule 7

Agents SHOULD reserve a sheet for a scoped, closely related task tied
to the current context, and use a full-screen presentation instead for
prolonged or complex multistep flows such as document or photo
editing.

## Compliant Example

-   ✓ A share sheet supports the medium detent so its most relevant items are visible without full expansion. (Rule 5)
-   ✓ Swiping down on a sheet with unsaved edits triggers a confirming action sheet before dismissing. (Rule 3)
-   ✓ A compose sheet shows Cancel on the leading edge and Send/Done on the trailing edge. (Rule 4)

## Non-Compliant Example

-   ✗ A sheet displays Cancel, Done, and Back buttons simultaneously. (Rule 2)
-   ✗ Closing one sheet immediately reveals a second, previously hidden sheet stacked behind it. (Rule 1)
-   ✗ A multistep photo-editing flow is crammed into a single fixed-height sheet instead of a full-screen presentation. (Rule 7)

## Dependencies

None.

## References

-   [Apple HIG — Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
