---
name: app-store-review-guidelines
description: Route App Store submission-compliance tasks to the correct Knowledge Contracts — app completeness, demo accounts, screenshot/description accuracy, in-app purchase requirements, external payment link restrictions, restore purchases, minimum functionality, spam/duplicate-app avoidance, permission usage strings, privacy manifest, and privacy nutrition label accuracy. Use when preparing an app for App Store submission, implementing in-app purchase, writing Info.plist usage descriptions, building a PrivacyInfo.xcprivacy manifest, filling out the App Store Connect privacy questionnaire, or reviewing App Store metadata before submitting. Triggers on App Store review, App Review guidelines, app rejected, in-app purchase, IAP, restore purchases, demo account, screenshot requirements, app description, privacy manifest, PrivacyInfo.xcprivacy, privacy nutrition label, App Store Connect privacy, spam app, duplicate app, minimum functionality, NSUsageDescription, permission usage string.
id: skill.app-store-review-guidelines.submission
title: App Store Review Guidelines — Submission Compliance
version: 0.1.0
status: Draft
artifact_type: skill
domain: App Store Review Guidelines
routes: [knowledge.app-store-review-guidelines.app-completeness, knowledge.app-store-review-guidelines.demo-account, knowledge.app-store-review-guidelines.screenshots-accuracy, knowledge.app-store-review-guidelines.description-accuracy, knowledge.app-store-review-guidelines.digital-goods-iap, knowledge.app-store-review-guidelines.external-payment-links, knowledge.app-store-review-guidelines.restore-purchases, knowledge.app-store-review-guidelines.minimum-functionality, knowledge.app-store-review-guidelines.spam-duplicate-apps, knowledge.app-store-review-guidelines.permission-usage-strings, knowledge.app-store-review-guidelines.privacy-manifest, knowledge.app-store-review-guidelines.privacy-nutrition-label]
related: []
last_updated: 2026-07-31
---

# App Store Review Guidelines — Submission Compliance Skill

## Purpose

Route App Store submission-compliance tasks to the minimum required
App Store Review Guidelines Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-store-review-guidelines/.

-   Submission completeness -> app-completeness.md, demo-account.md
-   Metadata accuracy -> screenshots-accuracy.md, description-accuracy.md
-   In-app purchase -> digital-goods-iap.md, external-payment-links.md, restore-purchases.md
-   App value & originality -> minimum-functionality.md, spam-duplicate-apps.md
-   Privacy compliance -> permission-usage-strings.md, privacy-manifest.md, privacy-nutrition-label.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-store-review-guidelines/ — do not guess or
fall back to general knowledge. Safety, most of Legal, Design (4.0,
owned by `human-interface-guidelines`), and Guideline 4.8 Sign in with
Apple are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
