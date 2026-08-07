# Apple Pay Payment Request

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.passkit.apple-pay-payment-request
artifact_type: knowledge
title: Apple Pay Payment Request
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines building a PKPaymentRequest (merchantIdentifier, countryCode, currencyCode, supportedNetworks, merchantCapabilities, paymentSummaryItems) and checking payment availability with PKPaymentAuthorizationController.canMakePayments()/canMakePayments(usingNetworks:) before offering Apple Pay as an option at all.
domain: PassKit
tags:
  - passkit
  - apple-pay
  - pkpaymentrequest
  - canmakepayments
  - paywithapplepaybutton
references:
  - https://developer.apple.com/documentation/passkit/pkpaymentrequest
  - https://developer.apple.com/documentation/passkit/pkpaymentbutton
  - https://developer.apple.com/documentation/passkit/paywithapplepaybutton
  - https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller
  - https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller/canmakepayments()
depends_on: []
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent builds a `PKPaymentRequest` and decides whether to offer Apple Pay as a payment option at all, before any authorization sheet is presented. Presenting that sheet and handling its result is a separate contract, `apple-pay-authorization-and-result-handling`, which this one feeds.

## Scope

### Included

-   Constructing `PKPaymentRequest`: `merchantIdentifier`, `countryCode`, `currencyCode`, `supportedNetworks`, `merchantCapabilities`, `paymentSummaryItems`
-   Checking availability with `PKPaymentAuthorizationController.canMakePayments()` and the network-scoped `canMakePayments(usingNetworks:)`
-   Choosing an entry-point control: the SwiftUI-native `PayWithApplePayButton` vs. the UIKit `PKPaymentButton`
-   That `PKPaymentAuthorizationController` and `PKPaymentAuthorizationViewController` both currently exist and are not deprecated, and how they differ

### Excluded

-   Presenting the authorization sheet, `PKPaymentAuthorizationControllerDelegate`, and handling `PKPayment`/`PKPaymentAuthorizationResult` — see `apple-pay-authorization-and-result-handling`
-   Server-side merchant validation, payment-token decryption, and payment-processor integration — not app-side Swift code, out of scope for this domain entirely
-   Recurring/automatic-reload/deferred payment requests and multi-token/multi-merchant contexts as their own deep topics

## Rules

### Rule 1

Agents MUST check payment availability before presenting or even advertising Apple Pay as an option, using `PKPaymentAuthorizationController.canMakePayments()` for a general check or `canMakePayments(usingNetworks:)` when the request needs specific card networks. Per Apple's documentation, `canMakePayments()` returns whether "the device supports making payments," while `canMakePayments(usingNetworks:)` returns whether "the user can make payments through any of the specified networks" — and Apple explicitly distinguishes the two: "On devices that support making payments but don't have any payment cards configured, the [`canMakePayments()`] method returns `true`... but the [`canMakePayments(usingNetworks:)`] method returns `false` regardless of network."

### Rule 2

Agents MUST set `merchantIdentifier`, `countryCode`, `currencyCode`, `supportedNetworks`, `merchantCapabilities`, and `paymentSummaryItems` on every `PKPaymentRequest`, since Apple's reference groups exactly these under "Setting merchant information," "Setting currency and region information," and "Setting the payment summary items" as the request's core identity and content. Agents MUST NOT construct a request with only some of these set and expect the authorization flow to fill in the rest.

### Rule 3

Agents choosing between the two ways to present the payment sheet MUST know both `PKPaymentAuthorizationController` and `PKPaymentAuthorizationViewController` currently exist and neither is marked deprecated, and MUST prefer `PKPaymentAuthorizationController` when the app targets any surface without UIKit. Per Apple's documentation, "The `PKPaymentAuthorizationController` class performs the same role as the `PKPaymentAuthorizationViewController` class, but it does not depend on the UIKit framework. This means that the authorization controller can be used in places where a view controller cannot (for example, in watchOS apps or in SiriKit extensions)."

### Rule 4

Agents building a SwiftUI entry point SHOULD use `PayWithApplePayButton` rather than wrapping the UIKit `PKPaymentButton` in a representable, because PassKit ships a SwiftUI-native equivalent for this specific control (unlike the add-to-Wallet UI in `adding-passes-ui`, which has none). Per Apple's documentation, `PayWithApplePayButton` should be used "as the SwiftUI equivalent to [`PKPaymentButton`]," and it is available on watchOS, where `PKPaymentButton` is not (Apple's `PKPaymentButton` reference directs watchOS apps to a WatchKit-specific button instead).

### Rule 5

Agents MUST NOT hardcode `supportedNetworks` from memory; the actual list of `PKPaymentNetwork` values changes across OS releases (new card networks are added), so agents MUST select networks the app's merchant configuration and target OS versions actually support, verified against the current `PKPaymentNetwork` reference rather than assumed from an older code sample.

## Compliant Example

```swift
import PassKit
import SwiftUI

func canOfferApplePay(networks: [PKPaymentNetwork]) -> Bool {
    PKPaymentAuthorizationController.canMakePayments(usingNetworks: networks) // Rule 1
}

func makeRequest(total: NSDecimalNumber) -> PKPaymentRequest {
    let request = PKPaymentRequest()
    request.merchantIdentifier = "merchant.com.example.store" // Rule 2
    request.countryCode = "US"
    request.currencyCode = "USD"
    request.supportedNetworks = [.visa, .masterCard, .amex]
    request.merchantCapabilities = .threeDSecure
    request.paymentSummaryItems = [
        PKPaymentSummaryItem(label: "Example Store", amount: total)
    ]
    return request
}

struct CheckoutButton: View {
    let request: PKPaymentRequest
    var body: some View {
        PayWithApplePayButton(.buy) { payment, completion in // Rule 4
            // Present authorization; see apple-pay-authorization-and-result-handling.
        }
    }
}
```

## Non-Compliant Example

```swift
import PassKit

func makeRequest(total: NSDecimalNumber) -> PKPaymentRequest {
    let request = PKPaymentRequest()
    request.merchantIdentifier = "merchant.com.example.store"
    // countryCode, currencyCode, supportedNetworks, merchantCapabilities never set -- violates Rule 2.
    request.paymentSummaryItems = [PKPaymentSummaryItem(label: "Example Store", amount: total)]
    return request
}

func presentApplePayButton() -> Bool {
    // Never checks canMakePayments()/canMakePayments(usingNetworks:) before deciding
    // to show Apple Pay as an option at all -- violates Rule 1.
    return true
}
```
Builds an incomplete `PKPaymentRequest` missing region/network/capability fields (Rule 2) and offers Apple Pay unconditionally without checking whether the device or user can actually pay (Rule 1).

## Dependencies

None within this domain — this is the foundational contract `apple-pay-authorization-and-result-handling` assumes a valid, availability-checked `PKPaymentRequest` already exists before presenting the authorization sheet.

## References

-   [Apple Developer — PKPaymentRequest](https://developer.apple.com/documentation/passkit/pkpaymentrequest)
-   [Apple Developer — PKPaymentButton](https://developer.apple.com/documentation/passkit/pkpaymentbutton)
-   [Apple Developer — PayWithApplePayButton](https://developer.apple.com/documentation/passkit/paywithapplepaybutton)
-   [Apple Developer — PKPaymentAuthorizationController](https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller)
-   [Apple Developer — canMakePayments()](https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller/canmakepayments())
