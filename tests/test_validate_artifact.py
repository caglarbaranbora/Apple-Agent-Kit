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
artifact_type: knowledge
title: Example
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: An example contract.
domain: Style Guide
tags:
  - example
depends_on: []
related: []
references:
  - https://developer.apple.com/design/human-interface-guidelines/inclusion
last_updated: 2026-08-07
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

## Dependencies

None.
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

    def test_old_metadata_dialect_is_rejected(self):
        # `type:` and `updated:` were the pre-v1 field names. The repository now
        # has one dialect; the old names must not satisfy the new requirement.
        text = VALID_KNOWLEDGE.replace(
            "artifact_type: knowledge", "type: knowledge"
        ).replace("last_updated: 2026-08-07", "updated: 2026-08-07")
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertTrue(any("artifact_type" in e for e in errors))
        self.assertTrue(any("last_updated" in e for e in errors))

    def test_dependencies_section_is_required(self):
        # Transitive resolution lives in the Knowledge layer, so every Contract
        # must declare its dependencies -- see docs/architecture/routing-model.md.
        text = VALID_KNOWLEDGE.replace("## Dependencies", "## Deps")
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertIn("missing required section: ## Dependencies", errors)


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


VALID_REFERENCE = """# Example Domain

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.example-domain
artifact_type: reference
title: Example Domain
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's example documentation.
domain: Example Domain
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/example

## Purpose

Reference index for Apple's example documentation.

## Primary Topics

- Example topic

## Used By

- [[knowledge/example-domain/example]]
"""


class TestValidateReference(unittest.TestCase):
    def test_valid_reference_has_no_errors(self):
        errors = validate_artifact.validate_text(VALID_REFERENCE, "reference")
        self.assertEqual(errors, [])

    def test_reference_requires_its_sections(self):
        # Before v1 finalization a Reference had no specification at all, so an
        # empty file passed. All four sections are now required.
        for heading in ("## Source", "## Purpose", "## Primary Topics", "## Used By"):
            text = VALID_REFERENCE.replace(heading, heading + " Renamed")
            errors = validate_artifact.validate_text(text, "reference")
            self.assertIn(f"missing required section: {heading}", errors)

    def test_reference_requires_base_metadata(self):
        text = VALID_REFERENCE.replace("artifact_type: reference\n", "")
        errors = validate_artifact.validate_text(text, "reference")
        self.assertTrue(any("artifact_type" in e for e in errors))

    def test_reference_line_cap_is_98(self):
        text = VALID_REFERENCE + ("\nextra line\n" * 60)
        errors = validate_artifact.validate_text(text, "reference")
        self.assertTrue(any("line cap" in e for e in errors))
        self.assertTrue(any("> 98" in e for e in errors))

    def test_empty_reference_no_longer_passes(self):
        errors = validate_artifact.validate_text("# Empty\n", "reference")
        self.assertIn("missing metadata YAML block", errors)
        self.assertTrue(any("missing required section" in e for e in errors))


class TestMetadataSchema(unittest.TestCase):
    def test_base_fields_required_of_every_type(self):
        for artifact_type in validate_artifact.ARTIFACT_TYPES:
            fields = validate_artifact.required_metadata_fields(artifact_type)
            for base in validate_artifact.BASE_METADATA_FIELDS:
                self.assertIn(base, fields, f"{artifact_type} is missing {base}")

    def test_workflow_and_entry_are_not_domain_scoped(self):
        # A workflow spans domains by definition; the entry point belongs to
        # none. Both are why `domain` is an extension, not a base field.
        self.assertNotIn("domain", validate_artifact.required_metadata_fields("workflow"))
        self.assertNotIn("domain", validate_artifact.required_metadata_fields("entry"))
        self.assertIn("domain", validate_artifact.required_metadata_fields("knowledge"))


