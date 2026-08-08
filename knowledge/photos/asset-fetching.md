# Asset Fetching

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.photos.asset-fetching
artifact_type: knowledge
title: Asset Fetching
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines querying the photo library once access is granted -- expressing filtering and ordering as PHFetchOptions, holding a PHFetchResult as the lazily-batched cursor it is, and refreshing it through a change observer rather than refetching.
domain: Photos
tags:
  - photos
  - phasset
  - phfetchoptions
  - phfetchresult
  - change-observer
references:
  - https://developer.apple.com/documentation/photos/phfetchoptions
  - https://developer.apple.com/documentation/photos/phfetchresult
  - https://developer.apple.com/documentation/photos/phasset/fetchassets(with:options:)
  - https://developer.apple.com/documentation/photos/phasset/location
  - https://developer.apple.com/documentation/photos/phassetcollection
  - https://developer.apple.com/documentation/photos/phphotolibrarychangeobserver
depends_on:
  - knowledge.photos.authorization-and-access-levels
related:
  - knowledge.photos.limited-library
  - knowledge.photos.image-requests
  - knowledge.core-location.authorization-and-usage-strings
  - knowledge.privacy.collected-data-types-declaration
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent queries the photo library once access is granted: expressing the query as fetch options rather than as post-filtering, holding the result in the form Photos returns it, and keeping it current as the library changes underneath.

## Scope

### Included

-   `PHFetchOptions` predicates and sort descriptors, and the restricted key set each fetching class supports
-   `PHFetchResult` snapshot and lazy-batching semantics, and why it is not an array
-   Refreshing a fetch result through `PHPhotoLibraryChangeObserver`
-   `PHAsset.location` as a fetched asset's recorded capture place, and the authorization it does not require

### Excluded

-   Obtaining access at all — see `authorization-and-access-levels`; every fetch here requires it
-   The device's *current* location, which is `knowledge.core-location.authorization-and-usage-strings`' domain entirely, and declaring location as a collected data type once a capture place leaves the device, which is `knowledge.privacy.collected-data-types-declaration`'s; Rule 5 below owns only the fact that an asset's recorded place is neither
-   Turning a fetched `PHAsset` into an image — see `image-requests`
-   What limited access removes from a fetch, and the selection-change trigger — see `limited-library` Rules 1 and 4
-   Writing to the library — see `saving-to-the-library`
-   Reading a picker's results, which needs no fetch at all — see `picker-and-selection-results`

## Rules

### Rule 1

Agents MUST express filtering and ordering as a `PHFetchOptions` predicate and sort descriptors, and MUST NOT fetch everything and narrow it in Swift. Per Apple's documentation, "The options you specify control which objects the fetch result includes, how those objects are arranged in the fetch result," and a fetch without them is documented as returning everything: "By default, the returned `PHFetchResult` object contains all assets with the specified type. To retrieve a more specific set of assets, provide a `PHFetchOptions` object containing a filter predicate." Apple also constrains what is expressible — "Photos supports only a restricted set of keys for the `predicate` and `sortDescriptors` properties. The set of available keys depends on which class you're using to fetch assets or collections" — so agents MUST check the supported keys for the class being fetched rather than assuming Core Data semantics.

### Rule 2

Agents MUST hold a `PHFetchResult` and index into it, and MUST NOT copy it into an `Array` to keep the assets. Per Apple's documentation, "Unlike an `NSArray` object, however, a `PHFetchResult` object dynamically loads its contents from the Photos library as needed, providing optimal performance even when handling a large number of results," and "A fetch result caches its contents, keeping a batch of objects around the most recently accessed index. Because objects outside of the batch are no longer cached, accessing these objects results in refetching those objects." Materializing the whole result defeats the batching that makes a large library usable.

### Rule 3

Agents MUST treat a fetch result as a snapshot and refresh it through a registered `PHPhotoLibraryChangeObserver`, and MUST NOT re-run the fetch on a timer or on every appearance. Per Apple's documentation, "After a fetch, the fetch result's `count` value is constant, and all objects in the fetch result keep the same `localIdentifier` value. (To get updated content for a fetch, register a change observer with the shared `PHPhotoLibrary` object.)" One observer covers every source of change — Apple documents it as firing "regardless of whether those changes are made by your app, by a user in the Photos app, or by another app that uses the Photos framework." This contract owns that refresh mechanic; `limited-library` Rule 4 states only that a limited-selection change is one of the events this same observer delivers.

### Rule 4

