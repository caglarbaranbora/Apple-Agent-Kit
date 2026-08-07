# v1 Finalization — Design

Status: Approved
Version: 1.0.0
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

### Carried into Phase 4

`scripts/validate_repo.py` reports exactly one finding against the repository:
`knowledge/authentication/accessibility-forms.md` declares `domain: Accessibility`
while sitting in `knowledge/authentication/`. The move is already listed as Phase 4
work and is entangled with the `authentication` Skill retirement, since moving the
Contract changes its id and therefore which Skill routes to it. It is left open
rather than suppressed: an allowlist in the validator is how a gate stops being one.

## Phase 5 — Tier 1 content completion

This is the goal, not a tail. The per-domain scope is **not yet decided** and requires
its own grilling round before Phase 5 is planned. Recorded here so it cannot be lost.

Gaps `docs/architecture/domain-map.md` declares against Tier 1:

| Domain | Declared unbuilt |
|---|---|
| `human-interface-guidelines` | Charts, Drag and Drop, Multitasking, Column Views, Sliders, Toolbars beyond navigation, Apple Pencil, Game Controllers |
| `app-store-review-guidelines` | Safety (1.x), most of Legal (5.x), Design 4.0, Guideline 4.8 |
| `swiftui` | Previews, custom `Layout` protocol conformances, legacy `ObservableObject`/`NavigationView` migration |
| `uikit` | Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, SwiftUI interop |
| `sf-symbols` | Symbol effects/animations, Symbol Composer authoring |
| `networking` | Completion-handler APIs, Combine, `URLSessionDelegate` background/progress/TLS |
| `xcode` | `xcodebuild` CLI, CI signing automation, SwiftPM build configuration — **plus two inherited hand-offs**: Test Plans and code coverage (deferred by `testing`), project language configuration and `.xcloc`/XLIFF (deferred by `localization`) |
| `accessibility`, `style-guide`, `local-authentication`, `app-tracking-transparency` | none — complete as declared |

Two questions must be grilled per domain before Phase 5 is planned:

1. Which of these are genuinely required for Tier 1 to be *complete*, and which are
   correctly-scoped v1 exclusions that should be restated as permanent rather than
   deferred? "Fully complete" is the goal, so the default answer is *build it* — but a
   deferral that is genuinely right (Storyboard/XIB was scoped out on purpose, not
   postponed) should be recorded as a decision, not silently carried.
2. What should be **removed** from each Skill — the question that opened this whole
   effort and has not yet been answered for any domain.

`xcode` carries the heaviest load: its own three gaps plus two hand-offs other domains
have already deferred to it. It is the strongest candidate to be scoped first.

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
- **Phase 5's scope is undecided**, and "fully complete Tier 1" could expand without a
  bound. The grilling round gated in front of it exists to set that bound explicitly.
