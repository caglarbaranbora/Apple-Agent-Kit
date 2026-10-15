# Video Asset Design

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.video-asset-design
artifact_type: knowledge
title: Video Asset Design
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable design guidance for App Store videos -- setting the poster frame before approval, leading with the value proposition, avoiding quick cuts, looping seamlessly, working without sound, and telling a complete story.
domain: App Store Product Page
tags:
  - app-store-product-page
  - video
  - app-previews
  - design
references:
  - https://developer.apple.com/app-store/asset-best-practices/
  - https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
  - https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
depends_on: []
related:
  - knowledge.app-store-product-page.app-preview-specifications
  - knowledge.app-store-product-page.creative-assets
  - knowledge.app-store-product-page.image-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines how to cut an App Store video — app preview or video
creative asset — for a placement that autoplays, loops, and starts muted.

## Scope

### Included

-   Poster frame
-   Opening, pacing, looping
-   Audio
-   Story structure of an app preview

### Excluded

-   Encoding, length, resolution — see `app-preview-specifications` and
    `creative-assets`; In-App Event video specifications — see
    `in-app-event-media`
-   Subjective guidance ("Consider compelling visuals") — Excluded; not checkable

## Rules

### Rule 1

Agents MUST explicitly set the poster frame before the asset is approved:
it is "the first image someone sees before your video plays", an app preview
defaults to the frame at 5 seconds, and "Poster frames can't be edited after
assets have been approved."

### Rule 2

Agents SHOULD open with the value proposition or the strongest feature. "Start
strong. Lead with your value proposition or most compelling feature."

### Rule 3

Agents SHOULD avoid quick cuts and fast motion. "Avoid quick cuts and
fast-moving visuals, as these can be difficult for people to follow and may
not be accessible for everyone."

### Rule 4

Agents SHOULD make the last frame flow into the first. "Loop seamlessly.
Videos autoplay and repeat…"

### Rule 5

Agents SHOULD make the video understandable with the sound off, and keep any
audio a short, clean-looping music bed without sudden loud moments. "In most
cases, audio is muted by default, so your creative must work silently first. …
Favor a short music loop over heavy sound effects, avoid sudden loud moments,
and ensure the audio loops cleanly".

### Rule 6

Agents SHOULD give each app preview a beginning, middle, and end. "Tell a
complete story. Consider having a beginning, middle, and end…"

## Compliant Example

-   ✓ A preview that opens on the core feature, holds each shot for several
    seconds, carries captions, and ends where it began. (Rules 2–5)
-   ✓ An app preview that shows a task being set up, performed, and completed.
    (Rule 6)

## Non-Compliant Example

-   ✗ A preview whose 5-second default poster frame is a blurred transition,
    left unchanged until after approval. (Rule 1)
-   ✗ An app preview cut at two cuts per second with the key message in voice-over
    only. (Rules 3, 5)
-   ✗ An app preview that is one unbroken screen recording with no start or
    finish. (Rule 6)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
-   [App Store Connect Help — Manage your App Store assets](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets)
-   [App Store Connect Help — App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications)
