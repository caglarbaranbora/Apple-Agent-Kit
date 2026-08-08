# Data Task Publisher

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.data-task-publisher
artifact_type: knowledge
title: Data Task Publisher
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when URLSession.dataTaskPublisher is the right choice over async/await, the (data, response) Output and URLError Failure that mean an HTTP error status is delivered as success rather than a failure, the tryMap that must therefore check the status code, delivering on the main queue before a UI sink, and the AnyCancellable whose release cancels the in-flight request with no error.
domain: Networking
tags:
  - networking
  - urlsession
  - combine
  - publisher
references:
  - https://developer.apple.com/documentation/foundation/urlsession/datataskpublisher
  - https://developer.apple.com/documentation/foundation/urlsession
  - https://developer.apple.com/documentation/foundation/httpurlresponse
  - https://developer.apple.com/documentation/foundation/urlerror
depends_on:
  - knowledge.networking.http-error-handling
related:
  - knowledge.networking.async-data-fetching
  - knowledge.networking.codable-decoding
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent uses Combine's
`URLSession.DataTaskPublisher`. Its central claim is that the publisher's
declared `Failure` type settles a question agents routinely get wrong:
`Failure` is `URLError`, so an HTTP 500 is not a failure of this publisher.
It arrives on the value path, and a chain that omits the status check
decodes an error page as though it were a payload.

## Scope

### Included

-   Choosing `dataTaskPublisher` over the async/await APIs
-   The `Output` and `Failure` types, and the status check they force
-   Scheduling for UI, and the cancellable's lifetime

### Excluded

-   The async/await APIs — see `async-data-fetching`; the completion-handler
    ones — see `completion-handler-apis`
-   `JSONDecoder` configuration and `DecodingError` — see `codable-decoding`
-   Combine's own publisher/operator semantics — owned by the `combine` domain

## Rules

### Rule 1

Agents MUST default to the async/await APIs and MUST use `dataTaskPublisher`
only to feed an existing Combine chain — a pipeline that already combines,
debounces, or merges this request with other publishers. A single request
awaited once is not such a case, and wrapping it in a publisher to `sink`
immediately adds a subscription lifetime for no benefit.

### Rule 2

Agents MUST check the HTTP status code inside the chain and MUST NOT treat
a delivered value as success. The publisher declares
`Output = (data: Data, response: URLResponse)` and `Failure = URLError`, so
only transport errors terminate it; a 404 or 500 is delivered as a normal
value carrying the error body. This is the same distinction
`http-error-handling` draws for `data(for:)`, and it must be enforced with
`tryMap` before any decoding operator.

### Rule 3

Agents MUST cast `response` to `HTTPURLResponse` inside that `tryMap` rather
than force-unwrapping it. `Output`'s response is typed as `URLResponse`; the
cast fails for non-HTTP schemes, and a `guard`/`throw` converts that into an
error the chain's completion handler can report.

### Rule 4

Agents MUST insert `.receive(on: DispatchQueue.main)` before any sink that
touches UI. The publisher emits on a URL-loading queue, not the main one, so
without it the `sink` closure writes UI state off the main thread.

### Rule 5

Agents MUST store the returned `AnyCancellable` for as long as the request
should live. Releasing it cancels the in-flight request, and the sink's
completion closure is not called — the request simply stops, which reads as
a hung server rather than a cancelled subscription. Assigning `sink(...)` to
`_` is the usual form of this defect.

## Compliant Example

```swift
URLSession.shared.dataTaskPublisher(for: request)
    .tryMap { data, response -> Data in                      // Rules 2, 3
        guard let http = response as? HTTPURLResponse else { throw URLError(.badServerResponse) }
        guard (200..<300).contains(http.statusCode) else { throw HTTPError(status: http.statusCode) }
        return data
    }
    .decode(type: Article.self, decoder: JSONDecoder())
    .receive(on: DispatchQueue.main)                         // Rule 4
    .sink(receiveCompletion: { [weak self] in self?.handle($0) },
          receiveValue: { [weak self] in self?.article = $0 })
    .store(in: &cancellables)                                // Rule 5
```

## Non-Compliant Example

```swift
_ = URLSession.shared.dataTaskPublisher(for: request)
    .map(\.data)
    .decode(type: Article.self, decoder: JSONDecoder())
    .sink(receiveCompletion: { _ in }, receiveValue: { self.article = $0 })
```
The cancellable is discarded, so the request is cancelled before it can
complete and nothing reports it (Rule 5). Had it survived, `map(\.data)`
discards the response without checking the status, so a 500's error body
would reach `decode` (Rules 2, 3), and the assignment happens off the main
queue (Rule 4).

## Dependencies

- `http-error-handling` -- it owns what a status code means and how to act on
  it; this contract owns only where that check goes in a Combine chain.

## References

- [Apple Developer — URLSession.DataTaskPublisher](https://developer.apple.com/documentation/foundation/urlsession/datataskpublisher)
- [Apple Developer — URLSession](https://developer.apple.com/documentation/foundation/urlsession)
- [Apple Developer — HTTPURLResponse](https://developer.apple.com/documentation/foundation/httpurlresponse)
- [Apple Developer — URLError](https://developer.apple.com/documentation/foundation/urlerror)
