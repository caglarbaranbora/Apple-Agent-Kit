# Apple Agent Kit

**Installs the Apple Agent Kit Claude Code plugin — turns Apple's official docs into Skills your coding agent routes to instead of guessing platform conventions.**

[![npm version](https://img.shields.io/npm/v/apple-agent-kit)](https://www.npmjs.com/package/apple-agent-kit)
[![License](https://img.shields.io/badge/license-PolyForm%20Strict-blue)](https://github.com/caglarbaranbora/Apple-Agent-Kit/blob/main/LICENSE)

Status: Stable
Version: 2.4.0

## Install

```bash
npx apple-agent-kit
```

Adds the Apple Agent Kit repository as a Claude Code plugin marketplace and
installs the `apple-agent-kit` plugin. Requires the `claude` CLI to already be
installed.

## Codex CLI

If `claude` isn't found but `codex` is, this installer prints Codex install
instructions instead of erroring — it never runs `codex` itself, since a
plugin install there is interactive. Manual steps:
https://github.com/caglarbaranbora/Apple-Agent-Kit/blob/main/.codex/INSTALL.md

## What you get

34 Skills across Apple's SDKs (SwiftUI, UIKit, StoreKit, WidgetKit, App
Intents, HIG, and more), each routing deterministically to small, traceable
Knowledge Contracts sourced from Apple's own documentation — no repo-wide
semantic search. Full pitch, an example of a Skill routing in action, and the
complete Skill/Workflow catalogue:
https://github.com/caglarbaranbora/Apple-Agent-Kit#readme

## License

Source-available under the PolyForm Strict License 1.0.0 — you may use it, not
redistribute or resell it:
https://github.com/caglarbaranbora/Apple-Agent-Kit/blob/main/LICENSE
