# Context Lifecycle

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.context-lifecycle
artifact_type: knowledge
title: Context Lifecycle
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct LAContext lifecycle -- one context per authentication attempt, invalidate() after use, evaluatedPolicyDomainState for detecting enrollment changes, and why a context must not be persisted across app launches.
domain: Local Authentication
tags:
  - local-authentication
  - lacontext
  - lifecycle
references:
  - https://developer.apple.com/documentation/localauthentication/lacontext
depends_on: []
related:
  - knowledge.local-authentication.policy-evaluation
  - knowledge.local-authentication.keychain-biometric-binding
last_updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent manages an `LAContext`'s
lifetime so each authentication attempt uses a fresh, correctly-scoped
context, and so a context is never persisted or reused in a way that
produces stale or undefined behavior.

## Scope

### Included

-   One `LAContext` per authentication attempt
-   `invalidate()` and when to call it
-   `evaluatedPolicyDomainState` for detecting that biometric enrollment changed since the last successful evaluation
-   Why an `LAContext` must not be stored in a persisted model or reused across app launches

### Excluded

-   Which policy to evaluate — see `policy-evaluation`
-   Passing a context into a Keychain query — see `keychain-biometric-binding`

## Rules

### Rule 1

Agents MUST create a new `LAContext` for each independent authentication
attempt rather than storing one instance for reuse across multiple
unrelated evaluations — see `policy-evaluation` Rule 2 for the specific
prohibition on re-evaluating the same context; a context is scoped to a
single attempt's lifecycle, not a long-lived app-wide singleton.

### Rule 2

Agents MUST call `context.invalidate()` when an in-flight evaluation is
no longer needed (e.g. the user navigates away from the screen that
triggered it, or the feature is canceled programmatically) — an
un-invalidated context with a pending evaluation can leave the system
biometric UI in an inconsistent state relative to the app's own
navigation.

### Rule 3

Agents MUST NOT persist an `LAContext` instance (e.g. in `UserDefaults`,
a Core Data/SwiftData model, or any serialized state) or reuse one across
separate app launches — `LAContext` is not `Codable`, is not designed for
persistence, and its validity is tied to the process it was created in;
attempting to reuse one from a prior launch is a logic error, not merely
inefficient.

### Rule 4

Agents SHOULD compare a newly-created context's
`evaluatedPolicyDomainState` against a previously-stored value (captured
right after a prior successful evaluation) when the app needs to detect
that the user changed their enrolled biometrics (e.g. added a new
fingerprint) since the last login — a changed `evaluatedPolicyDomainState`
signals the enrollment set changed, which is the correct trigger to
invalidate a biometric-bound Keychain item and require re-authentication
via passcode (see `keychain-biometric-binding`).

## Compliant Example

```swift
func authenticateForThisAttempt() async -> Bool {
    let context = LAContext()
    do {
        return try await context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: "Unlock your account")
    } catch {
        return false
    }
    // `context` goes out of scope here -- a fresh one is created for the next attempt.
}
```
A new `LAContext` is created for this single attempt and not stored anywhere for reuse. (Rules 1, 3)

## Non-Compliant Example

```swift
class AuthManager {
    static let shared = AuthManager()
    let context = LAContext() // Created once, reused for every login attempt across the app's lifetime.

    func authenticate() async -> Bool {
        (try? await context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: "Unlock")) ?? false
    }
}
```
A single `LAContext` is held as a singleton and reused across every authentication attempt for the app's entire lifetime, violating the one-context-per-attempt rule. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
