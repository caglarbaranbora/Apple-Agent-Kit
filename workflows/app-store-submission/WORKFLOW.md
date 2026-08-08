# App Store Submission

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: workflow.app-store-submission
artifact_type: workflow
title: App Store Submission
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Gates an app through review-guideline compliance and privacy declaration before it is signed, archived, and exported.
skills:
  - skill.app-store-review-guidelines.submission
  - skill.privacy.foundations
  - skill.xcode.foundations
related: []
last_updated: 2026-08-08
```

## Purpose

Take an app from "feature complete" to "uploaded to App Store Connect" without a
rejection that was predictable before the build was made.

## Scope

### Included

- App Review Guidelines compliance for the submitted build
- `PrivacyInfo.xcprivacy` declaration and required-reason API accounting
- Signing, entitlements, archive, and export

### Excluded

- Building the features themselves — every other domain
- App Store Connect metadata, pricing, and phased release — outside this repository
- TestFlight distribution mechanics beyond export

## Trigger Conditions

The task asks to submit, ship, release, or archive an app for the App Store, or to
diagnose a rejection.

Triggers: App Store submission, ship the app, archive, App Review rejection, privacy
manifest, export IPA.

## Skill Sequence

Ordered cheapest-check-first, so a failure surfaces before an archive is produced.

1. `skill.app-store-review-guidelines.submission` — compliance of what the app does.
   The most expensive failure to discover late, and the only one that can require a
   feature change rather than a build setting.
2. `skill.privacy.foundations` — `PrivacyInfo.xcprivacy`, tracking domains, collected
   data types, and required-reason APIs, including those of third-party SDKs. This
   must be correct **before** the archive, because the manifest ships inside the
   bundle.
3. `skill.xcode.foundations` — signing, entitlements, Release configuration, archive,
   and export.

This ordering is deliberate and differs from a build-then-check reading: steps 1 and 2
gate step 3. Producing an archive first and validating it afterwards means every
finding costs a rebuild.

## Exit Conditions

Complete when an exported build exists and:

- No known App Review Guideline violation remains unresolved or undocumented.
- The privacy manifest declares every collected data type and required-reason API.
- The archive is signed with the intended distribution identity and profile.

Stop and report if any Skill reports an unresolved dependency, naming the Skill and the
missing Contract. Never export a build past an unresolved step 1 or step 2 finding.