Agents fetching a collection's contents MUST fetch its members separately rather than expecting the collection object to carry them. Per Apple's documentation, "In the Photos framework, collection objects (including asset collections) do not directly reference their member objects, and there are no other objects that directly reference collection objects. To retrieve the members of an asset collection, fetch them with a `PHAsset` class method such as `fetchAssets(in:options:)`." A `PHAssetCollection` is a handle, not a container, and code that treats it as a list of assets has nothing to iterate.

### Rule 5

Agents MUST read a photo's recorded capture place from `PHAsset.location` and MUST NOT request Core Location authorization in order to obtain it. The property is declared `var location: CLLocation? { get }`, Apple describes it as "The location information for the asset," and notes that "Typically, an asset's location metadata identifies the place where the asset was captured." The `CLLocation` is metadata the library hands back under the grant this contract already depends on, not a fix Core Location produced — `CLLocationManager` authorization governs the device's *current* location and has no part in reading an asset's *recorded* one. A feature that needs only where a photo was taken and prompts for location access is asking the user for data it never uses. The property is optional, so an asset carrying no location metadata MUST be handled as absent rather than force-unwrapped.

## Compliant Example

```swift
import CoreLocation
import Photos

final class RecentPhotos: NSObject, PHPhotoLibraryChangeObserver {
    private(set) var result = PHFetchResult<PHAsset>()   // Rule 2: held, not arrayed

    func load() {
        let options = PHFetchOptions()                   // Rule 1: query, not post-filter
        options.sortDescriptors = [NSSortDescriptor(key: "creationDate", ascending: false)]
        result = PHAsset.fetchAssets(with: .image, options: options)
        PHPhotoLibrary.shared().register(self)           // Rule 3: refresh, never refetch
    }
    func photoLibraryDidChange(_ change: PHChange) {
        guard let details = change.changeDetails(for: result) else { return }
        result = details.fetchResultAfterChanges
    }
    func assets(in album: PHAssetCollection) -> PHFetchResult<PHAsset> {
        PHAsset.fetchAssets(in: album, options: nil)     // Rule 4: members are fetched
    }
    // Rule 5: place ships with the asset -- no manager, no prompt, nil if unrecorded.
    func place(of asset: PHAsset) -> CLLocation? { asset.location }
}
```

## Non-Compliant Example

```swift
import CoreLocation
import Photos

func recentPhotos() -> [PHAsset] {
    // No options, so this fetches the whole library -- violates Rule 1.
    let all = PHAsset.fetchAssets(with: .image, options: nil)
    var assets: [PHAsset] = []
    all.enumerateObjects { asset, _, _ in assets.append(asset) }   // violates Rule 2
    // Filtering and sorting in Swift, over every asset the user owns -- violates Rule 1.
    return assets.filter { $0.creationDate ?? .distantPast > .now.addingTimeInterval(-86_400) }
                 .sorted { ($0.creationDate ?? .distantPast) > ($1.creationDate ?? .distantPast) }
}

func refresh(every seconds: TimeInterval) {
    // Polls instead of observing, so it misses changes and repeats work -- violates Rule 3.
    Timer.scheduledTimer(withTimeInterval: seconds, repeats: true) { _ in _ = recentPhotos() }
}

func showPlace(of asset: PHAsset, on manager: CLLocationManager) {
    // Asks for access the feature never uses -- the place is on the asset already,
    // and the device's current location is a different fact. Violates Rule 5.
    manager.requestWhenInUseAuthorization()
}
```

Fetches the entire library and narrows it in Swift (Rule 1), copies a lazily-batched result into an array (Rule 2), polls on a timer instead of registering for the change notifications Photos already sends (Rule 3), and asks the user for location access to read a place the library already returned (Rule 5).

## Dependencies

-   `knowledge.photos.authorization-and-access-levels` — every fetch here requires granted access, and Apple prompts automatically on the first such call; that contract owns when and how the request is made.

## References
-   [Apple Developer — PHFetchOptions](https://developer.apple.com/documentation/photos/phfetchoptions)
-   [Apple Developer — PHFetchResult](https://developer.apple.com/documentation/photos/phfetchresult)
-   [Apple Developer — fetchAssets(with:options:)](https://developer.apple.com/documentation/photos/phasset/fetchassets(with:options:))
-   [Apple Developer — PHAsset.location](https://developer.apple.com/documentation/photos/phasset/location)
-   [Apple Developer — PHAssetCollection](https://developer.apple.com/documentation/photos/phassetcollection)
-   [Apple Developer — PHPhotoLibraryChangeObserver](https://developer.apple.com/documentation/photos/phphotolibrarychangeobserver)
