# Modal Presentation

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.modal-presentation
type: knowledge
title: Modal Presentation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of present(_:animated:completion:), dismiss(animated:completion:), and UIModalPresentationStyle to show a screen modally, including sheet-style presentation.
domain: UIKit
tags:
  - uikit
  - presentation
  - modal
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/present(_:animated:completion:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/dismiss(animated:completion:)
  - https://developer.apple.com/documentation/uikit/uimodalpresentationstyle
depends_on: []
related:
  - knowledge.uikit.navigation-controller
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent presents a screen modally
with `present(_:animated:completion:)`/`dismiss(animated:completion:)`
and an explicit `UIModalPresentationStyle`, for content that interrupts
the current flow rather than continuing it.

## Scope

### Included

-   `present(_:animated:completion:)` / `dismiss(animated:completion:)`
-   `UIModalPresentationStyle` selection (`.pageSheet`/`.formSheet`/`.fullScreen`, etc.)
-   Who calls dismiss (presenting vs. presented view controller)

### Excluded

-   Push/pop stack navigation — see `navigation-controller`

## Rules

### Rule 1

Agents MUST present a screen modally (`present(_:animated:completion:)`)
rather than pushing it, when the content is a self-contained task that
interrupts the current flow and has its own explicit completion (a
compose sheet, a settings flow, an onboarding step) — modal presentation
communicates "this is a separate task," matching the system's own use of
modals.

### Rule 2

Agents MUST set an explicit `modalPresentationStyle` on the presented
view controller rather than relying on the default — the default is
`.automatic`, which resolves to `.pageSheet` in most contexts; if the
design calls for `.fullScreen` (a sheet that must not be dismissed by a
downward swipe mid-task), it must be set explicitly.

### Rule 3

Agents MUST call `dismiss(animated:completion:)` on the *presenting*
view controller, or use `self.dismiss` from the presented one (which
forwards to its presenter) — dismissing is a paired operation with
`present`; calling it on an unrelated view controller in the hierarchy
has no effect.

### Rule 4

Agents SHOULD pass a completion handler to `dismiss(animated:completion:)`
for any work that must happen strictly after the dismissal animation
finishes (presenting a second modal, showing a toast) — starting that
work immediately after calling `dismiss` without the completion handler
races the still-running dismissal animation.

## Compliant Example

```swift
final class InboxViewController: UIViewController {
    func showCompose() {
        let composeVC = ComposeViewController()
        composeVC.modalPresentationStyle = .pageSheet
        present(composeVC, animated: true)
    }
}

final class ComposeViewController: UIViewController {
    func send() {
        submitDraft()
        presentingViewController?.dismiss(animated: true) {
            // safe to present another modal here
        }
    }
}
```
Explicit `.pageSheet` style, dismissal via the presenting controller with a completion handler. (Rules 2, 3, 4)

## Non-Compliant Example

```swift
final class ComposeViewController: UIViewController {
    func send() {
        submitDraft()
        navigationController?.popViewController(animated: true)
    }
}
```
A modally presented screen is torn down with `popViewController` instead of `dismiss` — since it was never pushed, this has no effect and the modal stays on screen. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — present(_:animated:completion:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/present(_:animated:completion:))
-   [Apple Developer — dismiss(animated:completion:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/dismiss(animated:completion:))
-   [Apple Developer — UIModalPresentationStyle](https://developer.apple.com/documentation/uikit/uimodalpresentationstyle)
