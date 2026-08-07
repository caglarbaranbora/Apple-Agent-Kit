# Pass Updates and Push Registration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.passkit.pass-updates-and-push-registration
artifact_type: knowledge
title: Pass Updates and Push Registration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how an already-added pass gets updated -- the webServiceURL/authenticationToken fields on a pass, the device-to-server web-service registration protocol, and why the app itself registers for no PassKit-specific push type, drawing a hard app-vs-server boundary.
domain: PassKit
tags:
  - passkit
  - webserviceurl
  - authenticationtoken
  - pass-updates
  - web-service
references:
  - https://developer.apple.com/documentation/passkit/pkpass/webserviceurl
  - https://developer.apple.com/documentation/passkit/pkpass/authenticationtoken
  - https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes
  - https://developer.apple.com/documentation/walletpasses/register-a-pass-for-update-notifications
depends_on:
  - knowledge.passkit.pass-content-and-required-fields
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an already-added Wallet pass receives updates, and draws the boundary between what the hosting app's Swift code does (essentially nothing) and what the pass's `webServiceURL`/`authenticationToken` fields and the developer's own web service are responsible for. It corrects a natural but wrong assumption: there is no app-side PassKit/PushKit API an app registers with to receive pass-update pushes — that entire path runs between the device's system Wallet component, Apple's servers, and the developer's web service.

## Scope

### Included

-   The `webServiceURL`/`authenticationToken` fields on `PKPass`/`pass.json` that make a pass updatable at all
-   The high-level shape of the web-service protocol: device registration, Apple Push Notification service (APNs) triggering, and the device's follow-up requests for updated serial numbers
-   Why this protocol is a server-implemented REST contract, not a set of Swift API calls, and why no `PKPushRegistry`/`PKPushType` registration exists in the app for this purpose
-   What changing vs. not changing on an update means for `serialNumber`/`authenticationToken`

### Excluded

-   `.pkpass`/`pass.json` field authoring and signing in general — see `pass-content-and-required-fields`
-   Implementing the web-service server endpoints themselves (out of scope entirely for this app-side domain — see Explicit Exclusions in the PassKit reference)
-   Querying/adding passes through `PKPassLibrary`, and the add-to-Wallet UI — see `pass-library-and-authorization` / `adding-passes-ui`

## Rules

### Rule 1

Agents making a pass updatable MUST set both `webServiceURL` and `authenticationToken` on the pass at creation time, and MUST treat their absence as "this pass can never be updated after distribution." Per Apple's documentation, `webServiceURL` is "The URL for the web service... for updating passes," and `authenticationToken` is "The token for authenticating update requests... Use this property to store an authentication token for your web service. When the device requests an updated copy of the pass, the request's header includes this authorization token."

### Rule 2

Agents MUST NOT change a pass's `authenticationToken` on an update, since Apple's documentation states plainly: "Don't change the authentication token during an update." Agents MUST also keep `serialNumber` stable across an update, since Apple's web-service documentation describes an update as producing "a new pass with the same pass type identifier and serial number" — a changed serial number creates a distinct pass registration, not an update to the existing one.

### Rule 3

Agents MUST treat the device-registration, push-trigger, and updated-serial-number-fetch sequence as a REST protocol the developer's server implements and the device's system Wallet component calls — never as Swift methods the hosting app invokes. Apple's own Wallet Passes documentation lists this sequence as three distinct HTTP endpoints under "Web Service Endpoint" role — registering a device (`POST /v1/devices/{deviceLibraryIdentifier}/registrations/{passTypeIdentifier}/{serialNumber}`, with a `PushToken` request body), fetching updated serial numbers (`GET /v1/devices/{deviceLibraryIdentifier}/registrations/{passTypeIdentifier}?passesUpdatedSince={tag}`), and returning the updated pass — none of which the app's own code calls or exposes.

### Rule 4

Agents MUST NOT implement a `PKPushRegistry` registration for a pass-update push type, because no such PassKit push type exists in current PushKit: `PKPushType` documents exactly three cases — `.complication`, `.fileProvider`, and `.voIP` — with no pass-related case. This corrects a natural assumption based on how the same app registers for other silent-push categories; the device's push token used to notify a pass update is captured and sent to the developer's server entirely by the system Wallet component (as the `PushToken` body of the device-registration endpoint in Rule 3), with zero participation from the hosting app's Swift code.

### Rule 5

Agents MUST scope the app's own responsibility to authoring correct `webServiceURL`/`authenticationToken` values into the pass (Rule 1) and nothing else in this update path — server authentication of registration/update calls using the pass's `authenticationToken`, storage of device-to-pass registrations, and sending the APNs push itself are entirely the developer's server's job, per Apple's guidance that the server must "Authenticate each call to your server using a shared secret... Use the value of [`authenticationToken`] for the pass to authenticate the calls that register and unregister a pass." Agents MUST NOT present any of these server responsibilities as something the app calls at runtime.

## Compliant Example

```json
{
  "passTypeIdentifier": "pass.com.example.loyalty",
  "serialNumber": "abc123",
  "webServiceURL": "https://passes.example.com/",
  "authenticationToken": "a-long-random-per-pass-secret"
}
```
The app's only job is authoring these two fields correctly at pass-creation time (Rule 1); it makes no further API calls related to updates — registration, push delivery, and serving updated serial numbers are entirely the developer's server and Apple's push infrastructure (Rule 3, Rule 4, Rule 5).

## Non-Compliant Example

```swift
import PushKit

final class PassUpdateHandler: NSObject, PKPushRegistryDelegate {
    let registry = PKPushRegistry(queue: .main)

    func start() {
        // No such push type exists for pass updates -- violates Rule 4.
        registry.desiredPushTypes = [PKPushType(rawValue: "PKPass")]
        registry.delegate = self
    }

    func pushRegistry(_ registry: PKPushRegistry, didUpdatePushCredentials pushCredentials: PKPushCredentials, for type: PKPushType) {
        // Also assumes the app must forward its own push token for pass updates,
        // when the system Wallet component handles this, not the app -- violates Rule 4 and Rule 5.
    }
}
```
Invents a nonexistent `PKPushType` for passes and assumes the hosting app must register for and forward pass-update push tokens itself, when neither API nor responsibility exists on the app side (Rule 4, Rule 5).

## Dependencies

-   `knowledge.passkit.pass-content-and-required-fields` — this contract assumes the pass already declares valid `webServiceURL`/`authenticationToken` fields as part of its `pass.json`.

## References

-   [Apple Developer — webServiceURL](https://developer.apple.com/documentation/passkit/pkpass/webserviceurl)
-   [Apple Developer — authenticationToken](https://developer.apple.com/documentation/passkit/pkpass/authenticationtoken)
-   [Apple Developer — Adding a Web Service to Update Passes](https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes)
-   [Apple Developer — Register a Pass for Update Notifications](https://developer.apple.com/documentation/walletpasses/register-a-pass-for-update-notifications)
