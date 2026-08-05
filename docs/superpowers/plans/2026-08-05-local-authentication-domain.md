# Local Authentication Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `local-authentication` domain (1 Reference, 7 Knowledge Contracts, 1 native Skill) covering Face ID/Touch ID/device-passcode authentication via Apple's LocalAuthentication framework — availability/biometry detection, policy evaluation, reason strings, error handling, context lifecycle, Keychain-biometric binding, and fallback UX — per `docs/superpowers/specs/2026-08-05-local-authentication-domain-design.md`, replacing the placeholder `local-authentication` row in `docs/architecture/domain-map.md`. This is the 11th of 12 Tier 1 domains; only `app-tracking-transparency` remains after this to close out Tier 1.

**Architecture:** Mirrors every prior domain exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. Subject matter is Swift API usage (`LAContext`, `LABiometryType`, `LAPolicy`, `LAError`, `SecAccessControl`), so Compliant/Non-Compliant Examples use fenced Swift code blocks, matching the style of `networking` and `swiftui` rather than the ✓/✗ workflow-description style used for `xcode` (a project-configuration domain, not an API domain). No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/local-authentication.md`

**Files:**
- Create: `references/apple/local-authentication.md`

- [ ] **Step 1: Create the file**

```markdown
# Local Authentication

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/localauthentication

## Purpose

Reference index for Apple's LocalAuthentication framework documentation,
scoped to this domain's v1: biometry availability and type detection,
policy evaluation, reason-string/Info.plist requirements, error handling,
context lifecycle, Keychain-biometric binding, and fallback UX.
macOS/watchOS-specific behavior, general Keychain storage APIs (owned by
the future `security` domain), and Sign in with Apple/passkeys (owned by
`authentication`) are out of scope.

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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/local-authentication.md --type reference`
Expected: `PASS: references/apple/local-authentication.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/local-authentication.md
git commit -m "docs: add local-authentication reference index"
```

---

## Task 2: Knowledge Contract — `availability-and-biometry-type`

**Files:**
- Create: `knowledge/local-authentication/availability-and-biometry-type.md`

- [ ] **Step 1: Create the file**

```markdown
# Availability and Biometry Type

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.availability-and-biometry-type
type: knowledge
title: Availability and Biometry Type
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of canEvaluatePolicy to check biometric availability before evaluating, and LABiometryType to detect which biometry (Face ID/Touch ID/none) is present.
domain: Local Authentication
tags:
  - local-authentication
  - biometrics
  - lacontext
references:
  - https://developer.apple.com/documentation/localauthentication/lacontext
  - https://developer.apple.com/documentation/localauthentication/labiometrytype
depends_on: []
related:
  - knowledge.local-authentication.policy-evaluation
  - knowledge.local-authentication.error-handling
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent checks whether biometric
authentication is available and which biometry type is present, before
ever calling `evaluatePolicy`, so the app can pick correct UI copy and
iconography and avoid calling an API that is guaranteed to fail.

## Scope

### Included

-   `LAContext.canEvaluatePolicy(_:error:)` as the required pre-check before `evaluatePolicy`
-   `LAContext.biometryType` (`.faceID`, `.touchID`, `.opticID`, `.none`) for icon/copy selection
-   Distinguishing "biometry not available on this device" from "available but not enrolled" via the `canEvaluatePolicy` out-error

### Excluded

-   Actually running the authentication prompt — see `policy-evaluation`
-   Interpreting `LAError` codes in depth — see `error-handling`

## Rules

### Rule 1

Agents MUST call `canEvaluatePolicy(_:error:)` before calling
`evaluatePolicy` and branch on its Boolean result — calling
`evaluatePolicy` directly on a device with no biometric hardware, or with
biometrics disabled, still returns a failure, but only after presenting
(or failing to present) a system UI the user never should have seen;
`canEvaluatePolicy` fails synchronously and cheaply, before any prompt.

### Rule 2

