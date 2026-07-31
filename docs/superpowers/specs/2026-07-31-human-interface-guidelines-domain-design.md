# Human Interface Guidelines Domain — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Add `human-interface-guidelines` as the first new domain built since the
Native Skill Foundation Hardening project (PR #4). Validates that the
hardened native-skill pipeline (References → Knowledge → Skills, real
`SKILL.md` frontmatter, `scripts/validate_artifact.py` schema) works for a
second, larger domain — and delivers real value: HIG governs nearly every
UI decision, so it's Tier 1 in `docs/architecture/domain-map.md`.

## Context

Apple's Human Interface Guidelines (`developer.apple.com/design/human-interface-guidelines`)
is a single multiplatform document covering four top-level sections:
**Foundations** (18 topics), **Patterns** (25 topics), **Components**
(8 topic groups, dozens of sub-components), **Inputs** (13 topics, mostly
platform-specific hardware). Confirmed by fetching Apple's own
documentation JSON index (`developer.apple.com/tutorials/data/design/...`)
— this is roughly 5-10x the surface area `style-guide` covered in its first
pass (~25 knowledge contracts from one page).

## Decisions

### 1. Scope: Foundations only, iOS/iPadOS only, v1

Patterns, Components, and Inputs are explicitly out of scope for this pass
— tracked as required follow-up work in domain-map.md (Decision 6), not
dropped. Foundations was chosen because it's the layer every other HIG
section and most other domains' UI guidance will eventually reference
(mirrors why `style-guide` and `authentication` were built early: high
reuse value for later domains).

visionOS-only Foundations topics are excluded (contradict the "iOS/iPadOS
only" platform decision, and this repo's stated goal is an iOS kit):
- **Immersive experiences** — spatial computing, no iOS equivalent
- **Spatial layout** — spatial computing, no iOS equivalent

One Foundations topic is excluded for ownership, not platform, reasons:
- **Writing** — already fully owned by the `style-guide` domain
  (`domain-map.md` Owns: "UI copy wording, capitalization rules,
  punctuation, inclusive writing"). Including it here would violate
  `domain-map.md`'s own "No duplicate ownership" validation rule. Any task
  needing HIG's Writing guidance routes to `style-guide` instead — the new
  skill's `related:` field points there.

**Final v1 scope: 15 Knowledge Contracts**, all under
`knowledge/human-interface-guidelines/`:

1. `accessibility` — design-level accessibility (Dynamic Type, contrast, VoiceOver-friendly layout)
2. `app-icons`
3. `branding`
4. `color`
5. `dark-mode`
6. `icons`
7. `images`
8. `inclusion`
9. `layout`
10. `materials`
11. `motion`
12. `privacy` — design-level transparency/consent UI patterns
13. `right-to-left`
14. `sf-symbols` — when/how to choose and compose symbols in a design
15. `typography`

### 2. Cross-domain overlap: accept, document, resolve later

Three of the 15 topics overlap conceptually with future domains already in
`domain-map.md`:

- `accessibility` (HIG) vs. future `accessibility` domain (Tier 1,
  unbuilt): HIG's angle is design guidance, the dedicated domain's angle is
  API implementation.
- `privacy` (HIG) vs. future `privacy` domain (Tier 2, unbuilt): HIG's
  angle is UI/consent-flow design, the dedicated domain's angle is privacy
  manifest / data-use disclosure implementation.
- `sf-symbols` (HIG) vs. future `sf-symbols` domain (Tier 1, unbuilt): HIG's
  angle is symbol selection/composition in a design, the dedicated domain's
  angle is API usage and rendering modes.

Same pattern already accepted in `domain-map.md` for
`authentication`/`authenticationservices`/`sign-in-with-apple`: overlap is
fine, boundary gets resolved when the second domain in the pair is
actually built. Three new Cross-Domain Notes entries are added for these.

### 3. File layout: mirrors `style-guide`, no new pattern

- **Reference:** one file, `references/apple/human-interface-guidelines.md`
  — same shape as `references/apple/style-guide.md` (Source, Purpose,
  Primary Topics, Used By listing all 15 knowledge contracts). Source URL:
  `https://developer.apple.com/design/human-interface-guidelines/foundations`.
- **Knowledge:** 15 files under `knowledge/human-interface-guidelines/`,
  one per topic above, each following the existing knowledge-contract
  format (`## Metadata` fenced YAML block — id/type/title/version/status/
  owner/summary/domain/tags/references/depends_on/related/updated — plus
  `## Intent`, `## Rules`, `## Compliant Example`, `## Non-Compliant
  Example`; 150-line cap). `domain: Human Interface Guidelines` in each.
- **Skill:** one native skill, `skills/human-interface-guidelines/SKILL.md`,
  post-hardening format (frontmatter `name`/`description`/`id: skill.human-
  interface-guidelines.foundations`/`title`/`version`/`status`/
  `artifact_type`/`domain`/`routes:` [15 ids]/`related: [skill.style-guide.
  writing]`/`last_updated`; body `## Purpose`, `## Routing`, `## Stop
  Conditions`; 80-line cap).

No per-topic reference files, no directory nesting beyond the established
`knowledge/<domain>/<slug>.md` and `skills/<domain>/SKILL.md` conventions.

### 4. Routing: keyword-clustered, deterministic, load-minimum

Mirrors `skills/style-guide/SKILL.md`'s `## Routing` section exactly: the
frontmatter `routes:` list is the full flat set (all 15), but the body
groups them into task-keyword clusters so the agent loads only what's
relevant to the specific question — never the full 15 for a single-topic
question.

Proposed clusters:
- Visual identity / iconography → `branding.md`, `app-icons.md`, `icons.md`, `images.md`
- Color & appearance → `color.md`, `dark-mode.md`
- Layout & structure → `layout.md`, `right-to-left.md`
- Typography → `typography.md`
- Materials & motion → `materials.md`, `motion.md`
- Accessibility & inclusion (design-level) → `accessibility.md`, `inclusion.md`
- Privacy (design-level) → `privacy.md`
- Symbol design system → `sf-symbols.md`

### 5. `domain-map.md` updates (part of this project, not a separate pass)

- `human-interface-guidelines` row's **Initial Scope** cell updated from
  the current broad text to: "Foundations (iOS/iPadOS): layout, color,
  typography, accessibility-design, dark mode, materials, motion, icons,
  branding, privacy-design, SF Symbols usage, RTL. Patterns/Components/
  Inputs deferred — see domain-map Cross-Domain Notes."
- Three new Cross-Domain Notes entries (Decision 2 above).
- **Build Order** section's "Completed" line gets `human-interface-
  guidelines (Foundations subset)` appended once this ships.

## Consequences

- Establishes the second full domain under the hardened native-skill
  pipeline — validates the pipeline generalizes beyond `style-guide`/
  `authentication`.
- Patterns (25 topics), Components (8 groups), Inputs (13 topics) remain
  explicitly unbuilt. Not silently dropped: `domain-map.md`'s Initial Scope
  cell and this spec both record them as deferred, so future work has a
  paper trail instead of rediscovering the full HIG surface from scratch.
- Adds 3 new Cross-Domain Notes entries that must be checked when
  `accessibility`, `privacy`, or `sf-symbols` domains are eventually built.
- No changes to `scripts/validate_artifact.py`, `docs/specifications/*`, or
  any hardening-project file — this project only produces new
  reference/knowledge/skill content on top of the already-hardened schema.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py references/apple/human-interface-guidelines.md --type reference` — `PASS`.
- `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/<slug>.md --type knowledge` for all 15 files — all `PASS`.
- `python3 scripts/validate_artifact.py skills/human-interface-guidelines/SKILL.md --type skill` — `PASS`.
- `python3 -m unittest tests/test_validate_artifact.py -v` — full pass (no regressions).
- `claude plugin validate .` — confirms the new `SKILL.md` is discovered.
- `skills/index.md` Discovery Rules table gets a new row for
  `human-interface-guidelines`.
- Manual invocation check in a fresh session (same caveat as the
  `authentication`/`style-guide` migration — the harness enumerates skills
  at session start, so this can't be verified same-session).

## Out of Scope

- HIG Patterns, Components, Inputs sections — future passes, already
  tracked in `domain-map.md`.
- Resolving the three cross-domain overlaps — deferred until the second
  domain in each pair is built.
- Any change to already-hardened schema/validator/spec files.
