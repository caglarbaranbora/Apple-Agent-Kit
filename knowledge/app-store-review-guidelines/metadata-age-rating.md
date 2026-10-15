# Metadata Age Rating

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.metadata-age-rating
artifact_type: knowledge
title: Metadata Age Rating
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 2.3.8 -- app and in-app purchase icons, screenshots, and previews must suit a 4+ audience whatever the app's rating, violent games choose non-graphic images, "For Kids"/"For Children" is reserved for the Kids Category, and icons and app name stay similar across sizes.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - metadata
  - age-rating
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.8
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.asset-content-restrictions
last_updated: 2026-10-15
```

## Intent

This contract defines guideline 2.3.8: App Store metadata is seen by every
audience, so its imagery is held to a 4+ rating even when the app is not.

## Scope

### Included

-   4+ suitability of app and in-app purchase icons, screenshots, previews
-   Violent games' metadata imagery
-   "For Kids" / "For Children" wording
-   Similarity of app name and icons across icon sizes and variants

### Excluded

-   Creative assets and the asset page's objectionable-content list — see
    `asset-content-restrictions`
-   The app's own age rating questionnaire — not covered

## Rules

### Rule 1

Agents MUST keep app and in-app purchase icons, screenshots, and previews
suitable for a 4+ age rating, even when the app is rated higher. Metadata
should "adhere to a 4+ age rating even if your app is rated higher."

### Rule 2

Agents MUST, for a game that includes violence, choose metadata images that
"don’t depict a gruesome death or a gun pointed at a specific character."

### Rule 3

Agents MUST NOT use "For Kids" or "For Children" in app metadata unless the
app is in the Kids Category; those terms are "reserved in the App Store for the
Kids Category."

### Rule 4

Agents SHOULD keep the app name and icons (small, large, Apple Watch app,
alternate icons, etc.) similar, "to avoid creating confusion."

## Compliant Example

-   ✓ A 17+ horror game's screenshots show its atmosphere and puzzles, with
    no gore. (Rules 1, 2)

## Non-Compliant Example

-   ✗ A shooter's first screenshot frames a gun aimed at a character's head.
    (Rule 2)
-   ✗ A general-audience drawing app subtitled "For Kids". (Rule 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3.8](https://developer.apple.com/app-store/review/guidelines/#2.3.8)
