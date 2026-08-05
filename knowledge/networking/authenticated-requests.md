# Authenticated Requests

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.authenticated-requests
type: knowledge
title: Authenticated Requests
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines attaching credentials to a network request via the Authorization header, a single-flight 401-triggered refresh-and-retry pattern, and never logging the raw header value.
domain: Networking
tags:
  - networking
  - authentication
  - authorization-header
references:
  - https://developer.apple.com/documentation/foundation/urlrequest/setvalue(_:forhttpheaderfield:)
depends_on:
  - knowledge.networking.url-request-construction
  - knowledge.networking.http-error-handling
related:
  - knowledge.authentication.authentication
  - knowledge.networking.http-error-handling
  - knowledge.networking.url-request-construction
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent attaches credentials to a
network request and reacts to an authentication-related HTTP failure —
the networking-mechanics half of authenticated API calls. Sign-in UX,
terminology, and flow are owned by the `authentication` domain; this
contract fills the "Authentication networking" gap that domain's own
Knowledge Contract explicitly excludes.

## Scope

### Included

-   Attaching credentials via the `Authorization` HTTP header
-   Single-flight 401-triggered token-refresh-and-retry pattern
-   Centralizing token attachment at one choke point
-   Not logging the raw credential/header value

### Excluded

-   Sign-in UX, terminology, and flow — see `knowledge.authentication.authentication`
-   Building the rest of the request — see `url-request-construction`
-   General (non-auth) HTTP status handling — see `http-error-handling`

## Rules

### Rule 1

Agents MUST attach credentials via the `Authorization` HTTP header
(e.g. `"Bearer <token>"`) using `setValue(_:forHTTPHeaderField:)`, never
via a URL query parameter — a token in a query parameter leaks into
server access logs, intermediate proxy logs, and can be exposed via
`Referer` headers on subsequent requests.

### Rule 2

Agents MUST implement a single-flight refresh-and-retry on a 401
response — refresh the token once and retry the original request once,
rather than retrying indefinitely — an unconditional retry loop on a
persistently invalid token spins forever or floods the auth server with
refresh attempts.

### Rule 3

Agents SHOULD centralize token attachment behind a single
helper/actor/request-builder rather than duplicating
`if let token = ...` header-setting logic at every call site — a single
choke point is the only place that needs updating if the token type or
auth scheme changes.

### Rule 4

Agents MUST NOT log the raw `Authorization` header value (or the token
itself) in application logs at any log level, including debug/verbose —
token leakage into logs (which may be persisted, shipped to a crash
reporter, or viewed by more people than intended) is a common source of
real security incidents.

## Compliant Example

```swift
actor TokenProvider {
    private var token: String
    private var isRefreshing = false

    func authorizedRequest(_ request: URLRequest) async throws -> URLRequest {
        var authedRequest = request
        authedRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        return authedRequest
    }

    func refreshOnce() async throws {
        guard !isRefreshing else { return }
        isRefreshing = true
        defer { isRefreshing = false }
        token = try await fetchRefreshedToken()
    }
}
```
Token attachment centralized in one actor; refresh is guarded against concurrent duplicate calls. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
func fetchProfile(token: String) async throws -> Data {
    let url = URL(string: "https://api.example.com/profile?access_token=\(token)")!
    print("Requesting with token: \(token)")
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}
```
Token passed as a URL query parameter (leaks into logs) and printed directly to the console. (Rules 1, 4)

## Dependencies

- `knowledge.networking.url-request-construction` — the `Authorization` header is set on an already-constructed request.
- `knowledge.networking.http-error-handling` — a 401 is detected via the same status-code-checking mechanism.

## References

-   [Apple Developer — URLRequest.setValue(_:forHTTPHeaderField:)](https://developer.apple.com/documentation/foundation/urlrequest/setvalue(_:forhttpheaderfield:))
