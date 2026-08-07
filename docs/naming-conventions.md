# Naming Conventions

Status: Approved
Version: 1.0.0

## Purpose

Define naming rules for repository artifacts to ensure consistency, discoverability,
and deterministic routing.

## General Rules

- Use lowercase.
- Use kebab-case for file names.
- Use descriptive names that state the artifact's responsibility.
- Avoid abbreviations unless universally recognized.
- A directory that holds a collection is plural (`knowledge/`, `skills/`,
  `references/`, `workflows/`). An artifact filename names its topic in whatever
  number reads naturally — `accessibility-labels.md` and `relationships-and-delete-rules.md`
  are both correct.

## Repository Naming

    docs/          architecture.md, routing-model.md
    knowledge/     <domain>/<slug>.md
    skills/        <domain>[-<facet>]/SKILL.md
    workflows/     <slug>/WORKFLOW.md
    references/    apple/<domain>.md
    templates/     knowledge-contract.md

Skill directories are always flat; see specifications/skill-spec.md [[skill-spec]].

## Artifact IDs

Pattern: `<type>.<scope>.<name>`

    knowledge.localization.localized-string-apis
    skill.swiftui.interaction
    reference.apple.networking
    workflow.app-store-submission
    entry.apple-agent-kit
    template.knowledge.contract

A `workflow` id has no domain segment — a Workflow spans domains. An `entry` id has
none either.

Ids MUST be unique, MUST agree with the artifact's path, and MUST be immutable. An
artifact is never renamed for consistency; it is retired and replaced.

## Domain Names

Use official Apple terminology wherever possible: SwiftUI, StoreKit, Accessibility,
WidgetKit.

Directory names remain lowercase kebab-case: `swiftui/`, `storekit/`,
`accessibility/`, `app-store-review-guidelines/`.

The `domain` metadata field MUST agree with the directory name, case-insensitively and
with spaces as hyphens.

## Versioning

Semantic Versioning.

- `0.x.y` — Draft
- `1.0.0` — established on first approval
- `1.1.0` — backward-compatible additions
- `2.0.0` — breaking changes

## Reserved Names

Not permitted as **artifact filenames**:

    temp  misc  test  new  final  copy

This restricts artifact names only. Tooling directories such as `tests/` and
`scripts/` are unaffected.

## Validation

Enforced as Validation Levels 1-2 by `scripts/validate_artifact.py` and
`scripts/validate_repo.py`; see validation-model.md [[validation-model]].

- File name format
- ID uniqueness
- ID / path agreement
- Domain / directory agreement
- Version format
