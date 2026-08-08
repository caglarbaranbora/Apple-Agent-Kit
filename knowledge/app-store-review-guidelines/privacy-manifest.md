# Privacy Manifest

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.privacy-manifest
artifact_type: knowledge
title: Privacy Manifest
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the requirement to ship an accurate PrivacyInfo.xcprivacy privacy manifest declaring data collection and required-reason API usage, and the App Store Connect rejection risk of a missing or incomplete manifest.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - privacy
  - privacy-manifest
  - xcprivacy
references:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.2
  - https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
  - knowledge.app-store-review-guidelines.permission-usage-strings
last_updated: 2026-08-08
```

## Intent

This contract defines what an agent must declare in a
`PrivacyInfo.xcprivacy` file so App Store Connect accepts the binary:
collected data types, required-reason API justifications, and
third-party SDK coverage.

## Scope

### Included

-   `PrivacyInfo.xcprivacy` file requirement and applicable OS versions
-   Collected-data-type declarations
-   Required-reason API justification-code declarations
-   Third-party SDK privacy-manifest coverage
-   Manifest-update obligation on functionality change

### Excluded

-   `Info.plist` runtime permission-prompt strings — see `permission-usage-strings`
-   App Store Connect privacy questionnaire ("nutrition label") — see `privacy-nutrition-label`

## Rules

### Rule 1

Agents MUST include a `PrivacyInfo.xcprivacy` file in the app bundle
for any app or SDK targeting iOS 17+, iPadOS 17+, tvOS 17+, or
watchOS 10+.

### Rule 2

Agents MUST declare every collected user-data category (e.g. contacts,
location, health, financial info, browsing/search history, purchase
history, user IDs) in `NSPrivacyCollectedDataTypes`.

### Rule 3

Agents MUST declare an approved `NSPrivacyAccessedAPITypeReasons`
justification code for every use of a required-reason API — the five
official categories are File Timestamp, System Boot Time, Disk Space,
Active Keyboard, and User Defaults APIs (e.g.
`NSPrivacyAccessedAPICategoryUserDefaults`) — custom or unlisted
justification codes are rejected.

### Rule 4

Agents MUST account for third-party SDK dependencies' data use in the
app's own manifest when a bundled SDK does not ship its own privacy
manifest.

### Rule 5

Agents MUST update the manifest whenever app functionality that changes
data collection or required-reason API usage changes — a stale manifest
is treated as inaccurate, not merely outdated.

## Compliant Example

-   ✓ App bundles `PrivacyInfo.xcprivacy` declaring `NSUserDefaults` access with an approved reason code, and lists Location as a collected data type matching actual behavior. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ App uses `UserDefaults` but ships no `PrivacyInfo.xcprivacy` file — App Store Connect rejects the binary at upload. (Rules 1, 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 5.1.2 Data Use and Sharing](https://developer.apple.com/app-store/review/guidelines/#5.1.2)
-   [Apple Developer — Privacy Manifest Files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
