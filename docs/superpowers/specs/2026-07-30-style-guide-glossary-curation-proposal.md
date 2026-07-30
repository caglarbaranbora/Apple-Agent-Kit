# Style Guide Glossary Curation Proposal

Status: Draft
Version: 0.1.0

Source: https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf (A-Z glossary, 1,706 terms)
Purpose: propose which terms to ingest into knowledge/style-guide/ and how to cluster them, per [[0001-style-guide-domain-and-domain-roadmap]] (../../../rfcs/0001-style-guide-domain-and-domain-roadmap.md) decision 9.

---

## Proposed Clusters

### capitalization-of-product-names
Terms: product names, app names, app/application/program, plurals, possessives, code names, generation, chip, beta, device, iOS, iOS device, iPadOS, iPadOS device, iPhone, iPad, iPod, internet/Internet, in-app purchase
Rationale: These are the mechanical rules (no verbing, no plurals/possessives of trademarked names, article usage, "device" vs. specific model names) an agent needs every time it writes copy that names the OS, the hardware, or the app itself.

### capitalization-of-system-features-and-services
Terms: App Store, Apple ID, Apple Account, Sign in with Apple, Apple Pay, AirDrop, AirPlay, Wi-Fi, Bluetooth, Dark Mode, Home Screen, Lock Screen, Control Center, Notification Center, Dock, Widget, Live Activities, Live Photos, Dynamic Island, Multi-Touch, Do Not Disturb, voiceover/VoiceOver, Writing Tools
Rationale: These are the first-party system features and services a typical iOS app actually integrates with or references (share sheets, sign-in, connectivity, widgets, system UI chrome), each with its own required capitalization pattern.

### capitalization-styles-sentence-vs-title
Terms: capitalization, command names, title-style capitalization, sentence-style capitalization
Rationale: The foundational mechanic (when to use sentence-style vs. title-style caps) that every button, menu, and header label in an app depends on, so it deserves its own compact, frequently-referenced contract.

### sign-in-and-general-buttons
Terms: button, sign-in (n., adj.)/sign in (v.), sign out, sign-on (n., adj.)/sign on (v.), single sign-on, login/log in (v.), log on/log off, into/in to, OK, user name, allow
Rationale: Required cluster — the general Sign In/Sign Out/Log In terminology and general button-label wording rules that `sign-in-terminology.md` and `button-labels.md` will later depend on.

### authentication-credentials-and-biometrics
Terms: passkey, passphrase, password, PIN, code/passcode, Touch ID, Face ID, two-factor authentication, two-step verification
Rationale: Distinct from general sign-in wording, these are the precise, easily-confused nouns for credential types and biometric methods an agent must not swap when writing auth flows.

### dialogs-menus-and-popups
Terms: dialog, dialog box, dialog message, box, sheet, share sheet, contextual menu, drop-down menu, pop-up, popover, panel, pane, picker, color picker, date picker, action sheet, alert
Rationale: A cluster of overlapping/easily-confused container-UI nouns (dialog vs. sheet vs. popover vs. alert) with a strong avoid-list character ("don't say dialog box," "don't name the popover").

### buttons-and-controls-naming
Terms: option names, Back button, More button/More menu, question-mark button, radio button, disclosure arrow, disclosure button, up arrow, checkbox, check, checkmark, slider, stepper, switch (n.), symbol, adjuster, incrementer, badge, index, alphabet column, progress indicator, determinate progress bar, indeterminate progress bar, asynchronous progress indicator, preset, library, Trash
Rationale: Names for the individual controls an agent will label or describe in instructional/help copy (steppers, sliders, switches, progress indicators, badges), most with an explicit "call it X, not Y" rule.

### touch-gesture-verbs
Terms: tap, tap and hold, touch and hold, double tap, swipe, pinch, rotate, zoom, drag, drag and drop, jiggle, wiggle, long press, press and hold, hold down, scroll, slide, flick, gestures, haptic/haptics
Rationale: The core touchscreen vocabulary for an iOS app — which verb goes with which gesture, and which informal synonyms (wiggle, long press, hold down, flick) to avoid in user-facing text.

### pointer-and-click-terminology
Terms: click, click on, click and drag, click and hold, click in, double click, double press, right-click, mouse, cursor
Rationale: Smaller, secondary cluster for iPad/Mac Catalyst pointer support, where an agent must not default to "click on" or "right-click" phrasing borrowed from desktop conventions.

