# Screenshot Specifications

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.screenshot-specifications
artifact_type: knowledge
title: Screenshot Specifications
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the App Store Connect screenshot specifications an agent must meet for iOS and iPadOS apps -- count, formats, required sizes, the scaling rule, alpha, and the iPhone Duo requirement.
domain: App Store Product Page
tags:
  - app-store-product-page
  - screenshots
  - specifications
  - iphone-duo
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
  - https://developer.apple.com/app-store/whats-new/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.asset-sequencing-and-story
last_updated: 2026-10-15
```

## Intent

This contract defines what App Store Connect accepts as a screenshot set for
an iOS or iPadOS app, so an agent producing or reviewing screenshots never
ships a size, count, or format the upload rejects.

## Scope

### Included

-   Count and file formats per device size
-   Required iPhone and iPad sizes
-   The scaling rule (highest required resolution)
-   Alpha channels
-   iPhone Duo sizes and the April 2027 requirement

### Excluded

-   What screenshots must depict (guideline 2.3.3) — see `screenshots-accuracy`
-   Mac, Apple TV, Apple Vision Pro and Apple Watch sizes — Excluded from v1;
    use the specification page directly
-   Device sizes other than those named here — the specification page is the
    only source; see Rule 7

## Rules

### Rule 1

Agents MUST provide at least one and at most 10 screenshots per device size,
in .jpeg, .jpg, or .png. "You must include at least one screenshot and can
upload up to 10 screenshots per device size in .jpeg, .jpg, or .png formats".

### Rule 2

Agents MUST include the required sizes: for iPhone, at least one screenshot
for "iPhone with Dynamic Island (medium display)" (1179 x 2556 or
1206 x 2622 portrait; 2556 x 1179 or 2622 x 1206 landscape); for an app that
supports iPadOS, at least one for "iPad 13-inch display" (2064 x 2752 or
2048 x 2732 portrait; 2752 x 2064 or 2732 x 2048 landscape).

### Rule 3

Agents MAY provide only the highest required resolution when the interface is
the same across device sizes and localizations. "If your app's user interface
is consistent across multiple device sizes and localizations, you only need to
provide screenshots for the highest required resolution."

### Rule 4

Agents MUST NOT upload screenshots with an alpha channel or transparency.
"Images can't include alpha channels or transparencies."

### Rule 5

Agents MUST provide iPhone Duo screenshots, starting April 2027, for any app
built with the iOS 27.1 SDK or later: outer display 1398 x 2034 or
2034 x 1398, inner display 2007 x 2853 or 2853 x 2007. "Starting in April
2027, screenshots will be required for any app using the iOS 27.1 SDK or
later."

### Rule 6

Agents SHOULD provide iPhone Duo screenshots for every iPhone app submitted
from April 2027, whatever its SDK. Apple's What's New page states the
requirement for "any apps or games submitted", which is broader than the
specification page's SDK condition in Rule 5; Rule 5 is the enforced minimum,
and this rule removes the risk of the broader reading.

### Rule 7

Agents MUST take any device size not named in this contract from the
specification page itself, and MUST NOT infer one from a device's display
resolution or aspect ratio.

## Compliant Example

-   ✓ An iPhone and iPad app uploads six 1206 x 2622 .png screenshots and
    six 2048 x 2732 .png screenshots, no alpha, and lets App Store Connect
    scale them down. (Rules 1–4)
-   ✓ An app built with the iOS 27.1 SDK adds 1398 x 2034 and
    2007 x 2853 iPhone Duo screenshots before April 2027. (Rule 5)

## Non-Compliant Example

-   ✗ Twelve screenshots for one device size, exported as transparent .png
    files. (Rules 1, 4)
-   ✗ An agent derives a 6.1-inch size from a phone's spec sheet instead of
    the specification page. (Rule 7)

## Dependencies

None.

## References

-   [App Store Connect Help — Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)
-   [App Store — What's New](https://developer.apple.com/app-store/whats-new/)
