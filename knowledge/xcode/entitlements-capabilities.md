# Entitlements & Capabilities

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.entitlements-capabilities
artifact_type: knowledge
title: Entitlements & Capabilities
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct addition of a capability via Signing & Capabilities and the resulting entitlements file, and how a capability constrains which provisioning profile is valid.
domain: Xcode
tags:
  - xcode
  - entitlements
  - capabilities
references:
  - https://developer.apple.com/documentation/bundleresources/entitlements
  - https://help.apple.com/xcode/mac/current/en.lproj/dev88ff319e7.html
depends_on: []
related:
  - knowledge.xcode.automatic-signing
  - knowledge.xcode.manual-signing-provisioning-profiles
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent adds a capability to a
target so the generated `.entitlements` file, the App ID's registered
capabilities, and the provisioning profile all stay consistent with each
other.

## Scope

### Included

-   Adding a capability via Signing & Capabilities (+ Capability)
-   The generated `.entitlements` file and its keys
-   Why adding or removing a capability can invalidate an existing manually-managed provisioning profile

### Excluded

-   Which capability a feature needs at a design/architecture level — implementation-only here
-   Sign in with Apple UX/flow — see the `authentication` domain

## Rules

### Rule 1

Agents MUST add a capability through Signing & Capabilities (the
+ Capability button), not by hand-editing the `.entitlements` file
directly, when automatic signing is enabled — Xcode also registers the
capability on the App ID in the Developer account and regenerates the
provisioning profile to match; a hand-edited entitlements file
requesting a capability the App ID isn't registered for fails code
signing.

### Rule 2

Agents MUST regenerate (or let Xcode regenerate) the provisioning
profile after adding or removing a capability under manual signing — a
profile issued before the capability was added does not grant it;
building with the stale profile fails with an entitlements-mismatch
signing error.

### Rule 3

Agents MUST keep the `.entitlements` file's keys consistent with what
the target actually uses — a leftover entitlement (e.g. Push
Notifications left in the file after removing the notification code)
still requires App ID registration and profile support, and is a
capability with no observable app behavior to justify it.

### Rule 4

Agents MUST use the exact entitlement key Apple defines for a capability
(e.g. `com.apple.developer.associated-domains`,
`com.apple.security.application-groups`) — a misspelled or incorrect key
is silently ignored by the OS at runtime rather than producing a build
error, so the capability appears configured but does nothing.

## Compliant Example

-   ✓ The App Groups capability is added via Signing & Capabilities. Xcode writes `com.apple.security.application-groups` to `<Target>.entitlements` and registers the group ID on the App ID automatically. (Rule 1)

## Non-Compliant Example

-   ✗ An entitlement key is typed by hand into the `.entitlements` file with a typo (`com.apple.security.aplication-groups`). The build signs successfully, but the app group silently doesn't work at runtime, since the OS doesn't recognize the misspelled key. (Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements)
-   [Apple — Add a capability to a target](https://help.apple.com/xcode/mac/current/en.lproj/dev88ff319e7.html)
