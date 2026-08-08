# Authorization and Access Levels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.photos.authorization-and-access-levels
artifact_type: knowledge
title: Authorization and Access Levels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requesting photo-library access when a picker is not enough -- choosing between the add-only and read/write levels, declaring the Information Property List key each one requires, and using the status API that reports limited access truthfully.
domain: Photos
tags:
  - photos
  - authorization
  - phaccesslevel
  - info-plist
  - usage-description
references:
  - https://developer.apple.com/documentation/photos/phphotolibrary/requestauthorization(for:handler:)
  - https://developer.apple.com/documentation/photos/phphotolibrary/authorizationstatus(for:)
  - https://developer.apple.com/documentation/photos/phaccesslevel
  - https://developer.apple.com/documentation/photos/phauthorizationstatus
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsphotolibraryusagedescription
  - https://developer.apple.com/documentation/bundleresources/information-property-list/nsphotolibraryaddusagedescription
  - https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app
depends_on: []
related:
  - knowledge.photos.picker-and-selection-results
  - knowledge.app-store-review-guidelines.permission-usage-strings
  - knowledge.human-interface-guidelines.privacy
  - knowledge.privacy.collected-data-types-declaration
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent requests access to the photo library once a picker is not enough: picking the narrowest access level the feature needs, declaring the Information Property List key that level requires, calling the request at the right moment, and reading back a status that does not lie about limited access.

## Scope

### Included

-   `PHAccessLevel.addOnly` versus `.readWrite`, and choosing the narrower one
-   `NSPhotoLibraryAddUsageDescription` and `NSPhotoLibraryUsageDescription`, and which level each serves
-   `requestAuthorization(for:handler:)` / `authorizationStatus(for:)` and why the unlabelled variants are wrong
-   Handling every `PHAuthorizationStatus` case, and re-reading status after a Settings change
-   When in the app's life the request is made

### Excluded

-   Choosing a picker instead, which needs none of this — see `picker-and-selection-results` Rule 1, which owns that decision
-   What `.limited` changes about the library once granted — see `limited-library`
-   How the usage-description string is *written* — see Rule 6
-   Declaring photo data in `PrivacyInfo.xcprivacy` — see `knowledge.privacy.collected-data-types-declaration`; this contract declares no manifest rules
-   Whether to show a pre-permission explanation screen and what it says — see `knowledge.human-interface-guidelines.privacy`

## Rules

### Rule 1

Agents MUST request the narrowest access level the feature needs, and MUST use `.addOnly` when the app only writes to the library. Per Apple's documentation, `.addOnly` is "A value that indicates the app may only add to the user's photo library" and `.readWrite` is "A value that indicates the app can read from and write to the user's photo library"; Apple's instruction is explicit — "Request authorization only for the level of access required." A save-only feature that requests `.readWrite` asks the user for read access it never uses.

### Rule 2

Agents MUST add the Information Property List key matching the requested level before any call that touches the library, and MUST NOT treat its absence as a denied-permission case. Per Apple's documentation, "If your app only adds to the library, use the `NSPhotoLibraryAddUsageDescription` key. For all other cases, use `NSPhotoLibraryUsageDescription`," and "Attempting to access the Photos library without a valid usage description causes your app to crash." Apple repeats this for fetches: "Apps linked on or after iOS 10.0 will crash if this key is not present."

### Rule 3

Agents MUST call `authorizationStatus(for:)` and `requestAuthorization(for:handler:)`, and MUST NOT call the unlabelled `authorizationStatus()` or `requestAuthorization(_:)`. Per Apple's documentation, "The `authorizationStatus()` and `requestAuthorization(_:)` methods aren't compatible with the limited library and return `authorized` when the user authorizes your app for limited access only. To determine whether the user has authorized your app for limited access, instead use `authorizationStatus(for:)` and `requestAuthorization(for:handler:)`." The old call does not fail — it reports a permission the app does not have, so every downstream assumption about a full library is silently wrong.

### Rule 4

