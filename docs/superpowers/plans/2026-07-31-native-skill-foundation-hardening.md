# Native Skill Foundation Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `authentication` and `style-guide` from simulated sub-skills (plain markdown, not recognized by Claude Code) into real native `skills/<domain>/SKILL.md` skills with true YAML frontmatter, update the validator/spec schema to require and check the new format, and fix the resulting drift (`login.md` currently fails its own validator).

**Architecture:** Each domain gets one `skills/<domain>/SKILL.md` file with real frontmatter (`---` at byte offset 0, `name` + `description` for Claude Code discovery, plus the existing `id`/`routes`/etc. fields for the validator). The umbrella `skills/apple-agent-kit/SKILL.md` stays as a broad fallback. Knowledge/Reference files are untouched — only `artifact_type: skill` files change format.

**Tech Stack:** Python 3 (`scripts/validate_artifact.py`, stdlib `unittest`/`re`), Markdown + YAML frontmatter, Claude Code plugin conventions.

**Spec:** `docs/superpowers/specs/2026-07-31-foundation-hardening-design.md` (approved).

---

### Task 1: Update the validator schema and its tests

**Files:**
- Modify: `scripts/validate_artifact.py`
- Test: `tests/test_validate_artifact.py`

- [ ] **Step 1: Update `VALID_SKILL` fixture and add new skill tests (write failing tests first)**

In `tests/test_validate_artifact.py`, replace the existing `VALID_SKILL` block and `TestValidateSkill` class with:

```python
VALID_SKILL = """---
name: example
description: Example skill description. Use when the task involves example things. Triggers on example, sample, demo.
id: skill.style-guide.example
title: Example Skill
version: 0.1.0
status: Draft
artifact_type: skill
domain: Style Guide
routes:
  - example
related:
  - knowledge.style-guide.example
last_updated: 2026-07-30
---

# Example Skill

## Purpose

Example purpose.

## Routing

Example routing.

## Stop Conditions

Example stop conditions.
"""

OLD_FORMAT_SKILL = """# Example Skill

## Metadata

```yaml
id: skill.style-guide.example
title: Example Skill
version: 0.1.0
status: Draft
artifact_type: skill
domain: Style Guide
routes:
  - example
related:
  - knowledge.style-guide.example
