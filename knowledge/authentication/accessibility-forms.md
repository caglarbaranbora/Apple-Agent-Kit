# Accessibility Forms

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authentication.accessibility-forms
type: knowledge
title: Accessibility Forms
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines accessibility requirements for authentication forms.
domain: Accessibility
tags:
  - accessibility
  - authentication
  - forms
references:
  - https://developer.apple.com/design/human-interface-guidelines/accessibility/
depends_on:
  - knowledge.authentication.button-labels
related:
  - knowledge.authentication.authentication
updated: 2026-07-29
```

## Intent

This contract defines the accessibility rules an AI coding agent must
follow when implementing authentication forms on Apple platforms.

## Scope

### Included

-   Login forms
-   Sign-up forms
-   Password fields
-   Validation messages
-   Focus order

### Excluded

-   Visual design
-   Authentication logic
-   Backend validation

## Rules

### Rule 1

Every interactive control MUST expose an accessible label.

### Rule 2

Validation errors MUST be programmatically available to assistive
technologies.

### Rule 3

Focus order MUST follow the visual reading order.

### Rule 4

Authentication forms MUST remain usable with VoiceOver.

## Compliant Example

-   Email field has an accessibility label.
-   Password field exposes secure text entry.
-   Error message is announced by VoiceOver.

## Non-Compliant Example

-   Placeholder used instead of an accessibility label.
-   Error indicated only by color.
-   Button cannot be reached via accessibility navigation.

Violation:

-   Fails accessibility requirements.
-   Reduces usability for assistive technology users.

## Dependencies

-   knowledge.authentication.button-labels

## References

-   Apple Human Interface Guidelines -- Accessibility
-   Apple Accessibility Documentation
