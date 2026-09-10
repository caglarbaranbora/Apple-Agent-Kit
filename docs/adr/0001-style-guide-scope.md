# ADR-0001: Apple Style Guide Domain Scope

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: adr.0001
artifact_type: adr
title: Apple Style Guide Domain Scope
version: 1.0.0
status: Approved
domain: Style Guide
related: []
last_updated: 2026-09-10
```

## Context

Established by ../../rfcs/0001-style-guide-domain-and-domain-roadmap.md
([[0001-style-guide-domain-and-domain-roadmap]]), Decision 1 ("Split `style-guide`
from `design`"). `style-guide` was the repository's first domain (Tier 1) and predates the habit,
visible in later `domain-map.md` entries, of narrating each domain's founding
rationale inline: the "Completed:" paragraph's own mention of it is just
`` `style-guide` (Tier 1) ``, with no elaborating clause. The domain's actual
founding rationale lives in its own design spec,
`docs/superpowers/specs/2026-07-30-style-guide-domain-design.md`, written before
`domain-map.md`'s narrative-paragraph convention existed. That spec's Overview
states the goal directly: "Build the `style-guide` domain end-to-end: References
→ Knowledge Contracts → Skill → validation, sourced from the Apple Style Guide
PDF... This is the first domain of Phase 5 (Production Knowledge) and the first
of 27 domains on the roadmap." Its Scope section further bounds the work to
"`style-guide` domain artifacts, the size-cap addition to `knowledge-spec.md`,
[and] the `depends_on` refactor of the two `authentication` files that currently
duplicate Style Guide rules," explicitly excluding "any other Tier 1–3 domain."

## Decision

Scope `style-guide` to terminology, capitalization, punctuation, and writing style
— UI copy wording, capitalization rules, punctuation, and inclusive writing —
exactly as `domain-map.md`'s Tier 1 table row states today:

> Apple Style Guide | style-guide | Terminology, capitalization, punctuation,
> writing style | UI copy wording, capitalization rules, punctuation, inclusive
> writing

## Consequences

- Established the pattern every later Foundations-adjacent domain follows: UI
  *wording* is `style-guide`'s angle, UI *visual design* is
  `human-interface-guidelines`'s — see `domain-map.md`'s Cross-Domain Notes for
  the specific angle-split entries this enabled later (out of scope for this ADR
  to restate; cited there, not duplicated here per `adr-spec.md`'s no-duplication
  rule).
- No other domain existed yet at authoring time, so no boundary was contested at
  the time this scope was set.

## Verification Log

- 2026-09-10: initial scope recorded, migrated out of `domain-map.md`'s
  "Completed:" paragraph into this ADR per
  `docs/superpowers/specs/2026-09-10-adr-artifact-type-design.md`. No scope
  change — a format migration only.
