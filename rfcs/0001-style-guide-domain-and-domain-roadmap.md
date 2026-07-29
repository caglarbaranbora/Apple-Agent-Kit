# RFC 0001: Style Guide Domain and Domain Roadmap

Status: Proposed (pending author sign-off)
Version: 0.1.0

## Purpose

Records the architectural decisions made when starting Phase 5 (Production Knowledge) with the `style-guide` domain, and establishes the roadmap for the remaining Apple platform domains.

## Context

Phase 0–2 validated the architecture with a single vertical slice (`authentication`, see ../validation/slices/0001/). Phase 5 begins production knowledge generation. The first source is the Apple Style Guide PDF (https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf), ~450 pages. The project's stated risk (see ../README.md) is that a wide domain surface, ingested naively, inflates knowledge/skill file size and defeats the "load only the minimum knowledge required" goal.

## Decisions

### 1. Split `style-guide` from `design`

Previous [[domain-map]] merged Style Guide, HIG, and SF Symbols into one `design` domain. Split into three domains: `style-guide` (words: terminology, capitalization, punctuation), `human-interface-guidelines` (visual/UX patterns), `sf-symbols` (iconography). Rationale: these are different concerns; merging them means any single task pulls a skill that routes toward both word and visual knowledge, inflating context for both. See ../docs/architecture/domain-map.md.

### 2. Full domain roadmap: 27 domains, 3 tiers

Roadmap expanded from 16 loosely-scoped domains to 27, organized into 3 priority tiers (Tier 1 must-have through Tier 3). Full list in [[domain-map]]. Some previously-mapped domains (`testing`, `networking`, `security`) have no tier yet — resolved when reached, not dropped.

### 3. Build order: one domain fully finished before the next starts

Within Tier order (1 → 2 → 3), a domain is not started until the previous one has completed Reference → Knowledge → Skill → Validation. `style-guide` is first. Rejected alternative: scaffold all 27 domains up front, fill content later — rejected because it produces 27 permanently-half-built domains instead of a working one, and defers the hard part (content) indefinitely.

### 4. Hard size caps on artifacts

No numeric cap existed before this RFC ("Context Budget" was a defined concept in ../docs/glossary.md but not a number). Added as a Level 1 (Structural) validation rule (../docs/validation-model.md), with each cap owned by its artifact's own spec (../docs/specifications/knowledge-spec.md, ../docs/specifications/skill-spec.md; Reference has no dedicated spec doc yet, so its cap lives directly in validation-model.md):

- Knowledge Contract: ≤150 lines
- Skill: ≤60 lines
- Reference: ≤80 lines

If a topic doesn't fit, split it into another atomic contract rather than raising the cap.

### 5. PDF ingestion delegated to subagents, reviewed in per-topic-cluster batches

The main thread never reads the raw PDF. A subagent fetches and works through the source one topic cluster at a time (e.g. all capitalization rules, then all punctuation rules), drafting Knowledge Contract candidates against the size cap. The author reviews and approves per topic-cluster batch — not per individual file, and not as one single end-of-domain dump.

### 6. Existing `authentication` contracts refactored to depend on `style-guide`

`knowledge/authentication/sign-in-terminology.md` and `knowledge/authentication/button-labels.md` currently restate Style-Guide-sourced rules inline. Once `style-guide` has its own general terminology/button-label contracts, this becomes duplication, which ../docs/specifications/knowledge-spec.md and Level 4 validation (../docs/validation-model.md) forbid. These two files are refactored to `depends_on` the new general `style-guide` contracts, keeping only the auth-specific narrowing (e.g., "Sign In / Sign Out" as the applicable case) local.

### 7. Wiki-link mirroring enforced going forward

[[linking-model]] (../docs/architecture/linking-model.md) already specifies relative-path-as-canonical with an optional `[[wiki link]]` mirror, but no existing artifact uses the mirror. This RFC does not change the linking model — it commits to actually using the optional wiki-link mirror consistently in all new `style-guide` artifacts, and backfilling it into the two `authentication` files touched by decision 6.

### 8. Decision records stay in project-native format

`grill-with-docs`-style sessions default to `CONTEXT.md` + `docs/adr/`. This project already has equivalent artifacts (../docs/glossary.md for terms, `rfcs/` for architecture proposals — ../docs/architecture.md already requires an RFC for architecture changes). This and future sessions record decisions here instead of introducing a second, parallel documentation system.

### 9. Curated subset, not the full glossary

Research at planning time (see plan doc, ../docs/superpowers/plans/) found the Apple Style Guide PDF is 86% a single alphabetical A–Z glossary of 1,706 terms with no thematic grouping, plus 5 real thematic back-matter chapters (Writing Inclusively, Units of Measure, Technical Notation, International Style, Copyright/Trademarks) that do match the original assumption. Ingesting all 1,706 terms was rejected: this project serves a coding agent writing iOS app UI text, not a full editorial catalog, and mechanical alphabet-batching (e.g. "terms A–C") produces contracts no skill would ever have a reason to route to. Decision: ingest the 5 thematic chapters in full, and a curated subset of the glossary — terms relevant to app-dev (product-name capitalization, UI terminology, abbreviations, numbers/units in-app text, avoid-lists), semantically clustered into contracts, not alphabetically. Estimated ~150–300 terms landing in ~15–25 contracts. The rest of the glossary is out of scope until a real need for it appears.

## Consequences

- `docs/architecture/domain-map.md` version bumped 0.1.0 → 0.2.0 (structural change, not yet Approved).
- `docs/specifications/knowledge-spec.md` needs the size-cap addition (follow-up, not yet applied by this RFC).
- Two existing `authentication` artifacts will change (follow-up implementation work, not yet applied by this RFC).
- Full 1,706-term Apple Style Guide glossary is explicitly NOT being ingested; only a curated, app-dev-relevant subset is (decision 9).