### core-ui-action-verbs
Terms: enter, type, press, choose, select, open, close, quit, start, stop, run/running, switch (v.), toggle, turn on/turn off, pin, post, put, connect, link (n.), link (v.), lookup (n.)/look up (v.), maximize, minimize, sync/synced/syncing, upload, uninstall
Rationale: The everyday, correct-usage verbs for actions and app lifecycle events that appear constantly in button labels, empty states, and instructional copy.

### action-verbs-avoid-list
Terms: abort, access, activate/deactivate, appear, attach, depress, disable/disabled, display (v.), eject, highlight, hit (v.), input (n., adj.), install, kill, let, mount (v.)/mounted (adj.), exit, uncheck, unclick, unhighlight (v.)/unhighlighted (adj.), unselected (adj.), deselect
Rationale: A companion "don't use X verb, use Y verb" list too large to fit in the core-verbs cluster, covering the informal/legacy verbs (kill, hit, hold down's cousins, disable, activate) an agent must not reach for.

### abbreviations-and-acronyms
Terms: abbreviations and acronyms (master rule), e.g., etc., FAQ, GUI, i.e., number, PDF, UI, user interface, URL, USB, VPN
Rationale: The general spell-out/pluralize/article rules for abbreviations plus the specific ones (UI, URL, USB, GUI) that actually show up in app copy and developer-facing strings.

### numbers-and-time-in-text
Terms: a.m./p.m., aspect ratio, battery level/battery life, fractions, GB, inch, millimeter (mm), percent, phone numbers, pixel, degrees, dates, dimensions, temperatures, time of day, time zone, version number, x (resolution notation), step, zip code
Rationale: Individual glossary entries about numeral formatting that are distinct from the already-ingested international-formatting/units-of-measure chapters (e.g., how to write "8:30 a.m.," "4:3," "step 1," "94103") — flagged for a human editor to confirm no overlap with those contracts before drafting.

### app-state-and-error-terminology
Terms: bug, crash, freeze, hang, corrupted, error message, problem, restart, restore, splash screen, opening display, grayed, unavailable, functionality
Rationale: The vocabulary for describing something going wrong or an app's lifecycle state, almost entirely avoid-list-driven ("crash" → "quits unexpectedly," "splash screen" → "opening display").

### instructional-voice-and-phrasing
Terms: and/or, can/might/may, desire/desired, end user, first person, if necessary, jargon, once, optionally, please, prompt, shows up, under, we, user, capability
Rationale: Sentence-level phrasing and point-of-view rules (avoid first person, avoid "please," address the reader as "you" not "the user") that shape the tone of onboarding and error copy.

### connectivity-and-media-terminology
Terms: cell phone/cellular phone, pair/paired, online, offline, onboard, podcast, photo, picture, preinstalled/preloaded, redownload, telephone number, text message, predictive text, push notification
Rationale: Terminology for describing connectivity/media state and device pairing that recurs in onboarding, settings, and messaging-adjacent UI text.

### general-word-choice-avoid-list
Terms: ampersand, exclamation points, free, grandfathered/grandfathered in, homepage, edit menu/Edit menu, ellipsis, latest, localizable, mode, new, one-click, over, print (v.), professional, resize, support, system, thumb, throw away, third party/third-party, tooltip, typeface/type size/type style, launch, Launchpad, default, document, window, parental controls
Rationale: A catch-all of miscellaneous nouns/adjectives with explicit "don't use X, use Y" rules that didn't fit a narrower theme but recur often enough in general app copy to be worth keeping.

### power-and-toggle-state-terminology
Terms: enable/enabled, power-down, power off, power on, power-up, switch on/switch off
Rationale: A small, tightly-scoped cluster on the single recurring mistake of using "power on/off" or "enable" instead of Apple's preferred "turn on/off," relevant to any settings screen.

## Excluded

Excluded the roughly 1,400+ remaining glossary terms covering: retail/Apple Store and enterprise/education administration terminology; legal, licensing, and corporate boilerplate; hardware and product-line naming trivia not touched by typical app UI (Vision Pro components like Light Seal, Apple Watch health features like Crash Detection/Fall Detection, Apple Card specifics, CarPlay/Mac-only system-administration terms, chip/M-series naming details, connector and port types); print/publishing production and typography-mechanics entries; niche developer-only or networking abbreviations (RAID, SDRAM, POP, DIMM, etc.) unlikely to appear in end-user copy; and generic English grammar entries (that/which, who/whom) with no Apple-specific rule. Also excluded entries already covered by separate contracts: inclusive/gender-neutral/disability language (`writing-inclusively.md`), code-font and placeholder-naming rules (`technical-notation.md`), and trademark/copyright attribution wording (`copyright-and-trademarks.md`).
