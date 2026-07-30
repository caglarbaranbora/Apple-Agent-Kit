# Claude Code Plugin Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the Apple Agent Kit repo into an installable Claude Code plugin (self-hosted marketplace + one adapter skill) plus a standalone `npx` install shortcut, without modifying any existing `skills/`, `knowledge/`, or `references/` file.

**Architecture:** Repo root doubles as both the plugin directory and a single-entry marketplace catalog (`.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`, plugin `source: "."`). One new native-format skill (`skills/apple-agent-kit/SKILL.md`) is the sole Claude-Code-invoked entry point; its body delegates entirely to the existing `AGENTS.md` deterministic routing flow. A separate, isolated `npx/` Node package wraps `claude plugin marketplace add` + `claude plugin install` as a convenience installer — it does not touch repo-root `package.json` (there isn't one) and is not published to npm as part of this plan.

**Tech Stack:** Claude Code plugin manifest format (JSON), Node.js (installer script, no dependencies), Python 3 (`json.tool` for manifest syntax checks — already used elsewhere in this repo via `scripts/validate_artifact.py`).

**Reference:** `docs/superpowers/specs/2026-07-30-claude-code-plugin-packaging-design.md` — read decisions 1–5 before starting; this plan implements decisions 1–3 and the Testing/Validation Plan section only. Decision 4 (npm publish, GitHub push, marketplace review) and decision 5 (Codex) are explicitly NOT implemented by this plan.

**Repo facts confirmed during planning:**
- git remote: `git@github.com:caglarbaranbora/Apple-Agent-Kit.git` → GitHub slug `caglarbaranbora/Apple-Agent-Kit`
- `claude` CLI is present on this machine at `/Users/caglarbaranbora/.npm-global/bin/claude`
- `node` v24.15.0 and `npm` 11.14.1 are present
- `scripts/validate_artifact.py` already exists in this repo for Knowledge/Skill artifact validation — it is unrelated to plugin manifest validation and is not used in this plan

---

### Task 1: Plugin manifest

**Files:**
- Create: `.claude-plugin/plugin.json`

- [ ] **Step 1: Create the `.claude-plugin` directory and manifest file**

```bash
mkdir -p "/Users/caglarbaranbora/vault/Apple Agent Kit/.claude-plugin"
```

Create `/Users/caglarbaranbora/vault/Apple Agent Kit/.claude-plugin/plugin.json`:

```json
{
  "name": "apple-agent-kit",
  "description": "Spec-first knowledge system for AI coding agents developing Apple platform applications.",
  "version": "0.1.0",
  "author": {
    "name": "caglarbaranbora"
  }
}
```

- [ ] **Step 2: Verify it's valid JSON**

Run:
```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && python3 -m json.tool .claude-plugin/plugin.json
```
Expected: the same JSON printed back, pretty-formatted, no error.

- [ ] **Step 3: Commit**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git add .claude-plugin/plugin.json
git commit -m "feat: add Claude Code plugin manifest"
```

---

### Task 2: Marketplace manifest

**Files:**
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create the marketplace catalog file**

Create `/Users/caglarbaranbora/vault/Apple Agent Kit/.claude-plugin/marketplace.json`:

```json
{
  "name": "apple-agent-kit-marketplace",
  "owner": {
    "name": "caglarbaranbora"
  },
  "plugins": [
    {
      "name": "apple-agent-kit",
      "source": ".",
      "description": "Spec-first knowledge system for AI coding agents developing Apple platform applications."
    }
  ]
}
```

- [ ] **Step 2: Verify it's valid JSON**

Run:
```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && python3 -m json.tool .claude-plugin/marketplace.json
```
Expected: the same JSON printed back, pretty-formatted, no error.

- [ ] **Step 3: Commit**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git add .claude-plugin/marketplace.json
git commit -m "feat: add self-hosted plugin marketplace catalog"
```

---

### Task 3: Adapter skill

**Files:**
- Create: `skills/apple-agent-kit/SKILL.md`

This is the only file in this plan that touches `skills/`. It is a NEW file at a NEW path (`skills/apple-agent-kit/`) — it does not modify `skills/index.md`, `skills/authentication/login.md`, or `skills/style-guide/writing.md`.

- [ ] **Step 1: Create the adapter skill directory and file**

```bash
mkdir -p "/Users/caglarbaranbora/vault/Apple Agent Kit/skills/apple-agent-kit"
```

Create `/Users/caglarbaranbora/vault/Apple Agent Kit/skills/apple-agent-kit/SKILL.md`:

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

Note the file starts directly with the `---` frontmatter block — no leading `# Title` heading, matching Claude Code's native `SKILL.md` convention (unlike this repo's other artifact types, which use a leading `# Title` line and a fenced `## Metadata` yaml block instead — the adapter skill is deliberately in the different, native format so Claude Code recognizes it).

