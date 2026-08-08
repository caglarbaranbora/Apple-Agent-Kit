# International Style

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.international-style
artifact_type: knowledge
title: International Style
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for representing countries, currencies, languages, and telephone numbers using standard international codes and conventions in Apple platform UI and documentation text.
domain: Style Guide
tags:
  - style-guide
  - international
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.international-formatting
  - knowledge.style-guide.units-of-measure
  - knowledge.style-guide.numeric-terminology-supplement
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent represents countries,
currencies, languages, and telephone numbers using standard international
conventions when writing UI text, documentation, or example data for Apple
platforms. Following international style helps readers with limited English
proficiency and helps human and machine translators localize the content by
minimizing cultural and customary language burdens. Agents SHOULD write in
simple structures, SHOULD NOT use idiomatic or colloquial expressions, and
SHOULD NOT use shortcuts, symbols, or abbreviations that could easily be
spelled out, varying from the standard conventions in this contract only
when there's a truly compelling advantage to a proprietary or customary
style.

## Scope

### Included

-   Representing country names with ISO 3166 codes
-   Expressing currency amounts with ISO 4217 codes
-   Representing language names with ISO 639 codes, including Apple
    localization extensions
-   Formatting telephone numbers for international dialing

### Excluded

-   Date and time formatting, decimal formatting, and unit-of-measure value
    formatting (see `knowledge/style-guide/international-formatting.md`)
-   Unit-of-measure naming, abbreviation, and pluralization rules (see
    `knowledge/style-guide/units-of-measure.md`)
-   Full ISO/ITU code reference tables

## Rules

### Rule 1

Agents MUST represent country names using the two-character ISO 3166 code
in a table, column, or row that clearly indicates the code represents a
country, e.g. "DE" for Germany, "JP" for Japan, "US" for United States.

### Rule 2

Agents MUST express currency amounts by writing the numeric amount followed
by a space and the three-letter ISO 4217 currency code in capitals (e.g.
"1199 USD"). Agents MUST NOT use currency symbols such as "$" in place of
the code, because such symbols aren't unique and are easily misread.

### Rule 3

Agents MUST represent language names using the two-character ISO 639 code
in a table, column, or row that clearly indicates the code represents a
language, e.g. "en" for English, "de" for German. Agents MUST append the
appropriate regional extension to the code when representing a particular
Apple localization, e.g. "en-GB" for British English, "zh-CN" for Simplified
Chinese, "zh-TW" for Traditional Chinese.

### Rule 4

Agents MUST format telephone numbers beginning with the plus sign ("+"),
followed by the country code, the city code, and the number, using spaces
to represent breaks in national numbering plans. Agents MUST express
freephone (toll-free) numbers in the local style and MUST always provide a
toll number alongside a freephone number when one is available.

## Compliant Example

-   ✓ "DE" used in a country column instead of "Germany" (Rule 1)
-   ✓ "The computer is priced at 1199 USD." / "The computer costs 1980 EUR." (Rule 2)
-   ✓ "en-GB" for British English content, "en" for a generic English table row (Rule 3)
-   ✓ "+1 408 996 1010 or 800-692-7753 (in North America)" (Rule 4)

## Non-Compliant Example

-   ✗ "Germany" spelled out in a column of two-character country codes (Rule 1)
-   ✗ "$1199" or "€1980" used in place of an ISO 4217 code (Rule 2)
-   ✗ "en" used to label British-English-specific localized content (Rule 3)
-   ✗ "(408) 996-1010" with no plus sign or country code (Rule 4)

## Dependencies

None.

## References

-   [Apple Style Guide — International style: Countries (p. 239)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — International style: Currency (p. 240)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — International style: Languages (p. 242)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — International style: Telephone numbers (p. 243)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
