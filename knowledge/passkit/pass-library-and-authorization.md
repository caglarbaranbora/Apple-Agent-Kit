# Pass Library and Authorization

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.passkit.pass-library-and-authorization
artifact_type: knowledge
title: Pass Library and Authorization
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines querying the user's Wallet pass library with PKPassLibrary -- isPassLibraryAvailable(), containsPass(_:), passes()/passes(of:), and adding passes already in hand with addPasses(_:withCompletionHandler:) -- and why PKPassLibrary has no EventKit-style general read/write permission gate.
domain: PassKit
tags:
  - passkit
  - pkpasslibrary
  - wallet
  - pass-query
  - availability
references:
  - https://developer.apple.com/documentation/passkit/pkpasslibrary
  - https://developer.apple.com/documentation/passkit/pkpasslibrary/ispasslibraryavailable()
  - https://developer.apple.com/documentation/passkit/pkpasslibrary/containspass(_:)
  - https://developer.apple.com/documentation/passkit/pkpasslibrary/passes()
  - https://developer.apple.com/documentation/passkit/pkpasslibrary/passes(of:)
  - https://developer.apple.com/documentation/passkit/pkpasstype
  - https://developer.apple.com/documentation/passkit/pkpasslibrary/addpasses(_:withcompletionhandler:)
  - https://developer.apple.com/documentation/passkit/pkpasslibraryaddpassesstatus
depends_on: []
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent queries and adds to the user's Wallet pass library through `PKPassLibrary`: confirming the library is usable at all, checking whether a specific pass is already present, listing the passes the app can see, and adding one or more `PKPass` objects the app already holds — as distinct from presenting the add-to-Wallet confirmation UI (`adding-passes-ui`) or the `.pkpass`/`pass.json` structure of the passes themselves (`pass-content-and-required-fields`).

## Scope

### Included

-   Calling `PKPassLibrary.isPassLibraryAvailable()` before any other library call
-   Checking presence with `containsPass(_:)`, which works even without read/write entitlement for that pass type
-   Listing accessible passes with `passes()` and filtering by `PKPassType` with `passes(of:)`
-   Adding one or more already-held `PKPass` objects with `addPasses(_:withCompletionHandler:)` (or its `async` form), and branching on `PKPassLibraryAddPassesStatus`
-   Why PKPassLibrary access to an app's own pass-type-identifier-scoped passes has no general runtime-permission gate comparable to `EKAuthorizationStatus`

### Excluded

-   Presenting `PKAddPassesViewController`/`PKAddPassButton` as UI, and the check specific to that flow, `PKAddPassesViewController.canAddPasses()` — see `adding-passes-ui`
-   `.pkpass`/`pass.json` field structure and constructing/inspecting a `PKPass` with `PKPass(data:)` — see `pass-content-and-required-fields`
-   `webServiceURL`/`authenticationToken` and server-driven pass updates — see `pass-updates-and-push-registration`
-   `PKAddSecureElementPassViewController`, NFC/secure-element passes, and `PKPassPersonalization` — a distinct, more specialized subsystem, not covered by this domain's v1

## Rules

### Rule 1

Agents MUST call `PKPassLibrary.isPassLibraryAvailable()` before any other `PKPassLibrary` call, and MUST NOT assume the library is usable just because the class exists. Per Apple's documentation, "This method exists because the pass library may be unavailable even if the `PKPassLibrary` class exists" — the class is present on every platform PassKit ships on, but the underlying Wallet library is not guaranteed to be.

### Rule 2

Agents checking whether a specific pass is already in the library MUST use `containsPass(_:)` rather than scanning `passes()`, because it works even when the app cannot read that pass's contents. Per Apple's documentation, "This method lets you determine that the pass library contains a pass even though your app can't read or modify the pass. For example, an email client doesn't have entitlements to read or write any passes from the library." Agents SHOULD use this to drive UI state (e.g., "Add to Wallet" vs. "Already in Wallet") without needing broader access.

### Rule 3

Agents listing passes MUST call `passes()` for everything the app can see and `passes(of:)` with a `PKPassType` (`.barcode` for ordinary Wallet passes, `.payment`, `.secureElement`, or `.any`) when filtering by type, and MUST NOT assume either call returns every pass on the device. Per Apple's documentation, `passes()` "Returns the passes in the user's pass library that the app can access" — visibility is scoped to the passes whose pass type identifiers belong to the calling app's entitlements.

