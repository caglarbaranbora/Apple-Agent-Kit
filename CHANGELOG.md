# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The project uses a single version number (`README.md` and `npx/package.json` share the same version).

## [Unreleased]

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
