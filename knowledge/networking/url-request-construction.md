# URL Request Construction

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.url-request-construction
artifact_type: knowledge
title: URL Request Construction
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct construction of a URLRequest — HTTP method, headers, body, and safe query-string building via URLComponents.
domain: Networking
tags:
  - networking
  - urlrequest
  - urlcomponents
references:
  - https://developer.apple.com/documentation/foundation/urlrequest
  - https://developer.apple.com/documentation/foundation/urlcomponents
depends_on: []
related:
  - knowledge.networking.async-data-fetching
  - knowledge.networking.authenticated-requests
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent builds a `URLRequest` —
setting the HTTP method, headers, and body, and constructing any query
string safely — so a request is well-formed before it's ever sent.

## Scope

### Included

-   `URLRequest` construction: `httpMethod`, headers, `httpBody`
-   `URLComponents` for safe query-string building
-   `Content-Type` header requirements when sending a body

### Excluded

-   Actually sending the request and reading a response — see `async-data-fetching`
-   Attaching an `Authorization` header — see `authenticated-requests`

## Rules

### Rule 1

Agents MUST build a URL's query string with `URLComponents` and
`URLQueryItem`, not by interpolating raw values into a URL string —
`URLComponents` percent-encodes each value deterministically and
guarantees it stays scoped to its own parameter. Manual interpolation is
unsafe: a value containing `&` gets silently split into extra,
unintended query parameters instead of staying part of the original
value's contents, and other reserved characters depend on the URL
parser's undocumented leniency rather than a guaranteed encoding.

### Rule 2

Agents MUST set `httpMethod` explicitly on a `URLRequest` for any
non-GET request — `URLRequest.httpMethod` defaults to `"GET"`; omitting
it on an intended `POST`/`PUT`/`DELETE`/`PATCH` request silently sends
the wrong verb.

### Rule 3

Agents MUST set the `Content-Type` header (e.g.
`"application/json"`) via `setValue(_:forHTTPHeaderField:)` whenever
`httpBody` is set — the server cannot infer the body's encoding from
`Data` alone; a missing or wrong `Content-Type` causes the server to
reject or misparse an otherwise well-formed body.

### Rule 4

Agents SHOULD use `setValue(_:forHTTPHeaderField:)` (which replaces any
existing value for that field) rather than `addValue(_:forHTTPHeaderField:)`
(which appends) for headers that should have exactly one value, such as
`Content-Type` or `Accept` — `addValue` is for headers that legitimately
support multiple values (e.g. `Accept-Language`).

## Compliant Example

```swift
func makeSearchRequest(query: String, baseURL: URL) -> URLRequest? {
    var components = URLComponents(url: baseURL, resolvingAgainstBaseURL: false)
    components?.queryItems = [URLQueryItem(name: "q", value: query)]
    guard let url = components?.url else { return nil }

    var request = URLRequest(url: url)
    request.httpMethod = "GET"
    request.setValue("application/json", forHTTPHeaderField: "Accept")
    return request
}
```
Query value passed through `URLQueryItem` (safely encoded), HTTP method set explicitly, header set with `setValue`. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
func makeSearchRequest(query: String, baseURL: URL) -> URLRequest {
    let url = URL(string: "\(baseURL.absoluteString)?q=\(query)")!
    return URLRequest(url: url)
}
```
Query value interpolated directly into the URL string — a query value containing `&` gets split into extra, unintended query parameters instead of staying part of the original value, and `httpMethod` is left at the default `"GET"` with no explicit statement of intent. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — URLRequest](https://developer.apple.com/documentation/foundation/urlrequest)
-   [Apple Developer — URLComponents](https://developer.apple.com/documentation/foundation/urlcomponents)
