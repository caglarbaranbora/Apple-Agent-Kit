# Locale and Language Resolution

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.localization.locale-and-language-resolution
artifact_type: knowledge
title: Locale and Language Resolution
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines where a Locale comes from and how the system resolves which localization an app runs in -- Locale.current as a snapshot of the app's resolved locale rather than the device's, autoupdatingCurrent and its equality caveat, preferredLanguages versus preferredLocalizations, the modern Locale.Language and Locale.Region split that replaced the deprecated string properties, development region, and the lproj fallback chain.
domain: Localization
tags:
  - locale
  - preferred-languages
  - bundle-localizations
  - development-region
  - language-resolution
references:
  - https://developer.apple.com/documentation/foundation/locale/current
  - https://developer.apple.com/documentation/foundation/locale/autoupdatingcurrent
  - https://developer.apple.com/documentation/foundation/locale/preferredlanguages
  - https://developer.apple.com/documentation/foundation/locale/region-swift.property
  - https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations
  - https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations(from:)
  - https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledevelopmentregion
  - https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts
  - https://developer.apple.com/library/archive/qa/qa1828/_index.html
  - https://developer.apple.com/videos/play/wwdc2022/10110/
  - https://developer.apple.com/videos/play/wwdc2024/10185/
depends_on: []
related:
  - knowledge.localization.localized-string-apis
  - knowledge.localization.localized-resources-and-infoplist
  - knowledge.foundation.date-time-formatting
  - knowledge.foundation.measurement-and-unit-formatting
last_updated: 2026-08-08
```

## Intent

This contract governs where a `Locale` comes from, what it actually represents, and how the system picks which localization an app runs in. Its central claim is that `Locale.current` describes the *app's resolved* locale, not the user's preferences -- a distinction that silently corrupts analytics, server requests, and content selection when ignored.

## Scope

### Included

- `Locale.current` vs. `Locale.autoupdatingCurrent`, the three inputs defining both, and the equality caveat
- `Locale.preferredLanguages` vs. `Bundle.preferredLocalizations` vs. `Bundle.localizations`, and `Bundle.preferredLocalizations(from:)`
- `Locale.Language`/`Locale.Region` and the deprecation of the older string properties
- `CFBundleDevelopmentRegion`/`Bundle.developmentLocalization`, Base localization's constraint, and the `.lproj` fallback chain
- Per-app language settings, the absence of an API to set them, and choosing identifiers at the right specificity

### Excluded

- Passing a `Locale` to a formatter to produce a date, number, or measurement string -- owned by the `foundation` domain
- The `locale:` parameter on the localized-string APIs -- see `localized-string-apis`
- Bundle resource lookup for non-string resources -- see `localized-resources-and-infoplist`; detecting writing direction to lay out an interface -- see `layout-direction-and-rtl-apis`

## Rules

### Rule 1

Agents MUST NOT read `Locale.current` to determine what language the *user* prefers, because it reports the locale the app resolved to. Per Apple's documentation, both `Locale.current` and `Locale.autoupdatingCurrent` are defined by "The current system locale. / Any app-specific locale choice made in the Settings app. / The availability of the preferred locale in the app," with the worked consequence: "if the person using an app has set their device to use a Spanish-language locale, but the app only supports English, this value returns an English locale." For the user's actual preferences, agents MUST use `Locale.preferredLanguages` -- "A list of the user's preferred languages."

### Rule 2

Agents MUST treat `Locale.current` as a snapshot and MUST use `Locale.autoupdatingCurrent` for any long-lived object that must follow settings changes. Per Apple's documentation, `Locale.current` is "A locale representing the user's region settings at the time the property is read," and "A locale instance obtained this way does not change even when the person using the device changes language or region settings." `Locale.autoupdatingCurrent` is "A locale which tracks the user's current preferences," but agents MUST NOT rely on it to trigger a refresh: "Although the locale obtained here automatically follows the latest language and region settings, it provides no indication when the settings change."

### Rule 3

Agents MUST NOT compare an autoupdating locale for equality with a fixed one, and MUST NOT mutate it. Per Apple's documentation: "The autoupdating `Locale` only compares as equal to another autoupdating `Locale`," and "If mutated, this `Locale` no longer tracks the user's preferences." Caches keyed on a `Locale`, `Equatable` view diffing, and equality assertions in tests are all affected.

### Rule 4

Agents MUST use `Locale.language` and `Locale.region` rather than the older string properties, which are deprecated at this domain's baseline. Per Apple's documentation, `Locale.languageCode` and `Locale.regionCode` are deprecated as of iOS 16.0 / macOS 13.0 / watchOS 9.0. Agents MUST NOT assume `Locale.region` equals the language's region: per Apple's documentation it "corresponds to the `rg` key of the Unicode BCP 47 extension. For locale instances created with the `rg` specifier (such as `en-GB@rg=US`)… this property represents the custom region. Otherwise, it represents the language's region."

### Rule 5

Agents MUST NOT treat a short `preferredLocalizations` result as an error, and MUST use `preferredLocalizations(from:)` to match an externally-supplied language list rather than comparing language codes by hand. Per Apple's documentation, `preferredLocalizations` "does not return all localizations in preference order but only those from which `NSBundle` would get localized content, typically either a single non-region-specific localization or a region-specific localization followed by a corresponding non-region-specific localization as a fallback," and "clients who want all localizations in preference order can make repeated calls, each time taking the top localizations out of the list." Per Apple's WWDC22 session "Building global apps: Localization by example," when choosing among server-provided languages "the device has all the knowledge about which languages the user prefers, so you don't have to check and compare them yourselves."

### Rule 6

Agents MUST set `CFBundleDevelopmentRegion` to the language the app's source strings are actually written in, because it is the terminal fallback. Per Apple's documentation, it is "The default language and region for the bundle, as a language ID. The system uses this key as the language if it can't locate a resource for the user's preferred language." Per Apple's technical Q&A "How iOS Determines the Language For Your App," the system walks the user's preferred languages in order, falls back from a regional variant to its generic language, and uses `CFBundleDevelopmentRegion` only when no preferred language matches; with Base Localization, `CFBundleDevelopmentRegion` must match the language used in `Base.lproj`.

### Rule 7

Agents MUST NOT attempt to set the app's language programmatically, because no supported API exists. Per Apple's WWDC24 session "Build multilingual-ready apps," the per-app language row appears automatically -- "For apps that support multiple localizations, if the user has more than one language in their Language & Region settings, the language setting is automatically shown" -- and the app's only supported affordances are the `UIPrefersShowingLanguageSettings` Info.plist key and deep-linking to Settings via `UIApplication.openSettingsURLString`.

### Rule 8

Agents SHOULD declare localizations at the specificity the app actually ships. Per Apple's documentation: "if you only support English and it is American English, choose English (United States) (en-US) instead of English (en)."

## Compliant Example

```swift
let userLanguages = Locale.preferredLanguages          // Rule 1: user preference

