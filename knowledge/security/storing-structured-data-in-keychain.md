# Storing Structured Data in the Keychain

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.security.storing-structured-data-in-keychain
artifact_type: knowledge
title: Storing Structured Data in the Keychain
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines encoding a Codable struct via JSONEncoder into Data for kSecValueData and decoding it back on read, the NSKeyedArchiver alternative, and why Codable/JSON is generally preferred for new code.
domain: Security
tags:
  - security
  - keychain
  - codable
references:
  - https://developer.apple.com/documentation/security/ksecvaluedata
  - https://developer.apple.com/documentation/foundation/jsonencoder/encode(_:)
  - https://developer.apple.com/documentation/foundation/jsondecoder/decode(_:from:)
  - https://developer.apple.com/documentation/foundation/nskeyedarchiver
depends_on: []
related:
  - knowledge.security.keychain-item-crud
  - knowledge.security.keychain-accessibility-levels
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent stores a structured Swift
value (e.g. a struct with multiple fields, not just a single password
string) in a Keychain item's `kSecValueData`: encoding it to `Data` with
`JSONEncoder` before the write, and decoding it back with the matching
`Decodable` type after the read — so round-tripping structured data
through the Keychain is type-safe and doesn't depend on a legacy
Objective-C archiving mechanism unless one is already in use.

## Scope

### Included

-   Encoding a `Codable`/`Encodable` struct with `JSONEncoder().encode(_:)` into `Data` for `kSecValueData`
-   Decoding the `Data` returned via `kSecReturnData` with `JSONDecoder().decode(_:from:)` using the matching `Decodable` type
-   `NSKeyedArchiver`/`NSKeyedUnarchiver` as the legacy alternative and when it's still the right choice
-   Why `Codable`/JSON is generally preferred over `NSKeyedArchiver` for new code

### Excluded

-   `SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate`/`SecItemDelete` call mechanics — see `keychain-item-crud`
-   `kSecAttrAccessible*` and `kSecAttrAccessGroup` selection — see `keychain-accessibility-levels`, `keychain-access-groups-and-sharing`
-   `SecAccessControl`/biometric-bound access control — see `knowledge.local-authentication.keychain-biometric-binding`

## Rules

### Rule 1

Agents MUST encode a structured value with `JSONEncoder().encode(_:)`
into a `Data` instance before assigning it to `kSecValueData` — Apple's
documentation states this value's type is `CFData`, and
`JSONEncoder.encode(_:)` is declared `func encode<T>(_ value: T) throws
-> Data where T : Encodable`. Assigning a struct or dictionary literal
directly does not satisfy this type requirement.

### Rule 2

Agents MUST decode the `Data` returned under `kSecReturnData` with
`JSONDecoder().decode(_:from:)` using the exact same `Decodable` type
used to encode it. Per Apple's documentation, invalid JSON throws
`DecodingError.dataCorrupted(_:)` — a type mismatch between encode and
decode is a runtime decoding failure, not a compile-time error, since
the Keychain itself stores only opaque bytes.

### Rule 3

Agents SHOULD prefer `Codable` with `JSONEncoder`/`JSONDecoder` over
`NSKeyedArchiver`/`NSKeyedUnarchiver` for new code storing structured
data in `kSecValueData`. Per Apple's documentation, `NSKeyedArchiver`
"provides a way to encode objects (and scalar values)" and requires the
encoded types to participate in the `NSCoding`/`NSSecureCoding`
object-archiving model; plain Swift structs and enums conform to
`Codable` directly with no such requirement. `NSKeyedArchiver` remains
correct only when interoperating with existing archived data or
Objective-C class hierarchies that already use it.

### Rule 4

Agents MUST NOT treat `kSecValueData`'s own at-rest encryption as a
substitute for setting an appropriate `kSecAttrAccessible*` value.
Encoding format and accessibility are orthogonal: which process may
query the item at all is governed by `kSecAttrAccessible*` and
`kSecAttrAccessGroup` (see the sibling `keychain-accessibility-levels`
and `keychain-access-groups-and-sharing` contracts), not by how the
payload inside `kSecValueData` was serialized.

## Compliant Example

```swift
struct StoredCredential: Codable {
    let username: String
    let refreshToken: String
}

func save(_ credential: StoredCredential, account: String) throws {
    let data = try JSONEncoder().encode(credential)
    let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                 kSecAttrAccount as String: account,
                                 kSecValueData as String: data]
    SecItemAdd(query as CFDictionary, nil)
}

func loadCredential(account: String) throws -> StoredCredential? {
    let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                 kSecAttrAccount as String: account,
                                 kSecReturnData as String: true]
    var result: CFTypeRef?
    guard SecItemCopyMatching(query as CFDictionary, &result) == errSecSuccess,
          let data = result as? Data else { return nil }
    return try JSONDecoder().decode(StoredCredential.self, from: data)
}
```
Encodes `StoredCredential` to `Data` with `JSONEncoder` before the write (Rule 1), and decodes it back with `JSONDecoder` using the same type (Rule 2). (Rules 1, 2)

## Non-Compliant Example

```swift
func save(_ credential: StoredCredential, account: String) {
    let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                 kSecAttrAccount as String: account,
                                 kSecValueData as String: credential] // not Data
    SecItemAdd(query as CFDictionary, nil)
}
```
Assigns the `Codable` struct directly to `kSecValueData` instead of first encoding it with `JSONEncoder` into `Data`. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — kSecValueData](https://developer.apple.com/documentation/security/ksecvaluedata)
-   [Apple Developer — JSONEncoder.encode(_:)](https://developer.apple.com/documentation/foundation/jsonencoder/encode(_:))
-   [Apple Developer — JSONDecoder.decode(_:from:)](https://developer.apple.com/documentation/foundation/jsondecoder/decode(_:from:))
-   [Apple Developer — NSKeyedArchiver](https://developer.apple.com/documentation/foundation/nskeyedarchiver)
