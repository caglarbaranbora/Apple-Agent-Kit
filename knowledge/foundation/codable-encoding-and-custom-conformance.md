# Codable Encoding and Custom Conformance

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.foundation.codable-encoding-and-custom-conformance
artifact_type: knowledge
title: Codable Encoding and Custom Conformance
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of JSONEncoder configuration and custom encode(to:)/init(from:) conformance for types needing non-synthesized Codable behavior.
domain: Foundation
tags:
  - foundation
  - codable
  - jsonencoder
  - encodable
references:
  - https://developer.apple.com/documentation/foundation/jsonencoder
  - https://developer.apple.com/documentation/swift/encodable
depends_on: []
related:
  - knowledge.networking.codable-decoding
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent encodes `Codable` types to
JSON with `JSONEncoder` and writes custom `encode(to:)`/`init(from:)
throws` conformance for types the compiler cannot synthesize (polymorphic
types, enums with associated values, nested/renamed keys) — general
Codable API mechanics. It does not cover decoding a network response's
`Data`, which `knowledge.networking.codable-decoding` owns; this contract's
rules apply regardless of where the resulting JSON goes or came from.

## Scope

### Included

-   `JSONEncoder.encode(_:)` and its strategy properties:
    `keyEncodingStrategy`, `dateEncodingStrategy`, `outputFormatting`
-   Writing custom `encode(to:) throws` / `init(from:) throws` for types
    needing non-synthesized conformance (polymorphic/nested types, enums
    with associated values)
-   `CodingKeys` customization for encoding (renaming, omitting properties)

### Excluded

-   `JSONDecoder`/`DecodingError` handling and fetching network response
    `Data` — see `knowledge.networking.codable-decoding`
-   `PropertyListEncoder` and non-JSON encoders

## Rules

### Rule 1

Agents MUST set `JSONEncoder.dateEncodingStrategy` explicitly (e.g.
`.iso8601`) when encoding `Date` properties for a consumer expecting a
specific format, rather than relying on the default `.deferredToDate`,
which encodes seconds since 2001 as a `Double`. Other strategies include `.secondsSince1970`, `.millisecondsSince1970`, `.formatted(DateFormatter)`, and `.custom` for cases `.iso8601` doesn't cover.

### Rule 2

Agents SHOULD set `keyEncodingStrategy = .convertToSnakeCase` when the
encoded JSON must use `snake_case` keys against Swift's `camelCase`
properties, rather than hand-writing a `CodingKeys` case per property —
reserve explicit `CodingKeys` for keys that don't follow that pattern
uniformly (e.g. one server-mandated name unrelated to its Swift property).

### Rule 3

Agents MUST write a custom `init(from: Decoder) throws` and
`encode(to: Encoder) throws` for any type the compiler cannot fully
synthesize `Codable` for — an enum with associated values encoded as a
discriminated JSON shape, a polymorphic type selecting its concrete case
from a type field, or a type whose JSON shape doesn't map 1:1 onto its
stored properties. Per Apple's documentation, `encode(to:)` "throws an
error if any values are invalid for the given encoder's format" — errors MUST be allowed to propagate (`throws`), not silenced.

### Rule 4

When a custom `init(from:)`/`encode(to:)` only needs to rename or omit a
subset of properties, agents SHOULD define a `CodingKeys` enum conforming
to `CodingKey` rather than hand-writing the full container logic per
property — this lets the compiler continue synthesizing the container
plumbing for keys that don't need custom handling.

### Rule 5

Agents MUST use `JSONEncoder.outputFormatting` to control JSON output
shape (`.prettyPrinted` for debug/log output, `.sortedKeys` for
deterministic key order in snapshot tests or content hashing,
`.withoutEscapingSlashes` when literal `/` must survive) rather than
post-processing the encoded `Data`/`String` with string manipulation.

## Compliant Example

```swift
enum Shape: Encodable {
    case circle(radius: Double)
    case square(side: Double)
    private enum CodingKeys: String, CodingKey { case type, radius, side }
    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        switch self {
        case .circle(let radius):
            try container.encode("circle", forKey: .type)
            try container.encode(radius, forKey: .radius)
        case .square(let side):
            try container.encode("square", forKey: .type)
            try container.encode(side, forKey: .side)
        }
    }
}
let encoder = JSONEncoder()
encoder.dateEncodingStrategy = .iso8601
encoder.outputFormatting = .sortedKeys
```
Custom `encode(to:)` for an associated-value enum the compiler can't synthesize, using `CodingKeys` for the discriminated shape, alongside an explicit `dateEncodingStrategy` and `outputFormatting` (Rules 1, 3, 4, 5).

## Non-Compliant Example

```swift
enum Shape {
    case circle(radius: Double)
    case square(side: Double)
}
// No Encodable conformance -- compiler can't synthesize one for an enum
// with associated values, so this type can't be encoded at all.
let encoder = JSONEncoder()
let data = try! encoder.encode(someDate) // Default strategy, force-tried.
```
Leaves an enum with associated values without the required custom `encode(to:)` (Rule 3), and encodes a `Date` with the default `.deferredToDate` strategy while force-trying the call instead of letting encode errors propagate (Rule 1, 3).

## Dependencies

None.

## References

-   [Apple Developer — JSONEncoder](https://developer.apple.com/documentation/foundation/jsonencoder)
-   [Apple Developer — Encodable](https://developer.apple.com/documentation/swift/encodable)
-   [Apple Developer — encode(to:)](https://developer.apple.com/documentation/swift/encodable/encode(to:))
-   [Apple Developer — JSONEncoder.DateEncodingStrategy](https://developer.apple.com/documentation/foundation/jsonencoder/dateencodingstrategy-swift.enum)
-   [Apple Developer — JSONEncoder.OutputFormatting](https://developer.apple.com/documentation/foundation/jsonencoder/outputformatting-swift.struct)
