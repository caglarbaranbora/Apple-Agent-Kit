# Xcode

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.xcode
artifact_type: reference
title: Xcode
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's Xcode project-configuration documentation, scoped to this domain — build settings, schemes, signing, archiving and export, test plans and coverage, and project localization.
domain: Xcode
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/xcode
https://developer.apple.com/documentation/xcode/configuring-the-build-settings-of-a-target
https://developer.apple.com/documentation/xcode/build-settings-reference
https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project
https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project
https://developer.apple.com/documentation/xcode/build-system
https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases
https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback
https://developer.apple.com/documentation/xcode/determining-how-much-code-your-tests-cover
https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions
https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts
https://developer.apple.com/documentation/xcode/exporting-localizations
https://developer.apple.com/documentation/xcode/importing-localizations
https://developer.apple.com/documentation/xcode/editing-xliff-and-string-catalog-files
https://developer.apple.com/documentation/bundleresources/entitlements
https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles
https://help.apple.com/xcode/mac/current/en.lproj/dev745c5c974.html
https://help.apple.com/xcode/mac/current/en.lproj/dev60b6fbbc7.html
https://help.apple.com/xcode/mac/current/en.lproj/dev23aab79b4.html
https://help.apple.com/xcode/mac/current/en.lproj/dev1bf96f17e.html
https://help.apple.com/xcode/mac/current/en.lproj/devcac6ab5b3.html
https://help.apple.com/xcode/mac/current/en.lproj/dev88ff319e7.html
https://help.apple.com/xcode/mac/current/en.lproj/dev1bc569500.html
https://help.apple.com/xcode/mac/current/en.lproj/dev23ea8b877.html
https://help.apple.com/xcode/mac/current/en.lproj/devff5ececf8.html

## Purpose

Reference index for Apple's Xcode project-configuration documentation,
scoped to this domain: build configurations and `.xcconfig` files,
schemes and targets, automatic and manual code signing,
entitlements/capabilities, the archive-to-export workflow, test plans and
code coverage, and adding and round-tripping project localizations.

`xcodebuild` command-line usage, CI signing automation (fastlane,
`match`), and Swift Package Manager build configuration are **Excluded**
from this domain — a decision, not a backlog entry. macOS-specific
signing and notarization is **Excluded** on the kit's platform scope,
which is iOS. Xcode Cloud is **Deferred**: no decision has been taken on
it, and it is not covered by the CI exclusion above.

## Primary Topics

- Build configurations
- `.xcconfig` files
- Schemes and targets
- Automatic signing
- Manual signing & provisioning profiles
- Entitlements & capabilities
- Archive process
- Export options
- Test plans
- Code coverage
- Project localizations
- Localization export & import (`.xcloc`/XLIFF)

## Used By

- knowledge/xcode/build-configurations.md ([[knowledge/xcode/build-configurations]])
- knowledge/xcode/xcconfig-files.md ([[knowledge/xcode/xcconfig-files]])
- knowledge/xcode/schemes-and-targets.md ([[knowledge/xcode/schemes-and-targets]])
- knowledge/xcode/automatic-signing.md ([[knowledge/xcode/automatic-signing]])
- knowledge/xcode/manual-signing-provisioning-profiles.md ([[knowledge/xcode/manual-signing-provisioning-profiles]])
- knowledge/xcode/entitlements-capabilities.md ([[knowledge/xcode/entitlements-capabilities]])
- knowledge/xcode/archive-process.md ([[knowledge/xcode/archive-process]])
- knowledge/xcode/export-options.md ([[knowledge/xcode/export-options]])
- knowledge/xcode/test-plans.md ([[knowledge/xcode/test-plans]])
- knowledge/xcode/code-coverage.md ([[knowledge/xcode/code-coverage]])
- knowledge/xcode/project-localizations.md ([[knowledge/xcode/project-localizations]])
- knowledge/xcode/localization-export-import.md ([[knowledge/xcode/localization-export-import]])
- knowledge/localization/localized-resources-and-infoplist.md ([[knowledge/localization/localized-resources-and-infoplist]])
- knowledge/localization/locale-and-language-resolution.md ([[knowledge/localization/locale-and-language-resolution]])
