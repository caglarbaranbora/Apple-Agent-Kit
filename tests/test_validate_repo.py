"""Tests for Levels 2-3 validation.

Each test builds a minimal, valid repository in a temporary directory, breaks
exactly one thing, and asserts that the matching rule fires. Building the
fixture rather than pointing at the real repository keeps these tests from
turning into a snapshot of whatever the repository happens to contain today.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_repo  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_repo.py"

URL = "https://developer.apple.com/documentation/example/thing"

REFERENCE = """# Example

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.example
artifact_type: reference
title: Example
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's example documentation.
domain: Example
last_updated: 2026-08-07
```

## Source

{url}

## Purpose

Reference index for Apple's example documentation.

## Primary Topics

- Example topic

## Used By

- knowledge/example/thing.md ([[knowledge/example/thing]])
""".format(url=URL)

KNOWLEDGE = """# Thing

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: knowledge.example.thing
artifact_type: knowledge
title: Thing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the thing.
domain: Example
tags:
  - thing
references:
  - {url}
depends_on: []
related: []
last_updated: 2026-08-07
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
""".format(url=URL)

SKILL = """---
name: example
description: Example skill. Use when the task involves example things. Triggers on example.
id: skill.example.foundations
title: Example
version: 1.0.0
status: Approved
artifact_type: skill
domain: Example
routes: [knowledge.example.thing]
related: []
last_updated: 2026-08-07
---

# Example Skill

## Purpose

Route example tasks.

## Routing

- Anything about the thing -> thing.md

## Stop Conditions

Stop if no contract matches.
"""

INDEX = """# Routing Index

## Skills

| Skill | Triggers |
|---|---|
| skills/example/SKILL.md | example |
"""


class RepoFixture:
    """A minimal repository that passes every Level 2-3 check."""

    def __init__(self, tmpdir):
        self.root = Path(tmpdir)
        self.write("references/apple/example.md", REFERENCE)
        self.write("knowledge/example/thing.md", KNOWLEDGE)
        self.write("skills/example/SKILL.md", SKILL)
        self.write("skills/index.md", INDEX)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def edit(self, rel, old, new):
        path = self.root / rel
        text = path.read_text()
        assert old in text, f"{old!r} not found in {rel}"
        path.write_text(text.replace(old, new, 1))

    def rules(self):
        _, findings = validate_repo.validate_repo(self.root)
        return [f.rule for f in findings]

    def findings(self):
        return validate_repo.validate_repo(self.root)[1]


class RepoTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = RepoFixture(self._tmp.name)

    def assertRule(self, rule):
        rules = self.repo.rules()
        self.assertIn(rule, rules, f"expected `{rule}`, got: {rules}")


class TestFixtureIsValid(RepoTestCase):
    def test_clean_repository_has_no_findings(self):
        self.assertEqual([str(f) for f in self.repo.findings()], [])


class TestLevel2(RepoTestCase):
    def test_duplicate_id_is_reported(self):
        self.repo.write(
            "knowledge/example/copy.md",
            KNOWLEDGE.replace("# Thing", "# Copy"),
        )
        self.assertRule("id-unique")

    def test_missing_id_is_reported(self):
        self.repo.edit("knowledge/example/thing.md", "id: knowledge.example.thing\n", "")
        self.assertRule("id-present")

    def test_id_must_agree_with_path(self):
        self.repo.edit(
            "knowledge/example/thing.md",
            "id: knowledge.example.thing",
            "id: knowledge.example.other",
        )
        self.assertRule("id-path")

    def test_skill_id_domain_segment_must_match_directory(self):
        self.repo.edit(
            "skills/example/SKILL.md",
            "id: skill.example.foundations",
            "id: skill.different.foundations",
        )
        self.assertRule("id-path")

    def test_skill_facet_directory_is_accepted(self):
        # `skills/<domain>-<facet>/` holding `skill.<domain>.<facet>` is the
        # documented layout (skills/swiftui-interaction), not a violation.
        skill = (self.repo.root / "skills/example/SKILL.md").read_text()
        (self.repo.root / "skills/example").rename(self.repo.root / "skills/example-x")
        (self.repo.root / "skills/example-x/SKILL.md").write_text(
            skill.replace("skill.example.foundations", "skill.example.x")
        )
        self.repo.edit("skills/index.md", "skills/example/", "skills/example-x/")
        self.assertNotIn("id-path", self.repo.rules())

    def test_domain_must_agree_with_directory(self):
        self.repo.edit("knowledge/example/thing.md", "domain: Example", "domain: Other")
        self.assertRule("domain-path")

    def test_domain_comparison_is_slug_insensitive(self):
        # `domain` carries the proper name, the directory carries the slug.
        (self.repo.root / "knowledge/example").rename(
            self.repo.root / "knowledge/two-words"
        )
        self.repo.edit(
            "knowledge/two-words/thing.md",
            "id: knowledge.example.thing",
            "id: knowledge.two-words.thing",
        )
        self.repo.edit("knowledge/two-words/thing.md", "domain: Example", "domain: Two Words")
        self.assertNotIn("domain-path", self.repo.rules())

    def test_unresolved_edge_is_reported(self):
        self.repo.edit(
            "knowledge/example/thing.md", "related: []", "related: [knowledge.example.gone]"
        )
        self.assertRule("edge-resolves")

    def test_unresolved_wiki_link_is_reported(self):
        self.repo.edit(
            "references/apple/example.md",
            "[[knowledge/example/thing]]",
            "[[knowledge/example/vanished]]",
        )
        self.assertRule("wiki-link-resolves")

    def test_used_by_must_list_every_citing_contract(self):
        # The reverse index is checked by URL. This is the check that found two
        # real cross-domain gaps that no directory-derived check could see.
        self.repo.write(
            "knowledge/other/second.md",
            KNOWLEDGE.replace("knowledge.example.thing", "knowledge.other.second")
            .replace("domain: Example", "domain: Other")
            .replace("# Thing", "# Second"),
        )
        self.assertRule("used-by-complete")

    def test_used_by_is_not_derived_from_directory_names(self):
        # A Contract outside the Reference's own domain is legitimate as long as
        # `## Used By` lists it -- Reference-to-Knowledge is many-to-many.
        self.repo.write(
            "knowledge/other/second.md",
            KNOWLEDGE.replace("knowledge.example.thing", "knowledge.other.second")
            .replace("domain: Example", "domain: Other")
            .replace("# Thing", "# Second"),
        )
        self.repo.edit(
            "references/apple/example.md",
            "- knowledge/example/thing.md ([[knowledge/example/thing]])",
            "- knowledge/example/thing.md ([[knowledge/example/thing]])\n"
            "- knowledge/other/second.md ([[knowledge/other/second]])",
        )
        self.repo.edit(
            "skills/example/SKILL.md",
            "routes: [knowledge.example.thing]",
            "routes: [knowledge.example.thing, knowledge.other.second]",
        )
        self.repo.edit("skills/example/SKILL.md", "-> thing.md", "-> thing.md, second.md")
        self.assertNotIn("used-by-complete", self.repo.rules())

    def test_broken_prose_link_is_reported(self):
        self.repo.write("docs/guide.md", "See [the spec](../docs/missing.md).\n")
        self.assertRule("prose-path-resolves")

    def test_resolving_prose_link_is_accepted(self):
        self.repo.write("docs/guide.md", "See [the index](../skills/index.md).\n")
        self.assertNotIn("prose-path-resolves", self.repo.rules())

    def test_a_link_inside_a_code_span_is_a_format_example(self):
        self.repo.write("docs/guide.md", "Format: `- **name** -> [SKILL.md](skills/name/SKILL.md)`\n")
        self.assertNotIn("prose-path-resolves", self.repo.rules())

    def test_a_link_inside_a_fenced_block_is_not_checked(self):
        self.repo.write("docs/guide.md", "```md\n[example](nowhere.md)\n```\n")
        self.assertNotIn("prose-path-resolves", self.repo.rules())

    def test_a_target_containing_whitespace_is_not_a_path(self):
        # `^[...](inflect: true)` is localization syntax, not a link.
        self.repo.write("docs/guide.md", "Use `^[one](inflect: true)` in translations.\n")
        self.assertNotIn("prose-path-resolves", self.repo.rules())

    def test_npx_readme_links_resolve_against_the_repository_root(self):
        # npx/README.md is a byte-for-byte mirror of the root README, published
        # to npm; its links are written for a reader on GitHub.
        self.repo.write("README.md", "See [the index](skills/index.md).\n")
        self.repo.write("npx/README.md", "See [the index](skills/index.md).\n")
        self.assertNotIn("prose-path-resolves", self.repo.rules())

    def test_unrouted_contract_is_an_orphan(self):
        self.repo.edit(
            "skills/example/SKILL.md", "routes: [knowledge.example.thing]", "routes: []"
        )
        self.assertRule("orphan")

    def test_contract_reached_only_by_depends_on_is_not_an_orphan(self):
        self.repo.write(
            "knowledge/example/base.md",
            KNOWLEDGE.replace("knowledge.example.thing", "knowledge.example.base")
            .replace("# Thing", "# Base"),
        )
        self.repo.edit(
            "knowledge/example/thing.md",
            "depends_on: []",
            "depends_on: [knowledge.example.base]",
        )
        self.repo.edit(
            "references/apple/example.md",
            "- knowledge/example/thing.md ([[knowledge/example/thing]])",
            "- knowledge/example/thing.md ([[knowledge/example/thing]])\n"
            "- knowledge/example/base.md ([[knowledge/example/base]])",
        )
        self.assertNotIn("orphan", self.repo.rules())

    def test_reference_with_empty_used_by_is_an_orphan(self):
        self.repo.edit(
            "references/apple/example.md",
            "- knowledge/example/thing.md ([[knowledge/example/thing]])",
            "",
        )
        self.assertRule("orphan")

    def test_skill_absent_from_the_routing_index(self):
        self.repo.edit("skills/index.md", "skills/example/SKILL.md", "nothing")
        self.assertRule("index-sync")

    def test_routing_index_naming_something_absent_from_disk(self):
        self.repo.edit(
            "skills/index.md",
            "| skills/example/SKILL.md | example |",
            "| skills/example/SKILL.md | example |\n| skills/ghost/SKILL.md | ghost |",
        )
        self.assertRule("index-sync")

    def test_prose_hand_off_to_a_domain_that_does_not_exist(self):
        # The shape both defects Phase 4 left behind had: an Excluded line
        # pointing at a domain, in prose rather than in an edge field.
        self.repo.edit(
            "knowledge/example/thing.md",
            "## Rules",
            "## Notes\n\n-   Sign-in wording -- see the `ghost` domain\n\n## Rules",
        )
        self.assertRule("prose-domain-resolves")

    def test_bare_mention_of_a_retired_domain(self):
        # Not code-spanned, so only the retirement register catches it.
        self.repo.write(
            "docs/architecture/domain-map.md",
            "| Domain | Status |\n|---|---|\n"
            "| ghost | **Retired 2026-08-07** |\n",
        )
        self.repo.edit(
            "skills/example/SKILL.md",
            "## Routing",
            "## Routing\n\nFor sign-in wording see the ghost skill.\n",
        )
        self.assertRule("prose-domain-resolves")

    def test_hyphenated_adjective_before_domain_is_not_a_name(self):
        # "concurrency-focused domain" is English. Reporting it was the whole
        # false-positive class this check had to survive.
        self.repo.edit(
            "knowledge/example/thing.md",
            "## Rules",
            "## Notes\n\n-   This is a concurrency-focused domain, and the\n"
            "    per-domain skill split follows from that.\n\n## Rules",
        )
        self.assertEqual([str(f) for f in self.repo.findings()], [])

    def test_a_workflow_does_not_make_a_retired_domain_name_resolve(self):
        # `workflow.authentication` took the name of the domain Phase 4
        # retired. Counting Workflow names as domain names made this check
        # pass on the very hand-offs it was written to catch, and every unit
        # test still went green -- only the real defect exposed it.
        self.repo.write(
            "workflows/ghost/WORKFLOW.md",
            "# Ghost\n\n## Metadata\n\n``` yaml\nid: workflow.ghost\n"
            "artifact_type: workflow\ntitle: Ghost\nversion: 0.1.0\n"
            "status: Draft\nowner: Apple Agent Kit\nsummary: Composes two.\n"
            "skills:\n  - skill.example.foundations\n  - skill.other.foundations\n"
            "related: []\nlast_updated: 2026-08-07\n```\n",
        )
        self.repo.edit(
            "knowledge/example/thing.md",
            "## Rules",
            "## Notes\n\n-   Sign-in wording -- see the `ghost` domain\n\n## Rules",
        )
        self.assertRule("prose-domain-resolves")

    def test_a_mention_of_an_existing_workflow_is_accepted(self):
        self.repo.write(
            "workflows/ghost/WORKFLOW.md",
            "# Ghost\n\n## Metadata\n\n``` yaml\nid: workflow.ghost\n"
            "artifact_type: workflow\ntitle: Ghost\nversion: 0.1.0\n"
            "status: Draft\nowner: Apple Agent Kit\nsummary: Composes two.\n"
            "skills:\n  - skill.example.foundations\n  - skill.other.foundations\n"
            "related: []\nlast_updated: 2026-08-07\n```\n",
        )
        self.repo.edit(
            "knowledge/example/thing.md",
            "## Rules",
            "## Notes\n\n-   Composing these is the `ghost` workflow's job.\n\n## Rules",
        )
        self.assertNotIn("prose-domain-resolves", self.repo.rules())

    def test_domain_map_may_still_name_what_it_retired(self):
        self.repo.write(
            "docs/architecture/domain-map.md",
            "| Domain | Status |\n|---|---|\n"
            "| ghost | **Retired 2026-08-07** |\n\n"
            "The `ghost` domain was retired; `example` absorbed it.\n",
        )
        self.assertEqual([str(f) for f in self.repo.findings()], [])

    def test_entry_needs_no_routing_index_row(self):
        # The entry point points at the Routing Index; it is not listed in it.
        self.repo.write(
            "skills/apple-agent-kit/SKILL.md",
            "---\nname: apple-agent-kit\ndescription: Entry point.\n"
            "id: entry.apple-agent-kit\nartifact_type: entry\ntitle: Apple Agent Kit\n"
            "version: 1.0.0\nstatus: Approved\nlast_updated: 2026-08-07\n---\n\nRead AGENTS.md.\n",
        )
        self.assertEqual([str(f) for f in self.repo.findings()], [])


