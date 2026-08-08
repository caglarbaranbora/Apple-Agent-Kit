# Policy Evaluation

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.local-authentication.policy-evaluation
artifact_type: knowledge
title: Policy Evaluation
version: 1.0.0
status: Approved
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
  - knowledge.local-authentication.reason-strings-and-info-plist
  - knowledge.local-authentication.fallback-ux-and-passcode
  - knowledge.local-authentication.context-lifecycle
last_updated: 2026-08-08
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

Agents MUST create a new `LAContext` for each independent authentication
attempt rather than reusing one after a completed evaluation, unless
deliberately opting into reuse — `LAContext.touchIDAuthenticationAllowableReuseDuration`
defaults to `0` (no reuse: each `evaluatePolicy` call re-prompts), but
setting it to a nonzero value (up to
`LATouchIDAuthenticationMaximumAllowableReuseDuration`) makes a
subsequent `evaluatePolicy` call on that *same* context succeed
automatically, without re-prompting, if the prior success occurred within
that window. Reusing a context without understanding this property means
either an unnecessary re-prompt (property left at its default) or a
silent, unintended auto-success (property set nonzero without realizing
it applies) — see `context-lifecycle` for the correct
one-context-per-attempt pattern.

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
let context = LAContext() // touchIDAuthenticationAllowableReuseDuration left at its default (0).
let firstSuccess = try await context.evaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics,
    localizedReason: "Unlock your account"
)
guard firstSuccess else { return }
unlockApp()

// Later, after the first evaluation has already completed, this feature
// reuses the same context to confirm a second, separate sensitive action:
let secondSuccess = try await context.evaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics,
    localizedReason: "Confirm this payment"
)
```
Uses biometrics-only for a general unlock flow (users without enrolled biometrics get no fallback at all), and reuses the same `LAContext` for a second, unrelated `evaluatePolicy` call after the first has already completed, instead of creating a fresh context per attempt. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — LAPolicy](https://developer.apple.com/documentation/localauthentication/lapolicy)
-   [Apple Developer — Logging a user into your app with Face ID or Touch ID](https://developer.apple.com/documentation/localauthentication/logging-a-user-into-your-app-with-face-id-or-touch-id)
