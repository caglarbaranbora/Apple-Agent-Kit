# Image Requests

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.photos.image-requests
artifact_type: knowledge
title: Image Requests
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines turning a fetched PHAsset into an image -- the result handler's multi-callback contract, when a synchronous request is legal, the iCloud assets the default options silently drop, and caching for list surfaces.
domain: Photos
tags:
  - photos
  - phimagemanager
  - phimagerequestoptions
  - icloud
  - thumbnails
references:
  - https://developer.apple.com/documentation/photos/phimagemanager/requestimage(for:targetsize:contentmode:options:resulthandler:)
  - https://developer.apple.com/documentation/photos/phimagerequestoptions/issynchronous
  - https://developer.apple.com/documentation/photos/phimagerequestoptions/isnetworkaccessallowed
  - https://developer.apple.com/documentation/photos/phimagerequestoptions/deliverymode
  - https://developer.apple.com/documentation/photos/phcachingimagemanager
depends_on:
  - knowledge.photos.asset-fetching
related:
  - knowledge.photos.picker-and-selection-results
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent turns a `PHAsset` into a displayable image: reading a result handler that Photos may call more than once, choosing synchronous delivery only where it is legal, deciding what happens to assets that live in iCloud, and preparing images ahead of a scrolling surface.

## Scope

### Included

-   `PHImageManager.requestImage(...)` and its multi-callback result handler
-   `PHImageRequestOptions.isSynchronous` and the threading rule attached to it
-   `PHImageRequestOptions.isNetworkAccessAllowed`, its default, and the iCloud case it hides
-   `PHCachingImageManager` for list and grid surfaces, and matching its parameters

### Excluded

-   Obtaining the `PHAsset` to request an image for — see `asset-fetching`
-   Obtaining access at all — see `authorization-and-access-levels`
-   Loading a picker selection, which uses `NSItemProvider`/`Transferable` and not this manager — see `picker-and-selection-results` Rule 4
-   Video playback and `AVAsset` export from an asset, out of this domain's v1 scope
-   Photo and video *editing* (`PHContentEditingInput`/`PHContentEditingOutput`), out of this domain's v1 scope

## Rules

### Rule 1

Agents MUST treat an asynchronous result handler as callable more than once, and MUST NOT treat the first image as final. Per Apple's documentation, "For an asynchronous request, Photos may call your result handler block more than once. Photos first calls the block to provide a low-quality image suitable for displaying temporarily while it prepares a high-quality image. (If low-quality image data is immediately available, the first call may occur before the method returns.) When the high-quality image is ready, Photos calls your result handler again to provide it." Apple names the flag that tells them apart: "The `PHImageResultIsDegradedKey` key in the result handler's `info` parameter indicates when Photos is providing a temporary low-quality image." Code that resumes a continuation or clears a loading state on the first call ships the placeholder as the final image.

### Rule 2

Agents MUST NOT set `isSynchronous` to `true` on the main thread. Per Apple's documentation, if `true` the request "blocks the calling thread until image data is ready or an error occurs," and Apple's note is unqualified: "Perform synchronous requests from a background thread only." The trade it buys is the one exception to Rule 1 — "Photos calls your result handler block exactly once" — so a synchronous request is the only shape where a single callback may be assumed.

### Rule 3

Agents MUST decide `isNetworkAccessAllowed` deliberately, because its default silently drops assets stored only in iCloud. Per Apple's documentation, "If `true`, and the requested image is not stored on the local device, Photos downloads the image from iCloud... If `false` (the default), and the image is not on the local device, the `PHImageResultIsInCloudKey` value in the result handler's `info` dictionary indicates that the image is not available unless you enable network access." An agent that keeps the default MUST read `PHImageResultIsInCloudKey` and show the user why nothing appeared; an agent that enables it SHOULD supply a `progressHandler`, which Apple documents as how "To be notified of the download's progress."

### Rule 4

