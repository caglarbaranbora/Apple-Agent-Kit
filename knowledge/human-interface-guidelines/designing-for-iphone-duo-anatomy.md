# Designing for iPhone Duo — Anatomy

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.designing-for-iphone-duo-anatomy
artifact_type: knowledge
title: Designing for iPhone Duo — Anatomy
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the hardware facts an AI coding agent must design against for iPhone Duo — dual displays, hinge/device poses, and the three reserved regions — and the size-class-based approach to supporting them.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - designing-for-iphone-duo
  - foldable
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo
depends_on: []
related:
  - knowledge.human-interface-guidelines.designing-for-iphone-duo-layout
  - knowledge.human-interface-guidelines.designing-for-iphone-duo-vertical-controls
  - knowledge.human-interface-guidelines.layout
last_updated: 2026-09-10
```

## Intent

This contract defines the hardware model an AI coding agent must design
against for iPhone Duo — a foldable iPhone with an inner and outer
display joined by a hinge — so that pose-handling and reserved-region
decisions in the sibling layout/vertical-controls contracts rest on
correct assumptions rather than treating Duo as a same-shape iPhone or
a miniature iPad.

## Scope

### Included

-   Inner/outer display anatomy and the front-facing camera per display
-   Device poses (book-fold, surface-set, edge-standing) and why size
    classes — not per-pose custom layouts — are the answer
-   The three reserved regions: outer camera, inner camera, folding
    region
-   That Duo is still iPhone: Designing for iOS patterns still apply

### Excluded

-   Adaptive layout construction (split views, arrangement views,
    dynamic resizing) — see `designing-for-iphone-duo-layout`
-   Toolbar/tab bar vertical-axis placement — see
    `designing-for-iphone-duo-vertical-controls`
-   SwiftUI/UIKit reserved-region API implementation — see `swiftui`/
    `uikit` domains

## Rules

### Rule 1

Agents MUST treat iPhone Duo as iPhone, not a new platform: apply
Designing for iOS patterns and best practices by default, and special-case
only what this domain's Duo contracts explicitly call out. "Although
iPhone Duo is a new form factor, keep in mind that you're still
designing for iPhone, and Designing for iOS patterns and best practices
still apply."

### Rule 2

Agents MUST design the inner and outer display as one continuous
experience — the same app, not two apps — since people move between
them as the device opens and closes. "An app designed for iPhone Duo
adapts seamlessly to both displays, providing a continuous experience
as the device opens and closes."

### Rule 3

Agents MUST support Duo's device poses (partially folded like a book,
placed on a surface, standing on an edge) through size classes, not a
custom layout per pose: a compact-width layout for the outer display
and a regular-width layout for the inner display are the fundamentals
that cover every pose. "Supporting the device's various poses doesn't
mean designing a custom layout for each one: instead, use size classes
so your app adapts naturally as it changes size."

### Rule 4

Agents MUST account for three reserved regions when placing content:
the outer front-facing camera (always present; expands into the
Dynamic Island for Live Activities), the inner front-facing camera
(present only while the camera is active), and the folding region
(present only while partially open; divides the inner display,
excluding the center). "The reserved regions on iPhone Duo include: The
outer front-facing camera... The inner front-facing camera... The
folding region."

### Rule 5

Agents SHOULD rely on standard system components (alerts, context
menus, sheets, split views) for automatic reserved-region avoidance,
and reach for the reserved-region APIs only when building a custom
component the system can't adapt for them. "Many system components
automatically adapt to reserved regions... For custom components, the
reserved region APIs provide a way to reposition content away from
reserved regions."

## Compliant Example

-   ✓ A screen ships one layout driven by size classes (compact/outer,
    regular/inner) instead of three hand-built layouts for
    book/surface/edge poses. (Rule 3)
-   ✓ A custom full-bleed header calls the reserved-region API to clear
    the folding region only while the device is partially open. (Rule 4,
    Rule 5)

## Non-Compliant Example

-   ✗ The app ships a distinct hand-built layout for every device pose
    instead of one size-class-driven layout. (Rule 3)
-   ✗ Custom content is drawn under the outer camera's region and gets
    clipped by the Dynamic Island. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
