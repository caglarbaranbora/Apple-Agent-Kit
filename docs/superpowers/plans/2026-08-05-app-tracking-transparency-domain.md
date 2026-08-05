# App Tracking Transparency Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `app-tracking-transparency` domain (1 Reference, 3 Knowledge Contracts, 1 native Skill) covering the ATT authorization prompt and IDFA access via Apple's AppTrackingTransparency and AdSupport frameworks — authorization-request mechanics, status handling and IDFA access, and the `NSUserTrackingUsageDescription` Info.plist requirement — per `docs/superpowers/specs/2026-08-05-app-tracking-transparency-domain-design.md`, replacing the placeholder `app-tracking-transparency` row in `docs/architecture/domain-map.md`. This is the 12th and final Tier 1 domain — completing this task closes out all of Tier 1.

**Architecture:** Mirrors every prior domain exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. Subject matter is Swift API usage (`ATTrackingManager`, `ATTrackingManagerAuthorizationStatus`, `ASIdentifierManager`), so Compliant/Non-Compliant Examples use fenced Swift code blocks, matching the style of `networking` and `local-authentication`. This domain is smaller than prior ones (3 KCs vs. 7–8) because the actual API surface (two frameworks, one method, one property, one enum) is genuinely narrow — padding to more KCs would fragment tightly-coupled rules, a decision already made and approved during brainstorming. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/app-tracking-transparency.md`

**Files:**
- Create: `references/apple/app-tracking-transparency.md`

- [ ] **Step 1: Create the file**

```markdown
# App Tracking Transparency

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/apptrackingtransparency
https://developer.apple.com/documentation/adsupport

## Purpose

Reference index for Apple's AppTrackingTransparency and AdSupport
framework documentation, scoped to this domain's v1: the tracking
authorization request, authorization status handling, IDFA access, and
the required `NSUserTrackingUsageDescription` Info.plist key. tvOS-specific
behavior, SKAdNetwork, AdServices attribution, custom pre-permission
screen design (owned by `human-interface-guidelines`), and App Store
Connect privacy-label disclosure (owned by `app-store-review-guidelines`)
are out of scope.

## Primary Topics

- Authorization request mechanics
- Authorization status handling
- IDFA access
- Usage string and Info.plist requirement

## Used By

