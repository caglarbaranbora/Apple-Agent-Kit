# Sign In With Apple Request and Credential

Status: Draft Version: 0.2.0

## Metadata

``` yaml
id: knowledge.authenticationservices.sign-in-with-apple-request-and-credential
artifact_type: knowledge
title: Sign In With Apple Request and Credential
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Defines building an ASAuthorizationAppleIDRequest via ASAuthorizationAppleIDProvider().createRequest(), setting requestedScopes, driving an ASAuthorizationController through its delegate and presentation-context protocols, extracting the resulting ASAuthorizationAppleIDCredential, and handling every ASAuthorizationError case including .canceled.
domain: AuthenticationServices
tags:
  - authenticationservices
  - sign-in-with-apple
  - authorization-controller
  - apple-id-credential
references:
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidrequest
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationcontroller
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationcontrollerdelegate
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationcontrollerpresentationcontextproviding
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential
  - https://developer.apple.com/documentation/authenticationservices/asauthorizationerror-swift.struct
depends_on: []
related:
  - knowledge.authenticationservices.nonce-and-identity-token-verification
  - knowledge.authenticationservices.credential-state-and-revocation
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent builds an `ASAuthorizationAppleIDRequest` via `createRequest()`, drives an `ASAuthorizationController` through its delegate protocols, and extracts the resulting `ASAuthorizationAppleIDCredential` — the entry point into Sign in with Apple, before any nonce, credential-state, or session-persistence concern applies.

## Scope

### Included

-   Creating a request via `createRequest()` and setting `requestedScopes` (`.fullName`/`.email`)
-   Creating an `ASAuthorizationController`, assigning delegates, and calling `performRequests()`
-   Implementing `ASAuthorizationControllerDelegate` and `ASAuthorizationControllerPresentationContextProviding`
-   Extracting `user`/`fullName`/`email`/`identityToken`/`authorizationCode` from the credential
-   The once-only population rule for `fullName`/`email`
-   Handling `ASAuthorizationError` codes without surfacing `.canceled` as an error

### Excluded

-   Nonce generation/hashing and sending tokens to a backend — see `nonce-and-identity-token-verification`
-   Server-side identity-token verification — out of v1 scope, backend responsibility
-   `getCredentialState(forUserID:)` and revocation — see `credential-state-and-revocation`
-   Persisting the `user` identifier and sign-out — see `session-persistence-and-sign-out`
-   Password AutoFill/credential-provider extensions and Passkeys/WebAuthn — out of v1 scope
-   Button UI/HIG — owned by `human-interface-guidelines`; sign-in terminology
    — owned by `style-guide`

## Rules

### Rule 1

Agents MUST create the request via `ASAuthorizationAppleIDProvider().createRequest()` — never construct `ASAuthorizationAppleIDRequest` directly — and set `requestedScopes`; v1 supports `.email` and `.fullName`.

### Rule 2

Agents MUST create an `ASAuthorizationController`, assign both `delegate` and `presentationContextProvider` (implementing `presentationAnchor(for:)` and both `ASAuthorizationControllerDelegate` completion methods), then call `performRequests()`. Omitting `presentationContextProvider` leaves no window to present the sheet in; omitting the error-handling method silently drops failures.

### Rule 3

Agents MUST cast `authorization.credential` to `ASAuthorizationAppleIDCredential` inside `didCompleteWithAuthorization` and read identifying properties only from that cast value — `credential` is the `ASAuthorizationCredential` protocol type and differs by authorization method.

### Rule 4

Agents MUST treat `fullName`/`email` as populated only on the first successful authorization per Apple ID + app. Every later sign-in returns `nil` for both; persist them on first arrival and never treat a later `nil` as failure.

### Rule 5

Agents MUST switch on `ASAuthorizationError.Code` (`.canceled`, `.failed`, `.invalidResponse`, `.notHandled`, `.unknown`), and MUST NOT surface `.canceled` as a user-facing error — it fires when the user dismisses the sheet, a silent no-op like `.userCancelled` in StoreKit. Every other code MAY be surfaced as a genuine failure.

## Compliant Example

```swift
final class SignInCoordinator: NSObject, ASAuthorizationControllerDelegate,
    ASAuthorizationControllerPresentationContextProviding {
    var window: ASPresentationAnchor!
    func startSignIn(presenting window: ASPresentationAnchor) {
        self.window = window
        let request = ASAuthorizationAppleIDProvider().createRequest()
        request.requestedScopes = [.fullName, .email] // Rule 1
        let controller = ASAuthorizationController(authorizationRequests: [request])
        controller.delegate = self
        controller.presentationContextProvider = self // Rule 2
        controller.performRequests()
    }
    func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor { window } // Rule 2
    func authorizationController(controller: ASAuthorizationController,
                                  didCompleteWithAuthorization authorization: ASAuthorization) {
        guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential else { return } // Rule 3
        handle(userID: credential.user, fullName: credential.fullName, email: credential.email)
    }
    func authorizationController(controller: ASAuthorizationController, didCompleteWithError error: Error) {
        guard let authError = error as? ASAuthorizationError else { return }
        switch authError.code {
        case .canceled: break // Silent no-op, not an error (Rule 5).
        case .failed, .invalidResponse, .notHandled, .unknown: presentSignInFailure() // Rule 5
        @unknown default: presentSignInFailure()
        }
    }
}
```
Creates via `createRequest()` (Rule 1), wires both delegates before `performRequests()` (Rule 2), safe-casts the credential (Rule 3), and switches on `ASAuthorizationError.Code` without surfacing `.canceled` (Rule 5). (Rules 1, 2, 3, 5)

## Non-Compliant Example

```swift
func authorizationController(controller: ASAuthorizationController,
                              didCompleteWithAuthorization authorization: ASAuthorization) {
    let credential = authorization.credential as! ASAuthorizationAppleIDCredential
    guard let fullName = credential.fullName, let email = credential.email else {
        return showError("Sign in failed: missing profile data") // Wrong -- nil is expected on repeat sign-ins.
    }
    store(userID: credential.user, fullName: fullName, email: email)
}
func authorizationController(controller: ASAuthorizationController, didCompleteWithError error: Error) {
    showError("Sign in with Apple failed.") // Also shown for .canceled.
}
```
Force-casts instead of a safe cast (Rule 3), treats a `nil` `fullName`/`email` on a repeat sign-in as failure (Rule 4), and surfaces `.canceled` to the user (Rule 5).

## Dependencies

None.

## References

-   [Apple Developer — ASAuthorizationAppleIDProvider](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidprovider)
-   [Apple Developer — ASAuthorizationAppleIDRequest](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidrequest)
-   [Apple Developer — ASAuthorizationController](https://developer.apple.com/documentation/authenticationservices/asauthorizationcontroller)
-   [Apple Developer — ASAuthorizationControllerDelegate](https://developer.apple.com/documentation/authenticationservices/asauthorizationcontrollerdelegate)
-   [Apple Developer — ASAuthorizationControllerPresentationContextProviding](https://developer.apple.com/documentation/authenticationservices/asauthorizationcontrollerpresentationcontextproviding)
-   [Apple Developer — ASAuthorizationAppleIDCredential](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidcredential)
-   [Apple Developer — ASAuthorizationError](https://developer.apple.com/documentation/authenticationservices/asauthorizationerror-swift.struct)
