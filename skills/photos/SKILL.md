---
name: photos
description: Route Photos and PhotoKit implementation tasks to the correct Knowledge Contracts -- picking assets with no authorization, requesting library access and its usage-description keys, the limited library, fetching assets, requesting images, and writing to the library. Use when presenting PhotosPicker or PHPickerViewController, configuring PHPickerConfiguration/selectionLimit/PHPickerFilter, reading PHPickerResult.itemProvider or assetIdentifier or PhotosPickerItem, calling PHPhotoLibrary.requestAuthorization(for:) or authorizationStatus(for:), declaring NSPhotoLibraryUsageDescription/NSPhotoLibraryAddUsageDescription, handling PHAuthorizationStatus.limited or presentLimitedLibraryPicker(from:), fetching with PHFetchOptions/PHFetchResult, requesting images through PHImageManager/PHCachingImageManager, or saving with performChanges and PHAssetCreationRequest. v1 is library access, reading, and saving only -- no photo editing (PHContentEditingInput/Output), no PHLivePhotoView, no AVAsset export, and no camera capture (that is AVFoundation, not this domain). Triggers on Photos, PhotoKit, PhotosUI, photo library, PHPickerViewController, PhotosPicker, PHPhotoLibrary, PHAsset, PHFetchResult, PHImageManager, PHAssetCreationRequest, limited library, photo permission, save to photos, photo picker.
id: skill.photos.foundations
title: Photos — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Photos
routes: [knowledge.photos.picker-and-selection-results, knowledge.photos.authorization-and-access-levels, knowledge.photos.limited-library, knowledge.photos.asset-fetching, knowledge.photos.image-requests, knowledge.photos.saving-to-the-library]
related: []
last_updated: 2026-08-09
---

# Photos — Foundations Skill

## Purpose

Route Photos and PhotoKit implementation tasks to the minimum required
Photos Knowledge Contracts. v1 scope is reaching the user's photo
library: selecting assets with no permission at all, requesting access
when selection is not enough, behaving correctly under limited access,
reading assets and their images, and writing new ones — not editing
photos, not playing Live Photos or video, and not capturing from the
camera.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/photos/.

-   Presenting `PhotosPicker` or `PHPickerViewController`; setting `selectionLimit`/`maxSelectionCount` or a `PHPickerFilter`; reading `PHPickerResult.itemProvider`/`assetIdentifier` or a `PhotosPickerItem` -> picker-and-selection-results.md
-   Calling `PHPhotoLibrary.requestAuthorization(for:handler:)`/`authorizationStatus(for:)`; choosing `PHAccessLevel.addOnly` vs `.readWrite`; declaring `NSPhotoLibraryUsageDescription`/`NSPhotoLibraryAddUsageDescription`; branching on `PHAuthorizationStatus` -> authorization-and-access-levels.md
-   Handling `PHAuthorizationStatus.limited`; calling `presentLimitedLibraryPicker(from:)`; setting `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` -> limited-library.md
-   Building a `PHFetchOptions` query; holding or refreshing a `PHFetchResult`; fetching a `PHAssetCollection`'s members; reading where a photo was taken from `PHAsset.location` -> asset-fetching.md
-   Calling `PHImageManager.requestImage(...)`; setting `PHImageRequestOptions`' `isSynchronous`/`deliveryMode`/`isNetworkAccessAllowed`; priming a `PHCachingImageManager` -> image-requests.md
-   Running `performChanges(_:completionHandler:)`; creating with `PHAssetChangeRequest`/`PHAssetCreationRequest`; capturing `placeholderForCreatedAsset` -> saving-to-the-library.md

Never load more than the contracts relevant to the specific question.
For how a usage-description string should be *worded*, route to
`skill.app-store-review-guidelines.submission`. For whether to show a
pre-permission screen and what it says, route to
`skill.human-interface-guidelines.foundations`. For declaring photo data
in `PrivacyInfo.xcprivacy`, route to `skill.privacy.foundations`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/photos/ — do not guess or fall back to general
knowledge. Photo and video editing (`PHContentEditingInput`,
`PHContentEditingOutput`, adjustment data, Photo Editing extensions),
`PHLivePhotoView`, `AVAsset` export from a `PHAsset`, and
`PHAssetResource`-level resource copying are out of scope entirely (see
docs/architecture/domain-map.md). Capturing a new photo from the camera
is AVFoundation's and has no Skill yet — report that rather than
answering.

A photo's recorded capture place is this domain's, not `core-location`'s:
`PHAsset.location` arrives with the library grant, so asset-fetching.md
Rule 5 owns it and no location authorization is involved. Route to
`core-location` only when the task needs the *device's* current or
ongoing location, which is a different fact about a different subject.

SwiftUI interop with this domain is split deliberately, and the split is
this Skill's: `PhotosPicker` is SwiftUI-native, so
picker-and-selection-results.md Rule 2 *forbids* wrapping the picker,
while `presentLimitedLibraryPicker(from:)` takes a `UIViewController`
and has no SwiftUI counterpart, so limited-library.md Rule 5 *requires*
a bridge. How any such wrapper is written belongs to `uikit-interaction`
and is not restated here.
