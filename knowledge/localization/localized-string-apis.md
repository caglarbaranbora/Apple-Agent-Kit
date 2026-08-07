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
- `AttributedString(localized:)` and Markdown carried in translations; `NSLocalizedString`'s remaining role

### Excluded

- How the string got into the catalog, keys, comments, and translation states -- see `string-catalogs-and-extraction`
- Plural and device variation of a string -- see `plural-and-device-variations`
- Which `Locale` the app resolved to -- see `locale-and-language-resolution`
- Looking a string up from a package or framework bundle -- see `localized-resources-and-infoplist`; date, number, and measurement formatting -- owned by `foundation`

## Rules

### Rule 1

Agents MUST NOT use the `locale:` parameter to select a language, because it does not do that. Per Apple's documentation for `String(localized:table:bundle:locale:comment:)`, `locale` is "The locale to use when localizing interpolated values, such as numbers. This doesn't change which locale the system uses to look up the localized string." The documented way to look a string up in a different locale is to set the locale on a `LocalizedStringResource` first: per Apple's documentation for `String(localized:)`, "Alter the resource's `locale` prior to calling this method if you want to localize this string in a different locale than the process that creates the `LocalizedStringResource`."

### Rule 2

Agents MUST pass a string *literal* to SwiftUI's localizing initializers and MUST treat a string variable as explicitly non-localized. Per Apple's documentation for `LocalizedStringKey`: "Passing a `String` variable to these initializers avoids localization, which is usually appropriate when the variable contains a user-provided value," and "to localize the value of a string variable, create a new `LocalizedStringKey` instance from it." Per Apple's documentation for `Text.init(_:tableName:bundle:comment:)`: "When you initialize a text view with a string variable rather than a string literal, the view triggers the `init(_:)` initializer instead, because it assumes you don't want localization." To opt a literal out deliberately, use `Text(verbatim:)`, which "Creates a text view that displays a string literal without localization."

### Rule 3

Agents MUST use `LocalizedStringResource` rather than an eagerly-resolved `String` whenever the string will be read in another process, and MUST NOT resolve it to a `String` before handing it over. Per Apple's documentation, initializers taking `String.LocalizationValue` "lookup the localized string immediately. If you want to perform the lookup at a later time, use this `LocalizedStringResource` type… This approach allows you to provide localizable strings to an entirely separate process, which may use a different locale." Apple names the canonical case: "The App Intents framework uses `LocalizedStringResource` to perform a late resolution of localized strings. This allows the Siri UI to potentially use different localization preferences than the app providing the intent."

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
Text("Recent Visitors")                      // Rule 2: literal -> localized
Text(verbatim: visitorName)                  // Rule 2: opt-out, user-provided
Text("You had \(visitCount) visits today")   // Rule 4: one interpolated string

// Rule 3: hand a resource, not a resolved String, to another process.
struct ShowVisitorsIntent: AppIntent {
    static var title: LocalizedStringResource = "Show Recent Visitors"
}

// Rule 1: `locale:` formats the interpolated number; the *text* still comes
// from the app's resolved localization, not from de_DE.
let caption = String(localized: "You had \(visitCount) visits today",
                     locale: Locale(identifier: "de_DE"),
                     comment: "Caption under the visitor chart")
```

## Non-Compliant Example

```swift
// violates Rule 1 -- expects German text, gets the app's current language
// with German number formatting. Passes any test that only asserts the number.
let german = String(localized: "Welcome back", locale: Locale(identifier: "de"))

// violates Rule 2 -- refactoring the literal into a constant silently
// un-localizes it. No warning, and English output is unchanged.
let heading = "Recent Visitors"
Text(heading)

// violates Rule 4 -- word order, inflection, and capitalization are all wrong
// in languages that don't follow English order.
Text(String(localized: "You had ") + "\(visitCount)" + String(localized: " visits today"))

// violates Rule 3 -- resolving eagerly defeats late resolution; Siri now
// shows the string in the app's locale, not the user's.
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
- [Apple Developer — Text.init(_:tableName:bundle:comment:)](https://developer.apple.com/documentation/swiftui/text/init(_:tablename:bundle:comment:)) · [Text.init(verbatim:)](https://developer.apple.com/documentation/swiftui/text/init(verbatim:))
- [Apple Developer — NSLocalizedString](https://developer.apple.com/documentation/foundation/nslocalizedstring(_:tablename:bundle:value:comment:))
- [Apple Developer — AttributedString](https://developer.apple.com/documentation/foundation/attributedstring)
- [Apple Developer — Xcode 16 Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes)
- [WWDC22 — Building global apps: Localization by example](https://developer.apple.com/videos/play/wwdc2022/10110/)
