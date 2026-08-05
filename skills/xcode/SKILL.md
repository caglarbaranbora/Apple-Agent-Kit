---
name: xcode
description: Route Xcode project-configuration implementation tasks to the correct Knowledge Contracts — build configurations, .xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archiving, and export. Use when configuring build settings, authoring an xcconfig file, editing a scheme, setting up code signing, adding a capability, or archiving/exporting an app in Xcode. v1 is Xcode GUI / project-file configuration only — no xcodebuild CLI, no CI signing automation (fastlane/match), no Swift Package Manager build configuration. Triggers on build configuration, Debug, Release, .xcconfig, Build Settings, scheme, target, Signing & Capabilities, automatic signing, manual signing, provisioning profile, certificate, entitlements, capability, Product > Archive, Organizer, ExportOptions, distribution method, Ad Hoc, Enterprise, App Store Connect distribution, IPA export.
id: skill.xcode.foundations
title: Xcode — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Xcode
routes: [knowledge.xcode.build-configurations, knowledge.xcode.xcconfig-files, knowledge.xcode.schemes-and-targets, knowledge.xcode.automatic-signing, knowledge.xcode.manual-signing-provisioning-profiles, knowledge.xcode.entitlements-capabilities, knowledge.xcode.archive-process, knowledge.xcode.export-options]
related: []
last_updated: 2026-08-01
---

# Xcode — Foundations Skill

## Purpose

Route Xcode project-configuration implementation tasks to the minimum
required Xcode Knowledge Contracts. v1 scope is Xcode GUI/project-file
configuration only — no `xcodebuild` CLI, no CI signing automation
(fastlane, `match`), no Swift Package Manager build configuration.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/xcode/.

-   Build configuration -> build-configurations.md, xcconfig-files.md, schemes-and-targets.md
-   Signing -> automatic-signing.md, manual-signing-provisioning-profiles.md, entitlements-capabilities.md
-   Archive & distribution -> archive-process.md, export-options.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/xcode/ — do not guess or fall back to general
knowledge. `xcodebuild` CLI usage, CI signing automation (fastlane,
`match`), and Swift Package Manager build configuration are deferred to
future scope, not yet built — report that explicitly rather than
answering from general knowledge (see docs/architecture/domain-map.md).
