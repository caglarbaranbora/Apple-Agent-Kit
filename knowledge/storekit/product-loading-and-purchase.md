# Product Loading and Purchase

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.storekit.product-loading-and-purchase
type: knowledge
title: Product Loading and Purchase
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines loading Product instances via Product.products(for:), initiating a purchase via product.purchase(options:), and handling all three Product.PurchaseResult cases.
domain: StoreKit
tags:
  - storekit
  - in-app-purchase
  - product
  - purchase
references:
  - https://developer.apple.com/documentation/storekit/product
  - https://developer.apple.com/documentation/storekit/product/products(for:)
  - https://developer.apple.com/documentation/storekit/product/purchase(options:)
  - https://developer.apple.com/documentation/storekit/product/purchaseresult
depends_on: []
related:
  - knowledge.storekit.transaction-verification-and-entitlements
  - knowledge.storekit.transaction-updates-and-restoring-purchases
  - knowledge.storekit.subscription-status-and-renewal-info
  - knowledge.app-store-review-guidelines.digital-goods-iap
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent loads `Product` instances
for a set of product identifiers and initiates a purchase, and how it
must branch on every case of the resulting `Product.PurchaseResult` —
the StoreKit 2 entry point into the purchase flow, before any
transaction-verification or entitlement concern applies.

## Scope

### Included

-   Loading products via `Product.products(for:)`
-   Initiating a purchase via `product.purchase(options:)`
-   Handling all three `Product.PurchaseResult` cases: `.success(let verification)`, `.userCancelled`, `.pending`
-   Handling thrown errors from both calls

### Excluded

-   Verifying the `VerificationResult<Transaction>` carried by `.success` and finishing the transaction — see `transaction-verification-and-entitlements`
-   Listening for transactions that occur outside this direct purchase flow and restoring purchases — see `transaction-updates-and-restoring-purchases`
-   Subscription-specific status and renewal info — see `subscription-status-and-renewal-info`
-   Legacy StoreKit 1 (`SKPaymentQueue`, `SKProduct`, `SKPaymentTransaction`) — out of v1 scope
-   Server-side receipt validation / App Store Server API — out of v1 scope
-   StoreKit Configuration file test setup in Xcode — out of v1 scope
-   The App Review requirement to use IAP to unlock content — see `knowledge.app-store-review-guidelines.digital-goods-iap`

## Rules

### Rule 1

Agents MUST load `Product` instances via
`Product.products(for:)`, passing the collection of product identifiers
configured in App Store Connect — never construct or fabricate a
`Product` value directly. Per Apple's documentation, "if any identifiers
are invalid or the App Store can't find them, the App Store excludes
them from the return value," so the returned array can be shorter than
the requested identifier list and callers must handle that.

### Rule 2

Agents MUST call `product.purchase(options:)` to initiate a purchase —
an `async throws` method that is also `@MainActor`-isolated, so it must
be called from a context that can await main-actor isolation (e.g. from
a SwiftUI button action). This call brings up the system payment sheet;
the method itself can throw for system-related errors, so the call site
MUST be wrapped in `try`/`catch`.

### Rule 3

Agents MUST branch on all three `Product.PurchaseResult` cases and MUST
NOT treat any case other than `.success` as a completed purchase:

-   `.success(let verification)` — a purchase occurred; the associated
    `VerificationResult<Transaction>` MUST be verified before granting
    any entitlement (see `transaction-verification-and-entitlements`).
-   `.userCancelled` — the user dismissed the payment sheet; treat as a
    normal, silent no-op, not an error condition.
-   `.pending` — the purchase requires further action outside the app
    (e.g. Ask to Buy, or a payment method that needs approval); the
    entitlement MUST NOT be granted yet. The eventual outcome arrives
    later via `Transaction.updates` (see
    `transaction-updates-and-restoring-purchases`).

### Rule 4

Agents MUST NOT surface every thrown error from `purchase(options:)` to
the user as if it were a hard failure — a thrown error still requires
`catch`, but distinguishing a user-facing message from a silent retry is
an app-specific UX decision this contract does not prescribe.

## Compliant Example

```swift
func buy(productID: String) async throws {
    let products = try await Product.products(for: [productID])
    guard let product = products.first else { return }

    switch try await product.purchase() {
    case .success(let verification):
        // Verify before unlocking -- see transaction-verification-and-entitlements.
        await handleVerifiedPurchase(verification)
    case .userCancelled:
        break // Silent no-op, not an error.
    case .pending:
        break // Outcome arrives later via Transaction.updates.
    @unknown default:
        break
    }
}
```
Loads via `products(for:)` (Rule 1), calls `purchase()` under `try` (Rule 2), and branches on every case without granting entitlement for `.pending` (Rule 3). (Rules 1, 2, 3)

## Non-Compliant Example

```swift
func buy(productID: String) async {
    let products = try? await Product.products(for: [productID])
    let product = products??.first
    if let result = try? await product?.purchase(), case .success = result {
        unlockContent() // Also unlocks on .pending, and swallows all thrown errors.
    }
}
```
Swallows thrown errors with `try?` (Rule 4) and only checks for `.success` loosely, without branching on `.userCancelled`/`.pending` or verifying the transaction (Rule 3).

## Dependencies

None.

## References

-   [Apple Developer — Product](https://developer.apple.com/documentation/storekit/product)
-   [Apple Developer — Product.products(for:)](https://developer.apple.com/documentation/storekit/product/products(for:))
-   [Apple Developer — Product.purchase(options:)](https://developer.apple.com/documentation/storekit/product/purchase(options:))
-   [Apple Developer — Product.PurchaseResult](https://developer.apple.com/documentation/storekit/product/purchaseresult)
