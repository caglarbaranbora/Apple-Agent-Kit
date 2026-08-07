# Lists and Tables

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.lists-and-tables
artifact_type: knowledge
title: Lists and Tables
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for structuring list and table rows, columns, selection feedback, and edit-mode gating on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - lists-and-tables
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
depends_on: []
related:
  - knowledge.human-interface-guidelines.typography
  - knowledge.human-interface-guidelines.layout
  - knowledge.accessibility.voiceover-navigation-order
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent structures list and table
content on iOS/iPadOS: row/column content conventions, edit-mode gating
for selection and reordering, selection feedback, and disclosure/info
control usage.

## Scope

### Included

-   List vs. table vs. grid selection for a given content type
-   Row and column content/text conventions
-   Edit-mode gating for select/reorder/delete
-   Selection feedback conventions (persistent vs. transient highlight)
-   Info button vs. disclosure indicator usage in rows

### Excluded

-   SwiftUI `List`/`Table` or UIKit `UITableView`/`UICollectionView`
    implementation — see `swiftui`/`uikit` domains
-   VoiceOver row announcement mechanics — see `accessibility` domain
-   Row/header copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST keep row/item text succinct to minimize truncation and
wrapping, keeping rows comfortable to scan and read.

### Rule 2

Agents SHOULD preserve readability of text that would otherwise be
clipped in a narrow table — for example, truncating in the middle of a
string rather than the end when that keeps both the start and end of
the content recognizable.

### Rule 3

Agents MUST use descriptive, noun-phrase column headings (no ending
punctuation) in a multicolumn table, and MUST provide a label or
header for context when a single-column table view has no visible
column heading.

### Rule 4

Agents MUST require people to enter an explicit edit mode before they
can select, reorder, add, or delete rows in an iOS/iPadOS list or
table.

### Rule 5

Agents MUST choose selection feedback appropriate to purpose:
persistently highlight the selected row when the list/table supports
hierarchical navigation; use a brief highlight plus a state indicator
(such as a checkmark) when the row toggles an option rather than
navigating.

### Rule 6

Agents MUST NOT use an info/detail-disclosure button to support
navigation into a row's subviews — use it only to reveal more
information about the row's content; use a disclosure indicator
accessory control for drill-down navigation.

### Rule 7

Agents SHOULD prefer a list or table for primarily text-based,
scannable content, and prefer a grid instead when items vary widely in
size or the content is mostly images.

## Compliant Example

-   ✓ A Settings-style list enters edit mode before showing reordering handles and delete controls. (Rule 4)
-   ✓ A hierarchy-navigation list keeps the tapped row highlighted while its detail view is shown. (Rule 5)
-   ✓ A multicolumn productivity table labels each column with a short noun phrase like "Date" and "Amount." (Rule 3)

## Non-Compliant Example

-   ✗ Rows can be reordered and deleted directly from the default (non-edit) list state. (Rule 4)
-   ✗ A row's info button is wired to push a new hierarchy screen instead of showing more detail about that row. (Rule 6)
-   ✗ Table rows contain multiple long, unbounded paragraphs of body text with no truncation strategy. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Lists and Tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
