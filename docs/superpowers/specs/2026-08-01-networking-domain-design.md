# Networking Domain Design

Status: Draft Version: 0.1.0

## Purpose

Replace the placeholder `networking` entry in `docs/architecture/domain-map.md`
(Initial Scope: "URLSession, ATS", Owns: "URLSession usage and App
Transport Security conventions") with a real Tier 1 domain covering
`URLSession`-based HTTP networking in Swift — how an AI coding agent
constructs requests, fetches data with structured concurrency, decodes
responses, handles errors, and attaches authentication to a network call.

This is the first backend/API-layer domain built this session — every
prior domain (`style-guide`, `human-interface-guidelines`,
`app-store-review-guidelines`, `swiftui`, `uikit`, `accessibility`,
`sf-symbols`) has been UI/design-facing.

## Context

`authentication` (shipped, Existing/Unscheduled tier) already routes
sign-in/session/credential *UX* implementation, but its own Knowledge
Contract (`knowledge/authentication/authentication.md`) explicitly lists
"Authentication networking" and "Backend architecture" under its
Excluded section — this domain fills that gap for the networking-mechanics
half (attaching a token to a request, retrying after a 401), while
`authentication` continues to own the UX/flow side (terminology, entry
points, form accessibility). No content is duplicated between the two;
this is a clean handoff, not an overlap requiring an angle-split.

## Decisions

### Decision 1: v1 API surface — async/await only

v1 covers `URLSession`'s structured-concurrency APIs
(`data(for:)`, `upload(for:)`, `download(for:)` with `async`/`await`).
Completion-handler-based APIs (`dataTask(with:completionHandler:)`) and
Combine's `dataTaskPublisher` are out of v1 — consistent with this
session's `swiftui` domain also targeting iOS 17+ conventions over
legacy patterns.

### Decision 2: `URLSessionDelegate`-based APIs excluded from v1

Background transfers, progress tracking, and custom TLS/challenge
handling all require `URLSessionDelegate` conformance, a fundamentally
different (callback-based, not structured-concurrency) API shape. v1
stays within the `async`/`await` data-task surface; delegate-based APIs
are deferred, not silently dropped — recorded in Build Order and the
Skill's Stop Conditions.

### Decision 3: Codable/JSON decoding is its own topic

Decoding is atomic enough (decoding strategies, decode-error handling,
optional/default-value handling) to warrant its own Knowledge Contract
rather than folding into request/response handling — matches the
atomicity precedent set by every prior domain's Knowledge Contracts.

### Decision 4: 8-topic atomic breakdown

| # | Slug | Covers |
|---|---|---|
| 1 | `url-request-construction` | Building a `URLRequest` — HTTP method, headers, body encoding |
| 2 | `async-data-fetching` | `URLSession.shared.data(for:)`/`upload(for:)`/`download(for:)` with `async`/`await` |
| 3 | `codable-decoding` | `JSONDecoder`, decoding strategies (`keyDecodingStrategy`, `dateDecodingStrategy`), decode-error handling |
| 4 | `http-error-handling` | HTTP status code checking, `URLError`, distinguishing network/decode/server error categories |
| 5 | `task-cancellation` | `Task` cancellation propagation, `Task.isCancelled`/`Task.checkCancellation()`, cooperative cancellation with `URLSession` |
| 6 | `url-session-configuration` | `URLSessionConfiguration` (`.default`/`.ephemeral`), timeout intervals, cache policy |
| 7 | `app-transport-security` | ATS requirements, `NSAppTransportSecurity` Info.plist exception keys, when an exception is (and isn't) justified |
| 8 | `authenticated-requests` | Attaching an `Authorization` header to a request, 401-triggered token-refresh-and-retry pattern |

Topics 7 and 8 fill the gap `authentication.md` explicitly excludes
("Authentication networking"), per Decision-context above.

### Decision 5: Cross-domain resolution

- **`networking` ↔ `authentication`**: clean handoff, not an overlap —
  `authentication` owns sign-in UX/terminology/flow, `networking` owns
  the mechanics of attaching credentials to a request and handling
  auth-related HTTP responses (401). `authenticated-requests.md`
  cross-references `knowledge.authentication.authentication` via
  `related:`.
- **`networking` ↔ `app-store-review-guidelines`**: no real overlap
  found. ATS's Info.plist declaration is this domain's implementation
  concern; App Store Review's existing privacy content (5.1.1/5.1.2) is
  about data-collection *disclosure* accuracy, not network transport
  security — different concern entirely. No Cross-Domain Notes entry
  needed beyond a one-line confirmation that no overlap exists (recorded
  for future domain builders who might otherwise assume one).
- **`networking` ↔ `swiftui`/`uikit`**: neither prior domain has any
  networking content; no boundary to resolve.

### Decision 6: File layout

```
references/apple/networking.md
knowledge/networking/url-request-construction.md
knowledge/networking/async-data-fetching.md
knowledge/networking/codable-decoding.md
knowledge/networking/http-error-handling.md
knowledge/networking/task-cancellation.md
knowledge/networking/url-session-configuration.md
knowledge/networking/app-transport-security.md
knowledge/networking/authenticated-requests.md
skills/networking/SKILL.md
```

### Decision 7: Skill routing clusters

`skills/networking/SKILL.md` routes across 4 clusters:
- **Requests**: `url-request-construction`, `async-data-fetching`, `url-session-configuration`
- **Data handling**: `codable-decoding`, `http-error-handling`
- **Lifecycle**: `task-cancellation`
- **Security & auth**: `app-transport-security`, `authenticated-requests`

`related:` lists `skill.authentication.login` — confirmed to be
`authentication`'s actual Skill id (its native `SKILL.md` predates this
session's domain builds but already uses the hardened frontmatter
format, `id: skill.authentication.login`, verified directly against
`skills/authentication/SKILL.md`).

### Decision 8: domain-map.md update

- `networking` row: Initial Scope replaced with the real v1 scope from
  Decision 1/4; Owns updated to reflect the 8-topic breakdown
- Build Order "Completed" line: append `networking` entry with its scope
  and explicitly-deferred items (completion-handler APIs, Combine
  `dataTaskPublisher`, `URLSessionDelegate`-based background
  transfer/progress/TLS handling)
- Cross-Domain Notes: add the `networking`↔`authentication` handoff
  entry per Decision 5

## Consequences

- Agents asking "how do I fetch and decode JSON from an API" get routed
  to `networking`, with a clear boundary against `authentication` so
  sign-in-flow and network-request concerns don't get conflated.
- Delegate-based background transfer/progress tracking remains a
  documented gap — flagged in Build Order, not silently missing.
- `README.md` gets a new `## Skills` bullet and a new `## What's New`
  top line, per `CLAUDE.md`'s same-PR requirement.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py <path> --type knowledge` for
  each of the 8 KCs and the Reference (`--type reference`)
- `python3 scripts/validate_artifact.py skills/networking/SKILL.md --type skill`
- `python3 -m unittest tests/test_validate_artifact.py -v`
- Every cited Apple Developer URL live-verified (`curl`/JSON endpoint,
  not WebFetch's summarized output) to resolve — standard practice this
  session after repeatedly catching dead/ambiguous URLs in the `uikit`
  and `sf-symbols` domain builds
- Final holistic review pass across all 8 KCs for v1-scope consistency
  (no completion-handler/Combine content, no `URLSessionDelegate`
  content, no duplicated authentication-UX content) — this class of
  issue was only caught by the holistic pass, not per-task review, in
  both the `uikit` and `sf-symbols` domain builds

## Out of Scope

- Completion-handler-based `URLSession` APIs — future work, unassigned owner
- Combine's `dataTaskPublisher` — future work, unassigned owner
- `URLSessionDelegate`-based background transfer, progress tracking, and custom TLS/challenge handling — future work, unassigned owner
- GraphQL, WebSocket, or gRPC networking — out of this domain's HTTP/REST-via-URLSession scope entirely