Agents MUST check `biometryType` only after a successful
`canEvaluatePolicy` call, not before — `biometryType` is populated as a
side effect of `canEvaluatePolicy` evaluating the policy; reading it
beforehand (e.g. immediately after `LAContext()` init) returns `.none`
regardless of the device's actual hardware.

### Rule 3

Agents MUST select prompt icon and copy based on the detected
`biometryType` (`.faceID` vs. `.touchID` vs. `.opticID`) rather than
hardcoding "Face ID" or a Face ID icon — an app hardcoded to Face ID copy
on a Touch ID device shows an incorrect, confusing prompt describing
hardware the device doesn't have.

### Rule 4

Agents MUST distinguish the `canEvaluatePolicy` out-error's code
`biometryNotAvailable` (no biometric hardware, or Restrictions disable
it) from `biometryNotEnrolled` (hardware present, but no Face/fingerprint
enrolled) — the correct recovery differs: `NotAvailable` means fall back
to passcode-only or another auth method entirely, `NotEnrolled` means
offer to guide the user to Settings to enroll.

## Compliant Example

```swift
let context = LAContext()
var error: NSError?

guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
    // Inspect `error` (see error-handling.md) and fall back accordingly.
    return
}

switch context.biometryType {
case .faceID:
    promptIcon = Image(systemName: "faceid")
case .touchID:
    promptIcon = Image(systemName: "touchid")
case .opticID:
    promptIcon = Image(systemName: "opticid")
default:
    promptIcon = nil
}
```
Checks availability before evaluating, and reads `biometryType` only after `canEvaluatePolicy` succeeds. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
let context = LAContext()
if context.biometryType == .faceID {
    // Show Face ID-branded UI, then call evaluatePolicy directly.
}
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, error in
    // ...
}
```
Reads `biometryType` before any `canEvaluatePolicy` call — it is `.none` on a freshly-initialized context regardless of actual hardware, so the Face ID branch never runs, and `evaluatePolicy` is called without ever confirming availability first. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
-   [Apple Developer — LABiometryType](https://developer.apple.com/documentation/localauthentication/labiometrytype)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/availability-and-biometry-type.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/availability-and-biometry-type.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/availability-and-biometry-type.md
git commit -m "feat: add availability-and-biometry-type knowledge contract"
```

---

## Task 3: Knowledge Contract — `policy-evaluation`

**Files:**
- Create: `knowledge/local-authentication/policy-evaluation.md`

- [ ] **Step 1: Create the file**

```markdown
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/policy-evaluation.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/policy-evaluation.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/policy-evaluation.md
git commit -m "feat: add policy-evaluation knowledge contract"
```

---

## Task 4: Knowledge Contract — `reason-strings-and-info-plist`

**Files:**
- Create: `knowledge/local-authentication/reason-strings-and-info-plist.md`

- [ ] **Step 1: Create the file**

