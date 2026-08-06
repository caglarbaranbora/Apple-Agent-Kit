# SwiftUI — Gestures & Animation Expansion — Design Spec

Status: Draft
Version: 0.1.0
Date: 2026-08-06

## Purpose

Extend the existing `swiftui` domain (currently Views/Navigation/Layout/State
v1, Tier 1) with Animation and Gestures Knowledge Contracts. This closes the
second of the two priority Tier 1 gaps identified in the Tier 1 completion
review (see `docs/architecture/domain-map.md` line 19) — the first,
`human-interface-guidelines` Patterns/Components/Inputs, shipped in PR #26.
The existing `swiftui` Skill's Stop Conditions explicitly name "Animation,
gestures... are out of scope for this skill" — this spec closes that gap.

This is a scope expansion of an existing domain, not a new domain.

## Scope

### Platform

iOS 17+ conventions, matching the existing `swiftui` domain.

### Breadth rationale

Unlike the HIG Patterns/Components expansion (60+ candidate topics,
requiring a curated subset), SwiftUI's Animation and Gestures API surface is
small and matches the existing domain's scale (12 Foundations topics). No
curation tradeoff is needed — this is comprehensive v1 coverage of the core
Animation and Gestures APIs, not a curated subset.

### Included (v1) — 10 Knowledge Contracts

**Animation (5)**, one topic each:
- `animation-modifiers` — implicit (`.animation(_:value:)`) vs. explicit
  (`withAnimation`) animation, timing curves (`.easeInOut`, `.spring`,
  `.interpolatingSpring`, custom timing)
- `transitions` — `.transition(_:)`, `AnyTransition`, asymmetric and
  combined transitions
- `matched-geometry-effect` — `matchedGeometryEffect`, namespace, shared-
  element transitions
- `animatable-values` — `Animatable` protocol, `animatableData`,
  `AnimatablePair`, custom animatable shapes/values
- `phase-and-keyframe-animators` — iOS 17+ `PhaseAnimator`,
  `KeyframeAnimator`, animation completion callbacks

**Gestures (5)**, one topic each:
- `tap-and-long-press-gestures` — `TapGesture`, `LongPressGesture`,
  `onTapGesture`/`onLongPressGesture` modifiers, count/minimumDuration
- `drag-gesture` — `DragGesture`, translation/predictedEndLocation,
  `updating` vs. `onChanged`/`onEnded`
- `magnification-and-rotation-gestures` — `MagnificationGesture`,
  `RotationGesture`
- `gesture-composition` — `.simultaneously(with:)`, `.sequenced(before:)`,
  `.exclusively(before:)`, gesture priority (`.highPriorityGesture` vs.
  `.gesture`)
- `gesture-state` — `GestureState` property wrapper, `updating(_:body:)`,
  transient gesture state reset

Each contract covers implementation-code guidance (which API, correct
syntax, common pitfalls) — same angle as the existing Foundations contracts
(`view-composition.md`, `navigation-stack.md`), not visual/UX design.

### Excluded (v1, deferred — recorded in domain-map.md as remaining gap)

- Previews (`#Preview` macro, `PreviewProvider`)
- Custom `Layout` protocol conformances
- Legacy `ObservableObject`/`NavigationView` migration guidance
- `UIGestureRecognizer` / Core Animation (UIKit) — owned by future `uikit`
  expansion, already recorded as unbuilt in domain-map.md
- Accessibility API implementation for gestures/animation (VoiceOver
  gesture alternatives, `accessibilityReduceMotion` Rules) — owned by
  `accessibility`; this expansion's contracts may reference the relevant
  `accessibility` Knowledge Contract via `related:` but do not restate its
  Rules
- Visual/UX design guidance for when/why to animate or which gesture to use
  — owned by `human-interface-guidelines` (`motion.md`,
  `touchscreen-gestures.md`)
- Combine-based animation/gesture publishers — owned by future `combine`
  domain (Tier 2, unbuilt)

## Cross-Domain Boundaries

