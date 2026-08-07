# Button Labels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authentication.button-labels
artifact_type: knowledge
title: Button Labels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for authentication button labels.
domain: Authentication
tags:
  - authentication
  - buttons
references:
  - https://developer.apple.com/design/human-interface-guidelines/
  - https://help.apple.com/applestyleguide/
depends_on:
  - knowledge.authentication.sign-in-terminology
  - knowledge.style-guide.general-button-labels
related:
  - knowledge.authentication.accessibility-forms
  - knowledge.style-guide.general-button-labels
last_updated: 2026-07-30
```

## Intent

Define the button labeling rules an AI coding agent must follow for
authentication interfaces.

## Scope

### Included

-   Primary authentication buttons
-   Secondary authentication actions

### Excluded

-   Visual styling
-   Layout
-   Accessibility labels
-   General button-quoting, icon-naming, and OK/user-name/allow wording
    — see `knowledge.style-guide.general-button-labels`

## Rules

### Rule 1

Primary actions MUST use concise verb phrases.

### Rule 2

Labels MUST match Apple terminology.

### Rule 3

Avoid redundant words such as "Click" or "Press".

### Rule 4

Keep labels consistent across the flow.

## Compliant Example

-   Sign In (Rules 1, 2)
-   Continue (Rule 1)
-   Create Account (Rules 1, 2)

## Non-Compliant Example

-   Click Here (Rule 3 — redundant "Click")
-   Login Now (Rule 2 — non-standard terminology; Apple's term is "Log In"/"Sign In")
-   Press to Continue (Rule 3 — redundant "Press")

Violation:

-   Non-standard terminology
-   Unnecessary wording

## Dependencies

-   knowledge.authentication.sign-in-terminology
-   knowledge.style-guide.general-button-labels

## References

-   Apple Human Interface Guidelines
-   Apple Style Guide
