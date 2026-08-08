# Remote Push Registration

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.usernotifications.remote-push-registration
artifact_type: knowledge
title: Remote Push Registration
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines client-side APNs device-token registration via UIApplication.registerForRemoteNotifications and its app delegate callbacks -- not server-side payload construction.
domain: UserNotifications
tags:
  - usernotifications
  - apns
  - remote-notifications
references:
  - https://developer.apple.com/documentation/uikit/uiapplication/registerforremotenotifications()
  - https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didregisterforremotenotificationswithdevicetoken:)
  - https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didfailtoregisterforremotenotificationswitherror:)
  - https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns
depends_on: []
related:
  - knowledge.usernotifications.authorization-request
  - knowledge.usernotifications.notification-delegate-handling
last_updated: 2026-08-08
```

## Intent

This contract defines the client-side mechanics of registering an app
with Apple Push Notification service (APNs): calling
`registerForRemoteNotifications`, implementing both the success and
failure app-delegate callbacks, and handling the device token correctly.
It does not cover constructing or sending the server-side APNs payload.

## Scope

### Included

-   `UIApplication.registerForRemoteNotifications()` call mechanics and relationship to notification authorization
-   `application(_:didRegisterForRemoteNotificationsWithDeviceToken:)` — device token handling
-   `application(_:didFailToRegisterForRemoteNotificationsWithError:)` — failure handling
-   The Push Notifications capability / entitlement as a registration precondition

### Excluded

-   APNs server-side payload construction, provider server implementation — out of v1 scope entirely
-   `UNAuthorizationOptions` selection and the authorization request itself — see `authorization-request.md`
-   Handling the resulting remote notification once delivered (foreground presentation, response handling) — see `notification-delegate-handling.md`
-   watchOS-specific registration via the extension delegate — deferred, out of v1 scope
-   VoIP push (PushKit) registration — a distinct framework, out of scope

## Rules

### Rule 1

Agents MUST call `registerForRemoteNotifications()` independently of
requesting `UNAuthorizationOptions` — per Apple's documentation for
`registerForRemoteNotifications`: "If you do not request and receive
authorization for your app's interactions, the system delivers all
remote notifications to your app silently." Registration and
authorization are separate calls; omitting the authorization request
does not prevent registration, it only limits how received notifications
are presented.

### Rule 2

Agents MUST implement both
`application(_:didRegisterForRemoteNotificationsWithDeviceToken:)` and
`application(_:didFailToRegisterForRemoteNotificationsWithError:)` — per
Apple: "If registration succeeds, the app calls your app delegate
object's [...] method and passes it a device token... If registration
fails, the app calls its app delegate's [...] method instead." An app
that only implements the success path has no way to detect or retry
after a registration failure.

### Rule 3

Agents MUST send the device token to the provider server on every
successful registration and MUST NOT cache it locally as a substitute —
per Apple: "Never cache the device token locally on the user's device.
Device tokens can change periodically, so caching the value risks
sending an invalid token to your server." Treat each callback invocation
as the source of truth, not a locally persisted prior value.

### Rule 4

Agents MUST NOT assume the device token is a fixed-length value — per
Apple: "APNs device tokens are of variable length. Do not hard-code their
size." Code must forward the `Data` token to the server unmodified rather
than truncating, padding, or hex-encoding it with an assumed byte count.

### Rule 5

Agents MUST implement retry/backoff logic in the failure callback rather
than leaving the app unregistered — per Apple's guidance: "You might use
your implementation of this method to make a note of the failed
registration so that you can try again later." Failures can occur from
network unavailability or APNs being unreachable and are expected to be
transient.

## Compliant Example

```swift
func application(_ application: UIApplication,
                  didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    application.registerForRemoteNotifications() // Independent of UNAuthorizationOptions request.
    return true
}

func application(_ application: UIApplication,
                  didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    sendTokenToServer(deviceToken) // Forwarded unmodified, not cached locally.
}

func application(_ application: UIApplication,
                  didFailToRegisterForRemoteNotificationsWithError error: Error) {
    scheduleRegistrationRetry() // Rule 5.
}
```
Implements both callbacks (Rule 2), forwards the token unmodified (Rules 3, 4), and retries on failure (Rule 5).

## Non-Compliant Example

```swift
func application(_ application: UIApplication,
                  didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    UserDefaults.standard.set(deviceToken, forKey: "cachedToken") // Cached locally -- Rule 3.
}
// didFailToRegisterForRemoteNotificationsWithError is never implemented.
```
Caches the device token locally instead of always forwarding the latest value (Rule 3), and omits the failure callback entirely, leaving no path to detect or retry a failed registration (Rules 2, 5).

## Dependencies

None.

## References

-   [Apple Developer — registerForRemoteNotifications()](https://developer.apple.com/documentation/uikit/uiapplication/registerforremotenotifications())
-   [Apple Developer — didRegisterForRemoteNotificationsWithDeviceToken:](https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didregisterforremotenotificationswithdevicetoken:))
-   [Apple Developer — didFailToRegisterForRemoteNotificationsWithError:](https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didfailtoregisterforremotenotificationswitherror:))
-   [Apple Developer — Registering your app with APNs](https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns)
