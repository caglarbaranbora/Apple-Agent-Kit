# Branding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.branding
type: knowledge
title: Branding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how an app's brand identity (voice, accent color, custom fonts, logo) appears in iOS/iPadOS UI without overriding platform conventions.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - branding
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/branding
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.typography
  - knowledge.style-guide.copyright-and-trademarks
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent expresses brand identity
in an iOS/iPadOS app — voice, accent color, custom fonts, logo
placement — while deferring to platform conventions and content.

## Scope

### Included

-   Brand voice/tone consistency (pointer to style-guide for exact wording)
-   Accent color usage
-   Custom font legibility/accessibility requirements
-   Logo placement restraint
-   Launch-screen branding restrictions
-   Apple trademark restrictions

### Excluded

-   Exact wording/copy rules — see style-guide domain
-   Color palette mechanics — see `color`
-   Font legibility/Dynamic Type mechanics — see `typography`

## Rules

### Rule 1

Agents SHOULD express brand voice/tone consistently in written copy
(defer exact wording rules to the `style-guide` domain).

### Rule 2

Agents MAY specify an app accent color applied to interface icons,
buttons, and text.

### Rule 3

If a custom font is used, agents MUST ensure it remains legible at all
sizes and supports Bold Text / Dynamic Type accessibility features.

### Rule 4

Agents MUST NOT use screen space purely to display a brand asset
(logo) at the expense of content and controls people care about.

### Rule 5

Agents MUST NOT use the launch screen as a branding surface. A
welcome/onboarding screen shown after launch is acceptable; the launch
screen itself is not.

### Rule 6

Agents MUST NOT display Apple trademarks in the app name or images.

## Compliant Example

-   ✓ Custom accent color applied to buttons and icons throughout the app. (Rule 2)
-   ✓ Logo appears once, in an About/Settings screen. (Rule 4)

## Non-Compliant Example

-   ✗ Logo repeated in every navigation bar as a persistent header element. (Rule 4)
-   ✗ Launch screen decorated with marketing copy and animation. (Rule 5)
-   ✗ Custom font ships with no Bold Text / Dynamic Type support. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Branding](https://developer.apple.com/design/human-interface-guidelines/branding)