```markdown
# Reason Strings and Info.plist

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.reason-strings-and-info-plist
type: knowledge
title: Reason Strings and Info.plist
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct localizedReason copy rules and the required NSFaceIDUsageDescription Info.plist key, without which Face ID calls fail at runtime.
domain: Local Authentication
tags:
  - local-authentication
  - info-plist
  - localizedreason
references:
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsfaceidusagedescription
  - https://developer.apple.com/documentation/localauthentication/lacontext
depends_on: []
related:
  - knowledge.local-authentication.policy-evaluation
  - knowledge.local-authentication.error-handling
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent writes the `localizedReason`
string passed to `evaluatePolicy` and configures the required
`NSFaceIDUsageDescription` Info.plist key, so a Face ID prompt has
task-specific copy and doesn't crash the app outright.

## Scope

### Included

-   `NSFaceIDUsageDescription` as a required Info.plist key for any app that calls Face ID APIs
-   `localizedReason` copy rules: task-specific, no restating "authenticate" or the app name
-   Where `localizedReason` appears in the system prompt relative to `NSFaceIDUsageDescription`

### Excluded

-   The fallback button's title string — see `fallback-ux-and-passcode`
-   `LAError` handling once evaluation has started — see `error-handling`

## Rules

### Rule 1

Agents MUST add an `NSFaceIDUsageDescription` key with a non-empty string
value to the app's Info.plist before shipping any code path that can call
`evaluatePolicy` on a Face ID-capable device — omitting this key does not
merely produce a degraded prompt; the app crashes when it attempts to use
Face ID, since iOS enforces the usage-description requirement the same
way it does for camera or location access.

### Rule 2

Agents MUST write `NSFaceIDUsageDescription`'s value as a specific,
task-grounded sentence (e.g. "Use Face ID to unlock your saved
passwords."), not a generic placeholder like "This app uses Face ID" —
App Review rejects usage-description strings that don't explain the
actual reason, the same standard applied to other permission-usage
strings (see `app-store-review-guidelines`).

### Rule 3

Agents MUST write `localizedReason` as a short, specific phrase
describing the action being authorized (e.g. "Unlock your account",
"Confirm this payment"), not a restatement of "Authenticate" or the app's
name — the system prompt template already supplies "[App Name] would
like to authenticate you"-style framing; a redundant or vague
`localizedReason` leaves the user unsure what they're approving.

### Rule 4

Agents MUST NOT include markup, trailing punctuation inconsistent with a
short phrase, or multi-sentence explanations in `localizedReason` — the
system prompt has limited layout space and truncates or wraps awkwardly
past roughly one short sentence.

## Compliant Example

```xml
<!-- Info.plist -->
<key>NSFaceIDUsageDescription</key>
<string>Use Face ID to quickly and securely unlock your saved passwords.</string>
```
```swift
try await context.evaluatePolicy(
    .deviceOwnerAuthentication,
    localizedReason: "Unlock your saved passwords"
)
```
Both strings are specific to the actual feature, and neither restates generic "authenticate" language. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
// Info.plist has no NSFaceIDUsageDescription entry at all.
try await context.evaluatePolicy(
    .deviceOwnerAuthentication,
    localizedReason: "Authenticate"
)
```
Missing `NSFaceIDUsageDescription` crashes the app on a Face ID device the first time this line runs; `localizedReason` merely restates "authenticate" without saying what's being authorized. (Rules 1, 3)

## Dependencies

None.

## References

