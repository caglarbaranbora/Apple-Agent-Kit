# Localization Export and Import

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.xcode.localization-export-import
artifact_type: knowledge
title: Localization Export and Import
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the .xcloc round trip — the build setting an export silently depends on, which of the catalog's four folders comes back on import, and what import overwrites in the project.
domain: Xcode
tags:
  - xcode
  - localization
  - xliff
references:
  - https://developer.apple.com/documentation/xcode/exporting-localizations
  - https://developer.apple.com/documentation/xcode/importing-localizations
  - https://developer.apple.com/documentation/xcode/editing-xliff-and-string-catalog-files
  - https://developer.apple.com/documentation/xcode/build-settings-reference
depends_on:
  - knowledge.xcode.project-localizations
related:
  - knowledge.xcode.build-configurations
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent moves a project's
localizable strings out to translators as an Xcode Localization Catalog
and back in again, so that nothing is silently omitted from the export
and nothing in the project is silently overwritten by the import.

## Scope

### Included

-   The build setting an export depends on, and what it silently omits when unset
-   The `.xcloc` catalog's four entries, and which of them the import reads
-   Editing XLIFF `<trans-unit>` entries, and how table names group them
-   What `Product > Import Localizations` overwrites in the project

### Excluded

-   Adding the languages that are exported — see `project-localizations`
-   String Catalog authoring, extraction semantics, plural variation, and the localizable-string APIs — owned by the `localization` domain
-   `xcodebuild -exportLocalizations` / `-importLocalizations` — CLI usage, Excluded from this domain
-   Screenshot generation for localizer context — Apple documents the "Include screenshots" option, but this domain does not own the tests that produce them

Sourcing note: Apple's export page lists the extracted file types as
"source code, storyboard, XIB, `.strings`, `.stringsdict`, and Siri
intent definition" and does not name `.xcstrings`. Rule 6 therefore
states the String Catalog behavior Apple documents directly.

## Rules

### Rule 1

Agents MUST verify the compiler-extraction build setting is enabled
before treating an export as complete. Per Apple's documentation: "To
include all localizable text in your export, enable the Use Compiler to
Extract Swift Strings build setting for your project. This setting only
impacts Swift strings. Objective-C string extraction works without any
additional build settings." An export with the setting off succeeds and
produces a catalog; the Swift strings are simply absent from it.

### Rule 2

Agents MUST direct translator-facing context into the catalog's `Notes`
folder and MUST NOT expect edits elsewhere to return. Per Apple's
documentation, `Localized Contents` holds "the localizable resources,
including an XLIFF file containing the localizable strings", `Notes`
holds "additional information for localizers, such as screenshots,
movies, or text files", and `Source Contents` holds "the assets to
produce the content that provides context for localizers". Only the
first is round-tripped: on import, "Xcode updates the strings files in
your project from the localized versions in the XLIFF file in the
catalog."

### Rule 3

Agents MUST NOT hand-edit a project's `.strings` or `.stringsdict` files
for a language that is round-tripped through a catalog. Per Apple's
documentation, on import "Xcode updates the strings and `.stringsdict`
files from the localized versions in the catalog. Xcode also updates any
localizable resources and assets in an asset catalog." The next import
replaces the hand edit without reporting a conflict.

### Rule 4

Agents MUST account for the table name when adding or changing a
localizable string in a project that is already being translated. Per
Apple's documentation: "If you specify a table name when you
internationalize your code… Xcode groups the strings into separate
`<file>` elements with `[table name].strings` as the filename. If you
don't specify a table name, Xcode uses the default `Localizable.strings`
as the filename." Moving a string to a new table moves it to a different
`<file>` in the next export, where translators see it as new work.

### Rule 5

Agents MUST read the import's warnings rather than confirming through
them. Per Apple's documentation: "Xcode ingests the files and warns you
if there are untranslated files," and the sheet that follows is where you
"review the warnings and errors" with "the imported catalog version of
the file… on the left and the current project file… on the right."
Untranslated is a reported outcome of a successful import, not a failure.

### Rule 6

Agents MAY edit a String Catalog in Xcode after an import without losing
the change on the next export. Per Apple's documentation: "After you
import localizations, you can edit the string catalog file in your
project and the next time you export localizations, Xcode includes your
changes in the XLIFF files."

## Compliant Example

-   ✓ Before `Product > Export Localizations`, Use Compiler to Extract Swift Strings is confirmed on. Reviewer notes go into `de.xcloc/Notes/`, and the translator adds targets in `Localized Contents`:

``` xml
<trans-unit id="Hello, world!" xml:space="preserve">
        <source>Hello, world!</source>
        <target>Hallo, Welt!</target>
        <note>A friendly greeting.</note>
</trans-unit>
```

The import sheet's two untranslated-file warnings are read and sent back before Import is clicked. (Rules 1, 2, 5)

## Non-Compliant Example

-   ✗ An export is taken with the build setting off, so the XLIFF carries only the Objective-C strings; the missing German copy is patched by editing `de.lproj/Localizable.strings` directly. The translator's real return arrives a week later, the import replaces the file with no conflict reported, and the patched strings are gone. (Rules 1, 3)

## Dependencies

-   knowledge.xcode.project-localizations — a language must be in the project's Localizations list before there is anything to export it as.

## References

-   [Apple Developer — Exporting localizations](https://developer.apple.com/documentation/xcode/exporting-localizations) · [Importing localizations](https://developer.apple.com/documentation/xcode/importing-localizations)
-   [Apple Developer — Editing XLIFF and string catalog files](https://developer.apple.com/documentation/xcode/editing-xliff-and-string-catalog-files)
-   [Apple Developer — Build settings reference: Use Compiler to Extract Swift Strings](https://developer.apple.com/documentation/xcode/build-settings-reference)
