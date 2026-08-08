---
name: authenticationservices
description: Route Sign in with Apple implementation tasks to the correct Knowledge Contracts -- building the authorization request and reading the resulting credential, nonce generation and identity-token/authorization-code handling, credential-state checks and revocation reactions, and session persistence and sign-out. Use when calling ASAuthorizationAppleIDProvider, createRequest(), ASAuthorizationController, ASAuthorizationControllerDelegate, ASAuthorizationControllerPresentationContextProviding, ASAuthorizationAppleIDCredential, ASAuthorizationError, getCredentialState(forUserID:), ASAuthorizationAppleIDProvider.CredentialState, or credentialRevokedNotification. v1 is Sign in with Apple only -- no Password AutoFill/credential-provider extensions, no Passkeys/WebAuthn, no server-side JWT verification. Triggers on Sign in with Apple, AuthenticationServices, ASAuthorizationAppleIDProvider, ASAuthorizationAppleIDRequest, ASAuthorizationController, ASAuthorizationAppleIDCredential, identityToken, authorizationCode, nonce, getCredentialState, CredentialState, credentialRevokedNotification.
id: skill.authenticationservices.foundations
title: AuthenticationServices — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: AuthenticationServices
routes: [knowledge.authenticationservices.sign-in-with-apple-request-and-credential, knowledge.authenticationservices.nonce-and-identity-token-verification, knowledge.authenticationservices.credential-state-and-revocation, knowledge.authenticationservices.session-persistence-and-sign-out]
related: []
last_updated: 2026-08-08
---

# AuthenticationServices — Foundations Skill

## Purpose

Route Sign in with Apple implementation tasks to the minimum required
AuthenticationServices Knowledge Contracts. v1 scope is the
`ASAuthorizationAppleIDProvider`/`ASAuthorizationController` Sign in with
Apple flow only — no Password AutoFill/credential-provider extensions,
no Passkeys/WebAuthn APIs, no server-side identity-token verification.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/authenticationservices/.

-   Building an `ASAuthorizationAppleIDRequest` via `createRequest()`, setting `requestedScopes`, driving `ASAuthorizationController` through its delegate/presentation-context protocols, or reading `user`/`fullName`/`email`/`identityToken`/`authorizationCode`/`ASAuthorizationError` from the result -> sign-in-with-apple-request-and-credential.md
-   Generating/hashing a nonce, or forwarding `identityToken`/`authorizationCode` to a backend -> nonce-and-identity-token-verification.md
-   Calling `getCredentialState(forUserID:)`, branching on `.authorized`/`.revoked`/`.notFound`/`.transferred`, or observing `credentialRevokedNotification` -> credential-state-and-revocation.md
-   Deciding what to persist for a signed-in session, or sign-out behavior -> session-persistence-and-sign-out.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/authenticationservices/ — do not guess or fall
back to general knowledge.

-   Password AutoFill / credential-provider extensions
    (`ASCredentialProviderExtension`, `ASCredentialProviderViewController`) — Deferred
-   Passkeys / WebAuthn (`ASAuthorizationPlatformPublicKeyCredentialProvider`,
    `ASAuthorizationSecurityKeyPublicKeyCredentialProvider`) — Deferred
-   Server-side JWT signature/claims verification of the identity token — Excluded,
    a backend responsibility this kit does not cover
-   "Sign in with Apple" button UI/HIG design — owned by `human-interface-guidelines`
-   Sign-in terminology and wording — owned by `style-guide`
-   General Keychain storage/CRUD — owned by `security`

Composing these with this Skill is `workflow.authentication`'s job.
