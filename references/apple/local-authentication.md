# Local Authentication

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.local-authentication
artifact_type: reference
title: Local Authentication
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's LocalAuthentication framework documentation, scoped to this domain's v1.
domain: Local Authentication
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/bundleresources/information-property-list/nsfaceidusagedescription
https://developer.apple.com/documentation/localauthentication
https://developer.apple.com/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id
https://developer.apple.com/documentation/localauthentication/labiometrytype
https://developer.apple.com/documentation/localauthentication/lacontext
https://developer.apple.com/documentation/localauthentication/laerror-swift.struct
https://developer.apple.com/documentation/localauthentication/lapolicy
https://developer.apple.com/documentation/localauthentication/logging-a-user-into-your-app-with-face-id-or-touch-id
https://developer.apple.com/documentation/security/secaccesscontrolcreateflags

## Purpose

Reference index for Apple's LocalAuthentication framework documentation,
scoped to this domain's v1: biometry availability and type detection,
policy evaluation, reason-string/Info.plist requirements, error handling,
context lifecycle, Keychain-biometric binding, and fallback UX.
macOS/watchOS-specific behavior, general Keychain storage APIs (owned by
the `security` domain, built 2026-08), and Sign in with Apple (owned by the
`authenticationservices` domain, built 2026-08, which defers passkeys and
WebAuthn within its own scope; the `authentication` domain that once shared
this boundary was retired 2026-08-07) are out of scope.

## Primary Topics

- Availability and biometry type detection
- Policy evaluation
- Reason strings and Info.plist requirements
- Error handling
- Context lifecycle
- Keychain-biometric binding
- Fallback UX and passcode

## Used By

- knowledge/local-authentication/availability-and-biometry-type.md ([[knowledge/local-authentication/availability-and-biometry-type]])
- knowledge/local-authentication/policy-evaluation.md ([[knowledge/local-authentication/policy-evaluation]])
- knowledge/local-authentication/reason-strings-and-info-plist.md ([[knowledge/local-authentication/reason-strings-and-info-plist]])
- knowledge/local-authentication/error-handling.md ([[knowledge/local-authentication/error-handling]])
- knowledge/local-authentication/context-lifecycle.md ([[knowledge/local-authentication/context-lifecycle]])
- knowledge/local-authentication/keychain-biometric-binding.md ([[knowledge/local-authentication/keychain-biometric-binding]])
- knowledge/local-authentication/fallback-ux-and-passcode.md ([[knowledge/local-authentication/fallback-ux-and-passcode]])
