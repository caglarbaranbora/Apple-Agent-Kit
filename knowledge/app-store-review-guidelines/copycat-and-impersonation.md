# Copycat and Impersonation

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.copycat-and-impersonation
artifact_type: knowledge
title: Copycat and Impersonation
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 4.1's three clauses — that copying a popular app's name or UI with minor changes is a rejection in its own right and not only an intellectual property risk, that submitting an app impersonating another app or service is a Developer Code of Conduct violation carrying removal from the Apple Developer Program rather than only from the App Store, and that another developer's icon, brand, or product name may not appear in an app's icon or name without that developer's approval.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - design
  - branding
  - metadata
references:
  - https://developer.apple.com/app-store/review/guidelines/#4.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.spam-duplicate-apps
  - knowledge.app-store-review-guidelines.description-accuracy
last_updated: 2026-08-08
```

## Intent

This contract defines the line between building something similar and
building a copy. Its central claim is that 4.1's three clauses carry
different consequences — (a) is a rejection, (b) reaches the developer
account rather than the submission, and (c) is a flat prohibition with a
single named cure, the other developer's approval — so treating 4.1 as one
undifferentiated "don't copy" rule loses the part that ends a Developer
Program membership.

## Scope

### Included

-   Cloning an existing app's name, UI, or concept
-   Impersonating another app or service, and where that consequence lands
-   Another developer's icon, brand, or product name in an icon or app name

### Excluded

-   Multiple near-identical apps from one developer — see
    `spam-duplicate-apps`
-   Third-party content, trademarks, and licensing generally — see
    `third-party-content-licensing`
-   Apple's own brand, products, and interfaces — see
    `apple-trademarks-and-product-confusion`
-   Whether a UI is well designed — owned by `human-interface-guidelines`

## Rules

### Rule 1

Agents MUST NOT reproduce another app's name or interface with minor
changes. Per Apple: "Don't simply copy the latest popular app on the App
Store, or make some minor changes to another app's name or UI and pass it
off as your own." Apple gives two grounds beyond infringement — "it makes
the App Store harder to navigate and just isn't fair to your fellow
developers" — so the rule applies even where no intellectual property claim
would succeed.

### Rule 2

Agents MUST NOT build an app that impersonates another app or service, and
MUST treat this as categorically heavier than a rejection. Per Apple,
submitting such apps "is considered a violation of the Developer Code of
Conduct and may result in removal from the Apple Developer Program." The
exposure is the account, not the submission, so it is not correctable by
resubmitting.

### Rule 3

Agents MUST NOT place another developer's icon, brand, or product name in
the app's own icon or name. Per Apple: "You cannot use another developer's
icon, brand, or product name in your app's icon or name, without approval
from the developer." Compatibility phrasing does not exempt it — an app
named for the service it connects to is using that service's product name in
its name.

### Rule 4

Agents MUST hold the named approval before shipping, not after being asked
for it. 4.1(c)'s only cure is "approval from the developer", so the question
at review time is whether permission exists, and an unanswered request is
not permission.

### Rule 5

Agents MUST apply 4.1 to visual identity as well as to text. An icon that
copies another app's silhouette, palette, and glyph is "minor changes to
another app's… UI" under 4.1(a) regardless of whether the app names its
model anywhere, because the App Store surface a customer confuses is the
icon.

## Compliant Example

-   ✓ A third-party client is named for its own brand, describes the service it connects to in the description body, and uses an original icon. (Rules 3, 5)
-   ✓ A partner integration ships only after written approval to use the partner's wordmark in the app name is on file. (Rule 4)
-   ✓ A note-taking app takes inspiration from a popular competitor's model but ships its own navigation, naming, and icon. (Rules 1, 5)

## Non-Compliant Example

-   ✗ An app is named "Instagrom" with an icon reproducing the original's gradient and camera glyph. (Rules 1, 3, 5)
-   ✗ A client app calls itself the official app of a service it has no relationship with. (Rule 2)
-   ✗ A team ships with a competitor's product name in the app name while a permission request sits unanswered. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 4.1 Copycats](https://developer.apple.com/app-store/review/guidelines/#4.1)
