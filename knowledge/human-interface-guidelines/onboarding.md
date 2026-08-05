# Onboarding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.onboarding
type: knowledge
title: Onboarding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for structuring an optional, fast, and focused first-run onboarding flow on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - onboarding
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/onboarding
depends_on: []
related:
  - knowledge.human-interface-guidelines.privacy
  - knowledge.human-interface-guidelines.settings
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent structures a first-run
onboarding experience on iOS/iPadOS: when it appears relative to
launch, how much it asks of people, and how it stays optional and
easy to skip or revisit.

## Scope

### Included

-   Timing of onboarding relative to app launch
-   Interactive vs. static teaching approach
-   Making onboarding flows optional, skippable, and re-discoverable
-   Splash-screen brevity and avoiding download-blocked onboarding
-   Placement of legal/licensing content relative to onboarding
-   Sequencing of setup steps, permission requests, and ratings/purchase prompts

### Excluded

-   Onboarding screen implementation code
-   Onboarding copy/wording — see `style-guide`
-   Permission purpose-string wording and system-alert mechanics — see `privacy`
-   Custom in-app settings area structure — see `settings`

## Rules

### Rule 1

Agents MUST present onboarding only after app launch has completed —
it is not part of the launch experience.

### Rule 2

Agents MUST make any prerequisite onboarding/tutorial flow optional
to skip, MUST NOT re-present it automatically on subsequent launches
once skipped, and SHOULD keep it easy to find later (e.g., in a help,
account, or settings area).

### Rule 3

Agents SHOULD favor an interactive, hands-on onboarding experience —
letting people actually perform an action or try a feature — over
static instructional screens.

### Rule 4

Agents SHOULD prefer contextual, in-place tips shown near the
relevant part of the interface over a single upfront onboarding flow,
when the app's structure supports it.

### Rule 5

Agents MUST NOT block onboarding on large downloads and MUST NOT
include licensing/legal agreement text within the onboarding flow.

### Rule 6

Agents SHOULD postpone nonessential setup or customization steps
during onboarding, relying on sensible defaults, and SHOULD defer
ratings or purchase prompts until after people have experienced core
functionality.

### Rule 7

Agents SHOULD integrate a permission request into onboarding only
when doing so helps explain its benefit in context; otherwise defer
the request to the point where the person first uses the feature that
needs it (see `privacy` Rule 1).

## Compliant Example

-   ✓ A photo-editing app skips straight into the editor and offers a "Show me around" tip the first time someone opens a tool, instead of a mandatory multi-screen tutorial. (Rules 3, 4)
-   ✓ A fitness app's onboarding flow can be skipped, and the skipped tutorial remains available later from Settings. (Rule 2)
-   ✓ A navigation app explains and requests location access during onboarding, since the benefit is obvious in context. (Rule 7)

## Non-Compliant Example

-   ✗ A splash-screen-and-slideshow onboarding sequence plays before the app has finished launching. (Rule 1)
-   ✗ Onboarding re-appears every time the app launches even after being skipped once. (Rule 2)
-   ✗ Onboarding requests camera, contacts, and location access up front, before any feature needs them. (Rule 7)

## Dependencies

None.

## References

-   [Apple HIG — Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)
