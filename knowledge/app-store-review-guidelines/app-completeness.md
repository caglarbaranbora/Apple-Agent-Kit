# App Completeness

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.app-completeness
artifact_type: knowledge
title: App Completeness
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines requirements for submitting a final, fully tested, non-placeholder app build to App Review, including functional in-app purchase items at submission time.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - app-completeness
  - submission
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.demo-account
  - knowledge.app-store-review-guidelines.digital-goods-iap
last_updated: 2026-08-08
```

## Intent

This contract defines what makes an app submission "complete" for App
Review purposes: no placeholder content, no on-device crashes, and fully
functional in-app purchase items at submission time (guideline 2.1).

## Scope

### Included

-   Prohibition on placeholder/temporary content in the submitted build
-   Prohibition on broken/non-functional URLs referenced by the app
-   On-device crash/stability testing before submission
-   Functional, reviewer-visible in-app purchase items at submission

### Excluded

-   Demo account / demo mode requirement for login-gated apps — see `demo-account`
-   In-app purchase implementation rules beyond submission-time visibility — see `digital-goods-iap`

## Rules

### Rule 1

Agents MUST NOT include placeholder text, empty websites, or temporary
content in the submitted build.

### Rule 2

Agents MUST test the app on-device for bugs and stability before
submission; App Review rejects binaries that crash or exhibit obvious
technical problems.

### Rule 3

Agents MUST ensure any in-app purchase items configured for the app are
complete, up-to-date, visible to the reviewer, and functional at
submission time. If a configured IAP item cannot be found or reviewed,
the review notes must explain why.

### Rule 4

Agents SHOULD ensure all URLs referenced by the app or its metadata are
fully functional, not broken or placeholder links.

## Compliant Example

-   ✓ Submitted build has all placeholder Lorem Ipsum content replaced with real copy, was tested on a real device with zero reproduced crashes, and its configured IAP items are purchasable in the reviewer's sandbox account. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ App ships with a "Coming Soon" placeholder screen in place of a promised feature. (Rule 1)
-   ✗ App crashes on first launch during reviewer testing. (Rule 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.1 App Completeness](https://developer.apple.com/app-store/review/guidelines/#2.1)
