# Apple Agent Kit

[![npm version](https://img.shields.io/npm/v/apple-agent-kit)](https://www.npmjs.com/package/apple-agent-kit)
[![License](https://img.shields.io/badge/license-PolyForm%20Strict-blue)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-CHANGELOG.md-blue)](CHANGELOG.md)

Status: Stable
Version: 1.2.0

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

- **`usernotifications`** — Routes UserNotifications framework implementation tasks (authorization, local notification scheduling, remote push registration, delegate handling, actions/categories, managing pending/delivered requests and badge count) to UserNotifications Knowledge Contracts.
  Example: `"schedule a local reminder notification that repeats weekly"` → `local-notification-scheduling.md`
  Example: `"my notification actions aren't showing up"` → `notification-actions-and-categories.md`

- **`privacy`** — Routes Privacy Manifest (`PrivacyInfo.xcprivacy`) implementation tasks (file structure/bundling, required-reason API declarations, collected data type declarations, tracking domains and third-party SDK signatures) to Privacy Knowledge Contracts.
  Example: `"what reason code do I use for reading UserDefaults"` → `required-reason-api-declarations.md`
  Example: `"my SDK dependency needs a privacy manifest, where does it go"` → `manifest-file-structure-and-scope.md`

- **`foundation`** — Routes Swift Foundation implementation tasks (date/time formatting, measurement and unit formatting, Codable encoding and custom conformance, FileManager app sandbox directories) to Foundation Knowledge Contracts. A curated, highest-usage subset — not an exhaustive Foundation reference.
  Example: `"my table view is janky, I'm creating a DateFormatter in cellForRow"` → `date-time-formatting.md`
  Example: `"where should I cache thumbnails without bloating iCloud backup"` → `filemanager-app-sandbox-directories.md`

- **`security`** — Routes Keychain Services implementation tasks (item CRUD, accessibility levels, access groups and sharing, storing structured/Codable data) to Security Knowledge Contracts. v1 is general (non-biometric-bound) Keychain item CRUD for generic/internet password items.
  Example: `"save a session token to the Keychain so it survives app relaunch"` → `keychain-item-crud.md`, `keychain-accessibility-levels.md`
  Example: `"share a login between my app and its share extension"` → `keychain-access-groups-and-sharing.md`

- **`storekit`** — Routes StoreKit 2 in-app purchase implementation tasks (product loading and purchase, transaction verification and entitlements, transaction updates and restoring purchases, subscription status and renewal info) to StoreKit Knowledge Contracts. v1 is the modern StoreKit 2 async/await API only — no legacy StoreKit 1, no server-side receipt validation.
  Example: `"unlock premium content after a StoreKit purchase"` → `product-loading-and-purchase.md`, `transaction-verification-and-entitlements.md`
  Example: `"why is my subscriber still getting access after a refund"` → `subscription-status-and-renewal-info.md`

- **`authenticationservices`** — Routes Sign in with Apple implementation tasks (authorization request and credential handling, nonce and identity-token verification, credential-state checks and revocation, session persistence and sign-out) to AuthenticationServices Knowledge Contracts. v1 is Sign in with Apple only — no Password AutoFill/credential-provider extensions, no Passkeys/WebAuthn.
  Example: `"add Sign in with Apple to my login screen"` → `sign-in-with-apple-request-and-credential.md`
  Example: `"check if the user revoked Sign in with Apple access"` → `credential-state-and-revocation.md`

- **`widgetkit`** — Routes WidgetKit implementation tasks (widget declaration and families, timeline provider and entries, widget interactivity and deep links, timeline reloading and refresh budget) to WidgetKit Knowledge Contracts. v1 is home-screen/Lock-Screen widgets only — no Live Activities/ActivityKit, no watchOS complications, no Control Widgets.
  Example: `"build a home screen widget that shows today's stats"` → `widget-declaration-and-families.md`, `timeline-provider-and-entries.md`
  Example: `"widget still shows stale data after I updated it in the app"` → `timeline-reloading-and-refresh-budget.md`

- **`app-intents`** — Routes App Intents implementation tasks (app intent declaration and parameters, app entities and queries, App Shortcuts and Siri phrases, intent results) to App Intents Knowledge Contracts. v1 is intent authoring only — no legacy SiriKit, no Interactive Snippets, no Spotlight indexing of entities; wiring an already-authored intent into a widget is `widgetkit`'s job.
  Example: `"add a Siri Shortcut that marks today's habit as done"` → `app-intent-declaration-and-parameters.md`, `app-shortcuts-and-siri-phrases.md`
  Example: `"expose my app's playlists as an entity Siri can search"` → `app-entities-and-queries.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).

## What's New

- 2026-08-06 — Added `app-intents` Skill (app intent declaration and parameters, app entities and queries, App Shortcuts and Siri phrases, intent results and widget hookup; App Intents framework API v1) — 4 Knowledge Contracts. Eighth Tier 2 domain. Resolves the seam `widgetkit` had proactively deferred (`AppIntent` authoring itself); clean handoff with `widgetkit` (intent authoring vs. widget-side wiring). Supersedes legacy SiriKit.
- 2026-08-06 — Added `widgetkit` Skill (widget declaration and families, timeline provider and entries, widget interactivity and deep links, timeline reloading and refresh budget; WidgetKit framework API v1) — 4 Knowledge Contracts. Seventh Tier 2 domain. No existing cross-domain content to overlap with; proactively defers `AppIntent` authoring to the future `app-intents` domain and background-refresh scheduling to the future `backgroundtasks` domain.
- 2026-08-06 — Added `authenticationservices` Skill (Sign in with Apple request-and-credential handling, nonce and identity-token verification, credential-state checks and revocation, session persistence and sign-out; AuthenticationServices framework API v1) — 4 Knowledge Contracts. Sixth Tier 2 domain. Resolves the `authentication`/`authenticationservices`/`sign-in-with-apple` three-way boundary domain-map.md had left unresolved, absorbing the former `sign-in-with-apple` placeholder outright; clean handoffs with `authentication` (sign-in UX/terminology) and `security` (Keychain storage).
- 2026-08-06 — Added `storekit` Skill (product loading and purchase, transaction verification and entitlements, transaction updates and restoring purchases, subscription status and renewal info; StoreKit 2 async/await API v1) — 4 Knowledge Contracts. Fifth Tier 2 domain. Clean handoff with `app-store-review-guidelines`'s `digital-goods-iap.md`/`restore-purchases.md` (API implementation vs. review compliance), resolving the boundary domain-map.md had flagged proactively.
- 2026-08-06 — Added `security` Skill (Keychain item CRUD, accessibility levels, access groups and sharing, storing structured/Codable data; general non-biometric-bound Keychain Services API v1) — 4 Knowledge Contracts. Fourth Tier 2 domain. Clean handoff with `local-authentication`'s `keychain-biometric-binding.md` (biometric-bound access control vs. general Keychain CRUD), resolving the boundary domain-map.md had flagged proactively.
- 2026-08-06 — Added `foundation` Skill (date/time formatting, measurement and unit formatting, Codable encoding and custom conformance, FileManager app sandbox directories; curated highest-usage v1 subset, not exhaustive) — 4 Knowledge Contracts. Third Tier 2 domain. Angle-split with `style-guide`'s `units-of-measure.md` (unit-value production vs. copy wording) and clean handoff with `networking`'s `codable-decoding.md` (encoding vs. network-response decoding).
- 2026-08-06 — Added `privacy` Skill (manifest file structure/bundling, required-reason API declarations, collected data type declarations, tracking domains and third-party SDK signature requirement; `PrivacyInfo.xcprivacy` implementation/schema v1) — 4 Knowledge Contracts. Second Tier 2 domain. Angle-split with `human-interface-guidelines`'s `privacy.md` (design vs. implementation) and `app-store-review-guidelines`'s `privacy-manifest.md`/`privacy-nutrition-label.md` (implementation vs. review consequence), resolving two boundaries domain-map.md had flagged proactively.
- 2026-08-06 — Added `usernotifications` Skill (authorization, local notification scheduling, remote push registration, delegate handling, actions/categories, managing pending/delivered requests and badge count; client-side UserNotifications + UIKit push-registration API v1) — 6 Knowledge Contracts. First Tier 2 domain, picked as the tier's highest real-world-usage domain. Angle-split with `human-interface-guidelines`'s `notifications.md` on notification design vs. API implementation, resolving the boundary that domain-map.md had flagged proactively.
- 2026-08-06 — Expanded `swiftui` with a new Skill, `swiftui-interaction` (implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState) — 10 Knowledge Contracts. Closes the second of the two named Tier 1 priority gaps (after HIG Patterns/Components). Second domain with more than one Skill, split to stay under the project's Skill size cap.
- 2026-08-06 — Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap (Foundations-only HIG coverage). First domain with more than one Skill, split by Apple's own information architecture to stay under the project's Reference/Skill size caps. Flags a new `usernotifications` (Tier 2) cross-domain boundary in domain-map.md.
- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
