# Localization Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `localization` domain (1 Reference, 6 Knowledge Contracts, 1 native Skill) covering how an app's user-facing strings and resources are extracted, stored, varied, and resolved across languages and regions — String Catalogs and extraction, the localized-string API surface, plural/device variation, `Locale` and language resolution, layout-direction/RTL APIs, and localized resources/Info.plist — per `docs/superpowers/specs/2026-08-07-localization-domain-design.md`, replacing the `Language, terminology` placeholder row in `docs/architecture/domain-map.md`. This is the 17th and final Tier 2 domain — completing this task closes out all of Tier 2.

**Architecture:** Mirrors every prior domain exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. Subject matter is Swift/Xcode API usage, so Compliant/Non-Compliant Examples use fenced Swift code blocks, matching `networking`, `local-authentication`, and `testing`.

**Baseline:** Xcode 16+, iOS 17+ for the API surface. String Catalogs impose no deployment-target cost (`.xcstrings` compiles to `.strings`/`.stringsdict` at build time), so the catalog half of this domain is gated on Xcode, not the OS. Xcode 16 specifically because "Don't Translate", stale-string warnings, format-specifier diagnostics, and the `xcstringstool` replacement for the deprecated `genstrings` do not exist in Xcode 15. Individual symbols carry their own availability and it is noted where it matters — `Locale.Language`/`Locale.Region`/`Locale.Language.characterDirection` are iOS 16+, and `Locale.languageCode`/`regionCode`/`characterDirection(forLanguage:)` are **deprecated as of iOS 16**, already dead at this baseline.

**Evidence rule (binding on every task):** Every Rule must quote an official Apple source — developer.apple.com documentation, a WWDC session transcript, or an Apple archived guide — in the `Per Apple's documentation:` form. Do **not** introduce claims derived from running local tooling. In particular: Apple publishes **no `.xcstrings` JSON schema**, so describe the catalog through its editor affordances and public APIs, never through JSON field names (`sourceLanguage`, `extractionState`, `stringUnit`, …). Do not assert the device-class identifier list, `NSStringDeviceSpecificRuleType`, or build-validator behavior — none is documented.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Before Starting

- [ ] Confirm you are on branch `feature/localization-domain` in the `localization-domain` worktree.
- [ ] Re-read `docs/superpowers/specs/2026-08-07-localization-domain-design.md` — the four cross-domain boundaries and the Excluded list are binding.
- [ ] Note the two open sourcing caveats carried into Task 7: Info.plist localization is documented only in a WWDC23 transcript and an archived 2009 reference, and no Apple source states in those words that permission usage strings *must* be localized.

---

## Task 1: Reference — `references/apple/localization.md`

**Files:**
- Create: `references/apple/localization.md`

- [ ] **Step 1: Create the file**

```markdown
# Localization

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/xcode/localization
https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog
https://developer.apple.com/documentation/xcode/preparing-your-apps-text-for-translation
https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization
https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals
https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions
https://developer.apple.com/documentation/xcode/adding-resources-to-localizations
https://developer.apple.com/documentation/xcode/localizing-assets-in-a-catalog
https://developer.apple.com/documentation/xcode/localizing-package-resources
https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts
https://developer.apple.com/documentation/xcode/previewing-localizations
https://developer.apple.com/documentation/xcode/testing-localizations-when-running-your-app
https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes
https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes
https://developer.apple.com/documentation/swift/string/init(localized:table:bundle:locale:comment:)
https://developer.apple.com/documentation/swift/string/init(localized:defaultvalue:table:bundle:locale:comment:)
https://developer.apple.com/documentation/swift/string/init(localized:)
https://developer.apple.com/documentation/swift/string/localizationvalue
https://developer.apple.com/documentation/foundation/localizedstringresource
https://developer.apple.com/documentation/foundation/nslocalizedstring(_:tablename:bundle:value:comment:)
https://developer.apple.com/documentation/foundation/attributedstring
https://developer.apple.com/documentation/swiftui/localizedstringkey
https://developer.apple.com/documentation/swiftui/text/init(_:tablename:bundle:comment:)
https://developer.apple.com/documentation/swiftui/text/init(verbatim:)
https://developer.apple.com/documentation/foundation/locale/current
https://developer.apple.com/documentation/foundation/locale/autoupdatingcurrent
https://developer.apple.com/documentation/foundation/locale/preferredlanguages
https://developer.apple.com/documentation/foundation/locale/language-swift.property
https://developer.apple.com/documentation/foundation/locale/region-swift.property
https://developer.apple.com/documentation/foundation/locale/language-swift.struct/characterdirection
https://developer.apple.com/documentation/foundation/locale/characterdirection(forlanguage:)
https://developer.apple.com/documentation/foundation/nslocale/languagedirection
https://developer.apple.com/documentation/foundation/bundle
https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations
https://developer.apple.com/documentation/foundation/bundle/localizations
https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations(from:)
https://developer.apple.com/documentation/foundation/bundle/developmentlocalization
https://developer.apple.com/documentation/foundation/bundle/localizedstring(forkey:value:table:)
https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledevelopmentregion
https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledisplayname
https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundlename
https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundleallowmixedlocalizations
https://developer.apple.com/documentation/packagedescription/package/defaultlocalization
https://developer.apple.com/documentation/swiftui/layoutdirection
https://developer.apple.com/documentation/swiftui/environmentvalues/layoutdirection
https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:)
https://developer.apple.com/documentation/swiftui/horizontalalignment/leading
https://developer.apple.com/documentation/uikit/uiview/semanticcontentattribute
https://developer.apple.com/documentation/uikit/uisemanticcontentattribute
https://developer.apple.com/documentation/uikit/uiview/effectiveuserinterfacelayoutdirection
https://developer.apple.com/documentation/uikit/uiview/userinterfacelayoutdirection(for:relativeto:)
https://developer.apple.com/documentation/uikit/uiimage/imageflippedforrighttoleftlayoutdirection()
https://developer.apple.com/documentation/uikit/creating-custom-symbol-images-for-your-app
https://developer.apple.com/videos/play/wwdc2023/10155/
https://developer.apple.com/videos/play/wwdc2022/10107/
https://developer.apple.com/videos/play/wwdc2022/10110/
https://developer.apple.com/videos/play/wwdc2024/10185/
https://developer.apple.com/library/archive/qa/qa1828/_index.html
https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html
https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/SupportingRight-To-LeftLanguages/SupportingRight-To-LeftLanguages.html
https://developer.apple.com/library/archive/documentation/Xcode/Reference/xcode_ref-Asset_Catalog_Format/ImageSetType.html

## Purpose

Reference index for Apple's localization documentation, scoped to this domain's v1: String Catalog (`.xcstrings`) file mechanics and compiler-driven string extraction, including the literal-argument requirement extraction depends on, translator comments, the catalog's translation states, explicit keys vs. value-as-key, and manually-managed entries; the localized-string API surface (`String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey` and SwiftUI's implicit `Text` literal localization, `AttributedString(localized:)`, and the remaining role of `NSLocalizedString`); plural and device variation, the CLDR plural categories and their language-dependence, substitutions, and the legacy `.stringsdict` form; `Locale` and language resolution (`current` vs. `autoupdatingCurrent`, `preferredLanguages` vs. `preferredLocalizations`, the `Locale.Language`/`Locale.Region` split, development region, and the `.lproj` fallback chain); layout-direction and RTL APIs across SwiftUI and UIKit including SF Symbols' name-driven mirroring; and localized resources (`InfoPlist.xcstrings`, `.lproj` structure, asset-catalog localization, Swift-package `defaultLocalization`/`Bundle.module`, and non-main-bundle lookup).

Baseline is Xcode 16+ with an iOS 17+ API surface. String Catalogs themselves carry no deployment-target requirement — per WWDC23, `.xcstrings` compiles to `.strings` and `.stringsdict` at build time, so "you can start using String Catalogs right away without having to update your minimum deployment target."

Out of scope for v1: the Xcode project-configuration side of localization (adding a project language, target localization settings, and the `.xcloc`/XLIFF export-and-import round trip with translators), which is `xcode`'s territory and deferred to a future `xcode` expansion; the iOS 18 Translation framework (`TranslationSession`, `.translationTask`, `.translationPresentation`), a real and documented capability deliberately excluded because it translates *user content at runtime* rather than shipping the app's own text pre-translated, and requires iOS 18; source-copy wording, capitalization, and international representation/formatting rules (owned by `style-guide`); date/time/number/measurement formatting mechanics (owned by `foundation`); RTL *visual-design* guidance (owned by `human-interface-guidelines`); App Store Connect localized metadata; APNs `loc-key`/`loc-args` server payloads (already out of scope for `usernotifications`); App Shortcuts phrase and `AppEnum` localization (owned by `app-intents`); and macOS/watchOS/tvOS-specific behavior.

Sourcing note: Apple publishes no schema reference for the `.xcstrings` file format — WWDC23 describes it only as "JSON files under the hood." This reference and the contracts that use it therefore describe the String Catalog through its editor affordances and public APIs, never through JSON field names. Separately, Info.plist localization is not covered by any of the 24 articles in Apple's current Xcode Localization documentation hub; its only current-era source is the WWDC23 transcript and its only prose specification is the archived Info.plist Key Reference listed above.

## Primary Topics

- String Catalog file mechanics, build-time extraction, the "Use Compiler to Extract Swift Strings" (`SWIFT_EMIT_LOC_STRINGS`) requirement, translator comments, translation states (New / Needs Review / Translated / Stale), "Don't Translate", explicit keys vs. value-as-key, and manually-managed entries
- `String(localized:)` overloads, `String.LocalizationValue`, `LocalizedStringResource` deferred resolution, `LocalizedStringKey` and SwiftUI implicit `Text` localization, `Text(verbatim:)`, `AttributedString(localized:)` and Markdown-in-translations, format specifiers and positional arguments, `NSLocalizedString`
- Plural variation and the CLDR categories (`zero`/`one`/`two`/`few`/`many`/`other`, with `other` required and the applicable set language-dependent), device variation, substitutions, `.stringsdict` (`NSStringLocalizedFormatKey`, `NSStringFormatSpecTypeKey`, `NSStringFormatValueTypeKey`), and the distinction from `^[…](inflect: true)` runtime inflection
- `Locale.current` vs. `Locale.autoupdatingCurrent`, the three inputs that define both, `Locale.preferredLanguages` vs. `Bundle.preferredLocalizations` vs. `Bundle.localizations`, `Bundle.preferredLocalizations(from:)`, `Locale.Language`/`Locale.Region`, `CFBundleDevelopmentRegion`/`Bundle.developmentLocalization`, the `.lproj` fallback chain, and per-app language settings
- SwiftUI `LayoutDirection`/`\.layoutDirection`/`flipsForRightToLeftLayoutDirection(_:)`, leading/trailing over left/right, UIKit `semanticContentAttribute`/`UISemanticContentAttribute`/`effectiveUserInterfaceLayoutDirection`, `UIImage.imageFlippedForRightToLeftLayoutDirection()`, asset-catalog `language-direction`, SF Symbols name-driven mirroring, `Locale.Language.characterDirection`/`Locale.LanguageDirection`, and the RTL pseudolanguages
- `InfoPlist.xcstrings`/`InfoPlist.strings`, `CFBundleDisplayName`/`CFBundleName`, `.lproj` structure and Base localization, per-asset catalog localization, Swift-package `defaultLocalization`/`Bundle.module`, and `Bundle.localizedString(forKey:value:table:)`

## Used By

- knowledge/localization/string-catalogs-and-extraction.md ([[knowledge/localization/string-catalogs-and-extraction]])
- knowledge/localization/localized-string-apis.md ([[knowledge/localization/localized-string-apis]])
- knowledge/localization/plural-and-device-variations.md ([[knowledge/localization/plural-and-device-variations]])
- knowledge/localization/locale-and-language-resolution.md ([[knowledge/localization/locale-and-language-resolution]])
- knowledge/localization/layout-direction-and-rtl-apis.md ([[knowledge/localization/layout-direction-and-rtl-apis]])
- knowledge/localization/localized-resources-and-infoplist.md ([[knowledge/localization/localized-resources-and-infoplist]])
- skills/localization/SKILL.md ([[skills/localization/SKILL]])
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py references/apple/localization.md --type reference
```

