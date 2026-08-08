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
- **`app-store-review-guidelines`** — App Store submission compliance: safety, metadata, IAP, privacy, intellectual property, ratings. → [SKILL.md](skills/app-store-review-guidelines/SKILL.md)
- **`swiftui`** — SwiftUI view composition, navigation, layout, state management, and legacy-code migration. → [SKILL.md](skills/swiftui/SKILL.md)
- **`swiftui-interaction`** — SwiftUI animation and gestures. → [SKILL.md](skills/swiftui-interaction/SKILL.md)
- **`accessibility`** — Accessibility API (labels, traits, Dynamic Type, VoiceOver, announcements, audits) across SwiftUI/UIKit. → [SKILL.md](skills/accessibility/SKILL.md)
- **`uikit`** — UIKit screen scaffolding: view controllers, Auto Layout, navigation, diffable views. → [SKILL.md](skills/uikit/SKILL.md)
- **`uikit-interaction`** — UIKit gestures, animation, view controller transitions, and SwiftUI interop. → [SKILL.md](skills/uikit-interaction/SKILL.md)
- **`sf-symbols`** — SF Symbols rendering, variants, and configuration across SwiftUI/UIKit. → [SKILL.md](skills/sf-symbols/SKILL.md)
- **`networking`** — URLSession networking across async/await, completion-handler, and Combine, plus delegates, background transfers, and TLS trust. → [SKILL.md](skills/networking/SKILL.md)
- **`xcode`** — Xcode project configuration: build settings, signing, entitlements, archive/export, test plans and coverage, project localization. → [SKILL.md](skills/xcode/SKILL.md)
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

- 2026-08-08 — Every Apple URL the kit cites is now fetched, not merely indexed, and CI runs the checks it had been skipping. 615 of the 739 cited URLs had never been fetched by anyone, and no check fetched URLs — so the previous pass could prove a citation was indexed by the right Reference and listed under the right `## Used By` while it was, in fact, a 404. The first full run found four such defects in four domains, each of which passed all three mechanical levels: two Core Data URLs 404 outright, because `fetch(_:)` and `performAndWait(_:)` are overloaded and Apple serves overloads at hashed paths while the sibling members on the same page resolve fine, which is why nothing looked wrong; and two redirects, `XCTSkip` to its `-swift.struct` form and the `developer.apple.com/accessibility/` marketing path to the documentation one. A redirect is treated as a finding rather than a pass — it is the address that 404s later, which is precisely what the two Core Data URLs already did. The check is deliberately not a seventeenth repository check: it asks another organisation's web server, so its answer can change without the kit changing, and it runs on a pull request's own changed files plus a weekly full sweep instead of blocking every commit. Also closes a gap in CI itself, which had been running structural validation only, on 322 of 326 artifacts — the sixteen repository-wide checks and the test suite were never in CI, and `workflows/` had gone entirely unvalidated since the layer was built. No Knowledge Contract changed.
- 2026-08-08 — Every Apple URL the kit cites is now indexed by a Reference, and a new validator check keeps it that way. 124 cited URLs across 15 domains were listed in no Reference at all, which put them outside the existing `## Used By` check entirely: that check walks indexed URLs, so an unindexed one matched nothing and was never examined. Coverage could only be re-measured by hand, and the hand-measurements drifted three times. Run against the previous commit, the new check reports 155 findings; after this pull request, zero. Indexing surfaced a stale Apple URL for the third consecutive pass — `LAError` and `UIImage.SymbolConfiguration` both redirect to a `-swift.struct`/`-swift.class` form, the same redirect the UIKit pass found, and one domain was carrying both spellings of one page with nothing to notice. A second check is widened: four References described built domains as "future" or "unbuilt", the exact defect `check_scope_vocabulary` exists to catch, but it read Skills only — so a Reference could send the next author to the wrong authority one layer away from a Skill that had been fixed for the identical sentence. No Knowledge Contract changed.
- 2026-08-08 — `app-store-review-guidelines` is complete. Eight Knowledge Contracts close every guideline the Skill had listed as Deferred — user-generated content moderation (1.2), developer contact information (1.5), data security (1.6), copycats and impersonation (4.1), the login-services equivalent option (4.8), third-party content licensing (5.2.1-5.2.3), and Apple trademarks and product confusion (5.2.4, 5.2.5) — plus a ninth topic the plan had not listed. Guideline 4.8 closes a **broken edge**: the authentication Workflow composed five Skills to build a sign-in screen and none of them knew that omitting an equivalent login option is a rejection, so it could produce a screen App Review turns down. It is now the Workflow's first step, because 4.8 decides how many buttons the screen has and is not correctable after submission. The addition is guideline 5.6.1: Apple states it "will disallow custom review prompts", which reaches the two designs teams actually build — a satisfaction gate ("Enjoying the app?" routing happy users to the system prompt) is itself a custom prompt, and a "Rate us" button is what Apple's own API documentation says not to build, because `requestReview` "may not present an alert". Ten Contracts had been citing the guidelines landing page as a single source; all 20 now cite per-guideline anchors and the Reference indexes 26 sources instead of 1. Indexing again surfaced a stale Apple URL — an unindexed URL is an unverified URL — and correcting it revealed a shared citation two References had been blind to. Guideline 1.1 and 4.6 are **Excluded**; 4.4, 4.5, 4.7 are **Deferred to Tier 3**. Also fixes a third hole in `prose-domain-resolves`: the mention regexes match the trailing noun case-insensitively, but the resolver compared it with `==`, so a capitalised "Workflow" fell through to the domain table and every mention of the authentication Workflow read as a hand-off to the retired domain of the same name.
Only the 3 most recent entries live here — see [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
