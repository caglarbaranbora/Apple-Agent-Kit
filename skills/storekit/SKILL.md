---
name: storekit
description: Route StoreKit 2 in-app purchase implementation tasks to the correct Knowledge Contracts -- product loading, purchase initiation, transaction verification, entitlements, transaction updates, restoring purchases, and subscription status/renewal info. Use when calling Product.products(for:), product.purchase(), handling Product.PurchaseResult, checking VerificationResult, reading Transaction.currentEntitlements, calling transaction.finish(), listening to Transaction.updates, calling AppStore.sync(), or reading Product.SubscriptionInfo.Status/RenewalInfo/renewalState. v1 is StoreKit 2 async/await API only -- no legacy StoreKit 1 (SKPaymentQueue/SKProduct/SKPaymentTransaction), no server-side receipt validation or App Store Server API, no StoreKit Configuration file test setup. Triggers on StoreKit, Product.products, product.purchase, PurchaseResult, VerificationResult, currentEntitlements, transaction.finish, Transaction.updates, AppStore.sync, restore purchases, SubscriptionInfo.Status, RenewalInfo, renewalState, subscription group, in-app purchase, IAP.
id: skill.storekit.foundations
title: StoreKit — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: StoreKit
routes: [knowledge.storekit.product-loading-and-purchase, knowledge.storekit.transaction-verification-and-entitlements, knowledge.storekit.transaction-updates-and-restoring-purchases, knowledge.storekit.subscription-status-and-renewal-info]
related: []
last_updated: 2026-08-06
---

# StoreKit — Foundations Skill

## Purpose

Route StoreKit 2 in-app purchase implementation tasks to the minimum
required StoreKit Knowledge Contracts. v1 scope is the modern StoreKit 2
async/await API surface only — no legacy StoreKit 1, no server-side
receipt validation or App Store Server API, no StoreKit Configuration
file test setup in Xcode.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/storekit/.

-   Loading products with `Product.products(for:)`, initiating a purchase with `product.purchase()`, or handling `Product.PurchaseResult` (`.success`/`.userCancelled`/`.pending`) -> product-loading-and-purchase.md
-   Checking a `VerificationResult` for `.verified`/`.unverified`, reading `Transaction.currentEntitlements`, or calling `transaction.finish()` -> transaction-verification-and-entitlements.md
-   The `Transaction.updates` listener task or calling `AppStore.sync()` to restore purchases -> transaction-updates-and-restoring-purchases.md
-   Reading `Product.SubscriptionInfo.Status`/`RenewalInfo`/`renewalState`, or same-subscription-group upgrade/downgrade behavior -> subscription-status-and-renewal-info.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/storekit/ — do not guess or fall back to general
knowledge. Legacy StoreKit 1 (`SKPaymentQueue`, `SKProduct`,
`SKPaymentTransaction`), server-side receipt validation, the App Store
Server API, and StoreKit Configuration file test setup are deferred to
future scope, not yet built — report that explicitly rather than
answering from general knowledge (see docs/architecture/domain-map.md).
The App Review compliance angle — the requirement to use IAP to unlock
content, prohibited alternative unlock mechanisms, loot-box odds
disclosure, the restore-mechanism requirement, and the non-expiration
rule for purchased currencies — is owned by the
`app-store-review-guidelines` Skill, not this one.
