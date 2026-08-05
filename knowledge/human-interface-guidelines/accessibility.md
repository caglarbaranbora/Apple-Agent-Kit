# Accessibility (Design)

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.accessibility
type: knowledge
title: Accessibility (Design)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design-level accessibility requirements for iOS/iPadOS interfaces — text scaling, contrast, VoiceOver labeling, alternatives to gesture and color-only cues.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - accessibility
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/accessibility
depends_on: []
related:
  - knowledge.accessibility.accessibility-labels
  - knowledge.accessibility.dynamic-type-api
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.inclusion
  - knowledge.human-interface-guidelines.typography
  - knowledge.style-guide.writing-inclusively
updated: 2026-08-05
```

## Intent

This contract defines the design-level accessibility rules an AI coding
agent must apply when laying out or reviewing an iOS/iPadOS interface —
text scaling, contrast, labeling, and non-visual/non-gesture
alternatives. It covers design decisions, not Accessibility API
implementation (VoiceOver traits, UIAccessibility properties), which
belongs to the `accessibility` domain (see
docs/architecture/domain-map.md Cross-Domain Notes).

## Scope

### Included

-   Dynamic Type / text-scaling support in layout
-   Minimum color-contrast requirements
-   Not conveying information through color alone
-   Accessibility labels for custom icon-only controls
-   Alternatives to custom gestures
-   Avoiding time-boxed auto-dismissing UI

### Excluded

-   Accessibility API implementation details (VoiceOver traits, UIAccessibility, Dynamic Type API) — see `knowledge.accessibility.accessibility-labels`, `knowledge.accessibility.dynamic-type-api`
-   Inclusive language/imagery — see `inclusion`
-   Color palette definition — see `color`

## Rules

### Rule 1

Agents MUST ensure text can scale via Dynamic Type to at least 200%
without loss of critical content. Ensuring the surrounding layout
doesn't break or truncate at those larger sizes is covered by
`layout` Rule 2.

### Rule 2

Agents MUST ensure a minimum 4.5:1 contrast ratio between foreground
text/icons and their background; prefer system-defined colors, which
provide accessible variants automatically (see also `dark-mode` Rule
3 for appearance-specific and small-text contrast targets).

### Rule 3

Agents MUST NOT convey status, state, or differentiation using color
alone — pair color with a text label, icon, or shape.

### Rule 4

Agents MUST provide a meaningful accessibility label for every
custom icon-only control so VoiceOver can announce its purpose (see
also `icons` Rule 4 for interface-icon-specific guidance).

### Rule 5

Agents SHOULD provide a non-gesture alternative for any custom
gesture-based interaction (e.g., a visible button alongside a
swipe-to-dismiss action).

### Rule 6

Agents SHOULD avoid time-boxed UI elements that auto-dismiss on a
timer; prefer an explicit dismissal action instead.

## Compliant Example

-   ✓ An icon-only delete button has accessibility label "Delete." (Rule 4)
-   ✓ Success/failure state shown with both a color change and a checkmark/X icon. (Rule 3)
-   ✓ Body text reflows without truncation at the largest Dynamic Type size. (Rule 1)

## Non-Compliant Example

-   ✗ Icon-only button with no accessibility label — VoiceOver reads only "button." (Rule 4)
-   ✗ Success/failure indicated by a red or green dot alone. (Rule 3)
-   ✗ Fixed-size label that truncates at larger accessibility text sizes. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
