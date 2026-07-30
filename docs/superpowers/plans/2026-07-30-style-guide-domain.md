# Style Guide Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `style-guide` domain end-to-end (Reference → Knowledge Contracts → Skill → validation) in Apple Agent Kit, sourced from the Apple Style Guide PDF, per `docs/superpowers/specs/2026-07-30-style-guide-domain-design.md` and `rfcs/0001-style-guide-domain-and-domain-roadmap.md`.

**Architecture:** Markdown knowledge-base repo, no runtime code except a small structural validator. Content is authored by dispatched subagents (never read raw by the main thread), reviewed by the author in per-topic-cluster batches, then committed. Two content sources: 5 thematic back-matter chapters (ingested in full) and a curated, semantically-clustered subset of the 1,706-term A–Z glossary (NOT ingested in full — app-dev-relevant terms only).

**Tech Stack:** Markdown, YAML metadata blocks, Python 3 stdlib (`scripts/validate_artifact.py`), `unittest` (stdlib, no new dependency).

---

## Task 1: Add size caps to the specs

**Files:**
- Modify: `docs/specifications/knowledge-spec.md`
- Modify: `docs/specifications/skill-spec.md`
- Modify: `docs/validation-model.md`

- [ ] **Step 1: Add the Knowledge Contract cap**

In `docs/specifications/knowledge-spec.md`, after the `## Rules` section, add:

```markdown
## Size Limit

A Knowledge Contract MUST NOT exceed 150 lines. If a topic does not fit, split it into another atomic contract — never raise this limit.
```

- [ ] **Step 2: Add the Skill cap**

In `docs/specifications/skill-spec.md`, after the `## Rules` section, add:

```markdown
## Size Limit

A Skill MUST NOT exceed 60 lines. If routing logic does not fit, split into multiple Skill files — never raise this limit.
```

- [ ] **Step 3: Add the Reference cap and cross-reference table**

In `docs/validation-model.md`, inside the `### Level 1 --- Structural` section, after the existing `Checks:` list, add:

```markdown
Size limits:

-   Knowledge Contract: 150 lines (see docs/specifications/knowledge-spec.md)
-   Skill: 60 lines (see docs/specifications/skill-spec.md)
-   Reference: 80 lines (no dedicated spec doc; limit defined here)
```

- [ ] **Step 4: Commit**

```bash
git add docs/specifications/knowledge-spec.md docs/specifications/skill-spec.md docs/validation-model.md
git commit -m "docs: add size caps for knowledge/skill/reference artifacts"
```

---

## Task 2: Build the structural validator (TDD)

**Files:**
- Create: `scripts/validate_artifact.py`
- Test: `tests/test_validate_artifact.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_validate_artifact.py`:

```python
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_artifact  # noqa: E402


VALID_KNOWLEDGE = """# Example

## Metadata

```yaml
id: knowledge.style-guide.example
type: knowledge
title: Example
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: An example contract.
domain: Style Guide
tags:
  - example
