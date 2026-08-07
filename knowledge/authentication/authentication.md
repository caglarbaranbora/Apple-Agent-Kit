# Authentication

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authentication.authentication
artifact_type: knowledge
title: Authentication
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the foundational authentication rules for Apple platform applications.
domain: Authentication
tags:
  - authentication
  - sign-in
  - login
references:
  - https://developer.apple.com/design/human-interface-guidelines/
depends_on: []
related:
  - knowledge.authentication.sign-in-terminology
last_updated: 2026-07-29
```

## Intent

This contract defines the baseline authentication requirements that an
AI coding agent must follow before implementing any authentication flow
on an Apple platform.

## Scope

### Included

-   Authentication terminology
-   Authentication entry points
-   User-facing authentication flows
-   Authentication-related UI decisions

### Excluded

-   StoreKit authentication
-   Passkeys implementation details
-   Sign in with Apple implementation
-   Authentication networking
-   Backend architecture

## Rules

### Rule 1

Authentication flows MUST use Apple's official terminology and
interaction patterns.

### Rule 2

Authentication-related decisions MUST be delegated to more specific
Knowledge Contracts when available.

### Rule 3

This contract defines foundational rules only and MUST NOT duplicate
guidance contained in child contracts.

### Rule 4

Implementation-specific details MUST remain outside this contract.

## Compliant Example

Task:

> Implement a login screen.

Agent loads:

-   Authentication
-   Sign In Terminology
-   Button Labels
-   Accessibility Forms

The implementation follows specialized contracts instead of embedding
assumptions.

## Non-Compliant Example

Task:

> Implement login.

Agent immediately decides button text, accessibility labels, and
terminology without loading the related contracts.

Violation:

-   Skips required dependencies
-   Introduces implicit knowledge
-   Breaks deterministic routing

## Dependencies

Required during implementation:

-   `knowledge.authentication.sign-in-terminology`

## References

-   Apple Human Interface Guidelines
-   Apple Style Guide
-   Apple Developer Documentation