---

## Task 2: Knowledge Contract — `string-catalogs-and-extraction`

**Files:**
- Create: `knowledge/localization/string-catalogs-and-extraction.md`

- [ ] **Step 1: Create the file**

```markdown
# String Catalogs and Extraction

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.string-catalogs-and-extraction
type: knowledge
title: String Catalogs and Extraction
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how a String Catalog (.xcstrings) collects an app's localizable text -- compiler-driven extraction at build time and the string-literal requirement it depends on, translator comments, the New/Needs Review/Translated/Stale states, explicit keys versus value-as-key, manually-managed entries for dynamic keys, and the per-table migration boundary with legacy .strings files.
domain: Localization
tags:
  - string-catalog
  - xcstrings
  - extraction
  - translation-state
  - localization-key
references:
  - https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog
  - https://developer.apple.com/documentation/xcode/preparing-your-apps-text-for-translation
  - https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes
  - https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes
  - https://developer.apple.com/videos/play/wwdc2023/10155/
depends_on: []
related:
  - knowledge.localization.localized-string-apis
  - knowledge.localization.plural-and-device-variations
updated: 2026-08-07
```

## Intent

This contract governs how an app's localizable text gets *into* a String Catalog and what the catalog's bookkeeping means -- build-time extraction, keys, comments, and translation states. It does not cover which API to call to read a localized string back out; that is `localized-string-apis`.

## Scope

### Included

- The `.xcstrings` String Catalog as the current authoring format, and its per-table relationship to legacy `.strings`/`.stringsdict`
- Build-time, compiler-driven extraction and the "Use Compiler to Extract Swift Strings" build setting it requires
- The string-literal requirement that extraction depends on, and the documented remedy when a key genuinely cannot be a literal
- `comment:` as translator context, including disambiguating heteronyms
- Translation states: New, Needs Review, Translated, Stale -- and what moves a string between them
- Explicit keys with an separate default value, versus using the development-language value as the key
- Manually-managed entries and "Don't Translate"

### Excluded

- Which localized-string API to call and its parameters -- see `localized-string-apis`
- Plural, device, and substitution variations inside a catalog entry -- see `plural-and-device-variations`
- The `.xcstrings` file's internal JSON structure -- Apple publishes no schema for it; this contract describes the catalog through the Xcode editor and the public APIs only
- Adding a language to the project, target localization settings, and `.xcloc`/XLIFF export-and-import -- Xcode project configuration, deferred to the `xcode` domain
- Localizing Info.plist keys and non-string resources -- see `localized-resources-and-infoplist`

## Rules

### Rule 1

Agents MUST rely on a build to populate a String Catalog rather than hand-adding ordinary source-derived entries, and MUST ensure compiler-based extraction is enabled. Per Apple's documentation: "To populate your string catalog with the localizable text from your app, choose Product > Build. Xcode discovers the localizable strings in your app and adds them to string catalogs in your project automatically." Per Apple's WWDC23 session "Discover String Catalogs": "String Catalogs make use of powerful technology in the Swift compiler in order to extract localizable Swift strings. For this reason, be sure to enable the build setting Use Compiler to Extract Swift Strings." Note that Xcode's automatic handling of the underlying `SWIFT_EMIT_LOC_STRINGS` setting changed: per Apple's Xcode 16 release notes, Xcode now sets it "at the project level when adding a new String Catalog or migrating a .strings or .stringsdict file… Xcode would previously do this at the target level and only upon migration."

### Rule 2

Agents MUST pass string *literals* to localizable APIs, because extraction is a compile-time read of the source and cannot resolve variables. Per Apple's documentation for `NSLocalizedString`: "The values for `key`, `tableName`, `value`, and `comment` must be string literal values. Xcode can read these values from source code to automatically create localization tables when exporting localizations, but it doesn't resolve string variables." The Swift APIs enforce part of this through their types -- `comment` is declared `StaticString?`, and the explicit-key overload of `String(localized:)` takes `key: StaticString`.

### Rule 3

When a key genuinely cannot be a literal, agents MUST add the entry to the catalog and mark it manually managed rather than assuming a runtime-resolvable expression will reach translators. Per Apple's WWDC23 session, manual entries are "useful for strings whose keys are either dynamically constructed in code or perhaps originate from a database," and "Manually-managed strings will never be updated or removed by Xcode when syncing localizations after a build."

### Rule 4

Agents MUST supply a `comment:` describing how the string appears to the user, and MUST give distinct keys and comments to identical words with different meanings. Per Apple's documentation, the parameter "provides the translator with some context about the localized string's presentation to the user." Apple's own worked example distinguishes a noun from a verb using the keys `"book-tag-title"` (comment: "noun: A label attached to literary items in the library.") and `"book-button-title"` (comment: "verb: Title of the button that makes a reservation.").

### Rule 5

Agents SHOULD use the explicit-key form when the development-language string is ambiguous, and SHOULD prefer it for text expected to be reworded, because editing the source string invalidates every existing translation. Per Apple's documentation: "This is useful if the localizable string in your development language is ambiguous. For example *call* in English can be a noun or a verb," motivating keys such as `CALL_NOUN` and `CALL_VERB`. Per Apple's WWDC23 session, the default key is the value -- "The key is a unique identifier for the string, often equivalent to the string itself" -- and "Anytime the source string changes, the translations will be marked for review," so a copy edit under value-as-key demotes all languages to Needs Review at once.

### Rule 6

Agents MUST read the catalog's four states as bookkeeping about the *translation*, not about the source. Per Apple's WWDC23 session: **New** "indicates that a string hasn't yet been translated into the selected language"; **Needs Review** "indicates that the string requires the localizer's attention because the value might need to be changed," resolved by choosing "Mark as Reviewed"; strings that are translated "show a green checkmark… This indicates that no further action is needed"; and **Stale** "indicates that the string could no longer be found in code."

### Rule 7

Agents MUST NOT infer that an absent Stale entry means nothing was deleted, because removal is handled asymmetrically. Per Apple's WWDC23 session: "If the string hasn't yet been translated, Xcode will remove it for you. However, if you've already provided translations for a string and then remove it, Xcode will instead leave it alone and mark it as Stale." Per Apple's Xcode 16 release notes, stale entries are now also surfaced at build time: "Warnings are now emitted by the String Catalog editor for stale strings. Fix-Its are provided to remove the string if you no longer need it or to manage manually if you'd like to keep it around."

### Rule 8

Agents MUST NOT place a String Catalog and a same-named legacy file in one target, and MUST migrate per table rather than wholesale. Per Apple's Xcode 15 release notes: "The build system will now consistently produce an error if a String Catalog coexists with .strings or .stringsdict files of the same name, within the same target." Per Apple's WWDC23 session, partial migration is the intended path -- "String Catalogs can coexist with the legacy formats, so I can choose to migrate the Localizable table whenever I'm ready" -- via the file's "Migrate to String Catalog" action.

## Compliant Example

```swift
// Value-as-key: the English text is the key. Fine for stable, unambiguous copy.
let title = String(
    localized: "Recent Visitors",
    comment: "Section header above the list of people who visited today"   // Rule 4
)

// Explicit key: 'Call' is ambiguous in English, and this label is being iterated on.
let actionLabel = String(
    localized: "CALL_VERB",                                                // Rule 5
    defaultValue: "Call",
    comment: "verb: Button that starts a phone call to the selected contact"
)

// A key that cannot be a literal. The literal below is what gets extracted;
// the catalog entry for the dynamic table is added by hand and marked
// manually managed in the editor so a build never removes it.            // Rule 3
func statusLabel(for code: ServerStatusCode) -> String {
    String(localized: "server.status.unknown",
           defaultValue: "Status unavailable",
           comment: "Shown when the server returns a status the app doesn't recognize")
}
```

## Non-Compliant Example

