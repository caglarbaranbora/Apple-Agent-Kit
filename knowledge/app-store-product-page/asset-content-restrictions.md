# Asset Content Restrictions

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.asset-content-restrictions
artifact_type: knowledge
title: Asset Content Restrictions
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines what Apple's asset guidance forbids in any App Store asset -- pricing and discounts, URLs and copyright symbols, unearned or Apple-designated recognitions, other platforms, content above 4+, graphic violence -- and the relation-to-functionality limit on content outside the app.
domain: App Store Product Page
tags:
  - app-store-product-page
  - content-restrictions
  - creative-assets
  - screenshots
references:
  - https://developer.apple.com/app-store/asset-best-practices/
  - https://developer.apple.com/app-store/review/guidelines/#2.3.7
depends_on: []
related:
  - knowledge.app-store-review-guidelines.description-accuracy
  - knowledge.app-store-review-guidelines.apple-trademarks-and-product-confusion
  - knowledge.app-store-product-page.creative-assets
last_updated: 2026-10-15
```

## Intent

This contract defines what no App Store asset — screenshot, app preview, or
creative asset — may contain, per Apple's asset best practices page. Apart
from pricing (guideline 2.3.7), these rules come from Apple's asset guidance,
not the App Review Guidelines: agents apply them as written but MUST NOT
present a breach as a stated rejection reason.

## Scope

### Included

-   Pricing, discounts, URLs, copyright symbols
-   Unearned awards and Apple-designated recognitions
-   Other platforms and 4+ suitability, extended to creative assets
-   Violence limits; content outside the app

### Excluded

-   Guideline 2.3.8 and 2.3.10 as review rules for screenshots and previews
    — `app-store-review-guidelines` owns them
-   Misleading marketing claims in text metadata — see `description-accuracy`

## Rules

### Rule 1

Agents MUST NOT show specific pricing or discounts in any asset. "Don't
include specific pricing, discounts, website URLs, copyright symbols."
Guideline 2.3.7 says the same for screenshots and previews, which "should not
include prices, terms, or descriptions that are not specific to the metadata
type".

### Rule 2

Agents MUST NOT show website URLs or copyright symbols in any asset.

### Rule 3

Agents MUST NOT claim awards or recognition the app has not received. "Avoid
claims that can't be verified, such as awards or recognition that your app or
game hasn't actually received."

### Rule 4

Agents MUST NOT show Apple-designated recognitions. "Please don't include any
Apple-designated recognitions — such as Editor's Choice, App of the Day, Game
of the Day, or Apple Design Award winner".

### Rule 5

Agents MUST keep logos and references to other platforms or marketplaces out
of creative assets too. "Don't include logos or references to other platforms
or marketplaces."

### Rule 6

Agents MUST hold creative assets to a 4+ age rating. "Assets displayed on the App
Store must meet a 4+ age rating, even if your app's rating is higher",
refraining from "explicit or harmful imagery, profanity, illegal drugs,
self-harm, hate speech, stereotypes, sexually suggestive content,
inflammatory religious commentary, or inaccurate and misleading quotations of
religious texts."

### Rule 7

Agents MAY use action imagery for a game with violence but MUST NOT show
"gore, graphic imagery, or weapons that are pointed directly at a person or
the audience."

### Rule 8

Agents MUST keep content from outside the app related to what the app does.
"While you may depict content outside of your app or game in use, it must
still relate to its general functionality."

## Compliant Example

-   ✓ A search result asset with the game's characters mid-action, no price,
    no URL, no platform logos. (Rules 1, 2, 5, 7)

## Non-Compliant Example

-   ✗ A header reading "50% off this week — example.com". (Rules 1, 2)
-   ✗ A screenshot captioned "App of the Day". (Rule 4)
-   ✗ A creative asset with a rifle aimed at the viewer. (Rule 7)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
-   [Apple App Review Guidelines — 2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)
