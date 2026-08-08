---
name: human-interface-guidelines-components
description: Route Human Interface Guidelines Components/Inputs design tasks to the correct Knowledge Contracts -- lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, and touchscreen gestures. Use when designing or reviewing iOS/iPadOS list/table layout, button hierarchy, modal presentation (sheets/alerts/action sheets), navigation chrome, form controls, or touch gesture usage. This is design-level guidance, not implementation code -- for SwiftUI/UIKit component code see swiftui/uikit; for component label wording see style-guide. Triggers on lists and tables, buttons, sheets, alerts, action sheet, navigation bar, tab bar, pickers, toggles, text fields, menus, touchscreen gestures, HIG components.
id: skill.human-interface-guidelines.components
title: Human Interface Guidelines — Components
version: 1.0.0
status: Approved
artifact_type: skill
domain: Human Interface Guidelines
routes: [knowledge.human-interface-guidelines.lists-and-tables, knowledge.human-interface-guidelines.buttons, knowledge.human-interface-guidelines.sheets, knowledge.human-interface-guidelines.alerts, knowledge.human-interface-guidelines.action-sheets, knowledge.human-interface-guidelines.navigation-bars, knowledge.human-interface-guidelines.tab-bars, knowledge.human-interface-guidelines.pickers, knowledge.human-interface-guidelines.toggles, knowledge.human-interface-guidelines.text-fields, knowledge.human-interface-guidelines.menus, knowledge.human-interface-guidelines.touchscreen-gestures]
related:
  - skill.human-interface-guidelines.foundations
  - skill.human-interface-guidelines.patterns
  - skill.style-guide.writing
last_updated: 2026-08-08
---

# Human Interface Guidelines — Components Skill

## Purpose

Route iOS/iPadOS Components and Inputs design-guidance tasks to the
minimum required Human Interface Guidelines Knowledge Contracts. v1
scope is a curated subset — 11 Components topics plus 1 Inputs topic
(Touchscreen Gestures) — not the full HIG Components/Inputs sections.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/human-interface-guidelines/.

-   List/table structure -> lists-and-tables.md
-   Buttons and menu actions -> buttons.md, menus.md
-   Modal presentation -> sheets.md, alerts.md, action-sheets.md
-   Navigation chrome -> navigation-bars.md, tab-bars.md
-   Form/input controls -> pickers.md, toggles.md, text-fields.md
-   Touch gestures -> touchscreen-gestures.md

Never load more than the contracts relevant to the specific question.
For component label/copy wording, route to `skill.style-guide.writing`
instead. For SwiftUI/UIKit implementation code, route to the `swiftui`
or `uikit` Skill instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. Foundations topics (layout, color,
typography, etc.) route to `skill.human-interface-guidelines.foundations`;
Patterns topics (onboarding, searching, settings, notifications,
feedback, undo/redo) route to `skill.human-interface-guidelines.patterns`.
Any other HIG Components/Inputs topic (e.g. Column Views, Disclosure
Controls, Sliders, Steppers, Toolbars beyond the navigation-bar subset,
Popovers, Context Menus, Apple Pencil, Game Controllers, Keyboards) is
out of scope (see docs/architecture/domain-map.md) — report that
explicitly rather than answering from general knowledge.
