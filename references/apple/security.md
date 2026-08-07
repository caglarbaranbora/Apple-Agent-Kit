# Security (Keychain Services)

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.security
artifact_type: reference
title: Security (Keychain Services)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's Security framework Keychain Services documentation, scoped to this domain's v1.
domain: Security (Keychain Services)
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/security/keychain-services
https://developer.apple.com/documentation/security/secitemadd(_:_:)
https://developer.apple.com/documentation/security/secitemcopymatching(_:_:)
https://developer.apple.com/documentation/security/secitemupdate(_:_:)
https://developer.apple.com/documentation/security/secitemdelete(_:)
https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility
https://developer.apple.com/documentation/security/sharing-access-to-keychain-items-among-a-collection-of-apps
https://developer.apple.com/documentation/bundleresources/entitlements/keychain-access-groups

## Purpose

Reference index for Apple's Security framework Keychain Services
documentation, scoped to this domain's v1: general (non-biometric-bound)
Keychain item CRUD via `SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate`/
`SecItemDelete` for generic and internet password items; the
`kSecAttrAccessible*` family of accessibility levels; Keychain access
groups and sharing (`kSecAttrAccessGroup`, the Keychain Sharing
capability, team-ID prefix convention); and storing structured (encoded)
data via `kSecValueData`.

Out of scope for v1: biometric-bound access control (`SecAccessControl`,
`.biometryCurrentSet`/`.biometryAny`, `kSecUseAuthenticationContext`) —
owned by `knowledge.local-authentication.keychain-biometric-binding`;
password AutoFill / credential provider extensions — deferred to a future
`authenticationservices` domain (Tier 2, unbuilt); iCloud Keychain sync
(`kSecAttrSynchronizable`) — deferred; Keychain item classes beyond
generic/internet password (certificates, cryptographic keys, identities)
— deferred.

## Primary Topics

- Keychain item CRUD and OSStatus result handling
- Keychain accessibility levels (`kSecAttrAccessible*`)
- Keychain access groups and sharing
- Storing structured data in the Keychain

## Used By

- knowledge/security/keychain-item-crud.md ([[knowledge/security/keychain-item-crud]])
- knowledge/security/keychain-accessibility-levels.md ([[knowledge/security/keychain-accessibility-levels]])
- knowledge/security/keychain-access-groups-and-sharing.md ([[knowledge/security/keychain-access-groups-and-sharing]])
- knowledge/security/storing-structured-data-in-keychain.md ([[knowledge/security/storing-structured-data-in-keychain]])
