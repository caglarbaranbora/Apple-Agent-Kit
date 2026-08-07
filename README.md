# Apple Agent Kit

[![npm version](https://img.shields.io/npm/v/apple-agent-kit)](https://www.npmjs.com/package/apple-agent-kit)
[![License](https://img.shields.io/badge/license-PolyForm%20Strict-blue)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-CHANGELOG.md-blue)](CHANGELOG.md)

Status: Stable
Version: 2.0.0

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

- **`authentication`** — Sign-in, sign-up, credential, and biometric implementation. → [SKILL.md](skills/authentication/SKILL.md)
- **`style-guide`** — UI copy and wording: labels, error text, capitalization, formatting. → [SKILL.md](skills/style-guide/SKILL.md)
- **`human-interface-guidelines`** — Visual design: layout, color, typography, dark mode, motion, icons. → [SKILL.md](skills/human-interface-guidelines/SKILL.md)
- **`human-interface-guidelines-components`** — HIG Components/Inputs: lists, buttons, sheets, alerts, navigation, pickers, gestures. → [SKILL.md](skills/human-interface-guidelines-components/SKILL.md)
- **`human-interface-guidelines-patterns`** — HIG Patterns: onboarding, search, settings, notifications, feedback, undo/redo. → [SKILL.md](skills/human-interface-guidelines-patterns/SKILL.md)
- **`app-store-review-guidelines`** — App Store submission compliance: metadata, IAP, privacy manifest, spam/duplicate. → [SKILL.md](skills/app-store-review-guidelines/SKILL.md)
- **`swiftui`** — SwiftUI view composition, navigation, layout, state management. → [SKILL.md](skills/swiftui/SKILL.md)
- **`swiftui-interaction`** — SwiftUI animation and gestures. → [SKILL.md](skills/swiftui-interaction/SKILL.md)
- **`accessibility`** — Accessibility API (labels, traits, Dynamic Type, VoiceOver, audits) across SwiftUI/UIKit. → [SKILL.md](skills/accessibility/SKILL.md)
- **`uikit`** — UIKit screen scaffolding: view controllers, Auto Layout, navigation, diffable views. → [SKILL.md](skills/uikit/SKILL.md)
- **`sf-symbols`** — SF Symbols rendering, variants, and configuration across SwiftUI/UIKit. → [SKILL.md](skills/sf-symbols/SKILL.md)
- **`networking`** — URLSession async/await networking and Codable decoding. → [SKILL.md](skills/networking/SKILL.md)
- **`xcode`** — Xcode project configuration: build settings, signing, entitlements, archive/export. → [SKILL.md](skills/xcode/SKILL.md)
- **`local-authentication`** — Face ID/Touch ID implementation. → [SKILL.md](skills/local-authentication/SKILL.md)
- **`app-tracking-transparency`** — App Tracking Transparency / IDFA authorization. → [SKILL.md](skills/app-tracking-transparency/SKILL.md)
- **`usernotifications`** — UserNotifications framework: local/push scheduling, delegate handling, actions. → [SKILL.md](skills/usernotifications/SKILL.md)
- **`privacy`** — Privacy Manifest (`PrivacyInfo.xcprivacy`) implementation. → [SKILL.md](skills/privacy/SKILL.md)
- **`foundation`** — Swift Foundation essentials: date/measurement formatting, Codable, FileManager. → [SKILL.md](skills/foundation/SKILL.md)
- **`security`** — Keychain Services item CRUD, accessibility levels, sharing. → [SKILL.md](skills/security/SKILL.md)
- **`storekit`** — StoreKit 2 in-app purchase: purchase, entitlements, subscriptions. → [SKILL.md](skills/storekit/SKILL.md)
- **`authenticationservices`** — Sign in with Apple implementation. → [SKILL.md](skills/authenticationservices/SKILL.md)
- **`widgetkit`** — WidgetKit: declaration, timelines, interactivity, refresh. → [SKILL.md](skills/widgetkit/SKILL.md)
- **`app-intents`** — App Intents: intent authoring, entities, App Shortcuts, Siri. → [SKILL.md](skills/app-intents/SKILL.md)
- **`backgroundtasks`** — BackgroundTasks scheduling and execution. → [SKILL.md](skills/backgroundtasks/SKILL.md)
- **`eventkit`** — EventKit calendar/reminder access and EventKitUI hand-off. → [SKILL.md](skills/eventkit/SKILL.md)
- **`tipkit`** — TipKit in-app feature tips. → [SKILL.md](skills/tipkit/SKILL.md)
- **`passkit`** — PassKit Wallet passes and Apple Pay. → [SKILL.md](skills/passkit/SKILL.md)
- **`swiftdata`** — SwiftData model definition, querying, relationships. → [SKILL.md](skills/swiftdata/SKILL.md)
- **`core-data`** — Core Data model definition, fetching, relationships. → [SKILL.md](skills/core-data/SKILL.md)
- **`combine`** — Combine publishers/subscribers, `@Published`, operators. → [SKILL.md](skills/combine/SKILL.md)
- **`testing`** — XCTest, Swift Testing, and XCUITest implementation. → [SKILL.md](skills/testing/SKILL.md)
- **`localization`** — String Catalogs, plurals, `Locale` resolution, RTL APIs. → [SKILL.md](skills/localization/SKILL.md)

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).

## What's New

- 2026-08-07 — Added `localization` Skill (String Catalogs and extraction, localized-string APIs, plural and device variations, `Locale` and language resolution, layout-direction and RTL APIs, localized resources and Info.plist) — 6 Knowledge Contracts. **Seventeenth and final Tier 2 domain — Tier 2 is now complete.** Baseline is Xcode 16+ with an iOS 17+ API surface: String Catalogs impose no deployment-target cost, since `.xcstrings` compiles to `.strings`/`.stringsdict` at build time, so the real gate is the Xcode version. Closes the SF Symbols RTL seam `human-interface-guidelines` had left open — mirroring is automatic and driven by the symbol's name, with no API to request it ("forward"/"backward" mirror, "left"/"right" do not). Corrects several natural-but-wrong assumptions: `String(localized:)`'s `locale:` parameter formats interpolated values but does **not** change which language is looked up; `Text(someVariable)` silently resolves to a non-localizing initializer; `Locale.current` reports the locale the *app* resolved to, not the user's preference; `Locale.autoupdatingCurrent` never compares equal to a fixed `Locale`; `UISemanticContentAttribute.unspecified` means *mirror*, not "do nothing"; and `imageFlippedForRightToLeftLayoutDirection()` sets a flag rather than returning a flipped image. Xcode project-language configuration and `.xcloc`/XLIFF export-import (deferred to `xcode`), the iOS 18 Translation framework, and non-iOS platforms remain out of scope.
- 2026-08-07 — Added `testing` Skill (`XCTestCase` structure and assertions, Swift Testing fundamentals, parameterized and async tests, UI testing with `XCUIApplication`, expectations for asynchronous code; curated v1 subset of XCTest/Swift Testing/XCUITest, not exhaustive) — 5 Knowledge Contracts. Sixteenth Tier 2 domain. Two clean, proactively-scoped handoffs rather than discovered conflicts: Xcode Test Plans/code coverage config remain `xcode`'s territory, and `performAccessibilityAudit()` remains `accessibility`'s territory. Corrects several natural-but-wrong assumptions: `setUp()`/`tearDown()` has a same-named once-per-class `class func` overload distinct from the per-test instance methods; `XCUIApplication`/`XCUIElement` are now documented under the XCUIAutomation framework, not XCTest; the `app.buttons["x"]`-style subscript matches any of an element's identifying properties, not only `accessibilityIdentifier`; `@Test(arguments:)` over two bare collections produces a Cartesian product while a `zip`-wrapped single argument produces paired invocations; and `wait(for:timeout:)` is guided-away-from in favor of `await fulfillment(of:timeout:)`, not deprecated. Performance testing, snapshot testing, UI test recording, and mocking/DI patterns remain out of scope.
- 2026-08-07 — Added `combine` Skill (publishers and subscribers, `@Published`/`ObservableObject`, subjects, transforming/combining operators, assign and memory management; Combine framework API v1) — 5 Knowledge Contracts. Fifteenth Tier 2 domain, resolving the `swiftui`/`combine` state-management boundary this repo had left open pending `combine`'s build. No corrections to the approved scope beyond citation-precision notes (the full `debounce(for:scheduler:options:)` signature, and citing `Publishers.Merge`'s type page for `merge(with:)`). Async/await interop, custom `Publisher`/`Subscriber` conformances, backpressure, and SwiftData/Core Data interop remain out of scope.

Only the 3 most recent entries live here — see [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
