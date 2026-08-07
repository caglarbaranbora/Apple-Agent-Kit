# v1 Finalization — Phase 1: Rule Corpus Reconciliation

Status: Approved
Version: 1.0.0
Date: 2026-08-07
Spec: ../specs/2026-08-07-v1-finalization-design.md

## Goal

Make the 19-document rule corpus self-consistent and complete, so Phases 2-6 have a
standard to be measured against. Documents only — this phase changes no Knowledge
Contract, Skill, or Reference.

## Approval and versioning

Per decision A2b, every governance document this phase rewrites exits as
`Status: Approved` / `Version: 1.0.0`. This is consistent with the repository's own
rules: `naming-conventions.md:68` defines 1.0.0 as "Initial stable", and
`artifact-lifecycle.md:52` says approval "SHOULD establish a stable version".

Approved means changes require review, not that the document is frozen forever. If
Phase 3 or 4 proves a rule wrong, that document takes a normal version bump — which
is the first real exercise of a lifecycle that has never been used.

`docs/foundation/principles.md` and `docs/development-process.md` are already
`Approved 1.0.0` and are not touched, except `development-process.md`'s phase list
(Task 19).

## Header convention

Two header styles exist in the corpus: `Status: Draft Version: 0.1.0` on one line and
`Status: Draft` / `Version: 0.1.0` on two. Normalize every rewritten document to two
lines. `docs/foundation/vision.md` has no `Status:` line at all — add one (Task 19).

---

## Task 1 — `schemas/metadata.schema.md` (full rewrite)

Drives: A1, A1b, A2, A4, B1

The schema doc and the spec docs currently disagree on 4 field names and on which
fields are required. This file becomes the single field-level authority.

- Required-fields table restructured into **common base** + **per-type extension**:
  - Base (every type): `id`, `artifact_type`, `title`, `version`, `status`, `domain`,
    `last_updated`
  - `knowledge` adds: `owner`, `summary`, `tags`, `depends_on`, `related`, `references`
  - `skill` adds: `name`, `description`, `routes`, `related`
  - `reference` adds: `owner`, `summary` (sections carry the source URLs — see Task 4)
  - `workflow` adds: `skills`, `related`
  - `entry` adds: `name`, `description`
- `type` → `artifact_type`; `updated` → `last_updated`
- `artifact_type` enum: `knowledge`, `skill`, `reference`, `workflow`, `entry`,
  `template`, `spec` (drop nothing; add `entry`)
- `status` enum: `Draft`, `Approved`, `Deprecated`, `Archived` — `Review` removed
- Field semantics section added, per B1: `depends_on` is the binding dependency edge;
  `related` is a non-binding cross-reference whose target must exist; `routes` is a
  Skill→Knowledge load instruction. Only `depends_on` is subject to DAG and direction rules.
- `tags` description changed to "Search and Obsidian metadata. **Not** a routing input."
  (decision C1)
- The example block updated to the new dialect and a real, resolvable set of IDs —
  the current example cites `knowledge.button-labels` and `knowledge.accessibility.forms`,
  neither of which exists.
- Rule "IDs MUST be immutable" retained and cross-referenced from Task 3 (S2).

Verify: field lists here match `validate_artifact.py`'s constants after Phase 3, and
match Tasks 2-6 exactly. Any divergence is the bug this whole phase exists to remove.

## Task 2 — `docs/specifications/knowledge-spec.md`

Drives: A1, A1b, B1, C1

- Required Metadata replaced with: base 7 + `owner`, `summary`, `tags`, `depends_on`,
  `related`, `references`. This adds `owner`/`summary`/`tags` (which the validator
  already enforces and all 232 Contracts already carry) and renames two fields.
- Required Sections: keep 4. Add `## Dependencies` as required — 232/232 Contracts
  already have it, and C1 makes it load-bearing for transitive routing.
- Rules: "Do not embed workflow logic" → "Do not embed orchestration logic"
  (the layer is real again, but the rule is about Knowledge staying non-orchestrating).
- Dependency Rules section scoped explicitly to `depends_on` (B1).
- Size limit 150 unchanged.

## Task 3 — `docs/specifications/skill-spec.md`

Drives: A1b, S1, S2, D1

- Frontmatter Format section: **remove the nested option**. Layout is always
  `skills/<domain>[-<facet>]/SKILL.md`. State why: Claude Code derives the invocable
  Skill name from the directory, and zero nested Skills exist.
