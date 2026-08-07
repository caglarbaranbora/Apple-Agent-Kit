# Documentation Style

Status: Approved
Version: 1.0.0

## Writing

- Write in English.
- Use RFC-style language.
- Prefer MUST/SHOULD/MAY.
- Be concise.
- Explain rationale.
- Avoid marketing language.
- Optimize for AI agents.
- Prefer examples over prose.

## Document Header

Every governance document under `docs/`, `schemas/`, and `templates/` opens with a
title, then status and version on **two separate lines**:

```md
# Document Title

Status: Approved
Version: 1.0.0
```

`Status` is one of the four lifecycle states in artifact-lifecycle.md
[[artifact-lifecycle]]. Do not invent status values, and do not put status and version
on one line.

Documents outside that lifecycle — design records under `docs/superpowers/`, reports
under `validation/` — describe their own state freely; they record history rather than
state live rules.

## Cross-References

Link with a relative Markdown path, optionally followed by a wiki link for Obsidian:

```md
See: ../glossary.md
[[glossary]]
```

Artifacts under `knowledge/`, `skills/`, `references/`, and `workflows/` do not link
each other in prose — their relationships are metadata edges. See
../architecture/linking-model.md [[linking-model]].
