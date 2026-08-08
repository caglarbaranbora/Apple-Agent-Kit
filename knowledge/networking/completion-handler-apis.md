# Completion Handler APIs

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.completion-handler-apis
artifact_type: knowledge
title: Completion Handler APIs
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when the completion-handler URLSession APIs are still the correct choice, the resume() call newly created tasks silently require, exhaustive handling of the (Data?, URLResponse?, Error?) triple, the delegate queue completion handlers run on, what passing a nil handler changes, and how to wrap a callback API in async/await with a continuation that must resume exactly once.
domain: Networking
tags:
  - networking
  - urlsession
  - completion-handler
  - async-await
  - migration
references:
  - https://developer.apple.com/documentation/foundation/urlsession
  - https://developer.apple.com/documentation/foundation/urlsessiondatatask
  - https://developer.apple.com/documentation/foundation/urlsessiontask/resume()
  - https://developer.apple.com/documentation/foundation/urlsession/data(for:delegate:)
depends_on:
  - knowledge.networking.async-data-fetching
related:
  - knowledge.networking.http-error-handling
  - knowledge.networking.url-session-delegate
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent works with `URLSession`'s
completion-handler APIs — when to reach for them at all, how to handle them
correctly, and how to wrap them in async/await. Its central claim is that
the most common defect here produces no error at all: a task created and
never resumed simply never runs, and the handler never fires.

## Scope

### Included

-   Choosing between the completion-handler and async/await API families
-   `resume()`, the `(Data?, URLResponse?, Error?)` triple, the queue the
    handler runs on, and the meaning of a `nil` handler
-   Bridging a callback API into async/await with a checked continuation

### Excluded

-   The async/await APIs themselves — see `async-data-fetching`; status-code
    checking — see `http-error-handling`
-   Combine's `dataTaskPublisher` — see `data-task-publisher`; delegate
    ownership and invalidation — see `url-session-delegate`

## Rules

### Rule 1

Agents MUST default to the async/await APIs and MUST use a completion
handler only when something forces it: a deployment target below iOS
15/macOS 12, an existing callback-shaped API being extended, or a framework
callback that cannot `await`. "The surrounding code uses callbacks" is a
reason to bridge (Rule 5), not to add another one.

### Rule 2

Agents MUST call `resume()` on every task they create. Per Apple's
documentation: "Newly-initialized tasks begin in a suspended state, so you
need to call this method to start the task." A task that is never resumed
produces no error, no warning, and no callback — the request never leaves.
The symptom is a spinner that never stops, which reads as a server problem
rather than a client one.

### Rule 3

Agents MUST handle all three completion-handler parameters as optional and
MUST NOT infer success from `error == nil`. The handler receives `Data?`,
`URLResponse?`, and `Error?`; a `nil` error means the transfer completed,
not that the server accepted the request. The response must still be cast
to `HTTPURLResponse` and its `statusCode` checked, exactly as
`http-error-handling` requires for the async APIs. Every path through the
handler must call back or update state; an unhandled combination leaves the
caller waiting forever.

### Rule 4

Agents MUST NOT update UI directly inside a completion handler. Per Apple's
documentation, the handler "is executed on the delegate queue" — for a
session built with `delegateQueue: nil`, a background queue. Passing `nil`
as the handler is also not a no-op: per Apple, "If you pass `nil`, only the
session delegate methods are called when the task completes."

### Rule 5

When bridging a callback API into async/await, agents MUST resume the
continuation exactly once on every path. `withCheckedThrowingContinuation`
traps on a double resume and leaks the awaiting task forever on a missing
one. The `guard`/`else` arms are where this is usually lost.

## Compliant Example

```swift
// Bridging a callback-only API into async/await (Rules 3, 5).
func fetch(_ request: URLRequest) async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error { return continuation.resume(throwing: error) }
            guard let http = response as? HTTPURLResponse, let data,
                  (200..<300).contains(http.statusCode) else {
                return continuation.resume(throwing: URLError(.badServerResponse))
            }
            continuation.resume(returning: data)
        }
        task.resume()                                              // Rule 2
    }
}
```

## Non-Compliant Example

```swift
func load(_ request: URLRequest, then handler: @escaping (Data) -> Void) {
    URLSession.shared.dataTask(with: request) { data, _, error in
        guard error == nil, let data else { return }
        self.label.text = "Loaded"
        handler(data)
    }
}
```
The task is never resumed, so none of this runs (Rule 2). Had it run, the
status code is never checked, so a 500 body arrives as success; the
`guard`'s `else` returns without informing the caller (Rule 3); and `label`
is touched off the main queue (Rule 4).

## Dependencies

- `async-data-fetching` -- it owns the API family Rule 1 routes callers toward;
  this contract owns the older family and the bridge between them.

## References

- [Apple Developer — URLSession](https://developer.apple.com/documentation/foundation/urlsession)
- [Apple Developer — URLSessionDataTask](https://developer.apple.com/documentation/foundation/urlsessiondatatask)
- [Apple Developer — resume()](https://developer.apple.com/documentation/foundation/urlsessiontask/resume())
- [Apple Developer — data(for:delegate:)](https://developer.apple.com/documentation/foundation/urlsession/data(for:delegate:))
