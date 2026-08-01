---
name: uikit
description: Route UIKit screen-scaffolding implementation tasks to the correct Knowledge Contracts — view controller lifecycle and composition, programmatic Auto Layout (constraints, stack views, safe area), navigation (UINavigationController, UITabBarController, modal presentation), and diffable table/collection views. Use when writing or reviewing UIKit screens, layout code, navigation flow, or list/grid UI. v1 is programmatic UI only (no Storyboard/XIB) and diffable data sources only (no classic cellForRowAt). Accessibility API implementation is out of scope here — see the accessibility skill. Triggers on UIViewController, viewDidLoad, viewWillAppear, addChild, NSLayoutConstraint, layout anchors, UIStackView, safeAreaLayoutGuide, UINavigationController, UITabBarController, UITableViewDiffableDataSource, UICollectionViewCompositionalLayout, UICollectionViewDiffableDataSource, CellRegistration, prepareForReuse, present, dismiss, UIModalPresentationStyle.
id: skill.uikit.foundations
title: UIKit — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: UIKit
routes: [knowledge.uikit.view-controller-lifecycle, knowledge.uikit.view-controller-composition, knowledge.uikit.auto-layout-constraints, knowledge.uikit.auto-layout-stack-views, knowledge.uikit.safe-area-and-layout-guides, knowledge.uikit.navigation-controller, knowledge.uikit.tab-bar-controller, knowledge.uikit.table-view-diffable, knowledge.uikit.collection-view-compositional-layout, knowledge.uikit.collection-view-diffable, knowledge.uikit.cell-configuration, knowledge.uikit.modal-presentation]
related:
  - skill.accessibility.foundations
  - skill.swiftui.foundations
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-01
---

# UIKit — Foundations Skill

## Purpose

Route UIKit screen-scaffolding implementation tasks to the minimum
required UIKit Knowledge Contracts. v1 scope is programmatic UI only (no
Storyboard/XIB) and diffable data sources only (no classic
`cellForRowAt`).

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/uikit/.

-   Screen lifecycle & composition -> view-controller-lifecycle.md, view-controller-composition.md
-   Layout -> auto-layout-constraints.md, auto-layout-stack-views.md, safe-area-and-layout-guides.md
-   Navigation & presentation -> navigation-controller.md, tab-bar-controller.md, modal-presentation.md
-   Lists & grids -> table-view-diffable.md, collection-view-compositional-layout.md, collection-view-diffable.md, cell-configuration.md

Never load more than the contracts relevant to the specific question.
For accessibility API tasks (accessibilityLabel, traits, VoiceOver,
Dynamic Type, etc.), route to `skill.accessibility.foundations` instead.
For SwiftUI view/state/navigation tasks, route to
`skill.swiftui.foundations` instead. For design-level guidance (when to
use a tab bar vs. a navigation stack, list vs. grid layout choice), route
to `skill.human-interface-guidelines.foundations` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/uikit/ — do not guess or fall back to general
knowledge. Storyboard/XIB and `IBOutlet`/`IBAction` workflow are
permanently out of scope for this domain. Gesture recognizers, Core
Animation/CALayer, custom transitions, and UIKit-SwiftUI interop
(`UIHostingController`/`UIViewRepresentable`) are deferred to future
scope, not yet built — report that explicitly rather than answering from
general knowledge (see docs/architecture/domain-map.md).
