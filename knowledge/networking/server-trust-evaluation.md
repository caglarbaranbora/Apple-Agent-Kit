# Server Trust Evaluation

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.server-trust-evaluation
artifact_type: knowledge
title: Server Trust Evaluation
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines when an app should evaluate a server's TLS credentials itself instead of accepting the system's default handling, the two legitimate reasons Apple gives (accepting a credential the system would reject, and pinning to reject one it would accept), the authenticationMethod and host checks that must precede any custom decision, the fact that ATS requirements can be tightened but never loosened, and the blanket-acceptance anti-pattern that disables TLS validation for the whole session.
domain: Networking
tags:
  - networking
  - urlsession
  - tls
  - security
  - certificate-pinning
references:
  - https://developer.apple.com/documentation/foundation/performing-manual-server-trust-authentication
  - https://developer.apple.com/documentation/foundation/handling-an-authentication-challenge
  - https://developer.apple.com/documentation/foundation/urlauthenticationchallenge
  - https://developer.apple.com/documentation/security/preventing-insecure-network-connections
depends_on:
  - knowledge.networking.authentication-challenges
related:
  - knowledge.networking.app-transport-security
last_updated: 2026-08-08
```

## Intent

This contract defines when an AI coding agent should take over evaluation of
a server's TLS credentials, and how. Its central claim is that the common
implementation of this delegate method — accepting
`challenge.protectionSpace.serverTrust` unconditionally — is not a narrow
shortcut but a session-wide disabling of TLS validation, and that it
produces working, passing code, which is why it survives review.

## Scope

### Included

-   Whether manual evaluation is warranted at all, and the two reasons Apple gives
-   The `authenticationMethod` and `host` checks that must gate any decision,
    the relationship to App Transport Security, and blanket acceptance

### Excluded

-   Username/password and other non-TLS challenges — see `authentication-challenges`
-   ATS configuration and exceptions in `Info.plist` — see `app-transport-security`
-   Delegate ownership and invalidation — see `url-session-delegate`

## Rules

### Rule 1

Agents MUST leave server trust to the system unless a stated requirement
demands otherwise. Per Apple's documentation: "In most cases, you should let
the URL Loading System's default handling evaluate the server trust. You get
this behavior when you either don't have a delegate or don't handle
authentication challenges." Adding the method is the decision; omitting it
is the secure default.

### Rule 2

Agents MUST be able to name which of Apple's two reasons applies. Apple gives
exactly two: accepting credentials "that would otherwise be rejected by the
system. For example… a development server that uses a self-signed
certificate", and rejecting credentials "that would otherwise be accepted by
the system. For example, you want to 'pin' your app to a set of specific keys
or certificates under your control." A reason that reduces to "the request
was failing" is the first case applied to production — Rule 5.

### Rule 3

Agents MUST verify both the challenge type and the host before evaluating,
and MUST return `.performDefaultHandling` otherwise. Per Apple's
documentation the implementation must check "the challenge type is server
trust, and not some other kind of challenge" and "the challenge's host name
matches the host that you want to perform manual credential evaluation
for." Omitting the host check applies a pin intended for one API to every
host the session contacts, including third-party SDKs sharing it.

### Rule 4

Agents MUST NOT present manual evaluation as a way around App Transport
Security. Per Apple's documentation: "You cannot loosen server trust
requirements for an ATS-protected domain, but you can tighten them, using
the manual evaluation technique." A delegate written to accept a weak
certificate on an ATS-protected domain does not take effect, so the
connection still fails and the delegate is a false explanation of why.

### Rule 5

Agents MUST NOT emit an unconditional
`.useCredential(URLCredential(trust:))`, and MUST NOT offer it as a
debugging step. It accepts any certificate any host presents for the entire
session, which defeats TLS rather than adjusting it. Development against a
self-signed certificate is Rule 2's first case and still requires Rule 3's
host check, narrowed to the development host and compiled out of release
builds.

## Compliant Example

```swift
func urlSession(_ s: URLSession, didReceive challenge: URLAuthenticationChallenge,
                completionHandler done: @escaping (URLSession.AuthChallengeDisposition,
                                                   URLCredential?) -> Void) {
    let space = challenge.protectionSpace
    guard space.authenticationMethod == NSURLAuthenticationMethodServerTrust,
          space.host == "api.example.com", let trust = space.serverTrust else {
        return done(.performDefaultHandling, nil)                     // Rules 1, 3
    }
    guard pinnedKeys.contains(publicKey(of: trust)) else {            // Rule 2 — pinning
        return done(.cancelAuthenticationChallenge, nil)
    }
    done(.useCredential, URLCredential(trust: trust))
}
```

## Non-Compliant Example

```swift
func urlSession(_ s: URLSession, didReceive challenge: URLAuthenticationChallenge,
                completionHandler done: @escaping (URLSession.AuthChallengeDisposition,
                                                   URLCredential?) -> Void) {
    done(.useCredential, URLCredential(trust: challenge.protectionSpace.serverTrust!))
}
```
Every certificate from every host is accepted for the session's lifetime,
including an attacker's (Rule 5), and neither the challenge type nor the
host is checked (Rule 3). Requests succeed and tests pass, so nothing
surfaces this before shipping.

## Dependencies

- `authentication-challenges` -- it owns challenge dispatch, disposition, and
  the obligation to call the completion handler; this contract owns only the
  server-trust decision inside that structure.

## References

- [Apple Developer — Performing manual server trust authentication](https://developer.apple.com/documentation/foundation/performing-manual-server-trust-authentication)
- [Apple Developer — Handling an authentication challenge](https://developer.apple.com/documentation/foundation/handling-an-authentication-challenge)
- [Apple Developer — URLAuthenticationChallenge](https://developer.apple.com/documentation/foundation/urlauthenticationchallenge)
- [Apple Developer — Preventing insecure network connections](https://developer.apple.com/documentation/security/preventing-insecure-network-connections)
