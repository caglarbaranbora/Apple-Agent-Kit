# Human Interface Guidelines — Patterns & Components Expansion — Design Spec

Status: Draft
Version: 0.1.0
Date: 2026-08-05

## Purpose

Extend the existing `human-interface-guidelines` domain (currently
Foundations-only, Tier 1) with a curated subset of Apple's Patterns,
Components, and Inputs sections. This closes the highest-priority named
gap identified in the Tier 1 completion review (see
`docs/architecture/domain-map.md` line 19) — the design guidance most
frequently needed when building everyday iOS/iPadOS app UI (lists,
buttons, sheets, alerts, navigation bars, form controls) currently has
no Knowledge Contract coverage.

This is a scope expansion of an existing domain, not a new domain.

## Scope

### Platform

iOS/iPadOS only, matching Foundations and every other Tier 1 domain.

### Curated subset rationale

Patterns (~20+ topics), Components (~30+ topics), and Inputs (~10
topics, mostly iPad/tvOS/watchOS-specific) are collectively far larger
than Foundations (15 topics). Full ingestion was rejected — same
reasoning as the style-guide domain's curated-glossary decision
(RFC 0001, decision 9): this kit serves a coding agent writing
iOS/iPadOS app UI, not a full editorial catalog of every HIG page, and
low-usage topics (Charts, Drag and Drop, Workouts, Apple Pencil, Game
Controllers, Column Views, Steppers, etc.) would produce contracts no
skill would realistically route to yet.

### Included (v1) — 18 Knowledge Contracts

**Components + Inputs (12)**, one HIG page each:
`lists-and-tables`, `buttons`, `sheets`, `alerts`, `action-sheets`,
`navigation-bars`, `tab-bars`, `pickers`, `toggles`, `text-fields`,
`menus`, `touchscreen-gestures` (the sole Inputs topic included — the
only Inputs page relevant to typical touch-based iOS/iPadOS app UI;
folded into the Components skill rather than given a third skill for a
single contract).

**Patterns (6)**:
`onboarding`, `searching`, `settings`, `notifications`, `feedback`,
`undo-and-redo`.

Each contract covers the **design layer only**: when to use the
pattern/component, layout and sizing conventions, and HIG-stated
behavioral rules. Content angle mirrors the existing Foundations
contracts (e.g. `layout.md`, `color.md`) — not implementation code.

**Verification caveat**: `alerts` / `action-sheets` are listed as two
HIG pages based on prior knowledge of Apple's information architecture.
If, when the reference/knowledge-authoring subagent fetches the live
HIG (per RFC 0001 decision 5), Apple has since merged Action Sheets
into the Alerts page, these collapse into one `alerts.md` contract and
the count becomes 17. This is a content-authoring detail, not a scope
change, and does not require a spec revision.

### Excluded (v1, deferred — recorded in domain-map.md as remaining gap)

- Remaining Components topics: Column Views, Disclosure Controls,
  Sliders, Steppers, Toolbars, Popovers, Context Menus, Activity Views,
  Search Fields (as a component distinct from the Searching pattern),
  Path Controls, Outline Views, Boxes, Collections, Split Views,
  Sidebars, Content views (Charts, Gauges, Progress/Rating indicators),
  and others.
- Remaining Patterns topics: Charts, Drag and Drop, Entering Data,
  Full-Screen Experiences, Launching, Loading, Managing Accounts,
  Modality, Multitasking, Playing Audio, Printing, Ratings and Reviews,
  Sharing, Status, Syncing, Workouts, and others.
- Remaining Inputs topics: Action Button, Apple Pencil and Scribble,
  Camera Control, Focus and Selection, Game Controllers, Gyro and
  Accelerometer, Keyboards, Nearby Interactions, Pointing Devices,
  Remotes.
- Implementation code for any component (SwiftUI `Button`/`TextField`/
  `NavigationStack`, UIKit `UIButton`/`UITableView`/
  `UINavigationController`) — owned by `swiftui` and `uikit` domains.
