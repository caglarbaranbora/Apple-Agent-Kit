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

- 2026-08-08 — Seventeen of the project's domains had never been read against the semantic review standard, and reading them found a defect that was about to be copied into new work. The standard itself is recent; the domains predate it, and the earlier read-through had covered only two domains, both from the other group. Measurements had suggested the older domains were fine — but every one of those measurements came from the automated checks, and the whole lesson of the previous round was that the automated checks are not the ones that find this kind of problem. Reading was aimed rather than exhaustive: every technical identifier appearing in a rule was mapped to the domains claiming it, which narrowed 1,604 names to the 97 where two domains both had something to say. The real finding: two documents tell an agent to wrap a screen component in a particular adapter, and neither points at the document that owns the constraint making the wrap correct — so the agent follows the instruction and never learns the part that keeps it from breaking. A third domain was about to inherit the same gap. Three structural gaps surfaced too, the largest being that the vocabulary for recording how two domains relate could only express whether they overlap, never whether a choice on one side forces a choice on the other — which is exactly the shape of the last two defects found, both in boundaries that had been recorded as clean. What passed is recorded as carefully as what failed, including one proposed automated check that was built, found to flag half the project, and rejected on the spot.
- 2026-08-08 — The last open architectural question was settled against both answers that had been proposed for it, because someone finally counted. Certain tasks need two domains at once — fixing an error message needs both the rule about what the message must explain and the rules about how to word it — and the router can only send a task to one place. The recorded options were to add a combined workflow or to let one router hand off to another; the first was called the smaller change. Counting showed the overlap is not a corner of the design but runs through 29 of 33 documents on the design side, so a combined workflow would have pulled in four times the material for any task involving text, defeating the efficiency the whole project exists for. The second would have permanently weakened a structural rule and was the only option that could not be undone. What shipped instead costs two paragraphs: each side now stops and says which neighbour owns the other half, rather than answering half the question silently. Separately, the next wave of domains opens as a deliberately small pilot — location and photo access — whose purpose is to test a claim rather than to add content. An earlier end-to-end run suggested that boundaries between domains stay clean when they are decided before either side is written, and go wrong when they are left to emerge. All nine boundaries these two share with existing domains are therefore settled in advance, in writing, before a single rule is authored. One of them already caught a conflict that would otherwise have become a duplicated rule discovered much later. If the pilot goes wrong anyway, that is worth learning on two domains rather than nineteen.
- 2026-08-08 — The repository's semantic review gate had no instrument, and building one found a defect class that grows every time the project does. The validation model opens by saying that a level with no named enforcement is an aspiration rather than a gate; its own domain-level checks named a review checklist that did not exist, so every semantic defect the project has found was found by a phase that happened to look rather than by the gate meant to catch it. That checklist now exists, written from the failures that earned each of its seven checks and carried into the pull request template. Two of the seven describe failures the model's own wording had never named: a rule left unowned between two contracts that each correctly defer it to the other, and a cross-reference that resolves to a real target whose scope does not actually cover the claim citing it. The two workflows nobody had ever tested end to end were run against real tasks. The sign-in workflow — which outlived the retirement of the domain it is named after — came through intact, but revealed a security decision Apple treats as one choice and this project had split across two domains, each offering its half as free: an app could store a fingerprint-protected secret that survives on a device whose passcode was later removed, with the prompt still appearing so nothing looked wrong. The submission workflow found nothing, which is itself the finding, and explains why: its boundary was classified before either side was written. Separately, nine contracts described seven already-shipped domains as unbuilt, sending readers to look for answers that had been on disk for weeks. The check that exists for this had been widened twice, one artifact type at a time, and had still never read a knowledge contract — the largest place such claims live. It now reads all of them, which matters because every domain that ships turns every mention of it as "future" into a quiet falsehood in files nobody is editing.
Only the 3 most recent entries live here — see [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to open a PR and what a good Knowledge Contract or Skill submission looks like. Repo dev conventions (validation scripts, naming, layer order) are in [CLAUDE.md](CLAUDE.md).

## License

Source-available under the [PolyForm Strict License 1.0.0](LICENSE). You may download and use this software; you may not copy, redistribute, republish, or resell it. See [LICENSE](LICENSE) for the full terms.
