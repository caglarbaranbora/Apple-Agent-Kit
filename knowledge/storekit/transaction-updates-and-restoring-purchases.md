# Transaction Updates and Restoring Purchases

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.storekit.transaction-updates-and-restoring-purchases
artifact_type: knowledge
title: Transaction Updates and Restoring Purchases
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the Transaction.updates AsyncSequence listener task started early to catch purchases/renewals/refunds/revocations outside the direct purchase flow, and AppStore.sync() as the explicit user-initiated Restore Purchases mechanism.
domain: StoreKit
tags:
  - storekit
  - in-app-purchase
  - transaction-updates
  - restore-purchases
references:
  - https://developer.apple.com/documentation/storekit/transaction/updates
  - https://developer.apple.com/documentation/storekit/appstore/sync()
depends_on:
  - knowledge.storekit.transaction-verification-and-entitlements
related:
  - knowledge.storekit.product-loading-and-purchase
  - knowledge.storekit.subscription-status-and-renewal-info
  - knowledge.app-store-review-guidelines.restore-purchases
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent starts a
`Transaction.updates` listener task early (e.g. at app launch) to catch
transactions that happen outside the direct purchase flow, and how it
calls `AppStore.sync()` as the explicit, user-initiated "Restore
Purchases" mechanism — the API mechanics only. *Why* a restore mechanism
is required by App Review is owned by
`knowledge.app-store-review-guidelines.restore-purchases`; this contract
does not restate that rule.

## Scope

### Included

-   Starting a `Transaction.updates` listener `Task` early (e.g. app launch)
-   What `Transaction.updates` emits: Ask to Buy completions, offer code redemptions, App Store purchases, cross-device purchases, renewals, refunds, revocations
-   Verifying and finishing transactions received via the listener (applies Rules from `transaction-verification-and-entitlements`)
-   Calling `AppStore.sync()` as the explicit, user-initiated restore mechanism

### Excluded

-   *Why* a restore mechanism is required, and its discoverability/UI placement — see `knowledge.app-store-review-guidelines.restore-purchases`
-   Loading products and initiating a purchase — see `product-loading-and-purchase`
-   Verifying a `VerificationResult<Transaction>` and calling `finish()` — see `transaction-verification-and-entitlements`
-   Subscription renewal state (`RenewalInfo`, `renewalState`) — see `subscription-status-and-renewal-info`
-   Legacy StoreKit 1 (`SKPaymentQueue`, `SKProduct`, `SKPaymentTransaction`) — out of v1 scope
-   Server-side receipt validation / App Store Server API — out of v1 scope
-   StoreKit Configuration file test setup in Xcode — out of v1 scope

## Rules

### Rule 1

Agents MUST start a listener `Task` iterating `Transaction.updates` as
early as possible in the app's lifecycle (e.g. at app launch, before any
purchase UI is shown) and keep it running for the process lifetime. Per
Apple's documentation, this sequence "receives transactions that occur
outside of the app, such as Ask to Buy transactions, offer code
redemptions, and purchases that customers make in the App Store," as
well as renewals, refunds, and revocations, and "emits transactions that
customers complete in your app on another device." Starting it late
risks missing transactions that arrive before the listener attaches.

### Rule 2

Agents MUST verify and finish each transaction received from
`Transaction.updates` using the same rules as any other transaction (see
`transaction-verification-and-entitlements`) — a transaction from this
sequence is not exempt from verification just because it did not
originate from a direct `purchase()` call in this process.

### Rule 3

Agents MUST NOT rely on `Transaction.updates` alone as the user-facing
restore mechanism — it is a passive background listener, not something a
user can trigger on demand. Per Apple's documentation, "note that after
a successful in-app purchase on the same device, StoreKit returns the
transaction through" the updates sequence too, but the listener has no
way to force a check against the App Store on demand.

### Rule 4

Agents MUST call `AppStore.sync()` (`async throws`) only in direct
response to an explicit user action (e.g. a "Restore Purchases" button),
never automatically or speculatively on every launch. Per Apple's
documentation, "in regular operations, there's no need to call [sync()].
StoreKit automatically keeps up to date transaction information and
subscription status available to your app," and calling it forces a
re-authentication round-trip with the App Store that is unnecessary
outside the rare case a user suspects the app isn't showing all their
transactions.

## Compliant Example

```swift
func startTransactionListener() -> Task<Void, Never> {
    Task { // Started at app launch, before purchase UI appears.
        for await result in Transaction.updates {
            await handleVerifiedPurchase(result) // Same rules as any transaction.
        }
    }
}

// Wired to a "Restore Purchases" button:
func restorePurchases() async throws {
    try await AppStore.sync() // Only on explicit user action.
}
```
Listener task started at app launch (Rule 1) and reuses transaction handling (Rule 2); `AppStore.sync()` is called only from a button action (Rule 4). (Rules 1, 2, 4)

## Non-Compliant Example

```swift
struct PurchaseView: View {
    var body: some View {
        Text("Store")
            .task {
                try? await AppStore.sync() // Called unconditionally on every appearance.
            }
    }
}
// No Transaction.updates listener exists anywhere in the app.
```
Calls `AppStore.sync()` unconditionally on view appearance rather than on explicit user action (Rule 4), and has no `Transaction.updates` listener to catch out-of-band transactions at all (Rule 1).

## Dependencies

- `knowledge.storekit.transaction-verification-and-entitlements` —
  transactions received via `Transaction.updates` are verified and
  finished using the same rules as transactions from a direct purchase.

## References

-   [Apple Developer — Transaction.updates](https://developer.apple.com/documentation/storekit/transaction/updates)
-   [Apple Developer — AppStore.sync()](https://developer.apple.com/documentation/storekit/appstore/sync())
