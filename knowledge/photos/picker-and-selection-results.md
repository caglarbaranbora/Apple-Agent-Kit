# Picker and Selection Results

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.photos.picker-and-selection-results
artifact_type: knowledge
title: Picker and Selection Results
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines letting the user choose assets with no library authorization at all -- PhotosPicker in SwiftUI, PHPickerViewController in UIKit, their configuration, and reading the placeholder results they return.
domain: Photos
tags:
  - photos
  - phpickerviewcontroller
  - photospicker
  - selection
  - itemprovider
references:
  - https://developer.apple.com/documentation/photosui/phpickerviewcontroller
  - https://developer.apple.com/documentation/photosui/photospicker
  - https://developer.apple.com/documentation/photosui/photospickeritem
  - https://developer.apple.com/documentation/photosui/phpickerconfiguration-swift.struct/selectionlimit
  - https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct/itemprovider
  - https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct/assetidentifier
  - https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app
depends_on: []
related:
  - knowledge.photos.authorization-and-access-levels
  - knowledge.uikit.swiftui-view-representable
last_updated: 2026-08-09
```

## Intent

This contract defines how an AI coding agent lets a user choose photos or videos without requesting access to the photo library: choosing the picker that matches the UI framework, configuring how many assets and which kinds it offers, and loading the deferred representations it hands back.

## Scope

### Included

-   Choosing a picker over library access when the task is only "let the user pick", and which of `PhotosPicker` (SwiftUI) / `PHPickerViewController` (UIKit) applies
-   `PHPickerConfiguration.selectionLimit` and `PHPickerFilter` / the `matching:` argument
-   Loading `PHPickerResult.itemProvider` and `PhotosPickerItem` representations, including failure
-   `PHPickerResult.assetIdentifier` and the authorization it converts the flow into needing

### Excluded

-   Requesting library access, the access levels, and the usage-description keys — see `authorization-and-access-levels`; and everything the limited library changes once access *is* requested — see `limited-library`
-   Fetching `PHAsset` objects and requesting their images — see `asset-fetching-and-image-requests`
-   How a `UIViewControllerRepresentable` wrapper is written when Rule 2's fallback applies — see `knowledge.uikit.swiftui-view-representable` Rule 5; this contract states none of those mechanics
-   Placing the picker in a SwiftUI view hierarchy, which is `knowledge.swiftui` view composition, not picker configuration

## Rules

### Rule 1

Agents MUST use a picker and request no photo-library authorization at all when the task is to let the user choose existing assets. Per Apple's documentation, `PHPickerViewController` runs outside the app: "Because the system manages its life cycle in a separate process, it's private by default. The user doesn't need to explicitly authorize your app to select photos, which results in a simpler and more streamlined user experience." Apple scopes library access to the cases the picker cannot serve — "If your app requires PhotoKit's advanced features, like retrieving assets and collections, or updating the library, the user must explicitly authorize it." A permission prompt added to a pure selection flow is a defect, not a precaution.

### Rule 2

Agents building this in SwiftUI MUST use `PhotosPicker` and MUST NOT wrap `PHPickerViewController` in a `UIViewControllerRepresentable`. PhotosUI ships a SwiftUI-native picker — "A view that displays a Photos picker for choosing assets from the photo library" — with initializers covering the same surface as the UIKit configuration, including the `photoLibrary:` variant Rule 5 describes. The wrapper is correct only below `PhotosPicker`'s availability (`PhotosPicker` is iOS 16.0; `PHPickerViewController` is iOS 14.0), and in that one case how the wrapper is written is `knowledge.uikit.swiftui-view-representable` Rule 5, which this contract does not restate. This domain differs deliberately from `eventkit` and `passkit`, whose frameworks ship no SwiftUI equivalent and so must always bridge.

### Rule 3

Agents MUST set `selectionLimit` (or `maxSelectionCount`) explicitly whenever the feature accepts more than one asset, and MUST NOT rely on the default. Per Apple's documentation, "The default value is `1`. Setting the value to `0` sets the selection limit to the maximum that the system supports." A multi-select feature left at the default silently becomes single-select. Agents SHOULD also narrow the picker with a filter — Apple's own example is `.any(of: [.images, .not(.screenshots)])` — rather than accepting everything and rejecting afterwards.

### Rule 4

Agents MUST load a selection asynchronously and MUST handle the failure case. Per Apple's documentation, "The selection results you get are placeholder objects. A `PhotosPickerItem` conforms to `Transferable`, and allows you to load a representation you request," and "A failure can occur when the system attempts to retrieve the data. For example, if the picker tries to download data from iCloud Photos without a network connection." Treating a returned item as an in-memory image is wrong on both counts. In SwiftUI the load is `loadTransferable(type:)`; in UIKit it is `PHPickerResult.itemProvider`, an `NSItemProvider` — "Representations of the selected asset."

### Rule 5

Agents MUST NOT read `PHPickerResult.assetIdentifier` expecting a value from a default configuration. `assetIdentifier` is "The local identifier of the selected asset" and is declared `String?`; it is populated only when the picker was configured with `init(photoLibrary:)`, and the identifier is useful only to code that can then fetch that `PHAsset` — which requires the library authorization Rule 1 avoided. Asking for identifiers therefore converts a zero-permission flow into a permissioned one, and agents MUST make that trade deliberately rather than as a side effect of copying a configuration.

### Rule 6

Agents MUST NOT subclass `PHPickerViewController` or alter its view's opacity. Per Apple's documentation, "As a system-rendered UI, you can't subclass `PHPickerViewController`. Its view hierarchy belongs to the system and therefore, the framework provides no access," and "In iOS 17 and later, the picker controller ignores touch events while its opacity is anything other than fully opaque." A fade-in animation applied to the presented picker disables it rather than styling it.

## Compliant Example

```swift
import SwiftUI
import PhotosUI

