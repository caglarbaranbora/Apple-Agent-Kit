# Async Data Fetching

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.async-data-fetching
type: knowledge
title: Async Data Fetching
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of URLSession's async/await data(for:), upload(for:from:), and download(for:) APIs, and why a successful call does not by itself mean the server returned success.
domain: Networking
tags:
  - networking
  - urlsession
  - async-await
references:
  - https://developer.apple.com/documentation/foundation/urlsession/data(for:delegate:)
  - https://developer.apple.com/documentation/foundation/urlsession
depends_on:
  - knowledge.networking.url-request-construction
related:
  - knowledge.networking.http-error-handling
  - knowledge.networking.url-request-construction
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent fetches data over the
network using `URLSession`'s structured-concurrency APIs, and the
critical distinction between a call *throwing* (transport-level failure)
and a call *succeeding* with an HTTP error status (which still requires
explicit checking).

## Scope

### Included

-   `URLSession.shared.data(for:)`, `upload(for:from:)`, `download(for:)`
    with `async`/`await`
-   Why a non-throwing call does not guarantee an HTTP 2xx response

### Excluded

-   Building the `URLRequest` itself — see `url-request-construction`
-   Checking the response's status code — see `http-error-handling`
-   Completion-handler-based `dataTask` APIs and Combine's
    `dataTaskPublisher` — out of v1 scope

## Rules

### Rule 1

Agents MUST use `URLSession.shared.data(for: request)` (or a
custom-configured session's `data(for:)`) when custom headers or a
non-GET method are needed, rather than `data(from: url)` — `data(from:)`
only accepts a `URL`, with no way to set headers or an HTTP method.

### Rule 2

Agents MUST treat a successful (non-throwing) `data(for:)` call as
meaning only that the transport layer completed — the server may still
have returned an HTTP error status (404, 500, etc.) in the same
response; agents MUST check the response's status code (see
`http-error-handling`) before treating the call as a business-level
success.

### Rule 3

Agents SHOULD use `download(for:)` instead of `data(for:)` when fetching
a large file that will be written to disk — `download(for:)` streams
directly to a temporary file URL rather than buffering the entire
response in memory as `Data`.

### Rule 4

Agents MUST NOT assume `data(for:)` throwing means the server is
unreachable — it also throws for a cancelled task
(`URLError.cancelled`), so the catch block must distinguish cancellation
from an actual transport failure before showing a network-error message
to the user (see `task-cancellation`).

## Compliant Example

```swift
func fetchUsers(from request: URLRequest) async throws -> Data {
    let (data, response) = try await URLSession.shared.data(for: request)
    guard let httpResponse = response as? HTTPURLResponse,
          (200...299).contains(httpResponse.statusCode) else {
        throw NetworkError.badStatus
    }
    return data
}
```
Transport success and HTTP status are checked separately — the throwing call only confirms transport completion, the status-code check confirms business-level success. (Rules 1, 2)

## Non-Compliant Example

```swift
func fetchUsers(from request: URLRequest) async throws -> Data {
    let (data, _) = try await URLSession.shared.data(for: request)
    return data
}
```
The response is discarded entirely — a 404 or 500 response returns non-throwing `Data` (e.g. an HTML error page or empty body) that gets treated as a successful payload. (Rule 2)

## Dependencies

- `knowledge.networking.url-request-construction` — a request must be built before it can be fetched.

## References

-   [Apple Developer — URLSession.data(for:delegate:)](https://developer.apple.com/documentation/foundation/urlsession/data(for:delegate:))
-   [Apple Developer — URLSession](https://developer.apple.com/documentation/foundation/urlsession)
