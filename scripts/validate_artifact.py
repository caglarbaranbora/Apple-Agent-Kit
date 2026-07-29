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
