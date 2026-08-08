# Archive Process

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.xcode.archive-process
artifact_type: knowledge
title: Archive Process
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the correct archive workflow — Product > Archive and validating the resulting archive in the Organizer — before it is exported or uploaded.
domain: Xcode
tags:
  - xcode
  - archive
  - organizer
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev1bc569500.html
  - https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases
depends_on: []
related:
  - knowledge.xcode.schemes-and-targets
  - knowledge.xcode.export-options
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent produces a valid archive —
choosing the correct run destination, running Product → Archive, and
validating the result in the Organizer — before any export or upload is
attempted.

## Scope

### Included

-   Run-destination prerequisite for Archive to be enabled (a physical device or "Any iOS Device", not a Simulator)
-   Product → Archive and the Organizer window
-   "Validate App" in the Organizer before "Distribute App"
-   Retaining the `.xcarchive` (and its dSYMs) after upload

### Excluded

-   Export destination/method selection and IPA export — see `export-options`

## Rules

### Rule 1

Agents MUST select a physical-device or "Any iOS Device (arm64)" run
destination before archiving — Product → Archive is disabled when the
active scheme's run destination is a Simulator, since Simulator builds
aren't code-signed for distribution and don't produce a device-slice
binary.

### Rule 2

Agents MUST run "Validate App" in the Organizer before "Distribute App"
for a submission-bound archive — validation checks App Store Connect
requirements (Info.plist keys, icon completeness, entitlement/capability
consistency) locally and surfaces the same class of error App Store
Connect would otherwise reject on upload, but faster and without
consuming an upload attempt.

### Rule 3

Agents MUST NOT delete an archive from the Organizer immediately after a
successful upload — the `.xcarchive` is the only local artifact
containing the dSYMs needed to symbolicate crash reports for that exact
build; Xcode does not retain a separate copy once the archive is
removed.

### Rule 4

Agents SHOULD confirm the scheme's Archive action build configuration is
Release (see `schemes-and-targets`) before archiving for distribution —
an archive built under a Debug configuration is unoptimized and may
include debug-only code paths that shouldn't ship.

## Compliant Example

-   ✓ The run destination is set to "Any iOS Device (arm64)", Product → Archive completes, and "Validate App" is run in the Organizer and passes before "Distribute App" is used. (Rules 1, 2)

## Non-Compliant Example

-   ✗ The scheme's run destination is left on an iOS Simulator when Product → Archive is attempted. The menu item is disabled, and the agent misdiagnoses it as project corruption instead of a destination-selection issue. (Rule 1)

## Dependencies

None.

## References

-   [Apple — About Archives organizer](https://help.apple.com/xcode/mac/current/en.lproj/dev1bc569500.html)
-   [Apple Developer — Distributing your app for beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
