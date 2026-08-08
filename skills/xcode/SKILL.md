---
name: xcode
description: Route Xcode project-configuration implementation tasks to the correct Knowledge Contracts — build configurations, .xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archiving, export, test plans and code coverage, and project localization including .xcloc/XLIFF export-and-import. Use when configuring build settings, authoring an xcconfig file, editing a scheme, setting up code signing, adding a capability, archiving/exporting an app, creating or editing an .xctestplan, enabling code coverage, adding a language to a project, or exporting/importing localizations in Xcode. Scope is Xcode GUI / project-file configuration only — no xcodebuild CLI, no CI signing automation (fastlane/match), no Swift Package Manager build configuration. Triggers on build configuration, Debug configuration, Release configuration, .xcconfig, Build Settings, Xcode scheme, Xcode target, Signing & Capabilities, automatic signing, manual signing, provisioning profile, signing certificate, entitlements, Xcode capability, Product > Archive, Organizer, ExportOptions, distribution method, Ad Hoc, Enterprise, App Store Connect distribution, IPA export, test plan, .xctestplan, default test plan, Include Tags, Exclude Tags, test plan configuration, code coverage, Gather coverage for, Coverage report, Localizations, add a language, language ID, .lproj, Base localization, Export Localizations, Import Localizations, .xcloc, Xcode Localization Catalog, XLIFF, trans-unit, Use Compiler to Extract Swift Strings.
id: skill.xcode.foundations
title: Xcode — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: Xcode
routes: [knowledge.xcode.build-configurations, knowledge.xcode.xcconfig-files, knowledge.xcode.schemes-and-targets, knowledge.xcode.automatic-signing, knowledge.xcode.manual-signing-provisioning-profiles, knowledge.xcode.entitlements-capabilities, knowledge.xcode.archive-process, knowledge.xcode.export-options, knowledge.xcode.test-plans, knowledge.xcode.code-coverage, knowledge.xcode.project-localizations, knowledge.xcode.localization-export-import]
related: []
last_updated: 2026-08-08
---

# Xcode — Foundations Skill

## Purpose

Route Xcode project-configuration implementation tasks to the minimum
required Xcode Knowledge Contracts. Scope is Xcode GUI/project-file
configuration only — no `xcodebuild` CLI, no CI signing automation
(fastlane, `match`), no Swift Package Manager build configuration.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/xcode/.

-   Build configuration -> build-configurations.md, xcconfig-files.md, schemes-and-targets.md
-   Signing -> automatic-signing.md, manual-signing-provisioning-profiles.md, entitlements-capabilities.md
-   Archive & distribution -> archive-process.md, export-options.md
-   Test plans & coverage -> test-plans.md, code-coverage.md
-   Project localization -> project-localizations.md, localization-export-import.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/xcode/ — do not guess or fall back to general
knowledge.

-   `xcodebuild` CLI usage — Excluded
-   CI signing automation (fastlane, `match`) — Excluded
-   Swift Package Manager build configuration — Excluded
-   macOS-specific signing and notarization — Excluded; the kit's platform scope is iOS
-   Xcode Cloud — Deferred
-   Writing the tests a test plan selects — owned by `testing`
-   String Catalogs, the localizable-string APIs, plural variation, and `Locale` resolution — owned by `localization`
