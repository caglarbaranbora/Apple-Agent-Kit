# Text Fields

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.text-fields
type: knowledge
title: Text Fields
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for sizing, spacing, validating, and securing single-line text field input on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - text-fields
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/text-fields
depends_on: []
related:
  - knowledge.style-guide.authentication-credentials-and-biometrics
  - knowledge.human-interface-guidelines.layout
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent sizes, spaces, validates,
and secures text field input on iOS/iPadOS for short, specific pieces
of text such as names, emails, or passwords.

## Scope

### Included

-   Field sizing relative to expected input length
-   Secure text field usage for sensitive data
-   Placeholder/label pairing
-   Multi-field form spacing and consistency
-   Validation timing
-   iOS/iPadOS Clear button and leading/trailing accessory placement

### Excluded

-   SwiftUI `TextField`/UIKit `UITextField` implementation — see `swiftui`/`uikit` domains
-   Placeholder/label copy wording — see `style-guide`
-   Dynamic Type scaling API — see `accessibility` domain

## Rules

### Rule 1

Agents MUST size a text field to roughly match the expected quantity
of input text, so its size visually communicates how much information
to provide.

### Rule 2

Agents MUST use a secure text field for sensitive input such as
passwords.

### Rule 3

Agents SHOULD provide placeholder/hint text describing a field's
purpose, and pair it with a persistent label when the placeholder
alone won't be remembered once typing starts, since placeholder text
disappears on input.

### Rule 4

Agents MUST evenly space and consistently size multiple text fields in
a form so each field is clearly associated with its label, stacking
fields vertically where possible.

### Rule 5

Agents SHOULD validate input at a contextually appropriate time — for
example, when focus leaves the field for something like an email
address, but before advancing for values like a chosen username or
password — and clearly communicate invalid input.

### Rule 6

Agents MUST show a Clear button at the trailing end of a text field to
let people erase input without repeated deletions.

### Rule 7

Agents SHOULD reserve the leading end of a text field for
purpose-indicating imagery and the trailing end for supplementary
actions (such as bookmarking).

## Compliant Example

-   ✓ A password field renders as a secure field and hides entered characters. (Rule 2)
-   ✓ An email field validates format only after the person moves to the next field, not on every keystroke. (Rule 5)
-   ✓ A one-line name field is sized for a short name, not full-paragraph width. (Rule 1)

## Non-Compliant Example

-   ✗ A password field displays entered characters in plain text. (Rule 2)
-   ✗ A short numeric field is drawn wide enough for a paragraph of text. (Rule 1)
-   ✗ Multiple fields in a form are inconsistently sized and spaced so labels are ambiguous. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Text Fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
