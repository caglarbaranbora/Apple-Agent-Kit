# Apple Pay Authorization and Result Handling

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.passkit.apple-pay-authorization-and-result-handling
type: knowledge
title: Apple Pay Authorization and Result Handling
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines presenting the Apple Pay sheet with PKPaymentAuthorizationController and its delegate, receiving PKPayment/PKPaymentToken in didAuthorizePayment(_:handler:), returning a PKPaymentAuthorizationResult, and dismissing via paymentAuthorizationControllerDidFinish(_:) -- with token decryption and processor validation kept strictly server-side.
domain: PassKit
tags:
  - passkit
  - apple-pay
  - pkpaymentauthorizationcontrollerdelegate
  - pkpaymenttoken
  - pkpaymentauthorizationresult
references:
  - https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontrollerdelegate
  - https://developer.apple.com/documentation/passkit/pkpayment
  - https://developer.apple.com/documentation/passkit/pkpaymenttoken
  - https://developer.apple.com/documentation/passkit/pkpaymentauthorizationresult
  - https://developer.apple.com/documentation/passkit/pkpaymentauthorizationstatus
depends_on:
  - knowledge.passkit.apple-pay-payment-request
related: []
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent presents the Apple Pay authorization sheet built from a `PKPaymentRequest` (`apple-pay-payment-request`) and handles its outcome: implementing `PKPaymentAuthorizationControllerDelegate`, receiving the encrypted `PKPayment`/`PKPaymentToken` in `didAuthorizePayment(_:handler:)`, returning a `PKPaymentAuthorizationResult`, and dismissing the sheet from `paymentAuthorizationControllerDidFinish(_:)`. It draws the same app-vs-server boundary discipline as `pass-updates-and-push-registration`: decrypting the token and validating with a payment processor is server-side work this contract does not attempt to document as app API.

## Scope

### Included

-   Presenting with `PKPaymentAuthorizationController.present(completion:)` after setting its `delegate`
-   `PKPaymentAuthorizationControllerDelegate.paymentAuthorizationController(_:didAuthorizePayment:handler:)` (completion-handler and `async` forms) receiving a `PKPayment`
-   Constructing `PKPaymentAuthorizationResult(status:errors:)` and the `PKPaymentAuthorizationStatus` cases
-   `paymentAuthorizationControllerDidFinish(_:)` as the required dismissal hook
-   That `PKPayment.token`/`PKPaymentToken.paymentData` is encrypted, and forwarding it to the app's own back end is the app's only responsibility for the payment data itself

### Excluded

-   Building the `PKPaymentRequest` and checking `canMakePayments`/`canMakePayments(usingNetworks:)` — see `apple-pay-payment-request`
-   Decrypting `PKPaymentToken.paymentData`, merchant session validation, and payment-processor submission — server-side/back-end work, not app-side Swift API, out of scope for this domain entirely
-   Shipping/coupon/method-selection delegate callbacks (`didSelectShippingContact`, `didChangeCouponCode`, etc.) as their own deep topic

## Rules

### Rule 1

Agents MUST set `PKPaymentAuthorizationController.delegate` before calling `present(completion:)`, and MUST implement `paymentAuthorizationController(_:didAuthorizePayment:handler:)` to receive the outcome. Apple's `PKPaymentAuthorizationControllerDelegate` reference groups this method under "Handling user's payment authorization," describing it as: "Tells the delegate that the user authorized the payment request, and asks for a result... The system calls this method after the payment request is authorized. You submit the payment information to your payment processor to authorize the transaction, and then call the handler."

### Rule 2

Agents MUST treat the `PKPayment` delivered to `didAuthorizePayment(_:handler:)` as containing only encrypted payment data, never as a plaintext card number or account identifier to inspect or log. Per Apple's documentation, `PKPayment` "Represents the result of authorizing a payment request and contains payment information, encrypted in the payment token," and `PKPaymentToken.paymentData` is documented as data the app should "Send... to your e-commerce back-end system, where it can be decrypted and submitted to your payment processor" — decryption and processor submission are explicitly server-side, matching the same app-vs-server boundary used in `pass-updates-and-push-registration`.

### Rule 3

