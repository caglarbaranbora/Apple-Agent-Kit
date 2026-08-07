#!/usr/bin/env python3
"""Level 1 (Structural) validation for Apple Agent Kit artifacts.

Authority for everything in this file:
  schemas/metadata.schema.md          -- field names and per-type extensions
  docs/specifications/*-spec.md       -- required sections and size limits
  docs/validation-model.md            -- what Level 1 covers

A disagreement between this file and those documents is a release-blocking
defect, not a preference. Levels 2-3 (repository-wide) live in validate_repo.py.
"""
import argparse
import re
import sys
from pathlib import Path

ARTIFACT_TYPES = ["knowledge", "skill", "reference", "workflow", "entry"]

LINE_CAPS = {"knowledge": 150, "skill": 80, "reference": 98, "workflow": 80}

REQUIRED_SECTIONS = {
    "knowledge": [
        "## Intent",
        "## Rules",
        "## Compliant Example",
        "## Non-Compliant Example",
        "## Dependencies",
    ],
    "skill": ["## Purpose", "## Routing", "## Stop Conditions"],
    "reference": ["## Source", "## Purpose", "## Primary Topics", "## Used By"],
    "workflow": [
        "## Purpose",
        "## Scope",
        "## Trigger Conditions",
        "## Skill Sequence",
        "## Exit Conditions",
    ],
}

# Required of every artifact type.
BASE_METADATA_FIELDS = [
    "id",
    "artifact_type",
    "title",
    "version",
    "status",
    "last_updated",
]

# Added per type. `domain` is an extension rather than a base field because a
# workflow spans domains by definition and an entry belongs to none.
METADATA_EXTENSIONS = {
    "knowledge": [
        "domain",
        "owner",
        "summary",
        "tags",
        "depends_on",
        "related",
        "references",
    ],
    "skill": ["domain", "name", "description", "routes", "related"],
    "reference": ["domain", "owner", "summary"],
    "workflow": ["skills", "related"],
    "entry": ["name", "description"],
}


def required_metadata_fields(artifact_type):
    return BASE_METADATA_FIELDS + METADATA_EXTENSIONS.get(artifact_type, [])


def extract_metadata_block(text, artifact_type=None):
    if artifact_type in ("skill", "entry"):
        # Real Claude Code skills need frontmatter at byte offset 0 -- a
        # fenced ```yaml block anywhere in the body (the knowledge/reference
        # convention) is not something the skill loader parses.
        match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
        return match.group(1) if match else ""
    match = re.search(r"```\s*ya?ml\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else ""


def validate_text(text, artifact_type):
    errors = []
    cap = LINE_CAPS.get(artifact_type)
    line_count = len(text.splitlines())
    if cap is not None and line_count > cap:
        errors.append(f"exceeds {artifact_type} line cap: {line_count} > {cap}")

    for heading in REQUIRED_SECTIONS.get(artifact_type, []):
        if not re.search(rf"^{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"missing required section: {heading}")

    block = extract_metadata_block(text, artifact_type)
    if not block:
        errors.append("missing metadata YAML block")
    else:
        for field in required_metadata_fields(artifact_type):
            if not re.search(rf"^{field}:", block, re.MULTILINE):
                errors.append(f"missing required metadata field: {field}")

    return errors


def validate_file(path, artifact_type):
    return validate_text(Path(path).read_text(), artifact_type)


def main():
    parser = argparse.ArgumentParser(
        description="Validate an Apple Agent Kit artifact (Level 1 - Structural)."
    )
    parser.add_argument("path", help="Path to the artifact markdown file")
    parser.add_argument(
        "--type", required=True, choices=ARTIFACT_TYPES, help="Artifact type"
    )
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
