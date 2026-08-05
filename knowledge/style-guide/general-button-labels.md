# General Button Labels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.general-button-labels
type: knowledge
title: General Button Labels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines general-purpose rules for referring to buttons, quoting or not quoting their labels, and wording for common labels like OK and Allow.
domain: Style Guide
tags:
  - style-guide
  - ui-text
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.authentication.button-labels
  - knowledge.style-guide.app-state-and-error-terminology
  - knowledge.style-guide.authentication-credentials-and-biometrics
  - knowledge.style-guide.capitalization-style-rules
  - knowledge.style-guide.input-controls
  - knowledge.style-guide.instructional-voice-and-phrasing
  - knowledge.style-guide.navigation-controls
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.sign-in-and-authentication-terminology
  - knowledge.style-guide.status-and-progress-indicators
  - knowledge.style-guide.ui-action-verbs
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent refers to buttons and writes
their labels in documentation and UI text: when a button name needs
quotation marks, how to name icon-only buttons, and the correct wording
for common generic labels (OK, user name field, allow-style permission
copy). It is domain-general and not specific to sign-in flows.

## Scope

### Included

-   Referring to and quoting button names in running text
-   Naming icon-only or image-only buttons
-   Correct spelling of "OK"
-   Two-word spelling of "user name"
-   Avoiding "allow" as a verb where a reader-focused rewrite is possible

### Excluded

-   Sign-in, sign-out, and authentication-specific button/label wording (see `sign-in-and-authentication-terminology`)
-   Passkey, password, and biometric terminology (see `authentication-credentials-and-biometrics`)
-   The definitions of "sentence-style" and "title-style" capitalization used
    in Rule 1 (see `capitalization-style-rules`)

## Rules

### Rule 1

Agents MUST write the names of buttons exactly as they appear onscreen. If
a button's label uses sentence-style capitalization, agents MUST enclose
the label in quotation marks in running text (Click the "Position on
screen" button). If the label uses title-style capitalization, agents MUST
NOT enclose it in quotation marks, even if one word in it is lowercase
(Tap Add to Favorites). If a button's onscreen label is in all caps or all
lowercase, agents MUST render it in title-style capitalization when
writing about it.

### Rule 2

Agents MUST call any interface element that initiates an action when
clicked or tapped a "button," even if it displays only an icon or image
rather than text, EXCEPT app icons in the Dock or on the Home Screen,
which MUST still be called "icons" even though they act like buttons
(Click the Safari icon in the Dock).

### Rule 3

Agents MUST spell the affirmative dialog label as "OK," never "okay."

### Rule 4

Agents MUST write "user name" as two words, not "username" or "user-name."

### Rule 5

Agents SHOULD avoid using "allow" as a verb when a sentence can be
restructured to make the reader the subject instead of the product (You
can create a database with FileMaker Pro, rather than FileMaker Pro allows
you to create a database). This does not apply to permission-prompt copy
that names an "Allow" button itself, which MUST follow Rule 1.

## Compliant Example

-   ✓ Click the "Position on screen" button. (Rule 1)
-   ✓ Tap Add to Favorites. (Rule 1)
-   ✓ Click the Safari icon in the Dock. (Rule 2)
-   ✓ OK (Rule 3)
-   ✓ user name (Rule 4)
-   ✓ You can create a database with FileMaker Pro. (Rule 5)

## Non-Compliant Example

-   ✗ Click the Position on screen button. missing quotation marks (Rule 1)
-   ✗ Tap "Add to Favorites." unnecessary quotation marks on a title-style label (Rule 1)
-   ✗ Click the Safari button in the Dock. calling a Dock icon a button (Rule 2)
-   ✗ Okay (Rule 3)
-   ✗ username / user-name (Rule 4)
-   ✗ FileMaker Pro allows you to create a database. (Rule 5)

## Dependencies

None.

## References

-   [Apple Style Guide — button (p. 43)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — OK (p. 151)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — user name (p. 212)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — allow (p. 18)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