- Add the ID rule: `skill.<domain>.<facet>`, facet derivable from the directory by
  stripping the domain prefix. `foundations` is the default facet for a domain's
  primary Skill, not mandatory.
- Required Metadata: base 7 + `name`, `description`, `routes`, `related`.
- Add a Splitting rule (S1): topical coherence is the trigger; 80 lines is a ceiling,
  not a trigger. Cross-reference `skill-management.md` (Task 7).
- Size Limit stays 80. Add the measured note that the largest Skill is 56 lines, so
  the cap has never bound — this is why S1 was needed.
- Rules: "A Skill routes Knowledge Contracts only" retained and sharpened — a Skill
  never routes to another Skill; that is a Workflow's job (A4).

## Task 4 — `docs/specifications/reference-spec.md` (NEW)

Drives: A3

Full body:

```markdown
# Reference Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the normative specification for every Reference in Apple Agent Kit.
A Reference maps a domain to the official Apple sources that authorize its
Knowledge Contracts. It is an index of authority, not a source of rules.

## Location

references/apple/<domain>.md

One Reference per Skill-scoped domain. A domain whose Knowledge lives in one
directory may still have several References when its Skills are split — for
example `human-interface-guidelines`, `-components` and `-patterns` share
`knowledge/human-interface-guidelines/`. Reference-to-Knowledge is therefore
many-to-many, and no tool may derive one from the other by directory name.

## Required Metadata

Base: id, artifact_type, title, version, status, domain, last_updated
Reference adds: owner, summary

artifact_type is `reference`. The id is `reference.apple.<domain>`.

## Required Sections

1. Source
2. Purpose
3. Primary Topics
4. Used By

## Rules

- Every URL under Source MUST resolve to an official Apple source:
  developer.apple.com documentation, a WWDC session, an Apple archived guide,
  or help.apple.com. No third-party sources.
- A URL MUST be specific enough to authorize a rule. A framework or guideline
  landing page is acceptable only when it is itself the cited surface; a bare
  hub that indexes unrelated topics is not.
- Used By lists every Knowledge Contract that cites this Reference, as a wiki
  link (`[[knowledge/<domain>/<slug>]]`), per the linking model.
- A Reference MUST NOT contain implementation rules. Rules live in Knowledge
  Contracts; the Reference records where their authority comes from.
- Primary Topics names the surface this Reference covers, not the Contracts.

## Size Limit

A Reference MUST NOT exceed 98 lines. If a domain's sources do not fit, split
the domain's Skill and give each Skill its own Reference — never raise this limit.

## Validation Checklist

- Metadata complete and valid
- All four sections present, in order
- Every Source URL is an official Apple source
- Used By resolves to existing Knowledge Contracts
- No implementation rules present
```

Note on the cap: 98 rather than 80 because the largest Reference is 78 lines
(`localization.md`) and a metadata block adds roughly 10. The line-counting rule is
unchanged for every type, so Skills gain no headroom as a side effect.

## Task 5 — `docs/specifications/workflow-spec.md`

Drives: A1b, E1, E1b

- Required Metadata replaced with base 7 + `skills`, `related`. (Currently it lists
  `artifact_type`, `skills`, `related`, `last_updated` but omits `domain`, and lists
  `id`/`title`/`version`/`status` — reconcile to the base.)
- Add Location: `workflows/<slug>/WORKFLOW.md`, mirroring the Skill layout.
- Add an Entry section stating how a Workflow is reached: via the Workflows table in
  `skills/index.md` (E1). A Workflow is never auto-discovered — Claude Code has no
  workflow primitive.
- Keep the 5 required sections and the orchestration-only rules.
- Add a size limit of 80, matching Skills, since a Workflow is also pure routing.

## Task 6 — `docs/specifications/template-spec.md`

Drives: B3, A1b

- Remove the implication that Templates are an architectural layer; state they are an
  authoring aid, like `scripts/`.
- Metadata Standard replaced by a pointer to the base 7 in `metadata.schema.md`
  rather than a fourth competing list.
- Supported Templates list trimmed to what exists, or the missing ones are recorded as
  unbuilt with a pointer — not silently listed as if present.

## Task 7 — `docs/specifications/skill-management.md` (NEW)

Drives: S1, S2, S3, E1

Full body:

