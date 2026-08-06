# Collected Data Types Declaration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.privacy.collected-data-types-declaration
type: knowledge
title: Collected Data Types Declaration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the NSPrivacyCollectedDataTypes array entry schema -- NSPrivacyCollectedDataType, NSPrivacyCollectedDataTypeLinked, NSPrivacyCollectedDataTypeTracking, and NSPrivacyCollectedDataTypePurposes valid values -- as manifest-level declaration mechanics.
domain: Privacy
tags:
  - privacy
  - privacy-manifest
  - nsprivacycollecteddatatypes
references:
  - https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests
  - https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatype
  - https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypepurposes
depends_on:
  - knowledge.privacy.manifest-file-structure-and-scope
related:
  - knowledge.privacy.required-reason-api-declarations
  - knowledge.app-store-review-guidelines.privacy-manifest
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
updated: 2026-08-06
```

## Intent

This contract defines the exact dictionary schema an agent writes into each entry of `NSPrivacyCollectedDataTypes`: the valid `NSPrivacyCollectedDataType` enum values, the `Linked`/`Tracking` Boolean keys, and the valid `NSPrivacyCollectedDataTypePurposes` enum values — the manifest-level declaration mechanics, distinct from the App Store Connect nutrition-label questionnaire that asks the same substantive questions in a separate web form.

## Scope

### Included

-   `NSPrivacyCollectedDataTypes` array-of-dictionaries schema
-   `NSPrivacyCollectedDataType` valid enum values
-   `NSPrivacyCollectedDataTypeLinked` and `NSPrivacyCollectedDataTypeTracking` Booleans
-   `NSPrivacyCollectedDataTypePurposes` valid enum values
-   The requirement to use only documented enum values so Xcode's privacy report generates correctly

### Excluded

-   `PrivacyInfo.xcprivacy` file placement/bundling — see `manifest-file-structure-and-scope`
-   Required-reason API declarations — see `required-reason-api-declarations`
-   App Store Connect "App Privacy" nutrition-label questionnaire (the web-form disclosure) — see `knowledge.app-store-review-guidelines.privacy-nutrition-label`
-   App Store Connect rejection-risk framing for an inaccurate manifest — see `knowledge.app-store-review-guidelines.privacy-manifest`

## Rules

### Rule 1

Agents MUST add one dictionary to `NSPrivacyCollectedDataTypes` per category of data the app or third-party SDK collects, with exactly four keys: `NSPrivacyCollectedDataType` (string), `NSPrivacyCollectedDataTypeLinked` (Boolean), `NSPrivacyCollectedDataTypeTracking` (Boolean), and `NSPrivacyCollectedDataTypePurposes` (array of strings) — per Apple's documentation, "add the following keys to the dictionary" for each data type collected.

### Rule 2

Agents MUST set `NSPrivacyCollectedDataType` to one of Apple's documented values only — representative examples: `NSPrivacyCollectedDataTypeName`, `NSPrivacyCollectedDataTypeEmailAddress`, `NSPrivacyCollectedDataTypePreciseLocation`, `NSPrivacyCollectedDataTypeCoarseLocation`, `NSPrivacyCollectedDataTypeHealth`, `NSPrivacyCollectedDataTypeContacts`, `NSPrivacyCollectedDataTypeBrowsingHistory`, `NSPrivacyCollectedDataTypeSearchHistory`, `NSPrivacyCollectedDataTypePurchaseHistory`, `NSPrivacyCollectedDataTypeUserID`, `NSPrivacyCollectedDataTypeDeviceID`, `NSPrivacyCollectedDataTypeCrashData`. Consult the live docs for the complete ~34-value list (it also covers financial, sensitive, audio/photo/video, gameplay, diagnostic, and visionOS environment-scanning/hands/head categories) before declaring a type not listed here.

### Rule 3

Agents MUST set `NSPrivacyCollectedDataTypePurposes` to one or more of exactly six documented values: `NSPrivacyCollectedDataTypePurposeThirdPartyAdvertising`, `NSPrivacyCollectedDataTypePurposeDeveloperAdvertising`, `NSPrivacyCollectedDataTypePurposeAnalytics`, `NSPrivacyCollectedDataTypePurposeProductPersonalization`, `NSPrivacyCollectedDataTypePurposeAppFunctionality`, and `NSPrivacyCollectedDataTypePurposeOther`.

### Rule 4

Agents MUST NOT invent custom values for `NSPrivacyCollectedDataType` or `NSPrivacyCollectedDataTypePurposes` — per Apple's documentation, "Xcode won't generate a privacy report correctly if you define your own collected data types... or provide your own reasons," so an undocumented value silently breaks the aggregated privacy report rather than producing a validation error at write time.

### Rule 5

Agents MUST NOT declare a third-party SDK's own data collection inside the app's manifest — per Apple's documentation, "your app's privacy manifest file doesn't need to cover data collected by third-party SDKs that your app links to," since each SDK ships its own manifest with its own `NSPrivacyCollectedDataTypes` entries.

## Compliant Example

```xml
<key>NSPrivacyCollectedDataTypes</key>
<array>
    <dict>
        <key>NSPrivacyCollectedDataType</key>
        <string>NSPrivacyCollectedDataTypePreciseLocation</string>
        <key>NSPrivacyCollectedDataTypeLinked</key>
        <true/>
        <key>NSPrivacyCollectedDataTypeTracking</key>
        <false/>
        <key>NSPrivacyCollectedDataTypePurposes</key>
        <array>
            <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
        </array>
    </dict>
</array>
```

Uses documented enum values for both the data type and its purpose, with `Linked`/`Tracking` set to match actual behavior. (Rules 1, 2, 3)

## Non-Compliant Example

```xml
<key>NSPrivacyCollectedDataTypes</key>
<array>
    <dict>
        <key>NSPrivacyCollectedDataType</key>
        <string>Location</string>
        <key>NSPrivacyCollectedDataTypePurposes</key>
        <array>
            <string>Maps</string>
        </array>
    </dict>
</array>
```

Uses a made-up data-type string (`Location` instead of `NSPrivacyCollectedDataTypePreciseLocation`/`...CoarseLocation`) and a made-up purpose (`Maps` instead of a documented purpose constant), and omits the required `Linked`/`Tracking` keys. (Rules 1, 2, 3, 4)

## Dependencies

- knowledge.privacy.manifest-file-structure-and-scope

## References

-   [Apple Developer — Describing Data Use in Privacy Manifests](https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests)
-   [Apple Developer — NSPrivacyCollectedDataType](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatype)
-   [Apple Developer — NSPrivacyCollectedDataTypePurposes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypepurposes)
