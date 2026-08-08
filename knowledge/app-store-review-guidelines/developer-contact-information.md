# Developer Contact Information

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.developer-contact-information
artifact_type: knowledge
title: Developer Contact Information
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines guideline 1.5's requirement that both the app itself and its App Store Connect Support URL carry an easy way to reach the developer, that the information be accurate and current because inaccuracy "may violate the law in some countries or regions", the heightened expectation for apps used in classrooms, and the separate obligation that Wallet passes carry issuer contact information and be signed with a certificate assigned to the brand owner.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - safety
  - support
  - metadata
references:
  - https://developer.apple.com/app-store/review/guidelines/#1.5
depends_on: []
related:
  - knowledge.app-store-review-guidelines.user-generated-content-moderation
  - knowledge.app-store-review-guidelines.description-accuracy
last_updated: 2026-08-08
```

## Intent

This contract defines where an app must expose a way to reach its
developer. Its central claim is that guideline 1.5 names two places and
requires both — the app and the Support URL — so a support page that exists
only on the web leaves the in-app half unbuilt, and the requirement is the
one metadata rule with a stated legal dimension rather than only a review
one.

## Scope

### Included

-   The two required locations, and what counts as reachable
-   Accuracy and currency of the information, and the classroom case
-   Wallet pass issuer contact information and pass signing

### Excluded

-   The `.pkpass` format and how a pass is built — owned by `passkit`
-   Support-screen layout and wording — owned by
    `human-interface-guidelines` and `style-guide`
-   Contact information as one of guideline 1.2's four required
    mechanisms — see `user-generated-content-moderation`

## Rules

### Rule 1

Agents MUST expose contact information inside the app, not only on the
Support URL. Per Apple: "Make sure your app **and** its Support URL include
an easy way to contact you." A Settings screen, an About screen, or a
Help entry carrying an email address or a contact form satisfies the in-app
half; a link that opens the marketing site's home page does not.

### Rule 2

Agents MUST keep the information accurate and current, and MUST NOT treat a
stale address as a cosmetic defect. Per Apple, failure to include accurate
and up-to-date contact information "not only frustrates customers, but may
violate the law in some countries or regions." This is the rule to check
when an app changes owner, company name, or support vendor.

### Rule 3

Agents MUST treat the requirement as heightened for apps that may be used in
a classroom. Apple names this case explicitly — "this is particularly
important for apps that may be used in the classroom" — so an education or
child-facing app should surface the contact path where a teacher or parent
will find it, not only inside an account section a signed-out user cannot
reach.

### Rule 4

Agents MUST ensure any Wallet pass the app issues carries valid issuer
contact information. Per Apple: "ensure that Wallet passes include valid
contact information from the issuer." A pass is a second surface the app
ships, and it carries its own copy of this obligation.

### Rule 5

Agents MUST NOT sign a Wallet pass with a certificate belonging to anyone
other than the brand owner. Per Apple, passes must be "signed with a
dedicated certificate assigned to the brand or trademark owner of the pass."
An agency or platform signing a client's passes with its own Pass Type ID
violates this even when the client authorized it.

## Compliant Example

-   ✓ Settings → Support shows `support@example.com` and a Contact Us form; the App Store Connect Support URL resolves to a page showing the same address. (Rule 1)
-   ✓ A company rename triggers an audit of the in-app address, the Support URL, and the Privacy Policy URL together. (Rule 2)
-   ✓ A classroom reading app puts Contact Support on the signed-out launch screen, not behind account creation. (Rule 3)
-   ✓ Each issued loyalty pass carries the merchant's phone number and email, and is signed with the merchant's own Pass Type ID. (Rules 4, 5)

## Non-Compliant Example

-   ✗ The only contact route is a Twitter handle in the App Store description. (Rule 1)
-   ✗ The Support URL redirects to the company home page with no support path. (Rule 1)
-   ✗ The in-app support address still points at a vendor the company stopped using a year ago. (Rule 2)
-   ✗ A white-label platform signs every customer's passes with the platform's certificate. (Rule 5)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 1.5 Developer Information](https://developer.apple.com/app-store/review/guidelines/#1.5)
