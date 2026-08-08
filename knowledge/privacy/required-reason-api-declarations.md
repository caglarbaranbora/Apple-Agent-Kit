# Required-Reason API Declarations

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.privacy.required-reason-api-declarations
artifact_type: knowledge
title: Required-Reason API Declarations
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the five documented required-reason API categories, their triggering APIs, and the exact NSPrivacyAccessedAPITypeReasons justification codes valid for each, per the live Apple Developer documentation.
domain: Privacy
tags:
  - privacy
  - privacy-manifest
  - required-reason-api
  - nsprivacyaccessedapitypereasons
references:
  - https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api
  - https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype
  - https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitypereasons
depends_on:
  - knowledge.privacy.manifest-file-structure-and-scope
related:
  - knowledge.privacy.collected-data-types-declaration
  - knowledge.app-store-review-guidelines.privacy-manifest
last_updated: 2026-08-08
```

## Intent

This contract defines which system APIs require a documented reason in `NSPrivacyAccessedAPITypes`, the five current category constants, and the exact `NSPrivacyAccessedAPITypeReasons` justification-code strings valid per category, verified against Apple's live documentation (this list has changed before and Apple states it will continue to review and update it).

## Scope

### Included

-   The five documented required-reason API categories and their triggering system APIs
-   The exact justification-code strings valid per category
-   The accuracy requirement (declared reasons must match actual use; no fingerprinting/tracking use)
-   The per-bundle declaration requirement (app code vs. third-party SDK code)
-   The May 1, 2024 App Store Connect enforcement date

### Excluded

-   `PrivacyInfo.xcprivacy` file placement/bundling — see `manifest-file-structure-and-scope`
-   `NSPrivacyCollectedDataTypes` schema — see `collected-data-types-declaration`
-   App Store Connect rejection-risk framing — see `knowledge.app-store-review-guidelines.privacy-manifest`

## Rules

### Rule 1

Agents MUST declare a category dictionary in `NSPrivacyAccessedAPITypes` for any use of one of the five current required-reason categories and their triggering APIs. Verify this table against the live docs before relying on it — Apple states it "continually reviews the list of required reason APIs":

| Category constant | Triggering APIs |
|---|---|
| `NSPrivacyAccessedAPICategoryFileTimestamp` | `creationDate`, `modificationDate`, `fileModificationDate`, `contentModificationDateKey`, `creationDateKey`, `stat`/`fstat`/`lstat`/`fstatat`, `getattrlist`/`fgetattrlist`/`getattrlistat`/`getattrlistbulk` |
| `NSPrivacyAccessedAPICategorySystemBootTime` | `systemUptime`, `mach_absolute_time()` |
| `NSPrivacyAccessedAPICategoryDiskSpace` | `volumeAvailable...Key`/`volumeTotalCapacityKey` family, `systemFreeSize`, `systemSize`, `statfs`/`statvfs`/`fstatfs`/`fstatvfs`, `getattrlist` family |
| `NSPrivacyAccessedAPICategoryActiveKeyboards` | `activeInputModes` |
| `NSPrivacyAccessedAPICategoryUserDefaults` | `UserDefaults` |

### Rule 2

Agents MUST choose `NSPrivacyAccessedAPITypeReasons` codes only from the category's documented set — custom or unlisted codes are rejected:

| Category | Approved codes (summary) |
|---|---|
| File Timestamp | `DDA9.1` display to user · `C617.1` app/app-group/CloudKit container metadata · `3B52.1` user-granted files (e.g. document picker) · `0A2A.1` SDK wrapper function (SDK-only) |
| System Boot Time | `35F9.1` elapsed-time/timers · `8FFB.1` absolute timestamps for in-app events · `3D61.1` optional bug report |
| Disk Space | `85F4.1` display to user · `E174.1` check space before writing/deleting files · `7D9E.1` optional bug report · `B728.1` health-research app |
| Active Keyboards | `3EC4.1` custom keyboard app · `54BD.1` customize UI per active keyboard |
| User Defaults | `CA92.1` app's own defaults · `1C8F.1` App Group–shared defaults · `C56D.1` SDK wrapper function (SDK-only) · `AC6B.1` MDM managed-configuration keys |

### Rule 3

Agents MUST NOT declare an SDK-wrapper reason code (`0A2A.1` or `C56D.1`) for app-level code — Apple's documentation states these "may only be declared by third-party SDKs" and may not be declared "if your third-party SDK was created primarily to wrap required reason API(s)."

### Rule 4

Agents MUST ensure the declared reason accurately reflects actual API use and MUST NOT use required-reason API or any data derived from it for fingerprinting or tracking, regardless of App Tracking Transparency status — per Apple's documentation, "fingerprinting is not allowed" and declared reasons "must be consistent with your app's functionality as presented to users."

### Rule 5

Agents MUST treat an undeclared required-reason API use as a hard App Store Connect blocker, not a warning: "Starting May 1, 2024, apps that don't describe their use of required reason API in their privacy manifest file aren't accepted by App Store Connect." Each executable or dynamic library that uses a required-reason API must be covered by a manifest reporting that use in its own bundle — an app's manifest does not cover a third-party SDK's usage or vice versa.

## Compliant Example

```xml
<key>NSPrivacyAccessedAPITypes</key>
<array>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array>
            <string>CA92.1</string>
        </array>
    </dict>
</array>
```

Declares `UserDefaults` access with `CA92.1` ("read and write information that is only accessible to the app itself"), an approved reason for that category. (Rules 1, 2)

## Non-Compliant Example

```xml
<key>NSPrivacyAccessedAPITypes</key>
<array>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array>
            <string>1XXX.1</string>
        </array>
    </dict>
</array>
```

Uses a fabricated, unlisted reason code instead of one of the four approved User Defaults codes — App Store Connect rejects this declaration. (Rule 2)

## Dependencies

- knowledge.privacy.manifest-file-structure-and-scope

## References

-   [Apple Developer — Describing Use of Required Reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)
-   [Apple Developer — NSPrivacyAccessedAPIType](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype)
-   [Apple Developer — NSPrivacyAccessedAPITypeReasons](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitypereasons)
