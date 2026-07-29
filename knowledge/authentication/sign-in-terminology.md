# Sign In Terminology

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authentication.sign-in-terminology
type: knowledge
title: Sign In Terminology
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the terminology rules for authentication-related user interfaces.
domain: Authentication
tags:
  - authentication
  - terminology
  - sign-in
references:
  - https://developer.apple.com/design/human-interface-guidelines/
  - https://help.apple.com/applestyleguide/
depends_on:
  - knowledge.authentication.authentication
related:
  - knowledge.authentication.button-labels
updated: 2026-07-29
```

## Intent

This contract defines the terminology an AI coding agent must use when
implementing authentication interfaces for Apple platforms.

## Scope

### Included

-   Sign in terminology
-   Sign out terminology
-   Account-related authentication wording

### Excluded

-   Button styling
-   Accessibility labels
-   Authentication implementation
-   Backend authentication

## Rules

### Rule 1

Use Apple's preferred terminology consistently.

### Rule 2

Use **Sign In** and **Sign Out** as two-word verb phrases.

### Rule 3

Do not invent synonyms such as "Log In", "Login", or "Authenticate"
unless required by an external API or product name.

### Rule 4

Maintain identical terminology across screens within the same
authentication flow.

## Compliant Example

✓ Sign In

✓ Sign Out

✓ Sign in with Apple

## Non-Compliant Example

✗ Login

✗ Log into your account

✗ Authenticate User

Violation:

-   Inconsistent Apple terminology.
-   Reduced platform consistency.

## Dependencies

-   knowledge.authentication.authentication

## References

-   Apple Human Interface Guidelines
-   Apple Style Guide