-   [Apple Developer — NSFaceIDUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsfaceidusagedescription)
-   [Apple Developer — LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/reason-strings-and-info-plist.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/reason-strings-and-info-plist.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/reason-strings-and-info-plist.md
git commit -m "feat: add reason-strings-and-info-plist knowledge contract"
```

---

## Task 5: Knowledge Contract — `error-handling`

**Files:**
- Create: `knowledge/local-authentication/error-handling.md`

- [ ] **Step 1: Create the file**

```markdown
# Error Handling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.error-handling
type: knowledge
title: Error Handling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the required agent behavior for each LAError code returned by canEvaluatePolicy/evaluatePolicy, so failures are handled with the correct recovery instead of a generic failure message.
domain: Local Authentication
tags:
  - local-authentication
  - laerror
  - error-handling
references:
  - https://developer.apple.com/documentation/localauthentication/laerror
  - https://developer.apple.com/documentation/localauthentication/lacontext
depends_on: []
related:
  - knowledge.local-authentication.availability-and-biometry-type
  - knowledge.local-authentication.fallback-ux-and-passcode
updated: 2026-08-05
```

## Intent

This contract defines the required agent behavior for each `LAError` code
so a biometric authentication failure is handled with the specific,
correct recovery — offering Settings, offering a passcode fallback,
retrying, or simply reporting cancellation — instead of a single generic
"authentication failed" message for every case.

## Scope

### Included

-   `LAError` code table and the specific recovery action required per code
-   Distinguishing user-initiated cancellation from system/hardware failure
-   Errors returned from `canEvaluatePolicy`'s out-parameter vs. errors thrown/returned from `evaluatePolicy`

### Excluded

-   The passcode fallback button's UX/copy — see `fallback-ux-and-passcode`
-   Availability pre-checks — see `availability-and-biometry-type`

## Rules

### Rule 1

Agents MUST branch on the specific `LAError.Code` rather than treating
every non-success result as one generic failure — `.userCancel` and
`.userFallback` mean the user deliberately declined or chose an
alternative (no error UI needed beyond returning to the prior screen),
while `.biometryLockout` means the user is now locked out of biometrics
until they enter their device passcode once elsewhere, a state a generic
"try again" retry cannot resolve.

### Rule 2

Agents MUST handle `.biometryNotEnrolled` by offering to open Settings
(`UIApplication.openSettingsURLString`) so the user can enroll Face
ID/Touch ID, not by retrying the same `evaluatePolicy` call — retrying
without enrollment produces the identical error every time.

### Rule 3

Agents MUST handle `.biometryLockout` by prompting the user to
authenticate with their device passcode at the OS level (e.g. by
attempting `.deviceOwnerAuthentication`, which triggers the system
passcode entry) rather than silently blocking the feature — biometry
lockout after repeated failed attempts is resolved system-wide by a
successful device passcode entry, not by anything the app itself can
bypass.

### Rule 4

Agents MUST NOT surface `.userCancel` or `.appCancel` as an error message
to the user — both represent an intentional cancellation (the user
tapped Cancel, or the app itself canceled the request, e.g. by
backgrounding), and displaying an alert for a cancellation the user
caused is confusing, redundant UI.

## Compliant Example

```swift
do {
    let success = try await context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: reason)
    if success { onSuccess() }
} catch let error as LAError {
    switch error.code {
    case .userCancel, .appCancel:
        break // No error UI -- intentional cancellation.
    case .biometryNotEnrolled:
        offerToOpenSettings()
    case .biometryLockout:
        // .deviceOwnerAuthentication already offers passcode entry to clear the lockout.
        showMessage("Enter your device passcode to re-enable Face ID.")
    default:
        showMessage("Authentication failed. Please try again.")
    }
}
```
Branches on the specific `LAError.Code`, with `.userCancel`/`.appCancel` producing no user-facing error and `.biometryNotEnrolled` routed to Settings. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
do {
    let success = try await context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: reason)
    if success { onSuccess() }
} catch {
    showMessage("Authentication failed. Please try again.")
}
```
Shows the same generic error for every failure, including a user-initiated cancel and a lockout that "try again" cannot fix. (Rules 1, 4)

## Dependencies

None.

## References

