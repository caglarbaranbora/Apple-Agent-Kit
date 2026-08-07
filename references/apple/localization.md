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
https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes
https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes
https://developer.apple.com/documentation/swift/string/init(localized:table:bundle:locale:comment:)
https://developer.apple.com/documentation/swift/string/init(localized:defaultvalue:table:bundle:locale:comment:)
https://developer.apple.com/documentation/swift/string/init(localized:)
https://developer.apple.com/documentation/foundation/localizedstringresource
https://developer.apple.com/documentation/foundation/nslocalizedstring(_:tablename:bundle:value:comment:)
https://developer.apple.com/documentation/foundation/attributedstring
https://developer.apple.com/documentation/swiftui/localizedstringkey
https://developer.apple.com/documentation/swiftui/text/init(_:tablename:bundle:comment:)
https://developer.apple.com/documentation/foundation/locale/current
https://developer.apple.com/documentation/foundation/locale/autoupdatingcurrent
https://developer.apple.com/documentation/foundation/locale/preferredlanguages
https://developer.apple.com/documentation/foundation/locale/language-swift.struct/characterdirection
https://developer.apple.com/documentation/foundation/bundle
https://developer.apple.com/documentation/foundation/bundle/preferredlocalizations
https://developer.apple.com/documentation/foundation/bundle/localizedstring(forkey:value:table:)
https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledevelopmentregion
https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledisplayname
https://developer.apple.com/documentation/packagedescription/package/defaultlocalization
https://developer.apple.com/documentation/swiftui/layoutdirection
https://developer.apple.com/documentation/uikit/uiview/semanticcontentattribute
https://developer.apple.com/documentation/uikit/uiview/effectiveuserinterfacelayoutdirection
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

