---
name: human-interface-guidelines
description: Route Human Interface Guidelines (Foundations) design tasks to the correct Knowledge Contracts — layout, color, typography, dark mode, materials, motion, app icons, interface icons, images, branding, accessibility design, inclusion, privacy-design permission UI, SF Symbols usage, and right-to-left support. Use when designing or reviewing iOS/iPadOS UI, choosing colors or fonts, laying out a screen, picking icons or symbols, supporting Dark Mode or RTL, or designing permission-request flows (design pattern, not the wording itself — see style-guide for wording). Triggers on HIG, human interface guidelines, layout, color, dark mode, typography, materials, Liquid Glass, motion, animation, app icon, interface icon, SF Symbols, branding, accent color, accessibility design, inclusive design, RTL, right-to-left, permission prompt design, safe area, Dynamic Type, image asset, inclusive design.
id: skill.human-interface-guidelines.foundations
title: Human Interface Guidelines — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Human Interface Guidelines
routes: [knowledge.human-interface-guidelines.accessibility, knowledge.human-interface-guidelines.app-icons, knowledge.human-interface-guidelines.branding, knowledge.human-interface-guidelines.color, knowledge.human-interface-guidelines.dark-mode, knowledge.human-interface-guidelines.icons, knowledge.human-interface-guidelines.images, knowledge.human-interface-guidelines.inclusion, knowledge.human-interface-guidelines.layout, knowledge.human-interface-guidelines.materials, knowledge.human-interface-guidelines.motion, knowledge.human-interface-guidelines.privacy, knowledge.human-interface-guidelines.right-to-left, knowledge.human-interface-guidelines.sf-symbols, knowledge.human-interface-guidelines.typography]
related:
  - skill.style-guide.writing
  - skill.human-interface-guidelines.components
  - skill.human-interface-guidelines.patterns
last_updated: 2026-07-31
---

# Human Interface Guidelines — Foundations Skill

## Purpose

Route iOS/iPadOS design-guidance tasks to the minimum required Human
Interface Guidelines Foundations Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/human-interface-guidelines/.

-   Visual identity, iconography assets -> branding.md, app-icons.md, icons.md, images.md
-   Color & appearance -> color.md, dark-mode.md
-   Layout & structure -> layout.md, right-to-left.md
-   Typography -> typography.md
-   Materials & motion -> materials.md, motion.md
-   Accessibility & inclusion (design-level) -> accessibility.md, inclusion.md
-   Privacy (design-level, permission-request UI patterns) -> privacy.md
-   Symbol design system -> sf-symbols.md

Never load more than the contracts relevant to the specific question.
For UI copy wording (not visual design), route to
`skill.style-guide.writing` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. For Components/Inputs topics (lists,
buttons, sheets, alerts, action sheets, navigation, tab bars, pickers,
toggles, text fields, menus, gestures), route to
`skill.human-interface-guidelines.components` instead. For Patterns
topics (onboarding, searching, settings, notifications, feedback,
undo/redo), route to `skill.human-interface-guidelines.patterns`
instead. Any other HIG Patterns, Components, or Inputs topic not
covered by those two sibling skills remains out of scope (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
