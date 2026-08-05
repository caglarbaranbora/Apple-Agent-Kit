# Export Options

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.export-options
type: knowledge
title: Export Options
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the Organizer's Distribute App export flow — distribution-method selection and signing-option choice — when exporting a signed IPA from an archive.
domain: Xcode
tags:
  - xcode
  - export
  - distribution
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev23ea8b877.html
  - https://help.apple.com/xcode/mac/current/en.lproj/devff5ececf8.html
depends_on: []
related:
  - knowledge.xcode.archive-process
  - knowledge.xcode.manual-signing-provisioning-profiles
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent exports a signed `.ipa`
from an archive via the Organizer's Distribute App flow — choosing the
distribution method and signing option that match the archive's intended
destination.

## Scope

### Included

-   Organizer "Distribute App" flow
-   Distribution-method selection: App Store Connect, Ad Hoc, Enterprise, Development
-   Automatic vs. manual re-signing during export
-   Re-validating an archive per distribution method

### Excluded

-   `xcodebuild -exportArchive` / CLI `ExportOptions.plist` authoring for scripted export — CLI is out of v1 scope, see `docs/architecture/domain-map.md`
-   Archiving itself — see `archive-process`

## Rules

### Rule 1

Agents MUST choose the distribution method matching the archive's
intended destination: App Store Connect for submission/TestFlight, Ad
Hoc for a fixed set of registered devices, Enterprise for in-house
distribution under an Enterprise Program account, Development for
installing directly on a connected device without going through
TestFlight — choosing the wrong method produces a correctly-signed but
unusable-for-the-intended-purpose `.ipa` (e.g. an Ad Hoc export won't
install on a device that isn't in the profile).

### Rule 2

Agents MUST select automatic signing during export whenever the archive
itself was built with automatic signing, unless a specific manual
profile is required for that distribution method — mixing an
automatic-signed archive with a manual re-sign step during export
requires a provisioning profile matching the archive's entitlements
exactly, which is easy to get wrong (see
`manual-signing-provisioning-profiles`).

### Rule 3

Agents MUST re-run "Validate App" if the distribution method or signing
option changes between export attempts — a validation pass for one
distribution method (e.g. Development) does not guarantee the same
archive validates for another (e.g. App Store Connect), since
entitlement and capability requirements differ per method.

### Rule 4

Agents SHOULD keep an exported `.ipa` together with its export report
when the export is handed off (e.g. to a QA team distributing via Ad
Hoc) — the export report records exactly which signing identity and
profile were used, which is otherwise hard to reconstruct from the
`.ipa` alone.

## Compliant Example

-   ✓ An archive is exported via Organizer → Distribute App → App Store Connect, with automatic signing selected to match the archive, and "Validate App" is re-run for that specific method before upload. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ An archive intended for App Store submission is exported using the Ad Hoc method, and the resulting `.ipa` is uploaded via Transporter. App Store Connect rejects the upload, since an Ad Hoc-signed `.ipa` isn't signed for App Store distribution. (Rule 1)

## Dependencies

None.

## References

-   [Apple — Export an iOS, tvOS, or watchOS app](https://help.apple.com/xcode/mac/current/en.lproj/dev23ea8b877.html)
-   [Apple — Distribution signing options](https://help.apple.com/xcode/mac/current/en.lproj/devff5ececf8.html)