- UI copy/wording for any of these screens or controls — owned by
  `style-guide`.
- Accessibility API implementation for these components (VoiceOver
  traits, labels) — owned by `accessibility`; this expansion's contracts
  may note a design-level accessibility consideration but do not restate
  `accessibility` domain Rules.

## Cross-Domain Boundaries

Same angle-split precedent used throughout the kit (design vs.
implementation vs. wording vs. review-consequence):

- **vs. `swiftui` / `uikit`** — clean handoff. This expansion's
  contracts own visual/layout design guidance (when to use a sheet vs.
  a full-screen cover, list row sizing conventions); `swiftui`/`uikit`
  own the API mechanics of building those views. No content overlap.
- **vs. `style-guide`** — clean handoff, same precedent as the existing
  Foundations skill's "route to `skill.style-guide.writing` for wording"
  stop condition, carried forward into both new skills.
- **vs. `accessibility`** — clean handoff. `accessibility`'s existing
  contracts (e.g. `element-grouping.md`, `custom-actions.md`) own the
  API-level accessibility implementation; this expansion does not
  restate those Rules.
- **vs. future Tier 2 `usernotifications` domain** — angle-split, flagged
  proactively since `notifications.md` (Patterns) covers notification
  *design* (content structure, when to request permission, grouping)
  while the future domain will cover `UNUserNotificationCenter` API
  implementation. Recorded as a new Cross-Domain Note in domain-map.md
  now so the boundary is pre-decided when `usernotifications` is built,
  following the same proactive-flagging precedent already used for the
  `privacy`/`testing`/`security` boundaries in domain-map.md.

## File Layout

Knowledge Contracts land in the existing domain directory (domain is
unchanged, only the routing layer splits):

```
knowledge/human-interface-guidelines/
  (15 existing Foundations files, unchanged)
  lists-and-tables.md, buttons.md, sheets.md, alerts.md,
  action-sheets.md, navigation-bars.md, tab-bars.md, pickers.md,
  toggles.md, text-fields.md, menus.md, touchscreen-gestures.md
  onboarding.md, searching.md, settings.md, notifications.md,
  feedback.md, undo-and-redo.md
```

Reference and Skill layers split by HIG section — required by the
project's hard size caps (Reference ≤80 lines, Skill ≤60 lines;
RFC 0001 decision 4). The existing Foundations reference (50/80 lines,
~2 lines/topic) and Foundations skill (48/60 lines) are already close
to cap at 15 topics; adding 18 more at the same density would push both
past their caps (reference to ~86 lines, skill to ~35-40 routing lines
alone). Splitting along Apple's own Foundations/Patterns/Components
information architecture is a principled boundary, not an arbitrary
one, and matches precedent: each HIG section becomes its own
Reference + Skill pair, same as any other domain, while sharing one
Knowledge directory:

```
references/apple/
  human-interface-guidelines.md              (existing, "out of scope"
                                               line removed)
  human-interface-guidelines-components.md   (new — 12 KCs)
  human-interface-guidelines-patterns.md     (new — 6 KCs)

skills/
  human-interface-guidelines/SKILL.md              (existing, unchanged)
  human-interface-guidelines-components/SKILL.md   (new)
  human-interface-guidelines-patterns/SKILL.md     (new)
```

All three skills cross-link via `related:` frontmatter. This is the
first domain in the kit with more than one Skill; it is treated as an
intentional, documented exception to the informal one-skill-per-domain
pattern, driven purely by the size caps, not by a domain boundary
change.

## Reference: `human-interface-guidelines-components.md`

Index into
https://developer.apple.com/design/human-interface-guidelines/ Component
and Input pages listed under Included above. Same structure as the
existing Foundations reference (Purpose, Primary Topics, Used By).

## Reference: `human-interface-guidelines-patterns.md`

