# Punctuation and Typography in Text

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.punctuation-and-typography-in-text
type: knowledge
title: Punctuation and Typography in Text
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines punctuation and typography conventions in running UI text — ampersand usage, exclamation points, ellipsis, and the correct terms for typeface, type size, and type style.
domain: Style Guide
tags:
  - style-guide
  - punctuation
  - typography
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.capitalization-style-rules
  - knowledge.style-guide.units-of-measure
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent uses the ampersand, exclamation
points, and the ellipsis character, and which terms to use for font-related
typography, when writing running UI text and documentation for Apple
platforms.

## Scope

### Included

-   When the ampersand character is permitted in running text
-   Tone guidance for exclamation points in promotional vs. documentation text
-   Formatting and running-text usage of the ellipsis character
-   Correct terms for typeface, type size, and type style

### Excluded

-   General capitalization style (see `capitalization-style-rules`)
-   Numeric and unit-of-measure punctuation, such as decimal points in units (see `units-of-measure`)

## Rules

### Rule 1

Agents MUST use the ampersand character (&) in running text only when
referring to onscreen elements, document titles, or other items that
actually contain the character (e.g., "Choose Insert > Date & Time"). In
all other cases, agents MUST spell out "and."

### Rule 2

Agents MAY use exclamation points occasionally in promotional text and
dialogue, but MUST avoid them in documentation.

### Rule 3

Agents MUST render an ellipsis as a single ellipsis character (not three
separate periods) to prevent line breaks between the dots. If the onscreen
name of a menu item or button ends with an ellipsis, agents MUST NOT include
the ellipsis when referring to that name in running text.

### Rule 4

Agents MUST NOT use "typeface," "type size," or "type style." Agents MUST
use "font" instead of "typeface," "size" or "font size" instead of "type
size," and "style" or "font style" instead of "type style."

## Compliant Example

-   ✓ "Choose Insert > Date & Time." (Rule 1)
-   ✓ "Discover amazing new features!" in promotional copy (Rule 2)
-   ✓ "Choose File > New and click a template." for a menu item named "New…" onscreen (Rule 3)
-   ✓ "Change the font and size of the selected text." (Rule 4)

## Non-Compliant Example

-   ✗ "Photos & Videos" used generically instead of "Photos and Videos" (Rule 1)
-   ✗ "Your download is complete!" in a reference manual (Rule 2)
-   ✗ "Choose File > New… and click a template." including the onscreen ellipsis in running text (Rule 3)
-   ✗ "Change the typeface and type size of the selected text." (Rule 4)

## Dependencies

None.

## References

-   [Apple Style Guide — ampersand (p. 19)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — exclamation points (p. 83)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — ellipsis (p. 79)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — typeface; type size; type style (p. 209)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
