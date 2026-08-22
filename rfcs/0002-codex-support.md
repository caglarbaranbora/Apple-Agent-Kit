# RFC 0002: Codex Support

Status: Proposed
Version: 0.1.0

## Purpose

Records the design for making Apple Agent Kit's content usable from OpenAI's Codex
CLI, not just Claude Code, and corrects a stale assumption in
`docs/specifications/skill-spec.md` about how that support would work.

## Context

`docs/specifications/skill-spec.md` line 34 reserves `skills/<domain>/agents/openai.yaml`
for "future Codex-specific behavior," implying each of the 36 domain Skills would need
its own hand-authored Codex translation file. That assumption predates any actual design
work and was never tested against how Codex's own extension mechanism behaves.

Investigation for this RFC found:

- `AGENTS.md` (this repo's root) is already fully platform-agnostic. Its Startup
  Procedure — read this file, read README, resolve the task via `skills/index.md`,
  load the matched Skill, load the Knowledge Contracts it routes to, load their
  dependencies, execute — never names a Claude-Code-specific tool or mechanism. It
  reads as generic instructions any file-reading agent can follow, and `AGENTS.md` is
  itself the OpenAI-originated convention Codex looks for automatically.
- `skills/index.md` (the Routing Index) and every `SKILL.md`'s body (`## Purpose`,
  `## Routing`, `## Stop Conditions`) are plain prose tables and bullet lists — no
  embedded Claude Code tool-call syntax (no literal `Read`/`Edit`/`Grep` invocations).
  The only Claude-Code-specific part of a Skill is its YAML frontmatter, which Claude
  Code's own Skill-loading mechanism parses for triggering; the prose body underneath
  is what actually gets followed, by either platform.
- Codex CLI has, since March 2026, its own plugin marketplace (`/plugin marketplace add
  owner/repo`, closely mirroring Claude Code's `claude plugin marketplace add`) plus a
  native skill-discovery mechanism via `~/.agents/skills/<name>` (a symlink to a
  `skills/` directory).
- `superpowers` (a comparable multi-skill plugin already installed in this environment)
  ships exactly this pattern: a `.codex-plugin/plugin.json` manifest whose `"skills"`
  field points at the **same** `skills/` directory used for Claude Code — no per-skill
  translation files — plus a `.codex/INSTALL.md` covering both the marketplace command
  and a manual clone-and-symlink fallback. superpowers' `openai.yaml`-shaped concern
  (see its `codex-tools.md` "Named agent dispatch" section) exists only because its
  *workflow* skills dispatch named subagents (`Task tool (superpowers:code-reviewer)`),
  which Codex has no named-agent registry for. Apple Agent Kit's Skills are pure
  routing tables — keyword → Knowledge Contract path — and never dispatch a named
  subagent, so that concern does not apply here at all.

The corrected scope is therefore small: no Knowledge Contract or Skill content changes,
no per-domain files, four additions/edits total.

## Decisions

### 1. Add `.codex-plugin/plugin.json`, pointing at the existing `skills/` directory

Mirrors superpowers' manifest shape: `name`, `version`, `description`, `author`,
`homepage`, `repository`, `license`, `keywords`, and `"skills": "./skills/"`. No
`interface`/`capabilities`/`defaultPrompt` block for v1 — those are Codex-marketplace
presentation metadata, not required for skills to load, and can be added later without
a breaking change. Content values (`description`, `keywords`) are drawn from
`.claude-plugin/plugin.json`, not duplicated by hand from scratch, so the two manifests
describe the same package consistently.

Rejected alternative: a per-domain `agents/openai.yaml` under each `skills/<domain>/`,
per the stale `skill-spec.md` line. Rejected because Codex's native skill discovery
already reads the same `SKILL.md` files Claude Code uses — there is nothing to
translate, and 36 hand-authored files would be pure duplication with no behavioral
purpose, carrying only drift risk (a Skill edited on the Claude Code side without its
Codex twin updated).

### 2. Add `.codex/INSTALL.md`

Two documented paths, both manual (Codex's marketplace command runs inside the Codex
CLI's own session, not from an external script):

- **Marketplace**: `/plugin marketplace add caglarbaranbora/Apple-Agent-Kit` then
  install, run inside Codex.
- **Manual clone + symlink**: `git clone` this repo to `~/.codex/apple-agent-kit`, then
  `ln -s ~/.codex/apple-agent-kit/skills ~/.agents/skills/apple-agent-kit`, matching
  superpowers' documented fallback for Codex versions or setups predating native
  marketplace support.

### 3. Correct `docs/specifications/skill-spec.md` line 34

Replace the `openai.yaml` claim with the real mechanism: Codex support lives at
`.codex-plugin/plugin.json` (repo root, one manifest, not per-Skill), pointing at the
same `skills/` directory Claude Code uses. Skills continue to route deterministically
to Knowledge Contracts and never embed domain knowledge or dispatch named subagents,
regardless of which platform loads them — nothing about the Skill authoring rules in
this spec changes.

### 4. `npx/bin/install.js` gains a Codex fallback path, instructions-only

Current behavior: check for `claude` on PATH; if absent, print an error and exit 1.

New behavior: if `claude` is absent, additionally check for `codex` on PATH.
- `codex` found: print the marketplace command
  (`/plugin marketplace add caglarbaranbora/Apple-Agent-Kit`) to run inside Codex, and
  a pointer to `.codex/INSTALL.md` for the manual path. Exit 0 — this is a successful
  outcome for a Codex-only environment, not an error.
- Neither `claude` nor `codex` found: keep today's error message, mentioning both
  tools.

The script never attempts to invoke `codex` itself (no `spawnSync('codex', ...)`) —
Codex's plugin install is a command typed inside an interactive Codex session, not a
non-interactive CLI subcommand this script could shell out to safely.

### 5. `.codex-plugin/plugin.json`'s `version` joins the release-version consistency check

`CLAUDE.md`'s "Release version consistency" section currently names five files that
must match exactly on every release. `.codex-plugin/plugin.json` becomes the sixth,
starting from its first commit: it ships already set to the repo's current release
version (2.2.0 at implementation time), not an independent `0.1.0`. `CLAUDE.md` itself
gets a one-line edit adding it to that list, since the check is defined there.

## What does NOT change

- No `knowledge/`, `skills/*/SKILL.md`, `references/`, or `workflows/` content.
- No new artifact type, no new validator level, no `scripts/validate_artifact.py`
  changes — `.codex-plugin/plugin.json` is plain JSON with no schema this repo's
  validators need to enforce beyond "is it valid JSON with the right version string,"
  which the existing release-version check already covers once it's added there.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — untouched;
  Claude Code's install path is unaffected.
- `AGENTS.md` and `skills/index.md` — already platform-agnostic, confirmed during
  investigation, no edit needed.

## Test Plan

- `.codex-plugin/plugin.json` is valid JSON (`python3 -m json.tool` or equivalent) and
  its `skills` path resolves to the real `skills/` directory.
- `claude plugin validate .` still passes unchanged (separate manifest, not read by
  Claude Code's validator).
- `npx/bin/install.js --dry-run`, manually exercised in three shell states: `claude` on
  PATH (existing behavior, unchanged output); `claude` absent + `codex` present (new
  Codex-instructions path, exit 0); neither present (existing error path, updated
  wording, exit 1).
- Release-version check (manual, per `CLAUDE.md`): all six files report the same
  version string before any release commit.
