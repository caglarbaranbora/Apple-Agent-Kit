# Status and Progress Indicators

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.status-and-progress-indicators
artifact_type: knowledge
title: Status and Progress Indicators
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the correct terms for progress indicators, progress bars, badges, and the alphabetical index column, and when developer-specific subtypes may be named.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - status-and-progress-indicators
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.input-controls
  - knowledge.style-guide.general-button-labels
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent names onscreen elements that
communicate process status or list position — progress indicators,
badges, and the index column — in UI text and documentation for Apple
platforms.

## Scope

### Included

-   The generic term "progress indicator" and its developer-materials subtypes
-   Naming badges and the three ways they're used (counter, type/state indicator, warning)
-   Naming the alphabetical index column in iOS list views

### Excluded

-   Dialogs, sheets, alerts, and other presentation surfaces (see `presentation-surfaces`)
-   Input controls such as checkboxes, sliders, and steppers (see `input-controls`)
-   General rules for referring to and quoting button names (see `general-button-labels`)

## Rules

### Rule 1

Agents MUST use "progress indicator" as the generic term, in user
materials, for an onscreen element that lets users know a process is
taking place, and MUST describe what it looks like when first mentioned
(for example, "A progress indicator (a spinning striped cylinder)...").

### Rule 2

Agents MUST use "determinate progress bar," in developer materials only,
for the progress bar that fills from left to right when the amount of
work completed is known. In user materials, agents MUST use "progress
indicator" and describe it as "a moving bar."

### Rule 3

Agents MUST use "indeterminate progress bar," in developer materials
only, for the spinning striped cylinder shown when a process's duration
can't be determined. In user materials, agents MUST use "progress
indicator" and describe it as "a spinning striped cylinder."

### Rule 4

Agents MUST use "asynchronous progress indicator," in developer materials
only, for the spinning-gear indicator, and MUST NOT use it for a process
that starts indeterminate but could become determinate. In user
materials, agents MUST use "progress indicator" and describe it as "a
spinning gear."

### Rule 5

Agents MUST use "badge (n.)" for a small icon, or small graphic with
text, that overlays an app/toolbar icon, a file thumbnail, or another UI
element — as a counter, an indicator of an item's type or state, or a
warning. Agents MUST NOT use "badge" as a verb or "badged" as an
adjective.

### Rule 6

Agents MUST use "index" for the vertical column of letters at the right
side of a list in iOS apps, and MUST use "indexes," not "indices," as its
plural unless referring to mathematical indices.

## Compliant Example

-   ✓ "A progress indicator (a spinning striped cylinder) lets you know that a process is taking place." (Rule 1)
-   ✓ Developer materials: "Use a determinate progress bar when you can tell the user how much of a process has been completed." (Rule 2)
-   ✓ User materials: "A progress indicator (a moving bar) shows the status of the download." (Rule 2)
-   ✓ Developer materials: "the indeterminate progress bar for the spinning striped cylinder" (Rule 3)
-   ✓ "A progress indicator (looks like a spinning gear) appears." (Rule 4)
-   ✓ "A badge indicates the number of unread messages." (Rule 5)
-   ✓ "Tap a letter in the index to jump to that section." (Rule 6)

## Non-Compliant Example

-   ✗ "A progress bar appears." with no description, in user materials (Rule 1)
-   ✗ "A determinate progress bar shows the download status." in user materials (Rule 2)
-   ✗ "An indeterminate progress bar appears." in user materials (Rule 3)
-   ✗ "An asynchronous progress indicator appears." for a process that could become determinate (Rule 4)
-   ✗ "The icon is badged with a warning." (Rule 5)
-   ✗ "Tap a letter in the alphabet list." meaning the index (Rule 6)

## Dependencies

None.

## References

-   [Apple Style Guide — progress indicator (p. 169)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — determinate progress bar (p. 65)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — indeterminate progress bar (p. 110)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — asynchronous progress indicator (p. 33)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — badge (n.) (pp. 36–37)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — index; indexes (p. 110)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
