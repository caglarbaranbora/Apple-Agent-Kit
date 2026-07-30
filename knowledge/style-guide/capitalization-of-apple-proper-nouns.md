# Capitalization of Apple Proper Nouns

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.capitalization-of-apple-proper-nouns
type: knowledge
title: Capitalization of Apple Proper Nouns
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct capitalization, pluralization, and article usage for Apple product names, platform names, and system feature names.
domain: Style Guide
tags:
  - style-guide
  - capitalization
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent capitalizes, pluralizes, and
forms possessives of Apple product names, platform names, and system
feature names when writing UI text, documentation, or example code
identifiers for Apple platforms.

## Scope

### Included

-   Exact capitalization of Apple product, platform, and feature names
-   General rules: no pluralizing/verbing/possessive of trademarked names
-   Article usage (the, a, an) before specific proper nouns
-   Product/feature-specific naming quirks (hyphenation, precedes with "the")

### Excluded

-   Generic sentence-style vs. title-style capitalization rules for UI text (see `capitalization-style-rules`)
-   Sign-in and authentication terminology (see `sign-in-and-authentication-terminology`)
-   Button label wording (see `general-button-labels`)

## Rules

Two general rules apply across every term below. First, agents MUST NOT
pluralize, verb, or possessive-form a trademarked Apple product or feature
name; instead rewrite using a generic noun ("iPad devices," not "iPads";
"You can use AirDrop to send," not "You can AirDrop"; rewrite around
`Keynote's slides`). Second, agents MUST reproduce the exact official
capitalization of each name regardless of surrounding sentence case, and
MUST NOT insert "the" before names that Apple's style forbids it for (e.g.
iPhone, iPad, Control Center, Notification Center) — note this is a
per-term rule, not universal: some names (App Store) specifically require
an article; check the table below for each term.

