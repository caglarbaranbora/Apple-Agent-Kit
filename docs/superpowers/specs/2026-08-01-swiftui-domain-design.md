# SwiftUI Domain — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Add `swiftui` as the third Tier 1 domain, after `human-interface-guidelines`
(Foundations subset, shipped in PR #5) and `app-store-review-guidelines`
(critical-subset v1, shipped in PR #7). Delivers agent-actionable
implementation conventions for SwiftUI — the framework layer, not the
visual-design layer, which `human-interface-guidelines` already owns.

## Context

SwiftUI's surface area is too large for a single v1 pass (views, layout,
navigation, state management, animation, gestures, accessibility APIs,
previews, and more). This domain bounds v1 to the areas most load-bearing
for correctness and most error-prone for an agent generating SwiftUI code:
Views, Navigation, Layout, and State management. `domain-map.md`'s
pre-existing Initial Scope text for `swiftui` ("Views, navigation, layout")
omitted state management; this project adds it to v1 because state-related
bugs (stale `@State`, wrong property wrapper, view-identity loss) are the
most common SwiftUI implementation mistake, and the domain-map text is
updated accordingly as part of this project.

v1 targets iOS 17+ conventions: `@Observable` (Swift 5.9+) as the
recommended state-management macro, `NavigationStack`/`NavigationSplitView`
as the recommended navigation APIs. Legacy APIs (`ObservableObject`,
`NavigationView`) are out of scope — this domain teaches the current
recommended way to write SwiftUI, not a migration guide.

## Decisions

### 1. Scope: 4 areas, iOS 17+, v1

Selected areas (confirmed with user during brainstorming):

- **Views** — composition, identity, modifier order
- **Navigation** — NavigationStack, NavigationSplitView
- **Layout** — stacks/spacing, safe area, lazy grids, GeometryReader
- **State management** — `@State`/`@Binding`, `@Observable`, `@Environment`

Excluded from v1 (future pass, not dropped): animation, gestures,
accessibility APIs (owned by future `accessibility` domain), previews,
custom `Layout` protocol conformances, legacy `ObservableObject`/
`NavigationView` migration guidance.

### 2. Knowledge Contract breakdown: atomic, one rule per file

Mirrors `human-interface-guidelines` and `app-store-review-guidelines`'s
resolution (atomic KCs, not one file per API/area) — a single area often
bundles multiple independent implementation rules, which would violate
`domain-map.md`'s "Knowledge Contracts remain atomic" rule if merged.

**Final v1 scope: 12 Knowledge Contracts**, all under `knowledge/swiftui/`:

1. `view-composition` (Views) — single-responsibility views, extract subviews, `ViewBuilder`
2. `view-identity` (Views) — stable `id`/`Identifiable` in `ForEach`/`List`, avoiding state-loss bugs from unstable identity
3. `modifier-order` (Views) — modifier order changes the result (`frame` vs `padding` vs `background`)
4. `navigation-stack` (Navigation) — `NavigationStack` + `NavigationPath`, programmatic/deep-link navigation
5. `navigation-split-view` (Navigation) — `NavigationSplitView` for multi-column/iPad layouts
6. `stacks-and-spacing` (Layout) — `VStack`/`HStack`/`ZStack`, `Spacer`, alignment
7. `safe-area` (Layout) — `safeAreaInset` vs `ignoresSafeArea`, correct usage
8. `lazy-grids` (Layout) — `LazyVGrid`/`LazyVStack` for large/dynamic content, avoiding non-lazy stacks in `ScrollView`
9. `geometry-reader-anti-pattern` (Layout) — `GeometryReader` pitfalls (breaks intrinsic sizing), when it's actually needed
10. `state-and-binding` (State) — `@State` for local view state, `@Binding` for child mutation
11. `observable-macro` (State) — `@Observable` (iOS17+) for reference-type models, replaces `ObservableObject`
12. `environment-values` (State) — `@Environment` for dependency injection/shared app state

### 3. Cross-domain overlap: `human-interface-guidelines` (layout angle)

`human-interface-guidelines`'s `layout.md` owns the visual-design angle
(spacing/alignment as a design decision, what makes a screen HIG-compliant).
This domain's `stacks-and-spacing.md`, `safe-area.md`, and `lazy-grids.md`
own the code-implementation angle (which API, correct syntax, performance
pitfalls) — same angle-split pattern already established for
`human-interface-guidelines`'s `privacy.md` vs the future `privacy` domain,
and for `app-store-review-guidelines`'s `privacy-manifest`/
`privacy-nutrition-label` vs the same future `privacy` domain. One new
Cross-Domain Notes entry records this.

### 4. Cross-domain overlap: `combine` (Tier 2, unbuilt)

`domain-map.md`'s existing Tier 2 table already lists `combine`'s Owns line
as "Publisher/subscriber usage conventions, SwiftUI interop." This domain's
`observable-macro.md` teaches `@Observable` as the modern, non-Combine
replacement for `ObservableObject` — not Combine-based state management.
One new Cross-Domain Notes entry records the boundary, resolved when
`combine` is actually built (its angle: Combine-specific publisher/
subscriber patterns; this domain's angle: the modern macro-based
replacement).

### 5. File layout: mirrors prior domains, no new pattern

- **Reference:** one file, `references/apple/swiftui.md` — same shape as
  `references/apple/human-interface-guidelines.md` and
  `references/apple/app-store-review-guidelines.md` (Source, Purpose,
  Primary Topics, Used By listing all 12 knowledge contracts). Source URL:
  `https://developer.apple.com/documentation/swiftui`.
- **Knowledge:** 12 files under `knowledge/swiftui/`, one per topic above,
  existing knowledge-contract format (`## Metadata` fenced YAML block —
  id/type/title/version/status/owner/summary/domain/tags/references/
  depends_on/related/updated — plus `## Intent`, `## Rules`,
  `## Compliant Example`, `## Non-Compliant Example`; 150-line cap).
  `domain: SwiftUI` in each.
- **Skill:** one native skill, `skills/swiftui/SKILL.md`, hardened format
  (frontmatter `name`/`description`/`id: skill.swiftui.foundations`/
  `title`/`version`/`status`/`artifact_type`/`domain`/`routes:` [12 ids]/
  `related:` [`skill.human-interface-guidelines.foundations`]/
  `last_updated`; body `## Purpose`, `## Routing`, `## Stop Conditions`;
  80-line cap). `related:` links to `human-interface-guidelines` since the
  layout angle-split (Decision 3) means an agent doing layout work may
  need both skills.

No per-topic reference files, no directory nesting beyond the established
`knowledge/<domain>/<slug>.md` and `skills/<domain>/SKILL.md` conventions.

### 6. Routing: keyword-clustered, deterministic, load-minimum

Mirrors prior domains' `## Routing` section: frontmatter `routes:` is the
full flat set (all 12), body groups into task-keyword clusters so the agent
loads only what a specific question needs.

Proposed clusters:
- Views → `view-composition.md`, `view-identity.md`, `modifier-order.md`
- Navigation → `navigation-stack.md`, `navigation-split-view.md`
- Layout → `stacks-and-spacing.md`, `safe-area.md`, `lazy-grids.md`, `geometry-reader-anti-pattern.md`
- State management → `state-and-binding.md`, `observable-macro.md`, `environment-values.md`

### 7. `domain-map.md` updates (part of this project, not a separate pass)

- `swiftui` row's **Initial Scope** cell updated from "Views, navigation,
  layout" to: "Views (composition, identity, modifier order), Navigation
  (NavigationStack, NavigationSplitView), Layout (stacks/spacing, safe
  area, lazy grids, GeometryReader), State management (@State/@Binding,
  @Observable, @Environment). Targets iOS 17+ conventions; legacy
  ObservableObject/NavigationView out of scope — see Cross-Domain Notes."
- Two new Cross-Domain Notes entries (Decisions 3 and 4 above).
- **Build Order** section's "Completed" line gets `swiftui` (iOS17+
  Views/Navigation/Layout/State v1) appended once this ships.

