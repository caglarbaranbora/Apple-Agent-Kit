# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The project uses a single version number (`README.md` and `npx/package.json` share the same version).

## [Unreleased]

## [1.3.0] - 2026-08-06
### Added
- v1.3.0 release: ninth Tier 2 domain, `backgroundtasks`.
- `backgroundtasks` Skill (background task registration and scheduling, task execution and expiration handling, processing task constraints and conditions, background refresh and widget timeline hookup; BackgroundTasks framework API v1) — 4 Knowledge Contracts. Resolves the second seam `widgetkit` had proactively deferred (background-refresh scheduling mechanics): `backgroundtasks` owns registering, submitting, and running the `BGAppRefreshTaskRequest` that produces fresh widget data; `widgetkit` continues to own the `WidgetCenter.reloadTimelines`/`reloadAllTimelines` call site and its refresh-budget reasoning once that data has landed — a clean handoff, not an angle-split. `BGContinuedProcessingTask`, legacy Background Fetch, unrelated background modes (audio/location/VoIP), and `URLSession` background transfer (owned by `networking`) remain out of scope.

## [1.2.0] - 2026-08-06
### Added
- v1.2.0 release: eighth Tier 2 domain, `app-intents`.
- `app-intents` Skill (app intent declaration and parameters, app entities and queries, App Shortcuts and Siri phrases, intent results and widget hookup; App Intents framework API v1) — 4 Knowledge Contracts. Resolves the seam `widgetkit` had proactively deferred (`AppIntent` authoring itself): `app-intents` owns declaring the intent (`perform()`, parameters, entities, result), `widgetkit` continues to own wiring an already-authored intent into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)` — a clean handoff, not an angle-split. Supersedes legacy SiriKit (donation-based intents) on current OS versions; no separate SiriKit domain planned.

## [1.1.0] - 2026-08-06
### Added
- v1.1.0 release: seventh Tier 2 domain, `widgetkit`.
- `widgetkit` Skill (widget declaration and families, timeline provider and entries, widget interactivity and deep links, timeline reloading and refresh budget; WidgetKit framework API v1) — 4 Knowledge Contracts. No existing cross-domain content to overlap with (no prior widget-design content in `swiftui`/`human-interface-guidelines`); proactively defers `AppIntent` authoring to the future `app-intents` domain and background-refresh scheduling mechanics to the future `backgroundtasks` domain.

## [1.0.9] - 2026-08-06
### Added
- v1.0.9 release: sixth Tier 2 domain, `authenticationservices`.
- `authenticationservices` Skill (Sign in with Apple request-and-credential handling, nonce and identity-token verification, credential-state checks and revocation, session persistence and sign-out; AuthenticationServices framework API v1) — 4 Knowledge Contracts. Resolves the `authentication`/`authenticationservices`/`sign-in-with-apple` three-way boundary domain-map.md had left unresolved, absorbing the former `sign-in-with-apple` placeholder outright (same framework, no distinct content). Clean handoffs with `authentication` (sign-in UX/terminology) and `security` (Keychain storage), resolving two boundaries domain-map.md had flagged proactively.

## [1.0.8] - 2026-08-06
### Added
- v1.0.8 release: fifth Tier 2 domain, `storekit`.
- `storekit` Skill (product loading and purchase, transaction verification and entitlements, transaction updates and restoring purchases, subscription status and renewal info; StoreKit 2 async/await API v1) — 4 Knowledge Contracts. Clean handoff with `app-store-review-guidelines`'s `digital-goods-iap.md`/`restore-purchases.md` (API implementation vs. review compliance), resolving the boundary domain-map.md had flagged proactively.

## [1.0.7] - 2026-08-06
### Added
- v1.0.7 release: fourth Tier 2 domain, `security`.
- `security` Skill (Keychain item CRUD, accessibility levels, access groups and sharing, storing structured/Codable data; general non-biometric-bound Keychain Services API v1) — 4 Knowledge Contracts. Clean handoff with `local-authentication`'s `keychain-biometric-binding.md` (biometric-bound access control vs. general Keychain CRUD), resolving the boundary domain-map.md had flagged proactively.

## [1.0.6] - 2026-08-06
### Added
- v1.0.6 release: third Tier 2 domain, `foundation`.
- `foundation` Skill (date/time formatting, measurement and unit formatting, Codable encoding and custom conformance, FileManager app sandbox directories; curated highest-usage v1 subset, not exhaustive) — 4 Knowledge Contracts. Angle-split with `style-guide`'s `units-of-measure.md` (unit-value production vs. copy wording) and clean handoff with `networking`'s `codable-decoding.md` (encoding vs. network-response decoding).

## [1.0.5] - 2026-08-06
### Added
- v1.0.5 release: second Tier 2 domain, `privacy`.
- `privacy` Skill (manifest file structure/bundling, required-reason API declarations, collected data type declarations, tracking domains and third-party SDK signature requirement; `PrivacyInfo.xcprivacy` implementation/schema v1) — 4 Knowledge Contracts. Angle-split with `human-interface-guidelines`'s `privacy.md` (design vs. implementation) and `app-store-review-guidelines`'s `privacy-manifest.md`/`privacy-nutrition-label.md` (implementation vs. review consequence), resolving two boundaries domain-map.md had flagged proactively.

## [1.0.4] - 2026-08-06
### Added
- v1.0.4 release: first Tier 2 domain, `usernotifications`.
- `usernotifications` Skill (authorization, local notification scheduling, remote push registration, delegate handling, actions/categories, managing pending/delivered requests and badge count; client-side UserNotifications + UIKit push-registration API v1) — 6 Knowledge Contracts. Picked as the tier's highest real-world-usage domain. Angle-split with `human-interface-guidelines`'s `notifications.md` on notification design vs. API implementation, resolving the boundary domain-map.md had flagged proactively.

## [1.0.3] - 2026-08-06
### Added
- v1.0.3 release: both named Tier 1 priority gaps closed — `human-interface-guidelines` Patterns/Components/Inputs and `swiftui` Animation/Gestures.
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
