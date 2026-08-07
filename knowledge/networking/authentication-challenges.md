# Authentication Challenges

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.networking.authentication-challenges
artifact_type: knowledge
title: Authentication Challenges
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how a URLSession delegate answers a server authentication challenge -- choosing the session-wide URLSessionDelegate method or the task-specific URLSessionTaskDelegate one, dispatching on protectionSpace.authenticationMethod and falling through to performDefaultHandling, the requirement that the completion handler be called exactly once on every path including cancellation, and using previousFailureCount and proposedCredential to stop a rejected credential from looping.
domain: Networking
tags:
  - networking
  - urlsession
  - authentication
  - delegate
references:
  - https://developer.apple.com/documentation/foundation/handling-an-authentication-challenge
  - https://developer.apple.com/documentation/foundation/urlauthenticationchallenge
  - https://developer.apple.com/documentation/foundation/urlsession/authchallengedisposition
  - https://developer.apple.com/documentation/foundation/urlsessiondelegate
depends_on:
  - knowledge.networking.url-session-delegate
related:
  - knowledge.networking.authenticated-requests
  - knowledge.networking.server-trust-evaluation
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent implements the `URLSession`
delegate methods that answer a server's demand for credentials. Its central
claim is that the completion handler is an obligation, not an option: a
delegate that returns without calling it leaves the task suspended
indefinitely, with no error and no way to distinguish it from a slow server.

## Scope

### Included

-   Choosing the session-wide or task-specific challenge method
-   Dispatching on `authenticationMethod` and building a `URLCredential`
-   Calling the completion handler on every path, and stopping retry loops

### Excluded

-   Server trust and certificate pinning — see `server-trust-evaluation`;
    delegate ownership and invalidation — see `url-session-delegate`
-   Attaching a token the app already holds — see `authenticated-requests`
-   The sign-in mechanism and its UX — owned by `authenticationservices`

## Rules

### Rule 1

Agents MUST choose the delegate method by the challenge's scope. Per
Apple's documentation, `urlSession(_:didReceive:completionHandler:)` on
`URLSessionDelegate` handles "session-wide challenges… like Transport Layer
Security (TLS) validation", where "your action remains in effect for all
tasks created from that `URLSession`";
`urlSession(_:task:didReceive:completionHandler:)` on
`URLSessionTaskDelegate` handles "task-specific challenges… like demands
for username/password authentication."

### Rule 2

Agents MUST verify `challenge.protectionSpace.authenticationMethod` before
answering and MUST fall through to `.performDefaultHandling` for anything
else. Per Apple's documentation, default handling "may satisfy the
challenge; otherwise, the task will move on to the next challenge in the
response and call this delegate again." A delegate that answers every
challenge as though it were the expected one breaks the challenges it was
not written for.

### Rule 3

Agents MUST call the completion handler exactly once on every path,
including failure and user cancellation. Per Apple's documentation: "you
must call the completion handler to complete the challenge and allow the
task to proceed, even if you're choosing to cancel." Use
`.cancelAuthenticationChallenge` when no credential can be produced and
`.useCredential` when one can. An early `return` that skips the handler
hangs the task silently — the compiler does not require the call.

### Rule 4

Agents MUST use `previousFailureCount` to bound retries rather than
resupplying a rejected credential. Per Apple's documentation, when a
credential is refused "the system calls your delegate method again", with
the rejected credential exposed as `proposedCredential` and the count of
rejections as `previousFailureCount`. Returning the same stored credential
unconditionally produces an unbounded loop against the server.

### Rule 5

Agents MUST choose `URLCredential` persistence deliberately. A credential
created with `.forSession` is, per Apple, "only stored by the `URLSession`
instance that created the task" — new sessions and later app runs must supply
it again. `.permanent` writes to the keychain: a storage decision, not a
networking one.

## Compliant Example

```swift
func urlSession(_ s: URLSession, task: URLSessionTask,
                didReceive challenge: URLAuthenticationChallenge,
                completionHandler done: @escaping (URLSession.AuthChallengeDisposition,
                                                   URLCredential?) -> Void) {
    guard challenge.protectionSpace.authenticationMethod
            == NSURLAuthenticationMethodHTTPBasic else {
        return done(.performDefaultHandling, nil)                    // Rule 2
    }
    guard challenge.previousFailureCount == 0,                       // Rule 4
          let credential = storedCredential else {
        return done(.cancelAuthenticationChallenge, nil)             // Rule 3
    }
    done(.useCredential, credential)
}
```

## Non-Compliant Example

```swift
func urlSession(_ s: URLSession, task: URLSessionTask,
                didReceive challenge: URLAuthenticationChallenge,
                completionHandler done: @escaping (URLSession.AuthChallengeDisposition,
                                                   URLCredential?) -> Void) {
    if let credential = storedCredential { done(.useCredential, credential) }
}
```
When no credential is stored, `done` is never called and the task hangs
forever with no error (Rule 3). When one is stored, it is resupplied after
every rejection (Rule 4) and offered to challenges of any type (Rule 2).

## Dependencies

- `url-session-delegate` -- answering a challenge requires a delegate session,
  so its retention, invalidation, and queue rules apply.

## References

- [Apple Developer — Handling an authentication challenge](https://developer.apple.com/documentation/foundation/handling-an-authentication-challenge)
- [Apple Developer — URLAuthenticationChallenge](https://developer.apple.com/documentation/foundation/urlauthenticationchallenge)
- [Apple Developer — URLSession.AuthChallengeDisposition](https://developer.apple.com/documentation/foundation/urlsession/authchallengedisposition)
- [Apple Developer — URLSessionDelegate](https://developer.apple.com/documentation/foundation/urlsessiondelegate)
