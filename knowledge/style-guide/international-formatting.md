# International Formatting

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.international-formatting
artifact_type: knowledge
title: International Formatting
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for formatting dates, times, decimal numbers, and unit-of-measure quantities using standard international conventions in Apple platform UI and documentation text.
domain: Style Guide
tags:
  - style-guide
  - international
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.international-style
  - knowledge.style-guide.units-of-measure
  - knowledge.style-guide.numeric-terminology-supplement
last_updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent formats dates, times, decimal
numbers, and unit-of-measure quantities using standard international
conventions when writing UI text, documentation, or example data for Apple
platforms. It covers locale-neutral formatting of numeric values — how
digits, separators, and symbols are arranged — as a companion to
`knowledge/style-guide/international-style.md`, which covers international
representation of countries, currencies, languages, and telephone numbers.
Agents SHOULD vary from these standard conventions only when there's a
truly compelling advantage to a proprietary or customary style.

## Scope

### Included

-   Date format order and separators (ISO 8601)
-   Time format, 24-hour clock notation, and UTC/time-zone offsets
-   Decimal separator conventions and grouping of large numbers
-   Nonbreaking-space usage between a quantity and its unit symbol
-   Presenting equivalent non-SI values alongside SI values

### Excluded

-   Country, currency, and language codes and telephone number formatting
    (see `knowledge/style-guide/international-style.md`)
-   Unit-of-measure naming, spelled-out-vs.-abbreviated usage,
    capitalization, and prefix/symbol-mixing rules (see
    `knowledge/style-guide/units-of-measure.md`) — this contract covers only
    how unit quantities are numerically formatted, not how unit names are
    chosen or spelled

## Rules

### Rule 1

Agents MUST express dates numerically as year, month, day, separated by
hyphens (ISO 8601), e.g. "2025-09-09." Agents MUST express times on a
24-hour clock with a colon separating hours, minutes, and seconds. Agents
MUST express Coordinated Universal Time (UTC) as "Z" and MUST express local
time zones as the number of hours offset from UTC, e.g. "(UTC–8)."

### Rule 2

Agents MUST use a period to produce a decimal point in English-language
content. For numbers larger than 999, agents MUST NOT use a period or comma
as a digit-grouping separator; agents MAY use a nonbreaking space
(Option-Space bar) to divide digits into groups of three for readability.
Agents SHOULD express large numbers in their smallest, easiest-to-read
form (e.g. "3.7 million" rather than "3700000").

### Rule 3

Agents MUST use a nonbreaking space (Option-Space bar), not a plain space,
between a quantity and its unit symbol, so the pair never breaks across a
line. Agents MAY give an equivalent non-SI value in parentheses following
an SI value. (Pluralization, hyphenation, and trailing-period rules for
unit symbols are covered by `knowledge/style-guide/units-of-measure.md`;
this rule governs only the spacing character used between a numeric
quantity and its unit symbol in international-formatted text.)

### Rule 4

Agents MUST express quantities using only International System of Units
(SI) units as the primary value; a non-SI equivalent MAY be added per Rule
3 but MUST NOT replace the SI value. Agents MUST NOT imply more precision
than is reasonable when choosing a unit symbol or decimal precision (e.g.,
prefer "about 1.2 km" over "1.19987 km" when the source value is not
precise to that many digits).

## Compliant Example

-   ✓ "Apple Watch Series 11 was introduced on 2025-09-09." (Rule 1)
-   ✓ "The file will be posted at 18:00Z." / "18:00 PST (UTC–8)" (Rule 1)
-   ✓ "Apple sold 300 000 iMac computers in the first quarter." / "Apple sold 3.7 million iMac computers in 2 years." (Rule 2)
-   ✓ "MacBook Neo weighs 1.23 kg" with a nonbreaking space before "kg" / "iPad mini (A17 Pro) Wi-Fi models weigh 293 g (0.65 lb.)." (Rule 3)
-   ✓ "The trailhead is about 1.2 km away." (Rule 4)

## Non-Compliant Example

-   ✗ "09/09/2025" for a date, ambiguous between month-day and day-month order (Rule 1)
-   ✗ "6:00 PM" instead of 24-hour time / "18:00 GMT" instead of "18:00Z" for UTC (Rule 1)
-   ✗ "300,000 iMac computers" or "300.000 iMac computers" using a period or comma as a thousands separator (Rule 2)
-   ✗ "1.23 kg" using a plain breaking space that could split "1.23" from "kg" across a line (Rule 3)
-   ✗ "The trailhead is 1.19987 km away." implying false precision (Rule 4)
-   ✗ "MacBook Neo weighs 2.7 lb." given as the only value with no SI equivalent (Rule 4)

## Dependencies

None.

## References

-   [Apple Style Guide — International style: Dates and times (p. 241)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — International style: Decimals (p. 241)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — International style: Units of measure (p. 243)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
