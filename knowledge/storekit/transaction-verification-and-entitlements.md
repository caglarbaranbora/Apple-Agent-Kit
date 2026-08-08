# Transaction Verification and Entitlements

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.storekit.transaction-verification-and-entitlements
artifact_type: knowledge
title: Transaction Verification and Entitlements
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines checking VerificationResult<Transaction> for .verified/.unverified, never trusting an .unverified payload, reading Transaction.currentEntitlements, and calling transaction.finish() after delivering content.
domain: StoreKit
tags:
  - storekit
  - in-app-purchase
  - verification
  - entitlements
references:
  - https://developer.apple.com/documentation/storekit/verificationresult
  - https://developer.apple.com/documentation/storekit/transaction
  - https://developer.apple.com/documentation/storekit/transaction/currententitlements
  - https://developer.apple.com/documentation/storekit/transaction/finish()
depends_on:
  - knowledge.storekit.product-loading-and-purchase
related:
  - knowledge.storekit.transaction-updates-and-restoring-purchases
  - knowledge.storekit.subscription-status-and-renewal-info
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent checks a
`VerificationResult<Transaction>` for cryptographic validity, reads
`Transaction.currentEntitlements` to determine what a user currently
owns, and calls `transaction.finish()` once — the verification and
entitlement-bookkeeping half of the purchase flow, applied uniformly to
transactions from a direct purchase, `Transaction.updates`, or
`Transaction.currentEntitlements` alike.

## Scope

### Included

-   Checking a `VerificationResult<Transaction>` for `.verified`/`.unverified`
-   Never trusting an `.unverified` payload
-   Reading `Transaction.currentEntitlements` to determine current ownership
-   Calling `transaction.finish()` after delivering content
-   The unfinished-transaction rule (finish exactly once, after delivery)

### Excluded

-   Loading products and initiating a purchase — see `product-loading-and-purchase`
-   The `Transaction.updates` listener task and `AppStore.sync()` — see `transaction-updates-and-restoring-purchases`
-   Subscription renewal state (`RenewalInfo`, `renewalState`) — see `subscription-status-and-renewal-info`
-   Legacy StoreKit 1 (`SKPaymentQueue`, `SKProduct`, `SKPaymentTransaction`) — out of v1 scope
-   Server-side receipt validation / App Store Server API — out of v1 scope
-   StoreKit Configuration file test setup in Xcode — out of v1 scope

## Rules

### Rule 1

Agents MUST switch on a `VerificationResult<Transaction>` and check for
`.verified(let transaction)` before treating the transaction as
legitimate. Per Apple's documentation, `.unverified(let transaction, let
error)` carries the `VerificationResult.VerificationError` that explains
why StoreKit's local, on-device cryptographic check of the signed
transaction failed.

### Rule 2

Agents MUST NOT grant an entitlement, unlock content, or otherwise act
on the payload of an `.unverified` result. An `.unverified` payload still
exposes the underlying value and the error via
`case unverified(SignedType, VerificationResult<SignedType>.VerificationError)`,
but reading that value for anything other than diagnostics/logging
treats an unauthenticated payload as trustworthy.

### Rule 3

Agents MUST use `Transaction.currentEntitlements` (an `AsyncSequence`,
`Transaction.Transactions`) to determine what a user currently owns —
per Apple's documentation, it "emits the latest transaction for each
product the customer has an entitlement to," and explicitly excludes
products the App Store has refunded or revoked, and excludes
consumables entirely. Each element is itself a
`VerificationResult<Transaction>` and MUST still be checked per Rule 1.

### Rule 4

Agents MUST call `transaction.finish()` exactly once per transaction,
and only after the purchased content has been delivered or the
purchased service enabled. Per Apple's documentation, for on-demand
resources "don't finish the transaction until the app completes
downloading the resource." An unfinished transaction is re-delivered by
StoreKit on a future launch or via `Transaction.updates`/`currentEntitlements`
— finishing before delivery risks losing the transaction if delivery
then fails.

## Compliant Example

```swift
func handleVerifiedPurchase(_ result: VerificationResult<Transaction>) async {
    switch result {
    case .verified(let transaction):
        await deliverContent(for: transaction.productID)
        await transaction.finish() // Only after delivery.
    case .unverified(_, let error):
        log("Unverified transaction: \(error)") // Not acted on.
    }
}
```
Checks `.verified` before acting (Rule 1), never acts on `.unverified` (Rule 2), and finishes only after delivery (Rule 4). (Rules 1, 2, 4)

## Non-Compliant Example

```swift
func handleVerifiedPurchase(_ result: VerificationResult<Transaction>) async {
    let transaction = switch result {
    case .verified(let t): t
    case .unverified(let t, _): t // Unverified payload used anyway.
    }
    await transaction.finish() // Finished before content is delivered.
    await deliverContent(for: transaction.productID)
}
```
Extracts and uses the transaction from `.unverified` (Rule 2), and finishes before delivering content, risking a lost transaction if delivery fails (Rule 4).

## Dependencies

- `knowledge.storekit.product-loading-and-purchase` — the
  `VerificationResult<Transaction>` verified here is the same value
  carried by `Product.PurchaseResult.success`.

## References

-   [Apple Developer — VerificationResult](https://developer.apple.com/documentation/storekit/verificationresult)
-   [Apple Developer — Transaction](https://developer.apple.com/documentation/storekit/transaction)
-   [Apple Developer — Transaction.currentEntitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements)
-   [Apple Developer — Transaction.finish()](https://developer.apple.com/documentation/storekit/transaction/finish())
