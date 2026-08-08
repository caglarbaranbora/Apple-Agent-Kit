# Description Accuracy

Status: Draft Version: 0.2.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.description-accuracy
artifact_type: knowledge
title: Description Accuracy
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Defines requirements for accurate, non-misleading App Store descriptions and keywords, and prohibits hidden/undocumented functionality, per guidelines 2.3, 2.3.1(a), and 2.3.7.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - description
  - metadata
  - keywords
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
last_updated: 2026-08-08
```

## Intent

This contract defines the accuracy bar for an app's textual App Store
metadata: no hidden features, no misleading marketing, and no
keyword-stuffing (guideline 2.3, 2.3.1(a), 2.3.7).

## Scope

### Included

-   Prohibition on hidden/dormant/undocumented app functionality
-   Review-notes specificity requirement for new features
-   Prohibition on misleading marketing claims
-   App name/keyword accuracy and length limits

### Excluded

-   Screenshot/preview content accuracy — see `screenshots-accuracy`

## Rules

### Rule 1

Agents MUST NOT ship hidden, dormant, or undocumented features — all
functionality must be clear to end users and to App Review.

### Rule 2

Agents MUST describe all new features, functionality, and product
changes with specificity in the App Store Connect "Notes for Review"
field — generic descriptions are rejected.

### Rule 3

Agents MUST NOT market the app in a misleading way, such as promoting
functionality the app does not actually provide, or a false price.

### Rule 4

Agents MUST choose a unique app name of 30 characters or fewer, and
accurate keywords; agents MUST NOT pack metadata with trademarked
terms, competitor app names, pricing information, or irrelevant phrases
to game search ranking.

## Compliant Example

-   ✓ App description matches shipped functionality exactly; review notes explain a newly added feature in specific, testable terms. (Rules 1, 2)

## Non-Compliant Example

-   ✗ App description advertises "AI-powered virus scanning" that the app doesn't perform. (Rule 3)
-   ✗ Keyword field is stuffed with competitor brand names. (Rule 4)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3 Accurate Metadata](https://developer.apple.com/app-store/review/guidelines/#2.3)
