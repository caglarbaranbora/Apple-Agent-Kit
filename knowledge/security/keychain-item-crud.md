# Keychain Item CRUD

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.security.keychain-item-crud
artifact_type: knowledge
title: Keychain Item CRUD
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of SecItemAdd/SecItemCopyMatching/SecItemUpdate/SecItemDelete for kSecClassGenericPassword and kSecClassInternetPassword items, query dictionary construction, and OSStatus result handling.
domain: Security
tags:
  - security
  - keychain
  - secitemadd
references:
  - https://developer.apple.com/documentation/security/secitemadd(_:_:)
  - https://developer.apple.com/documentation/security/secitemcopymatching(_:_:)
  - https://developer.apple.com/documentation/security/secitemupdate(_:_:)
  - https://developer.apple.com/documentation/security/secitemdelete(_:)
  - https://developer.apple.com/documentation/security/ksecclassgenericpassword
  - https://developer.apple.com/documentation/security/ksecclassinternetpassword
depends_on: []
related:
  - knowledge.security.keychain-accessibility-levels
  - knowledge.security.keychain-access-groups-and-sharing
  - knowledge.security.storing-structured-data-in-keychain
  - knowledge.local-authentication.keychain-biometric-binding
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent performs the four basic
Keychain item operations — `SecItemAdd`, `SecItemCopyMatching`,
`SecItemUpdate`, `SecItemDelete` — for `kSecClassGenericPassword` and
`kSecClassInternetPassword` items: query construction and interpreting
`OSStatus` against named `errSec*` constants rather than a bare zero
check, so lookups, writes, and deletes behave predictably.

## Scope

### Included

-   `SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate`/`SecItemDelete` call mechanics for `kSecClassGenericPassword`/`kSecClassInternetPassword`
-   Query construction: `kSecClass`, `kSecAttrAccount`, `kSecAttrService`/`kSecAttrServer`, `kSecValueData`
-   Composite-primary-key attributes that determine item identity and duplicate detection
-   `OSStatus` handling: `errSecSuccess`, `errSecItemNotFound`, `errSecDuplicateItem`, `errSecParam`
-   Off-main-thread call discipline

### Excluded

-   Choosing `kSecAttrAccessible*` — see `keychain-accessibility-levels`
-   `kSecAttrAccessGroup`/cross-app sharing — see `keychain-access-groups-and-sharing`
-   Encoding a `Codable` struct into `kSecValueData` — see `storing-structured-data-in-keychain`
-   `SecAccessControl`/`kSecAttrAccessControl`/`.biometryCurrentSet`/`.biometryAny`/`kSecUseAuthenticationContext` — see `knowledge.local-authentication.keychain-biometric-binding`
-   Certificate, key, and identity item classes — deferred per `references/apple/security.md`

## Rules

### Rule 1

Agents MUST call `SecItemAdd`, `SecItemCopyMatching`, `SecItemUpdate`,
and `SecItemDelete` from a background dispatch queue or an `async`
function, never on the main thread — each "blocks the calling thread, so
it can cause your app's UI to hang if called from the main thread."

### Rule 2

Agents MUST compare the returned `OSStatus` against named `errSec*`
constants, not a literal `0`. At minimum distinguish `errSecSuccess`,
`errSecItemNotFound` (no item matched on copy/update/delete), and
`errSecDuplicateItem` (add found an existing item with the same
composite primary key) — these are expected, handleable outcomes, not
generic failures to surface as opaque errors.

### Rule 3

Agents MUST set `kSecClass` to `kSecClassGenericPassword` with
`kSecAttrAccount` + `kSecAttrService`, or `kSecClassInternetPassword`
with `kSecAttrAccount` + `kSecAttrServer`, as the item's composite
primary key. Adding an item with the same values for all these
attributes as an existing item results in `errSecDuplicateItem`.
Omitting them makes lookups non-deterministic and duplicate detection
meaningless.

### Rule 4

Agents MUST NOT include item-return-result keys (`kSecReturnData`,
`kSecReturnAttributes`, `kSecReturnRef`, `kSecMatchLimit`) in the query
passed to `SecItemUpdate` or `SecItemDelete` — that query "can't contain
Item return result keys," since these calls only return a status; those
keys are meaningful only for `SecItemCopyMatching`.

### Rule 5

Agents MUST pass `SecItemUpdate`'s changed values in a separate, second
`attributesToUpdate` dictionary containing only the attributes to
change — never merged into the first `query` dictionary. `SecItemUpdate`
takes exactly these two distinct dictionaries; conflating them fails.

## Compliant Example

```swift
func updatePassword(_ newPassword: Data, forAccount account: String, service: String) async throws {
    try await Task.detached {
        let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                     kSecAttrAccount as String: account,
                                     kSecAttrService as String: service]
        let toUpdate: [String: Any] = [kSecValueData as String: newPassword]
        switch SecItemUpdate(query as CFDictionary, toUpdate as CFDictionary) {
        case errSecSuccess: return
        case errSecItemNotFound: throw KeychainError.noPassword
        case let status: throw KeychainError.unhandledError(status: status)
        }
    }.value
}
```
Runs off the main thread (Rule 1), separates `query` from `toUpdate` (Rule 5), and switches on named `errSec*` constants (Rule 2). (Rules 1, 2, 5)

## Non-Compliant Example

```swift
func updatePassword(_ newPassword: Data, forAccount account: String, service: String) -> Bool {
    let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                 kSecAttrAccount as String: account,
                                 kSecAttrService as String: service,
                                 kSecValueData as String: newPassword,
                                 kSecReturnData as String: true]
    return SecItemUpdate(query as CFDictionary, [:] as CFDictionary) == 0
}
```
Runs synchronously (Rule 1), merges the new value and a return-result key into `query` instead of a second dictionary (Rules 4, 5), and checks a bare `0` (Rule 2). (Rules 1, 2, 4, 5)

## Dependencies

None.

## References

-   [Apple Developer — SecItemAdd(_:_:)](https://developer.apple.com/documentation/security/secitemadd(_:_:))
-   [Apple Developer — SecItemCopyMatching(_:_:)](https://developer.apple.com/documentation/security/secitemcopymatching(_:_:))
-   [Apple Developer — SecItemUpdate(_:_:)](https://developer.apple.com/documentation/security/secitemupdate(_:_:))
-   [Apple Developer — SecItemDelete(_:)](https://developer.apple.com/documentation/security/secitemdelete(_:))
-   [Apple Developer — kSecClassGenericPassword](https://developer.apple.com/documentation/security/ksecclassgenericpassword)
-   [Apple Developer — kSecClassInternetPassword](https://developer.apple.com/documentation/security/ksecclassinternetpassword)
