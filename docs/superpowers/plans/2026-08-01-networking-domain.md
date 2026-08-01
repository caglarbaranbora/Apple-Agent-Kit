# Networking Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `networking` domain (1 Reference, 8 Knowledge Contracts, 1 native Skill) covering `URLSession` async/await HTTP networking — request construction, data fetching, Codable decoding, error handling, cancellation, session configuration, App Transport Security, and authenticated requests — per `docs/superpowers/specs/2026-08-01-networking-domain-design.md`, replacing the placeholder `networking` row in `docs/architecture/domain-map.md`.

**Architecture:** Mirrors the `sf-symbols` and `uikit` domains exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/networking.md`

**Files:**
- Create: `references/apple/networking.md`

- [ ] **Step 1: Create the file**

```markdown
# Networking

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/foundation/urlsession

## Purpose

Reference index for Apple's URLSession networking documentation, scoped
to this domain's v1: async/await HTTP networking — request construction,
structured-concurrency data fetching, Codable-based JSON decoding, error
handling, task cancellation, session configuration, App Transport
Security requirements, and authenticated request patterns. Completion-
handler-based `URLSession` APIs, Combine's `dataTaskPublisher`, and
`URLSessionDelegate`-based APIs (background transfers, progress
tracking, custom TLS/challenge handling) are deferred to a future pass.
Authentication UX/flow (sign-in terminology, entry points, form
accessibility) is owned by the `authentication` domain, not this one —
see docs/architecture/domain-map.md Cross-Domain Notes.

## Primary Topics

- URL request construction
- Async data fetching
- Codable decoding
- HTTP error handling
- Task cancellation
- URL session configuration
- App Transport Security
- Authenticated requests

## Used By

