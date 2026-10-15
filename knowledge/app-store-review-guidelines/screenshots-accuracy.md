# Screenshots Accuracy

Status: Approved Version: 1.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.screenshots-accuracy
artifact_type: knowledge
title: Screenshots Accuracy
version: 1.1.0
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
  - https://developer.apple.com/app-store/review/guidelines/#2.3.4
  - https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
depends_on: []
related:
  - knowledge.app-store-review-guidelines.description-accuracy
  - knowledge.app-store-product-page.screenshot-specifications
  - knowledge.app-store-product-page.creative-assets
last_updated: 2026-10-15
```

## Intent

This contract defines what App Store screenshots and App Preview videos
must show: a majority of the app in actual use per device and
localization, and what App Preview videos may contain (guideline 2.3.3,
2.3.4).

## Scope

### Included

-   Screenshot content requirements (in-app-use vs. title/login/splash art)
-   The majority-in-use rule per device and localization
-   Permitted overlays on screenshots
-   Overlay and hardware-only limits
-   App Preview video source-material restrictions
-   Permitted narration/overlays on preview videos

### Excluded

-   App description/keyword accuracy — see `description-accuracy`
-   Creative assets (product page header, search results) — exempt from the
    in-use rule; see `creative-assets`
-   Screenshot sizes and counts — see `screenshot-specifications`

## Rules

### Rule 1

Agents MUST ensure that, for each supported device and each localization,
more than half of the screenshots show the app in use; the rest MAY show the
app's benefits with marketing material, splash screens, or marketing text. App
Review "will approve only those submissions where more than half of
screenshots show the app in use." One screenshot is enough when it shows the
app in use, and one image of the app in use MAY span several screenshots.

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

### Rule 5

Agents MUST NOT let overlays or marketing visuals crowd out the app, and MUST
NOT submit a screenshot that shows only hardware, or an overlay with no app
interface behind it. "Don't let overlays or marketing visuals crowd out your
app." "Don't show only the hardware or an overlay with no app interface behind
it."

### Rule 6

Agents SHOULD update screenshots with each new version so they match the
current interface. "Update your screenshots with each new version so they
match the current user interface."

## Compliant Example

-   ✓ Screenshots show real in-app screens with actual content, with one overlay demonstrating a swipe gesture. (Rules 1, 2)
-   ✓ Four screenshots per device: three show real app screens, the fourth is a marketing panel. (Rule 1)

## Non-Compliant Example

-   ✗ Four screenshots per device, two of them marketing panels with no app UI — exactly half, not more than half, show the app. (Rule 1)
-   ✗ A screenshot of the bare device frame with a tagline. (Rule 5)
-   ✗ Preview video is a marketing reel with stock footage unrelated to the app UI. (Rule 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3 Accurate Metadata](https://developer.apple.com/app-store/review/guidelines/#2.3.3)
-   [Apple App Review Guidelines — 2.3.4](https://developer.apple.com/app-store/review/guidelines/#2.3.4)
-   [App Review — Guideline 2.3.3 Screenshots](https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots)
