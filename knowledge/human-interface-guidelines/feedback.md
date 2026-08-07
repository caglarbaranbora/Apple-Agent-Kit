# Feedback

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.feedback
artifact_type: knowledge
title: Feedback
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for matching the form and interruption level of interface feedback to the significance of the information it communicates on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - feedback
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/feedback
depends_on: []
related:
  - knowledge.human-interface-guidelines.notifications
  - knowledge.human-interface-guidelines.accessibility
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent designs feedback on
iOS/iPadOS — status, success/failure, warnings, and error
explanations — matching the delivery mechanism to the significance of
the information.

## Scope

### Included

-   Matching feedback interruption level to information significance
-   Passive/inline status feedback placement
-   When to use alerts vs. passive feedback
-   Data-loss warning timing
-   Success/failure confirmation timing
-   Explaining why a command can't be carried out
-   Multi-channel (accessible) feedback delivery

### Excluded

-   Feedback UI implementation code
-   Alert/feedback copy wording — see `style-guide`
-   Haptic feedback implementation
-   Notification-specific content rules — see `notifications`
-   Accessibility API implementation for non-visual feedback channels — see `accessibility` domain

## Rules

### Rule 1

Agents MUST deliver feedback through more than one channel (e.g.,
text or shape paired with color, plus optional sound/haptics) so it
reaches people regardless of how they perceive the device (see
`accessibility`).

### Rule 2

Agents SHOULD integrate passive status feedback into the interface
near the content it describes (e.g., an unread count in a toolbar)
rather than requiring people to take an action to check it.

### Rule 3

Agents MUST match the interruption level of feedback to the
significance of the information: reserve alerts for critical,
ideally actionable information, and avoid using alerts so often that
they lose impact.

### Rule 4

Agents MUST warn people before an action causes data loss that is
unexpected and irreversible, and MUST NOT warn when data loss is the
obvious, expected result of the action.

### Rule 5

Agents SHOULD confirm completion only for significant actions whose
success can't be assumed; avoid adding confirmation feedback for
routine actions people already expect to succeed.

### Rule 6

Agents MUST explain why a command can't be carried out when blocking
or rejecting an action, not just that it failed.

## Compliant Example

-   ✓ A mail app shows the unread-message count directly in the mailbox toolbar rather than requiring a manual refresh check. (Rule 2)
-   ✓ Deleting a file to the Trash produces no warning (expected, recoverable), while permanently erasing it produces a warning alert. (Rule 4)
-   ✓ A directions request with the same start and end location shows an explanation instead of a silent failure. (Rule 6)

## Non-Compliant Example

-   ✗ Success or failure is communicated with a color change alone, with no text or icon. (Rule 1)
-   ✗ An alert interrupts the person for a routine, always-successful action. (Rule 3, 5)
-   ✗ An action silently fails with no explanation of why it couldn't be completed. (Rule 6)

## Dependencies

None.

## References

-   [Apple HIG — Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