Same angle-split precedent used throughout the kit:

- **vs. `human-interface-guidelines.motion`** (Foundations) — clean
  angle-split. `motion.md` owns *when/why* to animate (design intent,
  purposeful motion, Reduce Motion as a design requirement); this
  expansion owns *how* (API mechanics, syntax, correct modifier usage).
  `motion.md` is already `related:` to `knowledge.accessibility.reduce-
  motion`; this expansion's `animation-modifiers.md` adds the same
  `related:` link rather than restating Reduce Motion Rules.
- **vs. `human-interface-guidelines.touchscreen-gestures`** (shipped in
  PR #26) — clean handoff, already established from the HIG side: that
  contract's Excluded section explicitly reads "`UIGestureRecognizer`/
  SwiftUI gesture modifier implementation — see `swiftui`/`uikit`
  domains." No changes needed to that file; this expansion is the
  fulfillment of that existing handoff.
- **vs. `accessibility.reduce-motion`** — clean handoff. This expansion's
  `animation-modifiers.md` may note that `accessibilityReduceMotion`
  (environment value) exists and affects animation choices, but the Rule
  content (when/how to respect it) stays owned by `accessibility`,
  referenced via `related:`.
- **vs. `uikit`** (Core Animation, gesture recognizers — still unbuilt) —
  no change. Boundary already recorded in domain-map.md as remaining gap
  for `uikit`.
- **vs. future `combine`** (Tier 2, unbuilt) — no overlap for v1; not
  flagged proactively since Combine-based animation/gesture publishers are
  a narrow, unlikely-to-be-built-first slice of that future domain.

## File Layout

Knowledge Contracts land in the existing domain directory (domain is
unchanged, only the routing layer splits):

```
knowledge/swiftui/
  (12 existing Foundations files, unchanged)
  animation-modifiers.md, transitions.md, matched-geometry-effect.md,
  animatable-values.md, phase-and-keyframe-animators.md,
  tap-and-long-press-gestures.md, drag-gesture.md,
  magnification-and-rotation-gestures.md, gesture-composition.md,
  gesture-state.md
```

The Reference stays a single file (no split needed — 10 new topics at the
existing ~2.5 lines/topic density pushes `references/apple/swiftui.md` from
48 to ~78 lines, under the 80-line cap). The Skill splits in two, because
10 new routing lines would push the existing 47-line Skill past the 60-line
cap:

```
references/apple/
  swiftui.md   (existing, extended with Animation + Gestures Primary Topics
                and Used By entries; "Animation, gestures... are out of
                scope" line removed from Purpose)

skills/
  swiftui/SKILL.md               (existing — Foundations routing unchanged,
                                   Stop Conditions updated to route instead
                                   of blanket-report-as-gap)
  swiftui-interaction/SKILL.md   (new)
```

Both skills cross-link via `related:`. This is the second domain in the kit
with more than one Skill (after `human-interface-guidelines`), same
precedent: driven purely by the size cap, not a domain boundary change.

## Reference: `references/apple/swiftui.md` (extended)

Same file, extended with an Animation and a Gestures Primary Topics
sub-list and matching Used By entries for the 10 new Knowledge Contracts.
Purpose paragraph's "Animation, gestures, previews, and custom `Layout`
protocol conformances are out of scope for this pass" sentence is rewritten
to drop "Animation, gestures," since those are now in scope; previews and
custom `Layout` protocol conformances remain out of scope.

## Skill: `skills/swiftui-interaction/SKILL.md`

`id: skill.swiftui.interaction`. Routes to the 10 Animation/Gestures KCs.
Routing clusters:

- Animation start/state -> `animation-modifiers.md`
- View transitions -> `transitions.md`, `matched-geometry-effect.md`
- Custom animatable values -> `animatable-values.md`
- Multi-phase/keyframe animation -> `phase-and-keyframe-animators.md`
- Tap/long-press -> `tap-and-long-press-gestures.md`
- Drag -> `drag-gesture.md`
- Pinch/rotate -> `magnification-and-rotation-gestures.md`
- Combining gestures -> `gesture-composition.md`, `gesture-state.md`

Stop condition: Foundations topics (view/navigation/layout/state) route to
`skill.swiftui.foundations`. Visual/UX design questions (when/why to
animate, which gesture to use) route to
`skill.human-interface-guidelines.foundations` or `.components`.
`UIGestureRecognizer`/Core Animation (UIKit) and any other Excluded-list
topic report the gap explicitly rather than answering from general
knowledge — same pattern as every other skill's stop condition.

## Skill Update: `skills/swiftui/SKILL.md`

Add `skill.swiftui.interaction` to `related:`. Rewrite the Stop Conditions
sentence that currently reads "Animation, gestures, previews, custom
`Layout` protocol conformances, legacy `ObservableObject`/`NavigationView`
migration guidance, and accessibility APIs... are out of scope for this
skill" to instead route Animation/Gestures questions to
`skill.swiftui.interaction`, while previews/custom `Layout`/legacy
migration/accessibility APIs remain explicitly out of scope (report the gap).

## Documentation Updates

Per `CLAUDE.md`'s "Updating README.md" rule, same commit as the domain work:

- `README.md` — one new Skills bullet (`swiftui-interaction`) with concrete
  example invocations (e.g. `"why isn't my view fading in smoothly" ->
  animation-modifiers.md`, `"how do I make list rows draggable" ->
  drag-gesture.md`); new top-of-list "What's New" line (3-item cap,
  rotates out the oldest entry).
- `CHANGELOG.md` — new entry under `## [Unreleased]`.
- `docs/architecture/domain-map.md`:
  - Tier 1 "Completed:" line (line 19) — `swiftui` clause rewritten from
    "animation, gestures, previews, custom Layout protocol conformances,
    and legacy ObservableObject/NavigationView migration guidance remain
    unbuilt" to name the new Animation/Gestures v1 scope, keeping previews/
    custom Layout/legacy migration as the remaining named gap.
  - Tier 1 table row (line 28, `swiftui`) — same update, both the
    "Completed:" prose line and the table row, matching the same mistake
    caught and fixed manually in the HIG expansion (see PR #26 commit
    `55ac2ac`) — both must be updated in the same task this time.
  - Cross-Domain Notes — no new bullet needed; the `swiftui` vs.
    `human-interface-guidelines` layout overlap note (line 98) and the
    `human-interface-guidelines.accessibility` vs. `accessibility` note
    (line 101) already establish the angle-split precedent this expansion
    follows. Optionally extend line 98's note to mention motion/gestures
    explicitly for discoverability.
- `skills/index.md` — one new Discovery Rules row (`swiftui-interaction`),
  inserted adjacent to the existing `swiftui` row.

## Validation

Same as every prior domain:

```bash
python3 scripts/validate_artifact.py <path> --type knowledge   # x10
python3 scripts/validate_artifact.py <path> --type skill       # x2
python3 scripts/validate_artifact.py <path> --type reference   # x1
python3 -m unittest tests/test_validate_artifact.py -v
claude plugin validate .
```

Line-cap check is part of validation for `references/apple/swiftui.md`
(target ~78/80 — closest to cap of any Reference in the kit) and both
Skill files.

## Build Order

Reference update -> Knowledge (Animation cluster, then Gestures cluster,
each reviewed as its own batch per RFC 0001 decision 5) -> Skills (new
`swiftui-interaction` + update existing `swiftui`) -> Documentation ->
Validation. Animation before Gestures (no dependency between them; order
chosen for consistency with this spec's listing order).

## Out of Scope for This Spec

- All Excluded-list topics above (previews, custom `Layout` protocol,
  legacy `ObservableObject`/`NavigationView` migration, UIKit gesture
  recognizers/Core Animation, accessibility API implementation).
- Any Tier 2 domain work.
- Further HIG Patterns/Components/Inputs topics (separate, already-shipped
  sub-project).
