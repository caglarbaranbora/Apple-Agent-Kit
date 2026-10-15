# In-App Event Media

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.in-app-event-media
artifact_type: knowledge
title: In-App Event Media
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the media an In-App Event needs -- the 16:9 event card and the 9:16 event details page, their image and video specifications -- and how it relates to the event badge.
domain: App Store Product Page
tags:
  - app-store-product-page
  - in-app-events
  - creative-assets
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on:
  - knowledge.app-store-product-page.creative-assets
related: []
last_updated: 2026-10-15
```

## Intent

This contract defines the two pieces of media every In-App Event needs, so an
agent produces both orientations to specification. In-App Event cards are
creative assets, so the general creative-asset rules (alpha, review) load with
this contract through its dependency.

## Scope

### Included

-   Event card and event details page media
-   Their image and video specifications
-   Relationship to the event badge

### Excluded

-   In-App Event metadata accuracy (guideline 2.3.13) — not covered; App
    Review compliance is `app-store-review-guidelines`'s angle

## Rules

### Rule 1

Agents MUST provide both media for an event. "You need media for the event
card (16:9 landscape) and the event details page (9:16 portrait)."

### Rule 2

Agents MUST build the event card at 16:9 between 1920 x 1080 and
3840 x 2160, with any image at most 500 MB and any video at 30 or 60 fps
and 15–30 seconds.

### Rule 3

Agents MUST build the event details page media at 9:16 between 1080 x 1920
and 2160 x 3840, with any image at most 500 MB and any video at 30 or 60 fps
and 15–30 seconds.

### Rule 4

Agents SHOULD design the media to complement the event's badge (Challenge,
Competition, Live Event, Major Update, New Season, Premiere, Special Event)
rather than repeat it. "Design your media to complement the badge rather than
duplicate it."

## Compliant Example

-   ✓ A 1920 x 1080 card and a 1080 x 1920 details video (20 seconds) for a
    "New Season" event, neither of which prints "New Season". (Rules 1–4)

## Non-Compliant Example

-   ✗ One 16:9 image reused for both the card and the details page. (Rule 1)
-   ✗ A 10-second event card video. (Rule 2)

## Dependencies

-   `knowledge.app-store-product-page.creative-assets` (Rules 5 and 9 — no
    alpha; standalone review — apply to event media.)

## References

-   [App Store Connect Help — Creative assets specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications)
-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
