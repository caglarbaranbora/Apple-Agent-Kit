# Credential State and Revocation

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.authenticationservices.credential-state-and-revocation
artifact_type: knowledge
title: Credential State and Revocation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines calling ASAuthorizationAppleIDProvider().getCredentialState(forUserID:) to check .authorized/.revoked/.notFound/.transferred, when to perform the check, reacting correctly to each state, and observing credentialRevokedNotification while the app is running.
domain: AuthenticationServices
tags:
  - authenticationservices
  - sign-in-with-apple
  - credential-state
  - revocation
references:
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/getcredentialstate(foruserid:completion:)
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/credentialstate
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/credentialrevokednotification
depends_on:
  - knowledge.authenticationservices.sign-in-with-apple-request-and-credential
related:
  - knowledge.authenticationservices.session-persistence-and-sign-out
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent checks the current authorization state of a previously signed-in Apple ID via `ASAuthorizationAppleIDProvider().getCredentialState(forUserID:)`, when that check must run, how it must react to each `ASAuthorizationAppleIDProvider.CredentialState` case, and how it observes `credentialRevokedNotification` to react if access is revoked while the app is already running.

## Scope

### Included

-   Calling `getCredentialState(forUserID:)` with the persisted `user` identifier
-   Checking all four `CredentialState` cases: `.authorized`, `.revoked`, `.notFound`, `.transferred`
-   When to perform the check: at minimum on app launch/foreground, per Apple's sample-code guidance
-   Reacting to `.revoked`/`.notFound` by signing the user out locally
-   Reacting to `.transferred` by treating the identifier as stale and needing migration
-   Observing `credentialRevokedNotification` for in-process reaction to revocation

### Excluded

-   Building the original request and obtaining the `user` identifier — see `sign-in-with-apple-request-and-credential`
-   Nonce generation and token forwarding — see `nonce-and-identity-token-verification`
-   Where and how the `user` identifier is persisted, and sign-out session/token cleanup mechanics — see `session-persistence-and-sign-out`
-   Server-side revocation webhooks (Apple's server-to-server notifications) — out of v1 scope, backend responsibility

## Rules

### Rule 1

Agents MUST call `ASAuthorizationAppleIDProvider().getCredentialState(forUserID:)`, passing the previously persisted `user` identifier — never a freshly generated or guessed value — and MUST branch on all four `CredentialState` cases: `.authorized`, `.revoked`, `.notFound`, `.transferred`.

### Rule 2

Agents MUST perform this check at minimum once per app launch and once per foreground, before presenting any authenticated UI, following the pattern Apple's own sample app uses: retrieving "the state of the user identifier saved in the keychain" immediately at launch to decide whether to show authenticated content or the sign-in flow.

### Rule 3

Agents MUST treat `.authorized` — "the user is authorized" — as the only state in which the locally cached session may be trusted without further action.

### Rule 4

Agents MUST sign the user out locally when the state is `.revoked` ("the given user's authorization has been revoked and they should be signed out") or `.notFound` ("the user hasn't established a relationship with Sign in with Apple"). Both mean the persisted credential no longer corresponds to a valid session; treating the user as signed in against either state serves stale authenticated state.

### Rule 5

Agents MUST treat `.transferred` — "the app has been transferred to a different team, and you need to migrate the user's identifier" — distinctly from `.revoked`/`.notFound`: the user's underlying Apple ID relationship is still valid, but the persisted `user` identifier is stale and must be migrated, not discarded as a sign-out.

### Rule 6

Agents MUST observe `ASAuthorizationAppleIDProvider.credentialRevokedNotification` (a static `NSNotification.Name`) to react to revocation while the app is already running, without waiting for the next launch/foreground to call `getCredentialState(forUserID:)` again. Per Apple's documentation, it is "a notification that indicates the user's credentials have been revoked and they should be signed out."

## Compliant Example

```swift
func checkCredentialState(forUserID userID: String) {
    ASAuthorizationAppleIDProvider().getCredentialState(forUserID: userID) { state, _ in
        DispatchQueue.main.async {
            switch state {
            case .authorized:
                break // Trust the cached session (Rule 3).
            case .revoked, .notFound:
                self.signOutLocally() // Discard stale session (Rule 4).
            case .transferred:
                self.migrateUserIdentifier() // Identifier is stale, not the relationship (Rule 5).
            @unknown default:
                self.signOutLocally()
            }
        }
    }
}

func observeRevocation() {
    NotificationCenter.default.addObserver(
        forName: ASAuthorizationAppleIDProvider.credentialRevokedNotification,
        object: nil, queue: .main
    ) { _ in
        self.signOutLocally() // React without waiting for next launch (Rule 6).
    }
}

// Called from app launch/foreground (Rule 2).
func applicationDidBecomeActive() {
    guard let userID = persistedUserID else { return }
    checkCredentialState(forUserID: userID)
}
```
Branches on all four `CredentialState` cases with distinct handling for `.transferred` versus `.revoked`/`.notFound` (Rules 1, 4, 5), runs the check on foreground (Rule 2), and observes `credentialRevokedNotification` for in-process reaction (Rule 6). (Rules 1, 2, 4, 5, 6)

## Non-Compliant Example

```swift
func checkCredentialState(forUserID userID: String) {
    ASAuthorizationAppleIDProvider().getCredentialState(forUserID: userID) { state, _ in
        if state != .authorized {
            self.signOutLocally() // .transferred treated the same as .revoked/.notFound.
        }
    }
}
// No launch/foreground call site, and no observer registered for revocation.
```
Collapses `.transferred` into the same handling as `.revoked`/`.notFound` instead of migrating the identifier (Rule 5), never registers an observer for `credentialRevokedNotification` (Rule 6), and has no call site tying the check to launch/foreground (Rule 2).

## Dependencies

-   `knowledge.authenticationservices.sign-in-with-apple-request-and-credential` — the `user` identifier checked here is the same value obtained from the original credential.

## References

-   [Apple Developer — ASAuthorizationAppleIDProvider.getCredentialState(forUserID:completion:)](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/getcredentialstate(foruserid:completion:))
-   [Apple Developer — ASAuthorizationAppleIDProvider.CredentialState](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/credentialstate)
-   [Apple Developer — ASAuthorizationAppleIDProvider.credentialRevokedNotification](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider/credentialrevokednotification)
