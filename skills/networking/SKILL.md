---
name: networking
description: Route URLSession async/await networking implementation tasks to the correct Knowledge Contracts — request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, and authenticated requests. Use when writing or reviewing code that makes an HTTP request, decodes a JSON response, or handles a network error in Swift. v1 is async/await URLSession only — no completion-handler dataTask, no Combine dataTaskPublisher, no URLSessionDelegate-based background transfer/progress/custom TLS handling. Sign-in UX/terminology is out of scope here — see the authenticationservices skill. Triggers on URLSession, URLRequest, URLComponents, async await network call, data(for:), JSONDecoder, Codable decoding, DecodingError, HTTPURLResponse, URLError, Task cancellation, URLSessionConfiguration, App Transport Security, ATS, NSAppTransportSecurity, Authorization header, Bearer token, 401 refresh.
id: skill.networking.foundations
title: Networking — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Networking
routes: [knowledge.networking.url-request-construction, knowledge.networking.async-data-fetching, knowledge.networking.codable-decoding, knowledge.networking.http-error-handling, knowledge.networking.task-cancellation, knowledge.networking.url-session-configuration, knowledge.networking.app-transport-security, knowledge.networking.authenticated-requests]
related:
  - skill.authenticationservices.foundations
last_updated: 2026-08-07
---

# Networking — Foundations Skill

## Purpose

Route URLSession async/await networking implementation tasks to the
minimum required Networking Knowledge Contracts. v1 scope is
async/await `URLSession` data-task APIs only — no completion-handler
APIs, no Combine, no `URLSessionDelegate`-based background/progress/TLS
handling.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/networking/.

-   Requests -> url-request-construction.md, async-data-fetching.md, url-session-configuration.md
-   Data handling -> codable-decoding.md, http-error-handling.md
-   Lifecycle -> task-cancellation.md
-   Security & auth -> app-transport-security.md, authenticated-requests.md

Never load more than the contracts relevant to the specific question.
For the sign-in mechanism itself, route to
`skill.authenticationservices.foundations`, and for its wording to
`skill.style-guide.writing` — this Skill covers only the networking
mechanics of attaching credentials to a request.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/networking/ — do not guess or fall back to
general knowledge. Completion-handler `URLSession` APIs, Combine's
`dataTaskPublisher`, and `URLSessionDelegate`-based background transfer,
progress tracking, and custom TLS/challenge handling are deferred to
future scope, not yet built — report that explicitly rather than
answering from general knowledge (see docs/architecture/domain-map.md).
