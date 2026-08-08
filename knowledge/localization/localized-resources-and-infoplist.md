# Localized Resources and Info.plist

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.localization.localized-resources-and-infoplist
artifact_type: knowledge
title: Localized Resources and Info.plist
version: 1.0.0
status: Approved
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
  - https://developer.apple.com/documentation/xcode/localizing-assets-in-a-catalog
  - https://developer.apple.com/documentation/xcode/localizing-package-resources
  - https://developer.apple.com/documentation/foundation/bundle
  - https://developer.apple.com/documentation/foundation/bundle/localizedstring(forkey:value:table:)
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
last_updated: 2026-08-08
```

## Intent

This contract governs localizing everything that is not a string literal in source code: Info.plist values, the app's name, asset-catalog resources, and resources shipped inside a framework or Swift package. Its central claim is that these surfaces fail *silently* -- a missing localized resource or a wrong bundle produces plausible English output rather than an error.

Sourcing note: Apple's current Xcode Localization documentation hub does not cover Info.plist localization, and no current reference page documents `InfoPlist.xcstrings`. The rules below draw on Apple's WWDC23 session and Apple's archived Info.plist Key Reference, which remains an accurate description of the runtime mechanism because String Catalogs compile into exactly the `InfoPlist.strings` artifact it describes.

## Scope

### Included

- Info.plist localization via `InfoPlist.strings`/`InfoPlist.xcstrings`, and the lookup order between them and `Info.plist`
- Permission usage descriptions and app-name keys as the values that most need localizing; `CFBundleDisplayName` vs. `CFBundleName` and the length constraint
- `.lproj` structure, Base localization, and the resource search order
- Per-asset catalog localization and which asset types support it
- Swift-package and framework localization (`defaultLocalization`, `.lproj` layout rules, `Bundle.module`) and `Bundle.localizedString(forKey:value:table:)`

### Excluded

- Source-code string extraction and catalog states -- see `string-catalogs-and-extraction`; which string API to call -- see `localized-string-apis`; which localization the app resolved to -- see `locale-and-language-resolution`
- The English wording of a permission usage string -- owned by `knowledge.app-store-review-guidelines.permission-usage-strings`; this contract owns getting that string translated
- Adding a language to the project -- owned by `knowledge.xcode.project-localizations`; `.xcloc`/XLIFF export-import -- owned by `knowledge.xcode.localization-export-import`

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
let package = Package(name: "VisitorKit",
                      defaultLocalization: "en",
                      targets: [.target(name: "VisitorKit")])

// Rule 6: package code must name its own bundle; the default is the app's.
struct VisitorBadge: View {
    var body: some View { Text("Verified Visitor", bundle: .module) }
}

// Rule 6, framework form.
let title = NSLocalizedString("badge.verified",
                              bundle: Bundle(for: VisitorBadgeController.self),
                              value: "Verified Visitor", comment: "Verified badge")

// Rule 1: localized plist values live in de.lproj/InfoPlist.strings, not in
// Info.plist:  "NSCameraUsageDescription" = "Erlaube den Zugriff…";
```

## Non-Compliant Example

```swift
// violates Rule 6 -- looks up "Verified Visitor" in the HOST APP's bundle,
// misses, and falls back to displaying the key. In English the key and the
// text are identical, so this looks perfect until someone runs it in German.
struct VisitorBadge: View {
    var body: some View { Text("Verified Visitor") }
}

// violates Rule 8 -- declared before any .lproj exists, so the package fails
// to build until localized resources are added.
let package = Package(name: "VisitorKit", defaultLocalization: "en",
                      targets: [.target(name: "VisitorKit")])  // no Resources/
```
Omits the bundle in package code so lookup silently targets the host app and falls back to returning the key (Rule 6), and declares `defaultLocalization` before the localized resources Xcode then requires (Rule 8). Editing a `NSCameraUsageDescription` value directly in `Info.plist` once localizations exist is the third common form of this failure, and changes the string for nobody who has a matching localization (Rule 1).

## Dependencies

- `string-catalogs-and-extraction` -- `InfoPlist.xcstrings` is a String Catalog and inherits its extraction and state behavior.

## References

- [Apple Developer — Adding support for languages and regions](https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions) · [Adding resources to localizations](https://developer.apple.com/documentation/xcode/adding-resources-to-localizations) · [Localizing assets in a catalog](https://developer.apple.com/documentation/xcode/localizing-assets-in-a-catalog)
- [Apple Developer — Localizing package resources](https://developer.apple.com/documentation/xcode/localizing-package-resources) · [Bundling resources with a Swift package](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package) · [Package.defaultLocalization](https://developer.apple.com/documentation/packagedescription/package/defaultlocalization)
- [Apple Developer — Bundle](https://developer.apple.com/documentation/foundation/bundle) · [Bundle.localizedString(forKey:value:table:)](https://developer.apple.com/documentation/foundation/bundle/localizedstring(forkey:value:table:))
- [Apple Developer — CFBundleDisplayName](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledisplayname) · [CFBundleName](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundlename)
- [Apple Developer — About Information Property List Files (archived)](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html)
- [WWDC23 — Discover String Catalogs](https://developer.apple.com/videos/play/wwdc2023/10155/)
