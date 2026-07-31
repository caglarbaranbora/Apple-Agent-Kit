import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_artifact  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_artifact.py"


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

    def test_substring_heading_match_is_rejected(self):
        # A heading that merely *contains* "## Rules" as a substring (e.g. a
        # renamed "## Rules of Thumb") must NOT satisfy the "## Rules"
        # requirement -- only an exact standalone heading line should.
        text = VALID_KNOWLEDGE.replace("## Rules", "## Rules of Thumb")
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertTrue(
            any(e == "missing required section: ## Rules" for e in errors),
            f"expected a missing '## Rules' error, got: {errors}",
        )

    def test_missing_metadata_yaml_block_entirely(self):
        # No ```yaml fence anywhere in the document (not just an empty one).
        text = re.sub(r"```\s*ya?ml\n.*?```\n", "", VALID_KNOWLEDGE, flags=re.DOTALL)
        self.assertNotIn("```", text)
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertIn("missing metadata YAML block", errors)


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


class TestValidateArtifactCLI(unittest.TestCase):
    def _run_cli(self, path, artifact_type):
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(path), "--type", artifact_type],
            capture_output=True,
            text=True,
        )

    def test_cli_pass_exit_code_and_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "valid.md"
            path.write_text(VALID_KNOWLEDGE)
            result = self._run_cli(path, "knowledge")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS:", result.stdout)
        self.assertNotIn("FAIL:", result.stdout)

    def test_cli_fail_exit_code_and_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "invalid.md"
            path.write_text(VALID_KNOWLEDGE.replace("## Rules", "## Rules of Thumb"))
            result = self._run_cli(path, "knowledge")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL:", result.stdout)
        self.assertIn("## Rules", result.stdout)


if __name__ == "__main__":
    unittest.main()
