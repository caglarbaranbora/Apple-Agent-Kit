# Codable Decoding

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.codable-decoding
artifact_type: knowledge
title: Codable Decoding
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct use of JSONDecoder to decode network response data into Codable types, including decoding-strategy configuration and DecodingError handling.
domain: Networking
tags:
  - networking
  - codable
  - jsondecoder
references:
  - https://developer.apple.com/documentation/foundation/jsondecoder
  - https://developer.apple.com/documentation/swift/decodingerror
depends_on:
  - knowledge.networking.async-data-fetching
related:
  - knowledge.networking.async-data-fetching
  - knowledge.networking.url-request-construction
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent decodes network response
`Data` into `Codable` types with `JSONDecoder` — configuring decoding
strategies to match the server's actual JSON shape, and handling decode
failures explicitly rather than crashing.

## Scope

### Included

-   `JSONDecoder.decode(_:from:)`
-   `keyDecodingStrategy` and `dateDecodingStrategy` configuration
-   `DecodingError` case handling

### Excluded

-   Fetching the `Data` being decoded — see `async-data-fetching`
-   Encoding a request body — see `url-request-construction`

## Rules

### Rule 1

Agents MUST wrap `JSONDecoder.decode(_:from:)` in `do`/`catch` (or an
equivalent `try?`/`Result`-based handling with explicit error surfacing)
rather than force-unwrapping or ignoring failures — malformed or
unexpected server JSON is a routine occurrence, not an exceptional
programmer error.

### Rule 2

Agents MUST set `dateDecodingStrategy` explicitly to match the server's
actual date format (e.g. `.iso8601` for ISO 8601 strings) rather than
relying on the default `.deferredToDate`, which expects a `Double`
representing seconds since 2001 — a mismatched strategy fails to decode
every date field in the payload, not just malformed ones.

### Rule 3

Agents SHOULD set `keyDecodingStrategy = .convertFromSnakeCase` when the
server consistently uses `snake_case` JSON keys against Swift's
`camelCase` properties, and fall back to explicit `CodingKeys` only for
keys that don't follow that pattern uniformly — avoids hand-writing a
`CodingKeys` case for every property when a single decoder-wide setting
covers the common case.

### Rule 4

Agents MUST NOT use `try!` on a `JSONDecoder.decode(_:from:)` call in
production code — an API response that doesn't match the expected shape
(a common occurrence: added/removed fields, an error payload instead of
the expected type) crashes the app instead of surfacing a handleable
`DecodingError`.

## Compliant Example

```swift
struct User: Decodable {
    let id: Int
    let displayName: String
    let joinedAt: Date
}

func decodeUsers(from data: Data) throws -> [User] {
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    decoder.dateDecodingStrategy = .iso8601
    do {
        return try decoder.decode([User].self, from: data)
    } catch let error as DecodingError {
        throw NetworkError.decodingFailed(error)
    }
}
```
Decoding strategies explicitly matched to the server's format, decode failure caught and wrapped rather than crashing. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
func decodeUsers(from data: Data) -> [User] {
    try! JSONDecoder().decode([User].self, from: data)
}
```
Force-unwrapped decode with no decoding-strategy configuration — a server error payload or an unexpected date format crashes the app instead of producing a catchable error. (Rules 1, 2, 4)

## Dependencies

- `knowledge.networking.async-data-fetching` — decoding operates on `Data` already fetched from the network.

## References

-   [Apple Developer — JSONDecoder](https://developer.apple.com/documentation/foundation/jsondecoder)
-   [Apple Developer — DecodingError](https://developer.apple.com/documentation/swift/decodingerror)
