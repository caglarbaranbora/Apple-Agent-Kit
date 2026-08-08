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

- 2026-08-08 — Every artifact in the repository is now `Approved`, and getting there cost three defects that no mechanical check could have found. 325 of 326 artifacts were `Draft`, which made `Approved` a word the project used about exactly one file. The lifecycle document requires two things before an artifact may be promoted, and only one of them held: the mechanical levels passed, but the sole end-to-end validation record on file tested five artifacts that had all been deleted a phase earlier, so it validated an architecture that no longer existed. Three new end-to-end runs replaced it, and each found something. The Workflow layer — built two phases ago and never exercised — routed a widget task correctly and loaded six Contracts of 326, then revealed a rule that lives in neither of the two domains it falls between: each defers it to the other, and the general rule an agent does reach tells it to request a widget refresh that Apple's documentation says the system has already performed, spending a daily budget the same Contract warns is limited to 40-70. Separately, nine routing keywords sent an agent to two Skills at once, with the tiebreak sitting in a file the routing procedure never opens. Both are fixed and both are now checked. A third finding — a task that two domains answer jointly and the router can only send to one — is recorded rather than fixed, because closing it means either a new Workflow or weakening a layer-order rule, and that is a decision rather than a repair. The lifecycle document also turned out to demand four validator rejections and receive one; three are now code, and the fourth runs on pull requests, because a state transition is a fact about two versions of a file and no single working tree can see it. No rule's meaning changed.
- 2026-08-08 — The Human Interface Guidelines and Style Guide domains were read end to end to decide which of their 58 Knowledge Contracts duplicate each other and should be retired, and the answer is none. The two domains are partitioned by kind rather than by topic — one decides what to build, the other decides what to call it — so where they name the same thing they are answering different questions. This settles a question left open two passes ago: the HIG's gesture Contract and the Style Guide's gesture-verb Contract are not duplicates and neither retires, since one governs whether a gesture may exist at all and the other governs the verb used to describe it. What the read-through did find is duplicated *rules*, in eight places, in Contracts that stay — including one Contract that stated a rule its own Excluded list had deferred to a neighbour, and one cross-reference pointing at a rule that did not cover the case it was cited for. Each is now resolved the way the repository already resolved others: one Contract owns the rule, the neighbour points at it and states that it defines none. A duplicated rule is worse than a missing one, because both copies are correct the day they are written, no mechanical check can tell that two differently-worded paragraphs are the same rule, and the failure only appears when Apple changes the guidance and one copy is updated — a failure this repository has already had once. 10 Contracts revised, none added or removed, and no rule's meaning changed.
- 2026-08-08 — Every Apple URL the kit cites is now fetched, not merely indexed, and CI runs the checks it had been skipping. 615 of the 739 cited URLs had never been fetched by anyone, and no check fetched URLs — so the previous pass could prove a citation was indexed by the right Reference and listed under the right `## Used By` while it was, in fact, a 404. The first full run found four such defects in four domains, each of which passed all three mechanical levels: two Core Data URLs 404 outright, because `fetch(_:)` and `performAndWait(_:)` are overloaded and Apple serves overloads at hashed paths while the sibling members on the same page resolve fine, which is why nothing looked wrong; and two redirects, `XCTSkip` to its `-swift.struct` form and the `developer.apple.com/accessibility/` marketing path to the documentation one. A redirect is treated as a finding rather than a pass — it is the address that 404s later, which is precisely what the two Core Data URLs already did. The check is deliberately not a seventeenth repository check: it asks another organisation's web server, so its answer can change without the kit changing, and it runs on a pull request's own changed files plus a weekly full sweep instead of blocking every commit. Also closes a gap in CI itself, which had been running structural validation only, on 322 of 326 artifacts — the sixteen repository-wide checks and the test suite were never in CI, and `workflows/` had gone entirely unvalidated since the layer was built. No Knowledge Contract changed.
Only the 3 most recent entries live here — see [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