## Consequences

- Fourth full domain under the hardened native-skill pipeline (after
  `style-guide`/`authentication`, `human-interface-guidelines`, and
  `app-store-review-guidelines`).
- First domain to use `related:` in its Skill frontmatter (points back to
  `human-interface-guidelines`) since the layout angle-split creates a
  genuine cross-skill dependency, unlike `app-store-review-guidelines`
  which left `related:` empty.
- Animation, gestures, previews, custom `Layout` protocol conformances, and
  legacy API migration guidance remain explicitly unbuilt. Not silently
  dropped: `domain-map.md`'s Initial Scope cell and this spec both record
  the boundary.
- Adds 2 new Cross-Domain Notes entries that must be checked when `privacy`
  and `combine` are eventually built.
- No changes to `scripts/validate_artifact.py`, `docs/specifications/*`, or
  any hardening-project file — this project only produces new
  reference/knowledge/skill content on top of the already-hardened schema.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py references/apple/swiftui.md --type reference` — `PASS`.
- `python3 scripts/validate_artifact.py knowledge/swiftui/<slug>.md --type knowledge` for all 12 files — all `PASS`.
- `python3 scripts/validate_artifact.py skills/swiftui/SKILL.md --type skill` — `PASS`.
- `python3 -m unittest tests/test_validate_artifact.py -v` — full pass (no regressions).
- `claude plugin validate .` — confirms the new `SKILL.md` is discovered.
- `skills/index.md` Discovery Rules table gets a new row for `swiftui`.
- `README.md` `## Skills` and `## What's New` sections updated per
  `CLAUDE.md`'s standing rule.
- Manual invocation check in a fresh session (same caveat as prior
  domains — the harness enumerates skills at session start, so this can't
  be verified same-session).

## Out of Scope

- Animation, gestures, previews, custom `Layout` protocol conformances,
  legacy `ObservableObject`/`NavigationView` migration guidance — future
  passes, tracked in `domain-map.md`.
- Accessibility APIs for SwiftUI views — owned by the future
  `accessibility` domain, not reopened here.
- Resolving the `stacks-and-spacing`/`safe-area`/`lazy-grids` overlap with
  `human-interface-guidelines`'s `layout.md`, or the `observable-macro`
  overlap with the future `combine` domain — both already resolved via
  angle-split (Decisions 3, 4), not deferred, but the domains themselves
  remain as-is (no changes to `human-interface-guidelines` in this project).
- Any change to already-hardened schema/validator/spec files.
