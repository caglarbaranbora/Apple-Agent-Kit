---
name: swiftui
description: Route SwiftUI implementation tasks to the correct Knowledge Contracts — view composition, view identity in ForEach/List, modifier order, NavigationStack/NavigationPath, NavigationSplitView, stack/spacing layout, safe area handling, lazy grids/stacks, GeometryReader pitfalls, @State/@Binding, the @Observable macro, and @Environment values. Use when writing or reviewing SwiftUI view code, structuring navigation, laying out a screen in code, choosing a state-management approach, or debugging view-identity/layout bugs. This is implementation-code guidance (iOS 17+), not visual design — for what a screen should look like, see human-interface-guidelines. Triggers on SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea.
id: skill.swiftui.foundations
title: SwiftUI — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: SwiftUI
routes: [knowledge.swiftui.view-composition, knowledge.swiftui.view-identity, knowledge.swiftui.modifier-order, knowledge.swiftui.navigation-stack, knowledge.swiftui.navigation-split-view, knowledge.swiftui.stacks-and-spacing, knowledge.swiftui.safe-area, knowledge.swiftui.lazy-grids, knowledge.swiftui.geometry-reader-anti-pattern, knowledge.swiftui.state-and-binding, knowledge.swiftui.observable-macro, knowledge.swiftui.environment-values]
related:
  - skill.human-interface-guidelines.foundations
  - skill.swiftui.interaction
last_updated: 2026-08-06
---

# SwiftUI — Foundations Skill

## Purpose

Route SwiftUI implementation-code tasks to the minimum required
SwiftUI Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/swiftui/.

-   Views -> view-composition.md, view-identity.md, modifier-order.md
-   Navigation -> navigation-stack.md, navigation-split-view.md
-   Layout -> stacks-and-spacing.md, safe-area.md, lazy-grids.md, geometry-reader-anti-pattern.md
-   State management -> state-and-binding.md, observable-macro.md, environment-values.md

Never load more than the contracts relevant to the specific question.
For visual/UX design guidance (what a screen should look like, not how
it's coded), route to `skill.human-interface-guidelines.foundations`
instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/swiftui/ — do not guess or fall back to general
knowledge. Animation and gesture questions route to
`skill.swiftui.interaction` instead of being reported as a gap.

-   Previews — Excluded
-   Custom `Layout` protocol conformances — Excluded
-   Legacy `ObservableObject`/`NavigationView` migration — Deferred
-   Accessibility APIs — owned by `accessibility`
