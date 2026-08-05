# Pickers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.pickers
type: knowledge
title: Pickers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for choosing and configuring pickers versus other selection controls on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - pickers
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/pickers
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.human-interface-guidelines.lists-and-tables
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use a picker
rather than another selection control on iOS/iPadOS, and conventions
for value ordering, in-context presentation, and date/time picker
style/granularity.

## Scope

### Included

-   Picker vs. segmented control vs. list-with-index decision
-   Value ordering predictability
-   In-context (inline/popover) presentation
-   Compact date-picker style for constrained space
-   Minute-interval granularity for time pickers

### Excluded

-   SwiftUI `Picker`/`DatePicker` or UIKit `UIPickerView`/`UIDatePicker` implementation — see `swiftui`/`uikit` domains
-   Picker item copy wording — see `style-guide`

## Rules

### Rule 1

Agents SHOULD use a picker for medium-to-long lists of selectable
values, preferring a smaller control (such as a segmented control) for
very short option sets, and a list/table with an index for very large
sets.

### Rule 2

Agents MUST order picker values predictably (for example,
alphabetically or chronologically) so people can anticipate hidden
values before interacting.

### Rule 3

Agents SHOULD present a picker in context — inline or in a popover near
the field it edits — rather than navigating to a separate screen to
show it.

### Rule 4

Agents MUST use the compact date-picker style when screen space is
constrained, opening a modal editor only on demand rather than
consuming persistent space.

### Rule 5

Agents SHOULD allow a coarser minute interval in a date/time picker
(any divisor of 60, such as 15-minute steps) instead of always
requiring all 60 discrete minute values, when fine-grained precision
isn't needed.

## Compliant Example

-   ✓ A country picker lists countries in alphabetical order matching device locale. (Rule 2)
-   ✓ A time picker offers 15-minute increments for a scheduling feature that doesn't need per-minute precision. (Rule 5)

## Non-Compliant Example

-   ✗ A picker with unordered, randomly arranged values makes it hard to predict where a value is. (Rule 2)
-   ✗ Selecting a date pushes to an entirely new screen instead of showing an inline/popover picker. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)
