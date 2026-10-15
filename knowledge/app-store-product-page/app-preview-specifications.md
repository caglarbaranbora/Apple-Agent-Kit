# App Preview Specifications

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.app-preview-specifications
artifact_type: knowledge
title: App Preview Specifications
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the App Store Connect app preview specifications for iOS and iPadOS apps -- count, length, file size, frame rate, encoding, accepted resolutions, unsupported targets, and where previews appear.
domain: App Store Product Page
tags:
  - app-store-product-page
  - app-previews
  - specifications
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.video-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines what App Store Connect accepts as an app preview, and
where a preview is shown, so an agent never renders a preview the upload
rejects or one that lands somewhere other than intended.

## Scope

### Included

-   Count, length, size, frame rate, video and audio encoding
-   Accepted iPhone (including iPhone Duo) and iPad resolutions
-   Unsupported targets
-   Placement relative to screenshots

### Excluded

-   What a preview may show (guideline 2.3.4) — see `screenshots-accuracy`
-   Poster frame, pacing, looping and audio choices — see `video-asset-design`
-   Mac, Apple TV and Apple Vision Pro previews — Excluded from v1
-   iPhone Duo device resolutions labelled "19.5:9" on the specification page
    — not encoded; the label does not match those sizes (about 1.45:1)

## Rules

### Rule 1

Agents MAY add up to three app previews per supported device size and
language; previews are optional. "App previews are optional. You can upload up
to three app previews per supported device size and language".

### Rule 2

Agents MUST deliver each preview at 15–30 seconds, at most 500 MB, at most
30 fps, as H.264 at 10–12 Mbps or ProRes 422 (HQ only) at about 220 Mbps VBR,
with stereo audio at 256 kbps AAC (or PCM for ProRes) at 44.1 or 48 kHz.

### Rule 3

Agents MUST use an accepted resolution. For iPhone with Dynamic Island (large
or medium display), iPhone with Face ID (large or medium display), and iPhone
Duo, that is 886 x 1920 or 1920 x 886. For iPhone with Home Button displays,
it is 1080 x 1920 or 1920 x 1080 for the large display and the 4" display, and
750 x 1334 or 1334 x 750 for the medium display. For iPad 13" display, it is
1200 x 1600 or 1600 x 1200. Agents MUST take any size not named here from the
specification page.

### Rule 4

Agents MUST NOT plan an app preview for a 3.5-inch iPhone ("App previews
aren't supported") or for an app on the App Store for iMessage ("App previews
are not available for apps on the App Store for iMessage").

### Rule 5

Agents MUST plan for previews appearing before screenshots on iPhone and
iPad whatever the upload order, and for a preview whose aspect ratio differs
from the screenshots appearing in "A Closer Look" instead. "App previews
always appear before screenshots on iPhone, iPad, Mac, and Apple TV — even if
you reorder them… If a preview video uses an aspect ratio different from your
screenshots, it appears in the “A Closer Look” section".

### Rule 6

Agents MUST allow for processing of an uploaded preview before it is
available. Apple lists the "Processing time" as "Up to 24 hours after
upload."

## Compliant Example

-   ✓ Two 25-second 886 x 1920 H.264 previews at 30 fps with stereo AAC audio,
    matching the portrait screenshots, for an iPhone with Dynamic Island
    display. (Rules 1–3, 5)

## Non-Compliant Example

-   ✗ A 45-second 60 fps preview. (Rule 2)
-   ✗ A landscape preview alongside portrait screenshots, expected to lead the
    screenshot row. (Rule 5)

## Dependencies

None.

## References

-   [App Store Connect Help — App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications)
