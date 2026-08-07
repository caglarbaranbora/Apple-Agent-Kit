# v1 Finalization — Design

Status: Approved
Version: 1.5.0
Date: 2026-08-07

## Goal

Complete Tier 1 and freeze the repository's structure and architecture, so that
"done" becomes a statement a tool can verify rather than a claim in prose.

Two co-equal outcomes:

1. **Tier 1 completion** — every Tier 1 domain finished to its declared scope, and
   every declared scope revisited so it is the *right* scope.
2. **Structure/architecture completion** — the rule corpus made self-consistent,
   the declared-but-unimplemented enforcement built, and the declared-but-empty
   Workflow layer made real.

The governance work is a prerequisite for the content work, not a substitute for it:
you cannot certify Tier 1 "complete" against a standard that contradicts itself in
nine places. The decisions recorded here are intended to carry forward — Tier 2 and
Tier 3 will be built and audited against exactly this standard.

## Non-goals

- Tier 3 domains. Suspended until this lands.
- Tier 2 content gaps (Live Activities, CloudKit sync, migration, Combine↔async
  interop, `NotificationCenter`/GCD, etc.). Deliberately deferred; they are
  scoped-out framework surface, not defects.
- Rewriting published historical records: `CHANGELOG.md` released entries,
  `validation/slices/0001/*`, `docs/superpowers/specs|plans/*` from prior sessions,
  and `rfcs/0001`. These are dated records, not live rules.

## Current state

An audit of all 295 artifacts plus the 19-document rule corpus was run
(`scripts/` equivalents are reproduced as permanent tooling in Phase 3).

**Content is disciplined.** Zero duplicate IDs, zero dangling `depends_on`/`related`/
`routes`, zero orphan Knowledge Contracts, zero line-cap violations, zero invalid
status values, `skills/index.md` ↔ `skills/` in sync both ways, `## Used By` 100%
consistent, no duplicate routing keywords across index rows.

**Governance is not.** The rule corpus contradicts itself, and almost none of it is
enforced:

| # | Contradiction |
|---|---|
| 1 | Metadata split into two dialects — `type`/`updated` (232 KCs, `metadata.schema.md`) vs. `artifact_type`/`last_updated` (32 skills, three spec docs) |
| 2 | Skill line cap declared 60 (`validation-model.md:24`) and 80 (`skill-spec.md:67`, validator) |
| 3 | Lifecycle declared with `Review` (`artifact-lifecycle.md:11`) and without it (`architecture.md:59`, `metadata.schema.md:17`) |
| 4 | Skill→Skill forbidden (`architecture.md:44`), unlisted (`linking-model.md`), silent (`dependency-graph.md`) — while 32/32 skills do it via `related:` |
| 5 | Knowledge→Knowledge allowed (`dependency-graph.md:16`), absent from `linking-model.md`'s allowed list — 67 live edges |
| 6 | Layer count 4 (`AGENTS.md`, `CLAUDE.md`, `README.md`) vs. 5 (`architecture.md`, +Templates) |
| 7 | Relative paths declared canonical (`linking-model.md:21`) — artifacts use zero of them; 31/31 references use wiki links |
| 8 | Routing model declares tag-based priority and transitive resolution; neither is built, and `tags:` has zero consumers |
| 9 | References have no spec at all — validator checks only a line cap, so an empty reference file passes |

**Enforcement gap.** ~55 check statements are declared across 8 documents. Three
kinds are implemented (line cap, required-section presence, required-metadata
presence). Value checking does not exist — `status: Banana` currently passes.
Levels 2-5 of `validation-model.md`, all marked `Blocking: Yes`, have zero code.

**Lifecycle never exercised.** 264/264 artifacts are `Draft`. Nothing has ever
transitioned. `Approved` has never meant anything in this repository.

**Workflow layer declared, empty.** `workflow-spec.md` was written in the founding
commit (`a79c499`, before any Knowledge Contract existed) for Phase 7, which has not
started. `AGENTS.md` advertises the layer to agents; `workflows/` holds one README.

## Decisions

Reached by grilling; the full record with measured facts is the decision log.

### Schema and identity

- **A1** One metadata dialect: `artifact_type` + `last_updated`. The spec layer wins
  3-to-1 over `metadata.schema.md`. 232 KCs are migrated mechanically.
