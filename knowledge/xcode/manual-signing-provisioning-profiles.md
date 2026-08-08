# Manual Signing & Provisioning Profiles

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.xcode.manual-signing-provisioning-profiles
artifact_type: knowledge
title: Manual Signing & Provisioning Profiles
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct manual code signing — selecting an explicit certificate and provisioning profile, and matching profile type (Development/Ad Hoc/Enterprise/App Store Connect) to build purpose.
domain: Xcode
tags:
  - xcode
  - code-signing
  - provisioning-profiles
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev1bf96f17e.html
  - https://help.apple.com/xcode/mac/current/en.lproj/devcac6ab5b3.html
  - https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles
depends_on: []
related:
  - knowledge.xcode.automatic-signing
  - knowledge.xcode.entitlements-capabilities
  - knowledge.xcode.export-options
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent selects an explicit
certificate and provisioning profile for manual signing, and how to
match profile type to build purpose so a device install or distribution
export doesn't fail for a mismatch reason unrelated to the actual
signing identity.

## Scope

### Included

-   Certificate types (Development vs. Distribution)
-   Provisioning profile types: Development, Ad Hoc, Enterprise/In-House, App Store Connect
-   Turning off "Automatically manage signing" and selecting a specific profile
-   Common manual-signing failure modes: App ID mismatch, missing device UDID, expired certificate/profile

### Excluded

-   Automatic signing — see `automatic-signing`
-   Entitlements/capabilities that constrain which profile is valid — see `entitlements-capabilities`
-   Selecting a distribution method during export — see `export-options`

## Rules

### Rule 1

Agents MUST match the provisioning profile's type to the build's
purpose: Development for local device testing (must list the device's
UDID), Ad Hoc for testing on a fixed set of registered devices outside
the App Store, Enterprise/In-House for internal distribution under an
Apple Developer Enterprise Program account, and App Store Connect for
submission/TestFlight — using the wrong type either fails to install on
the target device or is rejected downstream, even when the certificate
itself is valid.

### Rule 2

Agents MUST verify a provisioning profile's App ID matches the target's
bundle identifier exactly, or via a matching wildcard App ID, before
assigning it — a profile issued for a different bundle identifier is not
selectable for manual signing, and Xcode reports that the profile
"doesn't match" the target.

### Rule 3

Agents MUST confirm a Development or Ad Hoc profile lists every device's
UDID the build needs to install on before assuming a signing-identity
problem — Apple regenerates the profile when a device is added to the
account's registered device list; a "this app cannot be installed
because its integrity could not be verified" or "device not eligible"
failure is frequently a stale device list, not a certificate issue.

### Rule 4

Agents MUST NOT reuse an expired certificate or provisioning profile —
both carry an expiration date (profiles: one year; Development and
Distribution certificates: typically one year), and Xcode/`codesign`
reject signing with an expired credential outright rather than merely
warning.

## Compliant Example

-   ✓ An Ad Hoc distribution profile is selected manually. Its App ID matches the target's bundle identifier, and every QA device's UDID is confirmed present in the profile before building. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ An App Store Connect profile is used to try installing a build directly on a physical device outside TestFlight. App Store Connect profiles don't authorize direct device installation, so the install fails, and the agent misdiagnoses it as a certificate problem instead of the wrong profile type. (Rule 1)

## Dependencies

None.

## References

-   [Apple — Manually sign an app](https://help.apple.com/xcode/mac/current/en.lproj/dev1bf96f17e.html)
-   [Apple — Manually manage distribution signing](https://help.apple.com/xcode/mac/current/en.lproj/devcac6ab5b3.html)
-   [Apple Developer — TN3125: Inside Code Signing: Provisioning Profiles](https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles)