Reference index for Apple's localization documentation, scoped to this domain's v1: String Catalog (`.xcstrings`) mechanics and compiler-driven extraction, including the literal-argument requirement it depends on, translator comments, translation states, explicit keys vs. value-as-key, and manually-managed entries; the localized-string API surface (`String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey` and SwiftUI's implicit `Text` literal localization, `AttributedString(localized:)`, and the remaining role of `NSLocalizedString`); plural and device variation, the CLDR categories and their language-dependence, substitutions, and the legacy `.stringsdict` form; `Locale` and language resolution (`current` vs. `autoupdatingCurrent`, `preferredLanguages` vs. `preferredLocalizations`, the `Locale.Language`/`Locale.Region` split, development region, and the `.lproj` fallback chain); layout-direction and RTL APIs across SwiftUI and UIKit including SF Symbols' name-driven mirroring; and localized resources (`InfoPlist.xcstrings`, `.lproj` structure, asset-catalog localization, Swift-package `defaultLocalization`/`Bundle.module`, and non-main-bundle lookup).

Baseline is Xcode 16+ with an iOS 17+ API surface. String Catalogs carry no deployment-target requirement — per WWDC23, `.xcstrings` compiles to `.strings` and `.stringsdict` at build time, so "you can start using String Catalogs right away without having to update your minimum deployment target." Xcode 16 specifically, because marking a string "Don't Translate", stale-string build warnings, format-specifier conflict diagnostics, and the `xcstringstool` replacement for the deprecated `genstrings` do not exist in Xcode 15. `Locale.Language`, `Locale.Region`, and `Locale.Language.characterDirection` are iOS 16+, while `Locale.languageCode`, `Locale.regionCode`, and `Locale.characterDirection(forLanguage:)` are deprecated as of iOS 16 — already dead at this baseline despite remaining the form most third-party material uses.

Out of scope for v1: the Xcode project-configuration side of localization (adding a project language, target localization settings, and the `.xcloc`/XLIFF export-and-import round trip), which is `xcode`'s territory and deferred to a future `xcode` expansion; the iOS 18 Translation framework (`TranslationSession`, `.translationTask`, `.translationPresentation`), a real and documented capability deliberately excluded because it translates user content at runtime rather than shipping the app's own text pre-translated, and requires iOS 18; source-copy wording, capitalization, and international representation/formatting rules (owned by `style-guide`); date/time/number/measurement formatting mechanics (owned by `foundation`); RTL visual-design guidance (owned by `human-interface-guidelines`); App Store Connect localized metadata; APNs `loc-key`/`loc-args` server payloads (already out of scope for `usernotifications`); App Shortcuts phrase and `AppEnum` localization (owned by `app-intents`); and macOS/watchOS/tvOS-specific behavior.

Sourcing note: Apple publishes no schema reference for the `.xcstrings` file format — WWDC23 describes it only as "JSON files under the hood." This reference and the contracts using it therefore describe the String Catalog through its editor affordances and public APIs, never through JSON field names. Separately, Info.plist localization is covered by none of the articles in Apple's current Xcode Localization hub; its only current-era source is the WWDC23 transcript, and its only prose specification is the archived Info.plist Key Reference listed above.

## Primary Topics

- String Catalog mechanics, build-time extraction, the "Use Compiler to Extract Swift Strings" (`SWIFT_EMIT_LOC_STRINGS`) requirement, translator comments, translation states (New / Needs Review / Translated / Stale), "Don't Translate", explicit keys vs. value-as-key, and manually-managed entries
- `String(localized:)` overloads, `String.LocalizationValue`, `LocalizedStringResource` deferred resolution, `LocalizedStringKey` and SwiftUI implicit `Text` localization, `Text(verbatim:)`, `AttributedString(localized:)` and Markdown-in-translations, format specifiers and positional arguments, `NSLocalizedString`
- Plural variation and the CLDR categories (`zero`/`one`/`two`/`few`/`many`/`other`, with `other` required and the applicable set language-dependent), device variation, substitutions, `.stringsdict` (`NSStringLocalizedFormatKey`, `NSStringFormatSpecTypeKey`), and the distinction from `^[…](inflect: true)` runtime inflection
- `Locale.current` vs. `Locale.autoupdatingCurrent` and the three inputs defining both, `Locale.preferredLanguages` vs. `Bundle.preferredLocalizations`, `Bundle.preferredLocalizations(from:)`, `Locale.Language`/`Locale.Region`, `CFBundleDevelopmentRegion`, the `.lproj` fallback chain, and per-app language settings
- SwiftUI `LayoutDirection`/`\.layoutDirection`/`flipsForRightToLeftLayoutDirection(_:)`, leading/trailing over left/right, UIKit `semanticContentAttribute`/`effectiveUserInterfaceLayoutDirection`, `UIImage.imageFlippedForRightToLeftLayoutDirection()`, asset-catalog `language-direction`, SF Symbols name-driven mirroring, `Locale.Language.characterDirection`, and the RTL pseudolanguages
- `InfoPlist.xcstrings`/`InfoPlist.strings`, `CFBundleDisplayName`/`CFBundleName`, `.lproj` structure and Base localization, per-asset catalog localization, Swift-package `defaultLocalization`/`Bundle.module`, and `Bundle.localizedString(forKey:value:table:)`

## Used By

- knowledge/localization/string-catalogs-and-extraction.md ([[knowledge/localization/string-catalogs-and-extraction]])
- knowledge/localization/localized-string-apis.md ([[knowledge/localization/localized-string-apis]])
- knowledge/localization/plural-and-device-variations.md ([[knowledge/localization/plural-and-device-variations]])
- knowledge/localization/locale-and-language-resolution.md ([[knowledge/localization/locale-and-language-resolution]])
- knowledge/localization/layout-direction-and-rtl-apis.md ([[knowledge/localization/layout-direction-and-rtl-apis]])
- knowledge/localization/localized-resources-and-infoplist.md ([[knowledge/localization/localized-resources-and-infoplist]])
- skills/localization/SKILL.md ([[skills/localization/SKILL]])
