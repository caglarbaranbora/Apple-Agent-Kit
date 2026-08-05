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