-   [Apple Developer — LAError](https://developer.apple.com/documentation/localauthentication/laerror)
-   [Apple Developer — LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/error-handling.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/error-handling.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/error-handling.md
git commit -m "feat: add error-handling knowledge contract"
```

---

## Task 6: Knowledge Contract — `context-lifecycle`

**Files:**
- Create: `knowledge/local-authentication/context-lifecycle.md`

- [ ] **Step 1: Create the file**

```markdown
# Context Lifecycle

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.context-lifecycle
type: knowledge
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
updated: 2026-08-05
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/context-lifecycle.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/context-lifecycle.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/context-lifecycle.md
git commit -m "feat: add context-lifecycle knowledge contract"
```

---

## Task 7: Knowledge Contract — `keychain-biometric-binding`

**Files:**
- Create: `knowledge/local-authentication/keychain-biometric-binding.md`

- [ ] **Step 1: Create the file**

```markdown
# Keychain-Biometric Binding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.keychain-biometric-binding
type: knowledge
title: Keychain-Biometric Binding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct construction of a SecAccessControl for a biometric-protected Keychain item, the biometryCurrentSet vs. biometryAny tradeoff, and passing an evaluated LAContext into a Keychain query.
domain: Local Authentication
tags:
  - local-authentication
  - keychain
  - secaccesscontrol
references:
  - https://developer.apple.com/documentation/security/secaccesscontrolcreateflags
  - https://developer.apple.com/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id
  - https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility
depends_on: []
related:
  - knowledge.local-authentication.context-lifecycle
  - knowledge.local-authentication.error-handling
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent binds a Keychain item to
biometric authentication — the exact seam between LocalAuthentication and
Keychain — so a stored secret (e.g. a session token) is genuinely
protected by Face ID/Touch ID rather than merely stored alongside a
separate, disconnected authentication check. General Keychain item
storage (`SecItemAdd`/`SecItemCopyMatching` for non-biometric-bound
items) is out of scope for this domain; see the future `security` domain.

## Scope

### Included

-   `SecAccessControlCreateWithFlags` and the resulting `SecAccessControl` object
-   `kSecAttrAccessControl` as the Keychain query attribute carrying the access control
-   `.biometryCurrentSet` vs. `.biometryAny` access control flags and their re-enrollment behavior
-   Passing an evaluated `LAContext` into a Keychain query via `kSecUseAuthenticationContext`

### Excluded

-   General Keychain item storage/retrieval for non-biometric-bound items — future `security` domain
-   `LAContext` creation and policy evaluation themselves — see `policy-evaluation`, `context-lifecycle`

## Rules

### Rule 1

Agents MUST create the item's `SecAccessControl` with
`SecAccessControlCreateWithFlags`, passing a biometry-related flag
(`.biometryCurrentSet` or `.biometryAny`) combined with an accessibility
constant restricted to the device (e.g. `.whenUnlockedThisDeviceOnly`) —
a Keychain item written without a biometry flag in its access control is
retrievable without any biometric prompt at all, regardless of how the
app's own UI flow looks.

### Rule 2

Agents MUST choose `.biometryCurrentSet` when the item should become
inaccessible the moment the user's enrolled biometrics change (e.g. a new
fingerprint is added, or Face ID is reset) — this is the correct choice
for high-sensitivity items, since an enrollment change could mean a
different physical person now has biometric access to the device.

### Rule 3

Agents MUST choose `.biometryAny` only when the item should remain
accessible across a biometry re-enrollment (e.g. a convenience-login
token where surviving a fingerprint re-enrollment is preferred to forcing
a full re-login) — this is a deliberate security/convenience tradeoff,
not a default; `.biometryCurrentSet` is the safer default absent a
specific reason to choose otherwise.

### Rule 4

Agents MUST attach the same `LAContext` used for the biometric prompt to
the Keychain query via `kSecUseAuthenticationContext` when reading a
biometric-protected item immediately after a successful `evaluatePolicy`
call — omitting this attribute causes the Keychain query to trigger its
own separate, redundant biometric prompt instead of reusing the
already-succeeded evaluation.

## Compliant Example

```swift
var accessControlError: Unmanaged<CFError>?
guard let accessControl = SecAccessControlCreateWithFlags(
    kCFAllocatorDefault,
    kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    .biometryCurrentSet,
    &accessControlError
) else {
    // Handle accessControlError
    return
}

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "sessionToken",
    kSecValueData as String: tokenData,
    kSecAttrAccessControl as String: accessControl
]
SecItemAdd(query as CFDictionary, nil)

// Later, reading it back with the same context used for evaluatePolicy:
let readQuery: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "sessionToken",
    kSecUseAuthenticationContext as String: context,
    kSecReturnData as String: true
]
```
Uses `.biometryCurrentSet` for a sensitive token, and reuses the already-evaluated context via `kSecUseAuthenticationContext` on read. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "sessionToken",
    kSecValueData as String: tokenData,
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
]
SecItemAdd(query as CFDictionary, nil)
```
No `SecAccessControl`/`kSecAttrAccessControl` at all — the item is retrievable with no biometric prompt, even though the app's own screens gate access behind a Face ID check elsewhere. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — SecAccessControlCreateFlags](https://developer.apple.com/documentation/security/secaccesscontrolcreateflags)
-   [Apple Developer — Accessing keychain items with Face ID or Touch ID](https://developer.apple.com/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id)
-   [Apple Developer — Restricting keychain item accessibility](https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/keychain-biometric-binding.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/keychain-biometric-binding.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/keychain-biometric-binding.md
git commit -m "feat: add keychain-biometric-binding knowledge contract"
```

---

