# Schemes and Targets

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.xcode.schemes-and-targets
artifact_type: knowledge
title: Schemes and Targets
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct scheme structure — each scheme action (Run/Test/Profile/Analyze/Archive) maps to a build configuration and target set — and shared vs. user scheme management.
domain: Xcode
tags:
  - xcode
  - schemes
  - targets
references:
  - https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project
  - https://developer.apple.com/documentation/xcode/build-system
depends_on: []
related:
  - knowledge.xcode.archive-process
  - knowledge.xcode.automatic-signing
  - knowledge.xcode.build-configurations
  - knowledge.xcode.manual-signing-provisioning-profiles
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent structures and shares an
Xcode scheme so each action (Run, Test, Profile, Analyze, Archive)
builds the right targets under the right configuration, and so the
scheme is visible to teammates and CI rather than trapped in one
developer's local user data.

## Scope

### Included

-   Scheme action → build configuration mapping (Run/Test/Analyze default to Debug; Profile/Archive default to Release)
-   Shared vs. user schemes: the "Shared" checkbox, `xcshareddata` vs. `xcuserdata` storage location
-   Wiring a target into the correct scheme action (Build, Run, Test, Archive)

### Excluded

-   Build configuration definitions themselves — see `build-configurations`
-   Code signing for a scheme's targets — see `automatic-signing`/`manual-signing-provisioning-profiles`

## Rules

### Rule 1

Agents MUST mark a scheme "Shared" (Manage Schemes → Shared checkbox)
before committing it — an unshared scheme is written to
`xcuserdata/<username>.xcuserdatad/xcschemes/`, which is user-specific
and excluded from meaningful version control; teammates and CI checking
out the project won't see it.

### Rule 2

Agents MUST NOT change the Archive action's build configuration away
from Release without an explicit, stated reason — Xcode's default
scheme maps Archive to Release; switching it to Debug ships an
unoptimized, non-stripped binary through the same archive/export flow
used for App Store submission and TestFlight.

### Rule 3

Agents MUST verify a newly added target is wired into the correct
scheme action — e.g. a new watch app extension target added to the Run
action, a new unit test target added to the Test action — a target that
exists in the project but isn't included in any scheme action silently
never builds or runs when that scheme executes.

### Rule 4

Agents SHOULD keep one scheme per distributable product (the app, a
widget extension, a watch app) rather than combining unrelated targets
into a single scheme's Build action — this keeps the Test and Archive
actions scoped to exactly what's being validated or shipped for that
product.

## Compliant Example

-   ✓ A new scheme is created for a widget extension target, marked Shared, and stored at `<Project>.xcodeproj/xcshareddata/xcschemes/` — it is committed to git so CI and teammates can build and archive the widget independently of the app. (Rule 1)

## Non-Compliant Example

-   ✗ A developer duplicates the app scheme to test a build flag, leaves "Shared" unchecked, and the scheme is written only to their local `xcuserdata`. CI's checkout has no such scheme, and the pipeline fails with "scheme not found" until someone notices the checkbox was never set. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Customizing the build schemes for a project](https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project)
-   [Apple Developer — Build system](https://developer.apple.com/documentation/xcode/build-system)
