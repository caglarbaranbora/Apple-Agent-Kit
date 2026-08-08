# Apple Trademarks and Product Confusion

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.apple-trademarks-and-product-confusion
artifact_type: knowledge
title: Apple Trademarks and Product Confusion
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines guideline 5.2.4 and 5.2.5 — that an app may not suggest Apple is its source, supplier, or endorser and that the Editor's Choice badge is applied by Apple rather than by the developer, that an app may not look confusingly similar to an Apple product, interface, or app, that Apple emoji may not be included in apps, extensions, keyboards, or Sticker packs, that iTunes and Apple Music previews may not be used for entertainment value and require a link back, and that Activity rings and Apple Weather data carry their own display and attribution rules.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - legal
  - branding
  - apple-trademarks
references:
  - https://developer.apple.com/app-store/review/guidelines/#5.2.4
  - https://developer.apple.com/app-store/review/guidelines/#5.2.5
depends_on: []
related:
  - knowledge.app-store-review-guidelines.third-party-content-licensing
  - knowledge.app-store-review-guidelines.copycat-and-impersonation
last_updated: 2026-08-08
```

## Intent

This contract defines what an app may say and show about Apple. Its central
claim is that these two clauses catch things an agent does for good reasons:
the assets that look most native are Apple's own, and the phrasing that
sounds most reassuring is the phrasing that implies endorsement. Both are
rejections, and both are usually written without any intent to trade on
Apple's brand.

## Scope

### Included

-   Implying Apple is a source, supplier, or endorser, and the Editor's Choice badge
-   Resembling an Apple product, interface, or app
-   Apple emoji, iTunes and Apple Music previews, Activity rings, Apple Weather data

### Excluded

-   Non-Apple third-party material and licensing — see
    `third-party-content-licensing`
-   Copying another *developer's* app — see `copycat-and-impersonation`
-   How to draw a native-feeling interface — owned by
    `human-interface-guidelines`
-   SF Symbols usage terms — owned by `sf-symbols`

## Rules

### Rule 1

Agents MUST NOT imply Apple's involvement or endorsement. Per Apple: "Don't
suggest or imply that Apple is a source or supplier of the App, or that
Apple endorses any particular representation regarding quality or
functionality." Phrases such as "Apple-approved", "built with Apple", or
"as featured by Apple" in a description, onboarding screen, or marketing
string are the usual form.

### Rule 2

Agents MUST NOT draw or ship an Editor's Choice badge. Per Apple: "If your
app is selected as an 'Editor's Choice,' Apple will apply the badge
automatically." The badge is an App Store surface Apple controls, so
reproducing it in a screenshot or in the app is both a false claim and an
unauthorized asset.

### Rule 3

Agents MUST NOT make an app that resembles an Apple product or app. Per
Apple: "Don't create an app that appears confusingly similar to an existing
Apple product, interface (e.g. Finder), app (such as the App Store, iTunes
Store, or Messages) or advertising theme." A file browser styled as Finder
or a chat app styled as Messages is in scope even where every asset is
original.

### Rule 4

Agents MUST NOT include Apple emoji. Per Apple, "apps and extensions,
including third-party keyboards and Sticker packs, may not include Apple
emoji." The clause names extensions explicitly, so a keyboard or sticker
pack that bundles rendered Apple emoji images violates it — rendering the
system font at runtime on Apple's own platform is not the same as shipping
the artwork.

### Rule 5

Agents MUST respect the rules attached to specific Apple content. Music
previews from iTunes or Apple Music "may not be used for their entertainment
value (e.g. as the background music to a photo collage or the soundtrack to
a game)", and where previews are offered the app "must display a link to the
corresponding music in iTunes or Apple Music". Activity rings "should not
visualize Move, Exercise, or Stand data in a way that resembles the Activity
control", and Apple Weather data "should follow the attribution requirements
provided in the WeatherKit documentation."

## Compliant Example

-   ✓ The description says "Designed for iPhone" and makes no claim about Apple's approval. (Rule 1)
-   ✓ Screenshots show the app's own UI with no App Store chrome or award badges. (Rule 2)
-   ✓ A fitness app charts Move and Exercise data as bars and lines rather than as concentric rings. (Rule 5)
-   ✓ A music discovery app plays Apple Music previews and links each track to Apple Music. (Rule 5)

## Non-Compliant Example

-   ✗ An onboarding screen reads "Apple-certified secure storage". (Rule 1)
-   ✗ The App Store screenshots carry a hand-drawn "Editor's Choice" ribbon. (Rule 2)
-   ✗ A file manager reproduces Finder's sidebar, icon set, and window chrome. (Rule 3)
-   ✗ A sticker pack ships PNGs of Apple emoji. (Rule 4)
-   ✗ A photo-collage app uses a 30-second Apple Music preview as the export's background track. (Rule 5)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 5.2.4 Apple Endorsements](https://developer.apple.com/app-store/review/guidelines/#5.2.4)
-   [Apple App Review Guidelines — 5.2.5 Apple Products](https://developer.apple.com/app-store/review/guidelines/#5.2.5)
