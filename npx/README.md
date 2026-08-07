# Apple Agent Kit

[![npm version](https://img.shields.io/npm/v/apple-agent-kit)](https://www.npmjs.com/package/apple-agent-kit)
[![License](https://img.shields.io/badge/license-PolyForm%20Strict-blue)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-CHANGELOG.md-blue)](CHANGELOG.md)

Status: Stable
Version: 2.1.0

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

## Workflows

A Workflow composes several Skills into one task that no single domain owns. Routing matches Workflows first: if the task spans more than one of the Skills a Workflow names, that Workflow is loaded and sequences them; otherwise exactly one Skill is loaded.

- **`authentication`** — Build a sign-in feature end to end: wording, form accessibility, Sign in with Apple, biometric re-auth, Keychain storage. → [WORKFLOW.md](workflows/authentication/WORKFLOW.md)
- **`app-store-submission`** — Review-guideline compliance and privacy declaration, gated ahead of signing, archive, and export. → [WORKFLOW.md](workflows/app-store-submission/WORKFLOW.md)
- **`add-widget`** — Widget surface, its configuration and interaction intents, and the background refresh that keeps its timeline current. → [WORKFLOW.md](workflows/add-widget/WORKFLOW.md)

## Skills

Skills route a task to the minimum set of Knowledge Contracts it needs. Invoke them with a specific task, not a broad topic request — name the concrete thing you're doing (e.g. "check this screen's layout against HIG"), not "tell me about HIG."

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

- 2026-08-07 — Scope statements get a vocabulary, and it is enforced. Every statement of what a Skill does *not* cover is now marked **owned by `<domain>`** (a hand-off, and the domain must exist), **Deferred** (this domain will own it), or **Excluded** (no domain will) — three facts that 17 Skills had been stating in one interchangeable phrase. Enforcing it found five Skills suppressing domains that had already shipped: `foundation` called `localization` and `combine` "future" and "(Tier 2, unbuilt)", `accessibility` said the same of `testing`, `privacy` of `security`, `localization` of `xcode` — so an agent asking any of those questions was told the answer did not exist while the Contracts holding it sat on disk. `uikit`'s Storyboard/XIB support, ruled out on purpose, no longer appears in the domain map as outstanding work.
- 2026-08-07 — The Workflow layer is real. `skills/index.md` becomes the **Routing Index**: a Workflows table matched ahead of the Skills table, and Resolution Rules that retire the old "load exactly one Skill" ban on multi-domain tasks. Three Workflows ship, deliberately of three different shapes — `authentication` (fan-out across five domains), `app-store-submission` (sequential and gated), `add-widget` (three hand-offs whose boundaries were already resolved). The `authentication` Skill and its 4 Knowledge Contracts are **retired** — the first retirement this repository has performed. Its value was routing across domains, not knowledge of its own: its terminology rules are owned in far more detail by `style-guide`, its accessibility rules by `accessibility`, and its sign-in mechanics by `authenticationservices`. Retiring it also removed a contradiction it carried, where its own example named "Log In" as the term for an internet-account button, which the Apple Style Guide reserves for local system sessions.
- 2026-08-07 — Added `localization` Skill (String Catalogs and extraction, localized-string APIs, plural and device variations, `Locale` and language resolution, layout-direction and RTL APIs, localized resources and Info.plist) — 6 Knowledge Contracts. **Seventeenth and final Tier 2 domain — Tier 2 is now complete.** Baseline is Xcode 16+ with an iOS 17+ API surface: String Catalogs impose no deployment-target cost, since `.xcstrings` compiles to `.strings`/`.stringsdict` at build time, so the real gate is the Xcode version. Closes the SF Symbols RTL seam `human-interface-guidelines` had left open — mirroring is automatic and driven by the symbol's name, with no API to request it ("forward"/"backward" mirror, "left"/"right" do not). Corrects several natural-but-wrong assumptions: `String(localized:)`'s `locale:` parameter formats interpolated values but does **not** change which language is looked up; `Text(someVariable)` silently resolves to a non-localizing initializer; `Locale.current` reports the locale the *app* resolved to, not the user's preference; `Locale.autoupdatingCurrent` never compares equal to a fixed `Locale`; `UISemanticContentAttribute.unspecified` means *mirror*, not "do nothing"; and `imageFlippedForRightToLeftLayoutDirection()` sets a flag rather than returning a flipped image. Xcode project-language configuration and `.xcloc`/XLIFF export-import (deferred to `xcode`), the iOS 18 Translation framework, and non-iOS platforms remain out of scope.
Only the 3 most recent entries live here — see [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
