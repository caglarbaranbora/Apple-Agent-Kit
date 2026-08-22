# Codex Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Apple Agent Kit's Skills loadable from OpenAI's Codex CLI, exactly as approved in `rfcs/0002-codex-support.md`, with zero changes to Knowledge/Skill/Reference/Workflow content.

**Architecture:** Codex's native skill discovery reads the same `SKILL.md` files Claude Code uses, via one repo-root manifest (`.codex-plugin/plugin.json`) whose `skills` field points at the existing `skills/` directory — no per-domain translation. `npx/bin/install.js` gains a Codex-detection fallback that prints instructions rather than attempting to drive Codex's interactive marketplace command itself.

**Tech Stack:** Node.js (`npx/bin/install.js`, no dependencies), plain JSON/Markdown for the rest. No new test framework — CI's existing `npm pack --dry-run` + `test -f bin/install.js` checks are unaffected; this plan's own verification steps are manual shell commands using PATH-stubbed fake `claude`/`codex` executables.

Branch: `feature/codex-support` (already checked out; RFC committed as `79817cc`).

---

### Task 1: `.codex-plugin/plugin.json`

**Files:**
- Create: `.codex-plugin/plugin.json`

- [ ] **Step 1: Write the manifest**

```json
{
  "name": "apple-agent-kit",
  "version": "2.2.0",
  "description": "Spec-first knowledge system for AI coding agents developing Apple platform applications.",
  "author": {
    "name": "caglarbaranbora"
  },
  "homepage": "https://github.com/caglarbaranbora/Apple-Agent-Kit#readme",
  "repository": "https://github.com/caglarbaranbora/Apple-Agent-Kit",
  "license": "PolyForm-Strict-1.0.0",
  "keywords": [
    "apple",
    "swift",
    "swiftui",
    "ios",
    "ai-agent"
  ],
  "skills": "./skills/"
}
```

`description`, `author`, `homepage`, `repository`, `license` are copied from
`.claude-plugin/plugin.json`. `keywords` is `npx/package.json`'s list with the two
Claude-Code-specific entries (`claude-code`, `claude-code-plugin`) dropped, since this
manifest is Codex's. `version` matches the repo's current release version (2.2.0) —
this file joins the release-version consistency check in Task 5, so it must already be
correct here, not a placeholder.

- [ ] **Step 2: Verify it's valid JSON and the `skills` path resolves**

Run:
```bash
python3 -m json.tool .codex-plugin/plugin.json > /dev/null && echo "valid JSON"
test -d "$(python3 -c "import json; print(json.load(open('.codex-plugin/plugin.json'))['skills'])" | sed 's|^\./||')" && echo "skills dir resolves"
```
Expected: both `valid JSON` and `skills dir resolves` printed, no errors.

- [ ] **Step 3: Commit**

```bash
git add .codex-plugin/plugin.json
git commit -m "feat: add Codex plugin manifest, points at existing skills/"
```

---

### Task 2: `.codex/INSTALL.md`

**Files:**
- Create: `.codex/INSTALL.md`

- [ ] **Step 1: Write the install doc**

```markdown
# Installing Apple Agent Kit for Codex

Enable Apple Agent Kit's Skills in Codex via native skill discovery, or via Codex's
plugin marketplace. Both paths load the same `skills/` directory Claude Code uses —
there is no separate Codex build of this content.

## Option A: Plugin marketplace

Inside a Codex CLI session:

```
/plugin marketplace add caglarbaranbora/Apple-Agent-Kit
```

Then install the `apple-agent-kit` plugin from that marketplace and restart Codex.

## Option B: Manual clone + symlink

### Prerequisites

- Git

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/caglarbaranbora/Apple-Agent-Kit.git ~/.codex/apple-agent-kit
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/apple-agent-kit/skills ~/.agents/skills/apple-agent-kit
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\apple-agent-kit" "$env:USERPROFILE\.codex\apple-agent-kit\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

### Verify

```bash
ls -la ~/.agents/skills/apple-agent-kit
```

You should see a symlink (or junction on Windows) pointing at this repo's `skills/`
directory.

### Updating

```bash
cd ~/.codex/apple-agent-kit && git pull
```

Skills update instantly through the symlink.

### Uninstalling

```bash
rm ~/.agents/skills/apple-agent-kit
```

Optionally delete the clone: `rm -rf ~/.codex/apple-agent-kit`.
```

- [ ] **Step 2: Verify the doc's paths are internally consistent**

Run:
```bash
grep -c "apple-agent-kit" .codex/INSTALL.md
```
Expected: a count greater than 5 (repo name/clone path/symlink name appear repeatedly) — a quick sanity check that no leftover `superpowers` naming from the source pattern this was adapted from slipped through.