| Term | Correct Form | Notes |
|---|---|---|
| product names | Never abbreviated | Don't abbreviate any Apple product/service name (Rule 1) |
| app / application / program | app (iOS/iPadOS/tvOS/visionOS/watchOS); app or application (Mac, be consistent); program (no GUI) | (Rule 2) |
| app names | Follow the app's own capitalization/spacing; no "the" before app names (Finder is the exception) | "Open QuickTime Player," not "Open the QuickTime Player" (Rule 3) |
| plurals | Add generic plural noun, don't pluralize the trademarked name | "Mac computers," not "Macs" (Rule 4) |
| possessives | Rewrite to avoid a possessive of any product name | Not "Keynote's slides" (Rule 5) |
| code names | Use exactly one consistent form; don't use in final docs unless marketing approves | (Rule 6) |
| generation | Hyphenate as compound adjective; use numeral when generation follows name; never shorten to "gen" or "G" | "sixth-generation iPad mini"; "iPad (5th generation)" (Rule 7) |
| chip | Name alone is OK without "chip" | "A18 Pro chip" or just "A18 Pro" (Rule 8) |
| beta (n., adj.) | Lowercase generic use; capitalize in a proper name | "a public beta"; "Apple Beta Software Program" (Rule 9) |
| device | Generic hardware noun; use to avoid pluralizing a trademarked name | "iOS device," "multiple iPad devices" — derived from the iOS/iPadOS device entries, not an independent glossary term (see Rule 11, Rule 12) |
| iOS | No article | "iOS is the world's most advanced..." (Rule 11) |
| iOS device | Generic term for iOS mobile hardware; avoid "mobile device" for this | (Rule 11) |
| iPadOS / iPadOS device | No article for iPadOS; "iPadOS device" for generic hardware | (Rule 12) |
| iPhone | No "the" in general references; "the" OK for a specific iPhone | "To lock iPhone, press..." (Rule 13) |
| iPad | No "the" in general references; "the" OK for a specific iPad | "Rotate iPad to landscape orientation." (Rule 13) |
| iPod | Always include "iPod" in the name; never "touch" alone | "iPod touch," not "touch" (Rule 14) |
| internet / Internet | Lowercase always, including "the internet"; capitalize only in proper names like Internet Protocol | (Rule 15) |
| in-app purchase | Lowercase, hyphenated | (Rule 16) |
| App Store | Article required in text ("the App Store" or "on the App Store") | "Find the item you want on the App Store." (Rule 17) |
| Apple ID | Don't use; use Apple Account | (Rule 18) |
| Apple Account | Preferred term for the account users sign in to | "Sign in to your Apple Account" (Rule 18) |
| Sign in with Apple | Capitalize exactly; lowercase "in" | (Rule 19) |
| Apple Pay | Don't combine the Apple logo glyph with "Pay" in running text | "Find out where you can use Apple Pay." (Rule 20) |
| AirDrop / AirPlay | Never used as a verb | "use AirDrop to send," not "AirDrop photos" (Rule 21) |
| Wi-Fi | Exact form only | Not "wifi," "wi-fi," or "WiFi" (Rule 22) |
| Bluetooth | Never used as a noun; no hyphen | "devices that use Bluetooth wireless technology" (Rule 23) |
| Dark Mode | Capitalize; don't say a device "is using" or "is in" Dark Mode | "If you're using Dark Mode..." (Rule 24) |
| Home Screen | Capitalize both words | (Rule 25) |
| Lock Screen | Capitalize both words | (Rule 25) |
| Control Center | No "the" before it | "Click an item in Control Center" (Rule 26) |
| Notification Center | No "the" before it | "To open Notification Center..." (Rule 26) |
| Dock | Never a verb; items are "in the Dock," not "on" it | "put a window in the Dock," not "dock a window" (Rule 27) |
| widget | Capitalize the specific widget's name; lowercase "widget" itself | "the Weather widget" (Rule 28) |
| Live Activities | Capitalize; "Live Activity" or "activity" for one instance | (Rule 29) |
| Live Photos | Capitalize; "Live Photos" or "Live Photo" for the media itself | (Rule 29) |
| Dynamic Island | Precede with "the" | "The Dynamic Island appears whenever..." (Rule 30) |
| Multi-Touch | Capitalize both parts, hyphenated | "Multi-Touch trackpad" (Rule 31) |
| Do Not Disturb | Capitalize all three words | (Rule 32) |
| voiceover / VoiceOver | Lowercase for recorded narration; capitalize for the Apple screen reader | "record your own voiceover" vs. "VoiceOver lets you navigate" (Rule 33) |
| Writing Tools | Capitalize; takes a plural verb | "Writing Tools are available..." (Rule 34) |
| library | Lowercase in general references; capitalize only as an interface element label | "your music library" vs. "click Library" (Rule 35) |
| Trash | Capitalize; use an article | "drag the file to the Trash" (Rule 36) |

## Compliant Example

-   ✓ "You can use AirDrop to send photos to other Apple devices nearby." (Rule 21)
-   ✓ "Mac computers," not "Macs" (Rule 4)
-   ✓ "iOS is the world's most advanced mobile operating system." (Rule 11)
-   ✓ "To lock iPhone, press the side button." (Rule 13)
-   ✓ "Sign in to your Apple Account on all your devices." (Rule 18)
-   ✓ "Click an item in Control Center to see additional options." (Rule 26)
-   ✓ "Writing Tools are available nearly everywhere you write." (Rule 34)

## Non-Compliant Example

-   ✗ "You can AirDrop photos to nearby devices." (Rule 21)
-   ✗ "Connect your Macs to Wi-Fi." meaning multiple Mac computers (Rule 4)
-   ✗ "To lock the iPhone, press the side button." (Rule 13)
-   ✗ "An Apple ID gives you access to all Apple services." (Rule 18)
-   ✗ "Click an item in the Control Center." (Rule 26)
-   ✗ "To dock a window, click the minimize button." (Rule 27)

## Dependencies

None.

## References

-   [Apple Style Guide — app, application, program (p. 20)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — Apple Account; Apple ID (pp. 22, 24)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — iOS; iPad; iPadOS; iPhone; iPod (pp. 113–117)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — plurals; possessives (pp. 161, 163)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — Wi-Fi; widget; Writing Tools (pp. 219–221)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
