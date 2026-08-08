# Minimum Functionality

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.minimum-functionality
artifact_type: knowledge
title: Minimum Functionality
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the requirement that an app provide functionality, content, and UI beyond a repackaged website or template-generated wrapper, per guideline 4.2.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - minimum-functionality
  - quality
references:
  - https://developer.apple.com/app-store/review/guidelines/#4.2
depends_on: []
related:
  - knowledge.app-store-review-guidelines.spam-duplicate-apps
last_updated: 2026-08-08
```

## Intent

This contract defines the "app-like" bar an agent must clear: real
utility or lasting value beyond a repackaged website, and a prohibition
on unmodified template-generated apps (guideline 4.2, 4.2.2, 4.2.6).

## Scope

### Included

-   Requirement for native functionality beyond a website wrapper
-   Prohibition on marketing/aggregator-only apps
-   Prohibition on unmodified commercialized-template submissions
-   Aggregated "picker"-model exception for template providers

### Excluded

-   Duplicate/near-identical app submissions — see `spam-duplicate-apps`

## Rules

### Rule 1

Agents MUST include features, content, or UI that elevate the app
beyond a repackaged website; App Review rejects apps that are not
"app-like."

### Rule 2

Agents MUST ensure the app provides lasting entertainment value or
adequate utility — a thin marketing/advertising/content-aggregation
wrapper is not acceptable.

### Rule 3

Agents MUST NOT generate the app from a commercialized app-template or
app-generation service unless it is submitted directly by the content
provider itself; template-generation services must not submit apps on
behalf of their clients.

### Rule 4

Agents MAY use an aggregated/"picker" binary model (one binary hosting
many clients' customized content, e.g. a restaurant-finder app with
per-restaurant entries) as an acceptable alternative to per-client app
submissions.

## Compliant Example

-   ✓ App wraps a website's content but adds a native offline mode, push notifications, and platform-specific UI not present on the web. (Rule 1)

## Non-Compliant Example

-   ✗ App is a WebView pointed at the company's marketing site with no native functionality added. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 4.2 Minimum Functionality](https://developer.apple.com/app-store/review/guidelines/#4.2)
