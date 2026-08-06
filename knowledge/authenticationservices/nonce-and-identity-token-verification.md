# Nonce and Identity Token Verification

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authenticationservices.nonce-and-identity-token-verification
type: knowledge
title: Nonce and Identity Token Verification
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines generating a cryptographically random nonce per request, SHA256-hashing it into the request's nonce property, and sending the raw nonce plus identityToken and authorizationCode to a backend for verification, without performing server-side JWT verification client-side.
domain: AuthenticationServices
tags:
  - authenticationservices
  - sign-in-with-apple
  - nonce
  - identity-token
references:
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationopenidrequest/nonce
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/identitytoken
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/authorizationcode
depends_on:
  - knowledge.authenticationservices.sign-in-with-apple-request-and-credential
related:
  - knowledge.authenticationservices.credential-state-and-revocation
updated: 2026-08-06
```

## Intent

This contract defines the client-side half of replay-protected Sign in with Apple verification: generating a fresh, cryptographically random nonce per authorization request, hashing it with SHA256 into the request's `nonce` property before sending, and forwarding the raw (unhashed) nonce alongside the returned `identityToken` and `authorizationCode` to the app's own backend. It does not define what the backend does with those values.

## Scope

### Included

-   Generating a fresh, cryptographically random nonce per authorization request
-   SHA256-hashing the raw nonce into `ASAuthorizationOpenIDRequest.nonce` before sending
-   Sending the raw (unhashed) nonce, `identityToken`, and `authorizationCode` to the app's own backend
-   Never skipping the nonce
-   The short-lived, single-use nature of `authorizationCode`, and exchanging it promptly rather than caching it client-side

### Excluded

-   Verifying the identity token's JWT signature and claims (`iss`, `aud`, `exp`, matching the hashed `nonce` claim against the server-held raw nonce) — a server-side responsibility, out of this contract's scope, same exclusion pattern as `knowledge.storekit.transaction-verification-and-entitlements` excludes server-side receipt validation
-   Building the request and extracting the credential — see `sign-in-with-apple-request-and-credential`
-   `getCredentialState(forUserID:)` and revocation — see `credential-state-and-revocation`
-   Persisting the `user` identifier and sign-out — see `session-persistence-and-sign-out`

## Rules

### Rule 1

Agents MUST generate a new, cryptographically random nonce for every individual authorization request, and MUST NOT skip generating/setting one on any request, even for a quick prototype — a reused, predictable, or missing nonce removes the app's only defense against a replayed identity token, and cannot be safely retrofitted per-request later.

### Rule 2

Agents MUST set `ASAuthorizationAppleIDRequest.nonce` (inherited from `ASAuthorizationOpenIDRequest`) to the SHA256 hash of the raw nonce, not the raw nonce itself. Per Apple's documentation, `nonce` is "a string value to pass to the identity provider" — the returned `identityToken` carries this hashed value in its claims, so the backend must hash the raw nonce the same way (SHA256) to find a match.

### Rule 3

Agents MUST retain the raw, unhashed nonce used to derive the value in Rule 2, and send that raw nonce — never the hashed value — to the app's backend together with the `identityToken` and `authorizationCode`. The backend needs the raw nonce to reproduce the hash and compare it against the token's `nonce` claim; sending the already-hashed value makes that comparison impossible.

### Rule 4

Agents MUST NOT attempt to verify the `identityToken`'s JWT signature or claims on-device. Client-side code's only responsibilities toward the token are to obtain it from the credential and transmit it, intact, to the backend. Actual verification (checking the signature against Apple's public keys, and validating `iss`/`aud`/`exp`/`nonce` claims) is entirely a server-side concern and out of scope for this contract.

### Rule 5

Agents MUST treat `authorizationCode` as short-lived and single-use. Per Apple's documentation, the app "uses this short-lived token as proof that it has authorization to interact with the server" — it MUST be transmitted to the backend and exchanged promptly, and MUST NOT be cached, persisted, or retried against later, since a stale code will be rejected regardless.

## Compliant Example

```swift
import CryptoKit

func startSignIn(presenting window: ASPresentationAnchor) {
    let rawNonce = randomNonceString() // Fresh per request (Rule 1).
    currentRawNonce = rawNonce         // Retained to send raw, later (Rule 3).
    let request = ASAuthorizationAppleIDProvider().createRequest()
    request.requestedScopes = [.fullName, .email]
    request.nonce = sha256(rawNonce)   // Hashed value goes to Apple (Rule 2).
    let controller = ASAuthorizationController(authorizationRequests: [request])
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests()
}

func authorizationController(controller: ASAuthorizationController,
                              didCompleteWithAuthorization authorization: ASAuthorization) {
    guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential,
          let identityToken = credential.identityToken,
          let authorizationCode = credential.authorizationCode,
          let rawNonce = currentRawNonce else { return }
    // Backend verifies the JWT and exchanges the code -- not this contract's concern (Rule 4).
    Task { try await backend.verifySignIn(rawNonce: rawNonce, identityToken: identityToken, authorizationCode: authorizationCode) }
}
```
Generates a fresh nonce per request and hashes it before sending to Apple (Rules 1, 2), retains and forwards the raw nonce to the backend rather than the hash (Rule 3), and leaves JWT verification to the backend call (Rule 4). (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
func startSignIn(presenting window: ASPresentationAnchor) {
    let request = ASAuthorizationAppleIDProvider().createRequest()
    request.requestedScopes = [.fullName, .email] // No nonce set at all.
    let controller = ASAuthorizationController(authorizationRequests: [request])
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests()
}

func authorizationController(controller: ASAuthorizationController,
                              didCompleteWithAuthorization authorization: ASAuthorization) {
    guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential,
          let identityToken = credential.identityToken,
          let payload = decodeJWTPayloadLocally(identityToken) else { return } // Verifying locally.
    grantAccess(userID: payload.sub)
    cachedAuthorizationCode = credential.authorizationCode // Cached for "later".
}
```
Never sets `request.nonce` (Rule 1), decodes and trusts the JWT payload on-device instead of forwarding it to a backend (Rule 4), and caches the short-lived `authorizationCode` for later use instead of exchanging it promptly (Rule 5).

## Dependencies

-   `knowledge.authenticationservices.sign-in-with-apple-request-and-credential` — the request whose `nonce` is set here, and the credential whose `identityToken`/`authorizationCode` are forwarded here.

## References

-   [Apple Developer — ASAuthorizationOpenIDRequest.nonce](https://developer.apple.com/documentation/authenticationservices/asauthorizationopenidrequest/nonce)
-   [Apple Developer — ASAuthorizationAppleIDCredential.identityToken](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/identitytoken)
-   [Apple Developer — ASAuthorizationAppleIDCredential.authorizationCode](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/authorizationcode)
