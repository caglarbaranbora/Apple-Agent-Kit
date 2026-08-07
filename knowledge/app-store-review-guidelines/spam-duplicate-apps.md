# Spam / Duplicate Apps

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.spam-duplicate-apps
artifact_type: knowledge
title: Spam / Duplicate Apps
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the prohibition on submitting multiple near-identical apps (per-location/per-team variants) or apps indistinguishable from existing App Store listings, per guideline 4.3.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - spam
  - duplicate-apps
  - quality
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.minimum-functionality
last_updated: 2026-07-31
```

## Intent

This contract defines when a family of near-identical apps must be
consolidated into a single app with in-app variation instead of
separate Bundle IDs, and the bar for originality versus existing App
Store listings (guideline 4.3(a), 4.3(b)).

## Scope

### Included

-   Prohibition on multiple Bundle IDs for one underlying app
-   IAP-based variation as the preferred alternative
-   Originality bar relative to existing App Store listings

### Excluded

-   General "app-like" minimum-functionality bar — see `minimum-functionality`

## Rules

### Rule 1

Agents MUST NOT create multiple Bundle IDs of the same app for what
should be a single app with variant data (e.g., a separate app per city
instead of one app with in-app search/selection).

### Rule 2

Agents SHOULD use in-app purchase to deliver location/team/university-
specific variations from a single app binary, rather than submitting a
separate app per variation.

### Rule 3

Agents MUST NOT submit an app that is indistinguishable from apps
already widely available on the App Store without offering a
meaningfully different or improved experience.

## Compliant Example

-   ✓ A single "City Guides" app lets users search/select any city inside the app via IAP-unlocked city packs. (Rules 1, 2)

## Non-Compliant Example

-   ✗ Developer submits "City Guide: Paris", "City Guide: Berlin", and "City Guide: Tokyo" as separate apps built from a shared codebase with only the city name changed. (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 4.3 Spam](https://developer.apple.com/app-store/review/guidelines/)
