---
name: accessibility
description: Route Accessibility API implementation tasks to the correct Knowledge Contracts — accessibility labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion, Reduce Transparency/Increase Contrast, Full Keyboard Access and accessibility focus, hidden/decorative elements, and accessibility audits. Use when writing or reviewing VoiceOver support, custom-control accessibility, Dynamic Type handling, or accessibility test coverage in SwiftUI or UIKit. This is API-implementation guidance, not visual design — for the underlying design requirement (contrast ratio, text-scaling requirement, color-alone prohibition), see human-interface-guidelines. Triggers on VoiceOver, accessibilityLabel, accessibilityTraits, accessibilityValue, accessibilityHint, accessibilityAction, UIAccessibilityCustomAction, accessibilityElement, isAccessibilityElement, accessibilitySortPriority, Dynamic Type, ScaledMetric, UIFontMetrics, Reduce Motion, Reduce Transparency, Increase Contrast, Full Keyboard Access, AccessibilityFocusState, accessibilityHidden, performAccessibilityAudit, Accessibility Inspector.
id: skill.accessibility.foundations
title: Accessibility — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Accessibility
routes: [knowledge.accessibility.accessibility-labels, knowledge.accessibility.accessibility-traits, knowledge.accessibility.accessibility-value-and-hint, knowledge.accessibility.custom-accessibility-actions, knowledge.accessibility.accessibility-element-grouping, knowledge.accessibility.voiceover-navigation-order, knowledge.accessibility.dynamic-type-api, knowledge.accessibility.reduce-motion, knowledge.accessibility.reduce-transparency-increase-contrast, knowledge.accessibility.full-keyboard-access-and-focus, knowledge.accessibility.accessibility-hidden-decorative, knowledge.accessibility.accessibility-audits-testing]
related:
  - skill.human-interface-guidelines.foundations
  - skill.swiftui.foundations
last_updated: 2026-08-01
---

# Accessibility — Foundations Skill

## Purpose

Route Accessibility API implementation tasks to the minimum required
Accessibility Knowledge Contracts, across both SwiftUI and UIKit.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/accessibility/.

-   Labeling & description -> accessibility-labels.md, accessibility-traits.md, accessibility-value-and-hint.md
-   Interaction -> custom-accessibility-actions.md, full-keyboard-access-and-focus.md
-   Structure & navigation -> accessibility-element-grouping.md, voiceover-navigation-order.md, accessibility-hidden-decorative.md
-   User preferences -> dynamic-type-api.md, reduce-motion.md, reduce-transparency-increase-contrast.md
-   Verification -> accessibility-audits-testing.md

Never load more than the contracts relevant to the specific question.
For the underlying design requirement (why a 4.5:1 contrast ratio, why
text must scale to 200%, why color can't be the only differentiator),
route to `skill.human-interface-guidelines.foundations` instead. For
SwiftUI view/state/navigation questions unrelated to accessibility,
route to `skill.swiftui.foundations` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/accessibility/ — do not guess or fall back to
general knowledge. Design-level accessibility guidance (owned by
`human-interface-guidelines`) and general XCTest/Swift Testing/UI-testing
conventions beyond accessibility audits (owned by a future `testing`
domain) are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
