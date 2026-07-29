# Button Labels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authentication.button-labels
type: knowledge
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
related:
  - knowledge.authentication.accessibility-forms
updated: 2026-07-29
```

## Intent

Define the button labeling rules an AI coding agent must follow for
authentication interfaces.

## Scope

Included: - Primary authentication buttons - Secondary authentication
actions

Excluded: - Visual styling - Layout - Accessibility labels

## Rules

1.  Primary actions MUST use concise verb phrases.
2.  Labels MUST match Apple terminology.
3.  Avoid redundant words such as "Click" or "Press".
4.  Keep labels consistent across the flow.

## Compliant Example

-   Sign In
-   Continue
-   Create Account

## Non-Compliant Example

-   Click Here
-   Login Now
-   Press to Continue

Violation: - Non-standard terminology - Unnecessary wording

## Dependencies

-   knowledge.authentication.sign-in-terminology

## References

-   Apple Human Interface Guidelines
-   Apple Style Guide
