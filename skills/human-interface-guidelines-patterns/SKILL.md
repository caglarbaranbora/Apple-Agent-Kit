---
name: human-interface-guidelines-patterns
description: Route Human Interface Guidelines Patterns design tasks to the correct Knowledge Contracts -- onboarding, searching, settings, notifications, feedback, and undo/redo. Use when designing or reviewing an iOS/iPadOS first-run flow, in-app search placement, settings-screen structure, notification content/timing, status/error feedback, or undo/redo affordances. This is design-level guidance, not implementation code -- for UserNotifications/UIKit/SwiftUI implementation see the respective implementation domain; for copy wording see style-guide. Triggers on onboarding, first-run experience, searching, search UI, settings screen, notification design, feedback, error feedback, undo, redo, HIG patterns.
id: skill.human-interface-guidelines.patterns
title: Human Interface Guidelines — Patterns
version: 0.1.0
status: Draft
artifact_type: skill
domain: Human Interface Guidelines
routes: [knowledge.human-interface-guidelines.onboarding, knowledge.human-interface-guidelines.searching, knowledge.human-interface-guidelines.settings, knowledge.human-interface-guidelines.notifications, knowledge.human-interface-guidelines.feedback, knowledge.human-interface-guidelines.undo-and-redo]
related:
  - skill.human-interface-guidelines.foundations
  - skill.human-interface-guidelines.components
  - skill.style-guide.writing
last_updated: 2026-08-06
---

# Human Interface Guidelines — Patterns Skill

## Purpose

Route iOS/iPadOS Patterns design-guidance tasks to the minimum
required Human Interface Guidelines Knowledge Contracts. v1 scope is a
curated 6-topic subset of HIG Patterns, not the full section.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/human-interface-guidelines/.

-   First-run flow -> onboarding.md
-   Search UI -> searching.md
-   Settings screen structure -> settings.md
-   Notification design -> notifications.md
-   System/status feedback -> feedback.md
-   Undo/redo affordances -> undo-and-redo.md

Never load more than the contracts relevant to the specific question.
For pattern copy/wording, route to `skill.style-guide.writing` instead.
Notification *design* is covered here; the UserNotifications API
belongs to a future Tier 2 domain, not yet built.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. Foundations topics route to
`skill.human-interface-guidelines.foundations`; Components/Inputs
topics route to `skill.human-interface-guidelines.components`. Any
other HIG Patterns topic (e.g. Charts, Drag and Drop, Entering Data,
Full-Screen Experiences, Launching, Loading, Managing Accounts,
Modality, Multitasking, Playing Audio, Printing, Ratings and Reviews,
Sharing, Status, Syncing, Workouts) is out of scope (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
