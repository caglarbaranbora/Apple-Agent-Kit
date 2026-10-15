# Creative Assets

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.creative-assets
artifact_type: knowledge
title: Creative Assets
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines App Store creative assets -- what they are, their exemption from the in-use requirement, product page header and search result specifications, the universal asset, playback behaviour, fallback, and how they are reviewed.
domain: App Store Product Page
tags:
  - app-store-product-page
  - creative-assets
  - product-page-header
  - search-results
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
  - https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.header-and-search-result-messaging
  - knowledge.app-store-product-page.asset-content-restrictions
  - knowledge.app-store-review-guidelines.screenshots-accuracy
last_updated: 2026-10-15
```

## Intent

This contract defines creative assets — the optional product page header,
search result, and In-App Event card images and videos available from iOS 27
and iPadOS 27 — so an agent builds them to specification and does not confuse
them with screenshots and app previews, which carry different rules.

## Scope

### Included

-   Definition, optionality, OS availability
-   Exemption from the in-use requirement
-   Header and search result image and video specifications
-   Universal asset, playback behaviour, fallback, review

### Excluded

-   In-App Event card and details page media — see `in-app-event-media`
-   Messaging for header and search assets — see
    `header-and-search-result-messaging`

## Rules

### Rule 1

Agents MUST treat creative assets as optional and separate from screenshots
and app previews, available for apps "running iOS 27 or iPadOS 27 or later".
"Creative assets are optional and separate from your app's screenshots, app
previews, In-App Purchase and Subscription images, and any promotional artwork
requested by editorial teams."

### Rule 2

Agents MAY show brand, seasonal offerings, or new content in a creative asset
rather than the app in use: creative assets are "distinct from the in-use
functionality requirement in app previews and screenshots."

### Rule 3

Agents MUST build a product page header as a 21:9 image at 3840 x 1646
(.jpeg, .jpg, .png) or a 16:9 .png at 5244 x 2950, or as a 21:9 video at
3840 x 1646, 30 or 60 fps, 5–30 seconds (.mov, .m4v, .mp4).

### Rule 4

Agents MUST build a search result asset as a 3:2 image between 1920 x 1280
and 3840 x 2560 (.jpeg, .jpg, .png) or a 16:9 .png at 5244 x 2950, or as a
3:2 video within the same bounds, 30 or 60 fps, 5–30 seconds.

### Rule 5

Agents MUST NOT include an alpha channel or transparency. "Images can't
include alpha channels or transparencies."

### Rule 6

Agents MAY upload one universal creative asset for both placements. "If you
upload a universal creative asset, you can use it for both your product page
header and search results placement." Agents MUST NOT assume which
specification row is the universal one; the specification page does not label
it.

### Rule 7

Agents MUST expect videos to play muted and loop: muted with no unmute in
search results, muted by default but unmutable on the product page, and
looping in both. "Videos are muted by
default in search results and can't currently be unmuted. On your product
page, videos are also muted by default, but people can unmute them. Videos
loop continuously in both placements."

### Rule 8

Agents MUST expect In-App Events, app previews, and screenshots to appear in
search results when no search result creative asset is provided. "If you
choose to not use a search result creative asset, your In-App Events, app
previews, and screenshots will appear."

### Rule 9

Agents MUST check a creative asset submitted on its own against the app's
current release. "Standalone assets are reviewed against your app's latest
version."

## Compliant Example

-   ✓ A 3840 x 1646 .jpeg header showing a seasonal campaign, plus a
    1920 x 1280 search result video whose message reads without sound.
    (Rules 2, 3, 4, 7)

## Non-Compliant Example

-   ✗ A 16:9 3840 x 2160 header image. (Rule 3)
-   ✗ A search result video built to play once, with an end card that assumes
    it stops. (Rule 7)

## Dependencies

None.

## References

-   [App Store Connect Help — Creative assets specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications)
-   [App Store Connect Help — Manage your App Store assets](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets)
-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
