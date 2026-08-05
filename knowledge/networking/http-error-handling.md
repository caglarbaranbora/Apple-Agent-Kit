# HTTP Error Handling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.http-error-handling
type: knowledge
title: HTTP Error Handling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines checking HTTPURLResponse status codes, handling URLError transport failures, and unifying transport/HTTP-status/decoding failures behind a single custom error type.
domain: Networking
tags:
  - networking
  - error-handling
  - httpurlresponse
references:
  - https://developer.apple.com/documentation/foundation/httpurlresponse
  - https://developer.apple.com/documentation/foundation/urlerror
depends_on:
  - knowledge.networking.async-data-fetching
related:
  - knowledge.networking.async-data-fetching
  - knowledge.networking.authenticated-requests
  - knowledge.networking.codable-decoding
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent distinguishes and handles
the three distinct failure categories a network call can produce —
transport-level failure (`URLError`), an HTTP error status
(`HTTPURLResponse.statusCode` outside 2xx), and a decoding failure
(`DecodingError`) — behind one unified error type, so calling code
doesn't need to know about `URLSession`-specific types.

## Scope

### Included

-   Casting `URLResponse` to `HTTPURLResponse` and checking `statusCode`
-   `URLError` case handling (`.notConnectedToInternet`, `.timedOut`,
    `.cancelled`, etc.)
-   Defining a unified custom error type spanning all three failure
    categories

### Excluded

-   Making the request itself — see `async-data-fetching`
-   Decoding a successful response body — see `codable-decoding`
-   Retry logic specific to authentication (401) — see `authenticated-requests`

## Rules

### Rule 1

Agents MUST cast `URLResponse` to `HTTPURLResponse` and check
`statusCode` is in `200...299` before treating a network call as
successful — the async `data(for:)` family only throws for
transport-level failures, never for an HTTP error status returned by the
server.

### Rule 2

Agents MUST distinguish `URLError` cases rather than treating every
thrown error identically — `.notConnectedToInternet`/`.networkConnectionLost`
suggest a retry-when-reconnected UI, `.timedOut` suggests a possible
retry, and `.cancelled` MUST NOT be surfaced as a failure at all (see
`task-cancellation`).

### Rule 3

Agents SHOULD define an app-specific error type (e.g. a `NetworkError`
enum) that wraps all three failure categories — transport (`URLError`),
HTTP status, and decoding (`DecodingError`) — rather than propagating
`URLSession`-specific types directly to UI-layer or business-logic code,
so consumers of the network layer depend on one stable error type.

### Rule 4

Agents MUST NOT treat every thrown error as automatically retryable —
`.cancelled` must never be retried (it reflects deliberate cancellation,
not failure), and a 4xx HTTP status (client error, e.g. malformed
request or 404) should not be retried unchanged, unlike a 5xx status or
a transient `URLError`.

## Compliant Example

```swift
enum NetworkError: Error {
    case transport(URLError)
    case badStatus(Int)
    case decoding(DecodingError)
}

func checkResponse(_ response: URLResponse) throws {
    guard let httpResponse = response as? HTTPURLResponse else {
        throw NetworkError.badStatus(-1)
    }
    guard (200...299).contains(httpResponse.statusCode) else {
        throw NetworkError.badStatus(httpResponse.statusCode)
    }
}
```
A single `NetworkError` type spans all three failure categories; status-code checking happens explicitly rather than being inferred from whether the call threw. (Rules 1, 3)

## Non-Compliant Example

```swift
func fetchUsers() async throws -> [User] {
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode([User].self, from: data)
}
```
The response's status code is never checked — a 500 error response with an HTML error body gets passed straight to the decoder, producing a confusing `DecodingError` that masks the real HTTP failure. (Rule 1)

## Dependencies

- `knowledge.networking.async-data-fetching` — error handling applies to the result of a fetch.

## References

-   [Apple Developer — HTTPURLResponse](https://developer.apple.com/documentation/foundation/httpurlresponse)
-   [Apple Developer — URLError](https://developer.apple.com/documentation/foundation/urlerror)
