# Settings

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.settings
type: knowledge
title: Settings
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for where a setting belongs — the system Settings app, a custom in-app settings area, or inline with the task it affects — on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - settings
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/settings
depends_on: []
related:
  - knowledge.human-interface-guidelines.privacy
  - knowledge.human-interface-guidelines.onboarding
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent decides where a given
setting belongs on iOS/iPadOS — inline with the task, in a custom
in-app settings area, or in the system-provided Settings app — and
how to avoid duplicating systemwide options.

## Scope

### Included

-   Choosing between task-inline options, a custom settings area, and the system Settings app
-   Default-value selection to minimize required configuration
-   Avoiding duplication of systemwide/global options
-   Avoiding settings for information the app can detect automatically
-   Deciding what belongs in the system-provided Settings app

### Excluded

-   Settings screen implementation code
-   Settings label/copy wording — see `style-guide`
-   Per-app permission toggle mechanics — see `privacy`
-   macOS settings-window and watchOS-specific patterns (out of scope for this iOS/iPadOS contract)

## Rules

### Rule 1

Agents MUST place task-specific, frequently adjusted options (e.g.,
showing/hiding parts of a view, reordering items, filtering a list)
within the screen or task they affect, not in a separate settings
area.

### Rule 2

Agents SHOULD reserve a custom in-app settings area for general,
infrequently changed options that affect the overall app experience
(e.g., interface style, save behavior, account details).

### Rule 3

Agents MUST NOT duplicate systemwide options — such as accessibility
accommodations, scrolling behavior, or authentication methods —
inside a custom settings area; read and respect the system-level
value instead.

### Rule 4

Agents MUST choose default settings that give the best experience to
the largest number of people, so most people never need to open a
settings area at all.

### Rule 5

Agents SHOULD minimize the total number of settings exposed, since
too many settings make an app feel less approachable and make any
one setting harder to find.

### Rule 6

Agents MUST NOT ask people to manually configure something the app
can detect automatically (e.g., a connected controller, the current
Dark Mode state).

### Rule 7

Agents SHOULD add an option to the system-provided Settings app only
when it is among the most rarely changed options, and SHOULD provide
a button within the app that opens that system Settings entry
directly when doing so.

## Compliant Example

-   ✓ A reading app's font size and view-density controls live inline in the reading view, not in a separate settings screen. (Rule 1)
-   ✓ An app's custom settings area omits a "Reduce Motion" toggle and instead reads the system-wide accessibility setting. (Rule 3)
-   ✓ A game auto-detects a connected controller instead of asking the player to select one. (Rule 6)

## Non-Compliant Example

-   ✗ Changing a list's sort order requires leaving the list and opening a separate settings screen. (Rule 1)
-   ✗ A custom in-app "Contrast" toggle duplicates the system's Increase Contrast accessibility setting. (Rule 3)
-   ✗ The settings area has dozens of rarely used toggles with no clear default behavior. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Settings](https://developer.apple.com/design/human-interface-guidelines/settings)