- knowledge/app-tracking-transparency/authorization-request.md ([[knowledge/app-tracking-transparency/authorization-request]])
- knowledge/app-tracking-transparency/status-and-idfa-access.md ([[knowledge/app-tracking-transparency/status-and-idfa-access]])
- knowledge/app-tracking-transparency/usage-string-and-info-plist.md ([[knowledge/app-tracking-transparency/usage-string-and-info-plist]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/app-tracking-transparency.md --type reference`
Expected: `PASS: references/apple/app-tracking-transparency.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/app-tracking-transparency.md
git commit -m "docs: add app-tracking-transparency reference index"
```

---

## Task 2: Knowledge Contract — `authorization-request`

**Files:**
- Create: `knowledge/app-tracking-transparency/authorization-request.md`

- [ ] **Step 1: Create the file**

```markdown
# Authorization Request

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-tracking-transparency.authorization-request
type: knowledge
title: Authorization Request
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of ATTrackingManager.requestTrackingAuthorization -- one-time-only semantics, the .active-state requirement, and pre-call status checks.
domain: App Tracking Transparency
tags:
  - app-tracking-transparency
  - attrackingmanager
  - authorization
references:
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)
depends_on: []
related:
  - knowledge.app-tracking-transparency.status-and-idfa-access
  - knowledge.app-tracking-transparency.usage-string-and-info-plist
  - knowledge.human-interface-guidelines.privacy
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent calls
`ATTrackingManager.requestTrackingAuthorization` correctly: understanding
its one-time-only semantics, the conditions under which it will and won't
display a prompt, and checking status before calling it again, so the
app never issues a redundant or silently-ignored authorization request.

## Scope

### Included

-   `ATTrackingManager.requestTrackingAuthorization(completionHandler:)` call mechanics
-   One-time-only semantics: the system remembers the user's decision and doesn't re-prompt unless the app is uninstalled and reinstalled
-   The `UIApplicationState.active` requirement for the prompt to display
-   Pending-prompt, concurrent-call, and app-extension edge cases
-   Checking `trackingAuthorizationStatus == .notDetermined` before calling again
-   Dispatching the completion handler's UI work back to the main queue

### Excluded

-   Custom pre-permission screen design, request timing/UX judgment, purpose-string design conventions — see `knowledge.human-interface-guidelines.privacy`
-   Interpreting the resulting `ATTrackingManagerAuthorizationStatus` value and gating IDFA access on it — see `status-and-idfa-access`
-   The `NSUserTrackingUsageDescription` Info.plist key itself — see `usage-string-and-info-plist`

## Rules

### Rule 1

Agents MUST call `requestTrackingAuthorization` at most once per
authorization decision — Apple's documentation states it "is a one-time
request to authorize or deny access to app-related data that can be used
for tracking the user or the device. The system remembers the user's
choice and doesn't prompt again unless a user uninstalls and then
reinstalls the app on the device." Calling it again after a decision has
been made does not re-prompt; it simply invokes the completion handler
with the existing status.

### Rule 2

Agents MUST check `ATTrackingManager.trackingAuthorizationStatus ==
.notDetermined` before calling `requestTrackingAuthorization` again in
any code path that might run more than once (e.g. a settings screen with
a "Manage Tracking" button, or a feature entry point reached multiple
times per session) — calling it when status is already
`.authorized`/`.denied`/`.restricted` wastes a call for no effect, since
Rule 1 guarantees no new prompt appears.

### Rule 3

Agents MUST NOT assume `requestTrackingAuthorization` will display a
prompt in every call — per Apple's documentation, "calls to the API only
prompt when the application state is `UIApplicationStateActive`. The
authorization prompt doesn't display if another permission request is
pending user confirmation... and calls to the API through an app
extension don't prompt." Code that calls this from a background task, a
notification-response handler before the app becomes active, or an app
extension must not assume a completion handler result means the user was
actually shown anything.

### Rule 4

Agents MUST dispatch UI updates inside `requestTrackingAuthorization`'s
completion handler back to the main queue — the completion handler is
not guaranteed to run on the main thread, and any UI mutation (enabling
a feature, updating a label) triggered directly from it must be wrapped
in `DispatchQueue.main.async` or use the `async` `Task { @MainActor in
... }` pattern.

## Compliant Example

```swift
func requestTrackingIfNeeded() {
    guard ATTrackingManager.trackingAuthorizationStatus == .notDetermined else {
        return // Already decided -- see status-and-idfa-access.md for handling existing status.
    }

    ATTrackingManager.requestTrackingAuthorization { status in
        Task { @MainActor in
            updateUI(for: status)
        }
    }
}
```
Checks `.notDetermined` before calling (Rule 2), and dispatches the resulting UI update back to the main actor (Rule 4). (Rules 2, 4)

## Non-Compliant Example

```swift
func showTrackingPromptOnEveryLaunch() {
    ATTrackingManager.requestTrackingAuthorization { status in
        updateUI(for: status) // Called directly from the completion handler -- not guaranteed to be on the main thread.
    }
}
// Called unconditionally from applicationDidBecomeActive every launch.
```
Calls `requestTrackingAuthorization` unconditionally on every launch without checking status first (wasted call once a decision exists, Rule 2), and updates UI directly from the completion handler without dispatching to the main queue (Rule 4).

## Dependencies

None.

## References

-   [Apple Developer — ATTrackingManager](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager)
-   [Apple Developer — requestTrackingAuthorization(completionHandler:)](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-tracking-transparency/authorization-request.md --type knowledge`
Expected: `PASS: knowledge/app-tracking-transparency/authorization-request.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-tracking-transparency/authorization-request.md
git commit -m "feat: add authorization-request knowledge contract"
```

---

## Task 3: Knowledge Contract — `status-and-idfa-access`

**Files:**
- Create: `knowledge/app-tracking-transparency/status-and-idfa-access.md`

- [ ] **Step 1: Create the file**

```markdown
# Status and IDFA Access

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-tracking-transparency.status-and-idfa-access
type: knowledge
title: Status and IDFA Access
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct handling of ATTrackingManagerAuthorizationStatus and ASIdentifierManager.advertisingIdentifier, including the zeroed-UUID fallback and the requirement to read both live rather than cache them.
domain: App Tracking Transparency
tags:
  - app-tracking-transparency
  - idfa
  - authorization-status
references:
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/authorizationstatus-swift.enum
  - https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier
depends_on: []
related:
  - knowledge.app-tracking-transparency.authorization-request
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent interprets
`ATTrackingManagerAuthorizationStatus` and accesses
`ASIdentifierManager.advertisingIdentifier` correctly, so tracking-dependent
code paths are gated on the right status value and never rely on a stale
or incorrectly-cached IDFA.

## Scope

### Included

-   `ATTrackingManagerAuthorizationStatus` values (`.notDetermined`, `.restricted`, `.denied`, `.authorized`) and required agent behavior per value
-   `ASIdentifierManager.advertisingIdentifier` and its zeroed-UUID (`00000000-0000-0000-0000-000000000000`) fallback behavior
-   The requirement to read `advertisingIdentifier` live rather than store it
-   The requirement to re-check `trackingAuthorizationStatus` at each point of use rather than caching a value from launch

### Excluded

-   The `requestTrackingAuthorization` call itself — see `authorization-request`
-   App Store Connect privacy-label tracking-use disclosure — see `knowledge.app-store-review-guidelines.privacy-nutrition-label`

## Rules

### Rule 1

Agents MUST gate any tracking-dependent code path (attaching the IDFA to
an ad request, cross-app/cross-site event correlation, sharing data with
a data broker) on `ATTrackingManager.trackingAuthorizationStatus ==
.authorized` specifically — `.notDetermined`, `.restricted`, and
`.denied` all mean tracking-dependent behavior must not run, even though
they are three semantically distinct states (not yet asked, blocked by
a profile/parental control, and explicitly declined by the user,
respectively).

### Rule 2

Agents MUST NOT treat a zeroed `advertisingIdentifier`
(`00000000-0000-0000-0000-000000000000`) as a valid device identifier —
Apple's documentation lists multiple cases that return an all-zero
value, including "if you haven't requested authorization" and "if you've
requested authorization... and the user declines," alongside Simulator,
macOS, and visionOS-compatibility-mode always returning zeros regardless
of status. Code MUST check `trackingAuthorizationStatus == .authorized`
before treating the value as usable, not just check whether it happens
to be non-zero.

### Rule 3

Agents MUST NOT store or cache `advertisingIdentifier` in
`UserDefaults`, a database, or any persisted model — Apple's
documentation states "as a best practice, don't store the advertising
identifier value; access `advertisingIdentifier` instead," since the
user can change authorization in Settings > Privacy > Tracking at any
time without relaunching the app, which would leave a cached value stale
and pointing at a now-revoked identifier.

### Rule 4

Agents MUST re-check `trackingAuthorizationStatus` at each point of use
(e.g. immediately before constructing an ad request) rather than caching
the status from app launch or from the `requestTrackingAuthorization`
completion handler — the same Settings-change-without-relaunch behavior
from Rule 3 applies to the status value itself, not just the identifier.

## Compliant Example

```swift
func idfaForAdRequest() -> String? {
    guard ATTrackingManager.trackingAuthorizationStatus == .authorized else {
        return nil
    }
    return ASIdentifierManager.shared().advertisingIdentifier.uuidString
}
```
Checks live status immediately before reading the identifier, gates strictly on `.authorized`, and never stores the result. (Rules 1, 3, 4)

## Non-Compliant Example

```swift
class AdConfig {
    static let cachedIDFA = ASIdentifierManager.shared().advertisingIdentifier.uuidString // Read once at launch and cached.

    static func attachTrackingID(to request: inout URLRequest) {
        if cachedIDFA != "00000000-0000-0000-0000-000000000000" {
            request.setValue(cachedIDFA, forHTTPHeaderField: "X-Ad-ID")
        }
    }
}
```
Reads and caches the identifier once at launch instead of live at point of use (Rule 3), and checks only whether the string happens to be non-zero instead of checking `trackingAuthorizationStatus == .authorized` (Rule 2) — if the user revokes tracking permission in Settings after launch, this code keeps sending the stale cached identifier.

## Dependencies

None.

## References

-   [Apple Developer — ATTrackingManager.AuthorizationStatus](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/authorizationstatus-swift.enum)
-   [Apple Developer — advertisingIdentifier](https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-tracking-transparency/status-and-idfa-access.md --type knowledge`
Expected: `PASS: knowledge/app-tracking-transparency/status-and-idfa-access.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-tracking-transparency/status-and-idfa-access.md
git commit -m "feat: add status-and-idfa-access knowledge contract"
```

---

## Task 4: Knowledge Contract — `usage-string-and-info-plist`

**Files:**
- Create: `knowledge/app-tracking-transparency/usage-string-and-info-plist.md`

- [ ] **Step 1: Create the file**

```markdown
# Usage String and Info.plist

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-tracking-transparency.usage-string-and-info-plist
type: knowledge
title: Usage String and Info.plist
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the required NSUserTrackingUsageDescription Info.plist key and its wording rules, without which requestTrackingAuthorization fails at runtime.
domain: App Tracking Transparency
tags:
  - app-tracking-transparency
  - info-plist
  - nsusertrackingusagedescription
references:
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsusertrackingusagedescription
  - https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)
depends_on: []
related:
  - knowledge.app-tracking-transparency.authorization-request
  - knowledge.app-store-review-guidelines.permission-usage-strings
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent configures the required
`NSUserTrackingUsageDescription` Info.plist key, so a call to
`requestTrackingAuthorization` has task-specific copy and doesn't fail
at runtime.

## Scope

### Included

-   `NSUserTrackingUsageDescription` as a required Info.plist key before calling `requestTrackingAuthorization`
-   Wording rules: specific, explains the actual tracking use, not a generic placeholder

### Excluded

-   General Info.plist permission-usage-string conventions not specific to ATT — see `knowledge.app-store-review-guidelines.permission-usage-strings`
-   The `requestTrackingAuthorization` call mechanics themselves — see `authorization-request`

## Rules

### Rule 1

Agents MUST add an `NSUserTrackingUsageDescription` key with a non-empty
string value to the app's Info.plist before shipping any code path that
calls `requestTrackingAuthorization` — Apple's documentation states that
"to use `requestTrackingAuthorization(completionHandler:)`, the
`NSUserTrackingUsageDescription` key must be in the Information Property
List." Omitting this key is not a degraded-prompt situation; the
authorization request fails outright.

### Rule 2

Agents MUST write `NSUserTrackingUsageDescription`'s value as a
specific, task-grounded sentence describing the actual tracking use
(e.g. "Your data will be used to deliver personalized ads and measure
their effectiveness."), not a generic placeholder like "This app uses
tracking" — the same accuracy standard `permission-usage-strings.md`
applies to other Info.plist usage-description keys applies here.

### Rule 3

Agents MUST NOT write `NSUserTrackingUsageDescription` copy that
implies tracking is required for the app to function, when it is not —
the string should describe what tracking-dependent features (e.g.
personalized ads) do, not pressure the user into granting a permission
that is genuinely optional for the app's core functionality.

## Compliant Example

```xml
<!-- Info.plist -->
<key>NSUserTrackingUsageDescription</key>
<string>Your data will be used to deliver personalized ads and measure their effectiveness.</string>
```
```swift
ATTrackingManager.requestTrackingAuthorization { status in
    Task { @MainActor in
        updateUI(for: status)
    }
}
```
The usage string is specific about what tracking is used for, and the app calls `requestTrackingAuthorization` only after this key is present. (Rules 1, 2)

## Non-Compliant Example

```xml
<!-- Info.plist has no NSUserTrackingUsageDescription entry at all. -->
```
```swift
ATTrackingManager.requestTrackingAuthorization { status in
    updateUI(for: status)
}
```
Missing `NSUserTrackingUsageDescription` causes `requestTrackingAuthorization` to fail the first time this line runs. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — NSUserTrackingUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsusertrackingusagedescription)
-   [Apple Developer — requestTrackingAuthorization(completionHandler:)](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-tracking-transparency/usage-string-and-info-plist.md --type knowledge`
Expected: `PASS: knowledge/app-tracking-transparency/usage-string-and-info-plist.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-tracking-transparency/usage-string-and-info-plist.md
git commit -m "feat: add usage-string-and-info-plist knowledge contract"
```

---

## Task 5: Native Skill — `skills/app-tracking-transparency/SKILL.md`

**Files:**
- Create: `skills/app-tracking-transparency/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: app-tracking-transparency
description: Route App Tracking Transparency / IDFA implementation tasks to the correct Knowledge Contracts -- authorization request mechanics, authorization status handling, IDFA access, and the NSUserTrackingUsageDescription Info.plist requirement. Use when calling requestTrackingAuthorization, checking trackingAuthorizationStatus, reading advertisingIdentifier, or writing NSUserTrackingUsageDescription. v1 is iOS/iPadOS AppTrackingTransparency + AdSupport framework API only -- no tvOS-specific behavior, no SKAdNetwork, no AdServices attribution. Triggers on ATTrackingManager, requestTrackingAuthorization, trackingAuthorizationStatus, ATTrackingManagerAuthorizationStatus, ASIdentifierManager, advertisingIdentifier, IDFA, NSUserTrackingUsageDescription, App Tracking Transparency, tracking authorization.
id: skill.app-tracking-transparency.foundations
title: App Tracking Transparency — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: App Tracking Transparency
routes: [knowledge.app-tracking-transparency.authorization-request, knowledge.app-tracking-transparency.status-and-idfa-access, knowledge.app-tracking-transparency.usage-string-and-info-plist]
related: []
last_updated: 2026-08-05
---

# App Tracking Transparency — Foundations Skill

## Purpose

Route App Tracking Transparency / IDFA implementation tasks to the
minimum required App Tracking Transparency Knowledge Contracts. v1 scope
is the iOS/iPadOS AppTrackingTransparency and AdSupport framework API —
no tvOS-specific behavior, no SKAdNetwork, no AdServices attribution.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-tracking-transparency/.

-   Calling requestTrackingAuthorization or handling its call mechanics -> authorization-request.md
-   Checking trackingAuthorizationStatus or reading advertisingIdentifier -> status-and-idfa-access.md
-   Writing NSUserTrackingUsageDescription -> usage-string-and-info-plist.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-tracking-transparency/ — do not guess or fall
back to general knowledge. tvOS-specific App Tracking Transparency
behavior, SKAdNetwork, and AdServices attribution are deferred to future
scope, not yet built — report that explicitly rather than answering from
general knowledge (see docs/architecture/domain-map.md). Custom
pre-permission screen design and request-timing UX judgment are owned by
the `human-interface-guidelines` Skill, not this one.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/app-tracking-transparency/SKILL.md --type skill`
Expected: `PASS: skills/app-tracking-transparency/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/app-tracking-transparency/SKILL.md
git commit -m "feat: add app-tracking-transparency native skill"
```

---

## Task 6: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`local-authentication` row (the row containing
`skills/local-authentication/SKILL.md`):

```markdown
| ATTrackingManager, requestTrackingAuthorization, trackingAuthorizationStatus, ATTrackingManagerAuthorizationStatus, ASIdentifierManager, advertisingIdentifier, IDFA, NSUserTrackingUsageDescription, App Tracking Transparency, tracking authorization | skills/app-tracking-transparency/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `12` (authentication, style-guide, human-interface-guidelines,
app-store-review-guidelines, swiftui, accessibility, uikit, sf-symbols,
networking, xcode, local-authentication, app-tracking-transparency)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add app-tracking-transparency to skills index"
```

---

## Task 7: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `app-tracking-transparency` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| App Tracking Transparency | app-tracking-transparency | ATT prompt, IDFA access | Tracking-permission prompt and IDFA access conventions |
```

Replace with:

```markdown
| App Tracking Transparency | app-tracking-transparency | iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1: authorization-request mechanics (one-time-only semantics, .active-state requirement), authorization status handling, IDFA access (zeroed-UUID fallback, don't-cache rule), NSUserTrackingUsageDescription. No tvOS-specific behavior, no SKAdNetwork, no AdServices attribution. | Tracking-permission API implementation and IDFA access conventions |
```

- [ ] **Step 2: Add three new Cross-Domain Notes bullets**

Add these three bullets at the end of the `## Cross-Domain Notes` list
(after the `local-authentication`/`authentication` bullet, which is
currently the last one):

```markdown
- `app-tracking-transparency` and `human-interface-guidelines` overlap: `knowledge.human-interface-guidelines.privacy` already covers "Tracking-permission-alert integrity rules" (its Rules 3–4: custom pre-permission screen constraints, no deceptive screens before the system tracking alert) as a design/UX topic. Resolved via angle-split — `human-interface-guidelines` keeps the design/UX layer (whether/how to show a custom pre-permission screen, its button/copy constraints, anti-deception rule), `app-tracking-transparency` owns the API layer (the `requestTrackingAuthorization` call mechanics, the status enum, IDFA access). `app-tracking-transparency`'s `authorization-request.md` cross-references `knowledge.human-interface-guidelines.privacy` via `related:` rather than restating its Rules, same cross-domain `related:` pattern already used by `sf-symbols` KCs referencing `human-interface-guidelines`.
- `app-tracking-transparency` and `app-store-review-guidelines` (`privacy-nutrition-label` topic) do not overlap — this is a clean handoff. `privacy-nutrition-label.md`'s Rule 3 already states tracking-use marking "additionally requires App Tracking Transparency permission" without describing the API itself; `app-tracking-transparency` is the implementation that KC points at. No content is duplicated between the two domains.
- `app-tracking-transparency` and `app-store-review-guidelines` (`permission-usage-strings` topic) do not overlap — this is a clean handoff, same pattern as `local-authentication`'s `NSFaceIDUsageDescription` KC vs. the same `permission-usage-strings.md`. That KC's own examples (`NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`) never name `NSUserTrackingUsageDescription`; `app-tracking-transparency`'s `usage-string-and-info-plist.md` owns that key's wording specifically. No content is duplicated between the two domains.
```

- [ ] **Step 3: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt), `xcode` (Tier 1 — Xcode GUI/project-file v1: build configurations & xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; xcodebuild CLI, CI signing automation, and Swift Package Manager build configuration remain unbuilt), `local-authentication` (Tier 1 — iOS/iPadOS LocalAuthentication framework API v1: availability/biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; macOS/watchOS-specific behavior and general Keychain storage remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt), `xcode` (Tier 1 — Xcode GUI/project-file v1: build configurations & xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; xcodebuild CLI, CI signing automation, and Swift Package Manager build configuration remain unbuilt), `local-authentication` (Tier 1 — iOS/iPadOS LocalAuthentication framework API v1: availability/biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; macOS/watchOS-specific behavior and general Keychain storage remain unbuilt), `app-tracking-transparency` (Tier 1 — iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1: authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; tvOS-specific behavior, SKAdNetwork, and AdServices attribution remain unbuilt). **All 12 Tier 1 domains complete.**
```

- [ ] **Step 4: Validate manually**

Run: `grep -c "app-tracking-transparency" docs/architecture/domain-map.md`
Expected: a number greater than 1 (the updated row, the new Completed
line clause, and the three new Cross-Domain Notes bullets all mention
"app-tracking-transparency")

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope app-tracking-transparency v1, add cross-domain notes, close out Tier 1"
```

---

## Task 8: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `local-authentication` bullet,
immediately before the `Full routing tables:` line):

```markdown
- **`local-authentication`** — Routes Face ID/Touch ID/device-passcode implementation tasks (availability and biometry-type detection, policy evaluation, reason strings and Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX) to Local Authentication Knowledge Contracts.
  Example: `"Face ID prompt shows the wrong icon"` → `availability-and-biometry-type.md`
  Example: `"user is locked out of Face ID after too many failed attempts"` → `error-handling.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`local-authentication`** — Routes Face ID/Touch ID/device-passcode implementation tasks (availability and biometry-type detection, policy evaluation, reason strings and Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX) to Local Authentication Knowledge Contracts.
  Example: `"Face ID prompt shows the wrong icon"` → `availability-and-biometry-type.md`
  Example: `"user is locked out of Face ID after too many failed attempts"` → `error-handling.md`

- **`app-tracking-transparency`** — Routes App Tracking Transparency / IDFA implementation tasks (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription) to App Tracking Transparency Knowledge Contracts.
  Example: `"how do I ask for tracking permission without re-prompting every launch"` → `authorization-request.md`
  Example: `"advertisingIdentifier is returning all zeros"` → `status-and-idfa-access.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Update the What's New section (3-item cap)**

Find this exact block (the current `## What's New` section — 3 dated
lines plus the CHANGELOG.md link):

