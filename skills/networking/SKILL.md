---
name: networking
description: Route URLSession networking implementation tasks to the correct Knowledge Contracts — request construction, async/await and completion-handler data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests, session delegates and their invalidation, background transfers, progress reporting, authentication challenges, server trust and certificate pinning, and Combine's dataTaskPublisher. Use when writing or reviewing code that makes an HTTP request, decodes a JSON response, handles a network error, downloads a file in the background, reports transfer progress, or answers a TLS or credential challenge in Swift. Sign-in UX/terminology is out of scope here — see the authenticationservices skill. Triggers on URLSession, URLRequest, URLComponents, async await network call, data(for:), bytes(for:), dataTask, completionHandler, resume(), withCheckedThrowingContinuation, JSONDecoder, Codable decoding, DecodingError, HTTPURLResponse, URLError, Task cancellation, URLSessionConfiguration, background(withIdentifier:), URLSessionDelegate, URLSessionTaskDelegate, URLSessionDownloadDelegate, invalidateAndCancel, finishTasksAndInvalidate, didFinishDownloadingTo, handleEventsForBackgroundURLSession, didWriteData, didSendBodyData, URLAuthenticationChallenge, AuthChallengeDisposition, URLCredential, serverTrust, certificate pinning, App Transport Security, ATS, NSAppTransportSecurity, Authorization header, Bearer token, 401 refresh, dataTaskPublisher.
id: skill.networking.foundations
title: Networking — Foundations
version: 0.2.0
status: Draft
artifact_type: skill
domain: Networking
routes: [knowledge.networking.url-request-construction, knowledge.networking.async-data-fetching, knowledge.networking.completion-handler-apis, knowledge.networking.data-task-publisher, knowledge.networking.codable-decoding, knowledge.networking.http-error-handling, knowledge.networking.task-cancellation, knowledge.networking.url-session-configuration, knowledge.networking.url-session-delegate, knowledge.networking.background-transfers, knowledge.networking.transfer-progress-tracking, knowledge.networking.app-transport-security, knowledge.networking.authenticated-requests, knowledge.networking.authentication-challenges, knowledge.networking.server-trust-evaluation]
related:
  - skill.authenticationservices.foundations
last_updated: 2026-08-07
---

# Networking — Foundations Skill

## Purpose

Route `URLSession` networking implementation tasks to the minimum
required Networking Knowledge Contracts — the async/await request path,
the delegate-driven surface built on top of it, and the two older API
families (completion handlers, Combine) an existing codebase may already
be using.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/networking/.

-   Requests -> url-request-construction.md, async-data-fetching.md, url-session-configuration.md
-   Data handling -> codable-decoding.md, http-error-handling.md
-   Lifecycle -> task-cancellation.md
-   Security & auth -> app-transport-security.md, authenticated-requests.md
-   Delegates -> url-session-delegate.md (URLSessionDelegate, invalidation, delegate queue), background-transfers.md (background(withIdentifier:), handleEventsForBackgroundURLSession, didFinishDownloadingTo), transfer-progress-tracking.md (didWriteData, didSendBodyData, Task.progress)
-   Server challenges -> authentication-challenges.md (URLAuthenticationChallenge, AuthChallengeDisposition, URLCredential), server-trust-evaluation.md (serverTrust, certificate pinning)
-   Older API families -> completion-handler-apis.md (dataTask completionHandler, resume(), continuation bridging), data-task-publisher.md (Combine dataTaskPublisher)

Never load more than the contracts relevant to the specific question.
For the sign-in mechanism itself, route to
`skill.authenticationservices.foundations`, and for its wording to
`skill.style-guide.writing` — this Skill covers only the networking
mechanics of attaching credentials to a request.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/networking/ — do not guess or fall back to
general knowledge.

-   `BGTaskScheduler` background *work*, as opposed to background
    *transfers* — owned by `backgroundtasks`
-   Rendering a progress control or a credential prompt — owned by
    `human-interface-guidelines`
-   Keychain storage of a credential marked `.permanent` — Excluded
-   Writing a custom `URLProtocol` subclass — Excluded
