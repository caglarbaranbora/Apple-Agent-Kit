# Saving to the Library

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.photos.saving-to-the-library
artifact_type: knowledge
title: Saving to the Library
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines writing to the photo library -- running every change request inside a single change block, choosing the creation request that preserves metadata, handling a completion that reports failure on an arbitrary queue, and referencing the created asset afterwards.
domain: Photos
tags:
  - photos
  - performchanges
  - phassetchangerequest
  - phassetcreationrequest
  - metadata
references:
  - https://developer.apple.com/documentation/photos/phphotolibrary/performchanges(_:completionhandler:)
  - https://developer.apple.com/documentation/photos/phassetchangerequest
  - https://developer.apple.com/documentation/photos/phassetchangerequest/creationrequestforasset(from:)
  - https://developer.apple.com/documentation/photos/phassetchangerequest/creationrequestforassetfromimage(atfileurl:)
  - https://developer.apple.com/documentation/photos/phassetchangerequest/placeholderforcreatedasset
  - https://developer.apple.com/documentation/photos/phassetcreationrequest
depends_on:
  - knowledge.photos.authorization-and-access-levels
related:
  - knowledge.photos.limited-library
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent writes to the photo library: submitting every change through a change block, batching changes so the user is asked once, picking the creation request that keeps the file's metadata, and treating the completion as a result that can fail.

## Scope

### Included

-   `performChanges(_:completionHandler:)` as the only place a change request may exist
-   Batching several changes into one block, and what a second block costs the user
-   `PHAssetChangeRequest` versus `PHAssetCreationRequest`, and the metadata each preserves
-   `placeholderForCreatedAsset` for referencing a newly created asset
-   Handling the completion's `success`/`error` on the queue Photos calls it from

### Excluded

-   Obtaining write access and choosing `.addOnly` over `.readWrite` — see `authorization-and-access-levels` Rule 1, which owns that choice; this contract states no access-level rules
-   That a created asset joins the user's limited selection automatically — see `limited-library` Rule 6
-   Reading the library back afterwards — see `asset-fetching` and `image-requests`
-   Photo and video *editing* through `PHContentEditingInput`/`PHContentEditingOutput`, out of this domain's v1 scope

## Rules

### Rule 1

Agents MUST create and use every change request inside a change block and MUST NOT hold one outside. Per Apple's documentation, "To create a new asset from data resources, first start a change block using the shared `PHPhotoLibrary` method `performChanges(_:completionHandler:)` or `performChangesAndWait(_:)`. Then, within the change block: ... create a new asset creation request with the `forAsset()` method," and the failure is not graceful: "If you instantiate or use this class outside a photo library change block, Photos throws an exception."

### Rule 2

Agents saving more than one item MUST combine the writes into a single change block. Per Apple's documentation, "For each call to this method, iOS shows an alert asking the user for permission to edit the contents of the photo library. If your app needs to submit several changes at once, combine them into a single change block." A loop that calls `performChanges` once per photo therefore asks the user once per photo, which reads as a malfunction rather than as a permission flow.

### Rule 3

Agents MUST NOT create an asset from a `UIImage` when the source is a file whose metadata matters. Per Apple's documentation, "A `UIImage` object does not contain all metadata associated with the image file it was originally loaded from (for example, Exif tags such as geographic location, camera model, and exposure parameters). To ensure such metadata is saved in the Photos library, instead use the `creationRequestForAssetFromImage(atFileURL:)` method or the `PHAssetCreationRequest` class." `PHAssetCreationRequest` is the resource-level path — Apple describes it as working "in terms of the raw data resources that together form an asset" — and `creationRequestForAsset(from:)` is correct only for an image the app itself rendered and that has no original file behind it.

### Rule 4

Agents MUST read both `success` and `error` in the completion handler, and MUST dispatch any UI work to the main queue. Per Apple's documentation the completion reports "`success`: `true` if Photos successfully applied the changes requested in the block; otherwise, `false`" together with "an `NSError` object describing the error," and "Photos executes both the change block and the completion handler block on an arbitrary serial queue. To update your app's UI as a result of a change, dispatch that work to the main queue." A completion handler that shows a success message without checking `success` reports a save that may not have happened, from the wrong thread.

### Rule 5

Agents needing the created asset afterwards MUST capture `placeholderForCreatedAsset` inside the block rather than refetching the library to guess which asset is new. Per Apple's documentation, "To reference the newly created asset later in the same change block or after the change block completes, use the `placeholderForCreatedAsset` property to retrieve a placeholder object." The placeholder carries the identifier the completion can resolve; a "most recent asset" fetch after the fact is a race against every other app writing to the same library.

## Compliant Example

```swift
import Photos

// Rule 1: everything happens inside one change block.
// Rule 2: all URLs are written in that single block, so the user is asked once.
func save(_ urls: [URL]) async throws -> [String] {
    var placeholders: [PHObjectPlaceholder] = []
    try await PHPhotoLibrary.shared().performChanges {
        for url in urls {
            // Rule 3: from the file, so Exif and location survive the save.
            guard let request = PHAssetCreationRequest.creationRequestForAssetFromImage(
                atFileURL: url) else { continue }
            if let placeholder = request.placeholderForCreatedAsset {
                placeholders.append(placeholder)          // Rule 5
            }
        }
    }
    // Rule 4: the async form throws on failure; UI work happens on the main actor.
    return placeholders.map(\.localIdentifier)
}
```

## Non-Compliant Example

```swift
import Photos
import UIKit

func save(_ images: [UIImage], from urls: [URL]) {
    for image in images {
        // One block per image, so one permission alert per image -- violates Rule 2.
        PHPhotoLibrary.shared().performChanges {
            // Loses Exif, location, and camera metadata from the original file
            // -- violates Rule 3.
            PHAssetChangeRequest.creationRequestForAsset(from: image)
        } completionHandler: { _, _ in
            // Ignores success and error, and touches UI off the main queue
            // -- violates Rule 4.
            self.statusLabel.text = "Saved"
        }
    }
    // Guesses at the new asset instead of keeping a placeholder -- violates Rule 5.
    let newest = PHAsset.fetchAssets(with: .image, options: nil).lastObject
    _ = newest
}
```

Asks the user once per image instead of once (Rule 2), drops the original file's metadata by saving a `UIImage` (Rule 3), reports success without reading it and from the wrong queue (Rule 4), and identifies the created asset by refetching rather than by placeholder (Rule 5).

## Dependencies

-   `knowledge.photos.authorization-and-access-levels` — a write requires an access level and the Information Property List key that goes with it; that contract owns both, and this one assumes the grant is already in hand.

## References
-   [Apple Developer — performChanges(_:completionHandler:)](https://developer.apple.com/documentation/photos/phphotolibrary/performchanges(_:completionhandler:))
-   [Apple Developer — PHAssetChangeRequest](https://developer.apple.com/documentation/photos/phassetchangerequest)
-   [Apple Developer — creationRequestForAsset(from:)](https://developer.apple.com/documentation/photos/phassetchangerequest/creationrequestforasset(from:))
-   [Apple Developer — creationRequestForAssetFromImage(atFileURL:)](https://developer.apple.com/documentation/photos/phassetchangerequest/creationrequestforassetfromimage(atfileurl:))
-   [Apple Developer — placeholderForCreatedAsset](https://developer.apple.com/documentation/photos/phassetchangerequest/placeholderforcreatedasset)
-   [Apple Developer — PHAssetCreationRequest](https://developer.apple.com/documentation/photos/phassetcreationrequest)
