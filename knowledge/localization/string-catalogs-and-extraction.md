# String Catalogs and Extraction

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.string-catalogs-and-extraction
artifact_type: knowledge
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
last_updated: 2026-08-07
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
- Explicit keys with a separate default value, versus using the development-language value as the key
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

// A key that cannot be derived from a literal at the call site. The literal
// below is what gets extracted; entries for the dynamic table are added by
// hand and marked manually managed so a build never removes them.          // Rule 3
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
let sectionTitle = String(localized: "Recent Visitors", comment: "Section header")
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
