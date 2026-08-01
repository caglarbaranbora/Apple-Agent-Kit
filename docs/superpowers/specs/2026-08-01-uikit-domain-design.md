# UIKit Domain — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Add `uikit` as the sixth domain under the hardened native-skill pipeline, after
`style-guide`/`authentication`, `human-interface-guidelines` (PR #5),
`app-store-review-guidelines` (PR #7), `swiftui` (PR #8), and `accessibility`
(PR #9). Replaces the vague `domain-map.md` placeholder ("UIKit components" /
"UIKit component implementation conventions") with a real, scoped v1: the
imperative-UI screen-scaffolding surface — view controllers, Auto Layout,
navigation, and modern diffable table/collection views.

## Context

`domain-map.md`'s Tier 1 table lists `uikit` with the least specific
Initial Scope/Owns cells of any domain — a placeholder never fleshed out.
Meanwhile `swiftui` (PR #8) covers the declarative-UI equivalent (Views,
Navigation, Layout, State, iOS 17+) and `accessibility` (PR #9) already
covers UIKit's accessibility surface (`accessibilityLabel`/`Traits`/`Value`/
`Hint`, `UIAccessibilityCustomAction`, `isAccessibilityElement`/
`accessibilityElements`, `UIFontMetrics`, `UIFocusEnvironment`). This project
gives `uikit` a real v1 scope without duplicating either.

## Decisions

### 1. Scope: "screen scaffolding core," programmatic UI only

UIKit's full surface (view controllers, table/collection views, Auto Layout,
navigation, gestures, Core Animation, custom transitions, Storyboard/XIB) is
too broad for one v1 pass — the same reasoning that scoped `swiftui` down to
Views/Navigation/Layout/State and `app-store-review-guidelines` down to a
critical-guideline subset. v1 covers what's needed to build and navigate a
screen imperatively:

- View controller lifecycle and composition (container pattern)
- Auto Layout (constraints/anchors, `UIStackView`, safe area)
- Navigation (`UINavigationController`, `UITabBarController`)
- Modern list/grid UI (diffable data sources, compositional layout, cell
  registration)
- Modal presentation

**Programmatic UI only** — no Storyboard/XIB, no `IBOutlet`/`IBAction`
workflow. Code-based UI is the modern default and is more agent-reviewable
(diffable, no binary/XML interface files).

**Diffable data sources only** — `UITableViewDiffableDataSource`/
`UICollectionViewDiffableDataSource` and `NSDiffableDataSourceSnapshot`, not
the classic `cellForRowAt`/`numberOfRowsInSection` delegate pattern. Mirrors
`swiftui`'s "current convention, not legacy" precedent (iOS 17+ APIs,
`ObservableObject`/`NavigationView` migration explicitly out of scope there).

### 2. Explicitly out of scope for v1

