# App Transport Security

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.networking.app-transport-security
artifact_type: knowledge
title: App Transport Security
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines App Transport Security's HTTPS/TLS requirements and how to declare a narrowly-scoped Info.plist exception when genuinely required, rather than a blanket allow-arbitrary-loads exception.
domain: Networking
tags:
  - networking
  - ats
  - security
references:
  - https://developer.apple.com/documentation/security/preventing-insecure-network-connections
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent handles App Transport
Security (ATS) requirements — HTTPS with TLS 1.2 or later by default —
and how to declare a narrowly-scoped exception in `Info.plist` only when
a specific domain genuinely cannot meet that requirement, rather than
disabling ATS protection app-wide.

## Scope

### Included

-   ATS's default HTTPS/TLS 1.2+ requirement
-   `NSAppTransportSecurity`/`NSExceptionDomains` scoped Info.plist exceptions
-   Why `NSAllowsArbitraryLoads` is a last resort, not a default fix

### Excluded

-   `URLSessionDelegate` certificate/challenge handling — see
    `server-trust-evaluation` and `authentication-challenges`
-   App Store Review's evaluation of ATS exceptions — that's a submission-review concern, not an implementation one

## Rules

### Rule 1

Agents MUST NOT set `NSAllowsArbitraryLoads` to `true` in `Info.plist`
to work around an ATS connection failure — this disables ATS protection
for every network connection the app makes, not just the one that
failed, and is treated by App Review as requiring strong justification.

### Rule 2

Agents MUST scope any necessary ATS exception to the specific domain
via `NSExceptionDomains`, setting only the specific keys that domain
actually needs (e.g. `NSExceptionAllowsInsecureHTTPLoads` or
`NSExceptionMinimumTLSVersion`) rather than a blanket app-wide
exception — the narrowest exception that solves the actual problem.

### Rule 3

Agents SHOULD treat an ATS connection failure as a signal to fix the
server's TLS configuration (upgrade to TLS 1.2+, obtain a valid
certificate) before reaching for an `Info.plist` exception — an
exception is a documented last resort, not the default response to an
ATS failure.

### Rule 4

Agents MUST NOT implement a `URLSessionDelegate` certificate-validation
callback that unconditionally trusts any certificate as a way to bypass
an ATS or TLS failure — doing so removes protection against a
man-in-the-middle attack for that connection entirely, regardless of
whether an ATS exception is also present.

## Compliant Example

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>legacy-internal.example.com</key>
        <dict>
            <key>NSExceptionMinimumTLSVersion</key>
            <string>TLSv1.1</string>
            <key>NSIncludesSubdomains</key>
            <true/>
        </dict>
    </dict>
</dict>
```
Exception scoped to one specific legacy internal domain with only the minimum-TLS-version key needed, rather than a blanket app-wide allowance. (Rules 1, 2)

## Non-Compliant Example

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```
A blanket exception disabling ATS for every connection the app makes, applied to work around one endpoint's TLS issue. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Preventing Insecure Network Connections](https://developer.apple.com/documentation/security/preventing-insecure-network-connections)
