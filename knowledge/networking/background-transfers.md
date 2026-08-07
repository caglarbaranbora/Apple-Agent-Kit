# Background Transfers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.background-transfers
artifact_type: knowledge
title: Background Transfers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how a URLSession background configuration is built and driven -- the fixed session identifier, the upload/download-only restriction that follows from transfers running in a separate process, sessionSendsLaunchEvents and isDiscretionary, the app-relaunch handshake through handleEventsForBackgroundURLSession and urlSessionDidFinishEvents, recreating the session with the same identifier at launch, the file that is deleted when didFinishDownloadingTo returns, and the force-quit case the system does not resume.
domain: Networking
tags:
  - networking
  - urlsession
  - background
  - delegate
references:
  - https://developer.apple.com/documentation/foundation/downloading-files-in-the-background
  - https://developer.apple.com/documentation/foundation/urlsessionconfiguration/background(withidentifier:)
  - https://developer.apple.com/documentation/foundation/urlsessiondownloaddelegate
  - https://developer.apple.com/documentation/foundation/urlsessiondelegate
depends_on:
  - knowledge.networking.url-session-delegate
related:
  - knowledge.networking.url-session-configuration
  - knowledge.networking.transfer-progress-tracking
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent implements a transfer that
outlives the app's foreground lifetime. Its central claim is that a
background session is not a configuration change to an ordinary one: the
transfer runs in a different process, and its callback can arrive into a
freshly relaunched app rather than the one that started the download.

## Scope

### Included

-   Building the background configuration and its scheduling properties
-   The relaunch handshake, recreating the session at launch, the delivered
    file's lifetime, the force-quit case

### Excluded

-   Delegate retention and invalidation — see `url-session-delegate`;
    non-background configurations — see `url-session-configuration`; progress
    reporting — see `transfer-progress-tracking`
-   `BGTaskScheduler` background *work* (as opposed to transfers) — owned by
    `knowledge.backgroundtasks.background-task-registration-and-scheduling`

## Rules

### Rule 1

Agents MUST create the configuration with
`URLSessionConfiguration.background(withIdentifier:)` using a fixed string,
and MUST NOT generate the identifier at runtime. Per Apple's documentation:
"you can use a fixed string for the identifier, rather than a dynamically
generated identifier." A generated one cannot be matched at relaunch (Rule 4).

### Rule 2

Agents MUST use download or upload tasks in a background session and MUST
NOT use data tasks. Per Apple's documentation, `background(withIdentifier:)`
returns "a configuration object that causes the system to perform upload and
download tasks in a separate process" — an in-memory `Data` result has no
process to be delivered into. Leave `sessionSendsLaunchEvents` `true` (the
default) so the system wakes the app, and set `isDiscretionary` only for
time-insensitive work, where per Apple it "can wait for optimal conditions."

### Rule 3

Agents MUST implement the two-part relaunch handshake, not just the download
delegate. Per Apple's documentation the system "calls the
`UIApplicationDelegate` method
`application(_:handleEventsForBackgroundURLSession:completionHandler:)`";
store that handler, then invoke it from
`urlSessionDidFinishEvents(forBackgroundURLSession:)`, which per Apple "may
be called on a secondary queue" and so must dispatch to the main one.

### Rule 4

Agents MUST recreate the background session during launch setup with the
same identifier, before any event can be delivered. Per Apple's
documentation: "recreate the background session… using the same session
identifier as before, to allow the system to reassociate the background
download task with your session." Creating it lazily when a screen appears
is too late — the app may have been relaunched headless. Agents MUST also not
promise this always happens: per Apple, relaunch "applies only for normal
termination of the app by the system. If the user terminates the app from the
multitasking screen, the system cancels all of the session's background
transfers."

### Rule 5

Agents MUST move or read the downloaded file synchronously inside
`urlSession(_:downloadTask:didFinishDownloadingTo:)`. Per Apple's
documentation, "the file is fully downloaded, and will be available until
your delegate method returns." An asynchronous move races the system's
deletion, failing intermittently and only for large files.

## Compliant Example

```swift
final class Transfers: NSObject, URLSessionDownloadDelegate {
    static let shared = Transfers()          // created at launch — Rule 4
    private lazy var session = URLSession(
        configuration: .background(withIdentifier: "com.example.transfers"),  // Rule 1
        delegate: self, delegateQueue: nil)
    var backgroundCompletionHandler: (() -> Void)?
    func start(_ url: URL) { session.downloadTask(with: url).resume() }       // Rule 2
    func urlSession(_ s: URLSession, downloadTask: URLSessionDownloadTask,
                    didFinishDownloadingTo location: URL) {
        try? FileManager.default.moveItem(at: location, to: destination) }    // Rule 5
    func urlSessionDidFinishEvents(forBackgroundURLSession s: URLSession) {
        DispatchQueue.main.async { self.backgroundCompletionHandler?() } }    // Rule 3
}
```

## Non-Compliant Example

```swift
func urlSession(_ s: URLSession, downloadTask: URLSessionDownloadTask,
                didFinishDownloadingTo location: URL) {
    DispatchQueue.global().async {
        try? FileManager.default.moveItem(at: location, to: self.destination) }
}
```
The delegate method returns before the move runs, so the system deletes the
file first (Rule 5). Small files often win the race, so this passes in
testing and fails on slow devices and large downloads.

## Dependencies

- `url-session-delegate` -- a background session is delegate-only, so its
  retention and invalidation rules apply here in full.

## References

- [Apple Developer — Downloading files in the background](https://developer.apple.com/documentation/foundation/downloading-files-in-the-background)
- [Apple Developer — background(withIdentifier:)](https://developer.apple.com/documentation/foundation/urlsessionconfiguration/background(withidentifier:))
- [Apple Developer — URLSessionDownloadDelegate](https://developer.apple.com/documentation/foundation/urlsessiondownloaddelegate)
- [Apple Developer — URLSessionDelegate](https://developer.apple.com/documentation/foundation/urlsessiondelegate)
