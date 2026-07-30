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

## Commit conventions

- One vertical slice or one fix per commit where practical.
- Don't touch `npx/package.json` or root config without calling it out explicitly — see the license/publishing notes in `README.md`.