## Task 8: Knowledge Contract — `fallback-ux-and-passcode`

**Files:**
- Create: `knowledge/local-authentication/fallback-ux-and-passcode.md`

- [ ] **Step 1: Create the file**

```markdown
# Fallback UX and Passcode

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.local-authentication.fallback-ux-and-passcode
type: knowledge
title: Fallback UX and Passcode
version: 0.1.0
status: Draft
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
updated: 2026-08-05
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/local-authentication/fallback-ux-and-passcode.md --type knowledge`
Expected: `PASS: knowledge/local-authentication/fallback-ux-and-passcode.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/local-authentication/fallback-ux-and-passcode.md
git commit -m "feat: add fallback-ux-and-passcode knowledge contract"
```

---

## Task 9: Native Skill — `skills/local-authentication/SKILL.md`

**Files:**
- Create: `skills/local-authentication/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: local-authentication
description: Route Face ID/Touch ID/device-passcode implementation tasks to the correct Knowledge Contracts -- availability and biometry-type detection, policy evaluation, reason strings and Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, and fallback UX. Use when checking biometric availability, calling evaluatePolicy, writing an NSFaceIDUsageDescription string, handling an LAError, managing LAContext lifetime, binding a Keychain item to biometrics via SecAccessControl, or deciding on a passcode fallback. v1 is iOS/iPadOS LocalAuthentication framework API only -- no macOS/watchOS-specific behavior, no general Keychain storage (SecItemAdd/Copy/Update for non-biometric-bound items). Triggers on Face ID, Touch ID, LAContext, LABiometryType, canEvaluatePolicy, evaluatePolicy, deviceOwnerAuthentication, deviceOwnerAuthenticationWithBiometrics, LAPolicy, LAError, biometryNotEnrolled, biometryLockout, NSFaceIDUsageDescription, localizedReason, localizedFallbackTitle, SecAccessControl, biometryCurrentSet, biometryAny, biometric Keychain, Enter Passcode fallback, biometric authentication.
id: skill.local-authentication.foundations
title: Local Authentication — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Local Authentication
routes: [knowledge.local-authentication.availability-and-biometry-type, knowledge.local-authentication.policy-evaluation, knowledge.local-authentication.reason-strings-and-info-plist, knowledge.local-authentication.error-handling, knowledge.local-authentication.context-lifecycle, knowledge.local-authentication.keychain-biometric-binding, knowledge.local-authentication.fallback-ux-and-passcode]
related: []
last_updated: 2026-08-05
---

# Local Authentication — Foundations Skill

## Purpose

Route Face ID/Touch ID/device-passcode implementation tasks to the
minimum required Local Authentication Knowledge Contracts. v1 scope is
the iOS/iPadOS LocalAuthentication framework API plus the
Keychain-biometric binding seam — no macOS/watchOS-specific behavior, no
general Keychain storage.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/local-authentication/.

-   Checking availability or biometry type -> availability-and-biometry-type.md
-   Calling evaluatePolicy / choosing a policy -> policy-evaluation.md
-   Writing localizedReason or NSFaceIDUsageDescription -> reason-strings-and-info-plist.md
-   Handling an LAError -> error-handling.md
-   Managing LAContext lifetime or re-enrollment detection -> context-lifecycle.md
-   Binding a Keychain item to biometrics -> keychain-biometric-binding.md
-   Deciding on or configuring a passcode fallback -> fallback-ux-and-passcode.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/local-authentication/ — do not guess or fall back
to general knowledge. macOS/watchOS-specific LocalAuthentication
behavior and general Keychain storage (SecItemAdd/Copy/Update for
non-biometric-bound items) are deferred to future scope, not yet built —
report that explicitly rather than answering from general knowledge (see
docs/architecture/domain-map.md).
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/local-authentication/SKILL.md --type skill`
Expected: `PASS: skills/local-authentication/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/local-authentication/SKILL.md
git commit -m "feat: add local-authentication native skill"
```

---

## Task 10: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`xcode` row (the row containing `skills/xcode/SKILL.md`):

