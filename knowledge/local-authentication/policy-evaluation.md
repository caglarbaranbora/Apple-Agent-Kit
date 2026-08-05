# Policy Evaluation

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.policy-evaluation
type: knowledge
title: Policy Evaluation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct choice and use of LAPolicy (deviceOwnerAuthenticationWithBiometrics vs. deviceOwnerAuthentication) when calling evaluatePolicy.
domain: Local Authentication
tags:
  - local-authentication
  - lapolicy
  - evaluatepolicy
references:
  - https://developer.apple.com/documentation/localauthentication/lapolicy
  - https://developer.apple.com/documentation/localauthentication/logging-a-user-into-your-app-with-face-id-or-touch-id
depends_on: []
related:
  - knowledge.local-authentication.availability-and-biometry-type
  - knowledge.local-authentication.fallback-ux-and-passcode
  - knowledge.local-authentication.context-lifecycle
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent chooses between
`LAContext`'s two device-owner-authentication policies and calls
`evaluatePolicy` correctly, so the resulting prompt matches the security
and UX intent of the calling feature.

## Scope

### Included

-   `.deviceOwnerAuthenticationWithBiometrics` — biometrics only, no automatic passcode fallback
-   `.deviceOwnerAuthentication` — biometrics with automatic fallback to device passcode
-   `evaluatePolicy(_:localizedReason:reply:)` async/completion-handler usage and the async `evaluatePolicy(_:localizedReason:)` overload
-   Choosing which policy matches the feature's actual security requirement

### Excluded

-   Availability/biometry-type pre-checks — see `availability-and-biometry-type`
-   `localizedReason` copy rules — see `reason-strings-and-info-plist`
-   The "Enter Passcode" fallback button specifically (`.deviceOwnerAuthentication`'s built-in behavior vs. a custom fallback) — see `fallback-ux-and-passcode`

## Rules

### Rule 1

Agents MUST use `.deviceOwnerAuthenticationWithBiometrics` only when the
feature genuinely requires biometrics specifically (e.g. re-confirming
identity for a sensitive in-app action where a device passcode is
considered insufficient) — for general app-unlock or convenience-login
use cases, `.deviceOwnerAuthentication` is correct, since it degrades
gracefully to the device passcode when biometrics are unavailable,
unenrolled, or fail repeatedly.

### Rule 2

Agents MUST NOT call `evaluatePolicy` again on the same `LAContext`
instance after a completed evaluation (success or failure) without first
creating a new `LAContext` — reusing a context for a second evaluation
produces undefined/inconsistent behavior; see `context-lifecycle` for the
correct one-context-per-attempt pattern.

### Rule 3

Agents MUST treat `evaluatePolicy`'s completion as asynchronous and
update UI state only after it returns — the call presents system UI and
returns control to the reply/continuation only once the user has
responded (or the system times out/cancels), so UI must not assume
synchronous completion or block the calling thread waiting on it outside
of `await`.

### Rule 4

Agents SHOULD prefer the `async` `evaluatePolicy(_:localizedReason:)`
overload over the completion-handler form in new Swift code — it
composes directly with structured concurrency (`Task`, cancellation) used
elsewhere in the app, without a manual closure-to-continuation bridge.

## Compliant Example

```swift
let context = LAContext()
let reason = "Unlock your account"

do {
    let success = try await context.evaluatePolicy(
        .deviceOwnerAuthentication,
        localizedReason: reason
    )
    if success {
        unlockApp()
    }
} catch {
    // Handle per error-handling.md
}
```
Uses `.deviceOwnerAuthentication` for a general app-unlock case (graceful passcode fallback), and the `async` overload. (Rules 1, 4)

## Non-Compliant Example

```swift
let context = LAContext()
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Unlock your account") { success, error in
    if success { unlockApp() }
}
// Later, reusing the same context:
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Confirm again") { success, error in
    // Undefined/inconsistent behavior — same context reused for a second evaluation.
}
```
Uses biometrics-only for a general unlock flow (users without enrolled biometrics get no fallback at all), and reuses the same `LAContext` for a second `evaluatePolicy` call. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — LAPolicy](https://developer.apple.com/documentation/localauthentication/lapolicy)
-   [Apple Developer — Logging a user into your app with Face ID or Touch ID](https://developer.apple.com/documentation/localauthentication/logging-a-user-into-your-app-with-face-id-or-touch-id)
