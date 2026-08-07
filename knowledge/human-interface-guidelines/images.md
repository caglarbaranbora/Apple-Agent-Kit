# Images

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.images
artifact_type: knowledge
title: Images
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for delivering bitmap image assets at the correct resolution and color profile across iOS/iPadOS devices.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - images
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/images
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.icons
last_updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent delivers bitmap image
assets for iOS/iPadOS — scale-factor variants, color profiles, and
device testing — so images render correctly across the full range of
display densities.

## Scope

### Included

-   @1x/@2x/@3x scale-factor asset delivery
-   Designing at low resolution and scaling up
-   Embedded color profiles
-   Wide-color (Display P3) usage
-   On-device testing of image assets

### Excluded

-   Color palette/profile selection rationale — see `color`
-   Vector interface icon format rules — see `icons`

## Rules

### Rule 1

Agents MUST provide @1x/@2x/@3x scale-factor variants (as applicable)
for every bitmap image asset, named accordingly in the asset catalog.

### Rule 2

Agents SHOULD design at the lowest resolution and scale up to produce
higher-resolution variants, aligning vector control points to whole
values at 1x.

### Rule 3

Agents MUST embed a color profile with each image so colors render
correctly across displays.

### Rule 4

Agents SHOULD use the Display P3 color profile for wide-color images
on compatible displays, exporting as PNG for lossless quality.

### Rule 5

Agents MUST test images on actual devices — an image that looks
correct at design time can appear pixelated or stretched on-device.

## Compliant Example

-   ✓ An image asset ships @1x/@2x/@3x variants with an embedded sRGB or P3 color profile as appropriate. (Rules 1, 3, 4)

## Non-Compliant Example

-   ✗ A single-resolution PNG is reused for all scale factors, appearing blurry on high-density displays. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Images](https://developer.apple.com/design/human-interface-guidelines/images)
