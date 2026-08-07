---
name: localization
description: Route Apple-platform localization tasks to the correct Knowledge Contracts -- String Catalog (.xcstrings) mechanics, compiler-driven extraction and the string-literal requirement it depends on, translator comments, the New/Needs Review/Translated/Stale states, explicit keys vs. value-as-key, and manually-managed entries; the localized-string API surface (String(localized:), LocalizedStringResource for deferred cross-process resolution, LocalizedStringKey and SwiftUI's implicit Text literal localization, Text(verbatim:), AttributedString(localized:), format specifiers, NSLocalizedString); plural and device variation, the CLDR categories with other required, substitutions, and legacy .stringsdict; Locale and language resolution (current vs. autoupdatingCurrent, preferredLanguages vs. preferredLocalizations, Locale.Language/Locale.Region, CFBundleDevelopmentRegion, the .lproj fallback chain); layout-direction and RTL APIs including SF Symbols' name-driven mirroring; and localized resources (InfoPlist.xcstrings, .lproj structure, asset-catalog localization, Bundle.module, defaultLocalization). Use when writing String(localized:), LocalizedStringResource, LocalizedStringKey, Text("..."), Text(verbatim:), AttributedString(localized:), NSLocalizedString, adding or editing a .xcstrings file, varying a string by plural or device, editing a .stringsdict, reading Locale.current/autoupdatingCurrent/preferredLanguages/language/region, Bundle.preferredLocalizations/localizations/localizedString(forKey:value:table:), CFBundleDevelopmentRegion/CFBundleDisplayName/CFBundleName, InfoPlist.xcstrings, .lproj directories, Bundle.module, defaultLocalization, \.layoutDirection, flipsForRightToLeftLayoutDirection, semanticContentAttribute, effectiveUserInterfaceLayoutDirection, imageFlippedForRightToLeftLayoutDirection, or characterDirection. Baseline is Xcode 16+ with an iOS 17+ API surface. v1 excludes Xcode project-language configuration and .xcloc/XLIFF export-import (xcode domain), the iOS 18 Translation framework, source-copy wording rules (style-guide), date/number/measurement formatting (foundation), RTL visual-design guidance (human-interface-guidelines), App Store Connect localized metadata, APNs loc-key payloads, App Shortcuts phrase localization (app-intents), and macOS/watchOS/tvOS-specific behavior. Triggers on localization, localize, String Catalog, xcstrings, stringsdict, pluralization, CLDR, Locale, preferredLanguages, preferredLocalizations, lproj, InfoPlist.xcstrings, Bundle.module, layoutDirection, RTL, right-to-left, semanticContentAttribute, characterDirection.
id: skill.localization.foundations
title: Localization — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Localization
routes: [knowledge.localization.string-catalogs-and-extraction, knowledge.localization.localized-string-apis, knowledge.localization.plural-and-device-variations, knowledge.localization.locale-and-language-resolution, knowledge.localization.layout-direction-and-rtl-apis, knowledge.localization.localized-resources-and-infoplist]
related: []
last_updated: 2026-08-07
---

# Localization — Foundations Skill

## Purpose

Route Apple-platform localization implementation tasks to the minimum
required Knowledge Contracts. v1 covers how an app's user-facing strings
and resources are extracted, stored, varied, and resolved across languages
and regions -- not Xcode project configuration, translator XLIFF workflow,
runtime content translation, source-copy style rules, value formatting, or
RTL visual design. Baseline is Xcode 16+ with an iOS 17+ API surface;
String Catalogs impose no deployment-target cost, since `.xcstrings`
compiles to `.strings`/`.stringsdict` at build time.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/localization/.

-   Creating or populating a `.xcstrings` String Catalog; extraction and
    the literal requirement; translator `comment:`; New/Needs
    Review/Translated/Stale states; explicit keys vs. value-as-key;
    manually-managed entries; "Don't Translate"; migrating a
    `.strings`/`.stringsdict` table -> string-catalogs-and-extraction.md
-   Calling `String(localized:)`, `LocalizedStringResource`,
    `LocalizedStringKey`, `Text`/`Text(verbatim:)`,
    `AttributedString(localized:)`, or `NSLocalizedString`; format
    specifiers; the `locale:` parameter -> localized-string-apis.md
-   Varying a string by count or device; CLDR plural categories;
    substitutions; `.stringsdict`; `^[...](inflect: true)`
    -> plural-and-device-variations.md
-   `Locale.current`/`autoupdatingCurrent`;
    `preferredLanguages`/`preferredLocalizations`;
    `Locale.Language`/`Locale.Region`; `CFBundleDevelopmentRegion`; the
    `.lproj` fallback chain -> locale-and-language-resolution.md
-   RTL layout; `\.layoutDirection`;
    `flipsForRightToLeftLayoutDirection`; `semanticContentAttribute`;
    `effectiveUserInterfaceLayoutDirection`; SF Symbols mirroring;
    `characterDirection`; RTL pseudolanguages
    -> layout-direction-and-rtl-apis.md
-   `InfoPlist.xcstrings`/`InfoPlist.strings`;
    `CFBundleDisplayName`/`CFBundleName`; `.lproj` structure; localizing
    assets; `Bundle.module`/`defaultLocalization`;
    `Bundle.localizedString(forKey:value:table:)`
    -> localized-resources-and-infoplist.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/localization/ -- do not guess or fall back to general
knowledge. Adding a language to an Xcode project, target localization
settings, and `.xcloc`/XLIFF export-and-import are `xcode` territory and
not yet built -- report the boundary rather than answer here. The iOS 18
Translation framework (`TranslationSession`, `.translationTask`,
`.translationPresentation`) is a real, documented capability deliberately
out of scope -- do not fabricate guidance for it, and do not claim it does
not exist. Source-copy wording, capitalization, punctuation, and
international representation/formatting rules are owned by `style-guide`;
date, time, number, and measurement formatting by `foundation`; RTL
visual-design decisions by `human-interface-guidelines` (`right-to-left`).
App Store Connect localized metadata, APNs `loc-key`/`loc-args` payloads,
App Shortcuts phrase and `AppEnum` localization (owned by `app-intents`),
and macOS/watchOS/tvOS-specific behavior are out of scope entirely. Apple
publishes no schema for the `.xcstrings` format -- never assert its
internal JSON field names.
