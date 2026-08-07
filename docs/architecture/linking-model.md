# Linking Model

Status: Approved
Version: 1.0.0

## Purpose

Define how artifacts reference each other throughout the repository.

## Goals

- Deterministic navigation
- Stable references that survive file moves
- Obsidian compatibility
- Tool-agnostic parsing

## Three Conventions

There is no single canonical link mechanism. Three conventions exist, each with a
distinct job, and each is authoritative for its own job.

### 1. Metadata edges — artifact IDs

The dependency graph's source of truth. `depends_on`, `related`, and `routes` all name
artifacts by id, never by path.

```yaml
depends_on:
  - knowledge.localization.string-catalogs-and-extraction
routes: [knowledge.swiftui.view-identity, knowledge.swiftui.modifier-order]
```

Ids are immutable (../../schemas/metadata.schema.md [[metadata.schema]]), which is
exactly why ids and not paths carry the graph: a moved or renamed file does not break
an id.

### 2. Reference `## Used By` — wiki links

A Reference lists the Knowledge Contracts that cite it as wiki links:

```md
- [[knowledge/localization/localized-string-apis]]
```

This repository is maintained in an Obsidian vault, where wiki links are functional
navigation rather than decoration. A wiki link here stands alone; it does not need a
mirroring relative path.

### 3. Document prose — relative paths

Governance documents under `docs/` link each other with relative Markdown paths, with
an optional wiki link alongside for Obsidian:

```md
See: ../glossary.md
[[glossary]]
```

Artifacts (`knowledge/`, `skills/`, `references/`, `workflows/`) use no relative-path
links between each other. Their relationships are metadata edges.

## Rules

- An artifact relationship MUST be expressed as a metadata edge, never as a prose link.
- A prose link MUST NOT be the only record of a dependency.
- Never reference an artifact by title alone.
- Prefer linking to a file rather than a directory.
- Broken links are validation failures, in all three conventions.

## Cross-Layer Linking

Governs `depends_on`. See ../architecture/dependency-graph.md [[dependency-graph]] for
the full tables.

**Allowed:** Workflow → Skill · Skill → Knowledge · Knowledge → Knowledge ·
Knowledge → Reference · Specification → Specification

**Forbidden:** Knowledge → Skill · Knowledge → Workflow · Skill → Skill ·
Workflow → Knowledge · circular navigation used as a dependency

A Skill's `related` naming another Skill is legal and widespread. It is a
cross-reference, not a dependency.

## Reference-to-Knowledge Is Many-to-Many

A Reference's `## Used By` may name Contracts from more than one domain, and a domain's
Contracts may be indexed by more than one Reference.

Both happen today: the three `human-interface-guidelines*` References share one
Knowledge directory, and `references/apple/style-guide.md` is legitimately cited by
Contracts outside `knowledge/style-guide/`.

**A validator MUST NOT derive this relationship from directory names.** A
directory-derived check reports false positives on both cases.

## Validation

Enforced by `scripts/validate_repo.py`; see ../validation-model.md [[validation-model]].

- Every metadata-edge id resolves to an existing artifact
- Every wiki-link target resolves
- Every relative path resolves
- Artifact ids are unique
- No orphaned artifacts
