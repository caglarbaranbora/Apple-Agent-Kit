# Session Persistence and Sign-Out

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.authenticationservices.session-persistence-and-sign-out
artifact_type: knowledge
title: Session Persistence and Sign-Out
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines persisting the Apple-provided user identifier (not email) in Keychain as the durable account key, alongside the app's own derived session/auth token rather than Apple credentials themselves, and that app sign-out does not revoke Sign-in-with-Apple access at Apple's end.
domain: AuthenticationServices
tags:
  - authenticationservices
  - sign-in-with-apple
  - session-persistence
  - sign-out
references:
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/user
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/email
depends_on:
  - knowledge.authenticationservices.sign-in-with-apple-request-and-credential
related:
  - knowledge.security.keychain-item-crud
  - knowledge.style-guide.sign-in-and-authentication-terminology
last_updated: 2026-08-08
```

## Intent

This contract defines what an AI coding agent must persist to keep a
Sign in with Apple session across launches — the Apple-provided `user`
identifier and the app's own derived session/auth token, not Apple's
credential material itself — and the boundary of what an app-triggered
sign-out can and cannot do to the underlying Sign in with Apple
relationship at Apple's end.

## Scope

### Included

-   The `user` identifier as the durable, per-app-per-user account key
-   Why `email` must not be used as the account key
-   What to persist: the `user` identifier plus the app's own derived session/auth token
-   That app sign-out does not revoke Sign-in-with-Apple access at Apple's end
-   Not building revocation UI that expects the app to trigger Apple-side revocation

### Excluded

-   Keychain CRUD mechanics (`SecItemAdd`/`SecItemCopyMatching`/`SecItemUpdate`/`SecItemDelete`, query construction, `OSStatus` handling) — see `knowledge.security.keychain-item-crud`
-   Sign-in/sign-out UX terminology and wording — see `knowledge.style-guide.sign-in-and-authentication-terminology`
-   Checking whether a persisted `user` identifier is still valid — see `credential-state-and-revocation`
-   Nonce generation and identity-token forwarding — see `nonce-and-identity-token-verification`

## Rules

### Rule 1

Agents MUST persist `ASAuthorizationAppleIDCredential.user` — "an
identifier for the authenticated user" — as the durable account key for
a signed-in session. It is stable and opaque per app-per-user, and is
the only value guaranteed to be present on every successful
authorization, first sign-in or repeat.

### Rule 2

Agents MUST NOT use `email` as the account key. Per
`sign-in-with-apple-request-and-credential` Rule 5, `email` is `nil` on
every authorization after the first for a given Apple ID + app pair, and
even when present it may be an Apple-generated private relay address
rather than the user's real address — neither property makes it a
stable identifier.

### Rule 3

Agents MUST store the persisted `user` identifier in Keychain, not
`UserDefaults` or another non-encrypted store, for the same rationale
`knowledge.security.keychain-item-crud` and its related contracts
already establish for credential-adjacent data. This contract does not
restate Keychain CRUD mechanics, accessibility levels, or access-group
sharing — see `knowledge.security.keychain-item-crud` for how to perform
the read/write itself.

### Rule 4

Agents MUST persist only the `user` identifier and the app's own
derived session/auth token (whatever the backend issues after verifying
the identity token) — never the `identityToken` or `authorizationCode`
themselves. Both are transient proofs consumed by the backend at
sign-in time (see `nonce-and-identity-token-verification` Rule 6 for
`authorizationCode`); persisting them client-side keeps sensitive,
short-lived material around for no purpose after exchange.

### Rule 5

Agents MUST NOT implement app-triggered revocation of Sign-in-with-Apple
access. Signing a user out of the app removes the locally persisted
`user` identifier and session token, but it does not revoke the user's
Sign-in-with-Apple relationship with Apple — that revocation is
user-controlled from the user's Apple ID settings (a rare, explicit
re-consent/revocation flow on Apple's side), not something the app can
initiate. Agents MUST NOT build a "revoke Sign in with Apple access"
button or similar UI that assumes the app has that capability.

## Compliant Example

```swift
func handleSuccessfulSignIn(credential: ASAuthorizationAppleIDCredential, sessionToken: String) throws {
    // user is the durable key -- persisted alongside the app's own token (Rules 1, 4).
    try keychain.save(account: "appleIDUser", data: Data(credential.user.utf8))
    try keychain.save(account: "sessionToken", data: Data(sessionToken.utf8))
    // identityToken/authorizationCode already consumed by the backend exchange; not stored here.
}

func signOut() throws {
    try keychain.delete(account: "appleIDUser")
    try keychain.delete(account: "sessionToken")
    // This ends the app's local session only -- it does not revoke Sign in with Apple
    // access at Apple's end (Rule 5). No "revoke access" action is offered here.
}
```
Persists the `user` identifier plus the app's own session token via Keychain, not `email` or the raw tokens (Rules 1, 2, 3, 4), and sign-out clears only the local session without claiming to revoke Apple-side access (Rule 5). (Rules 1, 2, 3, 4, 5)

## Non-Compliant Example

```swift
func handleSuccessfulSignIn(credential: ASAuthorizationAppleIDCredential, sessionToken: String) {
    UserDefaults.standard.set(credential.email, forKey: "accountKey") // Wrong store, wrong key.
    UserDefaults.standard.set(credential.identityToken, forKey: "identityToken") // Persisted long-term.
}

func revokeAppleSignIn() {
    // Button in Settings that claims to revoke Sign in with Apple access from the app.
    callAppleRevocationAPI() // No such app-triggered API exists.
}
```
Uses `UserDefaults` instead of Keychain (Rule 3), keys the session on `email` instead of `user` (Rule 2), persists `identityToken` long-term instead of a derived session token (Rule 4), and implements UI assuming the app can trigger Apple-side revocation (Rule 5).

## Dependencies

-   `knowledge.authenticationservices.sign-in-with-apple-request-and-credential` — the `user` identifier persisted here is the same value extracted from the credential there.

## References

-   [Apple Developer — ASAuthorizationAppleIDCredential.user](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/user)
-   [Apple Developer — ASAuthorizationAppleIDCredential.email](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential/email)
