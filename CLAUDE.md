# CLAUDE.md

Repo dev conventions for anyone (human or agent) working *on* this codebase. This is different from `AGENTS.md`, which is the routing spec for agents *consuming* the kit as end-users of the plugin — don't conflate the two.

## Layer order (do not violate)

References → Knowledge → Skills → Workflows

- References are authoritative sources (traceable to official Apple docs).
- Knowledge Contracts define implementation rules, one per atomic concept.
- Skills route to Knowledge Contracts deterministically — they must never embed domain knowledge directly, and never route to another Skill.
- Workflows compose multiple Skills. Composing Skills is a Workflow's job, never a Skill's.

`templates/` and `scripts/` are authoring and tooling directories, not layers.

## The normative specs

These are the authority on artifact structure. Don't hand-roll a new shape — and if a
spec and the validator disagree, that's a release-blocking defect, not a preference.

| Artifact | Spec |
|---|---|
| Knowledge Contract | `docs/specifications/knowledge-spec.md` |
| Skill | `docs/specifications/skill-spec.md` |
| Reference | `docs/specifications/reference-spec.md` |
| Workflow | `docs/specifications/workflow-spec.md` |
| Metadata fields (all types) | `schemas/metadata.schema.md` |

Adding to, splitting, or retiring a Skill: `docs/specifications/skill-management.md`.

## File naming and structure

- One vertical slice = `references/apple/<domain>.md`, `knowledge/<domain>/`, `skills/<domain>[-<facet>]/`.
- Skill directories are always flat — never `skills/<domain>/<facet>/`. Claude Code derives the invocable name from the directory.
- Knowledge Contract IDs follow `knowledge.<domain>.<slug>` and must agree with the path; `domain` must agree with the directory name.
- New domains get their own entry in each of `references/apple/`, `knowledge/`, `skills/` — don't mix domains inside one file.

## Validating

Two scripts, split by scope. Both must pass before committing. See
`docs/validation-model.md` for what each level covers.

```bash
# Level 1 — one file, structural
python3 scripts/validate_artifact.py <path/to/artifact.md> --type knowledge   # or: skill | reference | workflow | entry

# Level 1 — every artifact at once, each type read from its own metadata
python3 scripts/validate_artifact.py . --all

# Levels 2-3 — repository-wide: ids, edges, the dependency DAG, routing, index sync
python3 scripts/validate_repo.py .
```

Levels 4-5 are semantic and are checked by reading, in review — no script decides them.

Link freshness is a third script, deliberately outside the levels because it leaves
the machine — it fetches every cited URL and treats a redirect as a finding, since
the form Apple redirects from is the one that later 404s. CI runs it on the files a
PR changes, plus a weekly full sweep. Run it yourself after editing any `## Source`
block or `references:` list:

```bash
python3 scripts/check_links.py . --files <changed files>   # or `.` for all 739
```

Lifecycle transitions are a fourth script, outside the levels for the same reason:
a transition exists between two versions of a file, not inside one working tree, so
it has nothing to check until there is a pull request. Run it after changing any
`status:`:

```bash
python3 scripts/check_transitions.py .            # vs origin/main
```

## Running tests

```bash
python3 -m unittest discover tests/ -v
```

## Validating the plugin manifest

```bash
claude plugin validate .
```

Run this after any change to `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, or `skills/apple-agent-kit/SKILL.md`.

## Codex support (future)

Not built yet. When added, Codex-specific behavior for a domain skill goes
at `skills/<domain>/agents/openai.yaml`, matching the per-domain skill
layout already in place — no directory restructuring needed when that work
starts.

## Updating README.md for a new/changed domain or Skill

Every new domain or Skill (and any material change to an existing one) must update `README.md`:

- `## Skills` section: one bullet per Skill, name + one-line description only — no examples, no routing tables, no v1-scope caveats. Format: `- **`name`** — one-line description. → [SKILL.md](skills/name/SKILL.md)`. Routing tables and example invocations belong in the Skill's own `SKILL.md` (and `skills/index.md`), not in `README.md` — this section is a table of contents, not documentation.
- `## What's New`: add one line at the top describing what shipped and when (`YYYY-MM-DD — <what shipped>`), **then trim the section to its 3 most recent bullets** — drop the oldest bullet(s) past 3 regardless of date. The full history already lives in `CHANGELOG.md`; `README.md`'s What's New is a preview, not an archive.

Do this in the same PR/commit that ships the domain or Skill — not as a follow-up.

## Release version consistency

The project has one release version number, shared by exactly these five files:

- `README.md` (the `Version:` line near the top)
- `npx/README.md` (the `Version:` line near the top)
- `npx/package.json` (`version` field)
- `.claude-plugin/plugin.json` (`version` field)
- `CHANGELOG.md` (its newest non-`[Unreleased]` release header, e.g. `## [1.0.0] - YYYY-MM-DD`)

These five MUST always match exactly. Before any commit that bumps the
release version, or as part of any final/holistic review, check all five —
a mismatch between them is a release-blocking defect, not a nitpick.
Per-artifact `version:` fields inside individual Knowledge Contracts,
Skills, and References are a separate, independent versioning scheme
(component-level, starts at `0.1.0`, bumped per-artifact as that artifact
changes) — they are NOT part of this four-file release-version check and
do not need to match the release version.

## npm package publishing

`npx apple-agent-kit` (`npx/`) is a thin installer — it runs `claude plugin marketplace add <repo>` and `claude plugin install`, pointing at this GitHub repo directly. It does not bundle References/Knowledge/Skills content. **Shipping a new domain or Skill does NOT require an npm publish** — content lands for users as soon as it's on `main`.

Only bump `npx/package.json` version and `npm publish` when `npx/package.json` or `npx/bin/install.js` itself changes.

## Commit conventions

- One vertical slice or one fix per commit where practical.
- Don't touch `npx/package.json` or root config without calling it out explicitly — see the license/publishing notes in `README.md`.
