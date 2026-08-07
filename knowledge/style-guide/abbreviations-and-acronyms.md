# Abbreviations and Acronyms

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.abbreviations-and-acronyms
artifact_type: knowledge
title: Abbreviations and Acronyms
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the master rule for spelling out, pluralizing, and using articles with abbreviations and acronyms, plus specific entries for common technical and Latin abbreviations.
domain: Style Guide
tags:
  - style-guide
  - abbreviations
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.units-of-measure
last_updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent spells out, pluralizes, and
forms articles for abbreviations and acronyms, and lists the correct form
for a set of common technical and Latin abbreviations, when writing UI
text or documentation for Apple platforms.

## Scope

### Included

-   The general spell-out-on-first-occurrence rule and how to present the pair
-   Pluralization (no apostrophe) and article (a/an) rules for abbreviations
-   Punctuation and Latin-abbreviation avoidance
-   Specific entries: e.g., etc., FAQ, GUI, i.e., number ("no."), PDF, UI, user interface, URL, USB, VPN

### Excluded

-   Unit-of-measure abbreviation spacing, hyphenation, and symbol-mixing rules (see `units-of-measure`)
-   Full abbreviation/acronym reference tables beyond the terms listed above

## Rules

Two rules apply across the whole table. First, on first occurrence in user
materials, agents MUST spell out an abbreviation or acronym, generally
putting the spelled-out form first with the abbreviation in parentheses
(e.g. "internet service provider (ISP)"); if the abbreviation is far more
familiar, agents MAY lead with it instead. Agents MUST NOT add an
apostrophe before the "s" to form a plural ("CDs," "ISPs") and MUST choose
"a" or "an" based on the abbreviation's pronunciation, not its spelling
("a USB port," "an FAQ"). Second, agents MUST NOT use periods in
abbreviations except for nonmetric units of measure and a.m., p.m., and
U.S., and MUST avoid Latin abbreviations in running text, spelling out the
meaning instead.

| Term | Correct Form | Notes |
|---|---|---|
| e.g. | for example | Don't use e.g.; it's one of the Latin abbreviations to avoid (Rule 1) |
| etc. | and so forth, and so on | Don't use etc. (Rule 2) |
| FAQ | an FAQ (singular); FAQs (plural) | Use title-style capitalization for the full term when it precedes a noun: "the Frequently Asked Questions document" (Rule 3) |
| GUI | interface (user materials), UI (developer materials) | Don't use GUI itself in text (Rule 4) |
| i.e. | that is | Don't use i.e. (Rule 5) |
| number | no. | Abbreviate as "no." (lowercase) only if space is limited; see also number sign (#) (Rule 6) |
| PDF | PDF | Not necessary to spell out on first occurrence; use to refer to a PDF file (Rule 7) |
| UI | UI (developer materials), interface (user materials) | Abbreviation for user interface (Rule 8) |
| user interface | interface | Don't use "user interface" in user materials (Rule 9) |
| URL | internet address, web address (user materials); URL (developer/technical materials) | Preceded by "a," not "an"; pronounced "you-are-ell" (Rule 10) |
| USB | USB | Abbreviation for Universal Serial Bus; avoid as a noun (Rule 11) |
| VPN | VPN | Abbreviation for virtual private network or virtual private networking (Rule 12) |

## Compliant Example

-   ✓ "An internet service provider (ISP) connects you to the internet." then "ISP" thereafter (intro rule)
-   ✓ "a USB port," "an FAQ" (intro rule)
-   ✓ "For example, restart your Mac." not "e.g., restart your Mac." (Rule 1)
-   ✓ "Use interface, not GUI, in this text." (Rule 4)
-   ✓ "You can add effects to PDFs in Preview." (Rule 7)
-   ✓ "In user materials, use interface." not "user interface" (Rule 9)
-   ✓ "Enter your web address." in user materials, not "Enter your URL." (Rule 10)

## Non-Compliant Example

-   ✗ "CD's" or "ISP's" to form a plural (intro rule)
-   ✗ "a FAQ" mispronouncing FAQ as letters instead of a word (intro rule)
-   ✗ "et al., e.g., i.e., etc." used freely in running text (Rule 1, Rule 2, Rule 5)
-   ✗ "The GUI lets you drag files." (Rule 4)
-   ✗ "Sign in with your No. or account ID." capitalized, and abbreviated unnecessarily when space allows "number" (Rule 6)
-   ✗ "Enter your UI settings." in a user-facing document (Rule 8)

## Dependencies

None.

## References

-   [Apple Style Guide — abbreviations and acronyms (pp. 11–12)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — e.g. (p. 78); etc. (p. 82); FAQ (p. 84); i.e. (p. 108)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — GUI (p. 96); number (p. 148); PDF (p. 156)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — UI (p. 209); user interface (p. 212); URL (p. 211)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — USB (p. 212); VPN (p. 216)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
