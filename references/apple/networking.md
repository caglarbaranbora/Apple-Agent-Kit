# Networking

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.networking
artifact_type: reference
title: Networking
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's URLSession documentation behind skill.networking.foundations -- request construction, async/await and completion-handler data fetching, Codable decoding, HTTP error handling, cancellation, session configuration, App Transport Security, authenticated requests, and the delegate-based surface (background transfers, progress, authentication challenges, server trust) plus Combine's dataTaskPublisher.
domain: Networking
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/foundation/urlsession
https://developer.apple.com/documentation/foundation/downloading-files-in-the-background
https://developer.apple.com/documentation/foundation/handling-an-authentication-challenge
https://developer.apple.com/documentation/foundation/httpurlresponse
https://developer.apple.com/documentation/foundation/jsondecoder
https://developer.apple.com/documentation/foundation/performing-manual-server-trust-authentication
https://developer.apple.com/documentation/foundation/urlauthenticationchallenge
https://developer.apple.com/documentation/foundation/urlcomponents
https://developer.apple.com/documentation/foundation/urlerror
https://developer.apple.com/documentation/foundation/urlrequest
https://developer.apple.com/documentation/foundation/urlrequest/setvalue(_:forhttpheaderfield:)
https://developer.apple.com/documentation/foundation/urlsession/authchallengedisposition
https://developer.apple.com/documentation/foundation/urlsession/bytes(for:delegate:)
https://developer.apple.com/documentation/foundation/urlsession/data(for:delegate:)
https://developer.apple.com/documentation/foundation/urlsession/datataskpublisher
https://developer.apple.com/documentation/foundation/urlsession/finishtasksandinvalidate()
https://developer.apple.com/documentation/foundation/urlsession/invalidateandcancel()
https://developer.apple.com/documentation/foundation/urlsessionconfiguration
https://developer.apple.com/documentation/foundation/urlsessionconfiguration/background(withidentifier:)
https://developer.apple.com/documentation/foundation/urlsessiondatatask
https://developer.apple.com/documentation/foundation/urlsessiondelegate
https://developer.apple.com/documentation/foundation/urlsessiondownloaddelegate
https://developer.apple.com/documentation/foundation/urlsessiontask/progress
https://developer.apple.com/documentation/foundation/urlsessiontask/resume()
https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate
https://developer.apple.com/documentation/security/preventing-insecure-network-connections
https://developer.apple.com/documentation/swift/decodingerror
https://developer.apple.com/documentation/swift/task
https://developer.apple.com/documentation/swift/task/checkcancellation()

## Purpose

Reference index for the Apple `URLSession` documentation behind
`skill.networking.foundations`. Covers the whole domain: the async/await
request path (construction, fetching, decoding, error handling,
cancellation, configuration, ATS, authenticated requests) and the
delegate-driven surface built on top of it (background transfers, progress
reporting, authentication challenges, server trust), plus the
completion-handler APIs and Combine's `dataTaskPublisher`. All three API
families index against one Reference because they document one framework
and one Skill routes them; the file was checked against the 98-line cap
when the delegate surface was added in 2026-08 and fits without a split.

Sign-in UX and the sign-in mechanism are not owned here: the mechanism
belongs to `authenticationservices`, the wording to `style-guide`, and form
accessibility to `accessibility` — see docs/architecture/domain-map.md
Cross-Domain Notes. `BGTaskScheduler` background *work*, as opposed to
background *transfers*, is owned by `backgroundtasks`.

## Primary Topics

- Requests and responses: `URLRequest`, `URLComponents`, `HTTPURLResponse`, `URLError`
- Fetching: async/await `data(for:)`, `bytes(for:)`, completion-handler data tasks
- Decoding: `JSONDecoder`, `DecodingError`
- Cancellation: `Task`, `Task.checkCancellation()`
- Sessions: `URLSessionConfiguration`, background configuration, invalidation
- Delegates: session, task, and download protocols; progress callbacks
- Security: App Transport Security, authentication challenges, server trust
- Combine: `URLSession.DataTaskPublisher`

## Used By

- knowledge/networking/url-request-construction.md ([[knowledge/networking/url-request-construction]])
- knowledge/networking/async-data-fetching.md ([[knowledge/networking/async-data-fetching]])
- knowledge/networking/completion-handler-apis.md ([[knowledge/networking/completion-handler-apis]])
- knowledge/networking/data-task-publisher.md ([[knowledge/networking/data-task-publisher]])
- knowledge/networking/codable-decoding.md ([[knowledge/networking/codable-decoding]])
- knowledge/networking/http-error-handling.md ([[knowledge/networking/http-error-handling]])
- knowledge/networking/task-cancellation.md ([[knowledge/networking/task-cancellation]])
- knowledge/networking/url-session-configuration.md ([[knowledge/networking/url-session-configuration]])
- knowledge/networking/url-session-delegate.md ([[knowledge/networking/url-session-delegate]])
- knowledge/networking/background-transfers.md ([[knowledge/networking/background-transfers]])
- knowledge/networking/transfer-progress-tracking.md ([[knowledge/networking/transfer-progress-tracking]])
- knowledge/networking/app-transport-security.md ([[knowledge/networking/app-transport-security]])
- knowledge/networking/authenticated-requests.md ([[knowledge/networking/authenticated-requests]])
- knowledge/networking/authentication-challenges.md ([[knowledge/networking/authentication-challenges]])
- knowledge/networking/server-trust-evaluation.md ([[knowledge/networking/server-trust-evaluation]])