- **Accessibility APIs** — owned by `accessibility` (PR #9). UIKit KCs here
  cross-reference it via `related:` where relevant (e.g.
  `cell-configuration` may reference `knowledge.accessibility.accessibility-labels`
  for cell accessibility) but never restate its Rules.
- **Gesture recognizers, Core Animation/CALayer, custom transitions/
  animations** — deferred to a future pass. Recorded as a Cross-Domain Notes
  entry (`uikit` internal future scope, not a separate domain).
- **UIKit↔SwiftUI interop** (`UIHostingController`, `UIViewRepresentable`/
  `UIViewControllerRepresentable`) — deferred. New Cross-Domain Notes entry:
  `uikit` ↔ `swiftui`, boundary to resolve when interop is eventually built.
- **Storyboard/XIB workflow** — out of scope entirely, not deferred (a
  deliberate convention choice, not a gap to fill later).

### 3. Knowledge Contract breakdown: atomic, 12 KCs

Mirrors the atomic-KC resolution used by all four prior full domains this
arc. All under `knowledge/uikit/`:

1. `view-controller-lifecycle` — `viewDidLoad`/`viewWillAppear`/
   `viewDidAppear`/`viewWillDisappear`/`viewDidDisappear`, correct placement
   of setup/teardown work
2. `view-controller-composition` — child view controllers, `addChild`/
   `didMove(toParent:)`/`willMove(toParent:)`
3. `auto-layout-constraints` — `NSLayoutConstraint`/anchors,
   `translatesAutoresizingMaskIntoConstraints`, activate/deactivate patterns
4. `auto-layout-stack-views` — `UIStackView` axis/distribution/alignment/
   spacing
5. `safe-area-and-layout-guides` — `safeAreaLayoutGuide`,
   `layoutMarginsGuide`
6. `navigation-controller` — `UINavigationController` push/pop,
   `navigationItem`, back button customization
7. `tab-bar-controller` — `UITabBarController`, tab item setup
8. `table-view-diffable` — `UITableViewDiffableDataSource`, cell
   registration, snapshot apply
9. `collection-view-compositional-layout` —
   `UICollectionViewCompositionalLayout`,
   `NSCollectionLayoutSection`/`Item`/`Group`
10. `collection-view-diffable` — `UICollectionViewDiffableDataSource`,
    snapshot apply (pairs with #9, same split pattern as
    `accessibility-element-grouping`/`voiceover-navigation-order`: one KC
    owns layout structure, the other owns data/snapshot binding)
11. `cell-configuration` — `UICollectionView.CellRegistration`/UITableView
    cell registration, reuse identifiers, `prepareForReuse`
12. `modal-presentation` — present/dismiss, `UIModalPresentationStyle`,
    sheets

### 4. Cross-domain resolution: `accessibility`

New Cross-Domain Notes entry: `uikit` ↔ `accessibility`. Angle-split —
`accessibility` owns all UIKit accessibility API implementation (labels,
traits, value/hint, custom actions, element grouping/order, Dynamic Type,
reduce-motion/transparency, focus, hidden/decorative, audits);  `uikit` owns
non-accessibility screen-scaffolding APIs. Where a UIKit KC's example touches
an accessibility property, it links via `related:` rather than restating
Rules — same non-duplication pattern `accessibility-hidden-decorative`
already uses toward `human-interface-guidelines`.

### 5. Cross-domain resolution: `swiftui`

New Cross-Domain Notes entry: `uikit` ↔ `swiftui`. Both domains cover
screen-building but on separate API surfaces (declarative vs imperative);
neither depends on the other for v1. The interop boundary
(`UIHostingController`/`UIViewRepresentable`) is recorded as future scope
for whichever domain builds it, not assigned yet.

### 6. Cross-domain resolution: `human-interface-guidelines`

New Cross-Domain Notes entry: `uikit` ↔ `human-interface-guidelines`, same
angle-split pattern `accessibility` already established with HIG — HIG owns
design guidance (when to use a tab bar vs navigation stack, list vs grid
layout choice, modal vs push presentation), `uikit` owns the API
implementation (the *how*). No existing HIG file needs modification; only
`domain-map.md` Cross-Domain Notes gets the new entry.

### 7. File layout: mirrors prior domains, no new pattern

- **Reference:** one file, `references/apple/uikit.md` — same shape as prior
  Reference files (Source, Purpose, Primary Topics, Used By listing all 12
  knowledge contracts). Source URL: `https://developer.apple.com/documentation/uikit`.
- **Knowledge:** 12 files under `knowledge/uikit/`, existing knowledge-
  contract format (`## Metadata` fenced YAML block — id/type/title/version/
  status/owner/summary/domain/tags/references/depends_on/related/updated —
  plus `## Intent`, `## Scope`, `## Rules`, `## Compliant Example`,
  `## Non-Compliant Example`, `## Dependencies`, `## References`; 150-line
  cap). `domain: UIKit` in each.
- **Skill:** one native skill, `skills/uikit/SKILL.md`, hardened format
  (frontmatter `name`/`description`/`id: skill.uikit.foundations`/`title`/
  `version`/`status`/`artifact_type`/`domain`/`routes:` [12 ids]/`related:`
  [`skill.accessibility.foundations`, `skill.swiftui.foundations`,
  `skill.human-interface-guidelines.foundations`]/`last_updated`; body
  `## Purpose`, `## Routing`, `## Stop Conditions`; 80-line cap). Third
  domain to link to multiple Skills, first to link to three.

No per-topic reference files, no directory nesting beyond the established
`knowledge/<domain>/<slug>.md` and `skills/<domain>/SKILL.md` conventions.

### 8. Routing: keyword-clustered, deterministic, load-minimum

Mirrors prior domains' `## Routing` section: frontmatter `routes:` is the
full flat set (all 12), body groups into task-keyword clusters.

Proposed clusters:
- Screen lifecycle & composition → `view-controller-lifecycle.md`,
  `view-controller-composition.md`
- Layout → `auto-layout-constraints.md`, `auto-layout-stack-views.md`,
  `safe-area-and-layout-guides.md`
- Navigation & presentation → `navigation-controller.md`,
  `tab-bar-controller.md`, `modal-presentation.md`
- Lists & grids → `table-view-diffable.md`,
  `collection-view-compositional-layout.md`, `collection-view-diffable.md`,
  `cell-configuration.md`

### 9. `domain-map.md` updates (part of this project, not a separate pass)

- `uikit` row's **Initial Scope** cell replaced with the real v1 scope
  (screen-scaffolding: lifecycle/composition, Auto Layout, navigation,
  diffable table/collection views, modal presentation; accessibility and
  SwiftUI interop out of scope — see Cross-Domain Notes).
- `uikit` row's **Owns** cell replaced correspondingly.
- **Build Order** section's "Completed" line gets `uikit` (screen-
  scaffolding core v1) appended once this ships.
