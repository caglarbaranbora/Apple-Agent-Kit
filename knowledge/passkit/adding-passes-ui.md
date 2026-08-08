# Adding Passes UI

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.passkit.adding-passes-ui
artifact_type: knowledge
title: Adding Passes UI
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines presenting the system add-to-Wallet UI for a pass the app already has as PKPass/Data -- PKAddPassesViewController(pass:)/(passes:), PKAddPassButton, the canAddPasses() availability check, and the UIKit-only delegate/dismissal pattern (no SwiftUI representable ships in PassKit).
domain: PassKit
tags:
  - passkit
  - pkaddpassesviewcontroller
  - pkaddpassbutton
  - wallet-ui
  - uikit
references:
  - https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller
  - https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller/canaddpasses()
  - https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller/init(pass:)
  - https://developer.apple.com/documentation/passkit/pkaddpassesviewcontrollerdelegate
  - https://developer.apple.com/documentation/passkit/pkaddpassbutton
depends_on:
  - knowledge.passkit.pass-library-and-authorization
related:
  - knowledge.uikit.swiftui-view-representable
last_updated: 2026-08-08
```

## Intent

This contract defines the client-side UI flow for adding a pass the app already holds as `PKPass`/`Data` to the user's Wallet: checking `PKAddPassesViewController.canAddPasses()` before presenting anything, constructing and presenting `PKAddPassesViewController`, styling the entry point with `PKAddPassButton`, and handling completion through `PKAddPassesViewControllerDelegate`. It assumes the app already knows how to query/add through `PKPassLibrary` directly (`pass-library-and-authorization`) and is choosing the UI-presentation path instead.

## Scope

### Included

-   `PKAddPassesViewController.canAddPasses()` as the availability check specific to this UI flow
-   Constructing `PKAddPassesViewController(pass:)` / `init(passes:)` from a `PKPass` (both are failable initializers)
-   Presenting the view controller and dismissing it via `PKAddPassesViewControllerDelegate.addPassesViewControllerDidFinish(_:)`
-   `PKAddPassButton` as the recommended entry-point control and its button styles
-   That this entire flow is UIKit-only, with no SwiftUI representable shipped by PassKit

### Excluded

-   Direct `PKPassLibrary` querying/adding without presenting UI — see `pass-library-and-authorization`
-   `.pkpass`/`pass.json` structure and constructing the `PKPass` this flow presents — see `pass-content-and-required-fields`
-   `PKAddSecureElementPassViewController` — a distinct, NFC/secure-element-specific view controller, not covered by this domain's v1

## Rules

### Rule 1

Agents MUST check `PKAddPassesViewController.canAddPasses()` before constructing or presenting the view controller, and MUST NOT assume every device that supports `PKPassLibrary` also supports this specific UI flow. Per Apple's documentation, `canAddPasses()` "Returns a Boolean value that indicates whether the device supports adding passes" — this is a separate, narrower check from `PKPassLibrary.isPassLibraryAvailable()` (see `pass-library-and-authorization`), scoped specifically to the add-passes UI.

### Rule 2

Agents MUST construct `PKAddPassesViewController` with `init(pass:)` for a single pass or `init(passes:)` for multiple, and MUST handle the failable initializer's `nil` case rather than force-unwrapping. Per Apple's documentation, `init(pass:)` "Initializes and returns a newly created add-passes view controller with a single pass," returning "the initialized add-passes view controller object or `nil` if there was a problem initializing the object."

### Rule 3

Agents MUST implement `PKAddPassesViewControllerDelegate.addPassesViewControllerDidFinish(_:)` and dismiss the presented view controller from that callback, rather than dismissing on a fixed timer or leaving dismissal to the system. Apple's `PKAddPassesViewControllerDelegate` reference documents exactly one delegate method — `addPassesViewControllerDidFinish(_:)` — as "Methods that an add-passes view controller's delegate implements," confirming this single callback is the intended dismissal hook regardless of whether the user added the pass or cancelled.

### Rule 4

Agents adding an entry point for this flow SHOULD use `PKAddPassButton` rather than a custom-styled button, so Wallet's system-provided appearance and localization stay correct. Per Apple's documentation, `PKAddPassButton` "Provides a button that enables users to add passes to Wallet," and "you choose the type and style of button, and the system provides a control with the correct content and appearance."

### Rule 5

Agents building this flow in SwiftUI MUST wrap `PKAddPassesViewController` in a `UIViewControllerRepresentable` as defined by `knowledge.uikit.swiftui-view-representable` Rule 5 — which this contract does not restate — and MUST NOT expect a SwiftUI-native equivalent to `TipView`/`EventKitUI`'s pattern. This is reasoned framework behavior rather than a literal Apple quote: `PKAddPassesViewController` and `PKAddPassButton` are documented only for iOS, iPadOS, Mac Catalyst, and visionOS with no SwiftUI counterpart in PassKit's topic index — unlike Apple Pay's `PayWithApplePayButton` (see `apple-pay-payment-request`), which does ship a SwiftUI-native button.

## Compliant Example

```swift
import UIKit
import PassKit

final class AddPassCoordinator: NSObject, PKAddPassesViewControllerDelegate {
    func presentAddPass(for pass: PKPass, from presenter: UIViewController) {
        guard PKAddPassesViewController.canAddPasses() else { return } // Rule 1
        guard let addPassesVC = PKAddPassesViewController(pass: pass) else { return } // Rule 2
        addPassesVC.delegate = self
        presenter.present(addPassesVC, animated: true)
    }

    func addPassesViewControllerDidFinish(_ controller: PKAddPassesViewController) {
        controller.dismiss(animated: true) // Rule 3
    }
}
```

## Non-Compliant Example

```swift
import UIKit
import PassKit

func presentAddPass(for pass: PKPass, from presenter: UIViewController) {
    // Never checks canAddPasses() -- violates Rule 1.
    let addPassesVC = PKAddPassesViewController(pass: pass)! // force-unwraps the failable init -- violates Rule 2
    // No delegate set, so addPassesViewControllerDidFinish(_:) never fires and the
    // sheet is dismissed on a fixed timer instead -- violates Rule 3.
    presenter.present(addPassesVC, animated: true)
    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
        addPassesVC.dismiss(animated: true)
    }
}
```
Skips the flow-specific availability check (Rule 1), force-unwraps a failable initializer (Rule 2), and dismisses on a guessed timer instead of the delegate callback Apple documents for this purpose (Rule 3).

## Dependencies

-   `knowledge.passkit.pass-library-and-authorization` — this contract assumes the app already has a `PKPass` in hand and knows how `PKPassLibrary` itself is queried; it covers only the UI-presentation path for adding that pass.

## References

-   [Apple Developer — PKAddPassesViewController](https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller)
-   [Apple Developer — canAddPasses()](https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller/canaddpasses())
-   [Apple Developer — init(pass:)](https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller/init(pass:))
-   [Apple Developer — PKAddPassesViewControllerDelegate](https://developer.apple.com/documentation/passkit/pkaddpassesviewcontrollerdelegate)
-   [Apple Developer — PKAddPassButton](https://developer.apple.com/documentation/passkit/pkaddpassbutton)
