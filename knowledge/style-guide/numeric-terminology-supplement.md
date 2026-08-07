# Numeric Terminology Supplement

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.numeric-terminology-supplement
artifact_type: knowledge
title: Numeric Terminology Supplement
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines formatting rules for a narrow set of numeric terms not covered by units of measure, international formatting, or international style — aspect ratio, fractions, version number, resolution "x" notation, step, and zip code.
domain: Style Guide
tags:
  - style-guide
  - numeric
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.units-of-measure
  - knowledge.style-guide.international-formatting
  - knowledge.style-guide.international-style
last_updated: 2026-07-30
```

## Intent

This contract defines formatting for six numeric terms that don't belong
to any other numeric-formatting contract in this domain — aspect ratio,
fractions, version number, the resolution/speed "x" notation, step, and
zip code — when writing UI text, documentation, or example data for Apple
platforms.

## Scope

### Included

-   Aspect ratio notation (colon-separated)
-   Fraction spelling-out and hyphenation
-   Version number formatting and comparison wording
-   The letter "x" used for resolution, placeholders, version ranges, and speed
-   Capitalization of "step" in step-by-step instructions
-   Capitalization of "zip code"

### Excluded

-   GB, inch, mm, percent, and degree formatting (see `units-of-measure`)
-   Dates, time of day, time zones, and a.m./p.m. (see `international-formatting`, Rule 1)
-   Phone number formatting (see `international-style`, Rule 4)

This contract is deliberately narrow: it covers only the six numeric terms
above. Agents MUST NOT extend it to any numeric term owned by the three
related contracts listed above.

## Rules

### Rule 1

Agents MUST use a colon, not "by" or "x," to express an aspect ratio, e.g.
"4:3," "16:9."

### Rule 2

In user materials, agents MUST spell out a fraction whose denominator is
10 or lower, except in specification lists, technical appendixes, or
tables, and MUST hyphenate the spelled-out form, e.g. "one-fifth,"
"three-fourths." When expressing a noninteger greater than 1, agents MUST
use a mixed numeral rather than an improper fraction, e.g. "1 1/6," not
"7/6."

### Rule 3

Agents MUST NOT include the word "version" or the letter "v" when citing a
software version alongside a product name, e.g. "Keynote 15.2," not
"Keynote version 15.2." Agents MUST omit a trailing ".0" from a major
release number unless needed for clarity, and MUST use "earlier" or
"later," not "lower," "higher," "newer," or "older," to describe a version
range. When listing multiple operating systems that share one version
number, agents MUST repeat the version number after each OS name rather
than placing it only at the end of the list.

### Rule 4

Agents MUST use a lowercase "x" with a space on both sides for screen
resolutions, e.g. "1024 x 768," and a lowercase "x" with no space for
optical-drive speed, e.g. "24x speed." Except in developer materials,
agents MUST NOT use "x" to express a range of version numbers (e.g.
"15.x"); use a specific number or range instead.

### Rule 5

Agents MUST NOT capitalize "step," even in a specific reference, e.g.
"step 1," "steps 1 and 2."

### Rule 6

Agents MUST use lowercase for "zip code."

## Compliant Example

-   ✓ "The video uses a 16:9 aspect ratio." (Rule 1)
-   ✓ "This app uses one-fifth of available memory." / "1 1/6 GB free" (Rule 2)
-   ✓ "Compressor 5 includes support for Apple Immersive Video packaging." (Rule 3)
-   ✓ "You need iOS 26, iPadOS 26, or later." (Rule 3)
-   ✓ "1024 x 768" / "24x speed" (Rule 4)
-   ✓ "Complete step 1, then continue to step 2." (Rule 5)
-   ✓ "Enter your zip code." (Rule 6)

## Non-Compliant Example

-   ✗ "The video is 16 by 9." or "16x9" for an aspect ratio (Rule 1)
-   ✗ "7/6 of the available space" (Rule 2)
-   ✗ "Keynote version 15.2" / "iOS, iPadOS, or macOS 26 or later" (Rule 3)
-   ✗ "1024x768" with no spaces / "15.x" outside developer materials (Rule 4)
-   ✗ "Complete Step 1, then continue to Step 2." (Rule 5)
-   ✗ "Enter your Zip Code." or "ZIP code" (Rule 6)

## Dependencies

None.

## References

-   [Apple Style Guide — aspect ratio (p. 33)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — fractions (p. 90)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — version number (p. 213)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — x (p. 221)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — step (p. 192)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — zip code (p. 222)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
