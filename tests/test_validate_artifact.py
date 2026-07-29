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


if __name__ == "__main__":
    unittest.main()
