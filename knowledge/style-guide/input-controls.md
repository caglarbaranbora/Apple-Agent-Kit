# Input Controls

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.input-controls
type: knowledge
title: Input Controls
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct terms and verbs for checkbox, radio button, slider, stepper, and switch controls, and rules for describing their states and interactions.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - input-controls
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.navigation-controls
  - knowledge.style-guide.touch-gesture-verbs
  - knowledge.style-guide.status-and-progress-indicators
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.presentation-surfaces
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent names selection and value
controls — checkbox, radio button, slider, stepper, and switch — and the
verbs used to describe their states and interactions in UI text and
documentation for Apple platforms.

## Scope

### Included

-   Naming checkbox, check/checkmark, radio button, slider, stepper, and switch controls
-   States and verbs for selecting/deselecting a checkbox or radio button
-   The discouraged "adjuster"/"incrementer" terms and their replacements

### Excluded

-   Up arrow, down arrow, and other named navigation buttons (see `navigation-controls`)
-   Touch gesture verbs used to operate these controls, e.g. tap, drag (see `touch-gesture-verbs`)
-   Progress indicators and badges (see `status-and-progress-indicators`)
-   General rules for referring to and quoting button names (see `general-button-labels`)

## Rules

### Rule 1

Agents MUST use "checkbox" for a labeled square control users select or
deselect, and MUST NOT instruct users to "click a checkbox" (its initial
state is ambiguous); use "select." A checkbox is "selected" or
"unselected," MUST NOT be described as "checked"/"unchecked," and MUST NOT
use "check" as a verb for this action.

### Rule 2

Agents MUST use "checkmark" as one word, referring to the mark shown next
to a chosen item in a menu, not to a checkbox's selection state.

### Rule 3

Agents MUST use "radio button" for a labeled circular control that
presents mutually exclusive options only in developer materials; in user
materials, agents MUST describe the action ("select") and refer to the
option's or group's label instead of naming the control.

### Rule 4

Agents MUST use "slider" for the object users drag to set a value on a
continuum; the whole control is "the slider control." Agents MUST NOT use
the verb "slide" with a slider — use "tap," "click," or "drag" instead.

### Rule 5

Agents MUST use "stepper" only in developer materials, for a control with
up/down or left/right arrows that increases or decreases a value. In user
materials, agents MUST refer to the individual arrows ("up arrow," "down
arrow," "right arrow," "left arrow," or "arrows") unless referring to the
control itself is unavoidable, in which case "stepper" MAY be used.

### Rule 6

Agents MUST use "switch (n.)" for an interface element offering two
mutually exclusive choices, usually on/off (lowercase "on"/"off" even if
the control's own labels are uppercase). Agents SHOULD describe the
action the user takes ("tap to turn on Location Services") rather than
naming the switch, and MUST NOT use the verbs "switch" or "slide" with it
— use "tap" or "click" instead.

### Rule 7

Agents MUST NOT use "adjuster" or "incrementer" for a control with
up/down or left/right arrows; use "up arrow," "down arrow," "right
arrow," "left arrow," or "arrows" in user materials, and "stepper" only
when the control itself must be named.

## Compliant Example

-   ✓ "Select the Encrypted Messages checkbox." (Rule 1)
-   ✓ "To show the library, choose Window > Library so that a checkmark appears next to Library." (Rule 2)
-   ✓ "Select 'Automatically based on mouse or trackpad.'" (Rule 3)
-   ✓ "Drag the Volume slider to change the volume." (Rule 4)
-   ✓ "Click one of the arrows to increase or decrease the volume." (Rule 5, Rule 7)
-   ✓ "Tap to turn Airplane Mode on or off." (Rule 6)

## Non-Compliant Example

-   ✗ "Click the Encrypted Messages checkbox." / "the checkbox is checked" (Rule 1)
-   ✗ "A check appears next to Library." meaning a checkmark (Rule 2)
-   ✗ "Click the radio button labeled Automatically..." in user materials (Rule 3)
-   ✗ "Slide the slider to change the volume." (Rule 4)
-   ✗ "Click the stepper to increase the volume." when arrows can be named directly (Rule 5)
-   ✗ "Slide the switch to turn Airplane Mode on." (Rule 6)
-   ✗ "Click the adjuster to increase the volume." (Rule 7)

## Dependencies

None.

## References

-   [Apple Style Guide — check; checkbox; checkmark (pp. 49–50)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — radio button (p. 173)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — slider (p. 188)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — stepper (p. 192)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — switch (n.), switch (v.) (p. 196)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — adjuster (p. 15); incrementer (p. 110)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