Agents populating a list or grid MUST use a `PHCachingImageManager` and prime it, rather than calling `PHImageManager.default()` per cell. Per Apple's documentation, "For quick performance when you are working with many assets, a caching image manager can prepare asset images in the background in order to eliminate delays when you later request individual images. For example, use a caching image manager when you want to populate a collection view or similar UI with thumbnails of photo or video assets." Apple requires the two calls to agree: prime with `startCachingImages(for:targetSize:contentMode:options:)` using "the target size, content mode, and options you plan to use when later requesting images," then request with "the same parameters you used when preparing that asset." A request whose parameters differ misses the cache entirely and re-does the work the priming was supposed to save.

### Rule 5

Agents MUST size a request to what the UI displays rather than passing the asset's full dimensions for a thumbnail. Per Apple's documentation, "Photos loads or generates an image of the asset at, or near, the size you specify. To serve your request more quickly, Photos may provide an image that is slightly larger than the target size — either because such an image is already cached or because it can be generated more efficiently." `targetSize` is therefore a hint that Photos optimizes against, and a grid that asks for full-resolution images forfeits that optimization for every cell.

## Compliant Example

```swift
import Photos
import UIKit

final class Thumbnails {
    private let manager = PHCachingImageManager()          // Rule 4
    private let size = CGSize(width: 200, height: 200)     // Rule 5: the displayed size
    private let opts: PHImageRequestOptions = {
        let o = PHImageRequestOptions()
        o.isNetworkAccessAllowed = true                    // Rule 3: iCloud assets included
        o.deliveryMode = .opportunistic                    // Rule 2: isSynchronous left false
        return o
    }()

    func prime(_ assets: [PHAsset]) {
        manager.startCachingImages(for: assets, targetSize: size,
                                   contentMode: .aspectFill, options: opts)
    }

    func thumbnail(for asset: PHAsset, show: @escaping (UIImage) -> Void) {
        // Rule 4: identical parameters to prime(_:), or the cache is missed.
        manager.requestImage(for: asset, targetSize: size,
                             contentMode: .aspectFill, options: opts) { image, info in
            // Rule 1: this runs again at full quality; do not tear down on the first call.
            if let image { show(image) }
        }
    }
}
```

## Non-Compliant Example

```swift
import Photos
import UIKit

@MainActor
func thumbnails(for assets: [PHAsset]) -> [UIImage] {
    var images: [UIImage] = []
    let options = PHImageRequestOptions()
    options.isSynchronous = true                     // on the main thread -- violates Rule 2
    for asset in assets {                            // shared manager per cell: violates Rule 4
        // isNetworkAccessAllowed left false and PHImageResultIsInCloudKey never read, so
        // every iCloud-only asset is dropped in silence -- violates Rule 3.
        PHImageManager.default().requestImage(
            for: asset,
            targetSize: CGSize(width: asset.pixelWidth, height: asset.pixelHeight),
            contentMode: .aspectFit,                 // full resolution for a grid: violates Rule 5
            options: options) { image, _ in
                if let image { images.append(image) }
            }
    }
    return images
}
```

Blocks the main thread on a synchronous request (Rule 2), skips every iCloud-only asset without noticing (Rule 3), requests each thumbnail through the shared manager with no priming (Rule 4), and asks for full-resolution images to fill a grid (Rule 5).

## Dependencies

-   `knowledge.photos.asset-fetching` — a request needs a `PHAsset`, and that contract owns how one is obtained and held; the caching rule here assumes the fetch result it primes from came from there.

## References
-   [Apple Developer — requestImage(for:targetSize:contentMode:options:resultHandler:)](https://developer.apple.com/documentation/photos/phimagemanager/requestimage(for:targetsize:contentmode:options:resulthandler:))
-   [Apple Developer — PHImageRequestOptions.isSynchronous](https://developer.apple.com/documentation/photos/phimagerequestoptions/issynchronous)
-   [Apple Developer — PHImageRequestOptions.isNetworkAccessAllowed](https://developer.apple.com/documentation/photos/phimagerequestoptions/isnetworkaccessallowed)
-   [Apple Developer — PHImageRequestOptions.deliveryMode](https://developer.apple.com/documentation/photos/phimagerequestoptions/deliverymode)
-   [Apple Developer — PHCachingImageManager](https://developer.apple.com/documentation/photos/phcachingimagemanager)
