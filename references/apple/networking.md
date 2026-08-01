# Networking

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/foundation/urlsession

## Purpose

Reference index for Apple's URLSession networking documentation, scoped
to this domain's v1: async/await HTTP networking — request construction,
structured-concurrency data fetching, Codable-based JSON decoding, error
handling, task cancellation, session configuration, App Transport
Security requirements, and authenticated request patterns. Completion-
handler-based `URLSession` APIs, Combine's `dataTaskPublisher`, and
`URLSessionDelegate`-based APIs (background transfers, progress
tracking, custom TLS/challenge handling) are deferred to a future pass.
Authentication UX/flow (sign-in terminology, entry points, form
accessibility) is owned by the `authentication` domain, not this one —
see docs/architecture/domain-map.md Cross-Domain Notes.

## Primary Topics

- URL request construction
- Async data fetching
- Codable decoding
- HTTP error handling
- Task cancellation
- URL session configuration
- App Transport Security
- Authenticated requests

## Used By

- knowledge/networking/url-request-construction.md ([[knowledge/networking/url-request-construction]])
- knowledge/networking/async-data-fetching.md ([[knowledge/networking/async-data-fetching]])
- knowledge/networking/codable-decoding.md ([[knowledge/networking/codable-decoding]])
- knowledge/networking/http-error-handling.md ([[knowledge/networking/http-error-handling]])
- knowledge/networking/task-cancellation.md ([[knowledge/networking/task-cancellation]])
- knowledge/networking/url-session-configuration.md ([[knowledge/networking/url-session-configuration]])
- knowledge/networking/app-transport-security.md ([[knowledge/networking/app-transport-security]])
- knowledge/networking/authenticated-requests.md ([[knowledge/networking/authenticated-requests]])
