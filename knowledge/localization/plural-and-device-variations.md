# Plural and Device Variations

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.plural-and-device-variations
artifact_type: knowledge
title: Plural and Device Variations
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how a single catalog entry varies by grammatical number and by device -- the CLDR plural categories with other required and the applicable set language-dependent, Vary by Plural and Vary by Device, substitutions for strings with more than one varying value, the legacy stringsdict form a catalog compiles into, and why runtime inflection is a separate mechanism from plural variation.
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
last_updated: 2026-08-07
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

Agents MUST NOT treat `^[…](inflect: true)` as a pluralization mechanism. Automatic grammatical agreement is a runtime `AttributedString` transform governed by `InflectionRule`, limited to the languages Apple's grammar engine supports; plural variation is catalog data resolved for every language through CLDR categories. Apple documents the inflection markup with localized attributed strings for grammatical agreement, independently of the plural-variation mechanism described in "Localizing strings that contain plurals."

### Rule 7

Agents MUST treat `.stringsdict` as legacy for *authoring* only, not as a removed format. Per Apple's documentation: "In Xcode 15 and later, string catalogs are the recommended way to localize strings that contain plurals." Per Apple's WWDC23 session, at build time String Catalogs "compile to .strings and .stringsdict files" -- which is why Apple's `.stringsdict` page remains the reference for plural-category semantics. When maintaining an existing `.stringsdict`, agents MUST read `NSStringLocalizedFormatKey` as "A formatted string that contains variables. To replace the string with a plural rule, precede the variable with the `%#@` characters and follow it by the `@` character, as in `%#@homes@`", with `NSStringFormatSpecTypeKey` whose "only possible value is `NSStringPluralRuleType`".

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
let hint = String(localized: "Tap to learn more",
                  comment: "Footer hint; varies by device -- click on macOS")
```

## Non-Compliant Example

```swift
// violates Rules 1 and 2 -- plural selection in code. Correct only in
// languages with exactly two forms; Russian needs one/few/many and Arabic
// needs six, so both get the wrong wording with no error anywhere.
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
