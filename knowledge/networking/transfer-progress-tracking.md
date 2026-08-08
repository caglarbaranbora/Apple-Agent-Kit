# Transfer Progress Tracking

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.transfer-progress-tracking
artifact_type: knowledge
title: Transfer Progress Tracking
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the three ways URLSession reports transfer progress -- the task's Progress object, the didWriteData/didSendBodyData delegate callbacks, and the bytes(for:) async sequence -- how to choose between them, and the NSURLSessionTransferSizeUnknown value a server that omits Content-Length produces, which turns a percentage calculation into a negative number rather than an error.
domain: Networking
tags:
  - networking
  - urlsession
  - progress
  - delegate
references:
  - https://developer.apple.com/documentation/foundation/urlsessiontask/progress
  - https://developer.apple.com/documentation/foundation/urlsessiondownloaddelegate
  - https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate
  - https://developer.apple.com/documentation/foundation/urlsession/bytes(for:delegate:)
depends_on:
  - knowledge.networking.url-session-delegate
related:
  - knowledge.networking.background-transfers
  - knowledge.networking.async-data-fetching
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent reports the progress of a
`URLSession` transfer. Its central claim is that the choice among the three
available mechanisms is forced by the transfer, not by preference — and
that whichever is chosen, an expected byte count is a value the server may
decline to supply, so it must be treated as optional rather than divided
by.

## Scope

### Included

-   Choosing between `URLSessionTask.progress`, the progress delegate
    callbacks, and `bytes(for:)`
-   Handling an unknown expected size, and the queue callbacks arrive on

### Excluded

-   Delegate ownership and invalidation — see `url-session-delegate`
-   Background transfer setup — see `background-transfers`
-   Rendering a progress control — owned by `human-interface-guidelines`

## Rules

### Rule 1

Agents MUST pick the mechanism the transfer supports rather than a
preferred one. `URLSessionTask.progress` — per Apple, "a representation of
the overall task progress" — needs no delegate and suits observation-based
UI. The `didWriteData`/`didSendBodyData` callbacks require a delegate and
are the only option for a background session. `bytes(for:)` returns "an
`AsyncBytes` sequence to iterate over, and a `URLResponse`", and is the
only option that also yields the data incrementally.

### Rule 2

Agents MUST NOT compute a fraction from the expected byte count without
checking it first. Per Apple's documentation, the expected length is "as
provided by the `Content-Length` header. If this header was not provided,
the value is `NSURLSessionTransferSizeUnknown`" — that is, `-1`. Dividing
by it yields a negative fraction, so the progress bar renders empty or
inverted; nothing throws, and it only reproduces against servers that
stream or chunk their response.

### Rule 3

When the expected size is unknown, agents MUST show indeterminate progress
rather than a fabricated percentage. Bytes received is still meaningful and
may be shown as a count; a percentage of an unknown total is not.

### Rule 4

Agents MUST NOT update UI directly from a progress callback. These arrive
on the session's `delegateQueue`, which is a background queue when `nil` is
passed. Progress callbacks fire far more often than completion ones, so an
unsynchronised UI write here is both more likely to be hit and more likely
to be dismissed as flakiness.

### Rule 5

Agents MUST NOT mix `bytes(for:)` with delegate progress callbacks for the
same transfer. The async sequence already delivers byte-level granularity;
adding a delegate to a call that has one duplicates the reporting and
re-introduces the retention obligation in `url-session-delegate` that the
async form avoids.

## Compliant Example

```swift
func urlSession(_ s: URLSession, downloadTask: URLSessionDownloadTask,
                didWriteData bytes: Int64, totalBytesWritten written: Int64,
                totalBytesExpectedToWrite expected: Int64) {
    let state: DownloadState = expected == NSURLSessionTransferSizeUnknown
        ? .indeterminate(bytesReceived: written)              // Rules 2, 3
        : .fraction(Double(written) / Double(expected))
    Task { @MainActor in self.state = state }                 // Rule 4
}
```

## Non-Compliant Example

```swift
func urlSession(_ s: URLSession, downloadTask: URLSessionDownloadTask,
                didWriteData bytes: Int64, totalBytesWritten written: Int64,
                totalBytesExpectedToWrite expected: Int64) {
    progressView.progress = Float(written) / Float(expected)
}
```
Against a server that sends `Content-Length` this looks correct. Against one
that omits it, `expected` is `-1`, so the fraction is negative and the bar
never moves (Rule 2) — with no error raised. The UIKit write is also off the
main queue (Rule 4).

## Dependencies

- `url-session-delegate` -- two of the three mechanisms in Rule 1 require a
  delegate, so its retention and queue rules govern them.

## References

- [Apple Developer — URLSessionTask.progress](https://developer.apple.com/documentation/foundation/urlsessiontask/progress)
- [Apple Developer — URLSessionDownloadDelegate](https://developer.apple.com/documentation/foundation/urlsessiondownloaddelegate)
- [Apple Developer — URLSessionTaskDelegate](https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate)
- [Apple Developer — bytes(for:delegate:)](https://developer.apple.com/documentation/foundation/urlsession/bytes(for:delegate:))
