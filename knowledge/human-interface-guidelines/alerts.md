# Alerts

Status: Draft Version: 0.2.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.alerts
artifact_type: knowledge
title: Alerts
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for when to show an alert, its structure, and button placement/role on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - alerts
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/alerts
depends_on: []
related:
  - knowledge.human-interface-guidelines.action-sheets
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
  - knowledge.human-interface-guidelines.color
last_updated: 2026-08-08
```

## Intent

This contract defines when an AI coding agent should use an alert on
iOS/iPadOS, its structural limits, and button placement/role/style
conventions, so alerts stay reserved for genuinely critical,
actionable interruptions.

## Scope

### Included

-   When an alert is/isn't appropriate (critical + actionable only)
-   Title/message/button count limits
-   Button placement, default button, and destructive-style rules
-   Cancel-button requirement for destructive choices
-   Alert vs. action sheet decision (iOS/iPadOS)

### Excluded

-   SwiftUI `.alert`/UIKit `UIAlertController` implementation — see `swiftui`/`uikit` domains
-   Alert title/message copy wording — see `style-guide`
-   Destructive-red exact color value — see `color`

## Rules

### Rule 1

Agents MUST use alerts sparingly and only for information that's both
important and actionable — an alert MUST NOT be purely informational
with no meaningful choice attached.

### Rule 2

Agents MUST NOT show an alert for common, undoable destructive actions
(such as deleting a single email); alerts are reserved for uncommon,
non-undoable destructive actions someone might trigger unintentionally.

### Rule 3

Agents MUST NOT show an alert automatically at app launch; startup
issues (such as no network) MUST be surfaced through a non-interrupting
in-context indicator instead.

### Rule 4

Agents MUST limit an alert to a title, an optional short informative
message, and up to three buttons.

### Rule 5

Agents MUST place the button people are most likely to choose on the
trailing side of a button row (or top of a stack) and Cancel on the
leading side (or bottom of a stack); Cancel MUST NOT be the default
button.

### Rule 6

Agents MUST apply the destructive style only to a button whose action
the person did not deliberately/originally choose — not to a button
that confirms an action they intentionally initiated.

### Rule 7

Agents MUST include a Cancel button whenever the alert offers a
destructive choice, giving people a clear, safe way out.

### Rule 8

Agents MUST apply the alert-versus-action-sheet boundary defined in
`action-sheets` Rule 1 — alerts does not define a separate boundary
rule. In short: an alert confirms/cancels a single action or
communicates a problem; multiple choices related to an intentional
action belong in an action sheet.

## Compliant Example

-   ✓ A "Delete Photo" alert (uncommon, non-undoable) asks for confirmation with Delete and Cancel buttons. (Rule 2, Rule 7)
-   ✓ Deleting a single email produces no alert since the action is common and undoable. (Rule 2)
-   ✓ A network-unavailable state at launch is shown via a non-intrusive indicator, not a startup alert. (Rule 3)

## Non-Compliant Example

-   ✗ An alert appears on every app launch to announce a new feature. (Rule 3)
-   ✗ A deliberately chosen "Empty Trash" alert styles its confirm button as destructive even though the person intentionally chose that action. (Rule 6)
-   ✗ An alert offers three unrelated choices about how to proceed with an action instead of using an action sheet. (Rule 8)

## Dependencies

None.

## References

-   [Apple HIG — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
