# Automatic Signing

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.automatic-signing
type: knowledge
title: Automatic Signing
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of Xcode-managed (automatic) code signing — Development Team selection, Xcode-generated certificates/profiles, and device registration.
domain: Xcode
tags:
  - xcode
  - code-signing
  - automatic-signing
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev60b6fbbc7.html
  - https://help.apple.com/xcode/mac/current/en.lproj/dev23aab79b4.html
depends_on: []
related:
  - knowledge.xcode.manual-signing-provisioning-profiles
  - knowledge.xcode.entitlements-capabilities
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent configures Xcode-managed
(automatic) code signing so a target builds and installs on a device
without a manually-selected certificate or provisioning profile, and how
to correctly diagnose the signing-identity errors that are still
possible under automatic signing.

## Scope

### Included

-   Enabling "Automatically manage signing" and selecting a Development Team
-   How Xcode creates and renews development/distribution certificates and provisioning profiles
-   Device registration for a Debug build's run destination

### Excluded

-   Manual signing / explicit provisioning profile selection — see `manual-signing-provisioning-profiles`
-   Capabilities/entitlements and their effect on provisioning — see `entitlements-capabilities`

## Rules

### Rule 1

Agents MUST set a Development Team on every target that gets built or
archived (Signing & Capabilities → Team) — a target with no team
selected and automatic signing enabled fails to build with a
code-signing error, since Xcode has no Apple Developer account under
which to generate a certificate or profile.

### Rule 2

Agents MUST NOT assume automatic signing alone provisions a physical
test device — a new device must still be registered to the account
(Xcode registers it automatically the first time that device is chosen
as a run destination, or it can be added manually in the account's
device list); an unregistered device fails to install a Debug build
even with automatic signing correctly configured.

### Rule 3

Agents SHOULD leave "Automatically manage signing" enabled for
Debug/development builds unless the project has a specific need — e.g.
CI without an interactively-logged-in Apple ID, or an Ad Hoc/Enterprise
distribution profile with entitlements not available to automatic
signing — that requires manual signing (see
`manual-signing-provisioning-profiles`). Automatic signing is Apple's
recommended default and removes an entire class of
expired-certificate/profile-mismatch failures for day-to-day
development.

### Rule 4

Agents MUST check the target's actual Team setting before regenerating
certificates or changing the bundle identifier in response to a "no
signing certificate found" error — this error is frequently caused by
the wrong team being selected (e.g. after cloning a project set up under
a different Apple Developer account), not by a genuinely missing
certificate.

## Compliant Example

-   ✓ A target has "Automatically manage signing" checked and Team set to the project's actual Apple Developer account. Xcode generates a development certificate and provisioning profile the first time the app is run on a connected device. (Rules 1, 3)

## Non-Compliant Example

-   ✗ A project cloned from another developer's machine still has their Team selected in Signing & Capabilities. The build fails with "No signing certificate found," and the agent starts regenerating certificates in the Apple Developer account before checking whether the Team dropdown points at the wrong account. (Rule 4)

## Dependencies

None.

## References

-   [Apple — Signing & Capabilities workflow](https://help.apple.com/xcode/mac/current/en.lproj/dev60b6fbbc7.html)
-   [Apple — Assign a project to a team](https://help.apple.com/xcode/mac/current/en.lproj/dev23aab79b4.html)
