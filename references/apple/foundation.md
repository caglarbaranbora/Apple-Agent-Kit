# Foundation

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: reference.apple.foundation
artifact_type: reference
title: Foundation
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's Foundation framework documentation, scoped to this domain's v1.
domain: Foundation
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/foundation/dateformatter
https://developer.apple.com/documentation/foundation/iso8601dateformatter
https://developer.apple.com/documentation/foundation/date/formatstyle
https://developer.apple.com/documentation/foundation/relativedatetimeformatter
https://developer.apple.com/documentation/foundation/measurement
https://developer.apple.com/documentation/foundation/measurementformatter
https://developer.apple.com/documentation/foundation/jsonencoder
https://developer.apple.com/documentation/swift/encodable
https://developer.apple.com/documentation/swift/decodable
https://developer.apple.com/documentation/foundation/filemanager
https://developer.apple.com/documentation/foundation/using-the-file-system-effectively
https://developer.apple.com/documentation/foundation/urlresourcevalues/isexcludedfrombackup

## Purpose

Reference index for Apple's Foundation framework documentation, scoped to
this domain's v1: a deliberately curated, highest-usage subset of Swift
Foundation's core data types and utilities — not an exhaustive Foundation
API reference (Foundation is enormous; see
`rfcs/0001-style-guide-domain-and-domain-roadmap.md` decision 9 for the
same curated-subset philosophy applied to another domain). v1 covers
exactly four topics: date/time formatting (`DateFormatter`,
`ISO8601DateFormatter`, `Date.FormatStyle`, `RelativeDateTimeFormatter`,
and the formatter-reuse performance pitfall); measurement and unit
formatting (`Measurement`, `.converted(to:)`, `MeasurementFormatter`);
Codable encoding and custom conformance (`JSONEncoder`, custom
`encode(to:)`/`init(from:)`, `CodingKeys`); and FileManager app sandbox
directories (`Documents`/`Caches`/`Application Support`, safe file I/O,
`isExcludedFromBackup`).

Explicitly out of scope for v1: general String/Unicode text processing,
`NotificationCenter`, the `Result` type, GCD/`DispatchQueue` (owned by a
future concurrency-focused domain), Locale/Bundle localization and
translation workflow mechanics (owned by the `localization` domain, built
2026-08), Combine (owned by the `combine` domain, built 2026-08, with
`dataTaskPublisher` specifically owned by `networking`), and
network-response `Codable` decoding (owned by
`networking`'s `codable-decoding.md`). Unit-of-measure UI copy wording
(spelling out vs. abbreviating, spacing, capitalization once a value is
already display text) is owned by `style-guide`'s `units-of-measure.md`;
this domain governs producing the locale-correct value/string via the API
in the first place.

## Primary Topics

- Date and time formatting
- Measurement and unit formatting
- Codable encoding and custom conformance
- FileManager app sandbox directories

## Used By

- knowledge/foundation/date-time-formatting.md ([[knowledge/foundation/date-time-formatting]])
- knowledge/foundation/measurement-and-unit-formatting.md ([[knowledge/foundation/measurement-and-unit-formatting]])
- knowledge/foundation/codable-encoding-and-custom-conformance.md ([[knowledge/foundation/codable-encoding-and-custom-conformance]])
- knowledge/foundation/filemanager-app-sandbox-directories.md ([[knowledge/foundation/filemanager-app-sandbox-directories]])
