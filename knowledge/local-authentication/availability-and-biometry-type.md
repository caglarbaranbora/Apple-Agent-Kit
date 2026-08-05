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

Agents MUST check `biometryType` only after calling `canEvaluatePolicy`
at least once, not before — Apple's documentation states the property
"is set only after you call the `canEvaluatePolicy(_:error:)` method, and
is set no matter what the call returns," so it is populated whether that
call succeeds or fails; reading it beforehand (e.g. immediately after
`LAContext()` init) returns `.none` regardless of the device's actual
hardware. This is what makes it possible to read `biometryType` from the
*failure* path too (see Rule 4) — the hardware type is known even when
biometrics aren't enrolled.

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
    // biometryType is populated even on failure, so hardware type is
    // still knowable here -- e.g. to say "Face ID" instead of "biometrics"
    // when guiding the user to Settings for a biometryNotEnrolled error.
    if let laError = error as? LAError, laError.code == .biometryNotEnrolled {
        offerToOpenSettings(for: context.biometryType) // See error-handling.md.
    }
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
Checks availability before evaluating, reads `biometryType` only after `canEvaluatePolicy` has been called (success or failure), and distinguishes `biometryNotEnrolled` from other failures on the error path. (Rules 1, 2, 3, 4)

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
