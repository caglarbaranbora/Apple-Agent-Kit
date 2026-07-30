# Apple Agent Kit as a Claude Code Plugin — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Package Apple Agent Kit so it can be installed into any Claude Code session as
a plugin — via a self-hosted plugin marketplace, with an `npx` command as a
convenience install shortcut. Codex-specific packaging is explicitly deferred
(see Decisions, item 5).

## Context

Apple Agent Kit (`references/`, `knowledge/`, `skills/`, `workflows/`,
`AGENTS.md`) is currently only usable by manually pointing an agent at this
repo. Claude Code's plugin system lets users install it with
`/plugin install` instead. This spec covers turning the existing repo into an
installable plugin without disturbing its existing architecture.

Style-guide domain build (RFC 0001) is complete and PDF-verified as of this
session; this is a separate, independent initiative.

## Decisions

### 1. Repo root is both the plugin and its own marketplace

Add `.claude-plugin/plugin.json` (plugin manifest) and
`.claude-plugin/marketplace.json` (single-entry marketplace catalog, plugin
`source: "."`) at repo root. No existing directory moves. This is the
documented "self-hosted marketplace" pattern from Claude Code's plugin docs —
a marketplace repo can list a plugin that lives at its own root via a
relative `source` path.

`plugin.json`:
```json
{
  "name": "apple-agent-kit",
  "description": "Spec-first knowledge system for AI coding agents developing Apple platform applications.",
  "version": "0.1.0",
  "author": { "name": "caglarbaranbora" }
}
```

`marketplace.json`:
```json
{
  "name": "apple-agent-kit-marketplace",
  "owner": { "name": "caglarbaranbora" },
  "plugins": [
    {
      "name": "apple-agent-kit",
      "source": ".",
      "description": "Spec-first knowledge system for AI coding agents developing Apple platform applications."
    }
  ]
}
```

### 2. One thin adapter skill, zero changes to existing skill/knowledge files

**Rejected alternative:** converting every existing `skills/**/*.md` file
into Claude Code's native `skills/<name>/SKILL.md` format (real frontmatter,
independently model-invoked). Rejected because Claude Code's native skill
system is semantic/model-invoked, and this project's core architectural
principle (AGENTS.md: "Prefer deterministic routing over semantic search";
architecture.md: "Routing is deterministic") is the opposite of that. Making
every skill independently model-invoked would let Claude's fuzzy matching
bypass the `skills/index.md` Discovery Rules table this project relies on.

**Chosen approach:** add exactly one new file,
`skills/apple-agent-kit/SKILL.md`, in Claude Code's native format (real YAML
frontmatter with a `description` field broad enough to trigger on Apple
platform UI/app development tasks). Its body is short and delegates
entirely to the existing system:

```markdown
---
description: Apple platform app development — UI terminology, style guide rules, authentication flows, and other Apple Agent Kit domains. Use for any task involving Apple platform UI text, capitalization, or implementation conventions.
---

Read AGENTS.md at the repository root and follow its Startup Procedure
exactly: read AGENTS.md, read README.md, resolve the correct Skill from
skills/index.md, load only the Knowledge Contracts that Skill routes to,
execute the task. Do not search the repository randomly. Do not bypass
routing.
```

This means the plugin has exactly one native entry point, but task
narrowing still happens via the existing deterministic
`skills/index.md` → specific skill → `routes:` → Knowledge Contract chain,
completely unchanged. A task scoped to (for example) button labels still
loads only `general-button-labels.md` (or
`knowledge/authentication/button-labels.md` via its `depends_on`), not the
other 24+ style-guide contracts.

No existing file under `skills/`, `knowledge/`, or `references/` is
modified, renamed, or moved by this work.

### 3. npx installer is a separate, isolated Node package

**Rejected alternative:** a `package.json` at repo root. Rejected per
existing project convention (`CLAUDE.md`: "Don't touch package.json,
lockfiles, or native config ... without approval — these are shared/risky
files") and because this repo is fundamentally a content repo, not a Node
project — conflating the two at the root is unnecessary.

**Chosen approach:** a new `npx/` directory containing its own
`package.json` (npm package name `apple-agent-kit`, matching the plugin
name) and a `bin/install.js` script. Running `npx apple-agent-kit` (once
published) executes that script, which shells out to the `claude` CLI:

```
claude plugin marketplace add <github-owner>/<repo>
claude plugin install apple-agent-kit@apple-agent-kit-marketplace
```

This assumes the user already has the `claude` CLI installed and
authenticated; the script should fail with a clear error message (not a
silent no-op) if `claude` isn't on `PATH`. The `npx` command is a
convenience shortcut only — the real, primary distribution channel is the
plugin marketplace itself. Nothing in this repo's existing content pipeline
depends on the npx package existing.

### 4. Explicitly out of scope for this plan (needs separate approval later)

- Running `npm publish` for the `npx/` package — claims a public npm
  package name and requires the user's npm credentials.
- Pushing this repo to GitHub / making the marketplace publicly addable —
  hard-to-reverse, visible-to-others actions.
- Submitting to Anthropic's community marketplace review.

These are not implementation tasks in the plan that follows this spec. They
require the user's explicit go-ahead when reached, per this project's
"check before hard-to-reverse or externally-visible actions" norm.

### 5. Codex marketplace packaging is deferred

The user confirmed Codex-specific packaging can be revisited later if scope
allows. No Codex-specific artifact is created by this plan. `AGENTS.md`
already gives Codex users baseline compatibility for free (Codex reads
`AGENTS.md` by convention), so nothing is lost by deferring further,
Codex-specific packaging work.

## Consequences

- Repo gains 4 new files: `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `skills/apple-agent-kit/SKILL.md`, and
  the `npx/` package (2+ files: `package.json`, `bin/install.js`).
- Zero existing files are modified.
- The project's deterministic-routing architecture (AGENTS.md,
  architecture.md) is unchanged and unaffected.
- Actually publishing to npm or pushing a public marketplace remains a
  separate, user-approved future step — this plan only builds the
  installable artifacts locally and validates them with
  `claude --plugin-dir`.

## Testing / Validation Plan

- `claude plugin validate .` (or the plugin-dir equivalent) against the
  repo root to confirm `plugin.json` and `marketplace.json` are
  well-formed.
- `claude --plugin-dir .` locally, then `/apple-agent-kit:apple-agent-kit`
  (or whatever the resolved skill invocation is) to confirm the adapter
  skill loads and correctly points Claude at AGENTS.md.
- Manually exercise one narrow task (e.g., "what's the correct button
  label wording?") through the installed plugin and confirm only the
  expected Knowledge Contract(s) load — i.e., confirm the adapter skill did
  not widen routing beyond what direct repo use already does.
- `npx/bin/install.js` tested locally via `node npx/bin/install.js`
  (without actual `npm publish`), confirming it calls the right `claude`
  CLI commands and fails clearly if `claude` isn't installed.
