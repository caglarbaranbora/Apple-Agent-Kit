# Manifest File Structure and Scope

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.privacy.manifest-file-structure-and-scope
type: knowledge
title: Manifest File Structure and Scope
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines PrivacyInfo.xcprivacy's top-level keys, per-bundle-type file location rules, the per-target/framework/xcframework manifest requirement, and Xcode's privacy report aggregation.
domain: Privacy
tags:
  - privacy
  - privacy-manifest
  - xcprivacy
  - bundle-structure
references:
  - https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
  - https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk
depends_on: []
related:
  - knowledge.privacy.required-reason-api-declarations
  - knowledge.privacy.collected-data-types-declaration
  - knowledge.privacy.tracking-domains-and-third-party-sdk-signatures
  - knowledge.app-store-review-guidelines.privacy-manifest
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent structures and places a
`PrivacyInfo.xcprivacy` file: its top-level keys, the correct bundle
location per product type (app, framework, Swift package, static
library, XCFramework), the rule that every target needs its own
manifest, and how Xcode aggregates manifests into a privacy report.
It does not cover the content rules for any individual key — those
are owned by the sibling contracts in this domain.

## Scope

### Included

-   `PrivacyInfo.xcprivacy` file name and property-list format
-   Top-level keys: `NSPrivacyTracking`, `NSPrivacyTrackingDomains`, `NSPrivacyCollectedDataTypes`, `NSPrivacyAccessedAPITypes`
-   Bundle location per product type (iOS/iPadOS/tvOS/visionOS/watchOS app vs. macOS/Mac Catalyst app; iOS-family framework vs. macOS framework; Swift package resource declaration; static library conversion)
-   The requirement that each executable/dynamic library bundle needing to report data needs its own manifest
-   Xcode's archive-based privacy report aggregation

### Excluded

-   Required-reason API category/reason-code content — see `required-reason-api-declarations`
-   `NSPrivacyCollectedDataTypes` entry schema/enum values — see `collected-data-types-declaration`
-   `NSPrivacyTracking`/`NSPrivacyTrackingDomains` values and third-party SDK signatures — see `tracking-domains-and-third-party-sdk-signatures`
-   App Store Connect rejection consequences of a missing/invalid manifest — see `knowledge.app-store-review-guidelines.privacy-manifest`

## Rules

### Rule 1

Agents MUST name the file `PrivacyInfo.xcprivacy` and structure it as a
property list whose top-level dictionary may contain exactly four keys:
`NSPrivacyTracking` (Boolean), `NSPrivacyTrackingDomains` (array of
strings), `NSPrivacyCollectedDataTypes` (array of dictionaries), and
`NSPrivacyAccessedAPITypes` (array of dictionaries) — per Apple's
documentation, these are the keys to add "at the top level of this
property list file."

### Rule 2

Agents MUST place the manifest at the bundle root for iOS, iPadOS,
tvOS, visionOS, or watchOS apps and frameworks (e.g.
`Sample.app/PrivacyInfo.xcprivacy`), and at `Contents/Resources/` for
macOS/Mac Catalyst apps or `Versions/A/Resources/` for macOS/Mac
Catalyst frameworks — per Apple's documentation on adding a privacy
manifest to an app or framework. For a Swift package, the manifest
goes in the target's default resource location (`Sources/<Target>/` or
its `Resources/` subfolder) and MUST be declared as an explicit
resource in `Package.swift` (e.g. `.process("PrivacyInfo.xcprivacy")`)
because Xcode does not treat it as a resource automatically.

### Rule 3

Agents MUST NOT attempt to bundle a manifest directly in a static
library (`.a`) — static libraries do not support resources. To ship a
manifest with a static library, agents MUST convert it to a static
framework target (Mach-O type "Static Library") and add the manifest
to that target's bundle resources instead.

### Rule 4

Agents MUST verify that every platform variant inside a distributed
XCFramework bundle contains its own correctly located manifest (e.g.
`ios-arm64/SampleFramework.framework/PrivacyInfo.xcprivacy` alongside a
separate copy under the macOS variant's `Versions/A/Resources/`) —
`xcodebuild -create-xcframework` carries each variant's manifest
through automatically, but a manually assembled XCFramework must
replicate this per-variant placement.

### Rule 5

When asked to produce an aggregate view of an app's declared data use,
agents MUST direct the user to Xcode's archive-based privacy report
(Product > Archive, then in the Organizer control-click the archive
and choose "Generate Privacy Report") rather than fabricate a summary —
this report aggregates the app's manifest with every linked
third-party SDK's manifest and is organized like the App Store Connect
Privacy Nutrition Label.

## Compliant Example

```
Sample.app/
    Info.plist
    Sample
    PrivacyInfo.xcprivacy
```

An iOS app manifest at the bundle root, matching Rule 2, with a
top-level dictionary restricted to the four documented keys (Rule 1).

## Non-Compliant Example

```
MacSample.app/
    Contents/
        MacOS/
            MacSample
        PrivacyInfo.xcprivacy
```

Places the manifest directly under `Contents/` instead of
`Contents/Resources/` for a macOS app — Xcode and App Store Connect
will not find it at this location. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — Privacy Manifest Files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
-   [Apple Developer — Adding a Privacy Manifest to Your App or Third-Party SDK](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk)