class TestEnumsAndVersion(unittest.TestCase):
    def test_unknown_status_is_rejected(self):
        # docs/artifact-lifecycle.md names four states. "Review" was dropped.
        text = VALID_KNOWLEDGE.replace("status: Draft", "status: Review")
        errors = validate_artifact.validate_text(text, "knowledge")
        self.assertTrue(any("unknown status" in e for e in errors), errors)

    def test_every_lifecycle_state_is_accepted(self):
        for status in validate_artifact.STATUSES:
            text = VALID_KNOWLEDGE.replace("status: Draft", f"status: {status}")
            errors = validate_artifact.validate_text(text, "knowledge")
            self.assertEqual(errors, [], f"{status} was rejected")

    def test_non_semantic_version_is_rejected(self):
        for bad in ("1.0", "v1.0.0", "1.0.0-beta", "latest"):
            text = VALID_KNOWLEDGE.replace("version: 0.1.0", f"version: {bad}")
            errors = validate_artifact.validate_text(text, "knowledge")
            self.assertTrue(
                any("semantic version" in e for e in errors), f"{bad} was accepted"
            )

    def test_artifact_type_must_match_the_type_being_validated(self):
        # A Reference validated as knowledge must fail on the field, not merely
        # on its sections -- the two are different failures.
        errors = validate_artifact.validate_text(VALID_REFERENCE, "knowledge")
        self.assertTrue(
            any("artifact_type is `reference`" in e for e in errors), errors
        )


class TestLocationAgreement(unittest.TestCase):
    def test_knowledge_under_references_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "references" / "apple" / "misfiled.md"
            path.parent.mkdir(parents=True)
            path.write_text(VALID_KNOWLEDGE)
            errors = validate_artifact.validate_file(path, "knowledge")
        self.assertTrue(any("belongs under `knowledge/`" in e for e in errors), errors)

    def test_knowledge_under_knowledge_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "knowledge" / "style-guide" / "example.md"
            path.parent.mkdir(parents=True)
            path.write_text(VALID_KNOWLEDGE)
            errors = validate_artifact.validate_file(path, "knowledge")
        self.assertEqual(errors, [])

    def test_a_file_outside_the_artifact_tree_is_not_misfiled(self):
        # A fixture in a scratch directory is in no artifact root at all, which
        # is not the same thing as being in the wrong one.
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.md"
            path.write_text(VALID_KNOWLEDGE)
            errors = validate_artifact.validate_file(path, "knowledge")
        self.assertEqual(errors, [])


class TestValidateAll(unittest.TestCase):
    def _build(self, tmpdir):
        root = Path(tmpdir)
        (root / "knowledge" / "style-guide").mkdir(parents=True)
        (root / "knowledge" / "style-guide" / "example.md").write_text(VALID_KNOWLEDGE)
        (root / "skills" / "style-guide").mkdir(parents=True)
        (root / "skills" / "style-guide" / "SKILL.md").write_text(VALID_SKILL)
        return root

    def test_type_is_taken_from_metadata_not_from_location(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._build(tmpdir)
            checked, failures = validate_artifact.validate_all(root)
        self.assertEqual(checked, 2)
        self.assertEqual(failures, {})

    def test_an_entry_among_the_skills_is_validated_as_an_entry(self):
        # skills/apple-agent-kit/SKILL.md is the entry point, not a Skill. Only
        # its metadata says so, and --all must believe the metadata.
        entry = (
            "---\nname: apple-agent-kit\ndescription: Entry point.\n"
            "id: entry.apple-agent-kit\nartifact_type: entry\n"
            "title: Apple Agent Kit\nversion: 1.0.0\nstatus: Approved\n"
            "last_updated: 2026-08-07\n---\n\nRead AGENTS.md.\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._build(tmpdir)
            (root / "skills" / "apple-agent-kit").mkdir()
            (root / "skills" / "apple-agent-kit" / "SKILL.md").write_text(entry)
            checked, failures = validate_artifact.validate_all(root)
        self.assertEqual(checked, 3)
        self.assertEqual(failures, {})

    def test_a_broken_artifact_is_reported_with_its_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._build(tmpdir)
            broken = root / "knowledge" / "style-guide" / "example.md"
            broken.write_text(VALID_KNOWLEDGE.replace("## Rules", "## Guidelines"))
            checked, failures = validate_artifact.validate_all(root)
        self.assertIn(broken, failures)
        self.assertIn("missing required section: ## Rules", failures[broken])


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
