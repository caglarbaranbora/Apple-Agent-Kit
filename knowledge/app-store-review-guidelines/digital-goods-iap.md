# Digital Goods In-App Purchase

Status: Draft Version: 0.2.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.digital-goods-iap
artifact_type: knowledge
title: Digital Goods In-App Purchase
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement to use Apple's in-app purchase system to unlock digital content or functionality, per guideline 3.1.1.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - in-app-purchase
  - monetization
references:
  - https://developer.apple.com/app-store/review/guidelines/#3.1.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.external-payment-links
  - knowledge.app-store-review-guidelines.restore-purchases
last_updated: 2026-08-08
```

## Intent

This contract defines when an agent must use StoreKit in-app purchase
to unlock digital content or functionality, and which alternative
unlock mechanisms are explicitly disallowed (guideline 3.1.1).

## Scope

### Included

-   Requirement to use IAP for unlocking features/content/currency
-   Prohibited alternative unlock mechanisms
-   Permitted IAP-based tipping
-   Loot-box odds disclosure requirement

### Excluded

-   External payment link/button restrictions — see `external-payment-links`
-   Restore-purchases mechanism requirement — see `restore-purchases`

## Rules

### Rule 1

Agents MUST use in-app purchase (StoreKit) to unlock any feature,
functionality, subscription, in-game currency, level, or premium
content within the app.

### Rule 2

Agents MUST NOT implement an app-owned mechanism to unlock
content/functionality instead of IAP — license keys, AR markers, QR
codes, cryptocurrency, and cryptocurrency wallets are explicitly
disallowed as unlock mechanisms.

### Rule 3

Agents MAY use IAP currencies to let users "tip" the developer or a
digital content provider inside the app.

### Rule 4

Agents MUST disclose the odds of receiving each item type, before
purchase, for any app offering loot boxes or other randomized
virtual-item purchases.

## Compliant Example

-   ✓ Premium tier is unlocked via a StoreKit non-consumable purchase. (Rule 1)

## Non-Compliant Example

-   ✗ App sells a "premium unlock" QR code on the developer's website that users scan in-app to unlock paid features, bypassing IAP. (Rule 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 3.1.1 In-App Purchase](https://developer.apple.com/app-store/review/guidelines/#3.1.1)
