# Navigation Controls

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.navigation-controls
artifact_type: knowledge
title: Navigation Controls
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the correct terms for named navigation buttons and controls — Back, More, Help, and disclosure elements — used to move between screens or reveal more content.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - navigation-controls
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.input-controls
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.touch-gesture-verbs
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent names specific navigation
buttons and controls — the Back button, More button/menu, Help button,
disclosure arrow/button, and up arrow — in UI text and documentation for
Apple platforms.

## Scope

### Included

-   Naming the Back button and the button/menu labeled with an ellipsis
-   Naming the Help button and the discouraged "question-mark button" term
-   Distinguishing disclosure arrow from disclosure button
-   Naming the up arrow used with a stepper control

### Excluded

-   Left arrow, right arrow, Forward button, and arrow keys (not requested for this contract)
-   Stepper and other input controls the up arrow can accompany (see `input-controls`)
-   General rules for referring to and quoting button names (see `general-button-labels`)
-   Presentation surfaces such as menus and sheets (see `presentation-surfaces`)
-   Sign-in and sign-out button wording (see `sign-in-and-authentication-terminology`)

## Rules

### Rule 1

Agents MUST use "Back button" to refer to a button — usually in a toolbar
or navigation bar — that lets users return to the previous screen or
webpage.

### Rule 2

Agents MUST use "More button" for a button labeled with an ellipsis
(circled or not), and "More menu" for the menu of options that button
opens. Agents MUST use an app-specific name instead when one exists (for
example, the View Options button in Mail on Mac).

### Rule 3

Agents MUST NOT use "question-mark button"; use "Help button" — a button
that opens help content for an app and displays a question-mark graphic.

### Rule 4

Agents MUST use "disclosure arrow" for a button that reveals or hides
options when clicked, and MUST NOT call it a "disclosure button." Agents
SHOULD NOT mention whether the arrow is closed (pointing right) or open
(pointing down) unless necessary. In developer materials, agents MAY use
"disclosure triangle" instead.

### Rule 5

Agents MUST use "disclosure button" for a button containing an arrow that
expands a dialog or utility window to reveal choices tied to a specific
list-based selection control (the arrow points down when closed and up
after the window expands), and MUST NOT conflate it with "disclosure
arrow."

### Rule 6

Agents MUST use "up arrow" for the small arrow that users click to
increase a value in a stepper control, and MUST NOT call it "the stepper"
or "the increment button." This rule names the arrow; naming the control
the arrow belongs to is `input-controls` Rule 5, which permits "stepper"
in developer materials and where referring to the control is unavoidable.

## Compliant Example

-   ✓ "Use the Back button to return to the previous screen." (Rule 1)
-   ✓ "Tap the More button, and then choose Show Completed." (Rule 2)
-   ✓ "Click the Help button to open help content for this app." (Rule 3)
-   ✓ "Click the disclosure arrow to reveal more information." (Rule 4)
-   ✓ "When the user clicks the disclosure button, the window expands." (Rule 5)
-   ✓ "Click the up arrow to increase the text indent." (Rule 6)

## Non-Compliant Example

-   ✗ "Tap Return to go to the previous screen." meaning the Back button (Rule 1)
-   ✗ "Tap the ellipsis button." instead of "More button" (Rule 2)
-   ✗ "Click the question-mark button for help." (Rule 3)
-   ✗ "Click the disclosure button to reveal more information." meaning the disclosure arrow (Rule 4)
-   ✗ "Click the disclosure arrow to expand the dialog for additional choices." meaning the disclosure button (Rule 5)
-   ✗ "Click the stepper to increase the text indent." meaning the up arrow (Rule 6)

## Dependencies

None.

## References

-   [Apple Style Guide — Back button (p. 36)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — More button, More menu (pp. 143–144)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — question-mark button (p. 172); Help button (p. 100)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — disclosure arrow; disclosure button (p. 69)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — up arrow (p. 211)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
