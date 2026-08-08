# Limited Library

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.photos.limited-library
artifact_type: knowledge
title: Limited Library
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines behaving correctly when the user grants limited photo-library access -- what stops working, suppressing the automatic selection alert, presenting the selection picker deliberately, and observing the change it produces.
domain: Photos
tags:
  - photos
  - limited-library
  - phauthorizationstatus
  - change-observer
  - info-plist
references:
  - https://developer.apple.com/documentation/photos/phauthorizationstatus/limited
  - https://developer.apple.com/documentation/photos/phphotolibrary/presentlimitedlibrarypicker(from:)
  - https://developer.apple.com/documentation/photos/phphotolibrarychangeobserver
  - https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app
depends_on:
  - knowledge.photos.authorization-and-access-levels
related:
  - knowledge.uikit.swiftui-view-representable
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent builds a feature that keeps working when the user shares only part of their library: adapting the UI to what limited access removes, taking control of the selection prompt instead of letting the system fire it, and reacting when the selection changes.

## Scope

### Included

-   What `PHAuthorizationStatus.limited` actually removes from the library API
-   The `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` Information Property List key
-   `presentLimitedLibraryPicker(from:)`, when it is a no-op, and the affordance that calls it
-   `PHPhotoLibraryChangeObserver` as the signal that the selection changed
-   Assets the app creates being added to the selection automatically

### Excluded

-   Requesting access and reading the status in the first place — see `authorization-and-access-levels`, which owns the API that reports `limited` at all
-   Avoiding this whole state by using a picker instead — see `picker-and-selection-results` Rule 1
-   Fetch and image-request mechanics that are unchanged by limited access — see `asset-fetching-and-image-requests`
-   How the `UIViewControllerRepresentable` wrapper Rule 5 requires is written — see `knowledge.uikit.swiftui-view-representable` Rule 5; this contract states none of those mechanics

## Rules

### Rule 1

Agents MUST treat `limited` as its own state with its own UI, and MUST NOT write code paths that assume the whole library is reachable. Per Apple's documentation the status means "The user authorized this app for limited photo library access," and while "The PhotoKit APIs largely function the same," Apple names the exception that breaks feature design: "You can't create or fetch user albums. If your app requires this functionality, you'll need to update its behavior and user interface appropriately when your app's authorization status is limited." An album browser built without this branch shows an empty screen rather than an explanation.

### Rule 2

Agents MUST add `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` with a Boolean value of `true` to the app's Information Property List, and MUST NOT ship the system's default prompt. Per Apple's documentation, "By default, the system automatically prompts the user to update their limited-library selection once per app life cycle. This automatic presentation isn't the preferred user experience for most apps. Instead, apps need to suppress the automatic prompt and present it programmatically." Apple states the key and value directly: "Add the `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` key with a Boolean value of `true` to your app's `Info.plist` file to prevent the system from automatically presenting the limited library selection prompt."

### Rule 3

Agents suppressing the alert under Rule 2 MUST add a user-facing affordance that calls `presentLimitedLibraryPicker(from:)`, and MUST gate it on the status being `limited`. Per Apple's documentation, "To present the limited-library picker programmatically, add an affordance in your user interface so the user can update their limited-library selection," and calling it in any other state is silent: "If the user hasn't enabled limited library access mode for your app, calling this method does nothing." A button that does nothing for fully-authorized users is a defect, so the affordance is shown conditionally rather than always.

### Rule 4

Agents MUST react to a selection change through a registered `PHPhotoLibraryChangeObserver` rather than re-fetching in the picker's completion. Per Apple's documentation, "Any changes the user applies to the limited library selection trigger a `PHPhotoLibraryChangeObserver` update," and the observer "notifies you of changes that occur in the photo library, regardless of whether those changes are made by your app, by a user in the Photos app, or by another app that uses the Photos framework." One observer therefore covers the selection change *and* every other source of change; a completion-handler refetch covers only the first.

