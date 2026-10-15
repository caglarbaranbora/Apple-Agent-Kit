---
name: app-store-product-page
description: Route App Store product page asset tasks to the correct Knowledge Contracts — screenshot specifications, app preview specifications, creative assets (product page header, search results, universal asset), In-App Event media, asset content restrictions, header and search result messaging, image and video asset design, and asset sequencing. Use when sizing or exporting screenshots or app previews, designing a product page header or search result creative asset, preparing In-App Event media, choosing a poster frame, or ordering screenshots for the App Store. v1 is iOS/iPadOS visual assets only — no product page text fields, no Mac/TV/Vision/Watch asset specs. Whether a screenshot passes App Review is owned by app-store-review-guidelines. Triggers on screenshot specifications, screenshot sizes, App Store screenshot size, app preview specifications, app preview video, product page header, search result creative asset, creative assets, universal creative asset, In-App Event media, event card, poster frame, Asset Library, product page preview tool, App Store asset best practices, iPhone Duo screenshots.
id: skill.app-store-product-page.foundations
title: App Store Product Page — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: App Store Product Page
routes: [knowledge.app-store-product-page.screenshot-specifications, knowledge.app-store-product-page.app-preview-specifications, knowledge.app-store-product-page.creative-assets, knowledge.app-store-product-page.in-app-event-media, knowledge.app-store-product-page.asset-content-restrictions, knowledge.app-store-product-page.header-and-search-result-messaging, knowledge.app-store-product-page.image-asset-design, knowledge.app-store-product-page.video-asset-design, knowledge.app-store-product-page.asset-sequencing-and-story]
related:
  - skill.app-store-review-guidelines.submission
  - skill.human-interface-guidelines.foundations
last_updated: 2026-10-15
---

# App Store Product Page — Foundations Skill

## Purpose

Route App Store product page asset tasks to the minimum required App Store
Product Page Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-store-product-page/.

-   Screenshot sizes and counts -> screenshot-specifications.md
-   App preview encoding and placement -> app-preview-specifications.md
-   Product page header, search result, universal asset -> creative-assets.md
-   In-App Event card and details media -> in-app-event-media.md
-   What no asset may show -> asset-content-restrictions.md
-   What a header or search asset should say -> header-and-search-result-messaging.md
-   Composing an image -> image-asset-design.md
-   Cutting a video, poster frame, preview story -> video-asset-design.md
-   Ordering and unifying the screenshots -> asset-sequencing-and-story.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-store-product-page/ — do not guess or
fall back to general knowledge.

-   Whether screenshots and previews pass App Review (guideline 2.3) — owned by
    `app-store-review-guidelines`
-   App icon design — owned by `human-interface-guidelines`
-   Product page text fields (subtitle, promotional text, keywords), product
    page optimization setup, and custom product pages — Deferred
-   Mac, Apple TV, Apple Vision Pro and Apple Watch asset specifications;
    App Store Connect upload mechanics and API — Excluded
