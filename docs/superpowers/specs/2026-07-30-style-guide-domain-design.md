# Style Guide Domain — Design Spec

Status: Draft
Version: 0.1.0
Date: 2026-07-30

## Overview

Build the `style-guide` domain end-to-end: References → Knowledge Contracts → Skill → validation, sourced from the Apple Style Guide PDF (https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf). This is the first domain of Phase 5 (Production Knowledge) and the first of 27 domains on the roadmap in [[domain-map]] (../../architecture/domain-map.md). Decisions and rationale are recorded in [[0001-style-guide-domain-and-domain-roadmap]] (../../../rfcs/0001-style-guide-domain-and-domain-roadmap.md); this spec covers the concrete build for `style-guide` only.

## Scope

**In scope:** `style-guide` domain artifacts, the size-cap addition to `knowledge-spec.md`, the `depends_on` refactor of the two `authentication` files that currently duplicate Style Guide rules.

**Out of scope:** any other Tier 1–3 domain. Each gets its own design/plan when its turn comes, per the one-domain-at-a-time build order.

## Architecture

Follows the existing layering unchanged (../../architecture/dependency-model.md): Reference → Knowledge → Skill → Workflow, one-way, no cycles. Nothing about the layering itself changes for this domain — only its content and the fact that a Reference file may now index a larger number of Knowledge Contracts than the `authentication` slice did.

## Components

**`references/apple/style-guide.md`** (or split into `references/apple/style-guide/<subtopic>.md` if the topic count would push the index past 80 lines — References stay index-only, so this is a capacity decision, not a content one, made at build time once the real topic count from the PDF is known).

**`knowledge/style-guide/*.md`** — one Knowledge Contract per atomic rule-topic (e.g. capitalization, punctuation, terminology-general, numerals, dates-and-times, acronyms — exact list drafted from the PDF's actual table of contents, not decided in advance). Each ≤150 lines, per ../../specifications/knowledge-spec.md required sections (Intent, Rules, Compliant/Non-compliant Examples) plus full metadata block.

**`skills/style-guide/*.md`** — routing skill(s), ≤60 lines each, no embedded knowledge. One skill file unless the topic clusters are broad enough to need separate trigger surfaces (decided at build time), following the `skills/authentication/login.md` pattern.

**`skills/index.md`** — new discovery rows added for `style-guide` triggers.

**Refactored:** `knowledge/authentication/sign-in-terminology.md` and `knowledge/authentication/button-labels.md` — `depends_on` the new general `style-guide` contracts, keep only auth-specific narrowing.

## Data Flow

1. Subagent fetches the PDF, works through it one topic cluster at a time.
2. Subagent drafts Knowledge Contract candidates for that cluster, respecting the 150-line cap and the required metadata/sections.
3. Author reviews and approves per topic-cluster batch (not per file, not all at once).
4. Approved contracts are committed; the Reference index is updated to point to them.
5. Once all clusters are done, the `style-guide` skill is written, routing to the finished contracts.
6. `skills/index.md` gets the new discovery rows.
7. The two `authentication` files are refactored to `depends_on` the new contracts.
8. Validation Levels 1–4 (../../validation-model.md) run over the new and changed artifacts. Level 5 (vertical slice) is not repeated — it validated the architecture itself in `validation/slices/0001` and is not re-run per domain.
9. RFC 0001 status updated from Proposed to reflect the completed build.

## Error Handling / Edge Cases

- **Contract would exceed 150 lines:** split into two atomic contracts, never raise the cap.
- **Ambiguous topic boundary** (a rule could belong to two clusters): author decides during batch review; not resolved by the subagent unilaterally.
- **PDF fetch fails or a page is unreadable:** subagent reports the gap; author supplies the section manually or the topic is deferred, not silently skipped.
- **Duplicate rule detected against an existing contract** (in `style-guide` or elsewhere): flagged in the batch review, resolved via `depends_on` rather than restating, per Level 4 validation.
- **Broken relative-path or `[[wiki link]]` mirror mismatch:** Level 2 validation catches it; wiki link must mirror the canonical relative path exactly (../../architecture/linking-model.md).

## Testing / Validation

Standard project validation applies unchanged: Level 1 (structural — includes the new size caps), Level 2 (repository integrity — link resolution, unique IDs, acyclic graph), Level 3 (architectural — layering, routing), Level 4 (domain — atomicity, no duplicated rules, references authoritative). No new validation machinery is introduced by this spec; the size caps are an addition to existing Level 1 checks.

## Follow-Up Implementation Items (not yet applied)

- Add the three size caps to ../../specifications/knowledge-spec.md.
- Everything in Components/Data Flow above.