- knowledge/networking/url-request-construction.md ([[knowledge/networking/url-request-construction]])
- knowledge/networking/async-data-fetching.md ([[knowledge/networking/async-data-fetching]])
- knowledge/networking/codable-decoding.md ([[knowledge/networking/codable-decoding]])
- knowledge/networking/http-error-handling.md ([[knowledge/networking/http-error-handling]])
- knowledge/networking/task-cancellation.md ([[knowledge/networking/task-cancellation]])
- knowledge/networking/url-session-configuration.md ([[knowledge/networking/url-session-configuration]])
- knowledge/networking/app-transport-security.md ([[knowledge/networking/app-transport-security]])
- knowledge/networking/authenticated-requests.md ([[knowledge/networking/authenticated-requests]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/networking.md --type reference`
Expected: `PASS: references/apple/networking.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/networking.md
git commit -m "docs: add networking reference index"
```

---

## Task 2: Knowledge Contract — `url-request-construction`

**Files:**
- Create: `knowledge/networking/url-request-construction.md`

- [ ] **Step 1: Create the file**

```markdown
# URL Request Construction

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.url-request-construction
type: knowledge
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
updated: 2026-08-01
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/url-request-construction.md --type knowledge`
Expected: `PASS: knowledge/networking/url-request-construction.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/url-request-construction.md
git commit -m "feat: add url-request-construction knowledge contract"
```

---

## Task 3: Knowledge Contract — `async-data-fetching`

**Files:**
- Create: `knowledge/networking/async-data-fetching.md`

- [ ] **Step 1: Create the file**

```markdown
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/async-data-fetching.md --type knowledge`
Expected: `PASS: knowledge/networking/async-data-fetching.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/async-data-fetching.md
git commit -m "feat: add async-data-fetching knowledge contract"
```

---

## Task 4: Knowledge Contract — `codable-decoding`

**Files:**
- Create: `knowledge/networking/codable-decoding.md`

- [ ] **Step 1: Create the file**

```markdown
# Codable Decoding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.codable-decoding
type: knowledge
title: Codable Decoding
version: 0.1.0
status: Draft
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
related: []
updated: 2026-08-01
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/codable-decoding.md --type knowledge`
Expected: `PASS: knowledge/networking/codable-decoding.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/codable-decoding.md
git commit -m "feat: add codable-decoding knowledge contract"
```

---

## Task 5: Knowledge Contract — `http-error-handling`

**Files:**
- Create: `knowledge/networking/http-error-handling.md`

- [ ] **Step 1: Create the file**

```markdown
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
related: []
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/http-error-handling.md --type knowledge`
Expected: `PASS: knowledge/networking/http-error-handling.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/http-error-handling.md
git commit -m "feat: add http-error-handling knowledge contract"
```

---

## Task 6: Knowledge Contract — `task-cancellation`

**Files:**
- Create: `knowledge/networking/task-cancellation.md`

- [ ] **Step 1: Create the file**

```markdown
# Task Cancellation

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.task-cancellation
type: knowledge
title: Task Cancellation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how network calls made inside a Swift Task respond to cancellation, when to check cancellation explicitly, and why CancellationError must not be treated as a generic failure.
domain: Networking
tags:
  - networking
  - task
  - cancellation
references:
  - https://developer.apple.com/documentation/swift/task
  - https://developer.apple.com/documentation/swift/task/checkcancellation()
depends_on:
  - knowledge.networking.async-data-fetching
related: []
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent handles cancellation of an
in-flight network call made from a `Task`, so a superseded or
no-longer-needed request stops cleanly instead of wasting work or
surfacing a spurious error to the user.

## Scope

### Included

-   Cancellation propagation through `await` inside a `Task`
-   `Task.checkCancellation()` for explicit cancellation checks
-   Explicitly cancelling a stored `Task` reference
-   Distinguishing `CancellationError`/`URLError(.cancelled)` from a real failure

### Excluded

-   The network call itself — see `async-data-fetching`
-   `URLSessionTask`-level cancellation via `URLSessionDelegate` — out of v1 scope

## Rules

### Rule 1

Agents MUST rely on implicit cancellation propagation for a simple
request/response chain — awaiting `URLSession.data(for:)` inside a
cancelled `Task` throws automatically (as `URLError(.cancelled)` or
`CancellationError`); no manual polling is needed for a single `await`
call.

### Rule 2

Agents SHOULD call `Task.checkCancellation()` before starting expensive
follow-up work after an `await` point in a longer chain (e.g. decode,
then a second dependent network call) — otherwise a cancelled task can
keep doing work the caller no longer needs after the network call itself
already returned.

### Rule 3

Agents MUST explicitly call `.cancel()` on a stored `Task` when its
initiating object is deallocated or the request is superseded (e.g. a
new search query supersedes the in-flight one) in code that isn't using
SwiftUI's `.task(id:)` modifier — `.task(id:)` cancels and restarts
automatically when its `id` changes, but a manually created `Task` has
no such automatic behavior.

### Rule 4

Agents MUST NOT catch `CancellationError` (or `URLError(.cancelled)`)
and surface it as a generic network-failure message to the user —
cancellation is a deliberate, expected outcome (the caller no longer
wants the result), not a failure condition to report.

## Compliant Example

```swift
final class SearchController {
    private var searchTask: Task<Void, Never>?

    func search(_ query: String) {
        searchTask?.cancel()
        searchTask = Task {
            do {
                let results = try await fetchResults(for: query)
                await MainActor.run { self.display(results) }
            } catch is CancellationError {
                // Expected: a newer search superseded this one.
            } catch {
                await MainActor.run { self.showError(error) }
            }
        }
    }
}
```
The previous task is explicitly cancelled before starting a new one, and `CancellationError` is caught separately and silently ignored rather than shown as a failure. (Rules 3, 4)

## Non-Compliant Example

```swift
func search(_ query: String) {
    Task {
        do {
            let results = try await fetchResults(for: query)
            display(results)
        } catch {
            showError(error)
        }
    }
}
```
No previous task is tracked or cancelled when a new search starts, and every caught error — including a deliberate cancellation from an app-wide task-cancellation policy — is shown to the user as a generic failure. (Rules 3, 4)

## Dependencies

- `knowledge.networking.async-data-fetching` — cancellation applies to an in-flight fetch.

## References

-   [Apple Developer — Task](https://developer.apple.com/documentation/swift/task)
-   [Apple Developer — Task.checkCancellation()](https://developer.apple.com/documentation/swift/task/checkcancellation())
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/task-cancellation.md --type knowledge`
Expected: `PASS: knowledge/networking/task-cancellation.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/task-cancellation.md
git commit -m "feat: add task-cancellation knowledge contract"
```

---

## Task 7: Knowledge Contract — `url-session-configuration`

**Files:**
- Create: `knowledge/networking/url-session-configuration.md`

- [ ] **Step 1: Create the file**

```markdown
# URL Session Configuration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.url-session-configuration
type: knowledge
title: URL Session Configuration
version: 0.1.0
status: Draft
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
updated: 2026-08-01
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
    delegate-based background transfers — out of v1 scope
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/url-session-configuration.md --type knowledge`
Expected: `PASS: knowledge/networking/url-session-configuration.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/url-session-configuration.md
git commit -m "feat: add url-session-configuration knowledge contract"
```

---

## Task 8: Knowledge Contract — `app-transport-security`

**Files:**
- Create: `knowledge/networking/app-transport-security.md`

- [ ] **Step 1: Create the file**

```markdown
# App Transport Security

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.app-transport-security
type: knowledge
title: App Transport Security
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines App Transport Security's HTTPS/TLS requirements and how to declare a narrowly-scoped Info.plist exception when genuinely required, rather than a blanket allow-arbitrary-loads exception.
domain: Networking
tags:
  - networking
  - ats
  - security
references:
  - https://developer.apple.com/documentation/security/preventing-insecure-network-connections
depends_on: []
related: []
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent handles App Transport
Security (ATS) requirements — HTTPS with TLS 1.2 or later by default —
and how to declare a narrowly-scoped exception in `Info.plist` only when
a specific domain genuinely cannot meet that requirement, rather than
disabling ATS protection app-wide.

## Scope

### Included

-   ATS's default HTTPS/TLS 1.2+ requirement
-   `NSAppTransportSecurity`/`NSExceptionDomains` scoped Info.plist exceptions
-   Why `NSAllowsArbitraryLoads` is a last resort, not a default fix

### Excluded

-   `URLSessionDelegate` certificate/challenge handling implementation — out of v1 scope
-   App Store Review's evaluation of ATS exceptions — that's a submission-review concern, not an implementation one

## Rules

### Rule 1

Agents MUST NOT set `NSAllowsArbitraryLoads` to `true` in `Info.plist`
to work around an ATS connection failure — this disables ATS protection
for every network connection the app makes, not just the one that
failed, and is treated by App Review as requiring strong justification.

### Rule 2

Agents MUST scope any necessary ATS exception to the specific domain
via `NSExceptionDomains`, setting only the specific keys that domain
actually needs (e.g. `NSExceptionAllowsInsecureHTTPLoads` or
`NSExceptionMinimumTLSVersion`) rather than a blanket app-wide
exception — the narrowest exception that solves the actual problem.

### Rule 3

Agents SHOULD treat an ATS connection failure as a signal to fix the
server's TLS configuration (upgrade to TLS 1.2+, obtain a valid
certificate) before reaching for an `Info.plist` exception — an
exception is a documented last resort, not the default response to an
ATS failure.

### Rule 4

Agents MUST NOT implement a `URLSessionDelegate` certificate-validation
callback that unconditionally trusts any certificate as a way to bypass
an ATS or TLS failure — doing so removes protection against a
man-in-the-middle attack for that connection entirely, regardless of
whether an ATS exception is also present.

## Compliant Example

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>legacy-internal.example.com</key>
        <dict>
            <key>NSExceptionMinimumTLSVersion</key>
            <string>TLSv1.1</string>
            <key>NSIncludesSubdomains</key>
            <true/>
        </dict>
    </dict>
</dict>
```
Exception scoped to one specific legacy internal domain with only the minimum-TLS-version key needed, rather than a blanket app-wide allowance. (Rules 1, 2)

## Non-Compliant Example

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```
A blanket exception disabling ATS for every connection the app makes, applied to work around one endpoint's TLS issue. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Preventing Insecure Network Connections](https://developer.apple.com/documentation/security/preventing-insecure-network-connections)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/app-transport-security.md --type knowledge`
Expected: `PASS: knowledge/networking/app-transport-security.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/app-transport-security.md
git commit -m "feat: add app-transport-security knowledge contract"
```

---

## Task 9: Knowledge Contract — `authenticated-requests`

**Files:**
- Create: `knowledge/networking/authenticated-requests.md`

- [ ] **Step 1: Create the file**

```markdown
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/networking/authenticated-requests.md --type knowledge`
Expected: `PASS: knowledge/networking/authenticated-requests.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/networking/authenticated-requests.md
git commit -m "feat: add authenticated-requests knowledge contract"
```

---

## Task 10: Native Skill — `skills/networking/SKILL.md`

**Files:**
- Create: `skills/networking/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: networking
description: Route URLSession async/await networking implementation tasks to the correct Knowledge Contracts — request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, and authenticated requests. Use when writing or reviewing code that makes an HTTP request, decodes a JSON response, or handles a network error in Swift. v1 is async/await URLSession only — no completion-handler dataTask, no Combine dataTaskPublisher, no URLSessionDelegate-based background transfer/progress/custom TLS handling. Sign-in UX/terminology is out of scope here — see the authentication skill. Triggers on URLSession, URLRequest, URLComponents, async await network call, data(for:), JSONDecoder, Codable decoding, DecodingError, HTTPURLResponse, URLError, Task cancellation, URLSessionConfiguration, App Transport Security, ATS, NSAppTransportSecurity, Authorization header, Bearer token, 401 refresh.
id: skill.networking.foundations
title: Networking — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Networking
routes: [knowledge.networking.url-request-construction, knowledge.networking.async-data-fetching, knowledge.networking.codable-decoding, knowledge.networking.http-error-handling, knowledge.networking.task-cancellation, knowledge.networking.url-session-configuration, knowledge.networking.app-transport-security, knowledge.networking.authenticated-requests]
related:
  - skill.authentication.login
last_updated: 2026-08-01
---

# Networking — Foundations Skill

## Purpose

Route URLSession async/await networking implementation tasks to the
minimum required Networking Knowledge Contracts. v1 scope is
async/await `URLSession` data-task APIs only — no completion-handler
APIs, no Combine, no `URLSessionDelegate`-based background/progress/TLS
handling.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/networking/.

-   Requests -> url-request-construction.md, async-data-fetching.md, url-session-configuration.md
-   Data handling -> codable-decoding.md, http-error-handling.md
-   Lifecycle -> task-cancellation.md
-   Security & auth -> app-transport-security.md, authenticated-requests.md

Never load more than the contracts relevant to the specific question.
For sign-in UX, terminology, or authentication entry points, route to
`skill.authentication.login` instead — this Skill covers only the
networking mechanics of attaching credentials to a request.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/networking/ — do not guess or fall back to
general knowledge. Completion-handler `URLSession` APIs, Combine's
`dataTaskPublisher`, and `URLSessionDelegate`-based background transfer,
progress tracking, and custom TLS/challenge handling are deferred to
future scope, not yet built — report that explicitly rather than
answering from general knowledge (see docs/architecture/domain-map.md).
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/networking/SKILL.md --type skill`
Expected: `PASS: skills/networking/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/networking/SKILL.md
git commit -m "feat: add networking native skill"
```

---

## Task 11: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`sf-symbols` row (the row containing `skills/sf-symbols/SKILL.md`):

```markdown
| URLSession, URLRequest, URLComponents, async await network call, data(for:), JSONDecoder, Codable decoding, DecodingError, HTTPURLResponse, URLError, Task cancellation, URLSessionConfiguration, App Transport Security, ATS, NSAppTransportSecurity, Authorization header, Bearer token, 401 refresh | skills/networking/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `9` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui, accessibility, uikit, sf-symbols, networking)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add networking to skills index"
```

---

## Task 12: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `networking` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| Networking | networking | URLSession, ATS | URLSession usage and App Transport Security conventions |
```

Replace with:

```markdown
| Networking | networking | Async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests. No completion-handler APIs, no Combine, no URLSessionDelegate-based background/progress/TLS handling. Sign-in UX owned by `authentication` — see Cross-Domain Notes. | URLSession async/await implementation conventions (requests, decoding, error handling, cancellation, session configuration, ATS, authenticated requests) |
```

- [ ] **Step 2: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt).
```

- [ ] **Step 3: Add a new Cross-Domain Notes entry**

Find this exact line (the last bullet in `## Cross-Domain Notes`):

```markdown
- `uikit` and `human-interface-guidelines` overlap: HIG owns design guidance (when to use a tab bar vs. navigation stack, list vs. grid layout choice, modal vs. push presentation), `uikit` owns API implementation (the *how*). Same angle-split pattern as `accessibility` vs. `human-interface-guidelines`.
```

Replace with (adds one new bullet after it):

```markdown
- `uikit` and `human-interface-guidelines` overlap: HIG owns design guidance (when to use a tab bar vs. navigation stack, list vs. grid layout choice, modal vs. push presentation), `uikit` owns API implementation (the *how*). Same angle-split pattern as `accessibility` vs. `human-interface-guidelines`.
- `networking` and `authentication` do not overlap — this is a clean handoff, not an angle-split. `authentication`'s own Knowledge Contract (`knowledge.authentication.authentication`) explicitly excludes "Authentication networking" and "Backend architecture" from its scope; `networking`'s `authenticated-requests` topic fills exactly that gap (attaching credentials to a request, 401 refresh-and-retry), while `authentication` continues to own sign-in UX, terminology, and entry points. No content is duplicated between the two domains.
```

- [ ] **Step 4: Validate manually**

Run: `grep -c "networking" docs/architecture/domain-map.md`
Expected: a number greater than 4 (the file already mentions "networking"
at least a few times before this task — the Tier 1 row and the
artifact-layout example — the updated row, Completed line, and new
Cross-Domain Notes entry push the count well above that baseline)

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope networking v1, add networking cross-domain note"
```

---

## Task 13: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `sf-symbols` bullet,
immediately before the `Full routing tables:` line):

```markdown
- **`sf-symbols`** — Routes SF Symbols API implementation tasks (rendering modes, symbol variants, variable value, weight/scale, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration) to SF Symbols Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this status icon should use two colors, one per layer"` → `rendering-modes.md`
  Example: `"how do I show wifi signal strength as a symbol"` → `variable-value-symbols.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`sf-symbols`** — Routes SF Symbols API implementation tasks (rendering modes, symbol variants, variable value, weight/scale, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration) to SF Symbols Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this status icon should use two colors, one per layer"` → `rendering-modes.md`
  Example: `"how do I show wifi signal strength as a symbol"` → `variable-value-symbols.md`

- **`networking`** — Routes URLSession async/await networking implementation tasks (request construction, data fetching, Codable decoding, error handling, task cancellation, session configuration, App Transport Security, authenticated requests) to Networking Knowledge Contracts.
  Example: `"my JSON response isn't decoding, dates are failing"` → `codable-decoding.md`
  Example: `"how do I retry a request after a 401 without an infinite loop"` → `authenticated-requests.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a new What's New line**

Find this exact line (the first/topmost line in `## What's New`):

```markdown
- 2026-08-01 — Added `sf-symbols` Skill (symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contracts. Resolves the human-interface-guidelines sf-symbols forward-reference and replaces the prior placeholder scope in domain-map.md.
```

Replace with (adds a new topmost line before it):

```markdown
- 2026-08-01 — Added `networking` Skill (URL request construction, async data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; async/await URLSession v1) — 8 Knowledge Contracts. Fills the "Authentication networking" gap authentication.md explicitly excludes, and replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `sf-symbols` Skill (symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contracts. Resolves the human-interface-guidelines sf-symbols forward-reference and replaces the prior placeholder scope in domain-map.md.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "networking" README.md`
Expected: a number greater than 0 (the new `networking` Skills bullet
and What's New line are the first mentions of "networking" in this
file)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add networking to README Skills + What's New"
```

---

## Task 14: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/networking.md --type reference
python3 scripts/validate_artifact.py skills/networking/SKILL.md --type skill
for f in knowledge/networking/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
```
Expected: `PASS` for all 10 files.

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 4: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 13 prior tasks committed).

- [ ] **Step 5: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire `networking` domain (all
10 new files plus the 3 modified docs) to check cross-file consistency:
every `related:`/`depends_on:` KC id resolves to a real file (including
the cross-domain `knowledge.authentication.authentication` reference in
`authenticated-requests.md`), the Skill's `routes:` list matches exactly
the 8 KC ids, the Reference's "Used By" list matches exactly the 8 KC
files, layer order (References → Knowledge → Skills) is respected, the
new Cross-Domain Notes entry reads correctly. The review must
specifically check for v1-scope violations that a per-task review could
miss (this class of bug slipped through per-task review in both the
`uikit` and `sf-symbols` domain builds and was only caught by the final
holistic pass):

-   No content anywhere describing completion-handler `dataTask` APIs
    or Combine's `dataTaskPublisher`
-   No content anywhere implementing (not just prohibiting)
    `URLSessionDelegate` conformance, background transfer, or progress
    tracking
-   No KC restates `authentication`'s sign-in UX/terminology/flow
    content — `authenticated-requests.md` should cross-reference it via
    `related:` instead
-   Live-verify (`curl`/JSON endpoint, not WebFetch's summarized output)
    every Apple Developer URL cited across all 10 files actually
    resolves — this is standard practice for every task in this domain,
    not just the final one, per the broken-URL findings in the prior
    `uikit` and `sf-symbols` domain builds

If the reviewer finds issues, fix them, re-validate the affected
file(s), commit the fix, and re-run Steps 1–4 to confirm no
regressions.

- [ ] **Step 6: Report final status**

Report the total commit count for this domain, confirm all validations
pass, and hand off to `superpowers:finishing-a-development-branch` for
shipping (branch + PR, per this session's established pattern).
