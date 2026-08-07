# Authentication

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: workflow.authentication
artifact_type: workflow
title: Authentication
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Composes the five Skills a sign-in feature spans, from user-facing wording through credential storage.
skills:
  - skill.style-guide.writing
  - skill.accessibility.foundations
  - skill.authenticationservices.foundations
  - skill.local-authentication.foundations
  - skill.security.foundations
related: []
last_updated: 2026-08-07
```

## Purpose

Build a complete sign-in feature. No single domain owns one: the wording comes from
the Apple Style Guide, the mechanism from AuthenticationServices, the re-authentication
from LocalAuthentication, and the credential storage from Keychain Services. It
replaces the retired `authentication` Skill, whose value was routing, not knowledge.

## Scope

### Included

- Sign-in and sign-out user-facing text
- Accessibility of the sign-in form
- Sign in with Apple request, credential, and session lifecycle
- Biometric and device-passcode re-authentication
- Credential persistence

### Excluded

- Backend authentication and token issuance — outside this repository
- Attaching credentials to network requests — `skill.networking.foundations`
- In-app purchase and account entitlement — `skill.storekit.foundations`

## Trigger Conditions

The task asks to build, review, or fix a sign-in, sign-up, or account-session feature
spanning more than one Skill below. A task confined to one loads that Skill directly.

Triggers: sign in, sign up, login screen, account session, sign out, credentials.

## Skill Sequence

1. `skill.style-guide.writing` — fix the terminology before it is written into views.
   Sign In / Sign Out, hyphenation, button label wording.
2. `skill.accessibility.foundations` — the form's labels, VoiceOver order, focus, and how its validation result reaches an assistive app.
3. `skill.authenticationservices.foundations` — the sign-in mechanism itself, and the
   credential-state and revocation handling that follows it.
4. `skill.local-authentication.foundations` — only when the feature re-authenticates a
   returning user with Face ID, Touch ID, or the device passcode.
5. `skill.security.foundations` — only when the previous steps produced something that
   must survive app launch. Keychain storage, never `UserDefaults`.

Steps 1-3 always apply. Steps 4 and 5 are conditional, as marked.

## Exit Conditions

Complete when every applicable Skill has been loaded, its routed Contracts applied, and:

- All user-facing text passes the terminology rules from step 1.
- Every form control has an accessible label and a defined focus order.
- The credential state is checked on launch, not only at sign-in.
- No credential is stored outside the Keychain.

Stop and report if any Skill reports an unresolved dependency, naming the Skill and the
missing Contract. Do not substitute general knowledge for a Contract that is absent.
