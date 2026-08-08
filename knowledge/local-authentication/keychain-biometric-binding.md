# Keychain-Biometric Binding

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.local-authentication.keychain-biometric-binding
artifact_type: knowledge
title: Keychain-Biometric Binding
version: 1.0.0
status: Approved
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
  - knowledge.security.keychain-accessibility-levels
  - knowledge.local-authentication.policy-evaluation
  - knowledge.local-authentication.context-lifecycle
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent binds a Keychain item to
biometric authentication — the exact seam between LocalAuthentication and
Keychain — so a stored secret (e.g. a session token) is genuinely
protected by Face ID/Touch ID rather than merely stored alongside a
separate, disconnected authentication check. General Keychain item storage
for non-biometric-bound items is `security`'s, as the Excluded list says.

## Scope

### Included

-   `SecAccessControlCreateWithFlags` and the resulting `SecAccessControl` object
-   `kSecAttrAccessControl` as the Keychain query attribute carrying the access control
-   `.biometryCurrentSet` vs. `.biometryAny` access control flags and their re-enrollment behavior
-   Passing an evaluated `LAContext` into a Keychain query via `kSecUseAuthenticationContext`

### Excluded

-   General Keychain item storage/retrieval for non-biometric-bound items — owned by `security`
-   `LAContext` creation and policy evaluation themselves — see `policy-evaluation`, `context-lifecycle`

## Rules

### Rule 1

Agents MUST create the item's `SecAccessControl` with
`SecAccessControlCreateWithFlags`, passing a biometry-related flag
(`.biometryCurrentSet` or `.biometryAny`) — a Keychain item written
without a biometry flag in its access control is retrievable without any
biometric prompt at all, regardless of how the app's own UI flow looks.
Agents MUST pair that flag with
`kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`, the constant Apple
passes in its own example, and MUST NOT treat the accessibility constant
as free to choose: per Apple's documentation it "prevents items from being
stored if the device has no passcode", so a weaker one leaves a
biometry-bound item on a device whose passcode was later removed. That
constant's semantics are `knowledge.security.keychain-accessibility-levels`
Rule 3.

### Rule 2

Agents MUST choose `.biometryCurrentSet` when the item should become
inaccessible the moment the user's enrolled biometrics change (e.g. a new
fingerprint is added, or Face ID is reset) — the correct choice for
high-sensitivity items, since an enrollment change could mean a different
physical person now has biometric access to the device.

### Rule 3

Agents MUST choose `.biometryAny` only when the item should remain
accessible across a biometry re-enrollment (e.g. a convenience-login token
where surviving re-enrollment beats forcing a full re-login) — a deliberate
security/convenience tradeoff, not a default; `.biometryCurrentSet` is the
safer default absent a specific reason.

### Rule 4

Agents MUST attach the same `LAContext` used for the biometric prompt to
the Keychain query via `kSecUseAuthenticationContext` when reading a
biometric-protected item immediately after a successful `evaluatePolicy`
call — omitting it makes the Keychain query trigger its own separate,
redundant prompt instead of reusing the already-succeeded evaluation.

## Compliant Example

```swift
var accessControlError: Unmanaged<CFError>?
guard let accessControl = SecAccessControlCreateWithFlags(
    kCFAllocatorDefault,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
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
Pairs `.biometryCurrentSet` with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`, and reuses the already-evaluated context via `kSecUseAuthenticationContext` on read. (Rules 1, 2, 4)

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
