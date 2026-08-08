# Presentation Surfaces

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.presentation-surfaces
artifact_type: knowledge
title: Presentation Surfaces
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the correct terms for dialogs, sheets, menus, pickers, and other UI surfaces used to present information or choices, and when each term is appropriate for user vs. developer materials.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - presentation-surfaces
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.input-controls
  - knowledge.style-guide.status-and-progress-indicators
  - knowledge.style-guide.navigation-controls
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.touch-gesture-verbs
  - knowledge.style-guide.app-chrome-and-window-terminology
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent names and describes onscreen
presentation surfaces — dialogs, sheets, menus, pickers, and related
elements — in UI text and documentation for Apple platforms, including
which terms are user-facing and which are developer-only.

## Scope

### Included

-   Naming dialogs, sheets, action sheets, and share sheets
-   Naming menus that present pop-up-style or contextual choices
-   Naming panels, panes, and pickers
-   Naming alerts and distinguishing them from other dialogs
-   User-materials vs. developer-materials term choice for each surface

### Excluded

-   Input controls such as checkboxes, sliders, steppers, and switches (see `input-controls`)
-   Progress indicators and badges (see `status-and-progress-indicators`)
-   Navigation buttons such as Back button, disclosure arrow/button, and More button (see `navigation-controls`)
-   General rules for referring to and quoting button names (see `general-button-labels`)
-   Touch gesture verbs used to interact with these surfaces (see `touch-gesture-verbs`)

## Rules

Two rules apply across the whole table. First, when a term below is marked
"Don't use" in user materials, agents MUST instead describe what the user
selects or does, rather than naming the surface. Second, several terms
(dialog, sheet, action sheet, popover) are acceptable in developer
materials even when disallowed in user materials; agents MUST pick the
form appropriate to the audience of the document being written.

| Term | Correct Form | Notes |
|---|---|---|
| dialog | Use for windows requiring an explicit dismissal action (OK, Cancel, Print); don't use "dialog box" | Can be implemented as a sheet, but don't call it a sheet in user materials (Rule 1) |
| dialog box | Don't use; use dialog | (Rule 2) |
| dialog message | Don't use; use message | (Rule 3) |
| box | Don't use "dialog box"; use dialog | Standalone glossary entry distinct from "dialog box" (Rule 4) |
| sheet | Don't use in user materials; call it a dialog (Mac) or describe the task (other platforms) | OK in developer materials for a view tied to the current context (Rule 5) |
| share sheet | Note capitalization: two words, lowercase | Avoid in most user materials; OK in developer materials and content about its options (Rule 6) |
| contextual menu | Use "shortcut menu" in user materials, not "contextual menu" | May note "(also called a contextual menu)" parenthetically on first reference (Rule 7) |
| drop-down menu | Don't use; use "menu," or "pull-down menu" (menu bar) / "pop-up menu" (dialog or window) as appropriate | (Rule 8) |
| pop-up | Adjective for ads/notices from a browser (pop-up ads, pop-up window); noun form OK only when space-constrained | Never use "pop-up" alone to mean "pop-up menu" (Rule 9) |
| popover | Don't use in user materials; describe what the user selects or does | Never call it a dialog or window; OK in developer materials (Rule 10) |
| panel | Don't use in user materials; use dialog, window, or pane | Use in developer materials (e.g., SFChooseIdentityPanel) (Rule 11) |
| pane | Use pane (not panel) for an area within a window/dialog changed by clicking a button | Don't call the switching control a "tab"; call it a button (Rule 12) |
| picker | Don't use in user materials to describe selecting a color or date | Describe the task or interface area instead (Rule 13) |
| color picker | Don't use | See picker (Rule 14) |
| date picker | Don't use | See picker (Rule 15) |
| action sheet | Developer materials: a sheet presenting choices tied to the current action | User materials: don't use action sheet, sheet, or popover; describe the task (Rule 16) |
| alert | Generic signal (visual dialog or auditory beep) calling attention to an unusual situation | Use "alert sound"/"alert message" for generic references; avoid "error message" outside developer materials (Rule 17) |

## Compliant Example

-   ✓ "Use the Print dialog to choose a printer and select print options." (Rule 1)
-   ✓ "Open dialog," not "Open dialog box" (Rule 2, Rule 4)
-   ✓ "Tap Customize, then turn on Bold Text." (Rule 5)
-   ✓ "A shortcut menu (also called a contextual menu) appears." (Rule 7)
-   ✓ "You can prevent websites from displaying pop-ups." (Rule 9)
-   ✓ "Select a color in the Colors window." (Rule 13)
-   ✓ "Tap Scan Documents." (Rule 16)
-   ✓ "An alert message appears if a problem occurs during installation." (Rule 17)

## Non-Compliant Example

-   ✗ "Click Save in the Print dialog box." (Rule 1, Rule 2)
-   ✗ "Tap Customize, then turn on Bold Text in the sheet that appears." (Rule 5)
-   ✗ "Click the drop-down menu, then choose a size." (Rule 8)
-   ✗ "Click the pop-up, then choose a size." meaning a pop-up menu (Rule 9)
-   ✗ "Tap Print in the popover." (Rule 10)
-   ✗ "Select a color in the color picker." (Rule 13, Rule 14)
-   ✗ "Tap Scan Documents in the sheet that appears." (Rule 16)

## Dependencies

None.

## References

-   [Apple Style Guide — dialog; dialog box; dialog message (pp. 66–67)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — box (p. 41)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — action sheet (p. 14)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — alert (n., adj.) (pp. 17–18)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — contextual menu (p. 57)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — color picker (p. 54); date picker (p. 62); picker (p. 158)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — drop-down menu (p. 76); menus (pp. 139–140)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — pane; panel (p. 153)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — popover; pop-up (n., adj.) (p. 163)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — share sheet (p. 184); sheet (p. 184)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