```markdown
## What's New

- 2026-08-05 — Added `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication` (which excludes biometrics entirely), replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `networking` Skill (URL request construction, async data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; async/await URLSession v1) — 8 Knowledge Contracts. Fills the "Authentication networking" gap authentication.md explicitly excludes, and replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

Replace with (new line added at top, oldest of the 3 — the `networking`
line — drops off since the cap stays at 3 dated lines):

```markdown
## What's New

- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 12 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- 2026-08-05 — Added `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication` (which excludes biometrics entirely), replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "app-tracking-transparency" README.md`
Expected: a number greater than 0 (the new Skills bullet and What's New
line are the first mentions of "app-tracking-transparency" in this file)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add app-tracking-transparency to README Skills + What's New"
```

---

## Task 9: Update `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add a new Unreleased entry**

Find this exact block (the current `## [Unreleased]` section):

```markdown
## [Unreleased]
### Added
- `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication`, replaces the prior placeholder scope in domain-map.md.
- `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
```

Replace with:

```markdown
## [Unreleased]
### Added
- `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 12 Tier 1 domains, replaces the prior placeholder scope in domain-map.md.
- `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication`, replaces the prior placeholder scope in domain-map.md.
- `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "app-tracking-transparency" CHANGELOG.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add app-tracking-transparency changelog entry"
```

---

## Task 10: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/app-tracking-transparency.md --type reference
python3 scripts/validate_artifact.py skills/app-tracking-transparency/SKILL.md --type skill
for f in knowledge/app-tracking-transparency/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
```
Expected: `PASS` for all 5 files.

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 4: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 9 prior tasks committed).

