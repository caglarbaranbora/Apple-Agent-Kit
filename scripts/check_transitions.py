#!/usr/bin/env python3
"""Lifecycle transition validation for Apple Agent Kit artifacts.

`docs/artifact-lifecycle.md` requires validators to reject invalid state
transitions. No working tree can decide that: a transition is a relationship
between two versions of a file, and Levels 1-3 are defined as offline and
deterministic -- "the same working tree gives the same answer forever", which
is what earns them the right to block a commit. A history-reading check does
not have that property, so it does not belong in `validate_repo.py`.

It belongs where a transition actually exists: a pull request. This script
compares a base ref against the working tree and reports any status change the
lifecycle does not allow, on the same reasoning that keeps `check_links.py`
outside the levels -- a check whose answer depends on something other than the
tree is a separate script on a separate trigger.

    python3 scripts/check_transitions.py .                       # vs origin/main
    python3 scripts/check_transitions.py . --base HEAD~1
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

# docs/artifact-lifecycle.md, "Allowed Transitions".
ALLOWED = {
    ("Draft", "Approved"),
    ("Approved", "Draft"),
    ("Approved", "Deprecated"),
    ("Deprecated", "Archived"),
}

STATUSES = ("Draft", "Approved", "Deprecated", "Archived")

ARTIFACT_GLOBS = (
    "knowledge/*/*.md",
    "skills/*/SKILL.md",
    "references/apple/*.md",
    "workflows/*/WORKFLOW.md",
)

STATUS_LINE = re.compile(r"^status:[ \t]*(\S+)[ \t]*$", re.MULTILINE)


def status_of(text):
    """The `status:` from an artifact's metadata block, whatever its dialect.

    Skills carry frontmatter and everything else a fenced yaml block; both put
    `status:` at the start of a line, so one pattern reads both.
    """
    match = STATUS_LINE.search(text or "")
    if match is None or match.group(1) not in STATUSES:
        return None
    return match.group(1)


def show(root, ref, rel):
    """A file's contents at `ref`, or None if it did not exist there."""
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{ref}:{rel}"],
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else None


def artifact_paths(root):
    for pattern in ARTIFACT_GLOBS:
        for path in sorted(root.glob(pattern)):
            # A README inside an artifact directory is documentation about the
            # directory, not an artifact -- validate_repo.py skips it too.
            if path.name == "README.md":
                continue
            yield path.relative_to(root).as_posix()


def check(root, base):
    findings = []
    for rel in artifact_paths(root):
        before = status_of(show(root, base, rel))
        if before is None:
            continue  # new artifact, or none declared at base -- no transition
        after = status_of((root / rel).read_text())
        if after is None or after == before:
            continue
        if (before, after) not in ALLOWED:
            findings.append((rel, before, after))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument(
        "--base",
        default="origin/main",
        help="the ref to compare against (default: origin/main)",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()

    try:
        findings = check(root, args.base)
    except FileNotFoundError:
        print("git is not available", file=sys.stderr)
        return 2

    for rel, before, after in findings:
        allowed = ", ".join(f"{a} -> {b}" for a, b in sorted(ALLOWED) if a == before)
        print(f"{rel}: {before} -> {after} is not an allowed transition")
        print(f"    from {before}, the lifecycle allows: {allowed or '(nothing)'}")

    total = len(list(artifact_paths(root)))
    print(f"\n{total} artifacts checked against {args.base}, {len(findings)} invalid")
    print("FAIL" if findings else "PASS")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