- **A1b** Common base + per-type extension — the model `template-spec.md:39` already
  declares. Base, required for every artifact type: `id`, `artifact_type`, `title`,
  `version`, `status`, `domain`, `last_updated`. Knowledge extends with `owner`,
  `summary`, `tags`, `depends_on`, `related`, `references`. Skill extends with `name`,
  `description`, `routes`, `related`.
- **A2** Lifecycle is four states: `Draft` → `Approved` → `Deprecated` → `Archived`.
  `Review` is dropped — two of three documents already omitted it, and the pull
  request is the review.
- **A2b** Governance documents (`docs/`, `schemas/`, `templates/`) are artifacts under
  the same lifecycle. Every rule file rewritten by this effort exits as
  `Approved 1.0.0`, which makes `architecture.md:49` ("Architecture changes require
  RFC") an enforceable statement rather than an aspiration.
- **A3** Write `docs/specifications/reference-spec.md`. References gain a metadata
  block; required sections are `## Source`, `## Purpose`, `## Primary Topics`,
  `## Used By` (already uniform across 31/31). Reference line cap 80 → 98, since the
  largest reference is 78 lines and a metadata block adds ~10. The line-counting rule
  itself is unchanged for all types, so skills gain no headroom as a side effect.
- **A4** New artifact type `entry` for `skills/apple-agent-kit/SKILL.md`, which is the
  plugin entry point and fails the Skill schema on 12 counts because it is not a
  domain Skill. This fixes three roles in place: **Skill** routes to Knowledge
  Contracts only, **Workflow** composes Skills, **Entry** is the plugin entry point.

### Dependency and linking

- **B1** Edge semantics defined — this was the undefined term that made every graph
  rule unenforceable. `depends_on` is *the* binding dependency edge; DAG, direction
  bans and cycle detection apply to it alone. `related` is a non-binding
  cross-reference whose target must exist but carries no direction constraint.
  `routes` is a Skill→Knowledge load instruction, a separate category. This makes
  32/32 skills' `related: skill.x` legal without changing a file, and preserves
  `architecture.md:44` scoped to `depends_on`.
- **B2** *(consequence)* Knowledge→Knowledge `depends_on` is allowed; `linking-model.md`
  is the stale document.
- **B3** Templates are not a layer — they are an authoring aid, like `scripts/`. Four
  layers everywhere. `architecture.md` loses layer 5 and the "Skill → Template" edge;
  `templates/` and `template-spec.md` remain, as governance artifacts.
- **B4** Three linking conventions are codified as used rather than one declared
  canonical mechanism: metadata edges use **artifact IDs** (the graph's source of
  truth; IDs are immutable per `metadata.schema.md:55`), reference `## Used By` uses
  **wiki links** (31/31, and this repository lives in an Obsidian vault), document
  prose uses **relative paths** (`docs/` only; zero in artifacts).

### Routing

- **C1** `routing-model.md` is rewritten to describe the mechanism that exists: the
  `skills/index.md` keyword table selects one Skill, that Skill's `## Routing` section
  selects the Knowledge Contracts, and each loaded Contract's own `## Dependencies`
  section pulls anything further (232/232 Contracts have one; 0/32 Skills do).
  Tag-based routing leaves the model. `tags:` stays required but is explicitly
  redefined as search/Obsidian metadata and **not** a routing input.

### Enforcement

- **D1** *(consequence)* Skill line cap is 80; `validation-model.md:24` is stale.
- **D2** Levels 1-3 become code; Levels 4-5 become a review checklist with a defined
  procedure, because they are semantic and a naive implementation would produce noise
  that gets silenced.
  - Level 1 — `scripts/validate_artifact.py`, per file: extended to the `reference`,
    `entry` and `workflow` types, plus enum-value checking and version-format checking.
  - Levels 2-3 — `scripts/validate_repo.py`, new, repo-wide: ID uniqueness, ID/path
    consistency, domain consistency, resolution of all three link kinds, DAG over
    `depends_on`, orphan detection, index sync, layer direction rules.
  - Both wired into `tests/`.

### Workflow layer (Phase 7)

- **E1** `skills/index.md` becomes the single **Routing Index**, with a Workflows table
  above the Skills table. Its Resolution Rules are rewritten: if the task matches a
  Workflow trigger, load that Workflow, which names its Skills in order; otherwise
  load exactly one Skill. This retires the `index.md:49` rule that currently forbids
  multi-Skill tasks outright.
- **E1b** Three first instances, chosen for three different shapes so the spec is not
  fitted to one example:
  - `authentication` — style-guide → accessibility → authenticationservices →
    local-authentication → security. Fan-out across five domains.
  - `app-store-submission` — xcode → app-store-review-guidelines → privacy.
    Sequential and gated, which exercises `Exit Conditions` properly.
  - `add-widget` — widgetkit → app-intents → backgroundtasks. Composes three
    hand-offs whose boundaries `domain-map.md` has already resolved.
  - `make-screen-accessible` is deferred; it is structurally the same as the others.

### Skill management

- **S1** A domain gets more than one Skill on **topical coherence**, not size: when its
  Knowledge divides into task families that one `## Routing` section cannot
  discriminate cleanly. The 80-line cap stays a hard ceiling but is not the trigger —
  no Skill is near it (largest is 56). This retroactively justifies the existing
  three-way `human-interface-guidelines` and two-way `swiftui` splits, whose real
  rationale was never written down.
- **S2** Layout is always flat: `skills/<domain>[-<facet>]/SKILL.md`. Claude Code
  derives the invocable Skill name from the directory, so `skill-spec.md:19-20`'s
  nested option is removed — zero nested files exist and the nesting would break
  discovery. The ID is `skill.<domain>.<facet>`, with the facet derivable from the
  directory name by stripping the domain prefix, which makes it validator-checkable.
  `foundations` is the default facet for a domain's primary Skill but is not
  mandatory, so `writing` and `submission` stay valid and `metadata.schema.md:55`'s
  ID-immutability rule is not violated.
- **S3** New `docs/specifications/skill-management.md`: when a Skill is created (S1),
  identity and layout (S2), the checklist for adding a Knowledge Contract to an
  existing Skill, splitting, retiring (`authentication` is the first case ever),
  `skills/index.md` maintenance, and the relationship to Workflows.

### Naming corrections

- **F1** `naming-conventions.md:78` reserves the name "test" while `tests/` exists —
  scope the reserved list to artifact filenames.
- **F2** `naming-conventions.md:14` requires singular nouns, which is violated by
  design throughout — collection directories are plural, artifact names describe their
  topic naturally.

## Phasing

| Phase | Content | Touches |
|---|---|---|
| 1 | Rule corpus reconciliation — 17 documents rewritten, 2 new specs | `docs/`, `schemas/`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` |
| 2 | Metadata migration — 232 KCs renamed, 31 references gain metadata blocks | `knowledge/`, `references/` |
| 3 | Validator Levels 1-3 + tests | `scripts/`, `tests/` |
| 4 | Workflow layer — `entry` type, Routing Index, 3 workflows, `authentication` retirement | `skills/`, `workflows/`, `knowledge/` |
| 5 | **Tier 1 content completion** | `references/`, `knowledge/`, `skills/` |
| 6 | Draft → Approved promotion | everything |

Phase 1 is documents only and changes no artifact. Phase 2 is mechanical and
scriptable, with a large diff and zero semantic change. Phase 3 makes 1 and 2
enforceable.

Phases 1-3 ship as one pull request. Phase 3 is what makes Phases 1 and 2
checkable, so reviewing them apart would mean reviewing rules with nothing
enforcing them. Phases 4-6 are separate pull requests.

### Carried into Phase 4 — resolved

`scripts/validate_repo.py` reported exactly one finding against the repository:
`knowledge/authentication/accessibility-forms.md` declared `domain: Accessibility`
while sitting in `knowledge/authentication/`. It was left open rather than suppressed,
on the grounds that an allowlist in the validator is how a gate stops being one.

Phase 4 closed it, but not by the move E1b assumed. Three of the Contract's four rules
were already owned in `knowledge/accessibility/` in far more depth, and all four named
no API, which every Contract in that directory does — moving it as written would have
planted a quality outlier in the repository's strongest domain. The Contract was
retired with the rest of the domain, and its one genuinely uncovered rule (announcing
form validation errors to assistive technologies) is recorded in `domain-map.md` as a
Tier 1 `accessibility` gap for Phase 5, where PR 3 closed it as
`knowledge.accessibility.accessibility-announcements` on 2026-08-07. The validator now
passes with zero findings.

### Deviations taken in Phase 4

E1b sketched `app-store-submission` as `xcode → app-store-review-guidelines → privacy`.
Built order is `app-store-review-guidelines → privacy → xcode`. A gated Workflow must
put the cheap checks first: the sketched order has an agent produce a signed archive and
only then discover that the privacy manifest shipped inside it is wrong, which costs a
rebuild per finding. The Workflow states the reordering and its reason inline.

## Phase 5 — Tier 1 content completion

This is the goal, not a tail. Its scope was decided by the grilling round recorded
below, held 2026-08-07 after Phase 4 merged.

Gaps `docs/architecture/domain-map.md` declares against Tier 1:

| Domain | Declared unbuilt |
|---|---|
| `human-interface-guidelines` | Charts, Drag and Drop, Multitasking, Column Views, Sliders, Toolbars beyond navigation, Apple Pencil, Game Controllers |
| `app-store-review-guidelines` | Safety (1.x), most of Legal (5.x), Design 4.0, Guideline 4.8 |
| `swiftui` | Previews, custom `Layout` protocol conformances (both **Excluded**), legacy `ObservableObject`/`NavigationView` migration — **closed in PR 4, 2026-08-07** |
| `uikit` | Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, SwiftUI interop |
| `sf-symbols` | Symbol effects/animations, Symbol Composer authoring |
| `networking` | Completion-handler APIs, Combine, `URLSessionDelegate` background/progress/TLS — **closed in PR 5, 2026-08-07** |
| `xcode` | `xcodebuild` CLI, CI signing automation, SwiftPM build configuration — **plus two inherited hand-offs**: Test Plans and code coverage (deferred by `testing`), project language configuration and `.xcloc`/XLIFF (deferred by `localization`). **Both closed in PR 2, 2026-08-07.** |
| `accessibility` | none from its own scoping — **plus one inherited hand-off**: announcing a validation result to assistive apps, surfaced by the `authentication` retirement. **Closed in PR 3, 2026-08-07.** |
| `style-guide`, `local-authentication`, `app-tracking-transparency` | none — complete as declared |

### Scope, decided 2026-08-07

The grilling round this section gated has been held. Its outcome:

**"Tier 1 complete" means task-complete.** A domain is complete when the tasks its
Skill claims to route can actually be carried out. Coverage-completeness — a Contract
for every topic the map calls unbuilt — was rejected as unbounded.

**A gap is required if any of four clauses holds:**

| | Clause |
|---|---|
| (i) | Another artifact defers to it — a broken edge inside the repository |
| (ii) | The domain's own Skill `description`/triggers already advertise the surface |
| (iii) | An agent editing an *existing* iOS app hits it |
| (iv) | Its silence causes concrete harm — App Store rejection, data leak, inaccessible UI — applied **per rule**, and only where the rule meets Tier 1's own bar of "nearly every iOS app" |

Otherwise the gap is a **permanent exclusion**. A gap that is merely *vertical* is
moved to Tier 3 instead, which is not the same thing as excluding it.

Clause (iii) is the consequential one. The repository is greenfield-biased — iOS 17+,
SwiftUI-first, async/await-only — while most of the declared gaps are brownfield
surface. `uikit`'s existence is itself a brownfield bet: a new iOS 17+ app has no
reason to reach for UIKit, so the domain exists because agents work in codebases that
already do. Excluding legacy surface from it contradicts why it is there.

Clause (iv) was added because (i)-(iii) produced a mechanically correct but
indefensible result: App Store Review Guideline 1.x (Safety) would have been recorded
as a permanent exclusion, leaving the kit silent on the single largest category of App
Store rejections. The Tier 1 filter inside (iv) is what keeps it bounded — 1.2
(user-generated content) is near-universal; 1.3 (Kids), 1.4 (physical harm), 5.3
(gambling), 5.4 (VPN) and 5.5 (MDM) are vertical and move to Tier 3.

**Two corrections to the gap table above**, found while applying the test:

- `uikit`'s Storyboard/XIB entry is not a gap. `skills/uikit/SKILL.md` already records
  it as "permanently out of scope", distinct from the four items it calls "deferred to
  future scope". The table flattened a distinction the Skill had drawn.
- `swiftui`'s `ObservableObject` entry is an over-promise, not merely a gap: the
  Skill's `description` trigger list names `ObservableObject`, pulling the task in,
  and the Stop Conditions then refuse it. **Resolved in PR 4, 2026-08-07**, by
  building the Contracts rather than by narrowing the trigger list.

Ownership decided: Combine's `dataTaskPublisher` goes to `networking`, not `combine`.
Routing matches tasks, not frameworks, and an agent asking about it is making an HTTP
request. This costs `combine` a cross-domain note and keeps Phase 5 inside Tier 1.

### Phase 5's shape

`docs/architecture/domain-map.md` states the build rule: "One domain is fully finished
(Reference → Knowledge → Skill → Validation) before the next domain starts." That
governs. **The framing of Phases 4-6 as one pull request each does not survive it** —
Phase 5 touches six domains and ships as one PR per domain.

| PR | Content | ~KC |
|---|---|---|
| 0 | Retired-domain prose hand-offs, and the check that catches them | 0 |
| 1 | Scope-vocabulary revision: `Excluded (permanent)` vs `Deferred (planned)`, enforced; the two corrections above; the Tier 3 reclassifications | 0 |
| 2 | `xcode` — Test Plans and coverage, `.xcloc`/XLIFF and project language *(both inherited)* — **shipped 2026-08-07, 4 KC** | 4-5 |
| 3 | `accessibility` — validation errors announced to assistive technologies — **shipped 2026-08-07, 1 KC** | 1-2 |
| 4 | `swiftui` — `ObservableObject`/`NavigationView` migration — **shipped 2026-08-07, 2 KC** | 2 |
| 5 | `networking` — completion-handler, `URLSessionDelegate`, `dataTaskPublisher` — **shipped 2026-08-07, 7 KC** | 5-6 |
| 6 | `uikit` — gesture recognizers, Core Animation and custom transitions, SwiftUI interop | 6-7 |
| 7 | `app-store-review-guidelines` — 1.2, 1.5, 1.6, 4.1, 4.8, 5.2 | 8-10 |

Broken edges first, largest last. PRs 0 and 1 add no content; they make the base
truthful before anything is built on it.

### Observed in PR 2

The estimate held: 4 Contracts, at the low end of 4-5. Two things the plan did not
anticipate, both worth carrying into PRs 3-7.

`references/apple/xcode.md` carried a single hub URL while its eight Contracts cited
deep pages. `used-by-complete` matches by URL, so the domain's entire reverse index was
outside the check — `## Used By` was hand-maintained prose that happened to be right.
Listing the real source URLs put it under enforcement, which immediately found a missing
row. **Before adding Contracts to a domain, check whether its Reference indexes URLs at
all**; a Reference that indexes nothing makes the check silently vacuous for that domain,
which is the PR 0 lesson in a different place.

`localization` and `testing` had both marked this surface `Deferred`, and PR 1 had added
the matching `Deferred` markers on `xcode`'s side. Building it invalidated all of them at
once — four scope statements across two Skills and two Contracts. **A PR that builds a
deferred topic must revisit every artifact that deferred it**, and nothing mechanical
catches this: `scope-vocabulary` verifies that a named domain exists, not that a topic
inside it is still unbuilt.

### Observed in PR 3

One Contract, at the low end of 1-2, and for a reason worth stating: the second
candidate would have restated a neighbour. `full-keyboard-access-and-focus` Rule 2
already owns `.screenChanged` with an element argument and moving VoiceOver focus to a
field that failed validation. A Contract covering the layout- and screen-change
notifications would have re-litigated that ownership for the sake of hitting an
estimate. **The recorded gap is the deliverable, not the API surface around it.**

Closing the gap exposed a smaller one. `AccessibilityNotification` has four cases;
`Announcement` is now owned and `ScreenChanged`-with-focus was already owned, which
leaves `LayoutChanged` and `PageScrolled` visibly unowned for the first time. Recorded
as `Deferred` in `skills/accessibility/SKILL.md` rather than absorbed to look complete.

`domain-map.md` recorded the gap's API as "`UIAccessibility.post(.announcement:)` /
`AccessibilityNotification.Announcement`" with no module. `AccessibilityNotification` is
published under Apple's **Accessibility** framework, not SwiftUI, even though Apple's own
example for it is SwiftUI code, and it is iOS 17+ while `UIAccessibility.post` goes back
to iOS 4. A gap recorded as two API names side by side hid a version boundary and a
framework boundary.

**PR 2's Reference finding is systemic, not an `xcode` accident.** The same defect was
present in `accessibility` — 1 URL indexed, 33 cited across 12 Contracts. Measured across
all 31 References, **9 index two URLs or fewer while their own Contracts cite more than
two**, so `used-by-complete` is vacuous on all 9:

| Reference | URLs indexed | URLs its Contracts cite |
|---|---|---|
| `swiftui` — **fixed in PR 4, 2026-08-07** | 1 | 50 |
| `uikit` | 1 | 34 |
| `human-interface-guidelines` | 1 | 33 |
| `usernotifications` | 2 | 26 |
| `sf-symbols` | 1 | 15 |
| `networking` — **fixed in PR 5, 2026-08-07** | 1 | 13 |
| `local-authentication` | 1 | 9 |
| `app-tracking-transparency` | 2 | 5 |
| `app-store-review-guidelines` | 1 | 3 |

PRs 4-7 cover `swiftui`, `networking`, `uikit`, and `app-store-review-guidelines` by
construction, and each MUST index its Reference before adding Contracts. The remaining
five — `human-interface-guidelines`, `usernotifications`, `sf-symbols`,
`local-authentication`, `app-tracking-transparency` — are on no Phase 5 PR's path and
need a pass of their own. Not folded into an `accessibility` PR: rewriting nine
References under an unrelated heading is how a scoped PR stops being reviewable.

**Corrected in PR 5:** the table above answers a narrower question than it reads as.
Its selection rule is "indexes two URLs or fewer while citing more than two" — the set
on which `used-by-complete` is *vacuous*. It is not the set of References with an
unindexed citation. Re-measured on 2026-08-07 across every domain, **17 References cite
at least one URL no Reference indexes**, and ten of them are recorded nowhere:

| Reference | Cited URLs not indexed anywhere |
|---|---|
| `security` | 12 of 19 |
| `localization` | 7 of 44 |
| `privacy` | 6 of 11 |
| `eventkit` | 4 of 23 |
| `tipkit` | 3 of 31 |
| `testing` | 2 of 23 |
| `storekit`, `style-guide`, `swiftdata`, `widgetkit` | 1 each |

The mechanism is the same in all of them and is worth stating plainly, because it is
what makes partial gaps invisible rather than merely smaller. `check_used_by_is_complete`
walks `## Source` URLs and asks which Contracts cite each one. A URL that **no**
Reference indexes resolves to an empty list and touches no check at all. Indexing
coverage is therefore unenforceable by construction: the check can only verify the
reverse index of what is already indexed. `security` at 12 unindexed of 19 cited is not
a rounding error, and nothing in the repository would ever have reported it.

The Reference pass this implies is larger than "the remaining five" and is still not
foldable into a domain PR. It also wants a sixteenth check — one that reads Contract
`references:` and reports any URL no Reference indexes — which is the only thing that
would make coverage enforceable rather than periodically re-measured by hand.

Guideline 4.8 satisfies clause (i) as well as (iv): `workflow.authentication`, shipped
in Phase 4, walks an agent through building a sign-in screen across five domains and
none of them mentions that omitting Sign in with Apple is a rejection under 4.8. The
Workflow does not know the rule that can reject its own output.

**Deliberately left open**, to be settled when PR 7 is scoped rather than assumed
here: whether Guideline 4.4 (extensions) satisfies clause (i) via `widgetkit`; whether
1.1 belongs in Tier 1 once 1.2 covers its actionable half; and the classification of
4.5, 4.6, 4.7 and 5.6.

### Observed in PR 4

**The `swiftui` Reference was not merely unindexed — it was a half-finished split.**
`reference-spec.md` states "One Reference per Skill-scoped domain," and `swiftui` has
had two Skills since its Animation/Gestures v1 shipped. It had one Reference. The
defect was invisible while that Reference indexed a single hub URL; indexing the real
56 made it unmissable, because the four sections then need 118 lines against a 98-line
cap. The spec already answers this — "If a domain's sources do not fit, split the
domain's Skill and give each Skill its own Reference" — and the Skill split had already
happened, so PR 4 wrote `references/apple/swiftui-interaction.md` and narrowed
`references/apple/swiftui.md` to the foundations surface. The two URL sets partition
cleanly with **zero overlap**, which is evidence the Skill boundary was drawn in the
right place, not just a convenient result.

The general lesson: **a Reference that indexes one hub URL hides more than a broken
`used-by-complete` check.** It also hides whether the domain still fits in one
Reference at all. The five References still on the list should be checked for the same
thing, not only refilled.

**Two migrations, two platform floors, one recorded gap.** `domain-map.md` recorded
"legacy `ObservableObject`/`NavigationView` migration" as a single deferred item. They
are not one task: Observation requires iOS 17/macOS 14, the navigation containers
require iOS 16/macOS 13, and a deployment target can permit one and refuse the other.
Both Contracts now state their own floor and cross-reference the other's. This is the
same failure shape PR 3 recorded — a gap written as a list of API names loses the
boundaries between them — and it is now the second consecutive PR to find it. The gap
table is a list of names, and names do not carry versions.

**The over-promise was resolved by building, not by narrowing.** The `swiftui` Skill's
`description` named `ObservableObject` as a trigger while its Stop Conditions refused
the task. Both directions were available: cut the trigger, or build the Contract. PR 4
built it, because the trigger was right — an agent asking about `ObservableObject` in
2026 is almost always holding existing code, which is exactly the task. A Skill that
attracts the right task and then refuses it is under-built, not over-scoped.

**Closing this gap assigned a boundary the map had left unowned.** `domain-map.md`
called UIKit-SwiftUI interop "future scope for whichever domain builds it — not yet
assigned," while `skills/uikit/SKILL.md` had already carried it as Deferred. The map
and the Skill disagreed, and nothing detects that: `scope-vocabulary` checks a Skill's
markers against reality, not against the map's prose. PR 4 assigned it to `uikit` and
made `skills/swiftui/SKILL.md` hand off there by name.

### Observed in PR 5

**The Reference fits in one file, at exactly the cap.** PR 4's lesson said the five
remaining under-indexed References should be checked for a half-finished split, not
just refilled. `networking` was checked and does not need one: its 15 Contracts cite 29
distinct URLs, and the indexed Reference is **98 lines against a 98-line cap**. That is
a pass with no headroom. Recording it rather than trimming prose to manufacture slack
is deliberate — the next Contract added to `networking` will fail Level 1, which forces
the split decision at the moment it becomes real instead of letting the file quietly
grow past the point where it was answerable. If that happens, the seam is the
async/await request path against the delegate-driven surface; the two share only the
`URLSession` hub, `URLSessionConfiguration`, and the ATS article, so a split would be
clean. It is not taken now because `reference-spec.md` ties Reference count to Skill
count, and splitting the Skill would need a topical-coherence argument (S1) that this
domain does not yet support: `authenticated-requests` and `authentication-challenges`
are both "authentication in networking," and two Skills whose descriptions both match
that phrase is a worse defect than a full Reference.

**The estimate was 5-6 Contracts; PR 5 shipped 7.** The overrun is not scope creep. The
Skill's Stop Conditions listed three deferred items, and the third — "`URLSessionDelegate`-based
background transfer, progress tracking, and custom TLS/challenge handling" — names
three sub-topics inside one bullet, then needs a fourth Contract (`url-session-delegate`)
underneath them to own delegate lifetime, which none of the three could hold alone.
This is the **third consecutive PR** where a gap's recorded name concealed its real
shape: PR 3 and PR 4 each found a version boundary hidden inside a name, and PR 5 found
a Contract count hidden inside one. The gap table sizes work by counting names.

**Four of the seven Contracts document a defect with no failure signal**, which is a
higher proportion than any prior PR in this phase. A delegate session that is never
invalidated leaks for the process lifetime while every request succeeds; a task that is
never `resume()`d produces no error, no warning, and no callback; an unconditional
`.useCredential(URLCredential(trust:))` accepts every certificate from every host and
passes every test; a discarded `AnyCancellable` cancels the request without calling the
completion closure. `URLSession`'s delegate surface is old API whose failure modes
predate the compiler diagnostics that would now catch them, so "it builds and the
requests work" is worth less here than anywhere else in the kit.

**The check that should have caught PR 5's stale hand-off had two holes, and the
smaller one was the obvious one.** `check_prose_domain_mentions_resolve` skipped
`docs/architecture/domain-map.md` outright, on the stated grounds that "recording a
retirement is the one place a retired name must still appear" — and the networking Tier
1 row was still reading "Sign-in UX owned by `authentication`", a live routing hand-off
to a domain retired in Phase 4, sitting in the one file nothing scanned.

Removing that exemption alone would not have caught it. Both mention regexes anchor on
a trailing "domain"/"skill"/"workflow" noun, and ``owned by `authentication` `` has
none. That phrasing is not incidental: it is the scope vocabulary's **own** hand-off
form, defined in PR 1 and used 57 times across the repository — the single most common
hand-off shape, and the one shape no check could see. Both holes are closed in PR 5:

- `describes_a_retirement()` becomes `describes_a_former_domain()`. Retirement is not
  the only way a domain stops existing — `design` was split by rfcs/0001 and the map
  still records that — so the predicate is "this sentence is history", over a small
  explicit verb list. Its sentence bounds now break on a blank line as well as a
  period, because a table row and the paragraph after it are not one sentence and a
  status cell reading "**Retired 2026-08-07**" was leaking its verb forward.
- A third regex matches the ownership form directly, and `domain-map.md` is scanned
  like every other file.

**Turning it on surfaced four live defects, two of them written by the passes that
introduced the vocabulary.** Two were genuine stale routing: the map's
`authenticationservices` entry, and `knowledge/authenticationservices/sign-in-with-apple-request-and-credential.md`,
which had carried ``owned by `authentication` `` in its Excluded section since before
the retirement — a Contract telling agents to consult a domain that no longer exists,
which is exactly the defect class PR 0 was written to eliminate and which it missed
because nothing could see this phrasing. The other two were marker misuse: PR 3 and PR
4 each wrote ``owned by `<contract>` `` where the target is a **sibling Contract**, not
a domain. `owned by` is reserved for cross-domain hand-offs; an intra-domain one is
"see `x`". Both files used the correct form on adjacent lines, which is what a
vocabulary with no enforcement produces — right most of the time, wrong silently.

### Deviation taken in PR 1

The grilling round settled on two terms, `Excluded (permanent)` and `Deferred
(planned)`. The Skills turned out to state a third fact as often as either: that
another domain owns the topic outright. Marking a hand-off `Excluded` would be false —
the kit does cover it — and marking it `Deferred` falser still.

So the vocabulary has three markers, of which two are the agreed pair. A hand-off is
not an exclusion; it is routing, and `prose-domain-resolves` was already enforcing it
from PR 0. Naming it alongside the other two is what stops the next author from
reaching for the wrong one, which is the entire failure this vocabulary exists to
prevent.

### Phase 5b — removal

The second question — what should be **removed** from each Skill — is answered in its
own phase, after Tier 1 is content-complete, and Phase 6 moves behind it.

Removal has no mechanical detector. The "names no API" heuristic that justified
retiring `accessibility-forms` in Phase 4 does not generalize: 70 of the 176 Tier 1
Contracts name no API, and `human-interface-guidelines` (design), `style-guide`
(wording), `app-store-review-guidelines` (policy) and much of `xcode` (GUI
configuration) are legitimately not API domains. The real standard is that a Contract
be decidable in its own domain's terms, and no script decides that — Levels 4-5 say so
already.

Sequencing is the argument for a separate phase: a Contract's redundancy is only
visible once its neighbours exist. Whether `human-interface-guidelines`'
`touchscreen-gestures` is duplicated cannot be judged before `uikit`'s gesture
Contracts are written. `human-interface-guidelines` (33 Contracts) and `style-guide`
(25) carry the read-through and neither has a content gap, so nothing else brings a
PR to them.

## Validation plan

- Every rewritten and new artifact passes `scripts/validate_artifact.py`.
- From Phase 3, `scripts/validate_repo.py` passes repo-wide.
- `python3 -m unittest discover tests/` passes.
- `claude plugin validate .` passes.
- Five-file release-version consistency holds (`README.md`, `npx/README.md`,
  `npx/package.json`, `.claude-plugin/plugin.json`, `CHANGELOG.md`).
- `diff README.md npx/README.md` is empty.

## Risks

- **Phase 2's diff is large** (263 files). Mitigated by making it mechanical,
  scriptable, and separate from every semantic change, so review is a script review.
- **`validate_repo.py`'s `## Used By` check must model reference↔knowledge as
  many-to-many.** A directory-derived check produces false positives — this was
  demonstrated during the audit, where `human-interface-guidelines` (three references
  sharing one knowledge directory) and `style-guide` (legitimate cross-domain
  citations) both looked broken and were not.
- **Traceability (Level 4) cannot be regexed.** URL depth does not separate a useless
  hub from a real framework landing page. It stays a review-checklist item.
- ~~**Phase 5's scope is undecided**~~ — retired 2026-08-07. The grilling round was
  held and the bound is the four-clause test above. The residual risk moved rather
  than closed: clause (iv) is the one that admits judgment, which is why it is applied
  per rule and filtered by Tier 1's own definition rather than per guideline block.
