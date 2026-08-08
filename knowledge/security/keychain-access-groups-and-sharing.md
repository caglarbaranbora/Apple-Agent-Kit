# Keychain Access Groups and Sharing

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.security.keychain-access-groups-and-sharing
artifact_type: knowledge
title: Keychain Access Groups and Sharing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines kSecAttrAccessGroup, the Keychain Sharing entitlement/capability, the team-ID prefix convention, and sharing Keychain items between apps/extensions signed by the same team.
domain: Security
tags:
  - security
  - keychain
  - ksecattraccessgroup
references:
  - https://developer.apple.com/documentation/security/ksecattraccessgroup
  - https://developer.apple.com/documentation/security/sharing-access-to-keychain-items-among-a-collection-of-apps
  - https://developer.apple.com/documentation/bundleresources/entitlements/keychain-access-groups
  - https://developer.apple.com/documentation/security/errsecmissingentitlement
depends_on: []
related:
  - knowledge.security.keychain-item-crud
  - knowledge.security.keychain-accessibility-levels
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent shares a Keychain item
between apps or app extensions signed by the same team: enabling the
Keychain Sharing capability, naming a team-ID-prefixed access group
consistently across targets, and setting `kSecAttrAccessGroup` on the
relevant queries — so a shared item is reachable by every intended
target and stays private otherwise.

## Scope

### Included

-   `kSecAttrAccessGroup` as a query/write attribute
-   The Keychain Sharing capability in Xcode and the resulting `keychain-access-groups` entitlement
-   The team-ID prefix convention for access-group strings
-   An app's ordered access-group list (entitlement strings, then app ID, then App Groups strings) and its default group
-   `errSecMissingEntitlement` when naming a group the app doesn't belong to

### Excluded

-   `SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate`/`SecItemDelete` call mechanics — see `keychain-item-crud`; `kSecAttrAccessible*` selection — see `keychain-accessibility-levels`
-   Non-Keychain data sharing via App Groups (e.g. shared `UserDefaults` suites) — out of scope beyond its role in the access-group list
-   `SecAccessControl`/biometric-bound access control — see `knowledge.local-authentication.keychain-biometric-binding`

## Rules

### Rule 1

Agents MUST enable the Keychain Sharing capability in Xcode for every
app or extension target that needs to read or write a shared item —
Apple's documentation for the resulting entitlement states: "To add this
entitlement to your app, enable the Keychain Sharing capability in
Xcode." `SecItemAdd`/`SecItemCopyMatching` only consult the access groups
the calling binary is actually entitled to.

### Rule 2

Agents MUST use a team-ID-prefixed string as the access-group name
(Xcode resolves an entitlement-editor value like
`com.example.SharedItems` to `<TEAMID>.com.example.SharedItems` at build
time) and use the identical string across every target that shares the
item. Per Apple's documentation, "Xcode automatically prefixes keychain
groups with your team ID" so groups stay specific to one development
team — apps signed by different teams can never share an access group.

### Rule 3

Agents MUST set `kSecAttrAccessGroup` explicitly in the `SecItemAdd`
attributes dictionary when writing an item intended for cross-app
sharing. Per Apple's documentation, omitting it applies the app's
default access group — the first entry in the concatenated list of (1)
the Keychain Access Groups Entitlement strings, (2) the app ID, then (3)
the App Groups Entitlement strings. An item added without this key lands
in the app's own private group, invisible to sibling apps.

### Rule 4

Agents MUST NOT set `kSecAttrAccessGroup` to a group string the calling
app doesn't belong to, including the empty string, which Apple's
documentation calls "always an invalid group." On `SecItemAdd` this
produces `errSecMissingEntitlement`; on `SecItemCopyMatching`,
`SecItemUpdate`, or `SecItemDelete` it instead produces
`errSecItemNotFound`, since per Apple's documentation the query then
simply fails to match anything.

### Rule 5

Agents SHOULD add `kSecAttrAccessGroup` to `SecItemCopyMatching`,
`SecItemUpdate`, and `SecItemDelete` queries whenever the app belongs to
more than one access group and the operation must target a specific one
— these functions otherwise "search all the access groups to which the
application belongs," which can silently match an unintended group.

## Compliant Example

```swift
// AppOne and AppTwo both have Keychain Sharing enabled with this group.
let sharedAccessGroup = "\(teamID).com.example.SharedItems"
let addQuery: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrAccount as String: username,
                                kSecAttrService as String: "shared-login",
                                kSecAttrAccessGroup as String: sharedAccessGroup,
                                kSecValueData as String: passwordData]
SecItemAdd(addQuery as CFDictionary, nil)

// From the sibling app, in the same access group:
let readQuery: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                 kSecAttrAccount as String: username,
                                 kSecAttrService as String: "shared-login",
                                 kSecAttrAccessGroup as String: sharedAccessGroup,
                                 kSecReturnData as String: true]
```
Both targets have Keychain Sharing enabled (Rule 1) with a team-ID-prefixed group name used identically on write and read (Rules 2, 3, 5). (Rules 1, 2, 3, 5)

## Non-Compliant Example

```swift
let addQuery: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrAccount as String: username,
                                kSecAttrService as String: "shared-login",
                                kSecValueData as String: passwordData]
SecItemAdd(addQuery as CFDictionary, nil)
// The sibling app's SecItemCopyMatching for the same account/service
// returns errSecItemNotFound -- the item landed in this app's private
// default group, not the intended shared group.
```
Omits `kSecAttrAccessGroup` on the add, so the item lands in the app's private default group instead of the intended shared group. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — kSecAttrAccessGroup](https://developer.apple.com/documentation/security/ksecattraccessgroup)
-   [Apple Developer — Sharing access to keychain items among a collection of apps](https://developer.apple.com/documentation/security/sharing-access-to-keychain-items-among-a-collection-of-apps)
-   [Apple Developer — Keychain Access Groups Entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/keychain-access-groups)
-   [Apple Developer — errSecMissingEntitlement](https://developer.apple.com/documentation/security/errsecmissingentitlement)
