# Privacy Manifest

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: reference.apple.privacy
artifact_type: reference
title: Privacy Manifest
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's `PrivacyInfo.xcprivacy` privacy manifest file documentation, scoped to this domain's v1.
domain: Privacy
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitypereasons
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatype
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypepurposes
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytracking
https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytrackingdomains
https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests
https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api
https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
https://developer.apple.com/support/third-party-sdk-requirements/

## Purpose

Reference index for Apple's `PrivacyInfo.xcprivacy` privacy manifest
file documentation, scoped to this domain's v1: manifest file
structure/bundling/scope, required-reason API declarations, collected
data type declarations, and tracking domains plus the third-party SDK
privacy-manifest-and-signature requirement. The App Store Connect "App
Privacy" nutrition-label questionnaire (owned by
`app-store-review-guidelines`), permission-request UI/consent-flow
design and purpose-string wording (owned by
`human-interface-guidelines`), `Info.plist` runtime usage-string keys
(owned by `app-store-review-guidelines`'s `permission-usage-strings.md`),
and Keychain/credential storage (owned by the `security` domain, built
2026-08) are out of scope.

## Primary Topics

- Manifest file structure, bundling location, and scope
- Required-reason API categories and justification-code declarations
- Collected data type declarations
- Tracking domains and third-party SDK signature requirement

## Used By

- knowledge/privacy/manifest-file-structure-and-scope.md ([[knowledge/privacy/manifest-file-structure-and-scope]])
- knowledge/privacy/required-reason-api-declarations.md ([[knowledge/privacy/required-reason-api-declarations]])
- knowledge/privacy/collected-data-types-declaration.md ([[knowledge/privacy/collected-data-types-declaration]])
- knowledge/privacy/tracking-domains-and-third-party-sdk-signatures.md ([[knowledge/privacy/tracking-domains-and-third-party-sdk-signatures]])
- knowledge/app-store-review-guidelines/privacy-manifest.md ([[knowledge/app-store-review-guidelines/privacy-manifest]])
