---
name: app-store-review-guidelines
description: Route App Store submission-compliance tasks to the correct Knowledge Contracts — app completeness, demo accounts, screenshot/description accuracy, in-app purchase requirements, external payment link restrictions, restore purchases, minimum functionality, spam/duplicate-app avoidance, permission usage strings, privacy manifest, privacy nutrition label accuracy, user-generated content moderation, developer contact information, data security, copycats and impersonation, the login-services equivalent option, third-party content licensing, Apple trademarks, and the ratings API. Use when preparing an app for App Store submission, implementing in-app purchase, writing Info.plist usage descriptions, building a PrivacyInfo.xcprivacy manifest, adding user-generated content or a social login, asking users for a rating, shipping third-party assets, or reviewing App Store metadata before submitting. Triggers on App Store review, App Review guidelines, app rejected, in-app purchase, IAP, restore purchases, demo account, screenshot requirements, app description, privacy manifest, PrivacyInfo.xcprivacy, privacy nutrition label, App Store Connect privacy, spam app, duplicate app, minimum functionality, NSUsageDescription, permission usage string, user-generated content, UGC moderation, report content, block user, support URL, contact information, guideline 1.2, guideline 4.8, Sign in with Apple requirement, social login, copycat app, impersonation, trademark, Apple emoji, requestReview, SKStoreReviewController, review prompt, rate this app.
id: skill.app-store-review-guidelines.submission
title: App Store Review Guidelines — Submission Compliance
version: 1.0.0
status: Approved
artifact_type: skill
domain: App Store Review Guidelines
routes: [knowledge.app-store-review-guidelines.app-completeness, knowledge.app-store-review-guidelines.demo-account, knowledge.app-store-review-guidelines.screenshots-accuracy, knowledge.app-store-review-guidelines.description-accuracy, knowledge.app-store-review-guidelines.digital-goods-iap, knowledge.app-store-review-guidelines.external-payment-links, knowledge.app-store-review-guidelines.restore-purchases, knowledge.app-store-review-guidelines.minimum-functionality, knowledge.app-store-review-guidelines.spam-duplicate-apps, knowledge.app-store-review-guidelines.permission-usage-strings, knowledge.app-store-review-guidelines.privacy-manifest, knowledge.app-store-review-guidelines.privacy-nutrition-label, knowledge.app-store-review-guidelines.user-generated-content-moderation, knowledge.app-store-review-guidelines.developer-contact-information, knowledge.app-store-review-guidelines.data-security, knowledge.app-store-review-guidelines.copycat-and-impersonation, knowledge.app-store-review-guidelines.login-services-equivalent-option, knowledge.app-store-review-guidelines.third-party-content-licensing, knowledge.app-store-review-guidelines.apple-trademarks-and-product-confusion, knowledge.app-store-review-guidelines.review-prompt-api]
related:
  - skill.authenticationservices.foundations
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-08
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
-   Safety -> user-generated-content-moderation.md (1.2 — filter, report, block, contact), developer-contact-information.md (1.5), data-security.md (1.6)
-   Originality & sign-in -> copycat-and-impersonation.md (4.1), login-services-equivalent-option.md (4.8)
-   Intellectual property -> third-party-content-licensing.md (5.2.1-5.2.3), apple-trademarks-and-product-confusion.md (5.2.4, 5.2.5)
-   Ratings -> review-prompt-api.md (5.6.1, 5.6.3)

Never load more than the contracts relevant to the specific question.
For implementing Sign in with Apple once 4.8 requires it, route to
`skill.authenticationservices.foundations`; for sign-in screen layout, to
`skill.human-interface-guidelines.foundations`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-store-review-guidelines/ — do not guess or
fall back to general knowledge.

-   Safety 1.1 (objectionable content) and 1.2.1 (creator age restriction);
    Design 4.6, which Apple's own text marks "Intentionally omitted"; Legal
    5.6.2 and 5.6.4, which govern developer conduct rather than the app —
    Excluded
-   Safety 1.3 (Kids), 1.4 (physical harm), 1.7; Design 4.4 (extensions), 4.5
    (Apple sites and services), 4.7 (mini apps and emulators); Legal 5.3, 5.4,
    5.5 — Deferred, scheduled at Tier 3; these are vertical, not the
    near-universal surface Tier 1 covers
-   Design 4.0 as design guidance — owned by `human-interface-guidelines`