```bash
grep -i "superpowers" .codex/INSTALL.md
```
Expected: no output. If any line matches, fix it before continuing.

- [ ] **Step 3: Commit**

```bash
git add .codex/INSTALL.md
git commit -m "docs: add Codex install instructions"
```

---

### Task 3: Fix the stale `openai.yaml` claim in `skill-spec.md`

**Files:**
- Modify: `docs/specifications/skill-spec.md:34-35`

- [ ] **Step 1: Replace the two stale lines**

Current text (lines 34-35):
```
Future Codex-specific behavior, if added, lives at `skills/<domain>/agents/openai.yaml`.
No such file exists yet; this is a reserved convention, not a requirement.
```

Replace with:
```
Codex CLI loads these same `SKILL.md` files directly — `.codex-plugin/plugin.json`'s
`skills` field points at this repo's `skills/` directory as a whole, not per domain.
No per-Skill Codex file exists or is needed; see `.codex/INSTALL.md` for how a Codex
user installs this repo.
```

- [ ] **Step 2: Confirm no other file still references the old `openai.yaml` convention**

Run:
```bash
grep -rn "agents/openai.yaml" --include="*.md" .
```
Expected: no output (the line just edited was the only occurrence).

- [ ] **Step 3: Re-run Level 1 validation on the edited file**

Run:
```bash
python3 scripts/validate_artifact.py docs/specifications/skill-spec.md --type reference 2>&1 || true
```
This file isn't one of the four validated artifact types, so the command is expected to
either report "not applicable" or be skipped — the real check is that the edit didn't
break Markdown structure, confirmed visually in Step 1's diff. Skip to the full-repo
sweep in Task 6 for the binding validation.

- [ ] **Step 4: Commit**

```bash
git add docs/specifications/skill-spec.md
git commit -m "fix: correct stale Codex-support claim in skill-spec.md"
```

---

### Task 4: `npx/bin/install.js` gains a Codex fallback

**Files:**
- Modify: `npx/bin/install.js` (full file — small enough to replace wholesale)

- [ ] **Step 1: Replace the file's contents**

