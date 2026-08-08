# UI Action Verbs

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.ui-action-verbs
artifact_type: knowledge
title: UI Action Verbs
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the correct verbs for common UI actions and the discouraged verbs each one replaces, covering entry, selection, window, sync, and power/toggle-state vocabulary.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - verbs
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.pointer-and-click-terminology
  - knowledge.style-guide.touch-gesture-verbs
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.instructional-voice-and-phrasing
  - knowledge.style-guide.connectivity-and-media-terminology
last_updated: 2026-08-08
```

## Intent

This contract defines the correct verb an AI coding agent uses for each
common UI action — entering data, selecting, opening/closing, running,
syncing, and changing a power or toggle state — and the discouraged verb
each correct term replaces, when writing UI text or documentation for
Apple platforms.

## Scope

### Included

-   Core action verbs for text entry, selection, window/app lifecycle, and content actions
-   Avoid-list verbs with their required replacement term
-   Power- and toggle-state phrasing: turn on/off vs. power on/off vs. enable/toggle

### Excluded

-   Touchscreen and pointer gesture verbs (tap, swipe, click, drag, etc.) (see `touch-gesture-verbs`, `pointer-and-click-terminology`)
-   Button naming and quoting conventions (see `general-button-labels`)

## Rules

Two rules apply across the whole table. First, several correct verbs below
have a narrower meaning than their everyday English sense (for example,
enter vs. type, or run vs. use); agents MUST follow the glossary's specific
distinction, not a general-purpose synonym. Second, for every avoid-list
row agents MUST substitute the listed Correct Form and MUST NOT use the
discouraged term even as a synonym for variety.

| Term | Correct Form | Notes |
|---|---|---|
| enter | enter | Use for inputting text by typing, pasting, dragging, or another method; use type for pressing keys, press for keyboard keys (Rule 1) |
| type (v.) | type | Use for pressing keys to produce characters onscreen; don't confuse with type (n.), which means displayed text, not font (Rule 2) |
| press | press | Quick press-and-release of a keyboard key, mechanical button/switch, or AirPods stem; don't use click, hit, push, tap, or type for it (Rule 3) |
| choose | choose | Use for menu items (including pop-up/shortcut menus); the user selects an object, then chooses a command (Rule 4) |
| select (v.) | select | Use when picking among multiple objects (icons, checkboxes, radio buttons) or highlighting text; don't use for menu items (Rule 5) |
| open | open | Users open icons, folders, documents, and apps (Rule 6) |
| close | close | In macOS, users close windows/documents and quit apps; in iOS, close means stop using an app temporarily, which may not quit it (Rule 7) |
| quit | quit | Use for stopping an app from running completely; don't use exit, exit from, or leave (Rule 8) |
| start | open | Don't use start when you mean open an app (Rule 9) |
| stop | stop | General term for ceasing a process, command, or program; don't use when you mean quit an app (Rule 10) |
| run (v.), running (adj.) | use (apps); running (background processes) | "Running" is for GUI-less background processes; don't use run for what a user does with an app (say use); don't use running to mean an app is open (say open) (Rule 11) |
| switch (v.) | switch | OK to mean change or substitute; don't use switch on/off or toggle to mean turn on/off (Rule 12) |
| toggle (v.) | turn on/off, switch between | OK in developer materials only; don't use in user materials (Rule 13) |
| turn on, turn off | turn on, turn off | OK for power to a computer/peripheral and for enabling features such as file sharing (Rule 14) |
| pin (n., v.) | pin | Noun: an item marking a map location. Verb: saving an item for later use, e.g. pinning a website or search result (Rule 15) |
| post (v.) | post to, post on | OK for publishing something on the internet or another network (Rule 16) |
| put | drag | Don't use put when you mean drag (Rule 17) |
| connect | connect | Use for joining devices together; don't use attach, hook up, or mate; don't use connect when you mean plug in (Rule 18) |
| link (n.) | link | A user clicks a link; don't use "follow a link" (Rule 19) |
| link (v.) | link | OK for creating a link on a webpage; don't use link to describe connecting to a webpage (Rule 20) |
| lookup (n., adj.), look up (v.) | lookup / look up | One word except as a verb (Rule 21) |
| maximize | maximize | Making a window as big as possible without going full screen; don't use for clicking a minimized window (use make active) (Rule 22) |
| minimize (v.), minimized (adj.) | minimize | OK to describe windows put in the Dock (Rule 23) |
| sync, synced, syncing | sync | Not synch/synched/synching; syncing devices takes "with," syncing content takes to/from/between; don't use synchronize/synchronization (Rule 24) |
| upload | upload | OK for copying files to a server; avoid for what iCloud does (say content is stored, kept up to date, or appears automatically) (Rule 25) |
| uninstall | uninstall | OK to use uninstall and uninstaller (Rule 26) |
| abort | exit, interrupt, quit, or stop | Avoid in user materials (Rule 27) |
| access (v.) | a more precise term, e.g. log in to, connect to | OK when a more specific term isn't available (Rule 28) |
| activate, deactivate | turn on, turn off | Avoid activate/deactivate (Rule 29) |
| appear | appear | Use for items becoming visible onscreen; pairs with display (v.), below, which is the discouraged form (Rule 30) |
| attach | connect | Don't use attach to mean connect (Rule 31) |
| depress | press | Don't use depress (Rule 32) |
| disable (v.), disabled (adj.) | turn off, deselect (v.); turned off, unavailable, inactive (adj.) | Don't use disable for turning off a feature or option; don't use disabled for features that are off/unavailable (Rule 33) |
| display (v.) | appear | Don't use display when you mean appear (Rule 34) |
| eject (trans. v.) | eject, transitive only | Don't use as an intransitive verb ("The disk ejects") (Rule 35) |
| highlight (v.) | select | Don't use highlight when you mean select; don't use as an intransitive verb (Rule 36) |
| hit (v.) | press or tap | Don't use hit to instruct users to press a key or touch a screen (Rule 37) |
| input (n., adj.) | enter or type (v.) | Avoid using input as a verb (Rule 38) |
| install | install | Items are installed on a disk, not onto a disk; don't use install as a noun (Rule 39) |
| kill | force quit, force exit, terminate, end, stop, halt, or cancel | Don't use kill for stopping an app or process (Rule 40) |
| let | restructure around what the user does | Don't overuse "lets you"; OK when generically describing a feature's capability (Rule 41) |
| mount (v.), mounted (adj.) | open, make available, connect to (v.); available, on your desktop (adj.) | Avoid in user materials; OK in server/technical materials; don't use mount as an intransitive verb (Rule 42) |
| exit | quit | Don't use exit to refer to quitting an app in user materials (Rule 43) |
| uncheck | deselect | Don't use uncheck (Rule 44) |
| unclick | deselect | Don't use unclick (Rule 45) |
| unhighlight (v.), unhighlighted (adj.) | deselect (v.); not highlighted (adj.) | Don't use unhighlight or unhighlighted (Rule 46) |
| unselected (adj.) | unselected | Use for something that's not selected; not deselected, unchecked, or dehighlighted (Rule 47) |
| deselect | deselect | OK to mean cancel a selection; not uncheck, unselect, unhighlight, or dehighlight (Rule 48) |
| power on, power off | turn on, turn off | Don't use power on/off, power up/down, or switch on/off in user materials (Rule 49) |
| enable (v.), enabled (adj.) | turn on (typically) | Avoid enable when you mean turn on; turn on initiates an action immediately, enable makes subsequent actions possible; OK for a task that makes other actions possible (Rule 50) |

## Compliant Example

-   ✓ "Enter your account information and tap Save." (Rule 1)
-   ✓ "Choose View > Sort By > Date." (Rule 4)
-   ✓ "To use Siri on your Mac, you must have macOS 10.12 or later installed." not "running" (Rule 11)
-   ✓ "You can turn the Accent setting on or off." not "toggle" (Rule 13)
-   ✓ "Cancel all background tasks." not "Kill all background tasks." (Rule 40)
-   ✓ "To hide an object's caption, deselect the Caption checkbox." (Rule 33)
-   ✓ "Turn on Windows file sharing." not "Enable Windows file sharing." (Rule 50)

## Non-Compliant Example

-   ✗ "Type your account information." meaning general text entry (Rule 1)
-   ✗ "Select File > Print." for a menu command (Rule 4, Rule 5)
-   ✗ "Check to see whether any apps are running." meaning open (Rule 11)
-   ✗ "Highlight the text you want to change." (Rule 36)
-   ✗ "Put the file in the Trash." (Rule 17)
-   ✗ "Power on your Mac to begin." (Rule 49)
-   ✗ "iMovie enables you to view, edit, and share movie projects." (Rule 50)

## Dependencies

None.

## References

-   [Apple Style Guide — enter (p. 81); type (v.) (p. 209); press (p. 166); choose (p. 50); select (v.) (p. 181)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — open (p. 152); close (p. 51); quit (p. 172); start (p. 192); stop (p. 193)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — run (v.), running (adj.) (p. 178); switch (v.) (p. 196); toggle (v.) (p. 205)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — turn on, turn off (p. 208); pin (n., v.) (p. 158); post (v.) (p. 164); put (p. 171)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — connect (p. 56); link (n.), link (v.) (p. 125); lookup (n., adj.), look up (v.) (p. 131)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — maximize (p. 137); minimize (v.), minimized (adj.) (p. 142); sync, synced, syncing (p. 197)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — upload (p. 211); uninstall (p. 210); abort (p. 12); access (n., v.) (p. 13); activate, deactivate (p. 14)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — appear (p. 21); attach (p. 33); depress (p. 65); disable (v.), disabled (adj.) (p. 68); display (v.) (p. 70)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — eject (trans. v.) (p. 78); highlight (v.) (p. 100); hit (v.) (p. 101); input (n., adj.) (p. 110); install (p. 111); kill (p. 122); let (p. 124); mount (v.) (p. 144); exit (p. 83); deselect (p. 65)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — uncheck, unclick (p. 209); unhighlight (v.), unselected (adj.) (p. 210); power off (v.), power on (v.) (p. 164); enable (v.), enabled (adj.) (p. 80)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