```swift
// violates Rule 2 -- the argument is a variable, so nothing is extracted.
// This still resolves at runtime, and in English it returns the key itself,
// so the bug is invisible until someone runs the app in another language.
let heading = sectionTitles[index]
let title = String(localized: String.LocalizationValue(heading))

// violates Rule 4 -- no comment. A translator sees the bare word "Call"
// with no way to know whether it is a noun or a verb.
let actionLabel = String(localized: "Call")

// violates Rule 5 -- value-as-key on copy that is still being reworded.
// Changing "Recent Visitors" to "Today's Visitors" marks every existing
// translation Needs Review across all languages at once.
let title = String(localized: "Recent Visitors", comment: "Section header")
```
Passes a variable where extraction requires a literal, so the string never reaches the catalog or a translator (Rule 2); omits the translator context that disambiguates a heteronym (Rule 4); and uses the English text as the key for copy that is expected to change, guaranteeing churn across every localization (Rule 5).

## Dependencies

None within this domain -- this contract is the entry point. `localized-string-apis` builds on it by covering which API to call at each extractable call site, and `plural-and-device-variations` builds on it by covering variation inside a catalog entry.

## References

- [Apple Developer — Localizing and varying text with a string catalog](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog)
- [Apple Developer — Preparing your app's text for translation](https://developer.apple.com/documentation/xcode/preparing-your-apps-text-for-translation)
- [Apple Developer — Xcode 15 Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes)
- [Apple Developer — Xcode 16 Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes)
- [WWDC23 — Discover String Catalogs](https://developer.apple.com/videos/play/wwdc2023/10155/)
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/localization/string-catalogs-and-extraction.md --type knowledge
```

---

## Task 3: Knowledge Contract — `localized-string-apis`

**Files:**
- Create: `knowledge/localization/localized-string-apis.md`

- [ ] **Step 1: Create the file**

```markdown
# Localized String APIs

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.localized-string-apis
type: knowledge
title: Localized String APIs
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines which localized-string API to call and how -- String(localized:) and its parameters including the locale parameter that does not change lookup language, LocalizedStringResource for deferred cross-process resolution, SwiftUI's implicit Text literal localization and the silent non-localization of string variables, format specifiers and positional arguments, AttributedString(localized:), and the remaining role of NSLocalizedString.
domain: Localization
tags:
  - string-localized
  - localizedstringresource
  - localizedstringkey
  - nslocalizedstring
  - format-specifier
references:
  - https://developer.apple.com/documentation/swift/string/init(localized:table:bundle:locale:comment:)
  - https://developer.apple.com/documentation/swift/string/init(localized:defaultvalue:table:bundle:locale:comment:)
  - https://developer.apple.com/documentation/swift/string/init(localized:)
  - https://developer.apple.com/documentation/foundation/localizedstringresource
  - https://developer.apple.com/documentation/swiftui/localizedstringkey
  - https://developer.apple.com/documentation/swiftui/text/init(_:tablename:bundle:comment:)
  - https://developer.apple.com/documentation/swiftui/text/init(verbatim:)
  - https://developer.apple.com/documentation/foundation/nslocalizedstring(_:tablename:bundle:value:comment:)
  - https://developer.apple.com/documentation/foundation/attributedstring
  - https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes
depends_on:
  - knowledge.localization.string-catalogs-and-extraction
related:
  - knowledge.localization.locale-and-language-resolution
  - knowledge.localization.localized-resources-and-infoplist
updated: 2026-08-07
```

## Intent

This contract governs which API an agent calls to produce a localized string and how its parameters behave -- particularly the two places the API surface does something other than what its name suggests: the `locale:` parameter, which does not select a language, and SwiftUI's `Text`, which localizes literals but silently does not localize variables.

## Scope

### Included

- `String(localized:)` in its value-as-key, explicit-key, and `LocalizedStringResource` forms, and what `table:`, `bundle:`, `locale:`, and `comment:` each do
- `LocalizedStringResource` and deferred, cross-process resolution
- `LocalizedStringKey`, SwiftUI's implicit localization of string literals, and `Text(verbatim:)`
- String interpolation, C-style format specifiers, and positional arguments
- `AttributedString(localized:)` and Markdown carried in translations
- `NSLocalizedString`'s remaining role

### Excluded

- How the string got into the catalog, keys, comments, and translation states -- see `string-catalogs-and-extraction`
- Plural and device variation of a string -- see `plural-and-device-variations`
- Which `Locale` the app resolved to, and how -- see `locale-and-language-resolution`
- Looking a string up from a package or framework bundle -- see `localized-resources-and-infoplist`
- Date, number, and measurement formatting -- owned by the `foundation` domain

## Rules

### Rule 1

Agents MUST NOT use the `locale:` parameter to select a language, because it does not do that. Per Apple's documentation for `String(localized:table:bundle:locale:comment:)`, `locale` is "The locale to use when localizing interpolated values, such as numbers. This doesn't change which locale the system uses to look up the localized string." The documented way to look a string up in a different locale is to set the locale on a `LocalizedStringResource` first: per Apple's documentation for `String(localized:)`, "Alter the resource's `locale` prior to calling this method if you want to localize this string in a different locale than the process that creates the `LocalizedStringResource`."

### Rule 2

Agents MUST pass a string *literal* to SwiftUI's localizing initializers and MUST treat a string variable as explicitly non-localized. Per Apple's documentation for `LocalizedStringKey`: "Passing a `String` variable to these initializers avoids localization, which is usually appropriate when the variable contains a user-provided value," and "to localize the value of a string variable, create a new `LocalizedStringKey` instance from it." Per Apple's documentation for `Text.init(_:tableName:bundle:comment:)`: "When you initialize a text view with a string variable rather than a string literal, the view triggers the `init(_:)` initializer instead, because it assumes you don't want localization." To opt a literal out deliberately, use `Text(verbatim:)`, which "Creates a text view that displays a string literal without localization."

### Rule 3

Agents MUST use `LocalizedStringResource` rather than an eagerly-resolved `String` whenever the string will be read in another process, and MUST NOT resolve it to a `String` before handing it over. Per Apple's documentation: initializers taking `String.LocalizationValue` "lookup the localized string immediately. If you want to perform the lookup at a later time, use this `LocalizedStringResource` type… This approach allows you to provide localizable strings to an entirely separate process, which may use a different locale." Apple names the canonical case: "The App Intents framework uses `LocalizedStringResource` to perform a late resolution of localized strings. This allows the Siri UI to potentially use different localization preferences than the app providing the intent."

### Rule 4

Agents MUST express dynamic values as interpolations within a single localized string rather than concatenating localized fragments. Per Apple's documentation for `NSLocalizedString`: "Use format strings instead of interpolated strings for dynamic values." Per Apple's WWDC22 session "Building global apps: Localization by example": "Joining strings might have surprising consequences in other languages: they might need to inflect the grammar or could have troubles with capitalization, but knowing that beforehand when writing the code is difficult. Keep that in mind when you're tempted to construct a string programmatically."

### Rule 5

Agents MUST use positional specifiers consistently when a translation may reorder arguments, and MUST NOT mix numbered and unnumbered specifiers in one string. Per Apple's Xcode 16 release notes, the String Catalog editor now diagnoses this: issues "are also produced when a single string contains conflicting format specifiers or a mixture of numbered and unnumbered variables. For example, both `The %1$@ crossed the %1$lld` and `The %1$@ crossed the %lld` are incorrect and would be diagnosed."

### Rule 6

Agents MUST put the styling of a localized rich-text string in the translation rather than in code. Per Apple's documentation for `AttributedString`: "To create localizable attributed strings, use Markdown syntax in your strings files." Because the markup travels with each translation, an agent MUST NOT assume emphasis or link placement is identical across languages.

### Rule 7

Agents SHOULD prefer `String(localized:)` and `LocalizedStringResource` in new Swift code, and MAY use `NSLocalizedString` when working in Objective-C/C or matching an existing codebase's convention -- it remains supported and is a recognized extraction source, not a deprecated API. Per Apple's documentation, `NSLocalizedString` is available from iOS 8.0 with no deprecation notice, and Apple's "Preparing your app's text for translation" lists it as the choice "for apps targeting older platforms." Agents MUST NOT use multiline string literals with it: per Apple's documentation, "Multiline string literals can result in unexpected newlines in exported localizations. Use string concatenation instead."

## Compliant Example

```swift
import SwiftUI

struct VisitorSummary: View {
    let visitorName: String        // user-provided; must NOT be localized
    let visitCount: Int

    var body: some View {
        VStack {
            Text("Recent Visitors")                    // Rule 2: literal -> localized
            Text(verbatim: visitorName)                // Rule 2: deliberate opt-out

            // Rule 4: one interpolated string, not "You had " + count + " visits"
            Text("You had \(visitCount) visits today")
        }
    }
}

// Rule 3: hand a resource, not a resolved String, to another process.
struct ShowVisitorsIntent: AppIntent {
    static var title: LocalizedStringResource = "Show Recent Visitors"
}

// Rule 1: format the interpolated number in a specific locale, while
// accepting that the *text* still comes from the app's resolved localization.
let caption = String(
    localized: "You had \(visitCount) visits today",
    locale: Locale(identifier: "de_DE"),
    comment: "Caption under the visitor chart"
)
```

## Non-Compliant Example

```swift
// violates Rule 1 -- expects German text, gets the app's current language
// with German number formatting. Silently wrong, and looks correct in tests
// that only assert the number.
let german = String(localized: "Welcome back", locale: Locale(identifier: "de"))

// violates Rule 2 -- refactoring the literal into a constant silently
// un-localizes it. No warning, and English output is unchanged.
let heading = "Recent Visitors"
Text(heading)

// violates Rule 4 -- concatenation. Word order, grammatical inflection, and
// capitalization are all wrong in languages that don't follow English order.
Text(String(localized: "You had ") + "\(visitCount)" + String(localized: " visits today"))

// violates Rule 3 -- resolving eagerly defeats late resolution entirely;
// Siri now shows the string in the app's locale, not the user's.
static var title: LocalizedStringResource =
    LocalizedStringResource(stringLiteral: String(localized: "Show Recent Visitors"))
```
Uses `locale:` as if it selected a language (Rule 1); passes a variable to `Text`, which resolves to the non-localizing initializer (Rule 2); builds a sentence by concatenating localized fragments (Rule 4); and collapses a `LocalizedStringResource` into an eagerly-resolved `String`, defeating the deferred resolution the type exists to provide (Rule 3).

## Dependencies

- `string-catalogs-and-extraction` -- every call site in this contract is also an extraction site, and the literal requirement stated there constrains every API here.

## References

- [Apple Developer — String.init(localized:table:bundle:locale:comment:)](https://developer.apple.com/documentation/swift/string/init(localized:table:bundle:locale:comment:))
- [Apple Developer — String.init(localized:defaultValue:table:bundle:locale:comment:)](https://developer.apple.com/documentation/swift/string/init(localized:defaultvalue:table:bundle:locale:comment:))
- [Apple Developer — String.init(localized:)](https://developer.apple.com/documentation/swift/string/init(localized:))
- [Apple Developer — LocalizedStringResource](https://developer.apple.com/documentation/foundation/localizedstringresource)
- [Apple Developer — LocalizedStringKey](https://developer.apple.com/documentation/swiftui/localizedstringkey)
- [Apple Developer — Text.init(_:tableName:bundle:comment:)](https://developer.apple.com/documentation/swiftui/text/init(_:tablename:bundle:comment:))
- [Apple Developer — Text.init(verbatim:)](https://developer.apple.com/documentation/swiftui/text/init(verbatim:))
- [Apple Developer — NSLocalizedString](https://developer.apple.com/documentation/foundation/nslocalizedstring(_:tablename:bundle:value:comment:))
- [Apple Developer — AttributedString](https://developer.apple.com/documentation/foundation/attributedstring)
- [Apple Developer — Xcode 16 Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes)
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/localization/localized-string-apis.md --type knowledge
```

---

## Task 4: Knowledge Contract — `plural-and-device-variations`

**Files:**
- Create: `knowledge/localization/plural-and-device-variations.md`

- [ ] **Step 1: Create the file**

```markdown
# Plural and Device Variations

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.plural-and-device-variations
type: knowledge
title: Plural and Device Variations
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how a single catalog entry varies by grammatical number and by device -- the CLDR plural categories with other required and the applicable set language-dependent, Vary by Plural and Vary by Device, substitutions for strings with more than one varying value, the legacy stringsdict form that a catalog compiles into, and why runtime inflection is a separate mechanism from plural variation.
domain: Localization
tags:
  - pluralization
  - cldr
  - stringsdict
  - device-variation
  - substitution
references:
  - https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog
  - https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals
  - https://developer.apple.com/documentation/foundation/inflectionrule
  - https://developer.apple.com/videos/play/wwdc2023/10155/
  - https://developer.apple.com/videos/play/wwdc2022/10110/
depends_on:
  - knowledge.localization.string-catalogs-and-extraction
related:
  - knowledge.localization.localized-string-apis
updated: 2026-08-07
```

## Intent

This contract governs varying one localizable string by grammatical number or by device, so that the correct wording is chosen by the localization system rather than by application logic. Its central claim is that plural selection is a translation-data concern, not a code concern.

## Scope

### Included

- Plural variation on a catalog entry, and Xcode's per-language category population
- The CLDR plural categories, which is mandatory, and why the applicable set differs per language
- Device variation and what it is for
- Substitutions, for a string with more than one varying value
- `.stringsdict` as the legacy authoring form and the current runtime artifact
- The distinction between plural variation and `^[…](inflect: true)` runtime inflection

### Excluded

- Getting the string into the catalog in the first place -- see `string-catalogs-and-extraction`
- Which API to call at the call site -- see `localized-string-apis`
- Number formatting itself (digit grouping, numeral systems, decimal separators) -- owned by the `foundation` domain
- The `.xcstrings` file's internal JSON structure -- Apple publishes no schema for it

## Rules

### Rule 1

Agents MUST express singular/plural wording as a plural variation on the catalog entry and MUST NOT branch on the count in application code. Per Apple's WWDC22 session "Building global apps: Localization by example": "You do not want to implement that logic in your code, and this is why you leverage Apple's frameworks. All you have to do is to declare the string in code and provide a stringsdict file, which encodes the plural rule."

### Rule 2

Agents MUST always provide the `other` category and MUST NOT assume the English category set applies elsewhere. Per Apple's documentation, the categories are "`zero, one, two, few, many, other`" and "The `other` category is a requirement." Per the same page: "The meaning of the plural categories is language-dependent, and not all languages have the same categories. For example, the English language only requires the `one` and `other` categories to represent plural forms, and `zero` is optional. Arabic has different plural forms for the `zero`, `one`, `two`, `few`, `many`, and `other` categories. Although Russian also uses the `many` category, the rules for which numbers are in the `many` category aren't the same as the Arabic rules."

### Rule 3

Agents MUST let Xcode populate a language's categories rather than assuming a fixed set, and MUST author plural variants on the source localization so they propagate. Per Apple's documentation: "Xcode adds One and Other variants for English when it's the source localization, and One, Few, Many, and Other variants for Russian when you add Russian." And: "You can add plural variants to the source localization before or after you add languages and Xcode keeps all the plural variants in sync. If you add plural variants to a language other than the source localization, that change affects only that language."

### Rule 4

Agents MUST use a substitution when one string varies by more than one value, rather than splitting it into several strings. Per Apple's WWDC23 session "Discover String Catalogs": "Each substitution, prefixed with an @ sign, stores a dictionary of plural cases and their values… At runtime, the top-level string shown here will be used, substituting in the appropriate plural case from each referenced substitution." Per the same session, "Substitutions usually correspond to arguments passed into the string, often using string interpolation."

### Rule 5

Agents SHOULD use device variation only for wording that must change because of the device's interaction model or available space, not as a general branching mechanism. Per Apple's documentation: "When you need to alter the text that displays on a device due to the available space, or because it has a different interaction, use the Vary by Device option." Apple's worked example varies "Tap to learn more" on iOS against "Click to learn more" on macOS.

### Rule 6

Agents MUST NOT treat `^[…](inflect: true)` as a pluralization mechanism. Automatic grammatical agreement is a runtime `AttributedString` transform governed by `InflectionRule`, limited to the languages Apple's grammar engine supports; plural variation is catalog data resolved for every language through CLDR categories. Per Apple's documentation for `AttributedString`, the inflection markup is used with localized attributed strings for grammatical agreement, and it is documented independently of the plural-variation mechanism described in "Localizing strings that contain plurals."

### Rule 7

Agents MUST treat `.stringsdict` as legacy for *authoring* only, not as a removed format. Per Apple's documentation: "In Xcode 15 and later, string catalogs are the recommended way to localize strings that contain plurals." Per Apple's WWDC23 session, at build time String Catalogs "compile to .strings and .stringsdict files" -- which is why Apple's `.stringsdict` page remains the reference for plural-category semantics. When reading or maintaining an existing `.stringsdict`, agents MUST read `NSStringLocalizedFormatKey` as "A formatted string that contains variables. To replace the string with a plural rule, precede the variable with the `%#@` characters and follow it by the `@` character, as in `%#@homes@`", with `NSStringFormatSpecTypeKey` whose "only possible value is `NSStringPluralRuleType`".

## Compliant Example

```swift
// One string, one call site. The catalog entry carries the plural variants;
// Xcode populated One/Other for English and One/Few/Many/Other for Russian.
// Rules 1, 2, 3
let summary = String(
    localized: "\(visitorCount) visitors today",
    comment: "Caption under the visitor chart; varies by number of visitors"
)

// Two varying values in one sentence -> two substitutions on one entry,
// not two separately-localized fragments. Rule 4
let detail = String(
    localized: "\(birdCount) birds across \(yardCount) backyards",
    comment: "Summary line on the sightings screen"
)

// Device variation: the verb differs because the interaction differs. Rule 5
let hint = String(
    localized: "Tap to learn more",
    comment: "Footer hint; varies by device -- click on macOS"
)
```

## Non-Compliant Example

```swift
// violates Rule 1 and Rule 2 -- plural selection in code. This is correct
// only in languages with exactly two forms; Russian needs one/few/many and
// Arabic needs six, so both get the wrong wording with no error anywhere.
let summary = visitorCount == 1
    ? String(localized: "1 visitor today")
    : String(localized: "\(visitorCount) visitors today")

// violates Rule 4 -- splitting a sentence to handle two counts. Translators
// cannot reorder across the split, and the join is ungrammatical in most
// languages.
let detail = String(localized: "\(birdCount) birds")
    + String(localized: " across \(yardCount) backyards")

// violates Rule 6 -- inflect markup used as if it pluralized. It is a
// runtime transform limited to the supported grammar-engine languages, so
// this silently produces nothing in Russian, Polish, or Arabic.
let label = AttributedString(localized: "^[\(visitorCount) visitor](inflect: true)")
```
Branches on the count in code, which is only ever correct for two-form languages (Rules 1–2); splits one sentence into two independently-translated fragments, removing the translator's ability to reorder (Rule 4); and uses runtime inflection markup in place of catalog plural variation, which does not pluralize outside the grammar engine's supported languages (Rule 6).

## Dependencies

- `string-catalogs-and-extraction` -- variation is authored on a catalog entry, which must exist and be extracted first.

## References

- [Apple Developer — Localizing and varying text with a string catalog](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog)
- [Apple Developer — Localizing strings that contain plurals](https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals)
- [Apple Developer — InflectionRule](https://developer.apple.com/documentation/foundation/inflectionrule)
- [WWDC23 — Discover String Catalogs](https://developer.apple.com/videos/play/wwdc2023/10155/)
- [WWDC22 — Building global apps: Localization by example](https://developer.apple.com/videos/play/wwdc2022/10110/)
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/localization/plural-and-device-variations.md --type knowledge
```

---

## Task 5: Knowledge Contract — `locale-and-language-resolution`

**Files:**
- Create: `knowledge/localization/locale-and-language-resolution.md`

- [ ] **Step 1: Create the file**

```markdown
# Locale and Language Resolution

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.locale-and-language-resolution
type: knowledge
title: Locale and Language Resolution
version: 0.1.0
status: Draft
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
  - https://developer.apple.com/documentation/foundation/bundle
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
updated: 2026-08-07
```

## Intent

This contract governs where a `Locale` comes from, what it actually represents, and how the system picks which localization an app runs in. Its central claim is that `Locale.current` describes the *app's resolved* locale, not the user's preferences -- a distinction that silently corrupts analytics, server requests, and content selection when ignored.

## Scope

### Included

- `Locale.current` vs. `Locale.autoupdatingCurrent`, the three inputs that define both, and the equality caveat
- `Locale.preferredLanguages` vs. `Bundle.preferredLocalizations` vs. `Bundle.localizations`, and `Bundle.preferredLocalizations(from:)`
- `Locale.Language`/`Locale.Region` and the deprecation of the older string properties
- `CFBundleDevelopmentRegion`/`Bundle.developmentLocalization` and Base localization's constraint
- The `.lproj` fallback chain the system walks to choose a localization
- Per-app language settings and the absence of an API to set them
- Choosing language identifiers at the right specificity

### Excluded

- Passing a `Locale` to a formatter to produce a date, number, or measurement string -- owned by the `foundation` domain (`date-time-formatting`, `measurement-and-unit-formatting`)
- The `locale:` parameter on the localized-string APIs -- see `localized-string-apis`
- Bundle resource lookup for non-string resources -- see `localized-resources-and-infoplist`
- Detecting writing direction in order to lay out an interface -- see `layout-direction-and-rtl-apis`

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
// Rule 1: the user's preference, not the app's resolved locale.
let userLanguages = Locale.preferredLanguages

// Rule 5: let the system match against a server-supplied list.
let serverLanguages = ["en", "de", "ar", "ja"]
let bestMatch = Bundle.preferredLocalizations(from: serverLanguages).first

// Rule 2: a long-lived formatter must follow settings changes.
final class PriceFormatter {
    private let formatter: NumberFormatter = {
        let f = NumberFormatter()
        f.numberStyle = .currency
        f.locale = .autoupdatingCurrent
        return f
    }()
}

// Rule 4: modern accessors; region and language.region are distinct.
let language = Locale.current.language.languageCode
let region = Locale.current.region

// Rule 7: send the user to Settings; don't try to switch languages in-app.
if let url = URL(string: UIApplication.openSettingsURLString) {
    await UIApplication.shared.open(url)
}
```

## Non-Compliant Example

```swift
// violates Rule 1 -- reports the app's localization coverage back to the
// server, not the user's preference. An Arabic-speaking user of an
// English-only build is recorded as an English speaker.
analytics.send(userLanguage: Locale.current.identifier)

// violates Rule 2 -- captures a snapshot at init. After the user changes
// region in Settings, this formatter keeps using the old one for the
// lifetime of the process.
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

- [Apple Developer — Locale.current](https://developer.apple.com/documentation/foundation/locale/current)
- [Apple Developer — Locale.autoupdatingCurrent](https://developer.apple.com/documentation/foundation/locale/autoupdatingcurrent)
- [Apple Developer — Locale.preferredLanguages](https://developer.apple.com/documentation/foundation/locale/preferredlanguages)
- [Apple Developer — Locale.region](https://developer.apple.com/documentation/foundation/locale/region-swift.property)
- [Apple Developer — Bundle](https://developer.apple.com/documentation/foundation/bundle)
- [Apple Developer — Bundle.preferredLocalizations](https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations)
- [Apple Developer — Bundle.preferredLocalizations(from:)](https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations(from:))
- [Apple Developer — CFBundleDevelopmentRegion](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledevelopmentregion)
- [Apple Developer — Choosing localization regions and scripts](https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts)
- [Apple Developer — QA1828: How iOS Determines the Language For Your App](https://developer.apple.com/library/archive/qa/qa1828/_index.html)
- [WWDC22 — Building global apps: Localization by example](https://developer.apple.com/videos/play/wwdc2022/10110/)
- [WWDC24 — Build multilingual-ready apps](https://developer.apple.com/videos/play/wwdc2024/10185/)
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/localization/locale-and-language-resolution.md --type knowledge
```

---

## Task 6: Knowledge Contract — `layout-direction-and-rtl-apis`

**Files:**
- Create: `knowledge/localization/layout-direction-and-rtl-apis.md`

> **Boundary reminder:** this contract is the API layer only. Design-level RTL guidance -- what mirrors, numeral handling, icon-flip decisions -- stays with `knowledge.human-interface-guidelines.right-to-left`, which this contract cross-references via `related:` rather than restating. It also closes the seam that contract's own Excluded section left open ("SF Symbols' built-in RTL-variant mechanics specifically is not yet covered by any current contract").

- [ ] **Step 1: Create the file**

```markdown
# Layout Direction and RTL APIs

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.layout-direction-and-rtl-apis
type: knowledge
title: Layout Direction and RTL APIs
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the API layer of right-to-left support -- leading and trailing over left and right, SwiftUI's automatic mirroring and why reading layoutDirection usually means double-flipping, flipsForRightToLeftLayoutDirection as a contents-mirroring modifier rather than an RTL switch, UIKit semanticContentAttribute whose unspecified default means flip, effectiveUserInterfaceLayoutDirection which does not inherit, SF Symbols' name-driven mirroring, and detecting direction through Locale.Language.characterDirection.
domain: Localization
tags:
  - rtl
  - layout-direction
  - semantic-content-attribute
  - character-direction
  - sf-symbols-mirroring
references:
  - https://developer.apple.com/documentation/swiftui/layoutdirection
  - https://developer.apple.com/documentation/swiftui/environmentvalues/layoutdirection
  - https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:)
  - https://developer.apple.com/documentation/swiftui/horizontalalignment/leading
  - https://developer.apple.com/documentation/uikit/uiview/semanticcontentattribute
  - https://developer.apple.com/documentation/uikit/uisemanticcontentattribute
  - https://developer.apple.com/documentation/uikit/uiview/effectiveuserinterfacelayoutdirection
  - https://developer.apple.com/documentation/uikit/uiview/userinterfacelayoutdirection(for:relativeto:)
  - https://developer.apple.com/documentation/uikit/uiimage/imageflippedforrighttoleftlayoutdirection()
  - https://developer.apple.com/documentation/uikit/creating-custom-symbol-images-for-your-app
  - https://developer.apple.com/documentation/foundation/locale/language-swift.struct/characterdirection
  - https://developer.apple.com/documentation/foundation/nslocale/languagedirection
  - https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization
  - https://developer.apple.com/videos/play/wwdc2022/10107/
depends_on: []
related:
  - knowledge.human-interface-guidelines.right-to-left
  - knowledge.localization.locale-and-language-resolution
  - knowledge.sf-symbols.symbol-variants
updated: 2026-08-07
```

## Intent

This contract governs the APIs that make an interface work in right-to-left languages. Its central claim is that RTL support is mostly achieved by *not* writing direction-aware code -- the system mirrors automatically, and most RTL bugs come from either overriding that or from choosing absolutely-directional APIs and assets.

## Scope

### Included

- `leading`/`trailing` over `left`/`right`, in SwiftUI alignment and UIKit Auto Layout
- SwiftUI `LayoutDirection`, `\.layoutDirection`, and automatic mirroring
- `flipsForRightToLeftLayoutDirection(_:)` and what it actually mirrors
- UIKit `semanticContentAttribute`, `UISemanticContentAttribute`, `effectiveUserInterfaceLayoutDirection`
- `UIImage.imageFlippedForRightToLeftLayoutDirection()` and asset-catalog direction
- SF Symbols' automatic, name-driven mirroring
- `Locale.Language.characterDirection` and `Locale.LanguageDirection`
- Exercising RTL through the scheme's RTL pseudolanguages

### Excluded

- RTL visual-design decisions -- what should mirror, numeral handling, whether an icon reads correctly reversed -- owned by `knowledge.human-interface-guidelines.right-to-left`
- Which localization the app resolved to -- see `locale-and-language-resolution`
- Number and date formatting, including numeral systems -- owned by the `foundation` domain
- General SF Symbols rendering, variants, weight, and scale -- owned by the `sf-symbols` domain; this contract covers only their RTL mirroring behavior
- Localizing the assets themselves -- see `localized-resources-and-infoplist`

## Rules

### Rule 1

Agents MUST use leading/trailing rather than left/right for anything that follows reading order. Per Apple's WWDC22 session "Get it right (to left)": "The 'leading' edge of something is the edge closest to beginning of the line or to the side of the screen or window where the reader would begin reading, left for left to right and right for right to left… Most of the time, you want to use these instead of 'left' and 'right,' saving 'left' and 'right' only for things that are tied to an absolute direction." Per Apple's Internationalization guide: "When you use the Auto Layout `leading` and `trailing` attributes (not the `right` and `left` attributes), most of the user interface appears mirrored in right-to-left languages." Note that this behavior is specified in those sources rather than on the `NSLayoutConstraint.Attribute` or `leadingAnchor` reference pages, which describe the anchors without stating their RTL semantics.

### Rule 2

Agents MUST NOT read `\.layoutDirection` in order to reorder content manually, because SwiftUI has already mirrored the layout. Per Apple's documentation for `LayoutDirection`: "in many cases, you don't need to take any action based on this value. SwiftUI horizontally flips the x position of each view within its parent, so layout calculations automatically produce the desired effect for both modes without any changes." Reversing a stack's contents in response to the value applies a second flip and restores left-to-right order.

### Rule 3

Agents MUST treat `flipsForRightToLeftLayoutDirection(_:)` as a way to mirror one view's *contents*, not as a switch that enables RTL layout, and MUST NOT apply it broadly. Per Apple's documentation, it "Sets whether this view mirrors its contents horizontally when the layout direction is right-to-left," and its parameter documentation states: "By default, views will adjust their layouts automatically in a right-to-left context and do not need to be mirrored."

### Rule 4

Agents MUST set an explicit `semanticContentAttribute` on UIKit views that must not mirror, because the default value mirrors. Per Apple's WWDC22 session: "The default is 'Unspecified,' which causes the control to reverse its appearance." Per Apple's documentation, the opt-outs are semantic: `playback` is "A view representing the playback controls, such as Play, Rewind, or Fast Forward buttons or playhead scrubbers," and `spatial` is "A view representing a directional control, such as a segment control for text alignment, or a D-pad control for a game." Apple's guidance is to pick by meaning: "Instead of thinking about whether or not a view should change its orientation, select the semantic content attribute that best describes your view."

### Rule 5

Agents MUST read `effectiveUserInterfaceLayoutDirection` on the view whose immediate content is being arranged, and MUST NOT cache it for a subtree. Per Apple's documentation: "When a view's immediate content is being arranged or drawn, you should always consult the value of this property. In addition, note that you can't assume that the value propagates through the view's subtree." Apple also directs agents toward this property over the class method: on `userInterfaceLayoutDirection(for:relativeTo:)`, "Although layout and drawing code can use this method to determine how to arrange elements, it might be easier to query the container view's `effectiveUserInterfaceLayoutDirection` property instead."

### Rule 6

Agents MUST choose SF Symbols by directional semantics, because mirroring is automatic and driven by the symbol's name with no API to request it. Per Apple's WWDC22 session: "SF Symbols follows this naming convention throughout with icons that you may or may not want to have flip for right to left. The 'forward' and 'backward' ones flip, and the 'left' and 'right' ones don't," and "When choosing images in SF Symbols, remember that 'left' and 'right' always point those directions and 'forward' and 'backward' point in different directions depending on the UI language." Per Apple's documentation on custom symbols: "Image variants adapt automatically according to the user's device language, including right-to-left writing systems." A back button therefore uses `chevron.backward`, not `chevron.left`.

### Rule 7

Agents MUST NOT assume `imageFlippedForRightToLeftLayoutDirection()` returns a mirrored image. Per Apple's documentation: "This method returns the current `UIImage` object with the `flipsForRightToLeftLayoutDirection` property set to `true`; it does not return a flipped image." The mirroring happens at display time, and Apple scopes it to display "in a `UIImageView` object" -- custom drawing of that image does not flip. For custom artwork, agents MUST opt each asset in explicitly: per Apple's asset catalog reference, with no direction set "The image has a fixed horizontal orientation and will display in the same direction."

### Rule 8

Agents MUST detect writing direction through `Locale.Language.characterDirection` and MUST test for right-to-left explicitly. Per Apple's documentation, `Locale.characterDirection(forLanguage:)` is deprecated as of iOS 16.0 with the replacement note "Use `Locale.Language(identifier:).characterDirection` instead." `Locale.LanguageDirection` has five cases -- `unknown`, `leftToRight`, `rightToLeft`, `topToBottom`, `bottomToTop` -- so a negated comparison against `.leftToRight` also matches unknown languages and vertical scripts.

### Rule 9

Agents SHOULD exercise RTL through the scheme's pseudolanguages rather than requiring an RTL localization, and SHOULD use the strings variant to catch bidirectional text problems. Per Apple's documentation, "Right-to-Left Pseudolanguage" "Simulates a right-to-left writing direction to test whether views flip accordingly," while "Right-to-Left Pseudolanguage With Right-to-Left Strings" "Simulates a right-to-left writing direction, using right-to-left strings."

## Compliant Example

```swift
import SwiftUI

struct ArticleRow: View {
    var body: some View {
        HStack {                                        // Rule 2: no manual reordering
            VStack(alignment: .leading) {               // Rule 1: leading, not .left
                Text("Article Title")
                Text("Subtitle")
            }
            Spacer()
            Image(systemName: "chevron.forward")        // Rule 6: forward mirrors
        }
        .padding(.leading, 16)                          // Rule 1
    }
}

// Rule 3: mirror one directional glyph's contents, not the screen.
Image("custom-reply-arrow")
    .flipsForRightToLeftLayoutDirection(true)

// Rule 8: explicit right-to-left test on the modern API.
let isRTL = Locale.current.language.characterDirection == .rightToLeft

// Rule 4: a scrubber must not mirror; say so semantically.
playbackScrubber.semanticContentAttribute = .playback

// Rule 5: read direction on the view being arranged.
let direction = containerView.effectiveUserInterfaceLayoutDirection
```

## Non-Compliant Example

```swift
// violates Rule 2 -- SwiftUI already mirrored the stack, so reversing here
// flips it back to left-to-right in Arabic.
@Environment(\.layoutDirection) private var direction
HStack {
    if direction == .rightToLeft {
        ForEach(items.reversed()) { ItemView($0) }
    } else {
        ForEach(items) { ItemView($0) }
    }
}

// violates Rule 1 and Rule 6 -- absolute edge, and a symbol that never
// mirrors, so the back button points the wrong way in RTL.
.padding(.leading, 16)
Image(systemName: "chevron.left")

// violates Rule 4 -- left at the default, so the playhead scrubber reverses
// and time appears to run backwards in Arabic.
let scrubber = UISlider()

// violates Rule 8 -- also true for .unknown and for vertical scripts.
let isRTL = Locale.current.language.characterDirection != .leftToRight
```
Reverses content that SwiftUI has already mirrored, producing a double flip (Rule 2); pairs an absolutely-directional symbol with a back action so it points the wrong way under RTL (Rule 6); leaves a playback control at the mirroring default (Rule 4); and treats a five-case enumeration as a boolean, so unknown languages and vertical scripts are misreported as right-to-left (Rule 8).

## Dependencies

None within this domain. Cross-references `knowledge.human-interface-guidelines.right-to-left` via `related:` for the design layer this contract deliberately does not cover, and `knowledge.sf-symbols.symbol-variants` for general symbol usage beyond mirroring behavior.

## References

- [Apple Developer — LayoutDirection](https://developer.apple.com/documentation/swiftui/layoutdirection)
- [Apple Developer — EnvironmentValues.layoutDirection](https://developer.apple.com/documentation/swiftui/environmentvalues/layoutdirection)
- [Apple Developer — flipsForRightToLeftLayoutDirection(_:)](https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:))
- [Apple Developer — HorizontalAlignment.leading](https://developer.apple.com/documentation/swiftui/horizontalalignment/leading)
- [Apple Developer — UIView.semanticContentAttribute](https://developer.apple.com/documentation/uikit/uiview/semanticcontentattribute)
- [Apple Developer — UISemanticContentAttribute](https://developer.apple.com/documentation/uikit/uisemanticcontentattribute)
- [Apple Developer — UIView.effectiveUserInterfaceLayoutDirection](https://developer.apple.com/documentation/uikit/uiview/effectiveuserinterfacelayoutdirection)
- [Apple Developer — userInterfaceLayoutDirection(for:relativeTo:)](https://developer.apple.com/documentation/uikit/uiview/userinterfacelayoutdirection(for:relativeto:))
- [Apple Developer — imageFlippedForRightToLeftLayoutDirection()](https://developer.apple.com/documentation/uikit/uiimage/imageflippedforrighttoleftlayoutdirection())
- [Apple Developer — Creating custom symbol images for your app](https://developer.apple.com/documentation/uikit/creating-custom-symbol-images-for-your-app)
- [Apple Developer — Locale.Language.characterDirection](https://developer.apple.com/documentation/foundation/locale/language-swift.struct/characterdirection)
- [Apple Developer — NSLocale.LanguageDirection](https://developer.apple.com/documentation/foundation/nslocale/languagedirection)
- [Apple Developer — Preparing your interface for localization](https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization)
- [Apple Developer — Supporting Right-to-Left Languages (archived)](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/SupportingRight-To-LeftLanguages/SupportingRight-To-LeftLanguages.html)
- [WWDC22 — Get it right (to left)](https://developer.apple.com/videos/play/wwdc2022/10107/)
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/localization/layout-direction-and-rtl-apis.md --type knowledge
```

---

## Task 7: Knowledge Contract — `localized-resources-and-infoplist`

**Files:**
- Create: `knowledge/localization/localized-resources-and-infoplist.md`

> **Sourcing constraint, binding on this task.** Research enumerated all 24 articles in Apple's current Xcode Localization documentation hub and found that **none** covers Info.plist localization; `documentation/xcode/localizing-your-apps-name` returns 404. The only current-era official source for `InfoPlist.xcstrings` is the WWDC23 transcript, and the only prose specification of the mechanism is the **archived** Info.plist Key Reference. Cite those honestly; do not imply a current reference page exists. Separately, no Apple source states in those words that permission usage strings *must* be localized — their user-visibility and required status are both documented, but the imperative is an inference and must be written as one.

- [ ] **Step 1: Create the file**

```markdown
# Localized Resources and Info.plist

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.localized-resources-and-infoplist
type: knowledge
title: Localized Resources and Info.plist
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines localization of everything that is not a source-code string -- Info.plist values which live in InfoPlist.strings rather than Info.plist itself, the app name keys and the 15-character CFBundleName cap, lproj structure and the rule that a non-localized resource shadows every localized variant, per-asset catalog localization, Swift-package defaultLocalization and Bundle.module, and non-main-bundle lookup whose missing-key result is the key itself.
domain: Localization
tags:
  - infoplist-strings
  - lproj
  - bundle-module
  - asset-localization
  - app-name
references:
  - https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions
  - https://developer.apple.com/documentation/xcode/adding-resources-to-localizations
  - https://developer.apple.com/documentation/xcode/localizing-assets-in-a-catalog
  - https://developer.apple.com/documentation/xcode/localizing-package-resources
  - https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
  - https://developer.apple.com/documentation/foundation/bundle
  - https://developer.apple.com/documentation/foundation/bundle/localizedstring(forkey:value:table:)
  - https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledisplayname
  - https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundlename
  - https://developer.apple.com/documentation/packagedescription/package/defaultlocalization
  - https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html
  - https://developer.apple.com/videos/play/wwdc2023/10155/
depends_on:
  - knowledge.localization.string-catalogs-and-extraction
related:
  - knowledge.localization.localized-string-apis
  - knowledge.localization.locale-and-language-resolution
  - knowledge.app-store-review-guidelines.permission-usage-strings
updated: 2026-08-07
```

## Intent

This contract governs localizing everything that is not a string literal in source code: Info.plist values, the app's name, asset-catalog resources, and resources shipped inside a framework or Swift package. Its central claim is that these surfaces fail *silently* -- a missing localized resource or a wrong bundle produces plausible English output rather than an error.

Sourcing note: Apple's current Xcode Localization documentation hub does not cover Info.plist localization, and no current reference page documents `InfoPlist.xcstrings`. The rules below draw on Apple's WWDC23 session and Apple's archived Info.plist Key Reference, which remains an accurate description of the runtime mechanism because String Catalogs compile into exactly the `InfoPlist.strings` artifact it describes.

## Scope

### Included

- Info.plist localization via `InfoPlist.strings`/`InfoPlist.xcstrings`, and the lookup order between them and `Info.plist`
- Permission usage descriptions and app-name keys as the values that most need localizing
- `CFBundleDisplayName` vs. `CFBundleName` and the length constraint
- `.lproj` structure, Base localization, and the resource search order
- Per-asset catalog localization and which asset types support it
- Swift-package and framework localization: `defaultLocalization`, `.lproj` layout rules, `Bundle.module`
- `Bundle.localizedString(forKey:value:table:)` and its missing-key behavior

### Excluded

- Source-code string extraction and catalog states -- see `string-catalogs-and-extraction`
- Which string API to call and its `bundle:` parameter semantics -- see `localized-string-apis`
- Which localization the app resolved to -- see `locale-and-language-resolution`
- The English wording of a permission usage string -- owned by `knowledge.app-store-review-guidelines.permission-usage-strings`; this contract owns getting that string translated
- Adding a language to the project and `.xcloc`/XLIFF export-import -- Xcode project configuration, deferred to the `xcode` domain

## Rules

### Rule 1

Agents MUST localize Info.plist values in a per-localization strings file, never by editing `Info.plist`, and MUST update both when a value changes. Per Apple's archived Info.plist Key Reference: "Localized values are not stored in the `Info.plist` file itself. Instead, you store the values for a particular localization in a strings file with the name `InfoPlist.strings`. You place this file in the same language-specific project directory that you use to store other resources for the same localization." And on resolution: "The routines that look up key values in the `Info.plist` file take the user's language preferences into account and return the localized version of the key… when one exists. If a localized version of a key does not exist, the routines return the value stored in the `Info.plist` file." Because the localized file wins, editing only `Info.plist` changes nothing for any user whose localization is present.

### Rule 2

Agents SHOULD localize permission usage descriptions along with the rest of the interface. Apple documents these strings as user-facing and required -- `NSCameraUsageDescription` is "A message that tells people why the app is requesting access to the device's camera," and "This key is required if your app uses APIs that access the device's camera" -- and the system, not the app, renders them inside its own alert, so a per-localization strings file is the only channel available. Note that Apple does not state a localization requirement for these keys in those words; this rule is an inference from their documented user-visibility and the documented Info.plist localization mechanism. Per Apple's WWDC23 session, the String Catalog form is `InfoPlist.xcstrings`: add it to the target, and each build adds a known set of localizable Info.plist keys to the catalog, with more addable by hand.

### Rule 3

Agents MUST use `CFBundleDisplayName` when a localized app name may exceed the short-name limit. Per Apple's documentation, `CFBundleName` is "A user-visible short name for the bundle" and "This name can contain up to 15 characters. The system may display it to users if `CFBundleDisplayName` isn't set," while `CFBundleDisplayName` is "The user-visible name for the bundle, used by Siri and visible on the iOS Home screen" and is the documented choice "if you want a product name that's longer than `CFBundleName`."

### Rule 4

Agents MUST NOT ship a non-localized copy of a resource alongside localized ones. Per Apple's documentation, the bundle searches "Global (nonlocalized) resources → Region-specific localized resources → Language-specific localized resources → Development language resources," and: "Because global resources take precedence over language-specific resources, you should never include both a global and localized version of a given resource in your app. When a global version of a resource exists, language-specific versions are never returned."

### Rule 5

Agents MUST opt each asset into localization individually and MUST NOT assume adding a project language localizes assets. Per Apple's documentation, only certain asset types qualify -- "color sets, image sets, symbol sets, watch complications, Apple TV image stacks, sprite atlases" -- and the flow is per-asset: "select the asset you want to localize in the outline view of the editor area. Under Localization in the Attributes inspector, click Localize."

### Rule 6

Agents MUST pass an explicit bundle when localizing strings in framework or package code, because the string APIs default to the main bundle. Per Apple's documentation for `Text.init(_:tableName:bundle:comment:)`: "bundle: The bundle containing the strings file. If `nil`, use the main bundle." Per Apple's documentation on Swift package resources: "Always use `Bundle.module` when you access resources. A package shouldn't make assumptions about the exact location of a resource." Apple's own framework sample obtains the bundle with `Bundle(for:)`.

### Rule 7

Agents MUST NOT read a successful-looking string as evidence that lookup succeeded. Per Apple's documentation for `Bundle.localizedString(forKey:value:table:)`, "If `key` is not found and `value` is `nil` or an empty string, returns `key`." Agents SHOULD use the documented diagnostic instead: with the `NSShowNonLocalizedStrings` user default set, "when the method can't find a localized string in the table, it logs a message to the console and capitalizes `key` before returning it" -- the same mechanism behind Xcode's "Show non-localized strings" scheme option, where per Apple's documentation "the nonlocalized strings appear in all caps."

### Rule 8

Agents MUST NOT declare `defaultLocalization` in a package manifest before localized resources exist, and MUST NOT nest directories inside an `.lproj`. Per Apple's documentation: "When you declare a value for `defaultLocalization` in the package manifest, Xcode requires the package to contain localized resources." And: "A language-specific directory has a name that uses an ISO 639 language code and optional designators, followed by the `.lproj` suffix, and doesn't contain subdirectories… Place your `.lproj` directories in a parent directory named `Resources`."

## Compliant Example

```swift
// Package.swift -- Rule 8: declared only because en.lproj/ and de.lproj/
// already exist under Sources/VisitorKit/Resources/
let package = Package(
    name: "VisitorKit",
    defaultLocalization: "en",
    targets: [.target(name: "VisitorKit")]
)
```

```swift
import SwiftUI

// Rule 6: package code must name its own bundle; the default is the app's.
struct VisitorBadge: View {
    var body: some View {
        Text("Verified Visitor", bundle: .module)
    }
}

// Rule 6, framework form.
let title = NSLocalizedString(
    "badge.verified",
    bundle: Bundle(for: VisitorBadgeController.self),
    value: "Verified Visitor",
    comment: "Badge shown next to a verified visitor's name"
)
```

```
# Rule 1: the localized permission string lives here, not in Info.plist.
# de.lproj/InfoPlist.strings
"NSCameraUsageDescription" = "Erlaube den Zugriff auf die Kamera, um Besucherausweise zu scannen.";
"CFBundleDisplayName" = "Besucherprotokoll";
```

## Non-Compliant Example

```swift
// violates Rule 6 -- looks up "Verified Visitor" in the HOST APP's bundle,
// misses, and falls back to displaying the key. In English the key and the
// text are identical, so this looks perfect until someone runs it in German.
struct VisitorBadge: View {
    var body: some View {
        Text("Verified Visitor")
    }
}
```

```xml
<!-- violates Rule 1 -- editing Info.plist after localizations exist changes
     the string for nobody who has a matching InfoPlist.strings. -->
<key>NSCameraUsageDescription</key>
<string>Allow camera access to scan visitor badges.</string>
```

```swift
// violates Rule 8 -- declared before any .lproj exists, so the package
// fails to build until localized resources are added.
let package = Package(
    name: "VisitorKit",
    defaultLocalization: "en",
    targets: [.target(name: "VisitorKit")]   // no Resources/ directory yet
)
```
Omits the bundle in package code so lookup silently targets the host app and falls back to returning the key (Rule 6); edits `Info.plist` for a value that localized strings files already override (Rule 1); and declares `defaultLocalization` before the localized resources Xcode then requires (Rule 8).

## Dependencies

- `string-catalogs-and-extraction` -- `InfoPlist.xcstrings` is a String Catalog and inherits its extraction and state behavior.

## References

- [Apple Developer — Adding support for languages and regions](https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions)
- [Apple Developer — Adding resources to localizations](https://developer.apple.com/documentation/xcode/adding-resources-to-localizations)
- [Apple Developer — Localizing assets in a catalog](https://developer.apple.com/documentation/xcode/localizing-assets-in-a-catalog)
- [Apple Developer — Localizing package resources](https://developer.apple.com/documentation/xcode/localizing-package-resources)
- [Apple Developer — Bundling resources with a Swift package](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package)
- [Apple Developer — Bundle](https://developer.apple.com/documentation/foundation/bundle)
- [Apple Developer — Bundle.localizedString(forKey:value:table:)](https://developer.apple.com/documentation/foundation/bundle/localizedstring(forkey:value:table:))
- [Apple Developer — CFBundleDisplayName](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledisplayname)
- [Apple Developer — CFBundleName](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundlename)
- [Apple Developer — Package.defaultLocalization](https://developer.apple.com/documentation/packagedescription/package/defaultlocalization)
- [Apple Developer — About Information Property List Files (archived)](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html)
- [WWDC23 — Discover String Catalogs](https://developer.apple.com/videos/play/wwdc2023/10155/)
```

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/localization/localized-resources-and-infoplist.md --type knowledge
```

---

## Task 8: Skill — `skills/localization/SKILL.md`

**Files:**
- Create: `skills/localization/SKILL.md`

- [ ] **Step 1: Create the file**

Follow the native Skill format used by every other domain skill: real YAML frontmatter with all twelve required metadata fields (`name`, `description`, `id`, `title`, `version`, `status`, `artifact_type`, `domain`, `routes`, `related`, `last_updated`), then `## Purpose`, `## Routing`, `## Stop Conditions`. Model the `description` on `skills/testing/SKILL.md` — a single long line naming the routed topics, the concrete symbols that trigger it, the v1 exclusions, and a trailing `Triggers on …` list.

- `id: skill.localization.foundations`
- `title: Localization — Foundations`
- `domain: Localization`
- `routes:` all six contract IDs, in the order they appear in Tasks 2–7
- `related: []`
- `last_updated: 2026-08-07`

`## Routing` maps each of the six contracts, all paths relative to `knowledge/localization/`:

- Creating or populating a `.xcstrings` String Catalog; string extraction and the literal requirement; translator comments; New/Needs Review/Translated/Stale states; explicit keys vs. value-as-key; manually-managed entries; "Don't Translate"; migrating a `.strings`/`.stringsdict` table → `string-catalogs-and-extraction.md`
- Calling `String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey`, `Text`/`Text(verbatim:)`, `AttributedString(localized:)`, or `NSLocalizedString`; format specifiers and positional arguments; the `locale:` parameter → `localized-string-apis.md`
- Varying a string by count or device; CLDR plural categories; substitutions; `.stringsdict`; `^[…](inflect: true)` → `plural-and-device-variations.md`
- `Locale.current`/`autoupdatingCurrent`; `preferredLanguages`/`preferredLocalizations`; `Locale.Language`/`Locale.Region`; `CFBundleDevelopmentRegion`; the `.lproj` fallback chain; per-app language → `locale-and-language-resolution.md`
- RTL layout; `\.layoutDirection`; `flipsForRightToLeftLayoutDirection`; `semanticContentAttribute`; `effectiveUserInterfaceLayoutDirection`; SF Symbols mirroring; `characterDirection`; RTL pseudolanguages → `layout-direction-and-rtl-apis.md`
- `InfoPlist.xcstrings`/`InfoPlist.strings`; `CFBundleDisplayName`/`CFBundleName`; `.lproj` structure; localizing assets; `Bundle.module`/`defaultLocalization`; `Bundle.localizedString(forKey:value:table:)` → `localized-resources-and-infoplist.md`

Close `## Routing` with the standard line: "Never load more than the contracts relevant to the specific question."

`## Stop Conditions` MUST name, as boundaries to report rather than answer:

- Adding a language to an Xcode project, target localization settings, and `.xcloc`/XLIFF export-and-import — `xcode` territory, not yet built; report the boundary.
- The iOS 18 Translation framework (`TranslationSession`, `.translationTask`, `.translationPresentation`) — a real, documented capability deliberately out of scope; do not fabricate guidance and do not claim it does not exist.
- Source-copy wording, capitalization, punctuation, and international representation/formatting rules — owned by `style-guide`.
- Date, time, number, and measurement formatting — owned by `foundation`.
- RTL visual-design decisions — owned by `human-interface-guidelines` (`right-to-left`).
- App Store Connect localized metadata; APNs `loc-key`/`loc-args` payloads; App Shortcuts phrase and `AppEnum` localization (owned by `app-intents`); macOS/watchOS/tvOS-specific behavior — all out of scope entirely.
- The `.xcstrings` internal JSON structure — Apple publishes no schema; do not assert field names.

- [ ] **Step 2: Validate**

```bash
python3 scripts/validate_artifact.py skills/localization/SKILL.md --type skill
```

---

## Task 9: Documentation updates

All four in the same commit as the domain, per `CLAUDE.md`.

**Files:**
- Modify: `docs/architecture/domain-map.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `skills/index.md`

- [ ] **Step 1: `docs/architecture/domain-map.md` — rewrite the Tier 2 row**

Replace the `| Localization | localization | Language, terminology | Localization and translation workflow conventions |` row's Initial Scope and Owns cells with detailed v1 wording in the style of every other completed Tier 2 row: the six KC topics, the Xcode 16+/iOS 17+ baseline, and the Excluded list (Xcode project configuration and XLIFF export-import deferred to `xcode`; iOS 18 Translation framework; `style-guide`/`foundation`/`human-interface-guidelines` boundaries; App Store Connect metadata; APNs `loc-key`; App Shortcuts phrases; non-iOS platforms).

- [ ] **Step 2: `docs/architecture/domain-map.md` — append to the "Completed:" paragraph**

Append the `localization` clause as the **seventeenth Tier 2 domain**, matching the existing sentence style, and state plainly that this closes out **all of Tier 2**.

- [ ] **Step 3: `docs/architecture/domain-map.md` — add four Cross-Domain Notes bullets**

1. **vs. `human-interface-guidelines` — angle-split.** HIG's `right-to-left.md` owns the design layer (what mirrors, numerals, icon-flip decisions); `localization` owns the API layer. Same pattern as `accessibility` vs. `human-interface-guidelines`. Note explicitly that this **closes the seam** `right-to-left.md`'s own Excluded section left open — "SF Symbols' built-in RTL-variant mechanics specifically is not yet covered by any current contract" — which `layout-direction-and-rtl-apis` now covers via SF Symbols' documented name-driven mirroring.
2. **vs. `foundation` — clean handoff.** `localization` owns where a `Locale` comes from and how it resolves; `foundation` owns passing it to a formatter. No correction needed on `foundation`'s side — its scope cell already excluded "Locale/Bundle localization" before this domain existed.
3. **vs. `style-guide` — clean handoff.** `style-guide` owns what the source copy says and how it is written and formatted, including `international-style`, `international-formatting`, and `units-of-measure`, none of which touch an API; `localization` owns extraction, storage, variation, and runtime resolution.
4. **vs. `xcode` — deferred, not yet resolved.** Project-language configuration, target localization settings, and the `.xcloc`/XLIFF round trip belong to `xcode` by domain type but are not in its v1. Word it in the style of the existing unresolved `arkit`/`realitykit` note.

> Note: no fifth bullet for `accessibility`. Verification during planning confirmed `knowledge/accessibility/accessibility-labels.md` Rule 5 only directs agents to "localize accessibility labels through the same localization pipeline as visible strings" — it points at the pipeline without describing it, so a one-way `related:` reference is sufficient and no boundary is in dispute.

- [ ] **Step 4: `README.md`**

Add the Skills bullet in the established format — ``- **`localization`** — one-line description. → [SKILL.md](skills/localization/SKILL.md)`` — with no examples, routing tables, or scope caveats. Then add one `## What's New` line at the top (`2026-08-07 — …`) and **trim the section to its three most recent bullets**, dropping the oldest regardless of date.

- [ ] **Step 5: `CHANGELOG.md`**

Add an entry under `## [Unreleased]`. Do **not** add a `[2.1.0]` release header here — per repo history the release-version bump is a separate chore commit (Task 10, Step 4).

- [ ] **Step 6: `skills/index.md`**

Add one Discovery Rules row with the trigger keywords: `String Catalog`, `.xcstrings`, `String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey`, `NSLocalizedString`, `Text(verbatim:)`, `AttributedString(localized:)`, `localization`, `localize`, `pluralization`, `stringsdict`, `NSStringLocalizedFormatKey`, `Locale`, `Locale.current`, `autoupdatingCurrent`, `preferredLanguages`, `preferredLocalizations`, `Locale.Language`, `characterDirection`, `lproj`, `InfoPlist.xcstrings`, `layoutDirection`, `RTL`, `right-to-left`, `semanticContentAttribute`, `flipsForRightToLeftLayoutDirection`, `effectiveUserInterfaceLayoutDirection`, `CFBundleDevelopmentRegion`, `CFBundleDisplayName`, `Bundle.module`, `defaultLocalization`.

---

## Task 10: Validation and completion

- [ ] **Step 1: Validate every new artifact**

```bash
python3 scripts/validate_artifact.py references/apple/localization.md --type reference
python3 scripts/validate_artifact.py knowledge/localization/string-catalogs-and-extraction.md --type knowledge
python3 scripts/validate_artifact.py knowledge/localization/localized-string-apis.md --type knowledge
python3 scripts/validate_artifact.py knowledge/localization/plural-and-device-variations.md --type knowledge
python3 scripts/validate_artifact.py knowledge/localization/locale-and-language-resolution.md --type knowledge
python3 scripts/validate_artifact.py knowledge/localization/layout-direction-and-rtl-apis.md --type knowledge
python3 scripts/validate_artifact.py knowledge/localization/localized-resources-and-infoplist.md --type knowledge
python3 scripts/validate_artifact.py skills/localization/SKILL.md --type skill
```

Every line must print `PASS`.

- [ ] **Step 2: Full test suite and plugin validation**

```bash
python3 -m unittest tests/test_validate_artifact.py -v
claude plugin validate .
```

- [ ] **Step 3: Cross-reference audit**

Confirm every `related:`/`depends_on:` ID resolves to a real artifact. The four cross-domain IDs used are `knowledge.human-interface-guidelines.right-to-left`, `knowledge.sf-symbols.symbol-variants`, `knowledge.app-store-review-guidelines.permission-usage-strings`, and `knowledge.foundation.date-time-formatting`/`knowledge.foundation.measurement-and-unit-formatting` — all verified to exist during planning, but re-check after writing.

Also confirm no `localization` contract restates Rules owned by `human-interface-guidelines`, `foundation`, or `style-guide` — cross-reference only.

- [ ] **Step 4: Release version bump (separate commit)**

After the domain commit lands, bump all five release-version files to **2.1.0** together, and verify they match exactly:

- `README.md` (the `Version:` line)
- `npx/README.md` (the `Version:` line)
- `npx/package.json` (`version`)
- `.claude-plugin/plugin.json` (`version`)
- `CHANGELOG.md` (promote `[Unreleased]` content to `## [2.1.0] - 2026-08-07`)

No `npm publish` — `npx/bin/install.js` and the installer's behavior are unchanged, and content reaches users from `main`.

- [ ] **Step 5: Open the PR**

Single PR from `feature/localization-domain`. The description should state that this is the seventeenth and final Tier 2 domain and that Tier 2 is now complete, and should call out the two sourcing caveats recorded in Task 7 so a reviewer does not have to rediscover them.