class TestScopeVocabulary(RepoTestCase):
    def stop(self, text):
        self.repo.edit("skills/example/SKILL.md", "Stop if no contract matches.", text)

    def test_ambiguous_phrasing_is_reported(self):
        self.stop("Widgets are out of scope for this skill.")
        self.assertRule("scope-vocabulary")

    def test_line_wrapped_ambiguous_phrasing_is_reported(self):
        # `swiftui` wraps between "this" and "skill". Matching the raw text
        # missed it, which is how a manual grep missed a hand-off in PR 0.
        self.stop("Widgets are out of scope for this\nskill.")
        self.assertRule("scope-vocabulary")

    def test_calling_a_built_domain_unbuilt_is_reported(self):
        self.stop("Keychain is owned by a future `other` domain, not yet built.")
        self.repo.write("knowledge/other/thing.md", KNOWLEDGE)
        self.assertRule("scope-vocabulary")

    def test_a_distant_hand_off_is_not_blamed_for_a_nearby_deferral(self):
        # One `accessibility` sentence hands off to a built domain and then
        # calls a second domain future. Splitting on sentences blamed both.
        self.repo.write("knowledge/other/thing.md", KNOWLEDGE)
        self.stop(
            "Design guidance is owned by `other`, and general testing "
            "conventions well beyond anything this one covers belong to a "
            "future domain nobody has built."
        )
        self.assertNotIn("scope-vocabulary", self.repo.rules())

    def test_the_marked_vocabulary_is_accepted(self):
        self.repo.write("knowledge/other/thing.md", KNOWLEDGE)
        self.stop(
            "Stop if no contract matches.\n\n"
            "-   Widgets — Deferred\n"
            "-   Storyboards — Excluded\n"
            "-   Keychain — owned by `other`\n"
        )
        self.assertNotIn("scope-vocabulary", self.repo.rules())


