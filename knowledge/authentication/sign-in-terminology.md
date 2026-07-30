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
  - knowledge.style-guide.sign-in-and-authentication-terminology
related:
  - knowledge.authentication.button-labels
updated: 2026-07-30
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
-   General sign-in/sign-out hyphenation, part-of-speech forms, and
    preposition usage (see
    knowledge/style-guide/sign-in-and-authentication-terminology.md,
    [[knowledge/style-guide/sign-in-and-authentication-terminology]])

## Rules

### Rule 1

In this authentication flow's internet-account context, use **Sign In**
and **Sign Out**, not "Log In," "Login," or "Authenticate." These are not
interchangeable synonyms: Apple reserves "Login"/"Log in" for a different
context (starting a local system-account session, e.g. logging in to a
file server), and "Authenticate" is developer-facing terminology, not
user-facing text. See
knowledge/style-guide/sign-in-and-authentication-terminology.md
([[knowledge/style-guide/sign-in-and-authentication-terminology]]) for the
full hyphenation, verb-form, and preposition rules governing both terms.

### Rule 2

Maintain identical terminology across screens within the same
authentication flow.

## Compliant Example

✓ Sign In

✓ Sign Out

✓ Sign in with Apple

## Non-Compliant Example

✗ Login (used in place of Sign In for an internet-account flow)

✗ Log into your account (wrong term for this context, and "into" is
never correct for this phrasal verb — see
knowledge/style-guide/sign-in-and-authentication-terminology.md Rule 7)

✗ Authenticate User

Violation:

-   Conflates Sign In with a different Apple-defined term (Login) or
    developer-only terminology (Authenticate).
-   Reduced platform consistency.

## Dependencies

-   knowledge.authentication.authentication
-   knowledge.style-guide.sign-in-and-authentication-terminology

## References

-   Apple Human Interface Guidelines
-   Apple Style Guide
