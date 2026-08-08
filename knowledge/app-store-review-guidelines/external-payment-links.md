# External Payment Links

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.external-payment-links
artifact_type: knowledge
title: External Payment Links
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the prohibition on in-app buttons, links, or calls to action that direct users to purchase digital goods outside of in-app purchase, per guideline 3.1.1(a).
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - in-app-purchase
  - external-links
  - monetization
references:
  - https://developer.apple.com/app-store/review/guidelines/#3.1.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.digital-goods-iap
last_updated: 2026-08-08
```

## Intent

This contract defines when an app's UI may or may not include a call
to action directing users to purchase digital goods outside of IAP
(guideline 3.1.1(a)), and the narrower US-storefront exception.

## Scope

### Included

-   Prohibition on in-app external-purchase calls to action (non-US storefronts)
-   US storefront External Purchase Link Entitlement exception
-   Outside-app communications about alternative purchasing methods

### Excluded

-   Underlying IAP-usage requirement itself — see `digital-goods-iap`

## Rules

### Rule 1

Agents MUST NOT include buttons, external links, or other calls to
action in the app or its metadata that direct customers to a purchasing
mechanism other than in-app purchase, for storefronts outside the
United States.

### Rule 2

Agents MAY include such external purchase links only on the United
States storefront, and only through Apple's StoreKit External Purchase
Link Entitlement where applicable.

### Rule 3

Agents MAY send communications outside the app (e.g., email, SMS) to
the existing user base about alternative purchasing methods — this is
distinct from an in-app call to action and is not restricted by Rule 1.

## Compliant Example

-   ✓ iOS app sold globally has no "Buy on our website" button in its UI; the developer emails existing subscribers about a website discount. (Rules 1, 3)

## Non-Compliant Example

-   ✗ App shown on a non-US storefront includes an in-app "Subscribe on our site and save 10%" button linking out to a web checkout. (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 3.1.1 In-App Purchase](https://developer.apple.com/app-store/review/guidelines/#3.1.1)
