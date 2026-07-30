# Contributing to Apple Agent Kit

## License note

This project is source-available under the [PolyForm Strict License 1.0.0](LICENSE) — not open source. Reading the code, running it, and forking on GitHub to submit a pull request back to this repository are fine. Republishing, redistributing, or reselling the software (including forks published elsewhere) is not permitted under the license.

By submitting a pull request, you agree that your contribution is licensed to this project under the same terms as [LICENSE](LICENSE).

## Before opening a PR

1. Read `CLAUDE.md` for repo dev conventions (validation scripts, file naming, layer order).
2. Read `AGENTS.md` if your change touches how Skills/Knowledge Contracts route — it defines the layer order (References → Knowledge → Skills → Workflows) and what's forbidden (e.g. embedding domain knowledge inside Skills, duplicating Knowledge Contracts).
3. Run the validation scripts under `scripts/` against any new or changed artifact before opening the PR.
4. Keep changes scoped to one domain/vertical slice per PR where possible.

## What makes a good contribution

- New Knowledge Contracts: atomic, traceable to an official Apple documentation source, and routed through exactly one Skill.
- Bug fixes: include the failing case you found, not just the fix.
- Docs: keep `README.md` and `AGENTS.md` in sync if you change repository structure.

## Reporting issues

Open a GitHub issue with a clear repro or the specific Knowledge Contract/Skill affected.
