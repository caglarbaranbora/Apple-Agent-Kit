# App State and Error Terminology

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.app-state-and-error-terminology
artifact_type: knowledge
title: App State and Error Terminology
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct vocabulary for describing something going wrong or an app's lifecycle state, replacing avoid-list terms like crash, bug, and splash screen with Apple's preferred phrasing.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - error-states
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.instructional-voice-and-phrasing
  - knowledge.style-guide.app-chrome-and-window-terminology
  - knowledge.style-guide.connectivity-and-media-terminology
last_updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent describes an app or device
misbehaving, or an app's startup/lifecycle state, in UI text and
documentation for Apple platforms — replacing developer-slang terms such
as bug, crash, and splash screen with Apple's user-facing vocabulary.

## Scope

### Included

-   Malfunction terms: bug, crash, freeze, hang, corrupted
-   Messaging terms: error message, problem
-   Lifecycle terms: restart, restore, splash screen, opening display
-   Availability terms: grayed, unavailable, functionality

### Excluded

-   Dialog and alert naming conventions (not in this glossary excerpt)
-   Button labels and permission-prompt wording (see `general-button-labels`)

## Rules

Two rules apply across the whole table. First, agents MUST prefer neutral,
non-alarming phrasing for malfunction terms — most of the discouraged
terms below describe user-visible symptoms (not responding) rather than
implying hardware or software damage. Second, several rows below are noun
forms of an otherwise-correct verb (restart, restore); the verb is
correct, but agents MUST NOT also use the same word as a noun.

| Term | Correct Form | Notes |
|---|---|---|
| bug | problem, condition, issue, or situation | Avoid "bug" (Rule 1) |
| crash | quits unexpectedly, doesn't respond, or stops responding | If "crash" must be used, quote it and reassure the reader that it doesn't imply hardware/software damage (Rule 2) |
| freeze | not responding | "Freeze" describes only pointer behavior onscreen; avoid it as a noun or to describe what the computer does (Rule 3) |
| hang | not responding | Don't use "hang" to describe computer behavior after a system error (Rule 4) |
| corrupted | damaged | Avoid "corrupted" if possible (Rule 5) |
| error message | message, alert, alert message, or alert sound | Don't use "error message" except in developer materials (Rule 6) |
| problem | condition, issue, or situation | Avoid in phrases like "this is a known problem"; OK in general use, e.g. "If you have a problem registering, try again." (Rule 7) |
| restart (v.) | restart | Verb only; don't use restart as a noun (Rule 8) |
| restore (v., adj.) | restore | Verb/adjective only; "Restoring stopped," not "The restore stopped." (Rule 9) |
| splash screen | opening display, startup display, or startup screen | Don't use "splash screen" (Rule 10) |
| opening display | opening display, startup display, or startup screen | These three terms are interchangeable for the screen shown while an app or computer starts up (Rule 11) |
| grayed | dimmed | Don't use "grayed" or "hollow" (Rule 12) |
| unavailable | unavailable | Describes an item, such as a menu command or dialog option, the user can't select or choose because conditions aren't met (Rule 13) |
| functionality | features | Avoid "functionality" in user materials when "features" works (Rule 14) |

## Compliant Example

-   ✓ "If you have a problem registering, try again in a few moments." (Rule 7)
-   ✓ "Safari quits unexpectedly" instead of "Safari crashes" (Rule 2)
-   ✓ "If the computer doesn't respond to input, a system error may have occurred." (Rule 4)
-   ✓ "Avoid stopping the restore process." (Rule 9)
-   ✓ "The opening display appears after a few seconds." (Rule 11)
-   ✓ "The Copy command is unavailable if there's no text selected." (Rule 13)
-   ✓ "Some features are not available in certain regions." (Rule 14)

## Non-Compliant Example

-   ✗ "There's a bug in this version." (Rule 1)
-   ✗ "The app crashed and lost my data." unquoted, with damage implied (Rule 2)
-   ✗ "If the computer freezes, follow these instructions." (Rule 3)
-   ✗ "The restore stopped because the disk is full." using restore as a noun (Rule 9)
-   ✗ "The splash screen appears while the app loads." (Rule 10)
-   ✗ "Some functionality is not available in certain regions." (Rule 14)

## Dependencies

None.

## References

-   [Apple Style Guide — bug (p. 42); crash (p. 60)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — freeze (p. 91); hang (p. 98); corrupted (p. 59)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — error message (p. 82); problem (p. 167)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — restart (v.), restore (v., adj.) (p. 176)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — opening display (p. 152); startup display, startup screen (p. 192)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — grayed (p. 96); dimmed (p. 68); unavailable (p. 209); functionality (p. 91)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
