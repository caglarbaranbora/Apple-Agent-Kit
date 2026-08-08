# Data Security

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.data-security
artifact_type: knowledge
title: Data Security
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines what guideline 1.6's one-sentence requirement for "appropriate security measures" resolves to in practice — credentials and personal data at rest belong in the Keychain rather than UserDefaults or a plist, data in transit stays under App Transport Security, secrets embedded in the bundle are extractable and therefore not secret, and an embedded third-party SDK is a third party under this guideline, so the app carries responsibility for what it does with user data.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - safety
  - security
  - privacy
references:
  - https://developer.apple.com/app-store/review/guidelines/#1.6
  - https://developer.apple.com/app-store/review/guidelines/#5.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.permission-usage-strings
  - knowledge.app-store-review-guidelines.privacy-manifest
last_updated: 2026-08-08
```

## Intent

This contract defines what an agent is actually being asked for by guideline
1.6. Its central claim is that 1.6 states an outcome in one sentence and
names no mechanism — "prevent its unauthorized use, disclosure, or access by
third parties" — so it is the guideline under which a storage or transport
mistake made anywhere in the app becomes a review finding. The mechanisms
belong to other domains; what belongs here is knowing which mistakes 1.6
reaches.

## Scope

### Included

-   Which storage and transport choices 1.6 makes a compliance question
-   Secrets shipped inside the app bundle
-   Responsibility for an embedded third-party SDK's handling of user data

### Excluded

-   Keychain APIs and accessibility levels — owned by `security`
-   App Transport Security configuration and TLS challenges — owned by
    `networking`
-   `PrivacyInfo.xcprivacy` declarations — see `privacy-manifest`
-   Consent and usage strings — see `permission-usage-strings`

## Rules

### Rule 1

Agents MUST store credentials, tokens, and personal data in the Keychain
rather than in `UserDefaults`, a plist, or an unprotected file. `UserDefaults`
is a plist inside the app container and is readable from an unencrypted
device backup, so a token kept there is disclosed by a mechanism the user
never sees. The APIs are owned by `security`; 1.6 is why the choice is not
a matter of taste.

### Rule 2

Agents MUST keep user data in transit under App Transport Security, and MUST
NOT add an `NSAllowsArbitraryLoads` exception to make a request work.
Transmitting personal data over a connection the app deliberately weakened
is the clearest form of "unauthorized… access by third parties". ATS
configuration is owned by `networking`.

### Rule 3

Agents MUST NOT embed API keys, shared secrets, or credentials in source,
`Info.plist`, or a bundled resource. Everything in the bundle ships to every
device and is recoverable from the IPA, so a key stored this way is
published, not stored. A value that must reach the device belongs behind an
authenticated request.

### Rule 4

Agents MUST treat an embedded third-party SDK as a third party under this
guideline. The app is what App Review examines, so an analytics or
advertising SDK that collects more than the app discloses is the app's
finding. This is the same fact `privacy-manifest` enforces mechanically
through required-reason declarations and SDK signatures.

### Rule 5

Agents MUST read 1.6 together with guideline 5.1, which it points to
directly — "(see Guideline 5.1 for more information)". 1.6 supplies the
security obligation and 5.1 supplies the collection, consent, and sharing
rules; a review finding about user data usually cites both, so satisfying
one is not a defence for the other.

## Compliant Example

-   ✓ A session token is written with `kSecClassGenericPassword` and `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`; nothing about the session reaches `UserDefaults`. (Rule 1)
-   ✓ Every endpoint is HTTPS with ATS at its defaults, and no exception dictionary exists in `Info.plist`. (Rule 2)
-   ✓ The analytics key is fetched from the app's own authenticated backend at launch rather than compiled in. (Rule 3)
-   ✓ Adding an SDK triggers a review of its privacy manifest and of what the nutrition label already declares. (Rule 4)

## Non-Compliant Example

-   ✗ The refresh token is stored in `UserDefaults` because "it is only a string". (Rule 1)
-   ✗ `NSAllowsArbitraryLoads` is set to `true` to unblock a partner's HTTP endpoint that receives user email addresses. (Rule 2)
-   ✗ A third-party API key sits in `Info.plist` under a custom key, on the reasoning that the plist is not source code. (Rule 3)
-   ✗ An advertising SDK collects the advertising identifier while the app declares no tracking. (Rule 4)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 1.6 Data Security](https://developer.apple.com/app-store/review/guidelines/#1.6)
-   [Apple App Review Guidelines — 5.1 Privacy](https://developer.apple.com/app-store/review/guidelines/#5.1)