### Rule 4

Agents adding passes the app already holds as `PKPass` objects MUST call `addPasses(_:withCompletionHandler:)` (or `addPasses(_:) async -> PKPassLibraryAddPassesStatus`) and branch on the resulting `PKPassLibraryAddPassesStatus`, reserving `PKAddPassesViewController` for the case where the pass(es) must be visually reviewed first. Per Apple's documentation, "Use this method whenever the user initiates an action that generates a single pass (like purchasing a concert ticket) or multiple passes... The user receives a prompt to confirm the overall action or to review the passes individually. If you want to force the user to review individual passes visually before adding them, use an instance of [`PKAddPassesViewController`]."

### Rule 5

Agents MUST NOT model PassKit's pass-library access as an EventKit-style permission state machine with a `.notDetermined`/`.denied` gate the app requests past. This is reasoned framework behavior rather than a literal single-quote citation: the documented "Accessing passes" and "Adding passes" API surface (Rules 1-4) contains no general authorization-request call comparable to `requestFullAccessToEvents(completion:)`; the only documented `authorizationStatus(for:)`/`requestAuthorization(for:completion:)` pair on `PKPassLibrary` is scoped narrowly to a single `PKPassLibrary.Capability` case, `.backgroundAddPasses`, not to reading or adding passes in general.

## Compliant Example

```swift
import PassKit

func isPassAlreadySaved(_ pass: PKPass, library: PKPassLibrary) -> Bool {
    guard PKPassLibrary.isPassLibraryAvailable() else { return false } // Rule 1
    return library.containsPass(pass) // Rule 2
}

func savedBarcodePasses(library: PKPassLibrary) -> [PKPass] {
    library.passes(of: .barcode) // Rule 3
}

func addPurchasedPass(_ pass: PKPass, library: PKPassLibrary) async -> Bool {
    let status = await library.addPasses([pass]) // Rule 4
    return status == .success
}
```

## Non-Compliant Example

```swift
import PassKit

func addPurchasedPass(_ pass: PKPass, library: PKPassLibrary) {
    // Never checks isPassLibraryAvailable() -- violates Rule 1.
    // Reads library.passes() and filters manually instead of containsPass(_:)/passes(of:),
    // assuming it enumerates every pass on the device -- violates Rule 2 and Rule 3.
    if !library.passes().contains(where: { $0.serialNumber == pass.serialNumber }) {
        library.addPasses([pass], withCompletionHandler: nil) // ignores the status -- violates Rule 4
    }
}
```
Never confirms the library is available (Rule 1), reimplements presence-checking instead of `containsPass(_:)` and treats `passes()` as exhaustive (Rule 2, Rule 3), and discards the `PKPassLibraryAddPassesStatus` result entirely (Rule 4).

## Dependencies

None within this domain — this is the foundational contract every other PassKit Wallet Knowledge Contract in this domain assumes the app already knows how to query and add to the pass library.

## References

-   [Apple Developer — PKPassLibrary](https://developer.apple.com/documentation/passkit/pkpasslibrary)
-   [Apple Developer — isPassLibraryAvailable()](https://developer.apple.com/documentation/passkit/pkpasslibrary/ispasslibraryavailable())
-   [Apple Developer — containsPass(_:)](https://developer.apple.com/documentation/passkit/pkpasslibrary/containspass(_:))
-   [Apple Developer — passes()](https://developer.apple.com/documentation/passkit/pkpasslibrary/passes())
-   [Apple Developer — passes(of:)](https://developer.apple.com/documentation/passkit/pkpasslibrary/passes(of:))
-   [Apple Developer — PKPassType](https://developer.apple.com/documentation/passkit/pkpasstype)
-   [Apple Developer — addPasses(_:withCompletionHandler:)](https://developer.apple.com/documentation/passkit/pkpasslibrary/addpasses(_:withcompletionhandler:))
-   [Apple Developer — PKPassLibraryAddPassesStatus](https://developer.apple.com/documentation/passkit/pkpasslibraryaddpassesstatus)
