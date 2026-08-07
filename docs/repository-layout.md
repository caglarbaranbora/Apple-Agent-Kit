# Repository Layout

Status: Approved
Version: 1.0.0

## Layers

The four architectural layers, in dependency order:

- `references/`: official Apple source mapping — the index of authority
- `knowledge/`: Knowledge Contracts — atomic implementation rules
- `skills/`: dispatchers — route a task to the Knowledge it needs
- `workflows/`: compose multiple Skills into one end-to-end task

## Supporting Directories

Not layers. Nothing depends on these at runtime.

- `docs/`: architecture, specifications, foundation documents, contributing guides,
  and dated design records under `docs/superpowers/`
- `schemas/`: the shared metadata schema
- `templates/`: authoring templates
- `scripts/`: validation tooling
- `tests/`: tests for that tooling
- `validation/`: vertical slices and findings
- `rfcs/`: architecture proposals

## Plugin Packaging

- `.claude-plugin/`: plugin and marketplace manifests
- `npx/`: the thin installer published to npm
- `skills/apple-agent-kit/SKILL.md`: the `entry` artifact — the plugin entry point
  Claude Code discovers first

See architecture.md [[architecture]].
