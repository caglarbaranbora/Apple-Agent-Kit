# PassKit

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/passkit
https://developer.apple.com/documentation/passkit/pkpasslibrary
https://developer.apple.com/documentation/passkit/pkpasslibrary/ispasslibraryavailable()
https://developer.apple.com/documentation/passkit/pkpasslibrary/containspass(_:)
https://developer.apple.com/documentation/passkit/pkpasslibrary/passes()
https://developer.apple.com/documentation/passkit/pkpasslibrary/passes(of:)
https://developer.apple.com/documentation/passkit/pkpasslibrary/addpasses(_:withcompletionhandler:)
https://developer.apple.com/documentation/passkit/pkpasslibraryaddpassesstatus
https://developer.apple.com/documentation/passkit/pkpasstype
https://developer.apple.com/documentation/passkit/pkpass
https://developer.apple.com/documentation/passkit/pkpass/init(data:)
https://developer.apple.com/documentation/passkit/pkpass/webserviceurl
https://developer.apple.com/documentation/passkit/pkpass/authenticationtoken
https://developer.apple.com/documentation/passkit/pkpass/serialnumber
https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller
https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller/canaddpasses()
https://developer.apple.com/documentation/passkit/pkaddpassesviewcontroller/init(pass:)
https://developer.apple.com/documentation/passkit/pkaddpassesviewcontrollerdelegate
https://developer.apple.com/documentation/passkit/pkaddpassbutton
https://developer.apple.com/documentation/walletpasses/pass
https://developer.apple.com/documentation/walletpasses/passfields
https://developer.apple.com/documentation/walletpasses/pass/barcode-data.dictionary
https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes
https://developer.apple.com/documentation/walletpasses/register-a-pass-for-update-notifications
https://developer.apple.com/documentation/passkit/pkpaymentrequest
https://developer.apple.com/documentation/passkit/pkpaymentbutton
https://developer.apple.com/documentation/passkit/paywithapplepaybutton
https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller
https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontroller/canmakepayments()
https://developer.apple.com/documentation/passkit/pkpaymentauthorizationviewcontroller
https://developer.apple.com/documentation/passkit/pkpaymentauthorizationcontrollerdelegate
https://developer.apple.com/documentation/passkit/pkpayment
https://developer.apple.com/documentation/passkit/pkpaymenttoken
https://developer.apple.com/documentation/passkit/pkpaymentauthorizationresult
https://developer.apple.com/documentation/passkit/pkpaymentauthorizationstatus

## Purpose

Reference index for Apple's PassKit documentation, scoped to this domain's v1: querying and adding to the user's Wallet pass library through `PKPassLibrary` (`isPassLibraryAvailable()`, `containsPass(_:)`, `passes()`/`passes(of:)`, `addPasses(_:withCompletionHandler:)` and its async form, `PKPassLibraryAddPassesStatus`); the structure of a `.pkpass` bundle's `pass.json` (`formatVersion`/`passTypeIdentifier`/`serialNumber`/`teamIdentifier`/`organizationName`/`description`, the five style keys `boardingPass`/`coupon`/`eventTicket`/`storeCard`/`generic`, the `PassFields` groups, `barcodes`, `locations`/`relevantDates`) and inspecting a pass client-side via `PKPass(data:)`; presenting the add-to-Wallet UI with `PKAddPassesViewController`/`PKAddPassButton`; the `webServiceURL`/`authenticationToken` pass fields and the web-service protocol that lets a server push pass updates; and building/presenting an Apple Pay payment request with `PKPaymentRequest`, `PKPaymentAuthorizationController`/`PKPaymentAuthorizationViewController`, `PayWithApplePayButton`/`PKPaymentButton`, and handling the result through `PKPaymentAuthorizationControllerDelegate`.

Out of scope for v1: server-side pass signing, certificate management, and the Pass Type ID/Apple Developer portal setup process, none of which is app-side Swift code; `PKAddSecureElementPassViewController` and NFC/secure-element-backed passes (transit cards, car keys, driver's-license-in-Wallet), a distinct and more specialized subsystem; `PKPassPersonalization` (the transit-pass personalization flow); and Apple Pay server-side merchant validation, payment-token decryption, and payment-processor integration — real, necessary parts of shipping Apple Pay, but not app-side Swift API surface this domain documents.

## Primary Topics

- Pass library querying and adding passes already on device or in hand (`PKPassLibrary`)
- `.pkpass`/`pass.json` structure and required fields, and client-side inspection via `PKPass`
- The add-to-Wallet UI flow (`PKAddPassesViewController`, `PKAddPassButton`)
- Pass updates: the web-service fields on a pass and the app-vs-server update boundary
- Building an Apple Pay `PKPaymentRequest` and checking payment availability
- Presenting Apple Pay authorization and handling `PKPayment`/`PKPaymentAuthorizationResult`

## Used By

- knowledge/passkit/pass-library-and-authorization.md ([[knowledge/passkit/pass-library-and-authorization]])
- knowledge/passkit/pass-content-and-required-fields.md ([[knowledge/passkit/pass-content-and-required-fields]])
- knowledge/passkit/adding-passes-ui.md ([[knowledge/passkit/adding-passes-ui]])
- knowledge/passkit/pass-updates-and-push-registration.md ([[knowledge/passkit/pass-updates-and-push-registration]])
- knowledge/passkit/apple-pay-payment-request.md ([[knowledge/passkit/apple-pay-payment-request]])
- knowledge/passkit/apple-pay-authorization-and-result-handling.md ([[knowledge/passkit/apple-pay-authorization-and-result-handling]])
- skills/passkit/SKILL.md ([[skills/passkit/SKILL]])