```markdown
# Skill Management Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the lifecycle of a Skill: when one is created, how it is identified,
what must change when it grows, when it splits, and how it is retired.
`skill-spec.md` defines a Skill's shape; this document defines its change
procedure.

## When a Skill Is Created

A domain gets exactly one Skill by default.

A domain gets more than one Skill on topical coherence: when its Knowledge
divides into task families that a single `## Routing` section cannot
discriminate cleanly. Size is not the trigger — the 80-line cap is a hard
ceiling, and no Skill in this repository has approached it.

Precedent: `human-interface-guidelines` splits three ways because Apple's own
guidelines split three ways (Foundations, Components, Patterns), and a single
routing table could not separate "check this screen's layout" from "which
control do I use". `swiftui` splits two ways because static composition and
interaction are distinct task families.

## Identity and Layout

Layout is always flat:

    skills/<domain>[-<facet>]/SKILL.md

Never nested. Claude Code derives the invocable Skill name from the directory
name, so `skills/<domain>/<facet>/SKILL.md` would not be discoverable as
`/<domain>-<facet>`.

The id is `skill.<domain>.<facet>`. The facet is derivable from the directory
name by stripping the domain prefix, and a validator checks the two agree.

`foundations` is the default facet for a domain's primary Skill. It is not
mandatory — `writing` and `submission` are valid where they describe the Skill
better. Ids are immutable (`metadata.schema.md`), so an existing facet name is
never changed for consistency alone.

## Adding a Knowledge Contract to an Existing Skill

Every one of these must change in the same commit:

1. The Knowledge Contract file itself.
2. The Skill's `routes:` list.
3. The Skill's `## Routing` section — a routed Contract with no routing line is
   unreachable.
4. The domain's Reference: add the new Contract to `## Used By`, and add any new
   Apple source to `## Source`.
5. `skills/index.md`: add trigger keywords if the Contract introduces terms the
   existing row does not cover.
6. `docs/architecture/domain-map.md`: extend the domain's scope cell.
7. `CHANGELOG.md`.
8. `README.md` only if a Skill or domain is added — not for a Contract.

Items 2-5 are machine-checkable and are enforced by `scripts/validate_repo.py`.
Items 6-8 are prose and belong to the Level 4 review checklist.

## Splitting a Skill

1. Confirm the trigger is topical, not size.
2. Create the new `skills/<domain>-<facet>/` directory and `SKILL.md`.
3. Move the relevant ids out of the original Skill's `routes:` and `## Routing`.
   Knowledge Contracts do not move — `knowledge/<domain>/` stays one directory.
4. Give the new Skill its own Reference if its sources differ; otherwise both
   Skills may share the domain Reference.
5. Add a row to `skills/index.md` and partition the trigger keywords so the two
   rows do not collide.
6. Update `README.md`, `domain-map.md` and `CHANGELOG.md`.

## Retiring a Skill

Retirement is the correct outcome when a Skill's Knowledge is owned by other
domains and its own value was routing, not knowledge.

1. Set each retired Knowledge Contract's `status:` to `Deprecated`, then remove
   it once nothing references it. Never delete a Contract another artifact still
   names.
2. Relocate any Contract that belongs to another domain, correcting its `domain:`
   field and id.
3. Remove the Skill's row from `skills/index.md`.
4. Resolve every `related:` reference to the retired Skill's id.
5. Record the retirement in `domain-map.md` — a retired domain stays in the
   record with its disposition, it is not erased.
6. If the routing value survives the Knowledge, replace the Skill with a
   Workflow (see below).

## Relationship to Workflows

A Skill routes to Knowledge Contracts. It never routes to another Skill.

When a task genuinely spans domains, that is a Workflow, and the Workflow names
the Skills in order. A "Skill that dispatches to Skills" is a Workflow written
in the wrong layer.

`authentication` is the worked example: its Knowledge was owned by `style-guide`
and `accessibility`, and its own Contracts encoded routing rules rather than
implementation rules. Its Knowledge retires; its routing value becomes
`workflows/authentication/`.

## Validation Checklist