class TestLevel3(RepoTestCase):
    def test_forbidden_dependency_direction(self):
        # Knowledge may not depend on a Skill.
        self.repo.edit(
            "knowledge/example/thing.md",
            "depends_on: []",
            "depends_on: [skill.example.foundations]",
        )
        self.assertRule("dependency-direction")

    def test_related_has_no_direction_constraint(self):
        # A Skill's `related` naming another Skill is legal and widespread.
        self.repo.edit(
            "knowledge/example/thing.md", "related: []", "related: [skill.example.foundations]"
        )
        self.assertNotIn("dependency-direction", self.repo.rules())

    def test_dependency_cycle_is_reported(self):
        self.repo.write(
            "knowledge/example/other.md",
            KNOWLEDGE.replace("knowledge.example.thing", "knowledge.example.other")
            .replace("# Thing", "# Other")
            .replace("depends_on: []", "depends_on: [knowledge.example.thing]"),
        )
        self.repo.edit(
            "knowledge/example/thing.md",
            "depends_on: []",
            "depends_on: [knowledge.example.other]",
        )
        rules = self.repo.rules()
        self.assertIn("dependency-acyclic", rules)

    def test_routed_contract_absent_from_the_routing_section(self):
        self.repo.edit("skills/example/SKILL.md", "-> thing.md", "-> something-else.md")
        self.assertRule("routing-coverage")

    def test_skill_may_not_route_to_a_skill(self):
        self.repo.write(
            "skills/second/SKILL.md",
            SKILL.replace("skill.example.foundations", "skill.second.foundations")
            .replace("name: example", "name: second")
            .replace("domain: Example", "domain: Second"),
        )
        self.repo.edit("skills/index.md", "| example |", "| example |\n| skills/second/SKILL.md | second |")
        self.repo.edit(
            "skills/example/SKILL.md",
            "routes: [knowledge.example.thing]",
            "routes: [knowledge.example.thing, skill.second.foundations]",
        )
        self.assertRule("no-skill-to-skill")

    def test_workflow_naming_one_skill_is_reported(self):
        self.repo.write(
            "workflows/example-flow/WORKFLOW.md",
            "# Example Flow\n\n## Metadata\n\n``` yaml\n"
            "id: workflow.example-flow\nartifact_type: workflow\ntitle: Example Flow\n"
            "version: 1.0.0\nstatus: Approved\nlast_updated: 2026-08-07\n"
            "skills: [skill.example.foundations]\nrelated: []\n```\n\n"
            "## Purpose\n\nP.\n\n## Scope\n\nS.\n\n## Trigger Conditions\n\nT.\n\n"
            "## Skill Sequence\n\n1. example\n\n## Exit Conditions\n\nE.\n",
        )
        self.repo.edit(
            "skills/index.md",
            "| example |",
            "| example |\n| workflows/example-flow/WORKFLOW.md | flow |",
        )
        self.assertRule("workflow-composes")


class TestCLI(unittest.TestCase):
    def _run(self, root):
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(root)],
            capture_output=True,
            text=True,
        )

    def test_clean_repository_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            RepoFixture(tmpdir)
            result = self._run(tmpdir)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS", result.stdout)

    def test_broken_repository_exits_one_and_names_the_remediation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = RepoFixture(tmpdir)
            repo.edit(
                "knowledge/example/thing.md", "related: []", "related: [knowledge.example.gone]"
            )
            result = self._run(tmpdir)
        self.assertEqual(result.returncode, 1)
        self.assertIn("edge-resolves", result.stdout)
        self.assertIn("fix:", result.stdout)


if __name__ == "__main__":
    unittest.main()
