# Fallback UX and Passcode

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.local-authentication.fallback-ux-and-passcode
artifact_type: knowledge
title: Fallback UX and Passcode
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when to offer a passcode fallback via .deviceOwnerAuthentication vs. biometrics-only, and correct use of localizedFallbackTitle.
domain: Local Authentication
tags:
  - local-authentication
  - fallback
  - passcode
references:
  - https://developer.apple.com/documentation/localauthentication/lacontext
  - https://developer.apple.com/documentation/localauthentication/lapolicy
depends_on: []
related:
  - knowledge.local-authentication.policy-evaluation
  - knowledge.local-authentication.error-handling
  - knowledge.local-authentication.keychain-biometric-binding
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent decides whether a feature
should offer a device-passcode fallback, and how to configure the
fallback button's title, so the user is never left with a biometric
failure and zero path to recovery when a passcode fallback would have
been the correct UX.

## Scope

### Included

-   Deciding `.deviceOwnerAuthentication` (automatic passcode fallback) vs. `.deviceOwnerAuthenticationWithBiometrics` (no fallback, "Enter Password" fallback button omitted by using a custom localizedFallbackTitle)
-   `LAContext.localizedFallbackTitle` — customizing or hiding the fallback button
-   `LAContext.localizedCancelTitle` — customizing the cancel button

### Excluded

-   `LAError` codes once the user has already interacted with fallback/cancel — see `error-handling`
-   The Keychain implications of a biometrics-only vs. passcode-fallback design — see `keychain-biometric-binding`

## Rules

### Rule 1

Agents MUST use `.deviceOwnerAuthentication` (not
`.deviceOwnerAuthenticationWithBiometrics`) whenever the feature's
security intent is "confirm this is the device owner," not specifically
"confirm via biometrics" — this is the majority case (app unlock,
convenience login) and gives every user a working fallback even if
biometrics are disabled, unenrolled, or temporarily locked out.

### Rule 2

Agents MUST set `localizedFallbackTitle` to an empty string only when the
feature deliberately requires biometrics with no passcode fallback at all
(paired with `.deviceOwnerAuthenticationWithBiometrics`) — setting it to
an empty string hides the fallback button entirely; doing this on a
policy that isn't actually biometrics-only produces a dead end with no
visible path to a passcode.

### Rule 3

Agents SHOULD set a task-specific `localizedFallbackTitle` (e.g. "Use
Passcode") when the default system-provided fallback title doesn't fit
the feature's context, rather than leaving Apple's default in a flow
where "Enter Password" reads as unrelated to what the user is actually
unlocking.

### Rule 4

Agents MUST NOT assume `localizedCancelTitle` changes the cancel button's
behavior, only its label — canceling always produces `LAError.userCancel`
regardless of the button's displayed text; do not implement custom logic
that branches on the cancel button's title string.

## Compliant Example

```swift
let context = LAContext()
context.localizedFallbackTitle = "Use Passcode"

let success = try await context.evaluatePolicy(
    .deviceOwnerAuthentication,
    localizedReason: "Unlock your account"
)
```
Uses `.deviceOwnerAuthentication` so a fallback always exists, with a task-specific fallback title. (Rules 1, 3)

## Non-Compliant Example

```swift
let context = LAContext()
context.localizedFallbackTitle = ""

let success = try await context.evaluatePolicy(
    .deviceOwnerAuthentication,
    localizedReason: "Unlock your account"
)
```
Hides the fallback button (`localizedFallbackTitle = ""`) while still using `.deviceOwnerAuthentication` for a general unlock feature — a user who fails or lacks biometrics has no way to fall back to a passcode, even though the policy itself would otherwise support it. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
-   [Apple Developer — LAPolicy](https://developer.apple.com/documentation/localauthentication/lapolicy)
