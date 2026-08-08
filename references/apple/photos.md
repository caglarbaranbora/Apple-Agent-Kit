# Photos

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.photos
artifact_type: reference
title: Photos
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's PhotoKit and PhotosUI documentation, scoped to this domain's v1.
domain: Photos
last_updated: 2026-08-09
```

## Source

https://developer.apple.com/documentation/bundleresources/information-property-list/nsphotolibraryaddusagedescription
https://developer.apple.com/documentation/bundleresources/information-property-list/nsphotolibraryusagedescription
https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app
https://developer.apple.com/documentation/photos
https://developer.apple.com/documentation/photos/phaccesslevel
https://developer.apple.com/documentation/photos/phasset
https://developer.apple.com/documentation/photos/phasset/fetchassets(in:options:)
https://developer.apple.com/documentation/photos/phasset/fetchassets(with:options:)
https://developer.apple.com/documentation/photos/phassetchangerequest
https://developer.apple.com/documentation/photos/phassetchangerequest/creationrequestforasset(from:)
https://developer.apple.com/documentation/photos/phassetchangerequest/creationrequestforassetfromimage(atfileurl:)
https://developer.apple.com/documentation/photos/phassetchangerequest/placeholderforcreatedasset
https://developer.apple.com/documentation/photos/phassetcollection
https://developer.apple.com/documentation/photos/phassetcreationrequest
https://developer.apple.com/documentation/photos/phauthorizationstatus
https://developer.apple.com/documentation/photos/phauthorizationstatus/limited
https://developer.apple.com/documentation/photos/phcachingimagemanager
https://developer.apple.com/documentation/photos/phchange
https://developer.apple.com/documentation/photos/phfetchoptions
https://developer.apple.com/documentation/photos/phfetchresult
https://developer.apple.com/documentation/photos/phimagemanager
https://developer.apple.com/documentation/photos/phimagemanager/requestimage(for:targetsize:contentmode:options:resulthandler:)
https://developer.apple.com/documentation/photos/phimagerequestoptions
https://developer.apple.com/documentation/photos/phimagerequestoptions/deliverymode
https://developer.apple.com/documentation/photos/phimagerequestoptions/isnetworkaccessallowed
https://developer.apple.com/documentation/photos/phimagerequestoptions/issynchronous
https://developer.apple.com/documentation/photos/phphotolibrary
https://developer.apple.com/documentation/photos/phphotolibrary/authorizationstatus(for:)
https://developer.apple.com/documentation/photos/phphotolibrary/performchanges(_:completionhandler:)
https://developer.apple.com/documentation/photos/phphotolibrary/presentlimitedlibrarypicker(from:)
https://developer.apple.com/documentation/photos/phphotolibrary/requestauthorization(for:handler:)
https://developer.apple.com/documentation/photos/phphotolibrarychangeobserver
https://developer.apple.com/documentation/photosui/photospicker
https://developer.apple.com/documentation/photosui/photospickeritem
https://developer.apple.com/documentation/photosui/phpickerconfiguration-swift.struct
https://developer.apple.com/documentation/photosui/phpickerconfiguration-swift.struct/selectionlimit
https://developer.apple.com/documentation/photosui/phpickerfilter-swift.struct
https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct
https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct/assetidentifier
https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct/itemprovider
https://developer.apple.com/documentation/photosui/phpickerviewcontroller

## Purpose

Reference index for Apple's PhotoKit and PhotosUI documentation, scoped to this domain's v1: picking assets without any authorization at all through `PHPickerViewController` and its SwiftUI-native equivalent `PhotosPicker`, reading what those pickers return (`PHPickerResult.itemProvider`, `assetIdentifier`, `PhotosPickerItem`'s `Transferable` conformance) and configuring them (`PHPickerConfiguration`, `selectionLimit`, `PHPickerFilter`); requesting library access when the picker is not enough — `PHPhotoLibrary.requestAuthorization(for:handler:)`/`authorizationStatus(for:)` with `PHAccessLevel` and `PHAuthorizationStatus`, and the matching Information Property List keys `NSPhotoLibraryUsageDescription` and `NSPhotoLibraryAddUsageDescription`; the limited library (`PHAuthorizationStatus.limited`, `presentLimitedLibraryPicker(from:)`, the `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` Information Property List key, and `PHPhotoLibraryChangeObserver` as the signal a selection changed); fetching and displaying assets (`PHAsset`, `PHAssetCollection`, `PHFetchOptions`, `PHFetchResult`, `PHImageManager`/`PHCachingImageManager` with `PHImageRequestOptions`); and writing to the library inside a change block (`performChanges(_:completionHandler:)`, `PHAssetChangeRequest`, `PHAssetCreationRequest`).

Out of scope for v1: photo and video *editing* (`PHContentEditingInput`/`PHContentEditingOutput`, adjustment data, and Photo Editing extensions); Live Photo playback surfaces (`PHLivePhotoView`); video playback and `AVAsset` export from a `PHAsset`; `PHAssetResource`-level resource copying; iCloud Shared Albums, Shared Photo Library, and cloud-identifier mapping; camera capture, which is AVFoundation's and not this framework's; and the deprecated `UIImagePickerController`, which `PHPickerViewController` replaces.

## Primary Topics

- Picking assets with no library authorization: `PHPickerViewController` and `PhotosPicker`
- Authorization levels, their usage-description keys, and the status API that reports `limited` truthfully
- The limited library: what it changes, and presenting its selection interface
- Fetching assets and requesting images, including the multi-callback delivery contract
- Writing to the library through a change block

## Used By

- knowledge/photos/picker-and-selection-results.md ([[knowledge/photos/picker-and-selection-results]])
- knowledge/photos/authorization-and-access-levels.md ([[knowledge/photos/authorization-and-access-levels]])
- knowledge/photos/limited-library.md ([[knowledge/photos/limited-library]])
- knowledge/photos/asset-fetching.md ([[knowledge/photos/asset-fetching]])
- knowledge/photos/image-requests.md ([[knowledge/photos/image-requests]])
- knowledge/photos/saving-to-the-library.md ([[knowledge/photos/saving-to-the-library]])
