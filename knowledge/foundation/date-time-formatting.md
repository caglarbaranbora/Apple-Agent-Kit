# Date/Time Formatting

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.foundation.date-time-formatting
type: knowledge
title: Date/Time Formatting
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of DateFormatter, ISO8601DateFormatter, Date.FormatStyle, and RelativeDateTimeFormatter, including the formatter-reuse performance rule.
domain: Foundation
tags:
  - foundation
  - dateformatter
  - date-formatstyle
  - relativedatetimeformatter
references:
  - https://developer.apple.com/documentation/foundation/dateformatter
  - https://developer.apple.com/documentation/foundation/iso8601dateformatter
  - https://developer.apple.com/documentation/foundation/date/formatstyle
  - https://developer.apple.com/documentation/foundation/relativedatetimeformatter
depends_on: []
related:
  - knowledge.style-guide.units-of-measure
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent formats and parses dates and
times using Foundation's formatters: choosing `DateFormatter` vs.
`ISO8601DateFormatter` vs. `Date.FormatStyle` for the task at hand,
avoiding the well-documented performance cost of re-creating formatters
per call, and producing correctly-worded relative time strings with
`RelativeDateTimeFormatter`.

## Scope

### Included

-   `DateFormatter` for user-visible and fixed-format (e.g. RFC 3339)
    date/time strings, including `dateStyle`/`timeStyle`/`dateFormat`
-   `ISO8601DateFormatter` for ISO 8601 string round-tripping
-   `Date.FormatStyle` and `.formatted()` (iOS 15+/Swift 5.5+) for
    locale-aware formatting and parsing
-   Caching/reusing formatter instances instead of allocating one per call
-   `RelativeDateTimeFormatter` for relative strings ("2 hours ago")

### Excluded

-   Locale-specific unit conversion and `MeasurementFormatter` — see
    `measurement-and-unit-formatting.md`
-   Unit-of-measure copy wording once a value is already display text —
    see `knowledge.style-guide.units-of-measure`
-   `Calendar` and `DateComponents` arithmetic beyond what a formatter needs
-   Locale/Bundle translation workflow mechanics — deferred to the future
    `localization` domain (Tier 2, unbuilt)

## Rules

### Rule 1

Agents MUST NOT create a new `DateFormatter` instance inside a loop, a
frequently-called function, or a table/list cell render path. Apple's
documentation states "creating a date formatter is not a cheap operation.
If you are likely to use a formatter frequently, it is typically more
efficient to cache a single instance than to create and dispose of
multiple instances." Cache the instance (a `static let`, a stored
property, or an injected shared instance) and reuse it.

### Rule 2

Agents MUST use `ISO8601DateFormatter` (or `Date.FormatStyle`'s `.iso8601`
variants) rather than a hand-configured `DateFormatter` with a manual
`dateFormat` string when producing or parsing ISO 8601 dates —
`ISO8601DateFormatter` "generates and parses string representations of
dates following the ISO 8601 standard" without the locale/timezone
misconfiguration risk of a hand-rolled format string.

### Rule 3

Agents SHOULD prefer `Date.FormatStyle`/`.formatted()` over `DateFormatter`
for new code targeting iOS 15+/Swift 5.5+ when producing user-visible
date/time strings, since it "shares the date and time formatting pattern
preferred by the user's locale" and supports round-trip parsing via
`Date(_:strategy:)` with the same style instance. `DateFormatter` remains
correct for earlier deployment targets or fixed-format strings (e.g. RFC
3339) requiring a `dateFormat` string with a POSIX locale.

### Rule 4

Agents MUST use `RelativeDateTimeFormatter` — not manual string
interpolation — to produce relative date/time strings, and MUST treat its
output ("1 hour ago", "in 2 weeks") as a standalone string. Per Apple's
documentation, "embedding them in other strings may not be grammatically
correct" across all locales, so agents MUST NOT concatenate the formatted string into a larger sentence.

### Rule 5

When caching a `DateFormatter`, `ISO8601DateFormatter`, or a
`Date.FormatStyle`-backed value that depends on the current locale or time
zone, agents MUST account for locale/time-zone changes while the app is
running (e.g. by not treating a cached instance as valid forever across a
locale change) rather than assuming a one-time-created formatter stays
correct for the app's full lifetime.

## Compliant Example

```swift
enum DateFormatting {
    static let iso8601 = ISO8601DateFormatter()
}

func renderTimestamp(_ date: Date) -> String {
    DateFormatting.iso8601.string(from: date) // Reused instance (Rule 1, 2).
}

func relativeLabel(for date: Date) -> String {
    let formatter = RelativeDateTimeFormatter()
    return formatter.localizedString(for: date, relativeTo: .now) // Standalone string (Rule 4).
}
```
Caches a shared `ISO8601DateFormatter` instead of allocating one per call, and uses `RelativeDateTimeFormatter`'s output as a standalone label rather than embedding it in a larger sentence. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
func renderRow(for date: Date) -> String {
    let formatter = DateFormatter() // Allocated on every call.
    formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ssZ"
    return "Posted " + formatter.string(from: date) + " ago" // Manually built relative phrase.
}
```
Allocates a new `DateFormatter` on every row render instead of reusing a cached instance (Rule 1), hand-rolls an ISO-8601-like format string instead of using `ISO8601DateFormatter` (Rule 2), and fabricates a relative-time phrase manually instead of using `RelativeDateTimeFormatter` (Rule 4).

## Dependencies

None.

## References

-   [Apple Developer — DateFormatter](https://developer.apple.com/documentation/foundation/dateformatter)
-   [Apple Developer — ISO8601DateFormatter](https://developer.apple.com/documentation/foundation/iso8601dateformatter)
-   [Apple Developer — Date.FormatStyle](https://developer.apple.com/documentation/foundation/date/formatstyle)
-   [Apple Developer — RelativeDateTimeFormatter](https://developer.apple.com/documentation/foundation/relativedatetimeformatter)
-   [Apple Developer (Archive) — Caching Date Formatters for Performance](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/DataFormatting/Articles/dfDateFormatting10_4.html)