struct AttachmentPicker: View {                       // Rule 1: no authorization requested
    @State private var selection: [PhotosPickerItem] = []
    @State private var images: [Image] = []

    var body: some View {
        PhotosPicker(selection: $selection,           // Rule 2: SwiftUI-native picker
                     maxSelectionCount: 5,            // Rule 3: stated, not defaulted
                     matching: .any(of: [.images, .not(.screenshots)])) {
            Text("Add Photos")
        }
        .onChange(of: selection) { _, items in Task { await load(items) } }
    }

    private func load(_ items: [PhotosPickerItem]) async {
        for item in items {   // Rule 4: deferred; can fail, e.g. iCloud with no network
            if let image = try? await item.loadTransferable(type: Image.self) {
                images.append(image)
            }
        }
    }
}
```

## Non-Compliant Example

```swift
import PhotosUI
import Photos

func showPicker(from parent: UIViewController) {
    // Requests library access for a flow that only needs a selection -- violates Rule 1.
    PHPhotoLibrary.requestAuthorization(for: .readWrite) { _ in
        // No photoLibrary:, and selectionLimit left at 1 for a multi-attach feature.
        let picker = PHPickerViewController(configuration: PHPickerConfiguration())
        picker.view.layer.opacity = 0.98           // disables the picker -- violates Rule 6.
        parent.present(picker, animated: true)     // violates Rule 3
    }
}
func handle(_ results: [PHPickerResult]) {
    for result in results {
        let id = result.assetIdentifier!           // always nil here -- violates Rule 5.
        _ = PHAsset.fetchAssets(withLocalIdentifiers: [id], options: nil)
        // Never loads result.itemProvider, and has no failure path -- violates Rule 4.
    }
}
```

Requests permission a picker does not need (Rule 1), leaves the selection limit at its default (Rule 3), force-unwraps an identifier a default configuration never populates (Rule 5), never loads the deferred representation or handles its failure (Rule 4), and makes the system-rendered picker non-interactive (Rule 6).

## Dependencies

This contract has no dependencies. A picker requires no library authorization, which is the point of Rule 1; the neighbouring contracts apply only once an app moves past selection.


## References
-   [Apple Developer — PHPickerViewController](https://developer.apple.com/documentation/photosui/phpickerviewcontroller)
-   [Apple Developer — PhotosPicker](https://developer.apple.com/documentation/photosui/photospicker)
-   [Apple Developer — PhotosPickerItem](https://developer.apple.com/documentation/photosui/photospickeritem)
-   [Apple Developer — PHPickerConfiguration.selectionLimit](https://developer.apple.com/documentation/photosui/phpickerconfiguration-swift.struct/selectionlimit)
-   [Apple Developer — PHPickerResult.itemProvider](https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct/itemprovider)
-   [Apple Developer — PHPickerResult.assetIdentifier](https://developer.apple.com/documentation/photosui/phpickerresult-swift.struct/assetidentifier)
-   [Apple Developer — Delivering an enhanced privacy experience in your Photos app](https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app)
