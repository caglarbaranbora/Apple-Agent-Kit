# Tracking Domains and Third-Party SDK Signatures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.privacy.tracking-domains-and-third-party-sdk-signatures
artifact_type: knowledge
title: Tracking Domains and Third-Party SDK Signatures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the NSPrivacyTracking/NSPrivacyTrackingDomains keys and Apple's third-party SDK privacy-manifest-and-signature requirement -- which SDKs must ship a manifest and cryptographic signature, and the consequence if one doesn't.
domain: Privacy
tags:
  - privacy
  - privacy-manifest
  - nsprivacytracking
  - third-party-sdk-signatures
references:
  - https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytracking
  - https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytrackingdomains
  - https://developer.apple.com/support/third-party-sdk-requirements/
depends_on:
  - knowledge.privacy.manifest-file-structure-and-scope
related:
  - knowledge.privacy.collected-data-types-declaration
  - knowledge.app-tracking-transparency.status-and-idfa-access
  - knowledge.app-store-review-guidelines.privacy-manifest
last_updated: 2026-08-06
```

## Intent

This contract defines the manifest-level `NSPrivacyTracking`/
`NSPrivacyTrackingDomains` keys and Apple's separate third-party SDK
privacy-manifest-and-signature requirement: which SDKs Apple requires
to ship a signed manifest for App Store submission, and what happens
when one doesn't.

## Scope

### Included

-   `NSPrivacyTracking` and `NSPrivacyTrackingDomains` keys and their runtime effect
-   The third-party SDK privacy-manifest-and-signature requirement and its trigger conditions
-   The consequence of a required SDK shipping without a valid manifest/signature

### Excluded

-   `PrivacyInfo.xcprivacy` file placement/bundling — see `manifest-file-structure-and-scope`
-   `NSPrivacyCollectedDataTypes` entry schema — see `collected-data-types-declaration`
-   Interpreting `ATTrackingManagerAuthorizationStatus` / IDFA access — see `knowledge.app-tracking-transparency.status-and-idfa-access`
-   App Store Connect nutrition-label tracking-use marking — owned by `app-store-review-guidelines`

## Rules

### Rule 1

Agents MUST set `NSPrivacyTracking` to `true` only when the app or third-party SDK uses data for tracking as defined under the App Tracking Transparency framework, and MUST then populate `NSPrivacyTrackingDomains` with every internet domain the app or SDK contacts for that purpose — per Apple's documentation, "when set to `true` you need to provide a list of internet domains in `NSPrivacyTrackingDomains`."

### Rule 2

Agents MUST account for the runtime effect of `NSPrivacyTrackingDomains`: if the user has not granted tracking permission through App Tracking Transparency, network requests to a listed domain fail and the app receives an error — code must not assume these requests silently succeed or silently no-op.

### Rule 3

Agents MUST include a valid `PrivacyInfo.xcprivacy` with signature for any third-party SDK dependency that appears on Apple's published "SDKs that require a privacy manifest and signature" list (e.g. representative entries: AFNetworking, Alamofire, FBSDKCoreKit, the Firebase\* family, GoogleSignIn, RealmSwift, SDWebImage — consult the live list for the current, much longer set) when submitting a new app, or an app update that adds one of those SDKs, to App Store Connect. The requirement covers "any version of a listed SDK, as well as any SDKs that repackage those on the list," and signatures apply specifically "where the listed SDKs are used as binary dependencies."

### Rule 4

Agents MUST treat a missing or invalid manifest on a required third-party SDK as a submission blocker, not a warning: "Starting February 12, 2025, apps you submit for review in App Store Connect must contain a valid privacy manifest file for a certain number of commonly used third-party SDKs," and App Store Connect separately "rejects app submissions that include invalid privacy manifest files." If the SDK vendor hasn't shipped a compliant update, the agent's remediation options are to obtain an updated SDK version from the vendor, or remove/replace the dependency — not to fabricate a manifest on the vendor's behalf.

### Rule 5

Agents MUST still evaluate whether a third-party SDK needs its own manifest even when it is not on the signature-required list: per Apple's documentation, a third-party SDK needs a privacy manifest if it uses a required-reason API, collects data about people using apps that include it, enables the app to collect data, or contacts tracking domains — any one of these conditions triggers the requirement independent of the named-SDK list.

## Compliant Example

```xml
<key>NSPrivacyTracking</key>
<true/>
<key>NSPrivacyTrackingDomains</key>
<array>
    <string>ads.example.com</string>
</array>
```

Declares tracking use and lists the exact domain contacted for it, matching Rule 1.

## Non-Compliant Example

```xml
<key>NSPrivacyTracking</key>
<true/>
<key>NSPrivacyTrackingDomains</key>
<array/>
```

Declares `NSPrivacyTracking` as `true` but leaves `NSPrivacyTrackingDomains` empty despite the app contacting `ads.example.com` for tracking — an inaccurate declaration relative to actual network behavior. (Rule 1)

## Dependencies

- knowledge.privacy.manifest-file-structure-and-scope

## References

-   [Apple Developer — NSPrivacyTracking](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytracking)
-   [Apple Developer — NSPrivacyTrackingDomains](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytrackingdomains)
-   [Apple Developer — Third-Party SDK Requirements](https://developer.apple.com/support/third-party-sdk-requirements/)
