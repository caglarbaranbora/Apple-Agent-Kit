# Other Platform References

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.other-platform-references
artifact_type: knowledge
title: Other Platform References
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 2.3.10 -- no names, icons, or imagery of other mobile platforms or alternative app marketplaces in the app or its metadata, including a third-party status bar in a screenshot.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - metadata
  - screenshots
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.10
  - https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.asset-content-restrictions
last_updated: 2026-10-15
```

## Intent

This contract defines guideline 2.3.10: an App Store app and its metadata stay
focused on Apple platforms and do not show other mobile platforms or
alternative app marketplaces.

## Scope

### Included

-   Names, icons, imagery of other mobile platforms and marketplaces
-   Third-party status bars in screenshots

### Excluded

-   Creative assets — see `asset-content-restrictions`

## Rules

### Rule 1

Agents MUST NOT include "names, icons, or imagery of other mobile platforms or
alternative app marketplaces" in the app or its metadata, unless there is
"specific, approved interactive functionality."

### Rule 2

Agents MUST NOT submit screenshots that show a third-party platform, a status
bar included. "Screenshots that reference third-party platforms, such as in a
status bar, are assessed under App Review Guideline 2.3.10."

## Compliant Example

-   ✓ Screenshots captured in the iOS Simulator with a clean status bar.
    (Rule 2)

## Non-Compliant Example

-   ✗ A screenshot taken on an Android build, its status bar visible. (Rule 2)
-   ✗ A description line "Also on Google Play". (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3.10](https://developer.apple.com/app-store/review/guidelines/#2.3.10)
-   [App Review — Guideline 2.3.3 Screenshots](https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots)
