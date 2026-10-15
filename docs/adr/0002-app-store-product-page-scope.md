# ADR-0002: App Store Product Page Domain Scope

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: adr.0002
artifact_type: adr
title: App Store Product Page Domain Scope
version: 1.0.0
status: Approved
domain: App Store Product Page
related: []
last_updated: 2026-10-15
```

## Context

Apple's "App Store asset best practices and resources" page
(https://developer.apple.com/app-store/asset-best-practices/), introduced on
2026-08-05, and the App Store Connect Help pages that went live with creative
assets on 2026-10-05 (header, search results, In-App Event media; iPhone Duo
screenshot sizes) had no coverage in this repository. The research is in
`docs/research/2026-10-app-store-asset-best-practices.md`; the decisions were
made in a maintainer review on 2026-10-15 and are listed in
`docs/superpowers/plans/2026-10-15-app-store-product-page-domain.md`.

Two constraints shaped the scope. `app-store-review-guidelines` already owned
screenshot and preview accuracy (2.3.3, 2.3.4), and its Reference was at the
98-line limit `reference-spec.md` sets. And most of Apple's asset guidance is
advice, not a review rule.

## Decision

Create `app-store-product-page` as its own domain: App Store Connect asset
specifications and Apple's asset guidance for iOS and iPadOS visual assets
(screenshots, app previews, creative assets, In-App Event media), as
`domain-map.md`'s Tier 1 row states. Product page text fields are Deferred;
other platforms' asset specifications are Excluded.

## Consequences

- Angle split with `app-store-review-guidelines`: it owns what gets rejected,
  this domain owns specifications and how to make assets effective.
- `references/apple/app-store-product-page.md` indexes the App Review URLs that
  `app-store-review-guidelines` Contracts cite for 2.3.3 (help page), 2.3.4,
  2.3.8 and 2.3.10, because the other Reference has no room. Indexing is by URL
  and many-to-many, so this is valid; a reader looking for those URLs in
  `references/apple/app-store-review-guidelines.md` will not find them there.
- "Don't" items on the asset page that no guideline states (URLs, copyright
  symbols, discounts) are encoded as MUST NOT, following Apple's wording, with
  each Contract's Intent saying they are asset guidance, not rejection reasons.
- Only craft guidance an agent can check is encoded (SHOULD); subjective
  guidance is Excluded.
- The iPhone Duo April 2027 requirement is encoded as the specification page's
  SDK-bound MUST plus a SHOULD for the broader What's New wording.
- `workflow.app-store-submission` gains no step; its Excluded list points here.

## Verification Log

- 2026-10-15: initial scope recorded; 9 Knowledge Contracts and
  `skill.app-store-product-page.foundations` shipped.
- 2026-10-15: `app-store-review-guidelines` slice — `screenshots-accuracy`
  1.1.0 (majority-in-use), new `metadata-age-rating` (2.3.8) and
  `other-platform-references` (2.3.10); their App Review URLs indexed in
  `references/apple/app-store-product-page.md` per Consequences.
