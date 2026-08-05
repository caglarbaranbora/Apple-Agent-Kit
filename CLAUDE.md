# CLAUDE.md

Repo dev conventions for anyone (human or agent) working *on* this codebase. This is different from `AGENTS.md`, which is the routing spec for agents *consuming* the kit as end-users of the plugin — don't conflate the two.

## Layer order (do not violate)

References → Knowledge → Skills → Workflows

- References are authoritative sources (traceable to official Apple docs).
- Knowledge Contracts define implementation rules, one per atomic concept.
- Skills route to Knowledge Contracts deterministically — they must never embed domain knowledge directly.
- Workflows compose multiple Skills.

## File naming and structure

- One vertical slice = one directory under `references/<domain>/`, `knowledge/<domain>/`, `skills/<domain>/`.
- Knowledge Contract IDs follow `knowledge.<domain>.<slug>` (see existing files under `knowledge/` for examples).
- New domains get their own subdirectory in each of `references/`, `knowledge/`, `skills/` — don't mix domains inside one file.
- Required metadata fields and section headers per artifact type are enforced by `scripts/validate_artifact.py` (see `REQUIRED_SECTIONS` / `REQUIRED_METADATA_FIELDS` in that file) — don't hand-roll a new structure.

## Validating an artifact

```bash
python3 scripts/validate_artifact.py <path/to/artifact.md> --type knowledge   # or: skill | reference
```

Run this against any new or modified Knowledge Contract, Skill, or Reference before committing.

## Running tests

```bash
python3 -m unittest tests/test_validate_artifact.py -v
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

- `## Skills` section: one bullet per Skill — name, one-line description of what it routes, and at least one concrete example invocation with its routing target (e.g. `"check this screen's layout against HIG" → layout.md`). Keep examples as *specific tasks*, not broad topic requests.
- `## What's New`: one line at the top describing what shipped and when (`YYYY-MM-DD — <what shipped>`).

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
