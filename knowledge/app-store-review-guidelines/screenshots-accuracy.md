# Screenshots Accuracy

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.screenshots-accuracy
artifact_type: knowledge
title: Screenshots Accuracy
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines what App Store screenshots and preview videos must and must not depict, per guideline 2.3.3 and 2.3.4.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - screenshots
  - metadata
  - previews
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.3
depends_on: []
related:
  - knowledge.app-store-review-guidelines.description-accuracy
last_updated: 2026-08-08
```

## Intent

This contract defines what App Store screenshots and App Preview videos
must show: the app in actual use, not marketing art or unrelated
footage (guideline 2.3.3, 2.3.4).

## Scope

### Included

-   Screenshot content requirements (in-app-use vs. title/login/splash art)
-   Permitted overlays on screenshots
-   App Preview video source-material restrictions
-   Permitted narration/overlays on preview videos

### Excluded

-   App description/keyword accuracy — see `description-accuracy`

## Rules

### Rule 1

Agents MUST ensure screenshots show the app in actual use — not merely
title art, a login page, or a splash screen.

### Rule 2

Agents MAY include text/image overlays on screenshots that demonstrate
input mechanisms (e.g., an animated touch point, Apple Pencil) or
extended on-device functionality (e.g., Touch Bar).

### Rule 3

Agents MUST limit App Preview videos to screen captures of the app
itself; Stickers/iMessage extensions may additionally show the Messages
app experience.

### Rule 4

Agents MAY add narration or textual/video overlays to preview videos to
clarify content not obvious from the video alone.

## Compliant Example

-   ✓ Screenshots show real in-app screens with actual content, with one overlay demonstrating a swipe gesture. (Rules 1, 2)

## Non-Compliant Example

-   ✗ All screenshots are variations of the app's logo splash screen. (Rule 1)
-   ✗ Preview video is a marketing reel with stock footage unrelated to the app UI. (Rule 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3 Accurate Metadata](https://developer.apple.com/app-store/review/guidelines/#2.3.3)
