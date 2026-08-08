"""Tests for lifecycle transition validation.

A transition only exists between two versions of a file, so each test builds a
real git repository in a temporary directory, commits one status, changes it in
the working tree, and asserts what the check makes of the pair.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_transitions  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check_transitions.py"

KNOWLEDGE = """# Thing

Status: {status}
Version: 1.0.0

## Metadata

``` yaml
id: knowledge.example.thing
artifact_type: knowledge
title: Thing
version: 1.0.0
status: {status}
owner: Apple Agent Kit
summary: Defines the thing.
domain: Example
tags:
  - thing
references: []
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

Intent.

## Rules

### Rule 1

Rule.

## Compliant Example

OK.

## Non-Compliant Example

Not OK.

## Dependencies

None.
"""

REL = "knowledge/example/thing.md"


class TransitionTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def git(self, *args):
        subprocess.run(
            ["git", "-C", str(self.root), *args], check=True, capture_output=True
        )

    def commit(self, status):
        path = self.root / REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(KNOWLEDGE.format(status=status))
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "Test")
        self.git("add", ".")
        self.git("commit", "-qm", "base")

    def transition(self, before, after):
        self.commit(before)
        (self.root / REL).write_text(KNOWLEDGE.format(status=after))
        return check_transitions.check(self.root, "HEAD")


class TestAllowedTransitions(TransitionTestCase):
    def test_every_documented_transition_is_accepted(self):
        for before, after in sorted(check_transitions.ALLOWED):
            with self.subTest(f"{before} -> {after}"):
                self.setUp()
                self.assertEqual(self.transition(before, after), [])

    def test_no_change_is_not_a_transition(self):
        self.assertEqual(self.transition("Draft", "Draft"), [])


class TestRejectedTransitions(TransitionTestCase):
    def test_draft_to_archived_skips_the_lifecycle(self):
        findings = self.transition("Draft", "Archived")
        self.assertEqual(findings, [(REL, "Draft", "Archived")])

    def test_archived_does_not_come_back(self):
        # "Retained for historical reference only." Nothing leaves Archived.
        self.assertEqual(
            self.transition("Archived", "Approved"), [(REL, "Archived", "Approved")]
        )

    def test_deprecated_does_not_return_to_approved(self):
        self.assertEqual(
            self.transition("Deprecated", "Approved"), [(REL, "Deprecated", "Approved")]
        )

    def test_draft_to_deprecated_is_rejected(self):
        # Deprecation means "scheduled for replacement", which presupposes the
        # artifact was current. A Draft was never current.
        self.assertEqual(
            self.transition("Draft", "Deprecated"), [(REL, "Draft", "Deprecated")]
        )


class TestScope(TransitionTestCase):
    def test_a_new_artifact_has_no_transition_to_judge(self):
        self.commit("Draft")
        (self.root / "knowledge/example/new.md").write_text(
            KNOWLEDGE.format(status="Approved").replace(
                "knowledge.example.thing", "knowledge.example.new"
            )
        )
        self.assertEqual(check_transitions.check(self.root, "HEAD"), [])

    def test_allowed_set_matches_the_lifecycle_document(self):
        # The document is the authority; this test is what makes editing one
        # without the other fail.
        text = (REPO_ROOT / "docs/artifact-lifecycle.md").read_text()
        section = text.split("## Allowed Transitions")[1].split("##")[0]
        # One entry carries a parenthetical gloss -- "Approved → Draft
        # (reopened for revision)" -- which names the reason, not the state.
        documented = {
            tuple(
                part.strip().split(" (")[0].strip()
                for part in line.lstrip("- ").split("→")
            )
            for line in section.strip().splitlines()
            if "→" in line
        }
        self.assertEqual(documented, check_transitions.ALLOWED)


class TestCLI(unittest.TestCase):
    def test_running_against_the_repository_passes(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(REPO_ROOT), "--base", "HEAD"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