- [ ] **Step 2: Commit**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git add skills/apple-agent-kit/SKILL.md
git commit -m "feat: add native adapter skill delegating to AGENTS.md routing"
```

---

### Task 4: Validate the plugin structurally

**Files:** none created or modified — this task only runs validation against Tasks 1–3's output.

- [ ] **Step 1: Run the Claude Code plugin validator**

Run:
```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && claude plugin validate .
```
Expected: output contains `Validation passed` (optionally `Validation passed with warnings` — if warnings appear, read them; do not proceed to Task 5 with unexplained warnings, but a warning about the repo having many non-plugin files, e.g. `docs/`, `rfcs/`, at the plugin root is expected and not a blocker, since Claude Code only reads the specific directories it recognizes — `skills/`, `agents/`, `hooks/`, `.claude-plugin/`, etc. — and ignores the rest).

If validation fails, fix the reported issue in `plugin.json`, `marketplace.json`, or `skills/apple-agent-kit/SKILL.md` before continuing — do not skip ahead.

- [ ] **Step 2: No commit needed**

This is a read-only verification step.

---

### Task 5: npx installer package — manifest

**Files:**
- Create: `npx/package.json`

- [ ] **Step 1: Create the npx package directory and manifest**

```bash
mkdir -p "/Users/caglarbaranbora/vault/Apple Agent Kit/npx/bin"
```

Create `/Users/caglarbaranbora/vault/Apple Agent Kit/npx/package.json`:

```json
{
  "name": "apple-agent-kit",
  "version": "0.1.0",
  "description": "Installs the Apple Agent Kit Claude Code plugin via the claude CLI.",
  "bin": {
    "apple-agent-kit": "./bin/install.js"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/caglarbaranbora/Apple-Agent-Kit.git"
  },
  "engines": {
    "node": ">=18"
  }
}
```

No `license` field is set — README.md's License section is currently `TBD`; adding an SPDX identifier here would assert a license that hasn't been decided.

- [ ] **Step 2: Verify it's valid JSON**

Run:
```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && python3 -m json.tool npx/package.json
```
Expected: the same JSON printed back, pretty-formatted, no error.

- [ ] **Step 3: Commit**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git add npx/package.json
git commit -m "feat: add npx installer package manifest"
```

---

### Task 6: npx installer package — install script

**Files:**
- Create: `npx/bin/install.js`

- [ ] **Step 1: Write the installer script**

Create `/Users/caglarbaranbora/vault/Apple Agent Kit/npx/bin/install.js`:

```javascript
#!/usr/bin/env node
'use strict';

const { spawnSync } = require('child_process');

const REPO = 'caglarbaranbora/Apple-Agent-Kit';
const MARKETPLACE_NAME = 'apple-agent-kit-marketplace';
const PLUGIN_NAME = 'apple-agent-kit';

const dryRun = process.argv.includes('--dry-run');

const commands = [
  ['claude', ['plugin', 'marketplace', 'add', REPO]],
  ['claude', ['plugin', 'install', `${PLUGIN_NAME}@${MARKETPLACE_NAME}`]],
];

function checkClaudeInstalled() {
  const result = spawnSync('claude', ['--version'], { stdio: 'ignore' });
  if (result.error || result.status !== 0) {
    console.error(
      'Error: the `claude` CLI was not found on PATH. Install Claude Code first: https://code.claude.com/docs/en/quickstart'
    );
    process.exit(1);
  }
}

function run() {
  checkClaudeInstalled();

  for (const [cmd, args] of commands) {
    const printable = [cmd, ...args].join(' ');
    if (dryRun) {
      console.log(`[dry-run] ${printable}`);
      continue;
    }
    console.log(`Running: ${printable}`);
    const result = spawnSync(cmd, args, { stdio: 'inherit' });
    if (result.status !== 0) {
      console.error(`Failed: ${printable}`);
      process.exit(result.status || 1);
    }
  }

  if (!dryRun) {
    console.log('Apple Agent Kit plugin installed.');
  }
}

run();
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x "/Users/caglarbaranbora/vault/Apple Agent Kit/npx/bin/install.js"
```

- [ ] **Step 3: Syntax-check the script**