// Rule 5: let the system match against a server-supplied list.
let serverLanguages = ["en", "de", "ar", "ja"]
let bestMatch = Bundle.preferredLocalizations(from: serverLanguages).first

// Rule 2: a long-lived formatter must follow settings changes.
let priceFormatter = NumberFormatter()
priceFormatter.numberStyle = .currency
priceFormatter.locale = .autoupdatingCurrent

// Rule 4: modern accessors; region and language.region are distinct.
let language = Locale.current.language.languageCode
let region = Locale.current.region
```

## Non-Compliant Example

```swift
// violates Rule 1 -- reports the app's localization coverage back to the
// server, not the user's preference. An Arabic-speaking user of an
// English-only build is recorded as an English speaker.
analytics.send(userLanguage: Locale.current.identifier)

// violates Rule 2 -- a snapshot at init. After the user changes region in
// Settings, this formatter keeps the old one for the process's lifetime.
let formatter = DateFormatter()
formatter.locale = Locale.current

// violates Rule 3 -- never true, even when both describe the same locale.
if Locale.autoupdatingCurrent == Locale.current { useFastPath() }

// violates Rule 4 -- deprecated since iOS 16, and collapses the distinction
// between the language's region and an explicit rg region override.
let region = Locale.current.regionCode
```
Treats the app's resolved locale as the user's preference (Rule 1); snapshots `Locale.current` into a long-lived formatter so it never follows settings changes (Rule 2); compares an autoupdating locale against a fixed one, which the documentation says can never be equal (Rule 3); and uses a property deprecated at this baseline that also conflates two distinct notions of region (Rule 4).

## Dependencies

None within this domain. Cross-references the `foundation` domain's `date-time-formatting` and `measurement-and-unit-formatting` contracts, which own passing the resulting `Locale` to a formatter -- this contract owns only where that `Locale` comes from.

## References

- [Apple Developer — Locale.current](https://developer.apple.com/documentation/foundation/locale/current) · [Locale.autoupdatingCurrent](https://developer.apple.com/documentation/foundation/locale/autoupdatingcurrent)
- [Apple Developer — Locale.preferredLanguages](https://developer.apple.com/documentation/foundation/locale/preferredlanguages) · [Locale.region](https://developer.apple.com/documentation/foundation/locale/region-swift.property)
- [Apple Developer — Bundle.preferredLocalizations](https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations) · [preferredLocalizations(from:)](https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations(from:))
- [Apple Developer — CFBundleDevelopmentRegion](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledevelopmentregion) · [Choosing localization regions and scripts](https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts)
- [Apple Developer — QA1828: How iOS Determines the Language For Your App](https://developer.apple.com/library/archive/qa/qa1828/_index.html)
- [WWDC22 — Building global apps: Localization by example](https://developer.apple.com/videos/play/wwdc2022/10110/) · [WWDC24 — Build multilingual-ready apps](https://developer.apple.com/videos/play/wwdc2024/10185/)
