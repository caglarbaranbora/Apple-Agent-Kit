# Third-Party Content Licensing

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.third-party-content-licensing
artifact_type: knowledge
title: Third-Party Content Licensing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 5.2.1 through 5.2.3 — that protected third-party material may not appear in an app without permission and that the submitting entity must be the one holding the rights, that using or displaying a third-party service's content requires being permitted under that service's terms of use, that saving, converting, or downloading media from third-party sources needs explicit authorization from those sources, and that in both cases Apple may require the authorization to be produced on request.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - legal
  - intellectual-property
  - licensing
references:
  - https://developer.apple.com/app-store/review/guidelines/#5.2.1
  - https://developer.apple.com/app-store/review/guidelines/#5.2.2
  - https://developer.apple.com/app-store/review/guidelines/#5.2.3
depends_on: []
related:
  - knowledge.app-store-review-guidelines.apple-trademarks-and-product-confusion
  - knowledge.app-store-review-guidelines.copycat-and-impersonation
last_updated: 2026-08-08
```

## Intent

This contract defines what an app may include that it did not create. Its
central claim is that 5.2 is an evidence rule as much as a permission rule:
Apple states twice that "authorization must be provided upon request", so
the compliance artifact is a document someone can produce, and an
integration built against a public endpoint with no written terms coverage
fails at the moment it is questioned rather than at the moment it ships.

## Scope

### Included

-   Protected third-party material in the app or its metadata
-   Building against a third-party service's content under its terms of use
-   Saving, converting, or downloading media from third-party sources

### Excluded

-   Apple's own brand, products, interfaces, and media — see
    `apple-trademarks-and-product-confusion`
-   Cloning another app's name or UI — see `copycat-and-impersonation`
-   User-supplied content and its moderation — see
    `user-generated-content-moderation`

## Rules

### Rule 1

Agents MUST NOT include protected third-party material without permission,
in the binary or in the metadata. Per Apple: "Don't use protected
third-party material such as trademarks, copyrighted works, or patented
ideas in your app without permission, and don't include misleading, false,
or copycat representations, names, or metadata in your app bundle or
developer name." Bundled fonts, icon sets, sound effects, and sample data
are all covered.

### Rule 2

Agents MUST ensure the submitting entity is the rights holder. Per Apple:
"Apps should be submitted by the person or legal entity that owns or has
licensed the intellectual property and other relevant rights." An agency
submitting under its own developer account on a client's behalf is the
common failure, and the fix is the account, not the app.

### Rule 3

Agents MUST check a third-party service's terms of use before building
against it. Per Apple: "If your app uses, accesses, monetizes access to, or
displays content from a third-party service, ensure that you are
specifically permitted to do so under the service's terms of use." A public
or undocumented endpoint being reachable is not permission — "monetizes
access to" means a paid tier over free public data is in scope.

### Rule 4

Agents MUST NOT build saving, converting, or downloading of media from
third-party sources without explicit authorization from those sources. Per
Apple, apps "should not facilitate illegal file sharing or include the
ability to save, convert, or download media from third-party sources (e.g.
Apple Music, YouTube, SoundCloud, Vimeo, etc.) without explicit
authorization from those sources." Apple adds that even streaming "may also
violate Terms of Use, so be sure to check before your app accesses those
services."

### Rule 5

Agents MUST be able to produce the authorization. Apple states "authorization
must be provided upon request" under both 5.2.2 and 5.2.3, so a verbal
agreement, an unanswered email, or a partner relationship with no written
scope is not evidence. The artifact should exist before submission, not be
assembled during an appeal.

## Compliant Example

-   ✓ Every bundled font, icon set, and audio asset has a license file recorded alongside it. (Rule 1)
-   ✓ The client's own developer account submits the app the agency built. (Rule 2)
-   ✓ An integration ships against the service's documented public API under its published terms, with the terms archived. (Rules 3, 5)
-   ✓ A media app plays third-party content through the provider's sanctioned SDK and offers no download or export. (Rule 4)

## Non-Compliant Example

-   ✗ A game ships a sprite sheet found online with no license recorded. (Rule 1)
-   ✗ An app scrapes a site's undocumented JSON endpoint and sells access as a paid tier. (Rule 3)
-   ✗ A "video saver" offers to download YouTube clips for offline viewing. (Rule 4)
-   ✗ A partner integration relies on a verbal agreement, and nothing can be produced when Apple asks. (Rule 5)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 5.2.1 Generally](https://developer.apple.com/app-store/review/guidelines/#5.2.1)
-   [Apple App Review Guidelines — 5.2.2 Third-Party Sites/Services](https://developer.apple.com/app-store/review/guidelines/#5.2.2)
-   [Apple App Review Guidelines — 5.2.3 Audio/Video Downloading](https://developer.apple.com/app-store/review/guidelines/#5.2.3)
