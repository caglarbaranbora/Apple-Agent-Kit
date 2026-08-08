# URL Session Delegate

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.url-session-delegate
artifact_type: knowledge
title: URL Session Delegate
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when a URLSession needs a delegate at all, which protocol in the URLSessionDelegate/URLSessionTaskDelegate/URLSessionDataDelegate/URLSessionDownloadDelegate hierarchy to implement, the fact that a delegate session is strongly retained and leaks until it is invalidated, the difference between finishTasksAndInvalidate() and invalidateAndCancel(), why URLSession.shared can never carry a delegate, and the delegate queue that callbacks arrive on.
domain: Networking
tags:
  - networking
  - urlsession
  - delegate
  - memory-management
references:
  - https://developer.apple.com/documentation/foundation/urlsession
  - https://developer.apple.com/documentation/foundation/urlsessiondelegate
  - https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate
  - https://developer.apple.com/documentation/foundation/urlsession/finishtasksandinvalidate()
  - https://developer.apple.com/documentation/foundation/urlsession/invalidateandcancel()
depends_on:
  - knowledge.networking.url-session-configuration
related:
  - knowledge.networking.async-data-fetching
last_updated: 2026-08-08
```

## Intent

This contract defines when an AI coding agent should introduce a
`URLSession` delegate, and the ownership obligations that come with one. Its
central claim: a delegate session is not a drop-in replacement for
`URLSession.shared` — assigning a delegate creates a strong reference cycle
Apple documents as an outright leak, and nothing reports it.

## Scope

### Included

-   Whether a delegate is needed at all, and which protocol a task type requires
-   Delegate retention, both invalidation methods, their effect on `shared`,
    and the queue callbacks are delivered on

### Excluded

-   What individual callbacks do: background transfers and the app-relaunch
    handshake (`background-transfers`), progress (`transfer-progress-tracking`),
    challenges (`authentication-challenges`, `server-trust-evaluation`)
-   Building the configuration itself — see `url-session-configuration`

## Rules

### Rule 1

Agents MUST NOT add a delegate to obtain a result an async/await or
completion-handler call already returns. Per Apple's documentation: "Your
`URLSession` object doesn't need to have a delegate. If no delegate is
assigned, a system-provided delegate is used." A delegate is justified only by
an event the return value cannot carry — incremental data, progress,
redirects, an authentication challenge, or a background transfer.

### Rule 2

Agents MUST invalidate any session they create with a delegate, and MUST
NOT rely on the session going out of scope. Per Apple's documentation:
"The session object keeps a strong reference to the delegate until your
app exits or explicitly invalidates the session. If you don't invalidate
the session, your app leaks memory until the app terminates." The delegate
is typically the object owning the session, so the retain is a cycle, and
nothing warns: it compiles, requests succeed, the leak shows only in
Instruments.

### Rule 3

Agents MUST choose the invalidation method by whether in-flight work
should complete, and MUST treat invalidation as terminal. Per Apple's
documentation, `finishTasksAndInvalidate()` "returns immediately without
waiting for tasks to finish… existing tasks continue until completion";
`invalidateAndCancel()` "cancels all outstanding tasks and then
invalidates the session." Both state: "After invalidation, session objects
cannot be reused" — one invalidated in `viewDidDisappear` cannot be reused
when the screen reappears. Neither works on `URLSession.shared`, where Apple
records that calling them "has no effect": `shared` takes no delegate, so
needing one means building a session and owning Rule 2 for it.

### Rule 4

Agents MUST implement the protocol matching the task type rather than
`URLSessionDelegate` alone. Per Apple's documentation: "most delegates
should also implement some or all of the methods in the
`URLSessionTaskDelegate`, `URLSessionDataDelegate`, and
`URLSessionDownloadDelegate` protocols to handle task-level events."
`URLSessionDelegate` carries session-level events only; a download's
completion callback lives on `URLSessionDownloadDelegate` and never arrives
if only the session protocol is adopted.

### Rule 5

Agents MUST NOT touch UI state directly inside a delegate callback.
Callbacks arrive on the queue passed as `delegateQueue`, and passing `nil`
— the form Apple's own examples use — creates a serial background queue
rather than defaulting to the main one. Hop to the main actor explicitly.

## Compliant Example

```swift
final class DownloadController: NSObject, URLSessionDownloadDelegate {   // Rule 4
    private lazy var session = URLSession(configuration: .default,
                                          delegate: self, delegateQueue: nil)
    func stop() { session.invalidateAndCancel() }                        // Rules 2, 3
    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask,
                    didFinishDownloadingTo location: URL) {
        let saved = persist(location)
        Task { @MainActor in self.status = .ready(saved) }               // Rule 5
    }
}
```

## Non-Compliant Example

```swift
final class Loader: NSObject, URLSessionDelegate {
    lazy var session = URLSession(configuration: .default,
                                  delegate: self, delegateQueue: nil)
    func load(_ r: URLRequest) async throws -> Data { try await session.data(for: r).0 }
}
```
The delegate buys nothing `data(for:)` already returns (Rule 1), and the
session is never invalidated, so `Loader` and its session retain each other
for the process lifetime (Rule 2). Every request still succeeds.

## Dependencies

- `url-session-configuration` -- it owns which configuration to build; this one
  owns what attaching a delegate to it commits the caller to.

## References

- [Apple Developer — URLSession](https://developer.apple.com/documentation/foundation/urlsession)
- [Apple Developer — URLSessionDelegate](https://developer.apple.com/documentation/foundation/urlsessiondelegate)
- [Apple Developer — URLSessionTaskDelegate](https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate)
- [Apple Developer — finishTasksAndInvalidate()](https://developer.apple.com/documentation/foundation/urlsession/finishtasksandinvalidate())
- [Apple Developer — invalidateAndCancel()](https://developer.apple.com/documentation/foundation/urlsession/invalidateandcancel())