updated: 2026-07-30
```

## Intent

Example intent.

## Rules

### Rule 1

Example rule.

## Compliant Example

OK.

## Non-Compliant Example

Not OK.
"""


class TestValidateKnowledge(unittest.TestCase):
    def test_valid_contract_has_no_errors(self):
        errors = validate_artifact.validate_text(VALID_KNOWLEDGE, "knowledge")
        self.assertEqual(errors, [])

    def test_line_cap_exceeded(self):
        text = VALID_KNOWLEDGE + ("\nextra line\n" * 150)
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertTrue(any("line cap" in e for e in errors))

    def test_missing_required_section(self):
        text = VALID_KNOWLEDGE.replace("## Rules", "## Renamed")
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertTrue(any("## Rules" in e for e in errors))

    def test_missing_metadata_field(self):
        text = VALID_KNOWLEDGE.replace("domain: Style Guide\n", "")
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertTrue(any("domain" in e for e in errors))

    def test_space_before_yaml_fence_is_accepted(self):
        # Repo convention (see knowledge/authentication/sign-in-terminology.md
        # and templates/knowledge-contract.md) is "``` yaml" with a space.
        text = VALID_KNOWLEDGE.replace("```yaml", "``` yaml")
        errors = validate_artifact.validate_text(text, "knowledge")
        metadata_errors = [e for e in errors if "metadata" in e]
        self.assertEqual(metadata_errors, [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_validate_artifact.py -v`
Expected: `ModuleNotFoundError: No module named 'validate_artifact'`

- [ ] **Step 3: Write the implementation**

Create `scripts/validate_artifact.py`:

```python
#!/usr/bin/env python3
"""Level 1 (Structural) validation for Apple Agent Kit artifacts."""
import argparse
import re
import sys
from pathlib import Path

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


def validate_text(text, artifact_type):
    errors = []
    cap = LINE_CAPS.get(artifact_type)
    line_count = len(text.splitlines())
    if cap is not None and line_count > cap:
        errors.append(f"exceeds {artifact_type} line cap: {line_count} > {cap}")

    for heading in REQUIRED_SECTIONS.get(artifact_type, []):
        if heading not in text:
            errors.append(f"missing required section: {heading}")

    if artifact_type in REQUIRED_METADATA_FIELDS:
        block = extract_metadata_block(text)
        if not block:
            errors.append("missing metadata YAML block")
        else:
            for field in REQUIRED_METADATA_FIELDS[artifact_type]:
                if not re.search(rf"^{field}:", block, re.MULTILINE):
                    errors.append(f"missing required metadata field: {field}")

    return errors


def validate_file(path, artifact_type):
    return validate_text(Path(path).read_text(), artifact_type)


def main():
    parser = argparse.ArgumentParser(description="Validate an Apple Agent Kit artifact (Level 1 - Structural).")
    parser.add_argument("path", help="Path to the artifact markdown file")
    parser.add_argument("--type", required=True, choices=["knowledge", "skill", "reference"], help="Artifact type")
    args = parser.parse_args()

    errors = validate_file(args.path, args.type)
    if errors:
        print(f"FAIL: {args.path}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"PASS: {args.path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_validate_artifact.py -v`
Expected: `OK` with 5 tests passed

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_artifact.py tests/test_validate_artifact.py
git commit -m "feat: add Level 1 structural validator for artifacts"
```

---

## Task 3: Ingest "Writing Inclusively" chapter

**Files:**
- Create: `knowledge/style-guide/writing-inclusively.md`
- Modify: `references/apple/style-guide.md`

- [ ] **Step 1: Dispatch a subagent to draft the contract**

Use the Agent tool (general-purpose, foreground, so the draft can be reviewed before committing) with this exact prompt:

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf and
read only the "Writing inclusively" chapter (page 223 in the PDF; subsections:
Intro to inclusive writing, General guidelines, Inclusive representation,
Gender identity, Writing about disability).

Draft ONE markdown file for path knowledge/style-guide/writing-inclusively.md
following this exact template (fill in the metadata and rules from the real
chapter content, do not invent rules not present in the source):

# Writing Inclusively

Status: Draft Version: 0.1.0

## Metadata

```yaml
id: knowledge.style-guide.writing-inclusively
type: knowledge
title: Writing Inclusively
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: <one sentence>
domain: Style Guide
tags:
  - style-guide
  - inclusive-writing
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
updated: 2026-07-30
```

## Intent
## Scope
### Included
### Excluded
## Rules
(use ### Rule 1, ### Rule 2, ... subheadings, MUST/SHOULD/MAY language)
## Compliant Example
## Non-Compliant Example
## Dependencies
## References

Hard constraint: the whole file, including metadata, MUST be 150 lines or
fewer. If the real chapter content doesn't fit, keep only the most
implementation-relevant rules (things an AI agent writing app UI text would
actually need) and drop the rest.

Return the complete file content in your final message inside a single
markdown code block. Do not write the file yourself — I will review and save it.
```

- [ ] **Step 2: Save the reviewed draft**

Read the subagent's returned content. If it looks correct (real Apple Style Guide content, not fabricated, follows the template), save it to `knowledge/style-guide/writing-inclusively.md` using the Write tool. If anything looks wrong, ask the subagent to revise before saving.

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/style-guide/writing-inclusively.md --type knowledge`
Expected: `PASS: knowledge/style-guide/writing-inclusively.md`

If FAIL, fix the reported errors directly in the file and re-run until PASS.

- [ ] **Step 4: Add the reference index entry**

In `references/apple/style-guide.md`, under `## Used By` (or a new `## Indexed Knowledge Contracts` section if it doesn't exist yet), add:

```markdown
- knowledge/style-guide/writing-inclusively.md
```

Also add the mirrored wiki link per `docs/architecture/linking-model.md`:

```markdown
- [[knowledge/style-guide/writing-inclusively]]
```

Run: `python3 scripts/validate_artifact.py references/apple/style-guide.md --type reference`
Expected: `PASS: references/apple/style-guide.md`

- [ ] **Step 5: Commit**

```bash
git add knowledge/style-guide/writing-inclusively.md references/apple/style-guide.md
git commit -m "feat(style-guide): add writing-inclusively knowledge contract"
```

---

## Task 4: Ingest "Units of Measure" chapter

**Files:**
- Create: `knowledge/style-guide/units-of-measure.md`
- Modify: `references/apple/style-guide.md`

- [ ] **Step 1: Dispatch a subagent to draft the contract**

Same procedure as Task 3, Step 1, with this prompt (chapter and page substituted):

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf and
read only the "Units of measure" chapter (page 230 in the PDF; subsections:
Intro to units of measure, Prefixes for units of measure, Names and unit
symbols for units of measure).

Draft ONE markdown file for path knowledge/style-guide/units-of-measure.md
following this exact template (fill in the metadata and rules from the real
chapter content, do not invent rules not present in the source):

# Units of Measure

Status: Draft Version: 0.1.0

## Metadata

```yaml
id: knowledge.style-guide.units-of-measure
type: knowledge
title: Units of Measure
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: <one sentence>
domain: Style Guide
tags:
  - style-guide
  - units-of-measure
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
updated: 2026-07-30
```

## Intent
## Scope
### Included
### Excluded
## Rules
(use ### Rule 1, ### Rule 2, ... subheadings, MUST/SHOULD/MAY language)
## Compliant Example
## Non-Compliant Example
## Dependencies
## References

Hard constraint: the whole file, including metadata, MUST be 150 lines or
fewer. If the real chapter content doesn't fit, keep only the most
implementation-relevant rules (things an AI agent writing app UI text would
actually need) and drop the rest.

Return the complete file content in your final message inside a single
markdown code block. Do not write the file yourself — I will review and save it.
```

- [ ] **Step 2: Save the reviewed draft** — same as Task 3 Step 2, target `knowledge/style-guide/units-of-measure.md`.

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/style-guide/units-of-measure.md --type knowledge`
Expected: `PASS`

- [ ] **Step 4: Add reference index entry** (same mechanism as Task 3 Step 4) for `knowledge/style-guide/units-of-measure.md`.

- [ ] **Step 5: Commit**

```bash
git add knowledge/style-guide/units-of-measure.md references/apple/style-guide.md
git commit -m "feat(style-guide): add units-of-measure knowledge contract"
```

---

## Task 5: Ingest "Technical Notation" chapter

**Files:**
- Create: `knowledge/style-guide/technical-notation.md`
- Modify: `references/apple/style-guide.md`

- [ ] **Step 1: Dispatch a subagent to draft the contract**

Same procedure as Task 3, Step 1, with this prompt:

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf and
read only the "Technical notation" chapter (page 237 in the PDF; subsections:
Intro to technical notation, Code, Syntax descriptions, Code font in text,
Placeholder names in text).

Draft ONE markdown file for path knowledge/style-guide/technical-notation.md
following this exact template (fill in the metadata and rules from the real
chapter content, do not invent rules not present in the source):

# Technical Notation

Status: Draft Version: 0.1.0

## Metadata

```yaml
id: knowledge.style-guide.technical-notation
type: knowledge
title: Technical Notation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: <one sentence>
domain: Style Guide
tags:
  - style-guide
  - technical-notation
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
updated: 2026-07-30
```

## Intent
## Scope
### Included
### Excluded
## Rules
(use ### Rule 1, ### Rule 2, ... subheadings, MUST/SHOULD/MAY language)
## Compliant Example
## Non-Compliant Example
## Dependencies
## References

Hard constraint: the whole file, including metadata, MUST be 150 lines or
fewer. If the real chapter content doesn't fit, keep only the most
implementation-relevant rules (things an AI agent writing app UI text or code
comments would actually need) and drop the rest.

Return the complete file content in your final message inside a single
markdown code block. Do not write the file yourself — I will review and save it.
```

- [ ] **Step 2: Save the reviewed draft** — target `knowledge/style-guide/technical-notation.md`.

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/style-guide/technical-notation.md --type knowledge`
Expected: `PASS`

- [ ] **Step 4: Add reference index entry** for `knowledge/style-guide/technical-notation.md`.

- [ ] **Step 5: Commit**

```bash
git add knowledge/style-guide/technical-notation.md references/apple/style-guide.md
git commit -m "feat(style-guide): add technical-notation knowledge contract"
```

---

## Task 6: Ingest "International Style" chapter

**Files:**
- Create: `knowledge/style-guide/international-style.md`
- Create (only if the 150-line cap forces a split): `knowledge/style-guide/international-formatting.md`
- Modify: `references/apple/style-guide.md`

- [ ] **Step 1: Dispatch a subagent to draft the contract**

Same procedure as Task 3, Step 1, with this prompt:

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf and
read only the "International style" chapter (page 239 in the PDF; subsections:
Intro to international style, Countries, Currency, Dates and times, Decimals,
Languages, Telephone numbers, Units of measure).

Draft markdown file(s) at knowledge/style-guide/international-style.md
following the same template used in prior tasks (Metadata / Intent / Scope /
Rules / Compliant Example / Non-Compliant Example / Dependencies /
References), id: knowledge.style-guide.international-style, domain: Style
Guide, tags: [style-guide, international].

Hard constraint: each file MUST be 150 lines or fewer. This chapter has 7
subsections and may not fit in one file — if it doesn't, split it into TWO
files: knowledge/style-guide/international-style.md (Countries, Currency,
Languages, Telephone numbers) and knowledge/style-guide/international-formatting.md
(id: knowledge.style-guide.international-formatting, Dates and times,
Decimals, Units of measure — these are formatting-of-numbers concerns,
distinct from naming/language concerns). Only split if needed to stay under
150 lines each; keep the most implementation-relevant rules (things an AI
agent formatting dates/currency/numbers in app UI would actually need) if
content must be dropped.

Return the complete content of each file in your final message, each in its
own labeled markdown code block. Do not write files yourself — I will review
and save them.
```

- [ ] **Step 2: Save the reviewed draft(s)** — one or two files depending on the subagent's split decision.

- [ ] **Step 3: Validate**

Run for each file produced:
`python3 scripts/validate_artifact.py knowledge/style-guide/international-style.md --type knowledge`
`python3 scripts/validate_artifact.py knowledge/style-guide/international-formatting.md --type knowledge` (only if it was created)
Expected: `PASS` for each.

- [ ] **Step 4: Add reference index entries** for each file produced.

- [ ] **Step 5: Commit**

```bash
git add knowledge/style-guide/international-style.md references/apple/style-guide.md
# if the split file was created:
git add knowledge/style-guide/international-formatting.md
git commit -m "feat(style-guide): add international-style knowledge contract(s)"
```

---

## Task 7: Ingest "Copyright and Trademarks" chapter

**Files:**
- Create: `knowledge/style-guide/copyright-and-trademarks.md`
- Modify: `references/apple/style-guide.md`

- [ ] **Step 1: Dispatch a subagent to draft the contract**

Same procedure as Task 3, Step 1, with this prompt:

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf and
read only the "Copyright and trademarks" section (page 244, no subsections).

Draft ONE markdown file for path knowledge/style-guide/copyright-and-trademarks.md
following the same template used in prior tasks (Metadata / Intent / Scope /
Rules / Compliant Example / Non-Compliant Example / Dependencies /
References), id: knowledge.style-guide.copyright-and-trademarks, domain:
Style Guide, tags: [style-guide, copyright, trademarks].

Hard constraint: 150 lines or fewer (this section is short, should easily fit).

Return the complete file content in your final message inside a single
markdown code block. Do not write the file yourself — I will review and save it.
```

- [ ] **Step 2: Save the reviewed draft** — target `knowledge/style-guide/copyright-and-trademarks.md`.

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/style-guide/copyright-and-trademarks.md --type knowledge`
Expected: `PASS`

- [ ] **Step 4: Add reference index entry** for `knowledge/style-guide/copyright-and-trademarks.md`.

- [ ] **Step 5: Commit**

```bash
git add knowledge/style-guide/copyright-and-trademarks.md references/apple/style-guide.md
git commit -m "feat(style-guide): add copyright-and-trademarks knowledge contract"
```

---

## Task 8: Produce the glossary curation proposal

**Files:**
- Create: `docs/superpowers/specs/2026-07-30-style-guide-glossary-curation-proposal.md`

- [ ] **Step 1: Dispatch a subagent to scan the glossary and propose clusters**

Use the Agent tool (general-purpose, foreground) with this exact prompt:

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf.
It contains a 1,706-term alphabetical A-Z glossary (pages 11-222) of Apple's
editorial terminology rules.

Do NOT ingest all 1,706 terms. This project is a knowledge base for an AI
coding agent that writes iOS app UI text (labels, buttons, error messages,
onboarding copy, in-app strings) — not a general editorial reference.

Scan the glossary and select ONLY terms relevant to that job: product-name
capitalization rules, UI terminology (e.g. terms like "tap" vs "click",
"Sign In" vs "Log In"), abbreviation rules, number/unit formatting rules that
appear as individual glossary entries (distinct from the already-ingested
"International style" and "Units of measure" chapters), and explicit
avoid-lists (Apple says use X, not Y).

Group the selected terms into semantic clusters (NOT alphabetical) — e.g.
"capitalization-of-product-names", "ui-action-verbs", "abbreviations",
"numbers-in-text". Aim for roughly 150-300 total terms across roughly 15-25
clusters, each small enough that one cluster's rules will fit in a single
150-line knowledge contract later.

Write a report with this exact structure and return it as your final
message (do not write any file):

## Proposed Clusters

### <cluster-slug-in-kebab-case>
Terms: <comma-separated list of the actual glossary terms in this cluster>
Rationale: <one sentence: why these terms belong together and why they matter for app-dev UI text>

(repeat for each cluster)

## Excluded

One sentence on what categories of the 1,706 terms were excluded and why
(e.g. retail/store terminology, legal boilerplate, hardware/product-line
naming trivia not relevant to in-app text).
```

- [ ] **Step 2: Save the proposal**

Save the subagent's returned report to `docs/superpowers/specs/2026-07-30-style-guide-glossary-curation-proposal.md`, prefixed with:

```markdown
# Style Guide Glossary Curation Proposal

Status: Draft
Version: 0.1.0

Source: https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf (A-Z glossary, 1,706 terms)
Purpose: propose which terms to ingest into knowledge/style-guide/ and how to cluster them, per rfcs/0001-style-guide-domain-and-domain-roadmap.md decision 9.

---
```

followed by the subagent's report verbatim.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-30-style-guide-glossary-curation-proposal.md
git commit -m "docs(style-guide): add glossary curation proposal for review"
```

---

## Task 9: Review checkpoint — approve the glossary clusters

**Files:** none (human review step)

- [ ] **Step 1: Present the proposal to the user**

Show the cluster list from `docs/superpowers/specs/2026-07-30-style-guide-glossary-curation-proposal.md`. Ask the user to approve, remove, merge, or rename clusters. Do not proceed to Task 10 until the user has explicitly approved a final cluster list.

- [ ] **Step 2: Record the approved list**

If the user requested changes, edit `docs/superpowers/specs/2026-07-30-style-guide-glossary-curation-proposal.md` to reflect the approved final state (mark `Status: Approved`), then commit:

```bash
git add docs/superpowers/specs/2026-07-30-style-guide-glossary-curation-proposal.md
git commit -m "docs(style-guide): mark glossary curation proposal approved"
```

---

## Task 10: Draft one knowledge contract per approved glossary cluster

**Files:**
- Create: `knowledge/style-guide/<cluster-slug>.md` — one per approved cluster from Task 9
- Modify: `references/apple/style-guide.md`

This task repeats once per approved cluster. Do not skip clusters; do not merge clusters beyond what was approved in Task 9.

- [ ] **Step 1: For each approved cluster, dispatch a subagent to draft the contract**

Use the Agent tool (general-purpose, foreground) with this prompt, substituting `<cluster-slug>`, `<Cluster Title>`, and `<term list>` from the approved proposal:

```
Fetch https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
and look up these specific glossary entries: <term list>.

Draft ONE markdown file for path knowledge/style-guide/<cluster-slug>.md
following this exact template (use the real rule text for each term, do not
invent rules not present in the source):

# <Cluster Title>

Status: Draft Version: 0.1.0

## Metadata

```yaml
id: knowledge.style-guide.<cluster-slug>
type: knowledge
title: <Cluster Title>
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: <one sentence>
domain: Style Guide
tags:
  - style-guide
  - <cluster-slug>
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
updated: 2026-07-30
```

## Intent
## Scope
### Included
### Excluded
## Rules
(one ### Rule N subheading per term or closely related group of terms, MUST/SHOULD/MAY language)
## Compliant Example
## Non-Compliant Example
## Dependencies
## References

Hard constraint: the whole file, including metadata, MUST be 150 lines or
fewer. If all terms don't fit, keep the ones most relevant to app UI text
and note which were dropped in a code comment is NOT allowed — just drop them
silently and keep the file within budget; the proposal document already
recorded the full intended list.

Return the complete file content in your final message inside a single
markdown code block. Do not write the file yourself — I will review and save it.
```

- [ ] **Step 2: Save each reviewed draft** to its `knowledge/style-guide/<cluster-slug>.md` path.

- [ ] **Step 3: Validate each file**

Run: `python3 scripts/validate_artifact.py knowledge/style-guide/<cluster-slug>.md --type knowledge`
Expected: `PASS` for every cluster file. Fix and re-run until all pass.

- [ ] **Step 4: Add a reference index entry for each cluster file** in `references/apple/style-guide.md`, same mechanism as Task 3 Step 4.

- [ ] **Step 5: Commit in batches, one commit per cluster (or a small group of clusters reviewed together)**

```bash
git add knowledge/style-guide/<cluster-slug>.md references/apple/style-guide.md
git commit -m "feat(style-guide): add <cluster-slug> knowledge contract"
```

---

## Task 11: Refactor `sign-in-terminology.md` to depend on style-guide

**Files:**
- Modify: `knowledge/authentication/sign-in-terminology.md`

- [ ] **Step 1: Identify the general contract to depend on**

From Task 10's output, find the cluster file that now contains the general "Sign In" / "Sign Out" / "Log In" terminology rule (per the curation proposal, this belongs in a UI-terminology or action-verbs cluster). Note its `id` (e.g. `knowledge.style-guide.ui-action-verbs`) and file path.

- [ ] **Step 2: Edit the metadata**

In `knowledge/authentication/sign-in-terminology.md`, update the `depends_on` field:

```yaml
depends_on:
  - knowledge.authentication.authentication
  - knowledge.style-guide.<cluster-slug>
```

(keep the existing `knowledge.authentication.authentication` entry, add the new one)

- [ ] **Step 3: Trim the restated rule, keep only the auth-specific narrowing**

Edit the `## Rules` section: remove any rule that just restates the general Sign In/Sign Out wording rule (that now lives in the style-guide contract), keep only rules specific to the authentication-flow context (e.g. "use identical terminology across all screens within one authentication flow"). Add one line under `## Scope` → `### Excluded`:

```markdown
-   General Sign In/Sign Out terminology (see knowledge/style-guide/<cluster-slug>.md, [[knowledge/style-guide/<cluster-slug>]])
```

- [ ] **Step 4: Add the wiki-link mirror**

Wherever the new dependency is mentioned in prose in this file, pair it with a `[[knowledge/style-guide/<cluster-slug>]]` mirror per `docs/architecture/linking-model.md`.

- [ ] **Step 5: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/authentication/sign-in-terminology.md --type knowledge`
Expected: `PASS`

- [ ] **Step 6: Commit**

```bash
git add knowledge/authentication/sign-in-terminology.md
git commit -m "refactor(authentication): depend on style-guide for general sign-in terminology"
```

---

## Task 12: Refactor `button-labels.md` to depend on style-guide

**Files:**
- Modify: `knowledge/authentication/button-labels.md`

- [ ] **Step 1-6:** Same procedure as Task 11, applied to `knowledge/authentication/button-labels.md`, using whichever Task 10 cluster now holds the general button-label wording rules (likely the same UI-terminology cluster, or a dedicated `button-labels`/`ui-action-verbs` cluster per the approved proposal).

- [ ] **Step 7: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/authentication/button-labels.md --type knowledge`
Expected: `PASS`

- [ ] **Step 8: Commit**

```bash
git add knowledge/authentication/button-labels.md
git commit -m "refactor(authentication): depend on style-guide for general button-label terminology"
```

---

## Task 13: Write the style-guide skill

**Files:**
- Create: `skills/style-guide/writing.md`

- [ ] **Step 1: Write the skill file**

Create `skills/style-guide/writing.md`:

```markdown
# Style Guide Writing Skill

Status: Draft Version: 0.1.0

## Purpose

Route writing/terminology implementation tasks to the minimum required
style-guide Knowledge Contracts.

## Triggers

Use this skill when the task involves:

-   Writing or reviewing app UI text (labels, buttons, errors, onboarding)
-   Capitalization or terminology questions
-   Formatting dates, numbers, currency, or units in-app
-   Inclusive-writing questions
-   Code font / placeholder-name conventions in text

## Routing

Load only the Knowledge Contracts relevant to the specific task:

-   General terminology/action-verb questions -> knowledge/style-guide/<ui-terminology-cluster>.md
-   Capitalization questions -> knowledge/style-guide/<capitalization-cluster>.md
-   Number/date/currency formatting -> knowledge/style-guide/international-style.md, knowledge/style-guide/international-formatting.md, knowledge/style-guide/units-of-measure.md
-   Inclusive writing -> knowledge/style-guide/writing-inclusively.md
-   Code/placeholder text conventions -> knowledge/style-guide/technical-notation.md
-   Copyright/trademark text -> knowledge/style-guide/copyright-and-trademarks.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/style-guide/ — do not guess or fall back to general knowledge.
```

Fill in the two `<...-cluster>` placeholders in the Routing section with the real cluster file names from Task 10 before saving — this file must not be committed with literal angle-bracket placeholders in it.

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/style-guide/writing.md --type skill`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add skills/style-guide/writing.md
git commit -m "feat(style-guide): add writing skill"
```

---

## Task 14: Update the skills index

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add discovery rows**

In `skills/index.md`, under `## Discovery Rules`, add a row to the table:

```markdown
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/writing.md |
```

- [ ] **Step 2: Commit**

```bash
git add skills/index.md
git commit -m "feat(style-guide): register writing skill in discovery index"
```

---

## Task 15: Final validation sweep

**Files:** none (verification only)

- [ ] **Step 1: Run the validator over every new/changed artifact**

```bash
for f in knowledge/style-guide/*.md; do
  python3 scripts/validate_artifact.py "$f" --type knowledge || echo "FAILED: $f"
done
python3 scripts/validate_artifact.py skills/style-guide/writing.md --type skill
python3 scripts/validate_artifact.py references/apple/style-guide.md --type reference
python3 scripts/validate_artifact.py knowledge/authentication/sign-in-terminology.md --type knowledge
python3 scripts/validate_artifact.py knowledge/authentication/button-labels.md --type knowledge
```

Expected: every line prints `PASS:` and nothing prints `FAILED:`. Fix any failures before proceeding.

- [ ] **Step 2: Check for broken relative links manually**

For each `.md` file under `knowledge/style-guide/`, `skills/style-guide/`, and the two modified `knowledge/authentication/` files, open every relative-path link and confirm the target file exists at that path.

- [ ] **Step 3: Update RFC 0001 status**

In `rfcs/0001-style-guide-domain-and-domain-roadmap.md`, change:

```
Status: Proposed (pending author sign-off)
```

to:

```
Status: Implemented — style-guide domain build complete
```

- [ ] **Step 4: Final commit**

```bash
git add rfcs/0001-style-guide-domain-and-domain-roadmap.md
git commit -m "docs: mark RFC 0001 implemented, style-guide domain complete"
```