Run:
```bash
node --check "/Users/caglarbaranbora/vault/Apple Agent Kit/npx/bin/install.js"
```
Expected: no output, exit code 0 (Node's `--check` prints nothing on success).

- [ ] **Step 4: Commit**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git add npx/bin/install.js
git commit -m "feat: add npx installer script (dry-run and claude-missing safe)"
```

---

### Task 7: Test the installer script's two behaviors

**Files:** none created or modified — this task only exercises Task 6's script.

- [ ] **Step 1: Test dry-run mode with `claude` present**

Run:
```bash
node "/Users/caglarbaranbora/vault/Apple Agent Kit/npx/bin/install.js" --dry-run
```
Expected output (exact commands, order matters):
```
[dry-run] claude plugin marketplace add caglarbaranbora/Apple-Agent-Kit
[dry-run] claude plugin install apple-agent-kit@apple-agent-kit-marketplace
```
Expected exit code: `0`. Verify with `echo $?` immediately after.

This step does NOT modify the user's actual Claude Code configuration — `--dry-run` only prints the commands, it never calls `spawnSync` on the real `claude plugin marketplace add` / `claude plugin install` commands.

- [ ] **Step 2: Test the missing-`claude`-CLI error path**

Run:
```bash
PATH="/usr/bin:/bin" node "/Users/caglarbaranbora/vault/Apple Agent Kit/npx/bin/install.js" --dry-run
```
Expected: stderr contains `Error: the \`claude\` CLI was not found on PATH.` and the process exits with a non-zero status. Verify with `echo $?` immediately after (expect `1`).

This stripped `PATH` deliberately excludes the directory containing the `claude` binary, simulating a machine without Claude Code installed, without changing the real shell's `PATH`.

- [ ] **Step 3: No commit needed**

This is a read-only verification task; nothing changed on disk.

---

### Task 8: Final validation sweep

**Files:** none created or modified — this task re-verifies everything from Tasks 1–7 together.

- [ ] **Step 1: Re-run the plugin validator**

Run:
```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && claude plugin validate .
```
Expected: `Validation passed` (or `Validation passed with warnings` with only the expected non-plugin-directory warnings noted in Task 4).

- [ ] **Step 2: Re-run both JSON syntax checks**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && echo "plugin.json OK"
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo "marketplace.json OK"
python3 -m json.tool npx/package.json > /dev/null && echo "npx/package.json OK"
```
Expected: three `OK` lines, no errors.

- [ ] **Step 3: Confirm existing artifacts are untouched**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git diff --stat main -- knowledge/ references/ skills/authentication skills/style-guide skills/index.md docs/architecture.md AGENTS.md
```
Expected: empty output (no changes to any pre-existing knowledge/skill/reference/architecture file on this branch relative to `main`).

- [ ] **Step 4: Confirm `scripts/validate_artifact.py` still passes on the existing artifact set**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
for f in knowledge/style-guide/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge || echo "FAIL: $f"; done
python3 scripts/validate_artifact.py skills/style-guide/writing.md --type skill
```
Expected: every line is `PASS: ...`; no `FAIL` lines printed (the new `skills/apple-agent-kit/SKILL.md` is intentionally NOT run through this validator — it's a different artifact type, Claude Code's native format, not this repo's custom Skill spec).

- [ ] **Step 5: Final status check and no-op commit skip**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && git status --short
```
Expected: clean (nothing to commit — everything from Tasks 1–7 was already committed at the end of its own task).

---

### Task 9: Manual interactive verification (human-run, not subagent-run)

**Files:** none created or modified.

The remaining two checks from the spec's Testing/Validation Plan
(adapter skill loads correctly; a narrow task loads only the expected
Knowledge Contract) require an interactive Claude Code session and
real judgment about the response — they cannot be scripted as a
pass/fail shell command, so they are NOT executed by the implementer
subagent. After Tasks 1–8 are complete and committed, the user (or a
human reviewer) runs this manually:

- [ ] **Step 1: Confirm the adapter skill loads**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit" && claude --plugin-dir .
```
Then, in the interactive session, run `/help` and check the **Custom
commands** / skills listing for `apple-agent-kit:apple-agent-kit`
(or ask "what skills do you have available?"). Expected: the adapter
skill is listed.

- [ ] **Step 2: Confirm narrow-task routing still works through the plugin**

In the same session, ask a narrow question, e.g.:
```
What's the correct label for the affirmative dialog button, "OK" or "Okay"?
```
Expected: Claude follows AGENTS.md's routing (per the adapter skill),
resolves through `skills/style-guide/writing.md`, and loads only
`knowledge/style-guide/general-button-labels.md` (not the other 24
style-guide Knowledge Contracts) to answer "OK" per that file's Rule 3.
If Claude's response or its stated reasoning shows it loaded unrelated
contracts, or answered from general knowledge instead of the routed
contract, routing is broken — stop and investigate before considering
this plan done.

- [ ] **Step 3: Exit the test session**

```
/exit
```

No commit for this task — it's verification only.

---

## Explicitly not part of this plan

Per the spec's decision 4 and decision 5, none of the following are tasks here, and no task above performs them:
- `npm publish` for the `npx/` package
- `git push` to make the marketplace publicly addable
- Submitting to Anthropic's community marketplace review
- Any Codex-specific packaging artifact

These require the user's separate, explicit go-ahead when reached.
