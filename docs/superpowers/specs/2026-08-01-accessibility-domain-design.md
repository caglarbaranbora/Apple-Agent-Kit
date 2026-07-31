# Accessibility Domain — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Add `accessibility` as the fourth Tier 1 domain, after `human-interface-guidelines`
(Foundations subset, PR #5), `app-store-review-guidelines` (critical-subset v1,
PR #7), and `swiftui` (Views/Navigation/Layout/State v1, PR #8). Delivers
agent-actionable Accessibility API implementation conventions — closing two
forward-references left open by prior domains.

## Context

Two prior domains explicitly deferred accessibility API implementation to
this domain:

- `human-interface-guidelines`'s `accessibility.md` (design angle: Dynamic
  Type support, contrast ratios, not conveying state by color alone,
  labeling custom icon-only controls) states in its Intent section that
  "Accessibility API implementation details (VoiceOver traits,
  UIAccessibility properties)... belongs to the future dedicated
  `accessibility` domain."
- `swiftui`'s Skill Stop Conditions explicitly defer "accessibility APIs"
  for SwiftUI views to this domain.

`domain-map.md`'s Cross-Domain Notes already records the
`human-interface-guidelines` ↔ `accessibility` boundary as "not yet
resolved — decide when `accessibility` is built." This project resolves it.

## Decisions

### 1. Scope: SwiftUI + UIKit accessibility API, framework-agnostic

Accessibility is a single underlying system (VoiceOver, the accessibility
tree, `UIAccessibility`) exposed through two API surfaces — SwiftUI
modifiers (`.accessibilityLabel()`, `.accessibilityElement(children:)`,
`@AccessibilityFocusState`) and UIKit properties/protocols
(`accessibilityLabel`, `UIAccessibilityCustomAction`, `UIFocusEnvironment`).
Splitting by framework would force every KC into an artificial dual (one
SwiftUI version, one UIKit version) or would leave UIKit projects
unsupported until a separate future pass. Each KC below covers both API
surfaces for its topic, matching the framework-agnostic pattern already
used by `human-interface-guidelines` (which isn't SwiftUI- or
UIKit-specific either).

### 2. Knowledge Contract breakdown: atomic, 12 KCs

Mirrors the atomic-KC resolution used by all three prior domains.

**Final v1 scope: 12 Knowledge Contracts**, all under
`knowledge/accessibility/`:

1. `accessibility-labels` — `accessibilityLabel`, SwiftUI
   `.accessibilityLabel()`, UIKit `UIAccessibility` protocol conformance
2. `accessibility-traits` — `accessibilityTraits`,
   `.accessibilityAddTraits()`, assigning correct traits to custom controls
3. `accessibility-value-and-hint` — `accessibilityValue`/`accessibilityHint`,
   communicating custom-control state (sliders, steppers, toggles)
4. `custom-accessibility-actions` — `.accessibilityAction()`,
   `UIAccessibilityCustomAction`, non-gesture alternatives for
   swipe-only interactions
5. `accessibility-element-grouping` — `.accessibilityElement(children:)`,
   `isAccessibilityElement`, collapsing composite views into one
   VoiceOver stop
6. `voiceover-navigation-order` — `.accessibilitySortPriority()`, custom
   reading order for non-linear layouts
7. `dynamic-type-api` — `@ScaledMetric`, `UIFontMetrics`, API-level layout
   response to Dynamic Type (implements the requirement HIG's
   `accessibility.md` Rule 1 sets at the design level)
8. `reduce-motion` — `@Environment(\.accessibilityReduceMotion)`,
   `UIAccessibility.isReduceMotionEnabled`
9. `reduce-transparency-increase-contrast` — corresponding
   environment values / `UIAccessibility` properties and change
   notifications
10. `full-keyboard-access-and-focus` — `.focusable()`,
    `@AccessibilityFocusState`, `UIFocusEnvironment`
11. `accessibility-hidden-decorative` — `.accessibilityHidden(true)`,
    excluding decorative images from the accessibility tree
12. `accessibility-audits-testing` — Accessibility Inspector,
    `XCTest`'s `performAccessibilityAudit`

`accessibility-audits-testing` is included in v1 rather than deferred to
the future Tier 2 `testing` domain (XCTest/Swift Testing/UI testing,
unbuilt) because accessibility audit APIs are accessibility-specific, not
general test infrastructure — deferring would leave a gap with nothing to
route to until `testing` is eventually built. One new Cross-Domain Notes
entry records the boundary for when `testing` is built (this domain's
angle: accessibility-specific audit APIs; `testing`'s future angle:
general XCTest/Swift Testing/UI-testing conventions).

### 3. Cross-domain resolution: `human-interface-guidelines`

Resolves the existing "not yet resolved" Cross-Domain Notes entry via the
angle-split already stated in HIG's `accessibility.md` Intent section:
HIG's angle is design guidance (Dynamic Type requirement, contrast ratios,
not color-alone, gesture alternatives — the *what* and *why*), this
domain's angle is API implementation (the *how* — which modifier,
property, or protocol). The existing Cross-Domain Notes bullet is updated
from "not yet resolved" to resolved, with both domains' KCs cross-linked
via `related:`.

### 4. Cross-domain resolution: `swiftui`

