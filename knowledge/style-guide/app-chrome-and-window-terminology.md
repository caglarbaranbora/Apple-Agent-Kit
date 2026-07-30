# App Chrome and Window Terminology

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.app-chrome-and-window-terminology
type: knowledge
title: App Chrome and Window Terminology
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct usage of window and app-chrome vocabulary — window, document, launch, mode, system — for Settings and Mac Catalyst UI text and documentation.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - app-chrome
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.capitalization-of-apple-proper-nouns
  - knowledge.style-guide.app-state-and-error-terminology
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent names and describes window and
app-chrome vocabulary — window, document, homepage, launch, Launchpad,
default, mode, system, tooltip, and parental controls — in Settings and Mac
Catalyst UI text and documentation for Apple platforms.

## Scope

### Included

-   Naming windows across macOS, iPadOS, and visionOS
-   Distinguishing "document" from generic "file"
-   Audience-gated terms: "launch" and "tooltip" (developer materials only)
-   "Mode," "default," and "system" overuse guidance
-   "Homepage," "Launchpad," and "parental controls" naming

### Excluded

-   Dialogs, sheets, panels, panes, popovers, and pickers (see `presentation-surfaces`)
-   Home Screen, Lock Screen, Control Center, Notification Center, and Dock capitalization (see `capitalization-of-apple-proper-nouns`)
-   Splash screen / opening display lifecycle vocabulary (see `app-state-and-error-terminology`)

## Rules

Two patterns recur across this table. First, several terms (window,
document, mode, system) are generic-sounding words that are frequently
overused as catch-alls; agents MUST use the more specific or accurate term
the row specifies rather than defaulting to these words. Second, some terms
are audience-gated: "launch" and "tooltip" are acceptable in developer
materials but MUST be replaced in user materials per the row's Correct Form.

| Term | Correct Form | Notes |
|---|---|---|
| window | Use for main app windows, document windows, and windows with controls affecting the active document/selection | iPadOS: also for app windows visible together in Split View/Slide Over; OK for a Picture in Picture window; don't use for a popover (Rule 1) |
| document | A file the user creates and can open, edit, and print | A document is a specific type of file; don't use "document" when the file could be another type — use "file" (Rule 2) |
| homepage | One word; the webpage that's the entry point to a website | Don't use "landing page" or "portal"; don't use "homepage" to mean an entire website (Rule 3) |
| launch | Avoid in user materials when you mean "open" an app | OK in developer materials (Rule 4) |
| Launchpad | Don't use in content about macOS 26 or later | Use "Apps icon" for the Dock icon; use "Spotlight" for the location to browse/open apps (Rule 5) |
| default (n., adj.) | OK to describe the state of settings before the user changes them | (Rule 6) |
| mode | Don't overuse; often omittable with no change in meaning | Avoid calling a feature a "mode" unless "mode" is part of the feature's actual name (Rule 7) |
| system | Don't use to refer to a computer by itself; use "computer" | OK when referring to a computer plus its peripherals, accessories, and software collectively (Rule 8) |
| tooltip | Don't use, except in developer materials | Use "help tag" in user materials (Rule 9) |
| parental controls | Correct term | Don't use "family controls" (Rule 10) |

## Compliant Example

-   ✓ "You can open two windows from the same app in Split View." (Rule 1)
-   ✓ "Time Machine backs up all your files to an external disk." (Rule 2)
-   ✓ "The Apple homepage has links to product information." (Rule 3)
-   ✓ "To use Siri on your Mac, open the app first." not "launch the app" (Rule 4)
-   ✓ "Tap the Apps icon in the Dock to browse your apps." (Rule 5)
-   ✓ "By default, iMovie inserts transitions between clips." (Rule 6)
-   ✓ "When you're using the paintbrush…" not "in paintbrush mode" (Rule 7)
-   ✓ "You must restart your computer for the changes to take effect." (Rule 8)
-   ✓ "Turn on parental controls for this account." (Rule 10)

## Non-Compliant Example

-   ✗ "Tap Print in the popover window." conflating a popover with a window (Rule 1)
-   ✗ "Time Machine backs up all your documents to an external disk." meaning all files (Rule 2)
-   ✗ "You can purchase products on the Apple homepage." meaning the whole site (Rule 3)
-   ✗ "Launch the app to get started." in user materials (Rule 4)
-   ✗ "Open Launchpad to find your apps." for macOS 26 or later (Rule 5)
-   ✗ "In Stage Manager mode, you can group apps together." (Rule 7)
-   ✗ "You must restart your system for the changes to take effect." (Rule 8)
-   ✗ "Hover to see the tooltip." in user materials (Rule 9)
-   ✗ "Turn on family controls for this account." (Rule 10)

## Dependencies

None.

## References

-   [Apple Style Guide — window (p. 219)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — document (p. 71)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — homepage (p. 102)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — launch (p. 123); Launchpad (p. 123)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — default (n., adj.) (p. 64)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — mode (p. 142)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — system (p. 198)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — tooltip (p. 205); parental controls (p. 154)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