- Three new Cross-Domain Notes entries: `uikit` ↔ `accessibility`,
  `uikit` ↔ `swiftui`, `uikit` ↔ `human-interface-guidelines`.

## Consequences

- Sixth full domain under the hardened native-skill pipeline.
- Third domain to use a non-empty `related:` in its Skill frontmatter, first
  to link to three other Skills (`accessibility`, `swiftui`,
  `human-interface-guidelines`).
- Fills in `domain-map.md`'s vaguest remaining Tier 1 entry with a concrete,
  bounded v1 scope.
- Adds 3 new Cross-Domain Notes entries, two of which record explicit future
  scope (UIKit↔SwiftUI interop; UIKit gestures/Core Animation/transitions)
  to be picked up in a later pass, not this one.
- No changes to `scripts/validate_artifact.py`, `docs/specifications/*`, or
  any hardening-project file — this project only produces new reference/
  knowledge/skill content plus documentation-only edits to `domain-map.md`.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py references/apple/uikit.md --type reference` — `PASS`.
- `python3 scripts/validate_artifact.py knowledge/uikit/<slug>.md --type knowledge` for all 12 files — all `PASS`.
- `python3 scripts/validate_artifact.py skills/uikit/SKILL.md --type skill` — `PASS`.
- `python3 -m unittest tests/test_validate_artifact.py -v` — full pass (no regressions).
- `claude plugin validate .` — confirms the new `SKILL.md` is discovered.
- `skills/index.md` Discovery Rules table gets a new row for `uikit`.
- `README.md` `## Skills` and `## What's New` sections updated per
  `CLAUDE.md`'s standing rule.
- Live `WebFetch`/`curl` verification of every cited Apple documentation URL
  during per-task review (established this session after catching a broken
  link and a fabricated symbol name in the `accessibility` domain).
- Manual invocation check in a fresh session (same caveat as prior domains —
  the harness enumerates skills at session start, so this can't be verified
  same-session).

## Out of Scope

- Accessibility API implementation — owned by `accessibility`.
- Gesture recognizers, Core Animation/CALayer, custom transitions/
  animations — future `uikit` scope, not this v1.
- UIKit↔SwiftUI interop (`UIHostingController`, `UIViewRepresentable`/
  `UIViewControllerRepresentable`) — future scope, domain owner undecided.
- Storyboard/XIB, `IBOutlet`/`IBAction` workflow — permanently out of scope
  (convention choice, not deferred).
- Classic (non-diffable) `UITableViewDataSource`/`UICollectionViewDataSource`
  `cellForRowAt` pattern — permanently out of scope (legacy convention).
- Design-level guidance (when to use tab bar vs nav stack, list vs grid) —
  owned by `human-interface-guidelines`, not duplicated here.
- Any change to already-hardened schema/validator/spec files.
- Any change to `swiftui`, `accessibility`, or `human-interface-guidelines`
  KC/Skill content files themselves (only `domain-map.md` Cross-Domain
  Notes is touched).
