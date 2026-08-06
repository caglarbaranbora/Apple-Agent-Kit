---
name: tipkit
description: Route TipKit implementation tasks to the correct Knowledge Contracts -- tip declaration and content, display rules and event triggers, tip options and app configuration, and presenting tips/tip groups. Use when conforming a struct to Tip, setting title/message/image/actions, writing #Rule(_:) with Tips.Parameter or Tips.Event, calling Tips.configure(_:), setting MaxDisplayCount/MaxDisplayDuration/IgnoresDisplayFrequency, presenting TipView/popoverTip/TipUIView/TipUIPopoverViewController, grouping tips with TipGroup, or calling invalidate(reason:). v1 is in-app feature tips/onboarding hints on iOS 17+ only -- no custom TipViewStyle authoring beyond the system default, no watchOS-specific presentation differences, and no CloudKit sync of the tip datastore (Tips.ConfigurationOption.cloudKitContainer(_:) is real and documented but out of scope). Triggers on TipKit, Tip protocol, TipView, TipUIView, TipUIPopoverViewController, TipGroup, Tips.configure, #Rule, Tips.Parameter, Tips.Event, Tip.Action, Tip.Option, MaxDisplayCount, IgnoresDisplayFrequency, invalidate(reason:), InvalidationReason.
id: skill.tipkit.foundations
title: TipKit — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: TipKit
routes: [knowledge.tipkit.tip-declaration-and-content, knowledge.tipkit.display-rules-and-event-triggers, knowledge.tipkit.tip-options-and-app-configuration, knowledge.tipkit.presenting-tips-and-tip-groups]
related: []
last_updated: 2026-08-06
---

# TipKit — Foundations Skill

## Purpose

Route TipKit implementation tasks to the minimum required TipKit
Knowledge Contracts. v1 scope is in-app feature tips and onboarding hints
on iOS 17+ -- declaring tip content, gating display with rules and
donated events, one-time app configuration plus per-tip options, and
presenting/grouping/dismissing tips -- not custom `TipViewStyle`
authoring, not watchOS-specific presentation differences, and not
CloudKit sync of the tip datastore.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/tipkit/.

-   Conforming a `struct` to `Tip`; implementing `title`/`message`/`image`; adding buttons via `actions`/`Tip.Action` -> tip-declaration-and-content.md
-   Writing the `rules` property with the `#Rule(_:)` macro over a `Tips.Parameter`-wrapped variable or a `Tips.Event`; donating with `sendDonation(_:)`/`donate()`; combining multiple rules -> display-rules-and-event-triggers.md
-   Calling `Tips.configure(_:)` at app launch; `datastoreLocation(_:)`/`displayFrequency(_:)`; per-tip `options` (`MaxDisplayCount`, `MaxDisplayDuration`, `IgnoresDisplayFrequency`) -> tip-options-and-app-configuration.md
-   Presenting with `TipView`/`popoverTip(_:arrowEdge:action:)`/`TipUIView`/`TipUIPopoverViewController`; grouping with `TipGroup`; dismissing with `invalidate(reason:)`/`Tip.InvalidationReason` -> presenting-tips-and-tip-groups.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/tipkit/ — do not guess or fall back to general
knowledge. Custom `TipViewStyle`/`TipViewStyleConfiguration` authoring
beyond the system default style is out of scope entirely -- not yet
built. watchOS-specific TipKit presentation differences are out of
scope entirely. `Tips.ConfigurationOption.cloudKitContainer(_:)` and any
cross-device sync of the tip datastore are out of scope entirely --
this is a real, documented TipKit capability (TipKit's datastore does
not sync by default, but can be configured to), not a fabricated
exclusion; report that boundary explicitly rather than routing to a
contract here.
