# ADR Artifact Type — Design

Status: Approved
Version: 1.0.0
Date: 2026-09-10

## Goal

Give the repository a sixth artifact type, `adr` (Architecture Decision Record), and
use it to record *why* each domain's scope is what it is — separately from
`docs/architecture/domain-map.md`, which records *what* the current scope is. This
replaces `domain-map.md`'s single, ever-growing "Completed:" prose paragraph (one
run-on sentence spanning ~30 domains, 30,344 characters, measured 2026-09-10) with one
short, targeted ADR per domain plus a one-line pointer from the domain's table row.

Motivating incident: implementing the "Designing for iPhone Duo" HIG addition
(2026-09-10) required editing that single paragraph with string-replace surgery —
every edit risked corrupting unrelated domains' history in the same block. Separately
sourced: `docs/research/2026-09-mattpocock-skills-architecture.md` §6-7, which found
that the `mattpocock/skills` repo applies its own `domain-modeling` ADR discipline to
its own packaging decisions, with a dated verification log rather than an unverified
claim, and that this is one of eight named reasons that repository's skill/agent
system holds up over time.

## Non-goals

- **Cross-Domain Notes migration.** `domain-map.md`'s second dense section (~50+
  boundary-classification bullets between domain *pairs*, plus several "vertical
  slice" incident write-ups) is a structurally different record — relational, not
  per-domain — and is explicitly deferred to its own future design cycle. Nothing in
  this design touches it.
- **Disclosed-reference sibling files for Knowledge Contracts** (the
  `writing-for-agents` progressive-disclosure pattern, so a 150-line-capped Contract
  can push a worked example to a sibling file instead of compressing prose). Deferred;
  a separate future design.
- **A "Rejected framings" required section** for Knowledge Contracts (formalizing
  what `## Scope`'s `### Excluded` already partially does). Deferred; a separate
  future design.
- Rewriting or re-litigating any of the ~30 domains' actual scope decisions. This is
  a format migration: content moves, it is not reconsidered.

## Current state

`docs/architecture/domain-map.md` (380 lines) has two dense sections:

1. A single paragraph (`## Build Order`, inside the "Completed:" sentence) narrating
   every Tier 1/2/3 domain's initial scope, every later expansion, and every closed
   gap, all as one continuously-appended run-on sentence with no per-domain
   boundaries a tool can parse.
2. `## Cross-Domain Notes` — 50+ bullets classifying boundaries between domain
   *pairs* (angle-split / clean-handoff / coupled), several with their own dated
   resolution history and incident write-ups (`#0002`, `#0005`, `#0006`, `#0007`).
   Out of scope here (see Non-goals).

The repo's five existing artifact types (`knowledge`, `skill`, `reference`,
`workflow`, `entry`) are each governed by a spec in `docs/specifications/`, validated
by `scripts/validate_artifact.py --type <type>` (Level 1, structural) and
`scripts/validate_repo.py` (Levels 2-3, repo-wide graph/routing/index checks).
`schemas/metadata.schema.md` is the field-level authority for all of them. Its
`artifact_type` enum today is `knowledge, skill, reference, workflow, entry,
template, spec`; `adr` is a genuinely new enum value this design adds.

