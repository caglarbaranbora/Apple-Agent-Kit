# StoreKit

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.storekit
artifact_type: reference
title: StoreKit
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's StoreKit 2 async/await documentation, scoped to this domain's v1.
domain: StoreKit
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/storekit/appstore/sync()
https://developer.apple.com/documentation/storekit/product
https://developer.apple.com/documentation/storekit/product/products(for:)
https://developer.apple.com/documentation/storekit/product/purchase(options:)
https://developer.apple.com/documentation/storekit/product/purchaseresult
https://developer.apple.com/documentation/storekit/product/subscriptioninfo/grouplevel
https://developer.apple.com/documentation/storekit/product/subscriptioninfo/renewalinfo
https://developer.apple.com/documentation/storekit/product/subscriptioninfo/renewalstate
https://developer.apple.com/documentation/storekit/product/subscriptioninfo/status-swift.struct
https://developer.apple.com/documentation/storekit/transaction
https://developer.apple.com/documentation/storekit/transaction/currententitlements
https://developer.apple.com/documentation/storekit/transaction/finish()
https://developer.apple.com/documentation/storekit/transaction/updates
https://developer.apple.com/documentation/storekit/verificationresult

## Purpose

Reference index for Apple's StoreKit 2 async/await documentation, scoped
to this domain's v1: loading `Product` instances via
`Product.products(for:)`; initiating a purchase via
`product.purchase(options:)` and handling every `Product.PurchaseResult`
case; verifying a `VerificationResult<Transaction>` and reading
`Transaction.currentEntitlements`; finishing a transaction via
`transaction.finish()`; the `Transaction.updates` listener task and
`AppStore.sync()` restore mechanism; and subscription status via
`Product.SubscriptionInfo.Status`/`RenewalInfo`/`renewalState`, including
same-subscription-group upgrade/downgrade behavior.

Out of scope for v1: legacy StoreKit 1 (`SKPaymentQueue`, `SKProduct`,
`SKPaymentTransaction`); server-side receipt validation and the App
Store Server API; StoreKit Configuration file test setup in Xcode. The
App Review compliance angle — the requirement to use IAP to unlock
content, prohibited alternative unlock mechanisms, loot-box odds
disclosure, the requirement to implement a restore mechanism, and the
non-expiration rule for purchased currencies — is owned by the
`app-store-review-guidelines` domain, not this one; this domain owns the
API implementation angle only.

## Primary Topics

- Product loading and purchase initiation
- Transaction verification and entitlements
- Transaction updates and restoring purchases
- Subscription status and renewal info

## Used By

- knowledge/storekit/product-loading-and-purchase.md ([[knowledge/storekit/product-loading-and-purchase]])
- knowledge/storekit/transaction-verification-and-entitlements.md ([[knowledge/storekit/transaction-verification-and-entitlements]])
- knowledge/storekit/transaction-updates-and-restoring-purchases.md ([[knowledge/storekit/transaction-updates-and-restoring-purchases]])
- knowledge/storekit/subscription-status-and-renewal-info.md ([[knowledge/storekit/subscription-status-and-renewal-info]])
