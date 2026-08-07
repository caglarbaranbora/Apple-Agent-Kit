# Template Specification

Status: Approved
Version: 1.0.0

## Purpose

Defines the standard templates used when authoring new artifacts.

Templates are an **authoring aid, not an architectural layer** — the same category as
`scripts/`. An agent never loads a template to perform an Apple development task, and
nothing depends on one at runtime. The four layers are References → Knowledge → Skills
→ Workflows; see ../architecture.md [[architecture]].

## Relationship to the specifications

Each artifact type's specification is the authority on its required metadata and
sections. A template is a convenience copy of that structure, never a second source of
truth. Where a template and its specification disagree, the specification wins and the
template is a defect.

| Artifact type | Authority |
|---|---|
| Knowledge Contract | knowledge-spec.md [[knowledge-spec]] |
| Skill | skill-spec.md [[skill-spec]] |
| Reference | reference-spec.md [[reference-spec]] |
| Workflow | workflow-spec.md [[workflow-spec]] |

## Available Templates

| Template | Status |
|---|---|
| `templates/knowledge-contract.md` | Present |
| Skill | Not built — use skill-spec.md's Required Metadata and Required Sections |
| Reference | Not built — use reference-spec.md |
| Workflow | Not built — use workflow-spec.md |
| Validation Report | Not built |

Templates are written on demand. An unbuilt template is not a gap, because the
governing specification already states the full structure.

## General Requirements

Every template MUST:

- Carry the metadata block its specification requires.
- Follow that specification's section order.
- Be human-readable and AI-parseable.
- Use Markdown only.
- Avoid unnecessary prose.

## Metadata Standard

Templates do not define a metadata standard. The common base and per-type extensions
live in ../../schemas/metadata.schema.md [[metadata.schema]].

## Naming Rules

- Filenames use lowercase kebab-case.
- One artifact per file.
- Names describe responsibility, not implementation.

## Validation Checklist

- Template matches its governing specification exactly
- Section order correct
- Naming convention followed
- Links resolve
