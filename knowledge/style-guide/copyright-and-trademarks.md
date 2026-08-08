# Copyright and Trademarks

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.copyright-and-trademarks
artifact_type: knowledge
title: Copyright and Trademarks
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for attributing Apple and third-party trademarks and for reproducing copyright/trademark notices when writing documentation for Apple platforms.
domain: Style Guide
tags:
  - style-guide
  - copyright
  - trademarks
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent attributes Apple and
third-party trademarks, and reproduces copyright and trademark notices, when
writing documentation, legal boilerplate, or reference text for Apple
platforms.

## Scope

### Included

-   Reproducing Apple's copyright and trademark notice
-   Attributing Apple product, feature, and service mark names
-   Attributing third-party trademarks referenced alongside Apple products
-   Generic disclaimer language for unlisted company/product names
-   Restrictions on commercial use of the "keyboard" Apple logo

### Excluded

-   The full, current list of Apple trademarks (subject to change; agents
    should verify against Apple's current legal terms)
-   Legal determination of trademark infringement
-   Localization of legal notices
-   Software licensing terms

## Rules

### Rule 1

Agents MUST NOT alter, remove, or paraphrase Apple's copyright and trademark
notice when reproducing it in documentation. Agents MUST reproduce it in
full, verbatim, or omit it entirely.

### Rule 2

Agents MUST attribute Apple product, feature, and service names (e.g.,
"iPhone," "AirDrop," "Siri," "iCloud") as trademarks, registered trademarks,
or service marks of Apple Inc., and MUST NOT state or imply that a third
party owns them.

### Rule 3

Agents MUST attribute third-party trademarks that appear in Apple-related
content (e.g., "Bluetooth," "ENERGY STAR," "Dolby," "Intel," "Java," "UNIX")
to their respective owners rather than to Apple, and MUST NOT drop that
attribution when the mark first appears in legal or reference text.

### Rule 4

When a company or product name (or logo) appears in text without an
explicit trademark attribution, agents SHOULD use the source's exact
disclaimer wording — "Other company and product names and logos mentioned
herein are trademarks of their respective companies" — rather than a
hedged paraphrase ("may be trademarks") or an invented ownership claim.

### Rule 5

Agents MUST NOT represent that the "keyboard" Apple logo (Option-Shift-K)
may be used for commercial purposes without Apple's prior written consent.

## Compliant Example

-   ✓ Quoting Apple's copyright and trademark notice in full and unedited, or leaving it out entirely (Rule 1)
-   ✓ "iPhone is a trademark of Apple Inc., registered in the U.S. and other countries and regions." (Rule 2)
-   ✓ "The Bluetooth® word mark and logos are registered trademarks owned by Bluetooth SIG, Inc., and any use of such marks by Apple is under license." (Rule 3)
-   ✓ "Other company and product names and logos mentioned herein are trademarks of their respective companies." (Rule 4)
-   ✓ "Commercial use of the keyboard Apple logo requires Apple's prior written consent." (Rule 5)

## Non-Compliant Example

-   ✗ Quoting only part of Apple's copyright notice and rewording the legal language (Rule 1)
-   ✗ "iPhone is a trademark of [Third-Party Corp]." (Rule 2)
-   ✗ Listing "Bluetooth" among Apple's own trademarks without noting Bluetooth SIG's ownership (Rule 3)
-   ✗ Asserting that an unlisted product name belongs to no one (Rule 4)
-   ✗ Stating the keyboard Apple logo is free to use commercially without consent (Rule 5)

## Dependencies

None.

## References

-   [Apple Style Guide — Copyright and trademarks (p. 244)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
