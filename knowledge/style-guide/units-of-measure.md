# Units of Measure

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.units-of-measure
type: knowledge
title: Units of Measure
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for spelling out, abbreviating, formatting, and capitalizing units of measure in Apple platform UI and documentation text.
domain: Style Guide
tags:
  - style-guide
  - units-of-measure
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent formats units of measure —
spelling out vs. abbreviating, spacing, hyphenation, capitalization, and
symbol usage — when writing UI text, documentation, or example data for
Apple platforms.

## Scope

### Included

-   When to spell out a unit vs. use its symbol/abbreviation
-   Spacing and hyphenation around unit symbols and abbreviations
-   Capitalization of unit names and symbols
-   Pluralization, SI unit usage, and mixing of symbols/names/prefixes

### Excluded

-   Locale-specific unit conversion (e.g., metric vs. imperial defaults)
-   Currency formatting
-   Date and time formatting
-   Full prefix and unit symbol reference tables

## Rules

### Rule 1

Agents MUST spell out a unit of measure on first occurrence in user
documentation and give the abbreviation in parentheses, e.g. "20 gigabytes
(GB) of memory." Agents MAY use the abbreviation alone in subsequent
occurrences within the same section if it isn't obscure. Nonmetric units
MUST always be spelled out in running text (e.g., "17-inch display"); they
MAY be abbreviated in tables and technical specifications.

### Rule 2

When a unit symbol or abbreviation is used as a noun, agents MUST insert a
space between the number and the abbreviation and use "of" before the value
it quantifies, e.g. "20 GB of memory."

### Rule 3

When a spelled-out unit of measure forms a compound adjective, agents MUST
hyphenate the compound, e.g. "17-inch display," "3-meter cable." When a unit
symbol or abbreviation forms a compound adjective, agents MUST NOT
hyphenate it and MUST add a space instead, e.g. "20 nA battery," "30 GB
capacity."

### Rule 4

Agents MUST NOT capitalize a unit of measure derived from a proper name when
it is spelled out (e.g., "joule," "ampere"), except degrees Celsius,
Fahrenheit, and Rankine. Agents MUST capitalize the unit symbol for such
units when abbreviated (e.g., the symbol for joule is "J").

### Rule 5

Agents MUST NOT alter unit symbols or abbreviations in plural form, e.g.
"5 lb.," not "5 lbs."

### Rule 6

Agents MUST use the unit symbol for International System of Units (SI)
units after first occurrence, and SHOULD spell out "meter" if its symbol
could be confused with another term in context. Agents MUST NOT add a
period after an SI unit unless it falls at the end of a sentence.

### Rule 7

Agents MUST NOT mix a unit symbol with a unit name (e.g., "m/second"), and
MUST NOT mix a unit symbol with an abbreviation (e.g., "J/sec."). Agents
MUST NOT mix a prefix name with a unit symbol (e.g., "kiloHz"), or a prefix
symbol with a unit name (e.g., "khertz").

## Compliant Example

-   ✓ "20 gigabytes (GB) of memory" on first use, then "20 GB of memory" (Rule 1)
-   ✓ "20 GB of memory" (Rule 2)
-   ✓ "17-inch display" / "20 nA battery" (Rule 3)
-   ✓ "measured in joules (symbol: J)" / "20 degrees Celsius" (Rule 4)
-   ✓ "5 lb. of sugar" (Rule 5)
-   ✓ "The cable is 40 meters long." / "35 mm" with no trailing period (Rule 6)
-   ✓ "20 km/h" (Rule 7)

## Non-Compliant Example

-   ✗ "20GB of memory" used in body documentation text (Rule 1, Rule 2)
-   ✗ "17 inch display" / "20-nA battery" (Rule 3)
-   ✗ "Joule" / "20 degrees celsius" (Rule 4)
-   ✗ "5 lbs. of sugar" (Rule 5)
-   ✗ "35 mm." mid-sentence (Rule 6)
-   ✗ "m/second" / "J/sec." / "kiloHz" / "khertz" (Rule 7)

## Dependencies

None.

## References

-   [Apple Style Guide — Units of measure (p. 230)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
