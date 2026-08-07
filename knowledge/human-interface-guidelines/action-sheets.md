# Action Sheets

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.action-sheets
artifact_type: knowledge
title: Action Sheets
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using an action sheet to offer choices related to an intentionally initiated action on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - action-sheets
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/action-sheets
depends_on: []
related:
  - knowledge.human-interface-guidelines.alerts
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
last_updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use an action
sheet on iOS/iPadOS rather than an alert or a menu, and how to
structure its title, buttons, and destructive-choice styling.

## Scope

### Included

-   Action sheet vs. alert decision
-   Action sheet vs. menu decision (iOS/iPadOS)
-   Title/message brevity
-   Cancel button placement, destructive-button styling and position
-   Scroll avoidance / button-count limits

### Excluded

-   SwiftUI `.confirmationDialog`/UIKit `UIAlertController` (`.actionSheet`) implementation — see `swiftui`/`uikit` domains
-   Action sheet title/button copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST use an action sheet — not an alert — to offer choices
related to an action people intentionally initiated; alerts are
reserved for unexpected problems or confirming/canceling a single
action.

### Rule 2

Agents MUST use an action sheet — not a menu — when the choices are a
direct clarification of an action someone just performed; menus are
for choices people open deliberately, not responses to a triggered
action.

### Rule 3

Agents SHOULD keep the action sheet title short enough to fit on a
single line, and add a message only when the title plus context isn't
enough to convey the choices.

### Rule 4

Agents MUST place a Cancel button (when the sheet needs one) at the
bottom of the action sheet, and MUST style destructive choices with
the destructive style, positioned at the top where they're most
noticeable.

### Rule 5

Agents MUST NOT let an action sheet scroll — keep the number of
buttons small enough to avoid scrolling and reduce the risk of
mis-tapping a button while scrolling.

### Rule 6

Agents MUST use action sheets sparingly, interrupting the current task
only when a clarifying choice is genuinely necessary.

## Compliant Example

-   ✓ Canceling an in-progress email draft shows an action sheet with Delete Draft / Save Draft / Cancel choices. (Rule 1)
-   ✓ The destructive "Delete Draft" choice uses the destructive style and appears at the top of the sheet. (Rule 4)

## Non-Compliant Example

-   ✗ A five-button action sheet requires scrolling to see all choices. (Rule 5)
-   ✗ An unrelated confirmation ("Turn on Notifications?") is presented as an action sheet instead of an alert. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Action Sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)
