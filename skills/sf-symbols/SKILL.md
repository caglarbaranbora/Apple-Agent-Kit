---
name: sf-symbols
description: Route SF Symbols API implementation tasks to the correct Knowledge Contracts — symbol basics (Image(systemName:)/UIImage(systemName:)), rendering modes, symbol variants, variable value symbols, weight/scale, color/tinting mechanics, custom symbol usage, and UIKit SymbolConfiguration composition. Use when writing or reviewing code that renders, styles, or configures an SF Symbol in SwiftUI or UIKit. v1 excludes symbol effects/animations (SymbolEffect) and Symbol Composer/custom symbol authoring. Design-level symbol selection (which symbol, which color, as a design decision) is out of scope here — see the human-interface-guidelines skill. Triggers on SF Symbols, Image(systemName:), UIImage(systemName:), symbolRenderingMode, SymbolVariants, variableValue, imageScale, fontWeight on a symbol, SymbolConfiguration, preferredSymbolConfiguration, withConfiguration, hierarchical rendering, palette rendering, multicolor rendering.
id: skill.sf-symbols.foundations
title: SF Symbols — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: SF Symbols
routes: [knowledge.sf-symbols.symbol-basics, knowledge.sf-symbols.rendering-modes, knowledge.sf-symbols.symbol-variants, knowledge.sf-symbols.variable-value-symbols, knowledge.sf-symbols.symbol-weight-and-scale, knowledge.sf-symbols.symbol-color-and-tinting, knowledge.sf-symbols.custom-symbol-usage, knowledge.sf-symbols.uikit-symbol-configuration]
related:
  - skill.human-interface-guidelines.foundations
  - skill.swiftui.foundations
  - skill.uikit.foundations
last_updated: 2026-08-08
---

# SF Symbols — Foundations Skill

## Purpose

Route SF Symbols API implementation tasks to the minimum required SF
Symbols Knowledge Contracts. v1 scope is core rendering, rendering
modes, variants, variable value, weight/scale, color/tinting, custom
symbol usage, and UIKit `SymbolConfiguration` composition — across
SwiftUI and UIKit.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/sf-symbols/.

-   Usage -> symbol-basics.md, custom-symbol-usage.md
-   Rendering -> rendering-modes.md, symbol-variants.md, variable-value-symbols.md, symbol-weight-and-scale.md, symbol-color-and-tinting.md
-   UIKit-specific -> uikit-symbol-configuration.md

Never load more than the contracts relevant to the specific question.
For which symbol to choose, which color fits a design, or fill vs.
outline as a design decision, route to
`skill.human-interface-guidelines.foundations` instead. For view
composition/state/navigation questions unrelated to symbol rendering
itself, route to `skill.swiftui.foundations` or `skill.uikit.foundations`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/sf-symbols/ — do not guess or fall back to general
knowledge.

-   Symbol effects/animations (`SymbolEffect`, `.bounce`, `.pulse`,
    `.variableColor`) — Excluded
-   Symbol Composer / custom symbol authoring — Excluded