```markdown
| Face ID, Touch ID, LAContext, LABiometryType, canEvaluatePolicy, evaluatePolicy, deviceOwnerAuthentication, deviceOwnerAuthenticationWithBiometrics, LAPolicy, LAError, biometryNotEnrolled, biometryLockout, NSFaceIDUsageDescription, localizedReason, localizedFallbackTitle, SecAccessControl, biometryCurrentSet, biometryAny, biometric Keychain, Enter Passcode fallback, biometric authentication | skills/local-authentication/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `11` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui, accessibility, uikit, sf-symbols, networking, xcode, local-authentication)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add local-authentication to skills index"
```

---

## Task 11: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `local-authentication` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| Local Authentication | local-authentication | Face ID, Touch ID, biometric/passcode auth | Biometric and device-passcode authentication implementation |
```

Replace with:

```markdown
| Local Authentication | local-authentication | iOS/iPadOS LocalAuthentication framework API v1: availability and biometry-type detection, policy evaluation (biometrics-only vs. biometrics-or-passcode), reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding (SecAccessControl), fallback UX. No macOS/watchOS-specific behavior, no general Keychain storage. | Biometric and device-passcode authentication API implementation, including the Keychain-biometric binding seam |
```

- [ ] **Step 2: Add a new Cross-Domain Notes bullet**

Add this bullet at the end of the `## Cross-Domain Notes` list (after the
`networking`/`authentication` bullet, which is currently the last one):

```markdown
- `local-authentication` and `authentication` do not overlap — this is a clean handoff, not an angle-split, same pattern as `networking`/`authentication`. `knowledge.authentication.authentication`'s Excluded list omits biometrics entirely (its exclusions are StoreKit authentication, passkeys implementation, Sign in with Apple implementation, authentication networking, backend architecture); `authentication` owns sign-in terminology, entry points, and user-facing flow decisions, while `local-authentication` owns the LocalAuthentication framework API surface reached once the decision to use biometrics has already been made. No content is duplicated between the two domains.
```

- [ ] **Step 3: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt), `xcode` (Tier 1 — Xcode GUI/project-file v1: build configurations & xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; xcodebuild CLI, CI signing automation, and Swift Package Manager build configuration remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt), `xcode` (Tier 1 — Xcode GUI/project-file v1: build configurations & xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; xcodebuild CLI, CI signing automation, and Swift Package Manager build configuration remain unbuilt), `local-authentication` (Tier 1 — iOS/iPadOS LocalAuthentication framework API v1: availability/biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; macOS/watchOS-specific behavior and general Keychain storage remain unbuilt).
```

- [ ] **Step 4: Validate manually**

Run: `grep -c "local-authentication" docs/architecture/domain-map.md`
Expected: a number greater than 3 (the file already mentions
"local-authentication" at least twice before this task — the Tier 1
placeholder row and possibly a mention elsewhere — the updated row, new
Cross-Domain Notes bullet, and Completed line push the count higher)

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope local-authentication v1, add cross-domain note"
```

---

## Task 12: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `xcode` bullet, immediately
before the `Full routing tables:` line):

```markdown
- **`xcode`** — Routes Xcode project-configuration implementation tasks (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options) to Xcode Knowledge Contracts.
  Example: `"my archive won't export, wrong provisioning profile"` → `manual-signing-provisioning-profiles.md`
  Example: `"Product > Archive is greyed out"` → `archive-process.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`xcode`** — Routes Xcode project-configuration implementation tasks (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options) to Xcode Knowledge Contracts.
  Example: `"my archive won't export, wrong provisioning profile"` → `manual-signing-provisioning-profiles.md`
  Example: `"Product > Archive is greyed out"` → `archive-process.md`

- **`local-authentication`** — Routes Face ID/Touch ID/device-passcode implementation tasks (availability and biometry-type detection, policy evaluation, reason strings and Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX) to Local Authentication Knowledge Contracts.
  Example: `"Face ID prompt shows the wrong icon"` → `availability-and-biometry-type.md`
  Example: `"user is locked out of Face ID after too many failed attempts"` → `error-handling.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Update the What's New section (3-item cap)**

Find this exact block (the current `## What's New` section — 3 dated
lines plus the CHANGELOG.md link):

