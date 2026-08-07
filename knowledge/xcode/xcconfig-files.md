# xcconfig Files

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.xcconfig-files
artifact_type: knowledge
title: xcconfig Files
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct authoring and attachment of .xcconfig build configuration files, and how xcconfig-supplied values interact with Build Settings UI values.
domain: Xcode
tags:
  - xcode
  - xcconfig
  - build-settings
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev745c5c974.html
  - https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project
depends_on: []
related:
  - knowledge.xcode.build-configurations
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent authors and attaches an
`.xcconfig` file so its values compose correctly with values Xcode or
another `.xcconfig` file already set, instead of silently overwriting
them.

## Scope

### Included

-   `.xcconfig` syntax: `KEY = value`, `$(inherited)`, `#include`/`#include?`
-   Attaching an `.xcconfig` file to a project or target configuration
-   Precedence between an `.xcconfig` value and a Build Settings UI value for the same key

### Excluded

-   Build configuration lifecycle itself (Debug/Release/custom) — see `build-configurations`
-   Where a given build setting is documented/what it controls — see `build-configurations`

## Rules

### Rule 1

Agents MUST include `$(inherited)` when appending to a settings key that
Xcode or a base `.xcconfig` also populates (e.g. `OTHER_SWIFT_FLAGS`,
`HEADER_SEARCH_PATHS`) — omitting it replaces the base value instead of
extending it, silently dropping flags another layer already set.

### Rule 2

Agents MUST use `#include "Base.xcconfig"` (a relative path) to share
settings across multiple configuration files rather than duplicating
key-value pairs across them — duplicated values drift out of sync the
first time one copy is edited and the other isn't.

### Rule 3

Agents MUST NOT assume an `.xcconfig` value overrides an explicit Build
Settings UI value for the same key at the same level — the reverse is
true: an explicit UI-entered value always wins over the xcconfig-supplied
value; the xcconfig value only takes effect where the UI field is left
blank.

### Rule 4

Agents SHOULD store environment-specific secrets (API keys, tokens) as
values in an `.xcconfig` file excluded from version control, included
via the optional-include syntax (`#include? "Secrets.xcconfig"`) rather
than committing them in a tracked file or hardcoding them in Swift — the
`?` makes the include a no-op (not a build error) when the file is
absent, e.g. on a fresh clone or CI checkout before secrets are
provisioned.

## Compliant Example

```
// Config.xcconfig
#include "Base.xcconfig"
#include? "Secrets.xcconfig"

OTHER_SWIFT_FLAGS = $(inherited) -DFEATURE_FLAG_X
API_BASE_URL = https://api.example.com
```
Extends `OTHER_SWIFT_FLAGS` with `$(inherited)` instead of replacing it, shares common settings via `#include`, and pulls secrets from an optional, untracked file via `#include?`. (Rules 1, 2, 4)

## Non-Compliant Example

```
// Config.xcconfig
OTHER_SWIFT_FLAGS = -DFEATURE_FLAG_X
```
Overwrites any `OTHER_SWIFT_FLAGS` value Xcode or a base `.xcconfig` already set instead of extending it — `$(inherited)` is omitted. (Rule 1)

## Dependencies

None.

## References

-   [Apple — Configuration Settings File (.xcconfig) format](https://help.apple.com/xcode/mac/current/en.lproj/dev745c5c974.html)
-   [Apple Developer — Adding a build configuration file to your project](https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project)