- [ ] **Step 5: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire `app-tracking-transparency`
domain (all 5 new files plus the 4 modified docs) to check cross-file
consistency: every `related:`/`depends_on:` KC id resolves to a real
file, the Skill's `routes:` list matches exactly the 3 KC ids, the
Reference's "Used By" list matches exactly the 3 KC files, layer order
(References → Knowledge → Skills) is respected. The review must
specifically check for v1-scope violations and cross-domain drift (this
class of bug slipped through per-task review in the `xcode` build and
was only caught by the final holistic pass; the `local-authentication`
build's final pass also caught a stale trigger-word collision in a
sibling domain's Skill file — check for the same class of issue here):

-   No content anywhere describing tvOS-specific App Tracking
    Transparency behavior, SKAdNetwork, or AdServices attribution
-   No KC restates `human-interface-guidelines`'s tracking-alert-UX
    Rules (custom pre-permission screen constraints) — verify the
    angle-split boundary actually holds, not just that it's described
    correctly in domain-map.md
-   No KC restates `app-store-review-guidelines`'s privacy-nutrition-label
    or permission-usage-strings content
-   Check whether any existing Skill's `description`/trigger-word list
    (particularly `human-interface-guidelines` and
    `app-store-review-guidelines`) now collides with this domain's new
    trigger words (`ATTrackingManager`, `IDFA`, `tracking authorization`,
    etc.) the way `skills/authentication/SKILL.md` collided with
    `local-authentication`'s trigger words in the prior domain build
-   Every cited Apple Developer URL is live (spot-check a sample with
    `curl -s -o /dev/null -w "%{http_code}"`)

Report findings; fix any issues found and re-commit before considering
the domain complete. Once this passes, all 12 Tier 1 domains are done —
flag this explicitly in the final report, since the next step after this
task is a full-repo final review before v1 release, not another domain.

---

## Self-Review Notes

-   **Spec coverage:** All 3 KC topics from the design spec's "Knowledge
    Contracts (3)" section have a task (Tasks 2–4), matching titles and
    scope exactly. The spec's Reference section is Task 1. The spec's
    Skill section (trigger keywords, routing clusters) is Task 5. The
    spec's Cross-Domain Boundary section (all three sub-boundaries) is
    reflected in Task 7 Step 2's three new Cross-Domain Notes bullets.
    The spec's Documentation Updates section is covered by Tasks 6, 8, 9.
-   **Placeholder scan:** No TBD/TODO; every Rule, Example, and Reference
    URL is concrete and was live-verified via `curl` against Apple's
    documentation JSON API during brainstorming (see Task 10 Step 5 for
    the re-check to run post-hoc).
-   **Type/id consistency:** Every KC `id`
    (`knowledge.app-tracking-transparency.<slug>`) referenced in Task 5's
    `routes:` list and Task 1's "Used By" list matches the `id` defined
    in that KC's own Task 2–4 Metadata block. Every `related:`
    cross-reference within the domain (e.g.
    `knowledge.app-tracking-transparency.status-and-idfa-access` listed in
    `authorization-request`'s `related:`) points at an id defined in this
    same plan; every cross-domain `related:` reference
    (`knowledge.human-interface-guidelines.privacy`,
    `knowledge.app-store-review-guidelines.privacy-nutrition-label`,
    `knowledge.app-store-review-guidelines.permission-usage-strings`)
    points at a file confirmed to already exist in the repo (checked
    during brainstorming).
