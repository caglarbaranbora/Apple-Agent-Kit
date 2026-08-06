# Subscription Status and Renewal Info

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.storekit.subscription-status-and-renewal-info
type: knowledge
title: Subscription Status and Renewal Info
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines reading Product.SubscriptionInfo.Status and RenewalInfo, branching on renewalState (.subscribed/.expired/.inBillingRetryPeriod/.inGracePeriod/.revoked), and same-subscription-group upgrade/downgrade behavior.
domain: StoreKit
tags:
  - storekit
  - in-app-purchase
  - subscriptions
  - renewal
references:
  - https://developer.apple.com/documentation/storekit/product/subscriptioninfo/status-swift.struct
  - https://developer.apple.com/documentation/storekit/product/subscriptioninfo/renewalinfo
  - https://developer.apple.com/documentation/storekit/product/subscriptioninfo/renewalstate
  - https://developer.apple.com/documentation/storekit/product/subscriptioninfo/grouplevel
depends_on:
  - knowledge.storekit.transaction-verification-and-entitlements
related:
  - knowledge.storekit.product-loading-and-purchase
  - knowledge.storekit.transaction-updates-and-restoring-purchases
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent reads a
`Product.SubscriptionInfo.Status`, checks its `RenewalInfo` and
`renewalState`, and reasons about upgrade/downgrade behavior between
subscriptions in the same subscription group — the subscription-specific
layer built on top of the generic transaction/entitlement rules.

## Scope

### Included

-   Reading `Product.SubscriptionInfo.Status` (`state`, `renewalInfo`, `transaction`)
-   Branching on `Product.SubscriptionInfo.RenewalState`: `.subscribed`, `.expired`, `.inBillingRetryPeriod`, `.inGracePeriod`, `.revoked`
-   Reading `RenewalInfo` fields relevant to upgrade/downgrade (`currentProductID`, `willAutoRenew`)
-   Same-subscription-group upgrade/downgrade/crossgrade behavior via `groupLevel`

### Excluded

-   Loading products and initiating a purchase — see `product-loading-and-purchase`
-   Verifying a `VerificationResult<Transaction>` and calling `finish()` — see `transaction-verification-and-entitlements`
-   The `Transaction.updates` listener and `AppStore.sync()` — see `transaction-updates-and-restoring-purchases`
-   Legacy StoreKit 1 (`SKPaymentQueue`, `SKProduct`, `SKPaymentTransaction`) — out of v1 scope
-   Server-side receipt validation / App Store Server API — out of v1 scope
-   StoreKit Configuration file test setup in Xcode — out of v1 scope

## Rules

### Rule 1

Agents MUST read subscription state from a `Product.SubscriptionInfo.Status`
value (obtained from `product.subscription.status` or
`SubscriptionInfo.status(for:)`), whose `state` property is a
`Product.SubscriptionInfo.RenewalState` and whose `renewalInfo` and
`transaction` properties are each a `VerificationResult` that MUST be
verified using the same `.verified`/`.unverified` check as any other
transaction (see `transaction-verification-and-entitlements`) before
being trusted.

### Rule 2

Agents MUST branch on all five `Product.SubscriptionInfo.RenewalState`
cases and MUST NOT treat any state other than `.subscribed` as active
paid access: `.subscribed`, `.expired`, `.inBillingRetryPeriod`,
`.inGracePeriod`, `.revoked`. `.inBillingRetryPeriod` and
`.inGracePeriod` both represent a renewal payment problem the system is
still trying to resolve — an agent MAY choose to keep entitlement active
during a grace period per its own product policy, but MUST NOT conflate
either state with `.subscribed` when reporting subscription health.

### Rule 3

Agents MUST use the verified `RenewalInfo`'s `willAutoRenew` and
`currentProductID` to determine what a subscriber will actually be
billed for next — `currentProductID` reflects an already-applied
downgrade/crossgrade scheduled for the next renewal, which can differ
from the product identifier of the currently active transaction.

### Rule 4

Agents MUST treat multiple auto-renewable subscriptions within the same
subscription group as mutually exclusive for a given user — a customer
holds at most one active subscription per group at a time. Per Apple's
documentation on `groupLevel`, "ranking your subscriptions determines
the upgrade, downgrade, and crossgrade paths available," where a lower
`groupLevel` value represents a higher level of service; moving to a
lower `groupLevel` value is an upgrade, and moving to a higher one is a
downgrade. Agents MUST NOT assume a user can hold simultaneous active
entitlements to two products in the same group.

## Compliant Example

```swift
func isActivelySubscribed(_ status: Product.SubscriptionInfo.Status) -> Bool {
    switch status.state {
    case .subscribed, .inGracePeriod:
        return true // Grace period treated as active per this app's policy.
    case .expired, .inBillingRetryPeriod, .revoked:
        return false
    @unknown default:
        return false
    }
}
```
Branches on every `RenewalState` case explicitly, with `.inGracePeriod` handled as a distinct, deliberate policy choice rather than conflated with `.subscribed`. (Rules 2)

## Non-Compliant Example

```swift
func isActivelySubscribed(_ status: Product.SubscriptionInfo.Status) -> Bool {
    return status.state != .expired // Treats .revoked and billing-retry as active.
}
```
Treats every state except `.expired` as active, silently granting access during `.revoked` (a refunded/revoked subscription) and `.inBillingRetryPeriod`. (Rule 2)

## Dependencies

- `knowledge.storekit.transaction-verification-and-entitlements` —
  `RenewalInfo` and `transaction` on `Status` are each a
  `VerificationResult` verified with the same rules.

## References

-   [Apple Developer — Product.SubscriptionInfo.Status](https://developer.apple.com/documentation/storekit/product/subscriptioninfo/status-swift.struct)
-   [Apple Developer — Product.SubscriptionInfo.RenewalInfo](https://developer.apple.com/documentation/storekit/product/subscriptioninfo/renewalinfo)
-   [Apple Developer — Product.SubscriptionInfo.RenewalState](https://developer.apple.com/documentation/storekit/product/subscriptioninfo/renewalstate)
-   [Apple Developer — Product.SubscriptionInfo.groupLevel](https://developer.apple.com/documentation/storekit/product/subscriptioninfo/grouplevel)
