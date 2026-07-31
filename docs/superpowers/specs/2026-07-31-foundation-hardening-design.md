# Native Skill Foundation Hardening — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Turn the two existing sub-skills (`authentication`, `style-guide`) into real,
independently-discoverable Claude Code skills, fix the metadata/section
drift that lets `skills/authentication/login.md` fail its own validator, and
update the skill schema/validator to support this — so that every future
domain (Widgets, HealthKit, App Intents/Siri, StoreKit, ...) can be added as
a native skill from day one instead of hidden behind a single umbrella
skill's internal routing table. This is explicitly foundation work: no new
domain is added in this pass.

## Context

Prompted by comparing this repo's architecture against
`github.com/jakubkrehel/skills` (the `interfaces` plugin). That repo ships
one native, independently-invocable skill per domain; this repo currently
ships exactly one native skill (`skills/apple-agent-kit/SKILL.md`) and
simulates two more (`skills/authentication/login.md`,
`skills/style-guide/writing.md`) via plain markdown files that the harness
does not recognize as skills at all — they lack real frontmatter and are not
named `SKILL.md`, so `claude plugin validate` and the Skill tool never see
them. Confirmed by running the repo's own validator:

```
FAIL: skills/authentication/login.md
  - missing required section: ## Triggers
  - missing required section: ## Stop Conditions
  - missing metadata YAML block
```

The stated goal (this session) is to grow this repo into a full "iOS
developer kit" covering most Apple frameworks over time (see
`docs/architecture/domain-map.md` Tier 1-3 roadmap). At that scale, forcing
every domain through one umbrella skill's internal text-routing table stops
scaling the way independently discoverable native skills do.

### Supersedes: `2026-07-30-claude-code-plugin-packaging-design.md` §2

That spec explicitly rejected converting sub-skills to native format,
reasoning that Claude Code's native skill invocation is
semantic/model-invoked and would let fuzzy matching bypass this project's
deterministic-routing principle (AGENTS.md: "Prefer deterministic routing
over semantic search").

This is superseded because native skills have two invocation paths, and
only one is fuzzy:

1. **Explicit `/skill-name` invocation** — fully deterministic, no semantic
   matching involved. This is the user's actual primary usage pattern
   (confirmed this session).
2. **Automatic/proactive invocation** — the agent judges relevance from the
   skill's frontmatter `description` when the user does not name a skill.
   This is the only fuzzy path, and its blast radius is bounded: routed
   domains already overlap at the edges (e.g. `style-guide` already routes
   `sign-in-and-authentication-terminology`), so a wrong pick lands on an
   adjacent, still-relevant knowledge set rather than an unrelated one. The
   umbrella skill remains as a broad fallback for anything that matches
   neither domain skill.

Given the goal shift toward a large, native-discoverable multi-domain kit,
this tradeoff is accepted.

## Decisions

### 1. Migrate both existing sub-skills to native format now

`skills/authentication/login.md` → `skills/authentication/SKILL.md`
`skills/style-guide/writing.md` → `skills/style-guide/SKILL.md`

Both get real top-of-file YAML frontmatter (see Decision 4) and drop their
old `## Triggers` body section in favor of the frontmatter `description`.
This also fixes the `login.md` validator drift as a side effect — it was
never a passing artifact.

### 2. Umbrella skill stays, becomes explicit fallback

`skills/apple-agent-kit/SKILL.md` is unchanged in role: broad-description
entry point for tasks that don't clearly match a domain skill. One gap is
fixed: it's missing an explicit `name` field (currently frontmatter has only
`description`); add `name: apple-agent-kit` for consistency with the new
requirement that every skill declares its name explicitly rather than
relying on directory-name inference.

### 3. Directory/file convention: `skills/<domain>/SKILL.md`

Matches Claude Code's native convention and `jakubkrehel/skills`. Preserves
room for a future `skills/<domain>/<sub-skill>/SKILL.md` nesting if a domain
ever needs more than one skill (none do yet).

### 4. Metadata format: single unified frontmatter (Option A)

**Rejected alternative:** two separate metadata blocks (harness-facing
`---name/description---` plus the existing internal ` ```yaml ` fenced
block). Rejected for duplicated fields and because it eats further into the
line budget on files already near the cap (`writing.md` was 59/60 lines).

**Chosen approach:** move the existing internal metadata (currently a
` ```yaml ` fenced block under a `## Metadata` heading, matched by regex
anywhere in the file) into real frontmatter at byte offset 0 of the file —
`---\n...\n---` before any other content, which is what Claude Code's skill
loader actually parses for `name`/`description`. Add two new required
fields, keep all existing ones:

```markdown
---
name: authentication
description: Route authentication-related Apple platform implementation tasks to the correct Knowledge Contracts — sign-in, sign-up, credentials, biometrics. Use when the task involves login screens, sign-in terminology, or authentication accessibility. Triggers on sign in, sign up, login, authentication, Apple Account, credentials, biometrics, Face ID, Touch ID, passkeys.
id: skill.authentication.login
title: Login Skill
version: 0.2.0
status: Draft
artifact_type: skill
domain: Authentication
routes:
  - knowledge.authentication.authentication
  - knowledge.authentication.sign-in-terminology
  - knowledge.authentication.button-labels
  - knowledge.authentication.accessibility-forms
related: []
last_updated: 2026-07-31
---

# Login Skill

## Purpose
...

## Routing
...

## Stop Conditions
...
```

