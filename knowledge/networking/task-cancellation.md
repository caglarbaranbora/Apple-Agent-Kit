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
            } catch let urlError as URLError where urlError.code == .cancelled {
                // URLSession.data(for:) throws URLError(.cancelled), not
                // CancellationError, when its containing Task is cancelled.
            } catch {
                await MainActor.run { self.showError(error) }
            }
        }
    }
}
```
The previous task is explicitly cancelled before starting a new one, and both forms cancellation can actually take — `CancellationError` and `URLError(.cancelled)` (the one `URLSession.data(for:)` actually throws) — are caught separately and silently ignored rather than shown as a failure. (Rules 3, 4)

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
