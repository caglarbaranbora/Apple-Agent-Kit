# Reason Strings and Info.plist

Status: Draft Version: 0.1.0

## Metadata

```yaml
id: knowledge.local-authentication.reason-strings-and-info-plist
type: knowledge
title: Reason Strings and Info.plist
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct localizedReason copy rules and the required NSFaceIDUsageDescription Info.plist key, without which Face ID calls fail at runtime.
domain: Local Authentication
tags:
  - local-authentication
  - info-plist
  - localizedreason
references:
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsfaceidusagedescription
  - https://developer.apple.com/documentation/localauthentication/lacontext
depends_on: []
related:
  - knowledge.local-authentication.policy-evaluation
  - knowledge.local-authentication.error-handling
updated: 2026-08-05
```

## Intent

This contract defines how an AI coding agent writes the `localizedReason`
string passed to `evaluatePolicy` and configures the required
`NSFaceIDUsageDescription` Info.plist key, so a Face ID prompt has
task-specific copy and doesn't crash the app outright.

## Scope

### Included

-   `NSFaceIDUsageDescription` as a required Info.plist key for any app that calls Face ID APIs
-   `localizedReason` copy rules: task-specific, no restating "authenticate" or the app name
-   Where `localizedReason` appears in the system prompt relative to `NSFaceIDUsageDescription`

### Excluded

-   The fallback button's title string — see `fallback-ux-and-passcode`
-   `LAError` handling once evaluation has started — see `error-handling`

## Rules

### Rule 1

Agents MUST add an `NSFaceIDUsageDescription` key with a non-empty string
value to the app's Info.plist before shipping any code path that can call
`evaluatePolicy` on a Face ID-capable device — omitting this key does not
merely produce a degraded prompt; the app crashes when it attempts to use
Face ID, since iOS enforces the usage-description requirement the same
way it does for camera or location access.

### Rule 2

Agents MUST write `NSFaceIDUsageDescription`'s value as a specific,
task-grounded sentence (e.g. "Use Face ID to unlock your saved
passwords."), not a generic placeholder like "This app uses Face ID" —
App Review rejects usage-description strings that don't explain the
actual reason, the same standard applied to other permission-usage
strings (see `app-store-review-guidelines`).

### Rule 3

Agents MUST write `localizedReason` as a short, specific phrase
describing the action being authorized (e.g. "Unlock your account",
"Confirm this payment"), not a restatement of "Authenticate" or the app's
name — the system prompt template already supplies "[App Name] would
like to authenticate you"-style framing; a redundant or vague
`localizedReason` leaves the user unsure what they're approving.

### Rule 4

Agents MUST NOT include markup, trailing punctuation inconsistent with a
short phrase, or multi-sentence explanations in `localizedReason` — the
system prompt has limited layout space and truncates or wraps awkwardly
past roughly one short sentence.

## Compliant Example

```xml
<!-- Info.plist -->
<key>NSFaceIDUsageDescription</key>
<string>Use Face ID to quickly and securely unlock your saved passwords.</string>
```
```swift
try await context.evaluatePolicy(
    .deviceOwnerAuthentication,
    localizedReason: "Unlock your saved passwords"
)
```
Both strings are specific to the actual feature, and neither restates generic "authenticate" language. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
// Info.plist has no NSFaceIDUsageDescription entry at all.
try await context.evaluatePolicy(
    .deviceOwnerAuthentication,
    localizedReason: "Authenticate"
)
```
Missing `NSFaceIDUsageDescription` crashes the app on a Face ID device the first time this line runs; `localizedReason` merely restates "authenticate" without saying what's being authorized. (Rules 1, 3)

## Dependencies

None.

## References

-   [Apple Developer — NSFaceIDUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsfaceidusagedescription)
-   [Apple Developer — LAContext](https://developer.apple.com/documentation/localauthentication/lacontext)
