# Asset Sequencing and Story

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.asset-sequencing-and-story
artifact_type: knowledge
title: Asset Sequencing and Story
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable guidance for ordering and unifying a product page's assets -- best features in the first three screenshots, a cohesive sequence, no screenshot spent on accolades or calls to action and one visual system.
domain: App Store Product Page
tags:
  - app-store-product-page
  - screenshots
  - sequencing
references:
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.screenshot-specifications
  - knowledge.app-store-product-page.video-asset-design
  - knowledge.app-store-product-page.creative-assets
last_updated: 2026-10-15
```

## Intent

This contract defines how a product page's screenshots are
ordered and unified, so that what search results show first and what the
product page shows together tell one story.

## Scope

### Included

-   Screenshot order and the search-results window
-   Screenshot content focus
-   Visual consistency across assets

### Excluded

-   Counts and sizes — see `screenshot-specifications`

## Rules

### Rule 1

Agents SHOULD put the strongest features in the first three screenshots,
which are what search results show when the app has no search result creative
asset and no app preview leads: "Depending on orientation, up to three
screenshots can appear in search results." "Lead with your best features."

### Rule 2

Agents SHOULD order screenshots so that, read in sequence, they tell one
story. "…sequence them so they tell a cohesive story…"

### Rule 3

Agents SHOULD NOT spend a whole screenshot on accolades or a call to action.
"…avoid using the entire asset to highlight general accolades or
call-to-action statements."

### Rule 4

Agents SHOULD share one visual system across every asset. "…consider using
similar visual style, such as color palette, iconography, fonts, message, and
tone."

## Compliant Example

-   ✓ Screenshots 1–3 show the three headline features in one type family
    and palette; 4–8 continue the same flow. (Rules 1, 2, 4)

## Non-Compliant Example

-   ✗ Screenshot 1 is a full-frame "Download now!" banner. (Rules 1, 3)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
