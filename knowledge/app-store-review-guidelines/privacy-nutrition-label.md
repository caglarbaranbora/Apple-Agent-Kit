# Privacy Nutrition Label

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.privacy-nutrition-label
type: knowledge
title: Privacy Nutrition Label
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the App Store Connect "App Privacy" nutrition-label disclosure requirements — declared data types, identity linkage, and tracking use — and the accuracy bar relative to actual app behavior, per guideline 5.1.1 and 5.1.2.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - privacy
  - nutrition-label
  - app-privacy-details
references:
  - https://developer.apple.com/app-store/app-privacy-details/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-manifest
  - knowledge.app-store-review-guidelines.permission-usage-strings
updated: 2026-07-31
```

## Intent

This contract defines how an agent fills out the App Store Connect
"App Privacy" questionnaire accurately: which data types to declare,
how to mark identity linkage and tracking use, and when a data type may
be omitted (guideline 5.1.1, 5.1.2).

## Scope

### Included

-   Data-type disclosure scope (first-party and third-party SDK collection)
-   Identity-linkage marking
-   Tracking-use marking and its relationship to App Tracking Transparency
-   Data-use-purpose accuracy and update obligation
-   Conditions for optional (omittable) disclosure

### Excluded

-   `PrivacyInfo.xcprivacy` bundle-level declarations — see `privacy-manifest`
-   Runtime `Info.plist` permission-prompt strings — see `permission-usage-strings`

## Rules

### Rule 1

Agents MUST declare, in App Store Connect, every data type collected by
the app itself or by any bundled third-party SDK/partner (analytics, ad
networks) — not only first-party collection.

### Rule 2

Agents MUST correctly mark each declared data type as linked or not
linked to user identity (account, device, or other identifying
detail).

### Rule 3

Agents MUST correctly mark whether each data type is used for tracking
(linking app data with third-party data for targeted ads/measurement,
or sharing with data brokers) — tracking additionally requires App
Tracking Transparency permission.

### Rule 4

Agents MUST keep declared data uses (third-party advertising, developer
marketing, analytics, product personalization, app functionality,
other) in sync with actual app behavior, updating App Store Connect
answers whenever practices change.

### Rule 5

Agents MAY omit a data type from disclosure only if it meets every
"optional disclosure" condition simultaneously: not used for tracking,
not used for third-party/developer advertising or "Other Purposes,"
collected only in an optional non-primary flow, and explicitly
user-provided with disclosed consent each time.

## Compliant Example

-   ✓ Privacy label declares "Precise Location — linked to identity — used for App Functionality," matching the app's actual location-based feature. (Rules 1, 2, 4)

## Non-Compliant Example

-   ✗ App's privacy label declares "Data Not Collected" while a bundled analytics SDK silently transmits device identifiers to a third-party ad network. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/)
