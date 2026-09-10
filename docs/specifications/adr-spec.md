# ADR Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the normative specification for every Architecture Decision Record (ADR)
in Apple Agent Kit.

An ADR records *why* one domain's scope was set where it was, and when it later
changed — separately from `docs/architecture/domain-map.md`, which records only
*what* the current scope is. It is a governance document, not domain content: it
carries no implementation rules and is never routed to by a Skill.

## When an ADR Is Warranted

For a *new* decision (as opposed to the initial migration this spec accompanies),
use `mattpocock/skills`' three-part test, cited in
`docs/research/2026-09-mattpocock-skills-architecture.md` §5-6:

- **Hard to reverse.**
- **Surprising without context** — a later reader would otherwise ask "why is it
  like this?"
- **The result of a real trade-off**, not a default choice with no alternative
  seriously considered.

A decision that fails all three stays as ordinary prose in the relevant Knowledge
Contract, Skill, or `domain-map.md` row instead of getting its own ADR.

## Location

    docs/adr/<NNNN>-<domain-slug>-scope.md

`NNNN` is a zero-padded, sequential, four-digit number, assigned once per domain
and never reused or renumbered. The id is `adr.<NNNN>` and MUST agree with the
number in the filename — a validator checks the two agree, the same pattern
`knowledge-spec.md` uses for id/path agreement.

## Required Metadata

Common base (see `../../schemas/metadata.schema.md` [[metadata.schema]]):
`id`, `artifact_type`, `title`, `version`, `status`, `last_updated`

ADR extension: `domain` (the domain name exactly as it appears in
`domain-map.md`'s `Domain` column), `related` (non-binding; used to point at the
ADR that supersedes this one, when `status` is `Deprecated`)

`artifact_type` is `adr`.

## Required Sections

1. `## Context` — why the decision was needed
2. `## Decision` — what was decided (the domain's initial scope)
3. `## Consequences` — what the decision affected: which files, which other
   domains, what it ruled out
4. `## Verification Log` — dated bullets. A later scope change (an expansion, a
   closed gap) is a new dated bullet here, **not** a rewrite of `## Decision`'s
   original text and **not** a new ADR — one ADR persists for the domain's whole
   life (see Granularity below)

## Granularity

One ADR per domain, for the life of that domain. When scope changes later
(an expansion, a closed gap, a retirement), append a dated bullet to
`## Consequences`/`## Verification Log` rather than opening a new ADR file. This
mirrors how `domain-map.md`'s prose already appended "expanded 2026-08-08 to add
X" before this spec existed — this changes *where* that sentence lives, not its
shape.

## Status Semantics

Reuses the four states `../artifact-lifecycle.md` [[artifact-lifecycle]] already
defines — no ADR-specific vocabulary:

- **Approved** — this decision currently governs the domain's scope.
- **Deprecated** — a later ADR supersedes this one. Point at the superseding ADR
  via `related:`.
- **Archived** — the domain itself is retired (e.g. `authentication`). Matches
  `domain-map.md`'s "Retired" status for that row.
- **Draft** — being authored; not yet a settled record.

## Rules

- One domain per ADR (see Granularity). Do not describe more than one domain's
  scope in a single ADR — that is what `## Cross-Domain Notes` is for, and ADRs do
  not currently cover that section (see the design's Non-goals; a future ADR
  variant or distinct artifact type may).
- `## Decision`/`## Consequences` content MUST be traceable to what
  `domain-map.md`'s current row for that domain says it owns, not asserted fresh.
  Where `domain-map.md` itself has no elaborating prose for the domain (a real
  case — some domains were never narrated in detail there), `## Context` MUST say
  so explicitly rather than inventing a rationale, and MAY instead cite that
  domain's own `docs/superpowers/specs/*-design.md` if one exists.
- Do not embed implementation rules. An ADR is never a Knowledge Contract in
  disguise — if a rule belongs in a Contract, it goes there, not here.
- `## Verification Log` entries are append-only. Do not edit or remove an earlier
  entry to "clean up" the record; a wrong entry gets a new dated entry that
  corrects it, the same way `domain-map.md`'s own history is never quietly
  rewritten.

## Size Limit

An ADR MUST NOT exceed 150 lines, the same cap as a Knowledge Contract. An ADR
that grows past it during `## Verification Log` accretion is a signal the domain
has enough independent decision history to warrant a closer look — not, by
itself, an automatic trigger to split it.

## References

Cite `domain-map.md`'s row for the domain, and that domain's own
`docs/superpowers/specs/*-design.md` where one exists.

## Validation Checklist

- Metadata complete and valid against the schema
- Filename number and `id`'s `<NNNN>` agree
- Exactly one domain described
- All four required sections present
- `## Decision`/`## Consequences` traceable to `domain-map.md`'s current row (or
  the domain's own design spec, where `domain-map.md` itself is silent)
- `status` is one of the four lifecycle states, with `Deprecated`/`Archived`
  semantics as defined above
