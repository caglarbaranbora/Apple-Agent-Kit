# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The project uses a single version number (`README.md` and `npx/package.json` share the same version).

## [Unreleased]
### Added
- Expanded `swiftui` with a new Skill, `swiftui-interaction` (implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState) — 10 Knowledge Contracts. Closes the second of the two named Tier 1 priority gaps (after HIG Patterns/Components). Second domain with more than one Skill, split by the project's Skill (≤60 lines) size cap.
- Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap. First domain with more than one Skill, split by Apple's own Foundations/Patterns/Components information architecture to stay under the project's Reference (≤80 lines) and Skill (≤60 lines) size caps.

## [1.0.2] - 2026-08-05
### Added
- v1.0.2 release: all 11 Tier 1 domains complete (`style-guide`, `human-interface-guidelines`, `app-store-review-guidelines`, `swiftui`, `accessibility`, `uikit`, `sf-symbols`, `networking`, `xcode`, `local-authentication`, `app-tracking-transparency`), plus `authentication` (cross-cutting, built ahead of tier order). See `docs/architecture/domain-map.md` for full per-domain scope and the Cross-Domain Notes documenting every resolved boundary.
- `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains, replaces the prior placeholder scope in domain-map.md.
- `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication`, replaces the prior placeholder scope in domain-map.md.
- `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.

## [0.1.2] - 2026-08-01
### Added
- `networking` Skill (URLSession async/await, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests) — 8 Knowledge Contracts. Fills the "Authentication networking" gap that `authentication.md` explicitly excludes.
- `sf-symbols` Skill (rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contracts.
- `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation) — 12 Knowledge Contracts.
- `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contracts.
- `swiftui` Skill (view composition/identity, NavigationStack/NavigationSplitView, layout, state management) — 12 Knowledge Contracts.

### Changed
- npm package README synced with the GitHub repo README (updated Skill list, installation notes added).

## [0.1.1] - 2026-07-31
### Added
- Added `LICENSE`, `CONTRIBUTING.md`, `CLAUDE.md`; enriched README.
- `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contracts.
- `human-interface-guidelines` Skill (layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL) — 15 Knowledge Contracts.

### Changed
- Hardened native Skill format (real YAML frontmatter, deterministic keyword routing, Stop Conditions) across all Skills.

## [0.1.0] - 2026-07-31
### Added
- Published the initial npm installer package (`npx apple-agent-kit`).
- `authentication` Skill (sign-in, sign-up, credentials, biometrics).
- `style-guide` Skill (terminology, capitalization, punctuation, inclusive writing).

[Unreleased]: https://github.com/caglarbaranbora/Apple-Agent-Kit/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/caglarbaranbora/Apple-Agent-Kit/releases/tag/v0.1.2
