# Keychain Accessibility Levels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.security.keychain-accessibility-levels
type: knowledge
title: Keychain Accessibility Levels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the kSecAttrAccessible* family and how to choose the correct value -- WhenUnlocked, AfterFirstUnlock, WhenPasscodeSetThisDeviceOnly, the ThisDeviceOnly variants, and the deprecated Always/AlwaysThisDeviceOnly -- per use case.
domain: Security
tags:
  - security
  - keychain
  - ksecattraccessible
references:
  - https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility
  - https://developer.apple.com/documentation/security/ksecattraccessiblewhenunlocked
  - https://developer.apple.com/documentation/security/ksecattraccessibleafterfirstunlock
  - https://developer.apple.com/documentation/security/ksecattraccessiblewhenpasscodesetthisdeviceonly
  - https://developer.apple.com/documentation/security/ksecattraccessiblealways
depends_on: []
related:
  - knowledge.security.keychain-item-crud
  - knowledge.security.keychain-access-groups-and-sharing
  - knowledge.local-authentication.keychain-biometric-binding
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent selects the correct
`kSecAttrAccessible*` value for a Keychain item — balancing when it must
be readable (foreground only vs. also from background code) against how
far it should travel (backup migration vs. pinned to one device vs.
destroyed if the passcode is removed) — so stored secrets are neither
unnecessarily exposed nor unreachable when legitimately needed.

## Scope

### Included

-   `kSecAttrAccessibleWhenUnlocked` (the system default)
-   `kSecAttrAccessibleAfterFirstUnlock`
-   `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`
-   The `ThisDeviceOnly` variants of `WhenUnlocked` and `AfterFirstUnlock`
-   The deprecated `kSecAttrAccessibleAlways` / `kSecAttrAccessibleAlwaysThisDeviceOnly`
-   Choosing a level based on foreground-vs-background access need and backup/migration behavior

### Excluded

-   `SecAccessControlCreateWithFlags`, `kSecAttrAccessControl`, `.biometryCurrentSet`/`.biometryAny`, `kSecUseAuthenticationContext` — see `knowledge.local-authentication.keychain-biometric-binding`
-   `kSecAttrAccessGroup` and cross-app sharing — see `keychain-access-groups-and-sharing`
-   `SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate`/`SecItemDelete` call mechanics — see `keychain-item-crud`

## Rules

### Rule 1

Agents MUST use `kSecAttrAccessibleWhenUnlocked` (or its `ThisDeviceOnly`
variant) for items that only need to be read while the app is in the
foreground — Apple's documentation states this "is recommended for items
that need to be accessible only while the application is in the
foreground" and it is "the default value for keychain items added without
explicitly setting an accessibility constant."

### Rule 2

Agents MUST use `kSecAttrAccessibleAfterFirstUnlock` (or its
`ThisDeviceOnly` variant) when the item must be read by code that can run
while the device is locked, such as a background `URLSession` task or a
push-notification handler — Apple's documentation states this level "is
recommended for items that need to be accessed by background
applications," remaining accessible from the first unlock until the next
restart.

### Rule 3

Agents MUST use `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` for the
most sensitive items that must never be included in an iCloud/encrypted
backup restore and must be destroyed outright if device security is
weakened — per Apple's documentation, items with this attribute "never
migrate to a new device," can't be stored on a device without a
passcode, and are deleted if the device passcode is disabled.

### Rule 4

Agents MUST append the `ThisDeviceOnly` variant whenever an item must
never be restored onto a different physical device from an encrypted
backup. Per Apple's documentation, an item whose attribute ends in
`ThisDeviceOnly` "isn't migrated when restoring another device's backup
data" — non-`ThisDeviceOnly` variants migrate to a new device by default.

### Rule 5

Agents MUST NOT use `kSecAttrAccessibleAlways` or
`kSecAttrAccessibleAlwaysThisDeviceOnly` in new code — both are
deprecated since iOS 12.0/macOS 10.14, and Apple's documentation states
this level "is not recommended for application use" since the item
remains accessible regardless of the device's lock state.

## Compliant Example

```swift
// Session token: only needed while the app is running in the foreground.
let sessionQuery: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "sessionToken",
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    kSecValueData as String: tokenData
]

// Sync credential: must be readable by a background upload task.
let syncQuery: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "syncCredential",
    kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
    kSecValueData as String: credentialData
]
```
Matches the level to each item's actual access pattern: foreground-only session token uses `WhenUnlockedThisDeviceOnly` (Rule 1), background-readable sync credential uses `AfterFirstUnlockThisDeviceOnly` (Rule 2), and both pin to the device (Rule 4). (Rules 1, 2, 4)

## Non-Compliant Example

```swift
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "sessionToken",
    kSecAttrAccessible as String: kSecAttrAccessibleAlways,
    kSecValueData as String: tokenData
]
SecItemAdd(query as CFDictionary, nil)
```
Uses the deprecated, unconditionally-accessible `kSecAttrAccessibleAlways` for a foreground-only session token instead of `kSecAttrAccessibleWhenUnlocked`. (Rules 1, 5)

## Dependencies

None.

## References

-   [Apple Developer — Restricting keychain item accessibility](https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility)
-   [Apple Developer — kSecAttrAccessibleWhenUnlocked](https://developer.apple.com/documentation/security/ksecattraccessiblewhenunlocked)
-   [Apple Developer — kSecAttrAccessibleAfterFirstUnlock](https://developer.apple.com/documentation/security/ksecattraccessibleafterfirstunlock)
-   [Apple Developer — kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly](https://developer.apple.com/documentation/security/ksecattraccessiblewhenpasscodesetthisdeviceonly)
-   [Apple Developer — kSecAttrAccessibleAlways](https://developer.apple.com/documentation/security/ksecattraccessiblealways)
