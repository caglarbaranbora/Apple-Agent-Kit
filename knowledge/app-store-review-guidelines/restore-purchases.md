# Restore Purchases

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.restore-purchases
type: knowledge
title: Restore Purchases
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement to provide a restore mechanism for restorable in-app purchases, and the non-expiration rule for purchased credits/currencies, per guideline 3.1.1.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - in-app-purchase
  - restore
  - monetization
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.digital-goods-iap
updated: 2026-07-31
```

## Intent

This contract defines how an agent must let users recover previously
purchased non-consumable/subscription IAP items, and the rule against
letting purchased in-game currency expire (guideline 3.1.1).

## Scope

### Included

-   Restore-mechanism requirement for non-consumable/subscription IAP
-   Non-expiration rule for purchased credits/currencies
-   Discoverability of the restore action

### Excluded

-   Initial purchase/unlock requirement itself — see `digital-goods-iap`

## Rules

### Rule 1

Agents MUST implement a restore-purchases mechanism for any
non-consumable or auto-renewable/non-renewing subscription IAP so users
can recover purchases after reinstall or a device change.

### Rule 2

Agents MUST NOT cause credits or in-game currencies purchased via IAP
to expire.

### Rule 3

Agents SHOULD expose the restore action from a discoverable location in
the app's purchase/settings UI, not only triggered implicitly on
launch.

## Compliant Example

-   ✓ Settings screen has a "Restore Purchases" button that calls the platform's restore-completed-transactions API and re-unlocks owned non-consumables. (Rules 1, 3)

## Non-Compliant Example

-   ✗ App offers a non-consumable "remove ads" purchase with no way to restore it after reinstalling the app. (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 3.1.1 In-App Purchase](https://developer.apple.com/app-store/review/guidelines/)