- Directory layout flat, facet agrees with id
- Every routed id exists and appears in `## Routing`
- `skills/index.md` row present, keywords non-colliding
- Reference `## Used By` complete
- No Skill routes to a Skill
```

## Task 8 — `docs/artifact-lifecycle.md`

Drives: A2, A2b

- Lifecycle line: remove `Review`. `Draft → Approved → Deprecated → Archived`.
- States section: delete the `Review` block.
- Allowed Transitions: `Draft → Approved`, `Approved → Deprecated`,
  `Deprecated → Archived`, `Approved → Draft` (revision reopened).
- Add a Scope section (A2b): governance documents under `docs/`, `schemas/` and
  `templates/` are artifacts under this lifecycle, alongside Knowledge, Skills,
  References, Workflows and the Entry.
- Approval Requirements: replace the unverifiable list with the concrete gate —
  Level 1-3 validation passes, and the Level 4-5 review checklist is complete.

## Task 9 — `docs/architecture.md`

Drives: A2, B1, B3

- Layers: remove item 5 (Templates). Four layers.
- Repository Structure line: keep `templates/` in the directory list but not in the
  layer list — the directory exists, the layer does not.
- Dependency Rules: remove `Skill -> Template` from Allowed. Scope the whole
  Allowed/Forbidden block to `depends_on` explicitly (B1), and state that `related:`
  is a non-binding cross-reference outside these rules.
- Artifact Lifecycle line: already four states; leave, and cross-reference Task 8.
- Add `entry` to the artifact vocabulary (A4).

## Task 10 — `docs/architecture/dependency-graph.md`

Drives: B1, B3, A4

- Add a header line scoping both tables to `depends_on`.
- Add the missing `Knowledge | Knowledge` row to Allowed — it is already legal per
  this file, but state it against `linking-model.md`'s omission (B2).
- Add `Workflow | Skill` (present) and confirm `Skill | Skill` is Forbidden **for
  `depends_on`**, with a note that `related:` between Skills is legal and used by
  32/32 Skills.
- No Template rows — Templates are not a layer (B3).
- Validation section: point at `scripts/validate_repo.py` (Phase 3) rather than
  describing checks nothing performs.

## Task 11 — `docs/architecture/linking-model.md` (full rewrite)

Drives: B1, B2, B4

The current document declares relative paths canonical and puts artifact IDs last.
Artifacts use zero relative-path links and 31/31 References use wiki links. Rewrite
to codify the three conventions actually in use:

- **Metadata edges** — artifact IDs. The graph's source of truth. IDs are immutable,
  which is why they, not paths, survive file moves.
- **Reference `## Used By`** — wiki links, `[[knowledge/<domain>/<slug>]]`. This
  repository lives in an Obsidian vault; wiki links are functional there. The current
  rule that a wiki link "must never be the only reference" is removed — it was
  violated by every Reference and served no purpose.
- **Document prose** — relative Markdown paths, in `docs/` only.

- Cross-Layer Linking table corrected: add `Knowledge → Knowledge` (B2), scope
  direction bans to `depends_on` (B1).
- Validation section points at `validate_repo.py` and states the many-to-many rule:
  Reference↔Knowledge is never derived from directory names.

## Task 12 — `docs/architecture/routing-model.md` (full rewrite)

Drives: C1, E1

Replace the declared-but-unbuilt model with the three-stage mechanism that exists:

1. `skills/index.md` — the Routing Index. Match the task against the Workflows table
   first, then the Skills table. A Workflow names its Skills in order; otherwise
   exactly one Skill is loaded.
2. The Skill's `## Routing` section maps task shape to Knowledge Contract ids.
3. Each loaded Contract's own `## Dependencies` section pulls anything further.
   232/232 Contracts carry this section; 0/32 Skills do, which is why transitive
   resolution lives in the Knowledge layer, not the Skill layer.

- Remove tag-based routing from Resolution Rules. State explicitly that `tags:` is
  search metadata and not a routing input.
- Keep the routing principles and the context-budget section; they are accurate.
- Routing Inputs "A Skill MUST NOT use" list retained — it is the point of the repo.

## Task 13 — `docs/validation-model.md`

Drives: D1, D2, A3

- Level 1 size limits corrected: Knowledge 150, Skill **80** (was 60), Reference **98**
  (was 80), Workflow 80.
- Each level gains an Implementation line naming what enforces it:
  - Level 1 → `scripts/validate_artifact.py`
  - Levels 2-3 → `scripts/validate_repo.py`
  - Levels 4-5 → the review checklist, with `Blocking: Yes` retained but the
    enforcement mechanism stated as human/agent review rather than code
