# AuthenticationServices

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: reference.apple.authenticationservices
artifact_type: reference
title: AuthenticationServices
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's AuthenticationServices documentation, scoped to this domain's v1.
domain: AuthenticationServices
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/authenticationservices
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/createrequest()
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidrequest
https://developer.apple.com/documentation/authenticationservices/asauthorizationopenidrequest
https://developer.apple.com/documentation/authenticationservices/asauthorizationopenidrequest/requestedscopes
https://developer.apple.com/documentation/authenticationservices/asauthorization/scope
https://developer.apple.com/documentation/authenticationservices/asauthorizationopenidrequest/nonce
https://developer.apple.com/documentation/authenticationservices/asauthorizationcontroller
https://developer.apple.com/documentation/authenticationservices/asauthorizationcontroller/performrequests()
https://developer.apple.com/documentation/authenticationservices/asauthorizationcontrollerdelegate
https://developer.apple.com/documentation/authenticationservices/asauthorizationcontrollerpresentationcontextproviding
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/user
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/fullname
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/email
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/identitytoken
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/authorizationcode
https://developer.apple.com/documentation/authenticationservices/asauthorizationerror-swift.struct
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/credentialstate
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/getcredentialstate(foruserid:completion:)
https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/credentialrevokednotification
https://developer.apple.com/documentation/authenticationservices/implementing-user-authentication-with-sign-in-with-apple

## Purpose

Reference index for Apple's AuthenticationServices documentation, scoped
to this domain's v1: building an `ASAuthorizationAppleIDRequest` via
`ASAuthorizationAppleIDProvider().createRequest()`, setting
`requestedScopes` (`.fullName`, `.email`); driving an
`ASAuthorizationController` through `ASAuthorizationControllerDelegate`
and `ASAuthorizationControllerPresentationContextProviding`; extracting
the `user` identifier, `fullName`, `email`, `identityToken`, and
`authorizationCode` from the resulting `ASAuthorizationAppleIDCredential`;
handling `ASAuthorizationError` codes; generating and hashing a nonce
before sending the raw value and tokens to a backend for verification;
checking `getCredentialState(forUserID:)` and observing
`credentialRevokedNotification`; and persisting the `user` identifier as
the durable account key with correct sign-out behavior.

Out of scope for v1: Password AutoFill / credential-provider extensions
(`ASCredentialProviderExtension`, `ASCredentialProviderViewController`);
Passkeys / WebAuthn APIs
(`ASAuthorizationPlatformPublicKeyCredentialProvider`,
`ASAuthorizationSecurityKeyPublicKeyCredentialProvider`); server-side JWT
signature/claims verification of the identity token (a backend
responsibility); and "Sign in with Apple" button UI/HIG design
conventions, owned by the `human-interface-guidelines` domain, and
sign-in terminology, owned by the `style-guide` domain. Composing those
with this domain is `workflow.authentication`'s job.
General Keychain CRUD mechanics are owned by the `security`
domain; this domain owns the Sign in with Apple API implementation angle
only.

## Primary Topics

- Sign in with Apple request and credential
- Nonce and identity token verification
- Credential state and revocation
- Session persistence and sign-out

## Used By

- knowledge/authenticationservices/sign-in-with-apple-request-and-credential.md ([[knowledge/authenticationservices/sign-in-with-apple-request-and-credential]])
- knowledge/authenticationservices/nonce-and-identity-token-verification.md ([[knowledge/authenticationservices/nonce-and-identity-token-verification]])
- knowledge/authenticationservices/credential-state-and-revocation.md ([[knowledge/authenticationservices/credential-state-and-revocation]])
- knowledge/authenticationservices/session-persistence-and-sign-out.md ([[knowledge/authenticationservices/session-persistence-and-sign-out]])
