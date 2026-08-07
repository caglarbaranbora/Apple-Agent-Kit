# Privacy (Design)

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.privacy
artifact_type: knowledge
title: Privacy (Design)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design-level rules for requesting permissions and communicating data use in iOS/iPadOS interfaces — UI and consent-flow patterns, not the Privacy Manifest/data-use-disclosure implementation.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - privacy
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/privacy
depends_on: []
related: []
last_updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent designs permission-request
UI and consent flows on iOS/iPadOS: when to ask, what the purpose
string must say, and what custom pre-permission screens may and may
not do. It does not cover the Privacy Manifest / data-use-disclosure
implementation, which belongs to the future dedicated `privacy` domain
(see docs/architecture/domain-map.md Cross-Domain Notes).

## Scope

### Included

-   Timing of permission requests (just-in-time vs. launch-time)
-   Purpose-string wording requirements
-   Custom pre-permission screen constraints
-   Tracking-permission-alert integrity rules
-   Lightweight permission surfaces (e.g., location button)

### Excluded

-   Privacy Manifest file contents / data-use disclosure — future `privacy` domain
-   Keychain/credential storage — future `security` domain

## Rules

### Rule 1

Agents MUST request access only to data a specific feature actually
needs, and only when the person is about to use that feature (not at
launch, unless the launch-time need is obvious, e.g. a navigation
app's location access).

### Rule 2

Agents MUST write a purpose string that clearly and specifically
explains why the app needs the requested access, in sentence case,
ending with a period.

### Rule 3

If showing a custom pre-permission screen, agents MUST include only
one button that clearly opens the system alert (label it "Continue" or
"Next," never "Allow") and MUST NOT offer a way to dismiss the screen
without seeing the system alert.

### Rule 4

Agents MUST NOT precede the system tracking-permission alert with a
custom screen designed to confuse or mislead — App Store review
rejects this pattern.

### Rule 5

Agents SHOULD prefer a one-time, lightweight permission surface (e.g.,
the Core Location location button) over the full system prompt when
the use case fits.

## Compliant Example

-   ✓ A maps feature requests location only after the person taps "Share my location," with a purpose string explaining the specific use. (Rules 1, 2)
-   ✓ A custom pre-permission screen has one "Continue" button that opens the system alert. (Rule 3)

## Non-Compliant Example

-   ✗ The app requests camera, contacts, and location access at first launch before any feature needs them. (Rule 1)
-   ✗ A custom pre-permission screen includes a "Skip" option that bypasses the system alert. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)
