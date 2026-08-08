# Authentication

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: workflow.authentication
artifact_type: workflow
title: Authentication
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Composes the six Skills a sign-in feature spans, from the App Store Review rule that decides which login services the screen must offer, through user-facing wording, to credential storage.
skills:
  - skill.app-store-review-guidelines.submission
  - skill.style-guide.writing
  - skill.accessibility.foundations
  - skill.authenticationservices.foundations
  - skill.local-authentication.foundations
  - skill.security.foundations
related: []
last_updated: 2026-08-08
```

## Purpose

Build a complete sign-in feature. No single domain owns one: which login services the
screen must offer comes from the App Store Review Guidelines, the wording from the
Apple Style Guide, the mechanism from AuthenticationServices, re-authentication from
LocalAuthentication, credential storage from Keychain Services.

## Scope

### Included

- Whether guideline 4.8 requires a second login service; sign-in/sign-out text
- Accessibility of the sign-in form; credential persistence
- Sign in with Apple request, credential, and session lifecycle
- Biometric and device-passcode re-authentication

### Excluded

- Backend authentication and token issuance — outside this repository; attaching
  credentials to requests — `skill.networking.foundations`; entitlement — `skill.storekit.foundations`

## Trigger Conditions

Build, review, or fix a sign-in, sign-up, or account-session feature spanning more than
one Skill below; a task confined to one loads that Skill directly. Triggers: sign in,
sign up, login screen, account session, sign out, credentials.

## Skill Sequence

1. `skill.app-store-review-guidelines.submission` — decide the screen's shape first.
   Guideline 4.8 requires an equivalent login option alongside any third-party or
   social login used for the primary account; discovering that after submission means
   rebuilding the screen.
2. `skill.style-guide.writing` — fix terminology before it reaches views: Sign In /
   Sign Out, hyphenation, button label wording.
3. `skill.accessibility.foundations` — the form's labels, VoiceOver order, focus, and how validation results reach an assistive app.
4. `skill.authenticationservices.foundations` — the sign-in mechanism, and the
   credential-state and revocation handling that follows it.
5. `skill.local-authentication.foundations` — only when re-authenticating a returning
   user with Face ID, Touch ID, or the device passcode.
6. `skill.security.foundations` — only when an earlier step produced something that
   must survive app launch. Keychain storage, never `UserDefaults`.

## Exit Conditions

Complete when every applicable Skill has been loaded, its routed Contracts applied, and:

- Guideline 4.8 is satisfied by an equivalent login option, or an exemption is named.
- All user-facing text passes the terminology rules from step 2.
- Every form control has an accessible label and a defined focus order.
- Credential state is checked on launch, and no credential leaves the Keychain.

Stop and report if any Skill reports an unresolved dependency, naming the Skill and the
missing Contract. Never substitute general knowledge for an absent Contract.
