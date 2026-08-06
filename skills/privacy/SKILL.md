---
name: privacy
description: Route Privacy Manifest (PrivacyInfo.xcprivacy) implementation tasks to the correct Knowledge Contracts -- file structure/bundling, required-reason API declarations, collected data type declarations, and tracking domains/third-party SDK signatures. Use when writing or editing PrivacyInfo.xcprivacy, NSPrivacyCollectedDataTypes, NSPrivacyAccessedAPITypes, NSPrivacyAccessedAPITypeReasons, NSPrivacyTracking, NSPrivacyTrackingDomains, NSPrivacyCollectedDataType, NSPrivacyCollectedDataTypePurposes, or handling "required reason API" / "privacy manifest" / "third-party SDK signature" tasks. v1 is manifest file implementation/schema only -- no App Store Connect nutrition-label questionnaire, no permission-request UI design, no Info.plist usage strings, no Keychain/security. Triggers on PrivacyInfo.xcprivacy, privacy manifest, NSPrivacyTracking, NSPrivacyTrackingDomains, NSPrivacyCollectedDataTypes, NSPrivacyAccessedAPITypes, NSPrivacyAccessedAPITypeReasons, required reason API, App Privacy Configuration, third-party SDK signature.
id: skill.privacy.foundations
title: Privacy — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Privacy
routes: [knowledge.privacy.manifest-file-structure-and-scope, knowledge.privacy.required-reason-api-declarations, knowledge.privacy.collected-data-types-declaration, knowledge.privacy.tracking-domains-and-third-party-sdk-signatures]
related: [knowledge.human-interface-guidelines.privacy, knowledge.app-store-review-guidelines.privacy-manifest, knowledge.app-store-review-guidelines.privacy-nutrition-label]
last_updated: 2026-08-06
---

# Privacy — Foundations Skill

## Purpose

Route Privacy Manifest (`PrivacyInfo.xcprivacy`) implementation tasks
to the minimum required Privacy Knowledge Contracts. v1 scope is the
manifest file's structure and schema mechanics — how to write it
correctly the first time — not App Store review consequences, not
permission-UI design, not Info.plist strings, not credential storage.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/privacy/.

-   File placement, bundling per product type, or per-target/framework/xcframework manifest requirements -> manifest-file-structure-and-scope.md
-   `NSPrivacyAccessedAPITypes`/`NSPrivacyAccessedAPITypeReasons`, required-reason API categories or justification codes -> required-reason-api-declarations.md
-   `NSPrivacyCollectedDataTypes` entries, `NSPrivacyCollectedDataType`/`NSPrivacyCollectedDataTypePurposes` values -> collected-data-types-declaration.md
-   `NSPrivacyTracking`/`NSPrivacyTrackingDomains`, or third-party SDK manifest-and-signature coverage -> tracking-domains-and-third-party-sdk-signatures.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/privacy/ — do not guess or fall back to general
knowledge, especially for specific enum values or reason codes, since
Apple has changed this list before. The following are explicitly out
of scope for this Skill and owned elsewhere — route to or name the
owning Skill rather than answering from general knowledge:

-   App Store Connect "App Privacy" nutrition-label questionnaire -> `app-store-review-guidelines` Skill
-   Permission-request UI/consent-flow design, purpose-string wording -> `human-interface-guidelines` Skill
-   `Info.plist` runtime usage-string keys -> `app-store-review-guidelines` Skill
-   Keychain/credential storage -> future `security` domain (unbuilt; not yet routable)
