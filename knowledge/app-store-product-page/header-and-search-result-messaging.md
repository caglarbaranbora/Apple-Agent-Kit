# Header and Search Result Messaging

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.header-and-search-result-messaging
artifact_type: knowledge
title: Header and Search Result Messaging
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable messaging guidance for product page header and search result creative assets -- one idea per header, purpose obvious at a glance, the firsthand experience in search, and testing header variants.
domain: App Store Product Page
tags:
  - app-store-product-page
  - product-page-header
  - search-results
  - messaging
references:
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.creative-assets
  - knowledge.app-store-product-page.image-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines what a product page header and a search result asset
should say, using only guidance an agent can check against the finished
asset.

## Scope

### Included

-   Header focus
-   Search result clarity and firsthand experience
-   Testing header variants

### Excluded

-   Specifications — see `creative-assets`
-   Subjective guidance ("Design with a first-time visitor in mind",
    "compelling visuals") — Excluded; not checkable

## Rules

### Rule 1

Agents SHOULD build each product page header around one idea, without dense or
cluttered visuals. "Focus on a single, clear idea. Visually dense or cluttered
assets dilute your impact."

### Rule 2

Agents SHOULD make the app's purpose readable from a search result asset alone.
"State the obvious. … be sure your app or game's purpose is obvious at a
glance."

### Rule 3

Agents SHOULD show the app or game experience itself in a search result asset.
"Showcase the firsthand experience."

### Rule 4

Agents SHOULD test alternative header visuals with product page optimization
rather than choosing one untested. "…you can use product page optimization to
test alternative header visuals…"

## Compliant Example

-   ✓ A recipe app's header shows one plated dish under the line "Dinner in
    20 minutes"; its search result asset shows the cooking-mode screen. (Rules 1–3)

## Non-Compliant Example

-   ✗ A header packing six feature callouts and a collage of screens. (Rule 1)
-   ✗ A search result asset of an abstract gradient and the app's logo, with
    no hint of what the app does. (Rules 2, 3)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