Agents MUST make the request in response to a user action rather than at launch. Per Apple's documentation, "Avoid making PhotoKit calls when your app first launches, to avoid interrupting its startup or onboarding process. Instead, make these calls in response to direct user action. Timing the authorization prompt to coincide with a user action provides greater context to the user about why your app is requesting access." A first-run prompt is also what the app gets by accident: "The first time your app performs an operation that requires authorization, the system automatically and asynchronously prompts the user for it" — so an unguarded PhotoKit call at launch *is* a launch-time prompt.

### Rule 5

Agents MUST handle all five `PHAuthorizationStatus` cases — `notDetermined`, `restricted`, `denied`, `authorized`, `limited` — with `@unknown default`, and MUST re-read the status when the app returns to the foreground rather than caching the first answer. Per Apple's documentation, "After the user sets the app's authorization status, the system remembers their choice and won't prompt them again. However, the user can change this choice at any time using the Settings app. Prepare your app to respond appropriately when a user changes your app's access." Treating `limited` as equivalent to `authorized` is the specific failure Rule 3 also guards against.

### Rule 6

This contract defines *which* key each access level requires and *when* it must exist. It defines no rule about how that string is written: the accuracy and specificity every usage-description string must meet is `knowledge.app-store-review-guidelines.permission-usage-strings`, and agents MUST route the wording question there rather than inventing a string here. That Contract's own examples may name photo keys illustratively; an example is not ownership, and the `.addOnly`/`.readWrite` split above is this domain's.

## Compliant Example

```swift
import Photos

// Rule 1: a save-only feature asks for add-only access, nothing wider.
// Rule 2: Info.plist carries NSPhotoLibraryAddUsageDescription before this runs.
@MainActor
func requestSaveAccess() async -> Bool {
    // Rule 3: the (for:) variants, which report .limited truthfully.
    var status = PHPhotoLibrary.authorizationStatus(for: .addOnly)
    if status == .notDetermined {
        // Rule 4: called from a "Save to Photos" tap, never from launch.
        status = await PHPhotoLibrary.requestAuthorization(for: .addOnly)
    }
    switch status {                                  // Rule 5: every case handled
    case .authorized, .limited: return true
    case .denied, .restricted: return false          // offer a route to Settings
    case .notDetermined: return false
    @unknown default: return false
    }
}
```

## Non-Compliant Example

```swift
import Photos

func setUp() {
    // Requests read/write for a save-only feature -- violates Rule 1,
    // and runs at launch rather than on a user action -- violates Rule 4.
    PHPhotoLibrary.requestAuthorization { status in   // unlabelled -- violates Rule 3
        // .limited arrives here as .authorized, so this branch is a lie.
        if status == .authorized {
            self.loadEntireLibrary()                  // also violates Rule 5
        }
    }
}
```

Asks for more access than the feature uses (Rule 1), at launch instead of at the user's request (Rule 4), through the API that reports limited access as full (Rule 3), and branches on two statuses out of five with no path for a later Settings change (Rule 5). With no `NSPhotoLibraryUsageDescription` in the Information Property List, the first call crashes rather than being denied (Rule 2).

## Dependencies

This contract has no dependencies. It is the entry point for every part of this domain that a picker cannot serve; `picker-and-selection-results` Rule 1 owns the prior decision of whether to come here at all.

## References
-   [Apple Developer — requestAuthorization(for:handler:)](https://developer.apple.com/documentation/photos/phphotolibrary/requestauthorization(for:handler:))
-   [Apple Developer — authorizationStatus(for:)](https://developer.apple.com/documentation/photos/phphotolibrary/authorizationstatus(for:))
-   [Apple Developer — PHAccessLevel](https://developer.apple.com/documentation/photos/phaccesslevel)
-   [Apple Developer — PHAuthorizationStatus](https://developer.apple.com/documentation/photos/phauthorizationstatus)
-   [Apple Developer — NSPhotoLibraryUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsphotolibraryusagedescription)
-   [Apple Developer — NSPhotoLibraryAddUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nsphotolibraryaddusagedescription)
-   [Apple Developer — Delivering an enhanced privacy experience in your Photos app](https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app)
