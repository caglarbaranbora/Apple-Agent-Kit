---
name: security
description: Route Keychain Services implementation tasks to the correct Knowledge Contracts -- item CRUD via SecItemAdd/SecItemCopyMatching/SecItemUpdate/SecItemDelete, accessibility levels, access groups and sharing, and storing structured/Codable data. Use when working with kSecClassGenericPassword, kSecClassInternetPassword, OSStatus, errSecSuccess, errSecItemNotFound, errSecDuplicateItem, kSecAttrAccessible, kSecAttrAccessGroup, Keychain Sharing, or kSecValueData. v1 is general (non-biometric-bound) Keychain item CRUD for generic/internet password items -- no SecAccessControl/biometric binding, no AutoFill/credential providers, no iCloud Keychain sync, no certificate/key/identity item classes. Triggers on SecItemAdd, SecItemCopyMatching, SecItemUpdate, SecItemDelete, kSecClassGenericPassword, kSecClassInternetPassword, kSecAttrAccessible, kSecAttrAccessGroup, Keychain access group, kSecValueData, Keychain, credential storage.
id: skill.security.foundations
title: Security — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Security
routes: [knowledge.security.keychain-item-crud, knowledge.security.keychain-accessibility-levels, knowledge.security.keychain-access-groups-and-sharing, knowledge.security.storing-structured-data-in-keychain]
related: [knowledge.local-authentication.keychain-biometric-binding]
last_updated: 2026-08-06
---

# Security — Foundations Skill

## Purpose

Route Keychain Services implementation tasks to the minimum required
Security Knowledge Contracts. v1 scope is general (non-biometric-bound)
Keychain item CRUD for `kSecClassGenericPassword` and
`kSecClassInternetPassword` items — accessibility levels, access-group
sharing, and storing structured/`Codable` data. No `SecAccessControl`
biometric binding, no AutoFill/credential-provider extensions, no iCloud
Keychain sync, no certificate/key/identity item classes.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/security/.

-   Calling `SecItemAdd`, `SecItemCopyMatching`, `SecItemUpdate`, `SecItemDelete`, constructing a query dictionary, or interpreting an `OSStatus`/`errSec*` result -> keychain-item-crud.md
-   Choosing a `kSecAttrAccessible*` value (`.WhenUnlocked`, `.AfterFirstUnlock`, `.WhenPasscodeSetThisDeviceOnly`, a `ThisDeviceOnly` variant, or the deprecated `.Always`/`.AlwaysThisDeviceOnly`) -> keychain-accessibility-levels.md
-   Setting `kSecAttrAccessGroup`, enabling Keychain Sharing, or sharing an item between apps/extensions from the same team -> keychain-access-groups-and-sharing.md
-   Encoding/decoding a `Codable` struct into or out of `kSecValueData`, or choosing between `JSONEncoder` and `NSKeyedArchiver` -> storing-structured-data-in-keychain.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/security/ — do not guess or fall back to general
knowledge. Biometric-bound access control (`SecAccessControlCreateWithFlags`,
`kSecAttrAccessControl`, `.biometryCurrentSet`/`.biometryAny`,
`kSecUseAuthenticationContext`) is owned by the `local-authentication`
Skill's `knowledge.local-authentication.keychain-biometric-binding`
contract, not this one — route there instead. Password AutoFill /
credential provider extensions, iCloud Keychain sync
(`kSecAttrSynchronizable`), and non-password Keychain item classes
(certificates, cryptographic keys, identities) are deferred, not yet
built — report that explicitly rather than answering from general
knowledge (see docs/architecture/domain-map.md).
