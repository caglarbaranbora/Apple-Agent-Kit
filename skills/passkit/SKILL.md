---
name: passkit
description: Route PassKit implementation tasks to the correct Knowledge Contracts -- pass library querying/adding, .pkpass/pass.json content and required fields, the add-to-Wallet UI flow, pass updates and the app-vs-server push boundary, and Apple Pay payment requests plus authorization/result handling. Use when calling PKPassLibrary.isPassLibraryAvailable()/containsPass(_:)/passes()/passes(of:)/addPasses(_:withCompletionHandler:), authoring pass.json (formatVersion/passTypeIdentifier/serialNumber/teamIdentifier/organizationName/description, boardingPass/coupon/eventTicket/storeCard/generic, PassFields, barcodes, locations/relevantDates), inspecting a pass with PKPass(data:), presenting PKAddPassesViewController/PKAddPassButton, wiring webServiceURL/authenticationToken, or building/presenting Apple Pay with PKPaymentRequest, PKPaymentAuthorizationController/PKPaymentAuthorizationViewController, PayWithApplePayButton/PKPaymentButton, PKPaymentAuthorizationControllerDelegate, PKPayment/PKPaymentToken, or PKPaymentAuthorizationResult. v1 is app-side Wallet-pass and Apple Pay Swift API only -- no server-side pass signing/certificate/Pass Type ID setup, no PKAddSecureElementPassViewController/NFC/secure-element passes, no PKPassPersonalization, and no Apple Pay server-side merchant validation/token decryption/payment-processor integration. Triggers on PassKit, PKPassLibrary, PKPass, pass.json, Wallet pass, PKAddPassesViewController, PKAddPassButton, webServiceURL, PKPaymentRequest, PKPaymentAuthorizationController, PKPaymentAuthorizationViewController, PayWithApplePayButton, PKPaymentButton, PKPayment, PKPaymentToken, Apple Pay.
id: skill.passkit.foundations
title: PassKit — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: PassKit
routes: [knowledge.passkit.pass-library-and-authorization, knowledge.passkit.pass-content-and-required-fields, knowledge.passkit.adding-passes-ui, knowledge.passkit.pass-updates-and-push-registration, knowledge.passkit.apple-pay-payment-request, knowledge.passkit.apple-pay-authorization-and-result-handling]
related: []
last_updated: 2026-08-08
---

# PassKit — Foundations Skill

## Purpose

Route PassKit implementation tasks to the minimum required PassKit
Knowledge Contracts. v1 scope is app-side Wallet-pass querying/adding,
`.pkpass`/`pass.json` structure, the add-to-Wallet UI flow, the
app-vs-server pass-update boundary, and building/presenting Apple Pay --
not server-side pass signing or certificate management, not
NFC/secure-element passes, not pass personalization, and not Apple Pay's
server-side merchant validation or token decryption.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/passkit/.

-   Calling `PKPassLibrary.isPassLibraryAvailable()`/`containsPass(_:)`/`passes()`/`passes(of:)`; adding held passes with `addPasses(_:withCompletionHandler:)`; or asking why there's no EventKit-style permission gate -> pass-library-and-authorization.md
-   Authoring or validating `pass.json` (`formatVersion`/`passTypeIdentifier`/`serialNumber`/`teamIdentifier`/`organizationName`/`description`, the `boardingPass`/`coupon`/`eventTicket`/`storeCard`/`generic` style keys, `PassFields` groups, `barcodes`, `locations`/`relevantDates`); or inspecting a pass with `PKPass(data:)` -> pass-content-and-required-fields.md
-   Presenting `PKAddPassesViewController`/`PKAddPassButton`; checking `canAddPasses()`; or the delegate/dismissal pattern -> adding-passes-ui.md
-   Wiring `webServiceURL`/`authenticationToken`; or understanding the device-registration/push/update-fetch protocol and why the app registers for no PassKit push type -> pass-updates-and-push-registration.md
-   Building `PKPaymentRequest`; checking `canMakePayments()`/`canMakePayments(usingNetworks:)`; or choosing `PayWithApplePayButton`/`PKPaymentButton` and `PKPaymentAuthorizationController`/`PKPaymentAuthorizationViewController` -> apple-pay-payment-request.md
-   Implementing `PKPaymentAuthorizationControllerDelegate`; handling `PKPayment`/`PKPaymentToken` in `didAuthorizePayment(_:handler:)`; returning `PKPaymentAuthorizationResult`; or dismissing via `paymentAuthorizationControllerDidFinish(_:)` -> apple-pay-authorization-and-result-handling.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/passkit/ — do not guess or fall back to general
knowledge. Server-side pass signing, certificate management, and the
Pass Type ID/Apple Developer portal setup process are out of scope
entirely -- not app-side Swift code, not planned as a contract here.
`PKAddSecureElementPassViewController` and NFC/secure-element-backed
passes (transit cards, car keys, driver's-license-in-Wallet) are out of
scope entirely -- a distinct, more specialized subsystem, not yet built.
`PKPassPersonalization` (the transit-pass personalization flow) is out
of scope entirely -- niche, not yet built. Apple Pay server-side merchant
validation, payment-token decryption, and payment-processor integration
are out of scope entirely -- report that this boundary exists and is
server-side rather than routing to a contract here or fabricating a
client-side decryption API.