`description` absorbs what the old `## Triggers` body section used to hold,
written in `jakubkrehel/skills` style (a "Use when..." clause plus a
"Triggers on ..." keyword list) since that's the text the harness actually
matches against for automatic invocation.

This applies to `artifact_type: skill` files only. Knowledge and Reference
files are untouched — they are never independently loaded by the harness as
skills, so they keep the existing `## Metadata` + fenced ` ```yaml ` block
convention unchanged.

### 5. Validator and skill-spec changes

`scripts/validate_artifact.py`:
- `REQUIRED_METADATA_FIELDS["skill"]`: add `name`, `description` to the
  existing list.
- `REQUIRED_SECTIONS["skill"]`: drop `## Triggers`. Remaining required:
  `## Purpose`, `## Routing`, `## Stop Conditions`.
- `LINE_CAPS["skill"]`: `60` → `80`, to absorb frontmatter overhead without
  squeezing routing content.
- `extract_metadata_block`: for `artifact_type: skill`, require the YAML
  block to be true frontmatter anchored at the start of the file
  (`^---\n(.*?)\n---`), not a fenced block matched anywhere in the document.
  Knowledge/Reference extraction logic (fenced-block-anywhere) is unchanged.

`docs/specifications/skill-spec.md`: update Required Metadata, Required
Sections, and Size Limit to match. Add a short "Frontmatter Format" section
documenting the byte-offset-0 requirement and noting `agents/openai.yaml`
(see Decision 7) as a documented-but-not-yet-built future convention.

An optional `## Review Output Format` section (severity table + verdict,
borrowed from `jakubkrehel/skills`) is documented as available but **not**
added to `REQUIRED_SECTIONS` — only relevant for skills whose task is
auditing existing text/code against a domain's rules (e.g. `style-guide`
reviewing UI copy), not for skills that only route implementation guidance
(e.g. `authentication`). Left as a per-skill author decision.

### 6. Ownership tracking: extend existing `domain-map.md`, no new artifact

No new ownership-table file. `docs/architecture/domain-map.md` already has
Tier tables and a `Cross-Domain Notes` section for overlap resolution
(currently covers the `authentication` / `authenticationservices` /
`sign-in-with-apple` overlap). Add a one-line **Owns** description per
domain row in the Tier tables, so scanning at a glance which domain is
responsible for what gets easier as more domains are added — mirrors what
`jakubkrehel/skills`' ownership table provides, without introducing a
parallel document to keep in sync.

### 7. Codex readiness: convention documented only, nothing scaffolded

No `agents/` directories or `openai.yaml` files are created in this pass —
there's no Codex-specific behavior to encode yet. `CLAUDE.md` gets one note:
future Codex support lands at `skills/<domain>/agents/openai.yaml` (matching
`jakubkrehel/skills`' layout) so the directory convention doesn't need to
change when that work starts.

## Consequences

- `skills/authentication/login.md` and `skills/style-guide/writing.md` are
  renamed and reformatted; both become real, independently-invocable Claude
  Code skills (`/apple-agent-kit:authentication`,
  `/apple-agent-kit:style-guide` once namespaced by the plugin).
- `skills/index.md`'s Discovery Rules table role narrows: it no longer
  decides *which skill fires* (the harness does that now, explicitly or via
  description matching) but each skill's own `## Routing` section still
  deterministically decides *which Knowledge Contracts load* — the
  knowledge-selection determinism this project cares about is unchanged.
- `scripts/validate_artifact.py` and `docs/specifications/skill-spec.md`
  schema changes are breaking for any skill file not yet migrated — none
  exist outside the two covered here, so no dangling artifacts.
- `.claude-plugin/plugin.json` / `marketplace.json` need no changes; skills
  are auto-discovered from `skills/` by directory convention.
- This is pre-1.0 (`npx/package.json` at `0.1.1`), no external consumers
  depend on the current sub-skill file paths, so no backward-compatibility
  shim is needed.

## Testing / Validation Plan

- Update `tests/test_validate_artifact.py`'s `VALID_SKILL` fixture to the
  new frontmatter format (real `---` block, `name`/`description` fields, no
  `## Triggers` section) and confirm `validate_artifact.validate_text`
  reports zero errors.
- Add a regression test asserting the old fenced-`## Metadata`-anywhere
  format now fails for `artifact_type: skill` (frontmatter must be at byte
  offset 0), to lock in the Decision 5 behavior change.
- `python3 -m unittest tests/test_validate_artifact.py -v` — full pass.
- `python3 scripts/validate_artifact.py skills/authentication/SKILL.md --type skill` and the `style-guide` equivalent — both `PASS`.
- `claude plugin validate .` — confirms the manifest and the two new native
  `SKILL.md` files are well-formed and discovered.
- Manually invoke `/apple-agent-kit:authentication` (or resolved name) in a
  Claude Code session and confirm it loads only the four routed
  authentication Knowledge Contracts — not the full style-guide set.

## Out of Scope

- Adding any new domain (Widgets, HealthKit, App Intents, etc.) — follow-up
  work, separate spec, once this foundation lands.
- Building actual Codex `agents/openai.yaml` content.
- Publishing/version-bumping the npm package.
