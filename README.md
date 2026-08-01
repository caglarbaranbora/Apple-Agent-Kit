# Apple Agent Kit

Status: Draft
Version: 0.1.0

## Overview

Apple Agent Kit is a source-available, spec-first knowledge system for AI coding agents developing Apple platform applications.

The project transforms official Apple documentation into small, atomic Knowledge Contracts that can be deterministically routed through Skills instead of relying on repository-wide semantic search.

## Why

AI coding agents working on Apple platform apps tend to either hallucinate platform conventions or burn tokens re-reading entire doc sets on every task. Apple Agent Kit exists to fix both: it pre-digests official Apple documentation into small, atomic, traceable Knowledge Contracts, and routes an agent to exactly the ones a task needs via deterministic Skills — not semantic search over the whole repo. The result is lower token cost per task, more consistent output across sessions, and a clear paper trail back to the Apple documentation that justifies each rule.

## Goals

- Reduce token usage
- Improve routing accuracy
- Increase implementation consistency
- Preserve traceability to Apple documentation
- Scale to hundreds of reusable Knowledge Contracts

## Installation

Install the Claude Code plugin via the npx installer:

```bash
npx apple-agent-kit
```

This adds this repository as a Claude Code plugin marketplace and installs the `apple-agent-kit` plugin, so its Skills, Knowledge Contracts, and routing become available inside Claude Code sessions. Requires the `claude` CLI to already be installed.

## Architecture

Apple Documentation
↓
References
↓
Knowledge Contracts
↓
Skills
↓
Workflows

## Skills

Skills route a task to the minimum set of Knowledge Contracts it needs. Invoke them with a specific task, not a broad topic request — name the concrete thing you're doing (e.g. "check this screen's layout against HIG"), not "tell me about HIG."

- **`authentication`** — Routes sign-in, sign-up, credential, and biometric implementation tasks to Authentication Knowledge Contracts.
  Example: `"add a Face ID unlock option to my login screen"` → `knowledge.authentication.authentication`, `knowledge.authentication.accessibility-forms`

- **`style-guide`** — Routes UI copy and wording tasks (button labels, error text, capitalization, punctuation, inclusive writing, formatting) to Style Guide Knowledge Contracts.
  Example: `"what's the correct label for a destructive delete button"` → `general-button-labels.md`

- **`human-interface-guidelines`** — Routes iOS/iPadOS visual design tasks (layout, color, typography, dark mode, materials, motion, icons, branding, accessibility-design, privacy UI, RTL) to HIG Foundations Knowledge Contracts.
  Example: `"check this screen's layout against HIG"` → `layout.md` (+ `right-to-left.md` if relevant)
  Example: `"does my dark mode palette meet contrast guidance"` → `dark-mode.md`, `color.md`

- **`app-store-review-guidelines`** — Routes App Store submission-compliance tasks (app completeness, metadata accuracy, in-app purchase, spam/duplicate-app avoidance, privacy manifest and nutrition label accuracy) to App Store Review Guidelines Knowledge Contracts.
  Example: `"why would this in-app subscription get rejected"` → `digital-goods-iap.md`, `restore-purchases.md`
  Example: `"what needs to go in my PrivacyInfo.xcprivacy"` → `privacy-manifest.md`

- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`

- **`accessibility`** — Routes Accessibility API implementation tasks (labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion/Transparency/Increase Contrast, Full Keyboard Access, hidden/decorative elements, accessibility audits) to Accessibility Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this icon-only button has no VoiceOver label"` → `accessibility-labels.md`
  Example: `"swipe-to-delete row needs a VoiceOver alternative"` → `custom-accessibility-actions.md`

- **`uikit`** — Routes UIKit screen-scaffolding implementation tasks (view controller lifecycle/composition, programmatic Auto Layout, navigation, diffable table/collection views, modal presentation) to UIKit Knowledge Contracts.
  Example: `"my child view controller's view isn't showing up correctly"` → `view-controller-composition.md`
  Example: `"how do I animate row insertion in a UITableView"` → `table-view-diffable.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).

## What's New

- 2026-08-01 — Added `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation; programmatic UI v1) — 12 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contracts. Resolves the human-interface-guidelines and swiftui accessibility forward-references.
- 2026-08-01 — Added `swiftui` Skill (Views: composition/identity/modifier order; Navigation: NavigationStack/NavigationSplitView; Layout: stacks/safe-area/lazy-grids/GeometryReader; State: @State/@Binding/@Observable/@Environment) — 12 Knowledge Contracts.
- 2026-07-31 — Added `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contracts.
- 2026-07-31 — Added `human-interface-guidelines` Skill (Foundations: layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL) — 15 Knowledge Contracts.
- 2026-07-31 — Hardened native Skill format (real YAML frontmatter, deterministic keyword routing, Stop Conditions) across all Skills.
- 2026-07-31 — Added `authentication` Skill (sign-in, sign-up, credentials, biometrics).
- 2026-07-31 — Added `style-guide` Skill (terminology, capitalization, punctuation, inclusive writing).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
