# App Store Review Guidelines

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: reference.apple.app-store-review-guidelines
artifact_type: reference
title: App Store Review Guidelines
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's App Store Review Guidelines behind skill.app-store-review-guidelines.submission -- the sections most frequently responsible for real-world rejections and actionable from application code or App Store Connect metadata, indexed per guideline anchor across Safety (1.2, 1.5, 1.6), Performance (2.1, 2.3), Business (3.1.1), Design (4.1, 4.2, 4.3, 4.8), and Legal (5.1, 5.2, 5.6).
domain: App Store Review Guidelines
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/app-store/app-privacy-details/
https://developer.apple.com/app-store/review/guidelines/#1.2
https://developer.apple.com/app-store/review/guidelines/#1.5
https://developer.apple.com/app-store/review/guidelines/#1.6
https://developer.apple.com/app-store/review/guidelines/#2.1
https://developer.apple.com/app-store/review/guidelines/#2.3
https://developer.apple.com/app-store/review/guidelines/#2.3.3
https://developer.apple.com/app-store/review/guidelines/#3.1.1
https://developer.apple.com/app-store/review/guidelines/#4.1
https://developer.apple.com/app-store/review/guidelines/#4.2
https://developer.apple.com/app-store/review/guidelines/#4.3
https://developer.apple.com/app-store/review/guidelines/#4.8
https://developer.apple.com/app-store/review/guidelines/#5.1
https://developer.apple.com/app-store/review/guidelines/#5.1.1
https://developer.apple.com/app-store/review/guidelines/#5.1.2
https://developer.apple.com/app-store/review/guidelines/#5.2.1
https://developer.apple.com/app-store/review/guidelines/#5.2.2
https://developer.apple.com/app-store/review/guidelines/#5.2.3
https://developer.apple.com/app-store/review/guidelines/#5.2.4
https://developer.apple.com/app-store/review/guidelines/#5.2.5
https://developer.apple.com/app-store/review/guidelines/#5.6.1
https://developer.apple.com/app-store/review/guidelines/#5.6.3
https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
https://developer.apple.com/documentation/storekit/skstorereviewcontroller
https://developer.apple.com/documentation/storekit/skstorereviewcontroller/requestreview(in:)
https://developer.apple.com/documentation/swiftui/environmentvalues/requestreview

## Purpose

Reference index for Apple's App Store Review Guidelines behind
`skill.app-store-review-guidelines.submission` — the sections most often
responsible for real-world rejections and actionable from application code
or App Store Connect metadata. Every source is a **per-guideline anchor**,
not the guidelines hub: the page carries an `id` for each numbered section,
so a Contract about 4.8 points at 4.8. Until 2026-08 ten Contracts shared a
single bare-hub citation, which reference-spec.md's specificity rule refuses
— "a bare hub that indexes unrelated topics is not" specific enough.

Four sources are not guideline text. The App Store Connect privacy details
page and the privacy manifest documentation authorize how a declaration is
made rather than that it is required, and the three ratings-API pages carry
the mechanics behind guideline 5.6.1's instruction to use the provided API.
Design guidance (guideline 4.0) is owned by `human-interface-guidelines`.

## Primary Topics

- Safety: user-generated content moderation, developer contact information, data security
- Performance: app completeness, demo accounts, metadata and screenshot accuracy
- Business: in-app purchase for digital goods, external payment links, restoring purchases
- Design: copycats and impersonation, minimum functionality, spam, login services
- Legal — privacy: consent and usage strings, privacy manifest, nutrition label
- Legal — intellectual property: third-party licensing, Apple trademarks and products
- Legal — code of conduct: the ratings API and review manipulation

## Used By

- knowledge/app-store-review-guidelines/app-completeness.md ([[knowledge/app-store-review-guidelines/app-completeness]])
- knowledge/app-store-review-guidelines/demo-account.md ([[knowledge/app-store-review-guidelines/demo-account]])
- knowledge/app-store-review-guidelines/screenshots-accuracy.md ([[knowledge/app-store-review-guidelines/screenshots-accuracy]])
- knowledge/app-store-review-guidelines/description-accuracy.md ([[knowledge/app-store-review-guidelines/description-accuracy]])
- knowledge/app-store-review-guidelines/digital-goods-iap.md ([[knowledge/app-store-review-guidelines/digital-goods-iap]])
- knowledge/app-store-review-guidelines/external-payment-links.md ([[knowledge/app-store-review-guidelines/external-payment-links]])
- knowledge/app-store-review-guidelines/restore-purchases.md ([[knowledge/app-store-review-guidelines/restore-purchases]])
- knowledge/app-store-review-guidelines/minimum-functionality.md ([[knowledge/app-store-review-guidelines/minimum-functionality]])
- knowledge/app-store-review-guidelines/spam-duplicate-apps.md ([[knowledge/app-store-review-guidelines/spam-duplicate-apps]])
- knowledge/app-store-review-guidelines/permission-usage-strings.md ([[knowledge/app-store-review-guidelines/permission-usage-strings]])
- knowledge/app-store-review-guidelines/privacy-manifest.md ([[knowledge/app-store-review-guidelines/privacy-manifest]])
- knowledge/app-store-review-guidelines/privacy-nutrition-label.md ([[knowledge/app-store-review-guidelines/privacy-nutrition-label]])
- knowledge/app-store-review-guidelines/user-generated-content-moderation.md ([[knowledge/app-store-review-guidelines/user-generated-content-moderation]])
- knowledge/app-store-review-guidelines/developer-contact-information.md ([[knowledge/app-store-review-guidelines/developer-contact-information]])
- knowledge/app-store-review-guidelines/data-security.md ([[knowledge/app-store-review-guidelines/data-security]])
- knowledge/app-store-review-guidelines/copycat-and-impersonation.md ([[knowledge/app-store-review-guidelines/copycat-and-impersonation]])
- knowledge/app-store-review-guidelines/login-services-equivalent-option.md ([[knowledge/app-store-review-guidelines/login-services-equivalent-option]])
- knowledge/app-store-review-guidelines/third-party-content-licensing.md ([[knowledge/app-store-review-guidelines/third-party-content-licensing]])
- knowledge/app-store-review-guidelines/apple-trademarks-and-product-confusion.md ([[knowledge/app-store-review-guidelines/apple-trademarks-and-product-confusion]])
- knowledge/app-store-review-guidelines/review-prompt-api.md ([[knowledge/app-store-review-guidelines/review-prompt-api]])
- knowledge/privacy/manifest-file-structure-and-scope.md ([[knowledge/privacy/manifest-file-structure-and-scope]])
