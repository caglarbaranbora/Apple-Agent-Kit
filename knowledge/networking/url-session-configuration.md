# URL Session Configuration

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.url-session-configuration
artifact_type: knowledge
title: URL Session Configuration
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when to create a custom URLSession with a configured URLSessionConfiguration versus using URLSession.shared, covering timeout, cache policy, and ephemeral (non-persistent) sessions.
domain: Networking
tags:
  - networking
  - urlsession
  - urlsessionconfiguration
references:
  - https://developer.apple.com/documentation/foundation/urlsessionconfiguration
depends_on: []
related:
  - knowledge.networking.async-data-fetching
last_updated: 2026-08-08
```

## Intent

This contract defines when an AI coding agent should create a custom
`URLSession` with a configured `URLSessionConfiguration` instead of
using `URLSession.shared`, and how to configure timeout, cache policy,
and persistence behavior correctly.

## Scope

### Included

-   `URLSessionConfiguration.default` vs. `.ephemeral`
-   `timeoutIntervalForRequest`/`timeoutIntervalForResource`
-   `requestCachePolicy`
-   Reusing a `URLSession` instance rather than creating one per request

### Excluded

-   `URLSessionConfiguration.background(withIdentifier:)` and
    delegate-based background transfers — see `background-transfers`
-   Making an individual request — see `async-data-fetching`

## Rules

### Rule 1

Agents MUST create a custom `URLSession` with an explicitly configured
`URLSessionConfiguration` when a request needs a non-default timeout,
cache policy, or ephemeral (non-persistent) behavior —
`URLSession.shared` uses `.default` configuration and cannot be
reconfigured after creation.

### Rule 2

Agents SHOULD use `.ephemeral` configuration for requests that must not
persist cookies, cache, or credentials to disk (e.g. a one-off request
handling a sensitive short-lived token) — `.ephemeral` keeps all session
data in memory only, cleared when the session is deallocated.

### Rule 3

Agents MUST set `timeoutIntervalForRequest` explicitly rather than
relying on the 60-second default when a request has a known tighter
latency requirement (e.g. an interactive autocomplete call that should
fail fast) — the default is tuned for general-purpose requests, not
latency-sensitive ones.

### Rule 4

Agents MUST NOT create a new `URLSession` instance for every individual
request when a single shared, appropriately configured session would
serve — each `URLSession` maintains its own connection pool; excessive
instantiation defeats connection reuse and wastes resources.

## Compliant Example

```swift
final class APIClient {
    private let session: URLSession

    init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 15
        self.session = URLSession(configuration: config)
    }

    func fetch(_ request: URLRequest) async throws -> (Data, URLResponse) {
        try await session.data(for: request)
    }
}
```
One configured `URLSession` instance is created once and reused for every request, with an explicit tighter timeout. (Rules 1, 3, 4)

## Non-Compliant Example

```swift
func fetch(_ request: URLRequest) async throws -> (Data, URLResponse) {
    let session = URLSession(configuration: .default)
    return try await session.data(for: request)
}
```
A new `URLSession` (with a new connection pool) is created on every call to this function, defeating connection reuse, with no reasoning given for not using `URLSession.shared`. (Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — URLSessionConfiguration](https://developer.apple.com/documentation/foundation/urlsessionconfiguration)
