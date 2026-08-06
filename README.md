# Apple Agent Kit

[![npm version](https://img.shields.io/npm/v/apple-agent-kit)](https://www.npmjs.com/package/apple-agent-kit)
[![License](https://img.shields.io/badge/license-PolyForm%20Strict-blue)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-CHANGELOG.md-blue)](CHANGELOG.md)

Status: Stable
Version: 1.0.2

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

- **`human-interface-guidelines-components`** — Routes iOS/iPadOS Components/Inputs design tasks (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures) to HIG Components Knowledge Contracts.
  Example: `"review this list screen's layout against HIG"` → `lists-and-tables.md`
  Example: `"when should I use an action sheet instead of an alert"` → `action-sheets.md`

- **`human-interface-guidelines-patterns`** — Routes iOS/iPadOS Patterns design tasks (onboarding, searching, settings, notifications, feedback, undo/redo) to HIG Patterns Knowledge Contracts.
  Example: `"design an onboarding flow for a fitness app"` → `onboarding.md`
  Example: `"how should notification content be worded and when should we send one"` → `notifications.md`

- **`app-store-review-guidelines`** — Routes App Store submission-compliance tasks (app completeness, metadata accuracy, in-app purchase, spam/duplicate-app avoidance, privacy manifest and nutrition label accuracy) to App Store Review Guidelines Knowledge Contracts.
  Example: `"why would this in-app subscription get rejected"` → `digital-goods-iap.md`, `restore-purchases.md`
  Example: `"what needs to go in my PrivacyInfo.xcprivacy"` → `privacy-manifest.md`

- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`

- **`swiftui-interaction`** — Routes SwiftUI Animation and Gesture implementation tasks (implicit/explicit animation, transitions, matchedGeometryEffect, Animatable, PhaseAnimator/KeyframeAnimator, tap/long-press, drag, magnification/rotation, gesture composition, GestureState) to SwiftUI Interaction Knowledge Contracts.
  Example: `"why isn't my view fading in smoothly"` → `animation-modifiers.md`
  Example: `"how do I make a card draggable and snap back if released early"` → `drag-gesture.md`

- **`accessibility`** — Routes Accessibility API implementation tasks (labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion/Transparency/Increase Contrast, Full Keyboard Access, hidden/decorative elements, accessibility audits) to Accessibility Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this icon-only button has no VoiceOver label"` → `accessibility-labels.md`
  Example: `"swipe-to-delete row needs a VoiceOver alternative"` → `custom-accessibility-actions.md`

- **`uikit`** — Routes UIKit screen-scaffolding implementation tasks (view controller lifecycle/composition, programmatic Auto Layout, navigation, diffable table/collection views, modal presentation) to UIKit Knowledge Contracts.
  Example: `"my child view controller's view isn't showing up correctly"` → `view-controller-composition.md`
  Example: `"how do I animate row insertion in a UITableView"` → `table-view-diffable.md`

- **`sf-symbols`** — Routes SF Symbols API implementation tasks (rendering modes, symbol variants, variable value, weight/scale, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration) to SF Symbols Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this status icon should use two colors, one per layer"` → `rendering-modes.md`
  Example: `"how do I show wifi signal strength as a symbol"` → `variable-value-symbols.md`

- **`networking`** — Routes URLSession async/await networking implementation tasks (request construction, data fetching, Codable decoding, error handling, task cancellation, session configuration, App Transport Security, authenticated requests) to Networking Knowledge Contracts.
  Example: `"my JSON response isn't decoding, dates are failing"` → `codable-decoding.md`
  Example: `"how do I retry a request after a 401 without an infinite loop"` → `authenticated-requests.md`

- **`xcode`** — Routes Xcode project-configuration implementation tasks (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options) to Xcode Knowledge Contracts.
  Example: `"my archive won't export, wrong provisioning profile"` → `manual-signing-provisioning-profiles.md`
  Example: `"Product > Archive is greyed out"` → `archive-process.md`

- **`local-authentication`** — Routes Face ID/Touch ID/device-passcode implementation tasks (availability and biometry-type detection, policy evaluation, reason strings and Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX) to Local Authentication Knowledge Contracts.
  Example: `"Face ID prompt shows the wrong icon"` → `availability-and-biometry-type.md`
  Example: `"user is locked out of Face ID after too many failed attempts"` → `error-handling.md`

- **`app-tracking-transparency`** — Routes App Tracking Transparency / IDFA implementation tasks (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription) to App Tracking Transparency Knowledge Contracts.
  Example: `"how do I ask for tracking permission without re-prompting every launch"` → `authorization-request.md`
  Example: `"advertisingIdentifier is returning all zeros"` → `status-and-idfa-access.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).

## What's New

- 2026-08-06 — Expanded `swiftui` with a new Skill, `swiftui-interaction` (implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState) — 10 Knowledge Contracts. Closes the second of the two named Tier 1 priority gaps (after HIG Patterns/Components). Second domain with more than one Skill, split to stay under the project's Skill size cap.
- 2026-08-06 — Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap (Foundations-only HIG coverage). First domain with more than one Skill, split by Apple's own information architecture to stay under the project's Reference/Skill size caps. Flags a new `usernotifications` (Tier 2) cross-domain boundary in domain-map.md.
- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
