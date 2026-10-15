# Image Asset Design

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.image-asset-design
artifact_type: knowledge
title: Image Asset Design
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable design guidance for App Store image assets -- centered focal point and safe area against clipping, previewing in App Store Connect, short text that adds to the visual, and localized text.
domain: App Store Product Page
tags:
  - app-store-product-page
  - images
  - design
  - localization
references:
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.video-asset-design
  - knowledge.app-store-product-page.header-and-search-result-messaging
last_updated: 2026-10-15
```

## Intent

This contract defines how to compose an App Store image — screenshot or image
creative asset — so it survives cropping on every device and reads in every
language the app supports.

## Scope

### Included

-   Focal point, safe area, clipping
-   App Store Connect Preview tool
-   Text length and role; text localization

### Excluded

-   Video assets — see `video-asset-design`
-   Subjective guidance ("Choose compelling visuals") — Excluded; not checkable

## Rules

### Rule 1

Agents SHOULD keep key elements inside a safe area and the focal point in the
center of the composition. "Design key elements with a safe area in mind to
accommodate different devices and orientations. Be sure your focal point
artwork is within the center of your composition to prevent any unwanted
clipping."

### Rule 2

Agents SHOULD check the result in App Store Connect's Preview tool before
submitting. "You can use the Preview tool in App Store Connect…"

### Rule 3

Agents SHOULD limit image text to a short phrase that adds to the visual
rather than describes it. "…use a short phrase that enhances your visual
rather than describes it."

### Rule 4

Agents SHOULD localize image text into every language the app supports. "Be
sure to localize for all languages your app supports."

## Compliant Example

-   ✓ A header with the subject centered, the headline well inside the safe
    area, and German and Japanese variants of the headline. (Rules 1, 4)

## Non-Compliant Example

-   ✗ A product shot pushed to the right edge, clipped on iPhone. (Rule 1)
-   ✗ The caption "This screenshot shows the timer screen" over the timer
    screen. (Rule 3)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