Index into the Patterns pages listed under Included above. Same
structure.

## Skill: `skills/human-interface-guidelines-components/SKILL.md`

`id: skill.human-interface-guidelines.components`. Routes to the 12
Components/Inputs KCs. Routing clusters:

- List/table structure -> `lists-and-tables.md`
- Buttons and menu actions -> `buttons.md`, `menus.md`
- Modal presentation -> `sheets.md`, `alerts.md`, `action-sheets.md`
- Navigation chrome -> `navigation-bars.md`, `tab-bars.md`
- Form/input controls -> `pickers.md`, `toggles.md`, `text-fields.md`
- Touch gestures -> `touchscreen-gestures.md`

Stop condition: Foundations or Patterns topics route to the sibling
skill; topics outside all three (see Excluded list) report the gap
explicitly rather than answering from general knowledge — same pattern
as the existing Foundations skill's stop condition.

## Skill: `skills/human-interface-guidelines-patterns/SKILL.md`

`id: skill.human-interface-guidelines.patterns`. Routes to the 6
Patterns KCs. Routing clusters:

- First-run flow -> `onboarding.md`
- Search UI -> `searching.md`
- Settings screen structure -> `settings.md`
- Notification design -> `notifications.md`
- System/status feedback -> `feedback.md`
- Undo/redo affordances -> `undo-and-redo.md`

Same stop-condition pattern as the Components skill.

## Router Update: `skills/apple-agent-kit/SKILL.md`

Add both new skill IDs to the routing table with their trigger
keywords (lists, buttons, sheets, alerts, action sheet, navigation bar,
tab bar, picker, toggle, text field, menu, gesture, onboarding, search
UI, settings screen, notification design, feedback, undo, redo). The
existing `human-interface-guidelines` (Foundations) entry is unchanged.

## Documentation Updates

Per `CLAUDE.md`'s "Updating README.md" rule, same commit as the
domain work:

- `README.md` — two new Skills bullets (Components, Patterns) with
  concrete example invocations (e.g. `"review this list screen's
  layout against HIG" -> lists-and-tables.md`,
  `"design an onboarding flow" -> onboarding.md`); new top-of-list
  "What's New" line.
- `CHANGELOG.md` — new entry under `## [Unreleased]`.
- `docs/architecture/domain-map.md`:
  - Tier 1 "Completed:" line (line 19) — `human-interface-guidelines`
    clause rewritten from "Foundations subset only; Patterns/Components/
    Inputs remain unbuilt" to the detailed v1 scope wording, listing
    Excluded items as what remains unbuilt (matching every other
    completed Tier 1 row's phrasing).
  - New Cross-Domain Notes bullet for the `usernotifications` boundary
    (see above).
- `skills/index.md` — two new Discovery Rules rows (Components,
  Patterns), inserted adjacent to the existing
  `human-interface-guidelines` row.

## Validation

Same as every prior domain:

```bash
python3 scripts/validate_artifact.py <path> --type knowledge   # x18
python3 scripts/validate_artifact.py <path> --type skill       # x2
python3 scripts/validate_artifact.py <path> --type reference   # x2
python3 -m unittest tests/test_validate_artifact.py -v
claude plugin validate .
```

Line-cap check is part of validation for the two new Reference files
and two new Skill files given how close to cap this expansion runs by
design.

## Build Order

Reference → Knowledge (Components cluster, then Patterns cluster,
each reviewed as its own batch per RFC 0001 decision 5) → Skills →
Router update → Documentation → Validation. Components before Patterns
(no dependency between them; order chosen for build-time consistency
with the size ordering already established in this spec).

## Out of Scope for This Spec

- All Excluded-list topics above (remaining Components/Patterns/Inputs
  pages).
- The `swiftui` gestures/animation expansion — separate sub-project,
  brainstormed after this one completes (one-domain-at-a-time
  convention).
- Any Tier 2 domain work.
