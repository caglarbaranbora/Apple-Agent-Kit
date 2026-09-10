# Branding

Status: Approved Version: 1.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.branding
artifact_type: knowledge
title: Branding
version: 1.1.0
status: Approved
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
  - knowledge.human-interface-guidelines.materials
  - knowledge.style-guide.copyright-and-trademarks
last_updated: 2026-09-10
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

Agents MUST apply the app's accent color judiciously rather than
broadly — spreading it across most controls overwhelms the interface
and dilutes its impact. Agents SHOULD minimize accent-color use on
controls, reserving it for primary actions or status indicators (e.g.,
an unread-content badge, the selected tab bar icon), and SHOULD prefer
expressing brand color in the content layer, where it scrolls beneath
Liquid Glass controls and is picked up dynamically, over tinting
controls directly. "Apply your app's accent color judiciously. Using
your brand color too broadly can overwhelm your interface and dilute
its impact. Minimize its use on controls and instead use it
intentionally for primary actions or status indicators... To express
your brand through color, consider moving it into the content layer,
where it scrolls beneath Liquid Glass controls and gets picked up
dynamically."

### Rule 3

If a custom font is used, agents MUST follow the Dynamic Type / Bold
Text accessibility requirements defined in `typography` Rule 5 —
branding does not define separate font-accessibility rules.

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

-   ✓ Accent color is reserved for the selected tab bar icon and unread-content badges, while most buttons and icons use the system tint. (Rule 2)
-   ✓ Logo appears once, in an About/Settings screen. (Rule 4)

## Non-Compliant Example

-   ✗ Accent color is applied broadly across every button, icon, and text element instead of reserved for primary actions/status indicators. (Rule 2)
-   ✗ Logo repeated in every navigation bar as a persistent header element. (Rule 4)
-   ✗ Launch screen decorated with marketing copy and animation. (Rule 5)
-   ✗ Custom font ships with no Bold Text / Dynamic Type support. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Branding](https://developer.apple.com/design/human-interface-guidelines/branding)
