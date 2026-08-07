# Authentication

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.authentication
artifact_type: reference
title: Authentication
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for the `authentication` domain.
domain: Authentication
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/design/human-interface-guidelines/
https://help.apple.com/applestyleguide/

## Purpose

Reference index for the `authentication` domain: sign-in terminology,
entry points, user-facing authentication flows, and authentication-related
UI decisions (button labels, accessibility forms), sourced from Apple's
Human Interface Guidelines and Apple Style Guide. StoreKit authentication,
passkeys implementation, Sign in with Apple implementation, authentication
networking, and backend architecture are out of scope — see the relevant
KC's own Excluded section. Biometric and device-passcode authentication
(Face ID/Touch ID/LocalAuthentication framework) is owned by
`local-authentication`, a clean handoff — see
docs/architecture/domain-map.md Cross-Domain Notes.

## Primary Topics

- Authentication terminology
- Authentication entry points
- User-facing authentication flows
- Authentication-related UI decisions (button labels, accessibility forms)

## Used By

- knowledge/authentication/authentication.md ([[knowledge/authentication/authentication]])
- knowledge/authentication/sign-in-terminology.md ([[knowledge/authentication/sign-in-terminology]])
- knowledge/authentication/button-labels.md ([[knowledge/authentication/button-labels]])
- knowledge/authentication/accessibility-forms.md ([[knowledge/authentication/accessibility-forms]])