- Level 1 checks extended: enum values, version format, artifact_type/path agreement.
- Add the Level 4-5 review checklist as a referenced document or an inline procedure —
  the Level 4 items (atomicity, duplicated rules, source traceability, no domain
  knowledge in Skills) are semantic and must be checked by reading, with the
  traceability item explicitly noting that URL shape does not prove specificity.

## Task 14 — `docs/naming-conventions.md`

Drives: F1, F2, S2

- General Rules: remove "Use singular nouns"; replace with the real convention —
  collection directories are plural, artifact filenames name their topic.
- Reserved Names: scope the list to artifact filenames, so `tests/` stops being a
  violation of the repository's own rule.
- Repository Naming examples: correct `workflows/ - release-ios-app.md` to the real
  layout `workflows/<slug>/WORKFLOW.md`, and `skills/` to `skills/<domain>[-<facet>]/`.
- Artifact IDs: add `reference.apple.<domain>`, `workflow.<slug>`, `entry.<name>`.
- Validation section: point at the implementing script rather than declaring MUSTs
  with no owner.

## Task 15 — `docs/repository-layout.md`

Drives: B3

- `templates/: reusable artifacts` → `templates/: authoring templates (not a layer)`.
- `docs/: specifications` → accurate description; `docs/` holds architecture,
  specifications, foundation, contributing and design records.
- Add `scripts/` and `tests/`, both of which exist and are unlisted.

## Task 16 — `docs/glossary.md`

Drives: A4, B1

- New `## Entry` term: the plugin entry point; the artifact Claude Code discovers
  first; not a Skill and not a router of Knowledge.
- `## Dependency Model` sharpened to name `depends_on` as the binding edge and
  `related` as explicitly outside it.
- `## Skill` definition: "Task entrypoint" is now ambiguous against `Entry` — reword
  to "Routes a task to the Knowledge it needs".
- `## Workflow` retained unchanged; it was always correct.

## Task 17 — `AGENTS.md`

Drives: B3, E1, A4

- Layer Order: four layers (already correct — verify).
- Rules: `Workflows compose multiple Skills` retained; add that a Skill never routes
  to a Skill.
- Startup Procedure step 3: "Resolve the correct Skill" → "Resolve the correct
  Workflow or Skill from skills/index.md" (E1).
- Expected Behavior: add "which Workflow was selected, if any".

## Task 18 — `CLAUDE.md` and `CONTRIBUTING.md`

Drives: B3, S3, A3

- `CLAUDE.md:7` layer order line — unchanged (already four layers), verify.
- `CLAUDE.md`: add `reference-spec.md` and `skill-management.md` to the validation
  section, and point the "Validating an artifact" block at both scripts once Phase 3
  lands (noted as a Phase 3 follow-up, not done here).
- `CONTRIBUTING.md:12`: layer order text unchanged; add a pointer to
  `skill-management.md` as the procedure for adding to an existing Skill.

## Task 19 — Phase list and stragglers

Drives: F3, A2b

- `docs/development-process.md`: Phase 7 Workflows is being started in Phase 4 of this
  effort — update its status rather than its numbering. Keep `Approved 1.0.0`; bump to
  `1.1.0` since content changed.
- `docs/foundation/vision.md`: add the missing `Status:` line.
- `docs/contributing/documentation-style.md`: review for the two-line header
  convention and any stale layer references.

## Task 20 — Validation and release bookkeeping

- `python3 -m unittest discover tests/` passes (no code changed this phase; this is a
  regression check).
- `claude plugin validate .` passes.
- Every rewritten document carries `Status: Approved` / `Version: 1.0.0`.
- Grep for stragglers: no document still declares `Review` as a lifecycle state, a
  60-line Skill cap, a 5-layer architecture, `type:`/`updated:` as the metadata
  dialect, or Templates as a layer.
- `CHANGELOG.md` gains an `[Unreleased]` entry. **No release version bump this
  phase** — the five-file version rule is untouched because no shipped artifact
  changed. The bump happens when Phase 2 lands the artifact migration.
- `README.md` and `npx/README.md` are not touched, so the byte-identical mirror holds
  trivially. Confirm with `diff`.

## Out of scope for Phase 1

- Any change to `knowledge/`, `skills/`, `references/`, `workflows/` — Phases 2 and 4.
- Any change to `scripts/` or `tests/` — Phase 3.
- Tier 1 content — Phase 5, and its scope is not yet decided.