### Rule 5

Agents presenting this picker from SwiftUI MUST obtain a `UIViewController` to pass it, and MUST NOT expect a SwiftUI-native equivalent. The method is declared `func presentLimitedLibraryPicker(from controller: UIViewController)` and is documented for iOS, iPadOS, Mac Catalyst, and visionOS only; PhotosUI's SwiftUI surface covers selecting assets (`PhotosPicker`) and not managing the limited-library grant, so this call has no `View`-based counterpart. How the controller is bridged into a SwiftUI hierarchy is `knowledge.uikit.swiftui-view-representable` Rule 5, which this contract does not restate. This is the inverse of `picker-and-selection-results` Rule 2, which forbids the bridge because a native picker exists — the two rules cover different symbols and disagree deliberately.

### Rule 6

Agents MUST NOT prompt the user to re-select an asset the app just saved. Per Apple's documentation, "The system automatically adds assets that your app creates with a `PHAssetCreationRequest` to the user's limited library selection." A save-then-read flow therefore works under limited access without any selection round trip, and adding one is a worse experience than doing nothing.

## Compliant Example

```swift
import Photos
import UIKit

// Rule 2: Info.plist carries PHPhotoLibraryPreventAutomaticLimitedAccessAlert = true.
final class LibraryModel: NSObject, PHPhotoLibraryChangeObserver {
    private var assets = PHFetchResult<PHAsset>()

    var isLimited: Bool {                                   // Rule 1: a real branch
        PHPhotoLibrary.authorizationStatus(for: .readWrite) == .limited
    }
    // Rule 3: shown only when isLimited, so it is never a dead button.
    func manageSelection(from controller: UIViewController) {
        PHPhotoLibrary.shared().presentLimitedLibraryPicker(from: controller)
    }
    func start() {
        PHPhotoLibrary.shared().register(self)              // Rule 4: one observer
    }
    func photoLibraryDidChange(_ change: PHChange) {        // covers the new selection
        guard let details = change.changeDetails(for: assets) else { return }
        assets = details.fetchResultAfterChanges
    }
}
```

## Non-Compliant Example

```swift
import Photos

func showAlbums() {
    // Assumes user albums exist under limited access -- violates Rule 1.
    let albums = PHAssetCollection.fetchAssetCollections(with: .album,
                                                        subtype: .any, options: nil)
    render(albums)   // silently empty when the status is .limited
}
func addMorePhotos(from controller: UIViewController) {
    // Called unconditionally: a no-op for fully-authorized users -- violates Rule 3.
    PHPhotoLibrary.shared().presentLimitedLibraryPicker(from: controller)
    // Refetches instead of observing, so changes from the Photos app are missed
    // -- violates Rule 4. No prevent-alert key is set, so the system also fires
    // its own prompt once per launch -- violates Rule 2.
    reloadEverything()
}
```

Renders an album list that limited access cannot populate (Rule 1), leaves the automatic system prompt in place (Rule 2), offers a selection button that does nothing for most users (Rule 3), and refreshes by refetching rather than by observing the library (Rule 4).

## Dependencies

-   `knowledge.photos.authorization-and-access-levels` — that contract's Rule 3 obtains a status that can report `limited` at all; every rule here assumes that check was made with the `(for:)` API rather than the unlabelled one.

## References
-   [Apple Developer — PHAuthorizationStatus.limited](https://developer.apple.com/documentation/photos/phauthorizationstatus/limited)
-   [Apple Developer — presentLimitedLibraryPicker(from:)](https://developer.apple.com/documentation/photos/phphotolibrary/presentlimitedlibrarypicker(from:))
-   [Apple Developer — PHPhotoLibraryChangeObserver](https://developer.apple.com/documentation/photos/phphotolibrarychangeobserver)
-   [Apple Developer — Delivering an enhanced privacy experience in your Photos app](https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app)