Current content (for reference — this is what you're replacing):
```js
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

New content (replace the whole file with this):
```js
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

function commandExists(cmd) {
  const result = spawnSync(cmd, ['--version'], { stdio: 'ignore' });
  return !result.error && result.status === 0;
}

function printCodexInstructions() {
  console.log('The `claude` CLI was not found on PATH, but `codex` was.');
  console.log('Apple Agent Kit installs into Codex from inside a Codex session, not from this script.');
  console.log('');
  console.log('Run inside Codex:');
  console.log(`  /plugin marketplace add ${REPO}`);
  console.log('');
  console.log('Then install the `apple-agent-kit` plugin from that marketplace and restart Codex.');
  console.log('For a manual install instead, see .codex/INSTALL.md in this repository.');
}

function printNeitherFoundError() {
  console.error('Error: neither the `claude` nor the `codex` CLI was found on PATH.');
  console.error('Install Claude Code: https://code.claude.com/docs/en/quickstart');
  console.error('...or install Codex CLI, then re-run this command.');
}

function run() {
  if (!commandExists('claude')) {
    if (commandExists('codex')) {
      printCodexInstructions();
      process.exit(0);
    }
    printNeitherFoundError();
    process.exit(1);
  }

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

The behavioral change: `checkClaudeInstalled()` (which used to check-and-exit in one
step) is replaced by `commandExists(cmd)`, a pure boolean check reused for both `claude`
and `codex`. `run()` now branches three ways instead of two. Nothing in the `commands`
array or the main install loop changes — Claude Code's install path is byte-for-byte
the same as before when `claude` is present.

- [ ] **Step 2: Set up three stub-PATH test scenarios**

Create a scratch directory with three fake executables to test each branch without
needing real `claude` or `codex` installs:

```bash
mkdir -p /tmp/aak-install-test/claude-only /tmp/aak-install-test/codex-only /tmp/aak-install-test/neither

cat > /tmp/aak-install-test/claude-only/claude <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x /tmp/aak-install-test/claude-only/claude

cat > /tmp/aak-install-test/codex-only/codex <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x /tmp/aak-install-test/codex-only/codex
```

(The `neither` directory stays empty on purpose.)

- [ ] **Step 3: Run scenario A — `claude` present**

```bash
PATH="/tmp/aak-install-test/claude-only" node npx/bin/install.js --dry-run
echo "exit code: $?"
```
Expected output:
```
[dry-run] claude plugin marketplace add caglarbaranbora/Apple-Agent-Kit
[dry-run] claude plugin install apple-agent-kit@apple-agent-kit-marketplace
exit code: 0
```
This confirms the pre-existing Claude Code path is unchanged.

- [ ] **Step 4: Run scenario B — `claude` absent, `codex` present**

```bash
PATH="/tmp/aak-install-test/codex-only" node npx/bin/install.js
echo "exit code: $?"
```
Expected output (exact text, from `printCodexInstructions()`):
```
The `claude` CLI was not found on PATH, but `codex` was.
Apple Agent Kit installs into Codex from inside a Codex session, not from this script.

Run inside Codex:
  /plugin marketplace add caglarbaranbora/Apple-Agent-Kit

Then install the `apple-agent-kit` plugin from that marketplace and restart Codex.
For a manual install instead, see .codex/INSTALL.md in this repository.
exit code: 0
```

- [ ] **Step 5: Run scenario C — neither present**

```bash
PATH="/tmp/aak-install-test/neither" node npx/bin/install.js
echo "exit code: $?"
```
Expected output:
```
Error: neither the `claude` nor the `codex` CLI was found on PATH.
Install Claude Code: https://code.claude.com/docs/en/quickstart
...or install Codex CLI, then re-run this command.
exit code: 1
```

- [ ] **Step 6: Clean up the scratch directory**

```bash
rm -rf /tmp/aak-install-test
```

- [ ] **Step 7: Commit**

```bash
git add npx/bin/install.js
git commit -m "feat: print Codex install instructions when claude CLI is absent"
```

---

### Task 5: `.codex-plugin/plugin.json` joins the release-version consistency check, and CLAUDE.md's Codex section is corrected

**Amended after Task 3's implementer flagged, via `grep -rn "agents/openai.yaml"`, that
`CLAUDE.md:89-94` still carried the exact stale claim Task 3 had just fixed in
`skill-spec.md` — CLAUDE.md's own "Codex support (future)" section. Since this task
already touches CLAUDE.md, fixing that section here (Step 1, below) rather than as a
separate task.**

**Files:**
- Modify: `CLAUDE.md:89-94` (the "Codex support" section)
- Modify: `CLAUDE.md:107-122` (release-version consistency section — line numbers shift
  by however many lines Step 1 adds/removes; find the section by its heading text, not
  by the original numbers, if they no longer match)

- [ ] **Step 1: Rewrite the stale "Codex support (future)" section**

Current text (lines 89-94):
```
## Codex support (future)

Not built yet. When added, Codex-specific behavior for a domain skill goes
at `skills/<domain>/agents/openai.yaml`, matching the per-domain skill
layout already in place — no directory restructuring needed when that work
starts.
```

Replace with:
```
## Codex support

Codex CLI loads this repo's Skills directly via `.codex-plugin/plugin.json` (repo
root), whose `skills` field points at the existing `skills/` directory as a whole — no
per-domain translation file, no directory restructuring. See `.codex/INSTALL.md` for
how a Codex user installs this repo (plugin marketplace or manual clone + symlink).
```

Verify:
```bash
grep -rn "agents/openai.yaml" --include="*.md" . | grep -v "docs/superpowers/\|rfcs/0002-codex-support.md\|\.claude/worktrees/"
```
Expected: no output. (The exclusions are: the plan/spec docs in `docs/superpowers/`,
which are historical records and legitimately keep the old text; `rfcs/0002-codex-support.md`,
which discusses the old convention as the thing being investigated and rejected; and
`.claude/worktrees/`, an unrelated separate checkout outside this branch's tracked
source tree.)

- [ ] **Step 2: Replace the file list and count**

Current text:
```
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
```

Replace with:
```
The project has one release version number, shared by exactly these six files:

- `README.md` (the `Version:` line near the top)
- `npx/README.md` (the `Version:` line near the top)
- `npx/package.json` (`version` field)
- `.claude-plugin/plugin.json` (`version` field)
- `.codex-plugin/plugin.json` (`version` field)
- `CHANGELOG.md` (its newest non-`[Unreleased]` release header, e.g. `## [1.0.0] - YYYY-MM-DD`)

These six MUST always match exactly. Before any commit that bumps the
release version, or as part of any final/holistic review, check all six —
a mismatch between them is a release-blocking defect, not a nitpick.
Per-artifact `version:` fields inside individual Knowledge Contracts,
Skills, and References are a separate, independent versioning scheme
(component-level, starts at `0.1.0`, bumped per-artifact as that artifact
changes) — they are NOT part of this six-file release-version check and
do not need to match the release version.
```

Note: the original text said "four-file release-version check" despite listing five
files above it — a pre-existing inconsistency, corrected to "six-file" here rather than
left wrong at a new number.

- [ ] **Step 3: Verify all six files currently agree**

```bash
echo "README.md:            $(grep '^Version:' README.md)"
echo "npx/README.md:        $(grep '^Version:' npx/README.md)"
echo "npx/package.json:     $(grep '"version"' npx/package.json)"
echo ".claude-plugin:       $(grep '"version"' .claude-plugin/plugin.json)"
echo ".codex-plugin:        $(grep '"version"' .codex-plugin/plugin.json)"
echo "CHANGELOG.md:         $(grep -m1 '^## \[2' CHANGELOG.md)"
```
Expected: all five version-bearing lines show `2.2.0`, and the CHANGELOG line reads
`## [2.2.0] - 2026-08-23`.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add .codex-plugin/plugin.json to release-version check, correct stale Codex section"
```

---

### Task 6: Full-repo verification sweep

**Files:** none (verification only)

- [ ] **Step 1: Confirm no Knowledge/Skill/Reference/Workflow content changed**

```bash
git diff --stat main...feature/codex-support
```
Expected: only these paths appear — `.codex-plugin/plugin.json`, `.codex/INSTALL.md`,
`docs/specifications/skill-spec.md`, `npx/bin/install.js`, `CLAUDE.md`, plus
`rfcs/0002-codex-support.md` and `docs/superpowers/plans/2026-08-23-codex-support.md`
from earlier in this branch. No path under `knowledge/`, `skills/*/SKILL.md` (only
`skill-spec.md`, which is a specification doc, not a Skill artifact), `references/`, or
`workflows/`.

- [ ] **Step 2: Run the existing validators (must still pass unchanged)**

```bash
python3 scripts/validate_artifact.py . --all
python3 scripts/validate_repo.py .
python3 -m unittest discover tests/ -v
```
Expected: `340/340 artifacts pass Level 1` (or whatever the current total is — the
count should be unchanged from before this branch, since no artifact was added, edited,
or removed), `PASS` with 0 findings, and all tests passing with no new failures.

- [ ] **Step 3: Validate the Claude Code plugin manifest is unaffected**

```bash
claude plugin validate .
```
Expected: `✔ Validation passed` — confirms `.codex-plugin/` living alongside
`.claude-plugin/` doesn't confuse Claude Code's own validator.

- [ ] **Step 4: Final commit if Steps 1-3 required any fixes**

Only if something needed correcting:
```bash
git add -A
git commit -m "fix: address verification sweep findings"
```
If nothing needed fixing, skip this step — there is no empty commit to make.

---

### Task 7: Push and open the PR

**Files:** none

- [ ] **Step 1: Push the branch**

```bash
git push -u origin feature/codex-support
```

- [ ] **Step 2: Open the PR**

```bash
gh pr create --title "Add Codex CLI support" --body "$(cat <<'EOF'
## Summary

Implements RFC 0002 (`rfcs/0002-codex-support.md`): Apple Agent Kit's Skills become loadable from OpenAI's Codex CLI, with zero changes to Knowledge Contracts, Skills, References, or Workflows.

- `.codex-plugin/plugin.json` — Codex plugin manifest, points at the existing `skills/` directory (no per-domain translation files; Codex reads the same `SKILL.md`s Claude Code does).
- `.codex/INSTALL.md` — marketplace-command path and manual clone+symlink fallback.
- `docs/specifications/skill-spec.md` — corrected a stale line that assumed a per-domain `skills/<domain>/agents/openai.yaml` was needed; it isn't.
- `npx/bin/install.js` — when `claude` isn't on PATH but `codex` is, prints Codex install instructions and exits 0 instead of erroring. Never spawns `codex` itself (its plugin install is interactive, run inside a Codex session).
- `CLAUDE.md` — `.codex-plugin/plugin.json` joins the release-version consistency check (five files → six); also fixed a pre-existing "four-file" miscount in the same paragraph.

## Test plan

- [x] `.codex-plugin/plugin.json` is valid JSON, `skills` path resolves
- [x] `npx/bin/install.js` manually exercised against three PATH-stubbed scenarios (claude present / codex-only / neither) — see plan `docs/superpowers/plans/2026-08-23-codex-support.md` Task 4 for exact commands and expected output
- [x] `python3 scripts/validate_artifact.py . --all` — unchanged pass count
- [x] `python3 scripts/validate_repo.py .` — 0 findings
- [x] `python3 -m unittest discover tests/ -v` — all pass
- [x] `claude plugin validate .` — passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Design doc

Full rationale, rejected alternatives, and investigation findings: `rfcs/0002-codex-support.md`.