last_updated: 2026-07-30
```

## Purpose

Example purpose.

## Triggers

Example triggers.

## Routing

Example routing.

## Stop Conditions

Example stop conditions.
"""


class TestValidateSkill(unittest.TestCase):
    def test_valid_skill_has_no_errors(self):
        errors = validate_artifact.validate_text(VALID_SKILL, "skill")
        self.assertEqual(errors, [])

    def test_missing_name_field(self):
        text = VALID_SKILL.replace("name: example\n", "")
        errors = validate_artifact.validate_text(text, "skill")
        self.assertTrue(any("name" in e for e in errors))

    def test_missing_description_field(self):
        text = VALID_SKILL.replace(
            "description: Example skill description. Use when the task involves example things. Triggers on example, sample, demo.\n",
            "",
        )
        errors = validate_artifact.validate_text(text, "skill")
        self.assertTrue(any("description" in e for e in errors))

    def test_old_fenced_metadata_format_is_rejected(self):
        # Real Claude Code skill discovery requires frontmatter at byte
        # offset 0. A fenced ```yaml block under a "## Metadata" heading
        # (the old repo convention) must no longer satisfy a skill artifact,
        # even though it still satisfies knowledge/reference artifacts.
        errors = validate_artifact.validate_text(OLD_FORMAT_SKILL, "skill")
        self.assertIn("missing metadata YAML block", errors)

    def test_triggers_section_not_required(self):
        # VALID_SKILL has no "## Triggers" section and must still pass --
        # trigger content now lives in the frontmatter `description`.
        self.assertNotIn("## Triggers", VALID_SKILL)
        errors = validate_artifact.validate_text(VALID_SKILL, "skill")
        self.assertEqual(errors, [])

    def test_line_cap_is_80(self):
        text = VALID_SKILL + ("\nextra line\n" * 70)
        errors = validate_artifact.validate_text(text, "skill")
        self.assertTrue(any("line cap" in e for e in errors))

    def test_line_cap_not_exceeded_at_79_lines(self):
        line_count = len(VALID_SKILL.splitlines())
        padding = 79 - line_count
        self.assertGreater(padding, 0)
        text = VALID_SKILL + ("\nx\n" * (padding // 2))
        errors = validate_artifact.validate_text(text, "skill")
        self.assertFalse(any("line cap" in e for e in errors))
```

- [ ] **Step 2: Run tests to verify the new ones fail**

Run: `python3 -m unittest tests.test_validate_artifact -v`

Expected: `test_valid_skill_has_no_errors`, `test_missing_name_field`,
`test_missing_description_field`, `test_old_fenced_metadata_format_is_rejected`,
`test_line_cap_is_80` FAIL (validator doesn't know about `name`/`description`
yet, still 60-line cap, still accepts fenced-block-anywhere format).
`test_triggers_section_not_required` and `test_line_cap_not_exceeded_at_79_lines`
may already pass incidentally — that's fine, the point is the others fail.

- [ ] **Step 3: Implement the schema changes**

In `scripts/validate_artifact.py`, replace:

```python
LINE_CAPS = {"knowledge": 150, "skill": 60, "reference": 80}

REQUIRED_SECTIONS = {
    "knowledge": ["## Intent", "## Rules", "## Compliant Example", "## Non-Compliant Example"],
    "skill": ["## Purpose", "## Triggers", "## Routing", "## Stop Conditions"],
}

REQUIRED_METADATA_FIELDS = {
    "knowledge": ["id", "type", "title", "version", "status", "owner", "summary", "domain", "tags", "updated"],
    "skill": ["id", "title", "version", "status", "artifact_type", "domain", "routes", "related", "last_updated"],
}


def extract_metadata_block(text):
    match = re.search(r"```\s*ya?ml\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else ""
```

with:

```python
LINE_CAPS = {"knowledge": 150, "skill": 80, "reference": 80}

REQUIRED_SECTIONS = {
    "knowledge": ["## Intent", "## Rules", "## Compliant Example", "## Non-Compliant Example"],
    "skill": ["## Purpose", "## Routing", "## Stop Conditions"],
}

REQUIRED_METADATA_FIELDS = {
    "knowledge": ["id", "type", "title", "version", "status", "owner", "summary", "domain", "tags", "updated"],
    "skill": ["name", "description", "id", "title", "version", "status", "artifact_type", "domain", "routes", "related", "last_updated"],
}


def extract_metadata_block(text, artifact_type=None):
    if artifact_type == "skill":
        # Real Claude Code skills need frontmatter at byte offset 0 -- a
        # fenced ```yaml block anywhere in the body (the knowledge/reference
        # convention) is not something the skill loader parses.
        match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
        return match.group(1) if match else ""
    match = re.search(r"```\s*ya?ml\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else ""
```

And update `validate_text` to pass `artifact_type` through — replace:

```python
    if artifact_type in REQUIRED_METADATA_FIELDS:
        block = extract_metadata_block(text)
```

with:

```python
    if artifact_type in REQUIRED_METADATA_FIELDS:
        block = extract_metadata_block(text, artifact_type)
```

- [ ] **Step 4: Run tests to verify everything passes**

Run: `python3 -m unittest tests.test_validate_artifact -v`

Expected: all tests PASS, including the pre-existing `TestValidateKnowledge`
and `TestValidateArtifactCLI` classes (knowledge extraction behavior is
unchanged since `extract_metadata_block(text, "knowledge")` falls through to
the same `re.search` branch as before).

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_artifact.py tests/test_validate_artifact.py
git commit -m "feat: require frontmatter for skill artifacts, drop Triggers section

Skill metadata must now be real YAML frontmatter at byte offset 0 (what
Claude Code's skill loader actually parses for name/description), not a
fenced yaml block anywhere in the body. Triggers content moves into the
frontmatter description field. Line cap raised 60->80 to absorb the
frontmatter overhead."
```

---

### Task 2: Migrate the authentication skill to native format

**Files:**
- Create: `skills/authentication/SKILL.md`
- Delete: `skills/authentication/login.md`

- [ ] **Step 1: Rename the file**

```bash
git mv skills/authentication/login.md skills/authentication/SKILL.md
```

- [ ] **Step 2: Replace its content**

Overwrite `skills/authentication/SKILL.md` with:

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
related:
  - skill.style-guide.writing
last_updated: 2026-07-31
---

# Login Skill

## Purpose

Route authentication-related implementation tasks to the minimum
required Knowledge Contracts.

## Routing

Load in order:

1.  ../../knowledge/authentication/authentication.md
2.  ../../knowledge/authentication/sign-in-terminology.md
3.  ../../knowledge/authentication/button-labels.md
4.  ../../knowledge/authentication/accessibility-forms.md

## Do Not Load

Do not load unrelated domains (StoreKit, Widgets, Notifications, etc.)
unless explicitly required.

## Output

Return only the routed Knowledge Contracts. This skill must not contain
implementation guidance.

## Stop Conditions

Stop and report if the requested authentication topic has no matching
Knowledge Contract in knowledge/authentication/ — do not guess or fall
back to general knowledge.
```

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py skills/authentication/SKILL.md --type skill`

Expected: `PASS: skills/authentication/SKILL.md`

- [ ] **Step 4: Commit**

```bash
git add skills/authentication/SKILL.md skills/authentication/login.md
git commit -m "feat: migrate authentication skill to native SKILL.md format"
```

---

### Task 3: Migrate the style-guide skill to native format

**Files:**
- Create: `skills/style-guide/SKILL.md`
- Delete: `skills/style-guide/writing.md`

- [ ] **Step 1: Rename the file**

```bash
git mv skills/style-guide/writing.md skills/style-guide/SKILL.md
```

- [ ] **Step 2: Replace its content**

Overwrite `skills/style-guide/SKILL.md` with:

```markdown
---
name: style-guide
description: Route writing and terminology implementation tasks to the minimum required style-guide Knowledge Contracts — capitalization, punctuation, button labels, inclusive writing, date and number formatting. Use when writing or reviewing app UI text, labels, buttons, errors, or onboarding copy. Triggers on writing, terminology, capitalization, punctuation, button label wording, inclusive writing, date and number formatting, style guide, UI copy.
id: skill.style-guide.writing
title: Style Guide Writing
version: 0.2.0
status: Draft
artifact_type: skill
domain: Style Guide
routes: [knowledge.style-guide.ui-action-verbs, knowledge.style-guide.pointer-and-click-terminology, knowledge.style-guide.touch-gesture-verbs, knowledge.style-guide.general-button-labels, knowledge.style-guide.navigation-controls, knowledge.style-guide.presentation-surfaces, knowledge.style-guide.input-controls, knowledge.style-guide.status-and-progress-indicators, knowledge.style-guide.app-chrome-and-window-terminology, knowledge.style-guide.app-state-and-error-terminology, knowledge.style-guide.connectivity-and-media-terminology, knowledge.style-guide.instructional-voice-and-phrasing, knowledge.style-guide.capitalization-style-rules, knowledge.style-guide.capitalization-of-apple-proper-nouns, knowledge.style-guide.punctuation-and-typography-in-text, knowledge.style-guide.abbreviations-and-acronyms, knowledge.style-guide.units-of-measure, knowledge.style-guide.numeric-terminology-supplement, knowledge.style-guide.international-formatting, knowledge.style-guide.international-style, knowledge.style-guide.writing-inclusively, knowledge.style-guide.technical-notation, knowledge.style-guide.copyright-and-trademarks, knowledge.style-guide.sign-in-and-authentication-terminology, knowledge.style-guide.authentication-credentials-and-biometrics]
related:
  - skill.authentication.login
last_updated: 2026-07-31
---

# Style Guide Writing Skill

## Purpose

Route writing/terminology implementation tasks to the minimum required
style-guide Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/style-guide/.

-   UI interaction verbs, clicks, taps, buttons, navigation -> ui-action-verbs.md, pointer-and-click-terminology.md, touch-gesture-verbs.md, general-button-labels.md, navigation-controls.md
-   UI components: dialogs/sheets, inputs, progress, chrome -> presentation-surfaces.md, input-controls.md, status-and-progress-indicators.md, app-chrome-and-window-terminology.md
-   App state, connectivity, instructional voice -> app-state-and-error-terminology.md, connectivity-and-media-terminology.md, instructional-voice-and-phrasing.md
-   Capitalization, punctuation, abbreviations -> capitalization-style-rules.md, capitalization-of-apple-proper-nouns.md, punctuation-and-typography-in-text.md, abbreviations-and-acronyms.md
-   Units, numeric edge cases, locale formatting -> units-of-measure.md, numeric-terminology-supplement.md, international-formatting.md, international-style.md
-   Inclusive writing -> writing-inclusively.md
-   Code font / placeholder-name conventions -> technical-notation.md
-   Copyright/trademark text -> copyright-and-trademarks.md
-   Sign-in, sign-out, login wording -> sign-in-and-authentication-terminology.md
-   Passkey, password, PIN, biometric wording -> authentication-credentials-and-biometrics.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/style-guide/ — do not guess or fall back to general knowledge.
```

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py skills/style-guide/SKILL.md --type skill`

Expected: `PASS: skills/style-guide/SKILL.md`

- [ ] **Step 4: Commit**

```bash
git add skills/style-guide/SKILL.md skills/style-guide/writing.md
git commit -m "feat: migrate style-guide skill to native SKILL.md format"
```

---

### Task 4: Add explicit `name` to the umbrella skill

**Files:**
- Modify: `skills/apple-agent-kit/SKILL.md`

- [ ] **Step 1: Add the `name` field**

In `skills/apple-agent-kit/SKILL.md`, replace:

```markdown
---
description: Apple platform app development — UI terminology, style guide rules, authentication flows, and other Apple Agent Kit domains. Use for any task involving Apple platform UI text, capitalization, or implementation conventions.
---
```

with:

```markdown
---
name: apple-agent-kit
description: Apple platform app development — UI terminology, style guide rules, authentication flows, and other Apple Agent Kit domains. Use for any task involving Apple platform UI text, capitalization, or implementation conventions.
---
```

- [ ] **Step 2: Validate the plugin manifest**

Run: `claude plugin validate .`

Expected: no errors reported for `skills/apple-agent-kit/SKILL.md`.

- [ ] **Step 3: Commit**

```bash
git add skills/apple-agent-kit/SKILL.md
git commit -m "fix: add explicit name field to umbrella skill frontmatter"
```

---

### Task 5: Update `skills/index.md` paths

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Update the Discovery Rules table**

In `skills/index.md`, replace:

```markdown
| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/login.md |
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/writing.md |
```

with:

```markdown
| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/SKILL.md |
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/SKILL.md |
```

- [ ] **Step 2: Verify no other stale references remain**

Run: `grep -rn "skills/authentication/login.md\|skills/style-guide/writing.md" --include="*.md" AGENTS.md README.md docs/architecture* docs/specifications skills/ knowledge/ workflows/`

Expected: no output (the only remaining hits are in historical
`docs/superpowers/plans/2026-07-30-*.md` and
`docs/superpowers/specs/2026-07-30-*.md` files, which are point-in-time
records and are intentionally left as-is).

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "fix: update skills/index.md paths to new native SKILL.md locations"
```

---

### Task 6: Update the skill specification document

**Files:**
- Modify: `docs/specifications/skill-spec.md`

- [ ] **Step 1: Rewrite the spec**

Replace the full contents of `docs/specifications/skill-spec.md` with:

```markdown
# Skill Specification

Status: Draft
Version: 0.2.0

## Purpose

Defines the normative specification for every Skill in Apple Agent Kit.

## Goals

- Deterministic routing
- Zero domain knowledge
- Minimal token consumption
- Reusable orchestration layer

## Frontmatter Format

Every Skill file is named `SKILL.md` and lives at `skills/<domain>/SKILL.md`
(or `skills/<domain>/<sub-skill>/SKILL.md` if a domain ever needs more than
one skill). Metadata is real YAML frontmatter — `---` at byte offset 0 of
the file, before any other content — not a fenced code block under a
heading. This is what the Claude Code skill loader parses for `name` and
`description`; both are required (see Required Metadata) so the skill is
independently discoverable and explicitly invocable as `/<domain>`.

Future Codex-specific behavior (if added) lives at
`skills/<domain>/agents/openai.yaml`, matching this same per-domain layout.
No such file exists yet — this is a reserved convention, not a current
requirement.

## Required Metadata

- name
- description
- id
- title
- version
- status
- artifact_type: skill
- domain
- routes
- related
- last_updated

## Required Sections

1. Purpose
2. Routing
3. Stop Conditions

An optional `Review Output Format` section (severity table + verdict) may
be added by any Skill whose task includes auditing existing text or code
against the domain's rules, not just routing implementation guidance. It is
not required for Skills that only route implementation Knowledge Contracts.

## Rules

- A Skill MUST NOT contain implementation guidance.
- A Skill MUST NOT duplicate Knowledge Contracts.
- A Skill routes Knowledge Contracts only.
- A Skill should load the minimum required artifacts.
- A Skill should resolve exactly one primary task.

## Size Limit

A Skill MUST NOT exceed 80 lines. If routing logic does not fit, split into multiple Skill files — never raise this limit.

## Routing Rules

- Routing must be explicit.
- Routing order must be deterministic.
- All routed artifacts must exist.
- Missing artifacts must stop execution.

## Validation Checklist

- Metadata complete
- No implementation knowledge
- Routing valid
- No circular routing
- Minimum artifact set
```

- [ ] **Step 2: Commit**

```bash
git add docs/specifications/skill-spec.md
git commit -m "docs: update skill-spec.md for native frontmatter format"
```

---

### Task 7: Add ownership column to the domain map

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Rewrite the domain map**

Replace the full contents of `docs/architecture/domain-map.md` with:

```markdown
# Domain Map

Status: Draft
Version: 0.3.0

See: ../glossary.md
[[glossary]]

## Purpose

Defines the top-level Apple development domains used to organize References, Knowledge Contracts, Skills, and Workflows, and the Tier (build-order priority, see glossary above) assigned to each.

## Build Order

One domain is fully finished (Reference → Knowledge → Skill → Validation) before the next domain starts. Domains are attempted in Tier order: all of Tier 1, then Tier 2, then Tier 3. Within a tier, order is chosen at build time.

`style-guide` is first.

## Tier 1 — Must-Have

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style | UI copy wording, capitalization rules, punctuation, inclusive writing |
| Human Interface Guidelines | human-interface-guidelines | Visual/UX design patterns, layout, interaction | Layout patterns, interaction conventions, visual design guidance |
| App Store Review Guidelines | app-store-review-guidelines | Review, metadata, distribution rules | App Store submission, metadata, and distribution compliance rules |
| SwiftUI | swiftui | Views, navigation, layout | SwiftUI view/navigation/layout implementation conventions |
| UIKit | uikit | UIKit components | UIKit component implementation conventions |
| AuthenticationServices | authenticationservices | Sign in with Apple API, credential provider | Sign in with Apple API and credential provider implementation |
| StoreKit | storekit | In-App Purchases, subscriptions | In-app purchase and subscription implementation and terminology |
| Accessibility | accessibility | Accessibility APIs and UX | Accessibility API usage and accessible UX requirements |
| SF Symbols | sf-symbols | Iconography | Icon selection and SF Symbols usage rules |
| Xcode | xcode | Build, signing, archives | Build configuration, signing, and archive/export conventions |

## Tier 2

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| App Intents | app-intents | App Intents & Shortcuts | App Intents and Shortcuts implementation and terminology |
| WidgetKit | widgetkit | Widgets | Widget implementation, sizing, and terminology |
| UserNotifications | usernotifications | Push & local notifications | Push and local notification implementation and terminology |
| BackgroundTasks | backgroundtasks | Background execution | Background task scheduling and execution conventions |
| Foundation | foundation | Core Swift/Obj-C data types & utilities | Core Swift/Obj-C data type and utility usage conventions |
| Localization | localization | Language, terminology | Localization and translation workflow conventions |
| Privacy | privacy | Privacy requirements | Privacy manifest and data-use disclosure requirements |
| Sign in with Apple | sign-in-with-apple | Sign in with Apple UX/flow (see Cross-Domain Notes) | Sign in with Apple UX/flow (see Cross-Domain Notes) |

## Tier 3

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| AVFoundation | avfoundation | Audio/video capture & playback | Audio/video capture and playback implementation |
| Vision | vision | Image analysis | Image analysis API usage |
| Core ML | core-ml | On-device ML | On-device ML model integration conventions |
| CloudKit | cloudkit | CloudKit | CloudKit sync and record management conventions |
| Core Data | core-data | Persistence | Core Data persistence conventions |
| HealthKit | healthkit | Health data | Health data access and terminology |
| MapKit | mapkit | Maps | Map display and interaction conventions |
| Photos | photos | Photo library access | Photo library access and permission conventions |
| Core Location | core-location | Location services | Location services access and permission conventions |

## Existing / Unscheduled Domains

Mapped before this Tier list existed. No Tier assigned yet — resolve when reached.

| Domain | Status | Initial Scope | Owns |
|---|---|---|---|
| authentication | Active (Phase 5, in progress) | Sign in, identity, sessions — see Cross-Domain Notes | Sign-in, identity, and session implementation routing (see Cross-Domain Notes) |
| testing | Unscheduled | XCTest, UI testing | XCTest and UI testing conventions |
| networking | Unscheduled | URLSession, ATS | URLSession usage and App Transport Security conventions |
| security | Unscheduled | Keychain, credentials | Keychain and credential storage conventions |

## Cross-Domain Notes

- `authentication`, `authenticationservices`, and `sign-in-with-apple` overlap conceptually (sign-in flows). Boundary not yet resolved — decide when `authenticationservices` or `sign-in-with-apple` is reached, per the rule in ../dependency-graph.md ([[dependency-graph]]) that cross-domain dependencies must be explicit.
- `human-interface-guidelines` and `sf-symbols` were previously merged with `style-guide` under a single `design` domain. Split per ../../rfcs/0001-style-guide-domain-and-domain-roadmap.md ([[0001-style-guide-domain-and-domain-roadmap]]).

## Artifact Layout

references/apple/<domain>/
knowledge/<domain>/
skills/<domain>/
workflows/<domain>/

## Rules

- Every artifact belongs to exactly one primary domain.
- Cross-domain dependencies must be explicit.
- Skills cannot span unrelated domains.
- Knowledge Contracts remain atomic.

## Validation Checklist

- Domain exists
- Artifact mapped
- Cross-domain dependencies declared
- No duplicate ownership
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: add Owns column to domain-map.md ahead of new-domain work"
```

---

### Task 8: Document the Codex convention and fix the stale naming example

**Files:**
- Modify: `CLAUDE.md`
- Modify: `docs/naming-conventions.md`

- [ ] **Step 1: Add a Codex support note to `CLAUDE.md`**

In `CLAUDE.md`, replace:

```markdown
Run this after any change to `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, or `skills/apple-agent-kit/SKILL.md`.

## Commit conventions
```

with:

```markdown
Run this after any change to `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, or `skills/apple-agent-kit/SKILL.md`.

## Codex support (future)

Not built yet. When added, Codex-specific behavior for a domain skill goes
at `skills/<domain>/agents/openai.yaml`, matching the per-domain skill
layout already in place — no directory restructuring needed when that work
starts.

## Commit conventions
```

- [ ] **Step 2: Fix the stale `skills/` example in `docs/naming-conventions.md`**

In `docs/naming-conventions.md`, replace:

```markdown
skills/ - login.md - app-store-review.md
```

with:

```markdown
skills/ - authentication/SKILL.md - style-guide/SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md docs/naming-conventions.md
git commit -m "docs: note future Codex convention, fix stale skills/ naming example"
```

---

### Task 9: Full verification pass

**Files:** none (verification only)

- [ ] **Step 1: Run the full test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`

Expected: all tests PASS.

- [ ] **Step 2: Validate every artifact**

```bash
python3 scripts/validate_artifact.py skills/authentication/SKILL.md --type skill
python3 scripts/validate_artifact.py skills/style-guide/SKILL.md --type skill
python3 scripts/validate_artifact.py knowledge/authentication/authentication.md --type knowledge
```

Expected: `PASS` for all three.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`

Expected: no errors. Confirms `skills/authentication/SKILL.md`,
`skills/style-guide/SKILL.md`, and `skills/apple-agent-kit/SKILL.md` are all
discovered as three independent native skills.

- [ ] **Step 4: Confirm no dangling references remain**

Run: `grep -rln "skills/authentication/login.md\|skills/style-guide/writing.md" AGENTS.md README.md CLAUDE.md docs/architecture* docs/specifications skills/ knowledge/ workflows/ 2>/dev/null`

Expected: no output.

- [ ] **Step 5: Manual invocation check**

In a Claude Code session with this plugin loaded, invoke the authentication
skill explicitly (e.g. `/apple-agent-kit:authentication` or the resolved
name shown by `/help`) and confirm it loads only the four routed
authentication Knowledge Contracts, not the style-guide set.