`swiftui`'s Skill Stop Conditions line ("accessibility APIs... deferred")
is satisfied by this domain's existence. No change needed to `swiftui`'s
files themselves (Stop Conditions correctly describe what SwiftUI's v1
doesn't cover) — this domain's Skill `related:` field links back to
`skill.swiftui.foundations` so an agent doing SwiftUI accessibility work
discovers this domain.

### 5. File layout: mirrors prior domains, no new pattern

- **Reference:** one file, `references/apple/accessibility.md` — same
  shape as the three prior Reference files (Source, Purpose, Primary
  Topics, Used By listing all 12 knowledge contracts). Source URL:
  `https://developer.apple.com/accessibility/`.
- **Knowledge:** 12 files under `knowledge/accessibility/`, one per topic
  above, existing knowledge-contract format (`## Metadata` fenced YAML
  block — id/type/title/version/status/owner/summary/domain/tags/
  references/depends_on/related/updated — plus `## Intent`, `## Rules`,
  `## Compliant Example`, `## Non-Compliant Example`; 150-line cap).
  `domain: Accessibility` in each. `accessibility-labels`,
  `accessibility-traits`, `dynamic-type-api`, and
  `accessibility-hidden-decorative` each set `related:` to the
  corresponding `knowledge.human-interface-guidelines.accessibility` (and,
  where relevant, `knowledge.human-interface-guidelines.color`/`typography`
  for the contrast/Dynamic-Type design-vs-API pairing).
- **Skill:** one native skill, `skills/accessibility/SKILL.md`, hardened
  format (frontmatter `name`/`description`/
  `id: skill.accessibility.foundations`/`title`/`version`/`status`/
  `artifact_type`/`domain`/`routes:` [12 ids]/
  `related:` [`skill.human-interface-guidelines.foundations`,
  `skill.swiftui.foundations`]/`last_updated`; body `## Purpose`,
  `## Routing`, `## Stop Conditions`; 80-line cap).

No per-topic reference files, no directory nesting beyond the established
`knowledge/<domain>/<slug>.md` and `skills/<domain>/SKILL.md` conventions.

### 6. Routing: keyword-clustered, deterministic, load-minimum

Mirrors prior domains' `## Routing` section: frontmatter `routes:` is the
full flat set (all 12), body groups into task-keyword clusters.

Proposed clusters:
- Labeling & description → `accessibility-labels.md`, `accessibility-traits.md`, `accessibility-value-and-hint.md`
- Interaction → `custom-accessibility-actions.md`, `full-keyboard-access-and-focus.md`
- Structure & navigation → `accessibility-element-grouping.md`, `voiceover-navigation-order.md`, `accessibility-hidden-decorative.md`
- User preferences → `dynamic-type-api.md`, `reduce-motion.md`, `reduce-transparency-increase-contrast.md`
- Verification → `accessibility-audits-testing.md`

### 7. `domain-map.md` updates (part of this project, not a separate pass)

- `accessibility` row's **Initial Scope** cell updated from "Accessibility
  APIs and UX" to: "SwiftUI + UIKit accessibility API implementation:
  labels/traits/value/hint, custom actions, element grouping, VoiceOver
  navigation order, Dynamic Type API, reduce-motion/transparency/
  increase-contrast, keyboard access & focus, hidden/decorative elements,
  accessibility audits. Design-level accessibility guidance owned by
  `human-interface-guidelines` — see Cross-Domain Notes."
- Existing `human-interface-guidelines` ↔ `accessibility` Cross-Domain
  Notes bullet updated from "not yet resolved" to resolved (angle-split
  per Decision 3).
- One new Cross-Domain Notes entry: `accessibility` ↔ future `testing`
  domain (Decision 2 above).
- **Build Order** section's "Completed" line gets `accessibility`
  (SwiftUI + UIKit API v1) appended once this ships.

## Consequences

- Fifth full domain under the hardened native-skill pipeline (after
  `style-guide`/`authentication`, `human-interface-guidelines`,
  `app-store-review-guidelines`, and `swiftui`).
- Second domain (after `swiftui`) to use a non-empty `related:` in its
  Skill frontmatter, and the first to link to two other Skills.
- Closes both outstanding forward-references from `human-interface-
  guidelines` and `swiftui` — no domain currently has an unresolved
  "deferred to future accessibility domain" note after this ships.
- Adds 1 new Cross-Domain Notes entry (`accessibility` ↔ `testing`) that
  must be checked when `testing` is eventually built.
- No changes to `scripts/validate_artifact.py`, `docs/specifications/*`,
  or any hardening-project file — this project only produces new
  reference/knowledge/skill content on top of the already-hardened
  schema, plus documentation-only edits to existing HIG/SwiftUI-adjacent
  files (`domain-map.md` Cross-Domain Notes).

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py references/apple/accessibility.md --type reference` — `PASS`.
- `python3 scripts/validate_artifact.py knowledge/accessibility/<slug>.md --type knowledge` for all 12 files — all `PASS`.
- `python3 scripts/validate_artifact.py skills/accessibility/SKILL.md --type skill` — `PASS`.
- `python3 -m unittest tests/test_validate_artifact.py -v` — full pass (no regressions).
- `claude plugin validate .` — confirms the new `SKILL.md` is discovered.
- `skills/index.md` Discovery Rules table gets a new row for `accessibility`.
- `README.md` `## Skills` and `## What's New` sections updated per
  `CLAUDE.md`'s standing rule.
- Manual invocation check in a fresh session (same caveat as prior
  domains — the harness enumerates skills at session start, so this can't
  be verified same-session).

## Out of Scope

- Design-level accessibility guidance (Dynamic Type *requirement*,
  contrast *ratio*, color-alone prohibition, gesture-alternative *rule*)
  — owned by `human-interface-guidelines`'s existing `accessibility.md`,
  not duplicated here.
- General XCTest/Swift Testing/UI-testing conventions beyond accessibility
  audits — owned by the future Tier 2 `testing` domain.
- Any change to already-hardened schema/validator/spec files.
- Any change to `swiftui` or `human-interface-guidelines` KC/Skill
  content files themselves (only `domain-map.md` Cross-Domain Notes is
  touched).