`docs/artifact-lifecycle.md`'s `Draft → Approved → Deprecated → Archived` lifecycle
already scopes itself to include "Governance documents under `docs/`, `schemas/`, and
`templates/`" and explicitly excludes "Design records and plans under
`docs/superpowers/`" as historical-only. An ADR under `docs/adr/` is a governance
document other live artifacts (`domain-map.md`'s table) will link to and depend on
being current — not a point-in-time plan like this very design doc — so it falls
inside the lifecycle, not outside it. This resolves what would otherwise be an
ambiguity before it becomes one.

## Decisions

Reached by grilling (recorded in the session; not re-derived here).

- **D1 — Phasing.** This design covers only the ~30 domain-scope ADRs (one per row in
  the `## Tier 1` / `## Tier 2` / `## Tier 3` tables, plus the retired `authentication`
  row in `## Existing / Unscheduled Domains`). Cross-Domain Notes is a separate future
  design (see Non-goals).
- **D2 — Location and validation rigor.** `docs/adr/NNNN-<domain-slug>-scope.md`.
  `adr` is a fully validated artifact type: a new `docs/specifications/adr-spec.md`,
  `scripts/validate_artifact.py --type adr` support, and a new `scripts/validate_repo.py`
  check (below). Not a `mattpocock`-style unvalidated free-format note — this repo's
  standing rule is that a spec/validator disagreement is release-blocking, and a
  sixth artifact type left undisciplined would be the repo's first double standard.
- **D3 — Template.** Metadata (common base per `metadata.schema.md`, plus a `domain`
  extension field) + `## Context` + `## Decision` + `## Consequences` + `## Verification
  Log`. A later expansion or closed gap for the same domain is a new dated bullet
  under `## Verification Log`, not a new ADR (see D4). The spec also states, for
  future authors, `mattpocock/skills`' three-part trigger test for when a *new*
  domain decision deserves its own ADR at all: hard to reverse, surprising without
  context, the result of a real trade-off (cited in
  `docs/research/2026-09-mattpocock-skills-architecture.md` §5-6). A decision that
  fails all three stays as prose in the relevant Knowledge Contract or Skill instead.
- **D4 — Granularity.** One ADR per domain, for its life. `## Consequences`/
  `## Verification Log` accumulate dated entries as the domain's scope changes later
  (mirrors how `domain-map.md`'s prose already appends "expanded 2026-08-08 to add
  X" today — this design changes *where* that sentence lives, not its shape).
- **D5 — `domain-map.md` structural change.** Each Tier table gains a fifth column,
  `ADR`, linking to that row's file. The "Completed:" run-on paragraph is deleted
  entirely and replaced with one sentence: scope lives in the table; rationale and
  history live in the linked ADR. `## Cross-Domain Notes` is untouched (Non-goals).
- **D6 — Numbering.** Sequential, zero-padded to 4 digits, assigned in the order
  domains currently appear in `domain-map.md`: Tier 1 table row order, then Tier 2,
  then the two Tier 3 pilot domains already built (`photos`, `core-location`), then
  `authentication` (retired) last. This is a one-time deterministic assignment for
  the migration; new domains after this point get the next unused number.
- **D7 — Status reuse, not a new enum.** ADR status values are the existing four
  (`Draft`, `Approved`, `Deprecated`, `Archived`) — no bespoke `Accepted`/`Superseded`
  vocabulary. `Approved` = currently governs. `Deprecated` = a later ADR supersedes
  it (the superseding ADR is named via `related:`, reusing the field
  `metadata.schema.md` already defines — no new field invented). `Archived` = the
  domain itself is retired (`authentication`'s ADR is the one `Archived` instance in
  the initial migration).

## `adr` artifact type — schema and spec shape

### `schemas/metadata.schema.md` changes

- `artifact_type` enum gains `adr`: `knowledge, skill, reference, workflow, entry,
  template, spec, adr`.
- New per-type extension row: `adr` adds `domain` (which domain this decision is
  about — string, matches a `domain-map.md` row's `Domain` column exactly) and
  `related` (already a common cross-reference field; used here for
  supersession links).

### `docs/specifications/adr-spec.md` (new file, same shape as `knowledge-spec.md`)

- **Location:** `docs/adr/<NNNN>-<domain-slug>-scope.md`. Id: `adr.<NNNN>` (matches
  the zero-padded number in the filename; a validator checks the two agree, same
  pattern `knowledge-spec.md` uses for id/path agreement).
- **Required sections:** `## Context`, `## Decision`, `## Consequences`,
  `## Verification Log`.
- **Rules:** one domain-scope decision per ADR (D4); later changes are dated
  `## Verification Log` bullets, never a rewrite of `## Decision`'s original text
  (the record is append-only, matching why an ADR is worth having at all); every
  claim in `## Decision`/`## Consequences` must be traceable to what
  `domain-map.md`'s current row says the domain owns, not asserted fresh.
- **Size limit:** reuse the `knowledge` type's 150-line cap. An ADR that grows past
  it during later `## Verification Log` accretion is a signal the domain has enough
  independent decision history to reconsider (not a hard trigger for anything in
  this design — flagged for future judgement, not auto-split).
- **The three-part trigger test** (D3) is documented here as guidance for *authoring
  new* ADRs going forward, credited to its source.

### `scripts/validate_artifact.py`

- Add `"adr": 150` to `LINE_CAPS`.
- Add required-section and id/path-agreement checks for `artifact_type: adr`,
  mirroring the existing `knowledge` handling.

### `scripts/validate_repo.py` — new check

- Every `ADR` column entry in `domain-map.md`'s Tier tables (and the
  `authentication` row) must resolve to an existing `docs/adr/*.md` file.
- Every `docs/adr/*.md` file must be referenced by exactly one `domain-map.md` row
  (bidirectional — the same "no orphan artifact" shape `validate_repo.py` already
  enforces for Knowledge Contracts' `## Used By`).

## `domain-map.md` after migration

Each Tier table row (`| Domain | Slug | Initial Scope | Owns |`) gains a fifth
column:

    | Domain | Slug | Initial Scope | Owns | ADR |
    |---|---|---|---|---|
    | Human Interface Guidelines | human-interface-guidelines | ... | ... | [ADR-0007](../adr/0007-human-interface-guidelines-scope.md) |

The "Completed:" run-on paragraph inside `## Build Order` is deleted in full and
replaced with:

> Current scope for every domain is recorded in the Tier tables below. The
> rationale, build history, and dated verification log for each domain's scope
> live in its linked ADR (`docs/adr/`) — this file states *what*, the ADR states
> *why and when*.

`## Existing / Unscheduled Domains` (currently just the retired `authentication`
row) gets the same fifth column, pointing at an `Archived`-status ADR.

`## Cross-Domain Notes` is untouched.

## Migration approach (for the implementation plan)

~30 ADRs need their `## Context`/`## Decision`/`## Consequences`/`## Verification
Log` content **extracted** from the existing "Completed:" paragraph's text for that
domain — not freshly written or paraphrased from general knowledge, since the
paragraph is the only authoritative source for *why* each scope line was drawn where
it was. Each domain's extraction is independent of every other domain's, which makes
this a natural fit for parallel subagent dispatch during implementation (one
subagent per batch of domains, each handed its exact slice of the source paragraph
plus the ADR template) rather than one long serial pass — a plan-level detail, not
a design-level one, but noted here since it affects how the implementation plan
should be structured.

## Testing / validation plan

- `python3 scripts/validate_artifact.py . --all` — all ~30 new ADRs plus the schema
  change pass Level 1.
- `python3 scripts/validate_repo.py .` — new bidirectional ADR-link check passes,
  plus all existing Level 2-3 checks still pass.
- `python3 scripts/check_transitions.py .` — every new ADR's `Draft → Approved`
  transition (or `Draft → Approved → Archived` for `authentication`) is valid per
  `artifact-lifecycle.md`.
- `python3 -m unittest discover tests/` — full suite still green.
- Manual: `domain-map.md` diff reviewed to confirm no domain's actual scope content
  (Tier table cells) changed — only the narrative paragraph moved out and a column
  was added.

## Open question for the next design cycle

Not blocking this one, but worth recording now while it's fresh: once Cross-Domain
Notes gets its own design (Non-goals), decide whether a boundary-classification
record is a *variant* of this same `adr` type (e.g. `domain: "X ↔ Y"`) or a
genuinely distinct sixth-or-seventh artifact type, since its content shape (two
domains, a classification enum, sometimes an incident write-up) doesn't map cleanly
onto `## Context`/`## Decision`/`## Consequences`.