```markdown
## What's New

- 2026-08-01 — Added `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `networking` Skill (URL request construction, async data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; async/await URLSession v1) — 8 Knowledge Contracts. Fills the "Authentication networking" gap authentication.md explicitly excludes, and replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `sf-symbols` Skill (symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contracts. Resolves the human-interface-guidelines sf-symbols forward-reference and replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

Replace with (new line added at top, oldest of the 3 — the `sf-symbols`
line — drops off since the cap stays at 3 dated lines):

```markdown
## What's New

- 2026-08-05 — Added `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication` (which excludes biometrics entirely), replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `networking` Skill (URL request construction, async data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; async/await URLSession v1) — 8 Knowledge Contracts. Fills the "Authentication networking" gap authentication.md explicitly excludes, and replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "local-authentication" README.md`
Expected: a number greater than 0 (the new Skills bullet and What's New
line are the first mentions of "local-authentication" in this file)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add local-authentication to README Skills + What's New"
```

---

## Task 13: Update `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add a new Unreleased entry**

Find this exact block (the current `## [Unreleased]` section):

```markdown
## [Unreleased]
### Added
- `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
```

Replace with:

```markdown
## [Unreleased]
### Added
- `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication`, replaces the prior placeholder scope in domain-map.md.
- `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "local-authentication" CHANGELOG.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add local-authentication changelog entry"
```

---

## Task 14: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/local-authentication.md --type reference
python3 scripts/validate_artifact.py skills/local-authentication/SKILL.md --type skill
for f in knowledge/local-authentication/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
```
Expected: `PASS` for all 9 files.

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 4: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 13 prior tasks committed).

- [ ] **Step 5: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire `local-authentication`
domain (all 9 new files plus the 4 modified docs) to check cross-file
consistency: every `related:`/`depends_on:` KC id resolves to a real
file, the Skill's `routes:` list matches exactly the 7 KC ids, the
Reference's "Used By" list matches exactly the 7 KC files, layer order
(References → Knowledge → Skills) is respected. The review must
specifically check for v1-scope violations that a per-task review could
miss (this class of bug slipped through per-task review in the `xcode`
build and was only caught by the final holistic pass):

-   No content anywhere describing macOS/watchOS-specific
    LocalAuthentication behavior
-   No content anywhere describing general Keychain storage
    (`SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate` for
    non-biometric-bound items) beyond the biometric-binding seam this
    domain owns
-   No KC restates `authentication`'s sign-in UX/terminology content
-   Every cited Apple Developer URL is live (spot-check a sample with
    `curl -s -o /dev/null -w "%{http_code}"`)

Report findings; fix any issues found and re-commit before considering
the domain complete.

---

## Self-Review Notes

-   **Spec coverage:** All 7 KC topics from the design spec's "Knowledge
    Contracts (7)" section have a task (Tasks 2–8), matching titles and
    scope exactly. The spec's Reference section is Task 1. The spec's
    Skill section (trigger keywords, routing clusters) is Task 9. The
    spec's Cross-Domain Boundary section is reflected in Task 11 Step 2's
    new Cross-Domain Notes bullet. The spec's Documentation Updates
    section is covered by Tasks 10–13.
-   **Placeholder scan:** No TBD/TODO; every Rule, Example, and Reference
    URL is concrete and was live-verified via `curl` during planning (see
    Task 14 Step 5 for the re-check to run post-hoc).
-   **Type/id consistency:** Every KC `id`
    (`knowledge.local-authentication.<slug>`) referenced in Task 9's
    `routes:` list and Task 1's "Used By" list matches the `id` defined
    in that KC's own Task 2–8 Metadata block. Every `related:`
    cross-reference (e.g. `knowledge.local-authentication.error-handling`
    listed in `availability-and-biometry-type`'s `related:`) points at an
    id defined in this same plan.
