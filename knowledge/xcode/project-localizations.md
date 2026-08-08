# Project Localizations

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.xcode.project-localizations
artifact_type: knowledge
title: Project Localizations
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines how a language and region is added to an Xcode project — the project-level Localizations list, the language ID that names the .lproj folder, the resource-selection sheet that decides what is localizable, and the Base entry Xcode adds by default.
domain: Xcode
tags:
  - xcode
  - localization
  - project-configuration
references:
  - https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions
  - https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts
depends_on: []
related:
  - knowledge.xcode.localization-export-import
  - knowledge.xcode.schemes-and-targets
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent adds a language and region
to an Xcode project, so that the localization the app ships is the one
the project was configured for and every resource intended for
translation is actually marked as localizable.

## Scope

### Included

-   Where localizations are added: the project editor's Info tab, under Localizations
-   The language ID, and how a regional variant is named
-   The resource-selection sheet, and what it decides
-   `Base` and the development language, which Xcode adds by default
-   What adding a localization does to the project's file structure

### Excluded

-   Handing the localizations to translators and taking them back — see `localization-export-import`
-   String Catalogs, `String(localized:)`, plural variation, `Locale` resolution, `InfoPlist.xcstrings`, `Bundle.module`, and the runtime `.lproj` fallback chain — owned by the `localization` domain
-   Right-to-left visual design — owned by the `human-interface-guidelines` domain
-   Storyboard and XIB localization beyond what Apple's page states about the strings file Xcode adds — Storyboards and XIBs are Excluded from the `uikit` domain

## Rules

### Rule 1

Agents MUST add a localization at the project level, not per target. Per
Apple's documentation: "In the project editor, select the project name
under Project, and click Info. Under Localizations, click the Add button
(+), then choose a language and region combination from the pop-up menu."
There is no per-target equivalent; a target participates by having its
resources selected in Rule 3's sheet.

### Rule 2

Agents MUST identify a localization by its language ID, including the
region when one is intended, because that ID is what names the directory
on disk. Per Apple's documentation: "For regional variants and scripts,
the region appears in parentheses followed by the language ID in
parentheses — for example, English (India) (en-IN) where en-IN is the
language ID." And: "The name of the folder is the language ID followed by
the `.lproj` file extension — for example, `de.lproj` if you choose
German (de) from the localization menu." Adding "German" and expecting
`de-AT.lproj` produces neither an error nor the directory.

### Rule 3

Agents MUST select every resource intended for translation in the sheet
Xcode presents, because that sheet is what marks a file localizable. Per
Apple's documentation: "If you have localizable resources in the project,
select the resource files that you want to localize in the sheet that
appears, and click Finish. For example, select images, audio, strings,
and `.stringsdict` files that you add to your project." A resource left
unselected is not an error and produces no warning — it simply never
appears for translation.

### Rule 4

Agents MUST NOT remove the `Base` entry from the Localizations list. Per
Apple's documentation: "Xcode adds the `Base` and the development
language to the localization table by default. Use the Base localization
for resources that support string substitution at runtime, such as
storyboard, XIB, and Siri intent definition files." `Base` is where those
resources' substitutable content lives; deleting it removes the source
the per-language strings files are generated against.

### Rule 5

Agents MUST expect the first localization added to restructure existing
resources, and MUST NOT read a later addition's small diff as evidence
the first one was reviewed. Per Apple's documentation: "The first time
you add a localization, Xcode changes every resource that you want to
localize into a group containing the original file and a
localization-specific version. The next time you add a localization,
Xcode adds another localization-specific file to the group."

## Compliant Example

-   ✓ Adding Arabic (ar) and English (India) (en-IN) to a project: both are added under Project > Info > Localizations, the asset-catalog images and the `.stringsdict` are checked in the resource sheet, and `Base` is left in place. Xcode creates `ar.lproj` and `en-IN.lproj`, and the first addition's large diff — every localizable resource becoming a group — is reviewed rather than skimmed. (Rules 1, 2, 3, 5)

## Non-Compliant Example

-   ✗ German is added, the resource sheet is dismissed without checking the onboarding audio narration, and `Base` is deleted "because the app is SwiftUI and has no storyboards." The narration ships in English to German users with no build warning, and the app's Siri intent definition loses the localization its substitutable phrases were generated from. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — Adding support for languages and regions](https://developer.apple.com/documentation/xcode/adding-support-for-languages-and-regions)
-   [Apple Developer — Choosing localization regions and scripts](https://developer.apple.com/documentation/xcode/choosing-localization-regions-and-scripts)