Agents MUST call the `handler`/return value of `didAuthorizePayment(_:handler:)` with a `PKPaymentAuthorizationResult` built via `init(status:errors:)`, choosing `.success` with an empty `errors` array or `.failure` (or a more specific status like `.invalidShippingContact`) with populated `errors`. Per Apple's documentation, "If the Apple Pay sheet contains errors, you provide a [`.failure`] status to [`PKPaymentAuthorizationResult`], and include the errors in the errors array. If there are no errors, you provide a [`.success`] status and leave the error array empty."

### Rule 4

Agents MUST implement `paymentAuthorizationControllerDidFinish(_:)` and dismiss the controller from that method, not from inside `didAuthorizePayment(_:handler:)` or on a timer. Per Apple's documentation, "Use this method to dismiss the payment authorization controller and update any other app state," and Apple is explicit about when it fires: "When the user authorizes a payment request, this method is called after the user is shown the status from the [`didAuthorizePayment(_:handler:)`] method's completion block. When the user cancels without authorizing the payment request, only [`paymentAuthorizationControllerDidFinish(_:)`] is called."

### Rule 5

Agents MUST NOT block the completion handler passed to `didAuthorizePayment(_:handler:)` on a synchronous network call to the app's own back end without a timeout, since the delegate method is `@MainActor` and the Apple Pay sheet visibly waits on that handler before showing a result to the user. This is reasoned framework behavior rather than a literal quote: Apple documents the method as `@MainActor`, and the sheet's own UX (showing a success/failure state before dismissal) depends on the handler being called in a bounded time.

## Compliant Example

```swift
import PassKit

final class CheckoutHandler: NSObject, PKPaymentAuthorizationControllerDelegate {
    func paymentAuthorizationController(
        _ controller: PKPaymentAuthorizationController,
        didAuthorizePayment payment: PKPayment,
        handler completion: @escaping (PKPaymentAuthorizationResult) -> Void
    ) {
        // Rule 2: payment.token.paymentData is encrypted; forward it as-is.
        submitToBackend(paymentData: payment.token.paymentData) { success in
            let status: PKPaymentAuthorizationStatus = success ? .success : .failure
            completion(PKPaymentAuthorizationResult(status: status, errors: nil)) // Rule 3
        }
    }

    func paymentAuthorizationControllerDidFinish(_ controller: PKPaymentAuthorizationController) {
        controller.dismiss(completion: nil) // Rule 4
    }

    private func submitToBackend(paymentData: Data, completion: @escaping (Bool) -> Void) {
        // Server decrypts the token and talks to the payment processor -- out of scope here.
    }
}
```

## Non-Compliant Example

```swift
import PassKit

final class CheckoutHandler: NSObject, PKPaymentAuthorizationControllerDelegate {
    func paymentAuthorizationController(
        _ controller: PKPaymentAuthorizationController,
        didAuthorizePayment payment: PKPayment,
        handler completion: @escaping (PKPaymentAuthorizationResult) -> Void
    ) {
        // Attempts to decrypt/inspect the payment token client-side -- violates Rule 2.
        let decoded = String(data: payment.token.paymentData, encoding: .utf8)
        print("Card data: \(decoded ?? "")")
        completion(PKPaymentAuthorizationResult(status: .success, errors: nil))
        // Dismisses immediately here instead of waiting for
        // paymentAuthorizationControllerDidFinish(_:) -- violates Rule 4.
        controller.dismiss(completion: nil)
    }
}
```
Treats the encrypted payment token as inspectable client-side data (Rule 2) and dismisses the sheet from inside the authorization callback instead of the dedicated finish callback (Rule 4).

## Dependencies

-   `knowledge.passkit.apple-pay-payment-request` — this contract assumes a `PKPaymentRequest` has already been built and availability-checked, and picks up at presenting the resulting authorization sheet.

## References

-   [Apple Developer — PKPaymentAuthorizationControllerDelegate](https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontrollerdelegate)
-   [Apple Developer — PKPayment](https://developer.apple.com/documentation/passkit/pkpayment)
-   [Apple Developer — PKPaymentToken](https://developer.apple.com/documentation/passkit/pkpaymenttoken)
-   [Apple Developer — PKPaymentAuthorizationResult](https://developer.apple.com/documentation/passkit/pkpaymentauthorizationresult)
-   [Apple Developer — PKPaymentAuthorizationStatus](https://developer.apple.com/documentation/passkit/pkpaymentauthorizationstatus)
