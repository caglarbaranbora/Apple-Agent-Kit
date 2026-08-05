# Xcode Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `xcode` domain (1 Reference, 8 Knowledge Contracts, 1 native Skill) covering Xcode project configuration — build configurations/`.xcconfig` files, schemes/targets, automatic and manual code signing, entitlements/capabilities, and the archive-to-export workflow — per `docs/superpowers/specs/2026-08-01-xcode-domain-design.md`, replacing the placeholder `xcode` row in `docs/architecture/domain-map.md`.

**Architecture:** Mirrors the `networking` and `sf-symbols` domains exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. Unlike the Swift-API domains built earlier this session, this domain's subject matter is Xcode project-file/GUI configuration, not `.swift` source — Compliant/Non-Compliant Examples use the ✓/✗ workflow-description style established by `app-store-review-guidelines`, except for the two topics with a real text-file format (`xcconfig-files`), where a fenced code block is used instead. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/xcode.md`

**Files:**
- Create: `references/apple/xcode.md`

- [ ] **Step 1: Create the file**

```markdown
# Xcode

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/xcode

## Purpose

Reference index for Apple's Xcode project-configuration documentation,
scoped to this domain's v1: build configurations and `.xcconfig` files,
schemes and targets, automatic and manual code signing,
entitlements/capabilities, and the archive-to-export workflow.
`xcodebuild` command-line usage, CI signing automation (fastlane,
`match`), Swift Package Manager build configuration, macOS-specific
signing/notarization, and Xcode Cloud are deferred to a future pass.

## Primary Topics

- Build configurations
- xcconfig files
- Schemes and targets
- Automatic signing
- Manual signing & provisioning profiles
- Entitlements & capabilities
- Archive process
- Export options

## Used By

- knowledge/xcode/build-configurations.md ([[knowledge/xcode/build-configurations]])
- knowledge/xcode/xcconfig-files.md ([[knowledge/xcode/xcconfig-files]])
- knowledge/xcode/schemes-and-targets.md ([[knowledge/xcode/schemes-and-targets]])
- knowledge/xcode/automatic-signing.md ([[knowledge/xcode/automatic-signing]])
- knowledge/xcode/manual-signing-provisioning-profiles.md ([[knowledge/xcode/manual-signing-provisioning-profiles]])
- knowledge/xcode/entitlements-capabilities.md ([[knowledge/xcode/entitlements-capabilities]])
- knowledge/xcode/archive-process.md ([[knowledge/xcode/archive-process]])
- knowledge/xcode/export-options.md ([[knowledge/xcode/export-options]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/xcode.md --type reference`
Expected: `PASS: references/apple/xcode.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/xcode.md
git commit -m "docs: add xcode reference index"
```

---

## Task 2: Knowledge Contract — `build-configurations`

**Files:**
- Create: `knowledge/xcode/build-configurations.md`

- [ ] **Step 1: Create the file**

```markdown
# Build Configurations

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.build-configurations
type: knowledge
title: Build Configurations
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of build configurations (Debug/Release, custom configurations) and Build Settings scoping (project vs. target, per-configuration) so build behavior stays predictable across environments.
domain: Xcode
tags:
  - xcode
  - build-configurations
  - build-settings
references:
  - https://developer.apple.com/documentation/xcode/configuring-the-build-settings-of-a-target
  - https://developer.apple.com/documentation/xcode/build-settings-reference
depends_on: []
related:
  - knowledge.xcode.xcconfig-files
  - knowledge.xcode.schemes-and-targets
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent edits build configurations
and Build Settings so a Debug build and a Release build behave
predictably differently — without leaking Debug-only values into a
Release/App Store build, or accidentally applying a target-specific
change to every target in the project.

## Scope

### Included

-   Debug/Release build configurations, adding a custom configuration
-   Build Settings scope: project-level vs. target-level, per-configuration ("Any Configuration" vs. a specific configuration column)
-   `SWIFT_ACTIVE_COMPILATION_CONDITIONS` / `GCC_PREPROCESSOR_DEFINITIONS` as the mechanism behind `#if DEBUG`-style conditional compilation

### Excluded

-   `.xcconfig` file authoring and precedence — see `xcconfig-files`
-   Mapping a scheme action (Run/Archive/Test) to a configuration — see `schemes-and-targets`

## Rules

### Rule 1

Agents MUST set a build-time value that should differ between Debug and
Release on the specific configuration column (Debug or Release), not
under "Any Configuration" (the Multiple Values placeholder), when the
two configurations need different values — setting it under "Any
Configuration" silently forces both configurations to the same value.

### Rule 2

Agents MUST NOT rely on `#if DEBUG` or a custom condition like
`#if RELEASE` without confirming the corresponding compilation condition
is actually defined for that configuration in
`SWIFT_ACTIVE_COMPILATION_CONDITIONS` (Swift) or
`GCC_PREPROCESSOR_DEFINITIONS` (Objective-C) — `DEBUG` is defined by
Xcode's default new-project template for the Debug configuration, but it
is not a Swift language built-in; a custom condition that was never
added to a configuration's compilation-condition setting never compiles
true, and the branch silently never runs.

### Rule 3

Agents MUST scope a new build setting at target level, not project
level, when only one target needs it — a project-level setting silently
applies to every target in the project, including targets (a widget
extension, a test target) that shouldn't inherit it.

### Rule 4

Agents SHOULD add a new configuration by duplicating an existing one
(the editor's "Duplicate 'Release' Configuration" action) rather than
creating one from scratch — duplicating preserves Xcode's per-configuration
default Build Settings values, which are easy to omit when starting
from nothing and leave the new configuration behaving inconsistently
with its siblings.

## Compliant Example

-   ✓ A new "Staging" configuration is created by duplicating "Release". A user-defined `API_BASE_URL` build setting is set per-configuration (Debug: staging URL, Staging: staging URL, Release: production URL), referenced from Info.plist as `$(API_BASE_URL)` and read at runtime via `Bundle.main.object(forInfoDictionaryKey:)` — no configuration-specific value is hardcoded in Swift source. (Rules 1, 4)

## Non-Compliant Example

-   ✗ The production API URL is hardcoded as a Swift string literal, and `#if RELEASE` is used to branch to a "production-only" code path — but no configuration's `SWIFT_ACTIVE_COMPILATION_CONDITIONS` was ever given a `RELEASE` value, so the `#if RELEASE` branch never compiles in and the intended code path never runs, in any configuration. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — Configuring the build settings of a target](https://developer.apple.com/documentation/xcode/configuring-the-build-settings-of-a-target)
-   [Apple Developer — Build settings reference](https://developer.apple.com/documentation/xcode/build-settings-reference)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/build-configurations.md --type knowledge`
Expected: `PASS: knowledge/xcode/build-configurations.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/build-configurations.md
git commit -m "feat: add build-configurations knowledge contract"
```

---

## Task 3: Knowledge Contract — `xcconfig-files`

**Files:**
- Create: `knowledge/xcode/xcconfig-files.md`

- [ ] **Step 1: Create the file**

```markdown
# xcconfig Files

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.xcconfig-files
type: knowledge
title: xcconfig Files
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct authoring and attachment of .xcconfig build configuration files, and how xcconfig-supplied values interact with Build Settings UI values.
domain: Xcode
tags:
  - xcode
  - xcconfig
  - build-settings
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev745c5c974.html
  - https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project
depends_on: []
related:
  - knowledge.xcode.build-configurations
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent authors and attaches an
`.xcconfig` file so its values compose correctly with values Xcode or
another `.xcconfig` file already set, instead of silently overwriting
them.

## Scope

### Included

-   `.xcconfig` syntax: `KEY = value`, `$(inherited)`, `#include`/`#include?`
-   Attaching an `.xcconfig` file to a project or target configuration
-   Precedence between an `.xcconfig` value and a Build Settings UI value for the same key

### Excluded

-   Build configuration lifecycle itself (Debug/Release/custom) — see `build-configurations`
-   Where a given build setting is documented/what it controls — see `build-configurations`

## Rules

### Rule 1

Agents MUST include `$(inherited)` when appending to a settings key that
Xcode or a base `.xcconfig` also populates (e.g. `OTHER_SWIFT_FLAGS`,
`HEADER_SEARCH_PATHS`) — omitting it replaces the base value instead of
extending it, silently dropping flags another layer already set.

### Rule 2

Agents MUST use `#include "Base.xcconfig"` (a relative path) to share
settings across multiple configuration files rather than duplicating
key-value pairs across them — duplicated values drift out of sync the
first time one copy is edited and the other isn't.

### Rule 3

Agents MUST NOT assume an `.xcconfig` value overrides an explicit Build
Settings UI value for the same key at the same level — the reverse is
true: an explicit UI-entered value always wins over the xcconfig-supplied
value; the xcconfig value only takes effect where the UI field is left
blank.

### Rule 4

Agents SHOULD store environment-specific secrets (API keys, tokens) as
values in an `.xcconfig` file excluded from version control, included
via the optional-include syntax (`#include? "Secrets.xcconfig"`) rather
than committing them in a tracked file or hardcoding them in Swift — the
`?` makes the include a no-op (not a build error) when the file is
absent, e.g. on a fresh clone or CI checkout before secrets are
provisioned.

## Compliant Example

```
// Config.xcconfig
#include "Base.xcconfig"
#include? "Secrets.xcconfig"

OTHER_SWIFT_FLAGS = $(inherited) -DFEATURE_FLAG_X
API_BASE_URL = https://api.example.com
```
Extends `OTHER_SWIFT_FLAGS` with `$(inherited)` instead of replacing it, shares common settings via `#include`, and pulls secrets from an optional, untracked file via `#include?`. (Rules 1, 2, 4)

## Non-Compliant Example

```
// Config.xcconfig
OTHER_SWIFT_FLAGS = -DFEATURE_FLAG_X
```
Overwrites any `OTHER_SWIFT_FLAGS` value Xcode or a base `.xcconfig` already set instead of extending it — `$(inherited)` is omitted. (Rule 1)

## Dependencies

None.

## References

-   [Apple — Configuration Settings File (.xcconfig) format](https://help.apple.com/xcode/mac/current/en.lproj/dev745c5c974.html)
-   [Apple Developer — Adding a build configuration file to your project](https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/xcconfig-files.md --type knowledge`
Expected: `PASS: knowledge/xcode/xcconfig-files.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/xcconfig-files.md
git commit -m "feat: add xcconfig-files knowledge contract"
```

---

## Task 4: Knowledge Contract — `schemes-and-targets`

**Files:**
- Create: `knowledge/xcode/schemes-and-targets.md`

- [ ] **Step 1: Create the file**

```markdown
# Schemes and Targets

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.schemes-and-targets
type: knowledge
title: Schemes and Targets
version: 0.1.0
status: Draft
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
  - knowledge.xcode.build-configurations
  - knowledge.xcode.archive-process
updated: 2026-08-01
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
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/schemes-and-targets.md --type knowledge`
Expected: `PASS: knowledge/xcode/schemes-and-targets.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/schemes-and-targets.md
git commit -m "feat: add schemes-and-targets knowledge contract"
```

---

## Task 5: Knowledge Contract — `automatic-signing`

**Files:**
- Create: `knowledge/xcode/automatic-signing.md`

- [ ] **Step 1: Create the file**

```markdown
# Automatic Signing

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.automatic-signing
type: knowledge
title: Automatic Signing
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of Xcode-managed (automatic) code signing — Development Team selection, Xcode-generated certificates/profiles, and device registration.
domain: Xcode
tags:
  - xcode
  - code-signing
  - automatic-signing
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev60b6fbbc7.html
  - https://help.apple.com/xcode/mac/current/en.lproj/dev23aab79b4.html
depends_on: []
related:
  - knowledge.xcode.manual-signing-provisioning-profiles
  - knowledge.xcode.entitlements-capabilities
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent configures Xcode-managed
(automatic) code signing so a target builds and installs on a device
without a manually-selected certificate or provisioning profile, and how
to correctly diagnose the signing-identity errors that are still
possible under automatic signing.

## Scope

### Included

-   Enabling "Automatically manage signing" and selecting a Development Team
-   How Xcode creates and renews development/distribution certificates and provisioning profiles
-   Device registration for a Debug build's run destination

### Excluded

-   Manual signing / explicit provisioning profile selection — see `manual-signing-provisioning-profiles`
-   Capabilities/entitlements and their effect on provisioning — see `entitlements-capabilities`

## Rules

### Rule 1

Agents MUST set a Development Team on every target that gets built or
archived (Signing & Capabilities → Team) — a target with no team
selected and automatic signing enabled fails to build with a
code-signing error, since Xcode has no Apple Developer account under
which to generate a certificate or profile.

### Rule 2

Agents MUST NOT assume automatic signing alone provisions a physical
test device — a new device must still be registered to the account
(Xcode registers it automatically the first time that device is chosen
as a run destination, or it can be added manually in the account's
device list); an unregistered device fails to install a Debug build
even with automatic signing correctly configured.

### Rule 3

Agents SHOULD leave "Automatically manage signing" enabled for
Debug/development builds unless the project has a specific need — e.g.
CI without an interactively-logged-in Apple ID, or an Ad Hoc/Enterprise
distribution profile with entitlements not available to automatic
signing — that requires manual signing (see
`manual-signing-provisioning-profiles`). Automatic signing is Apple's
recommended default and removes an entire class of
expired-certificate/profile-mismatch failures for day-to-day
development.

### Rule 4

Agents MUST check the target's actual Team setting before regenerating
certificates or changing the bundle identifier in response to a "no
signing certificate found" error — this error is frequently caused by
the wrong team being selected (e.g. after cloning a project set up under
a different Apple Developer account), not by a genuinely missing
certificate.

## Compliant Example

-   ✓ A target has "Automatically manage signing" checked and Team set to the project's actual Apple Developer account. Xcode generates a development certificate and provisioning profile the first time the app is run on a connected device. (Rules 1, 3)

## Non-Compliant Example

-   ✗ A project cloned from another developer's machine still has their Team selected in Signing & Capabilities. The build fails with "No signing certificate found," and the agent starts regenerating certificates in the Apple Developer account before checking whether the Team dropdown points at the wrong account. (Rule 4)

## Dependencies

None.

## References

-   [Apple — Signing & Capabilities workflow](https://help.apple.com/xcode/mac/current/en.lproj/dev60b6fbbc7.html)
-   [Apple — Assign a project to a team](https://help.apple.com/xcode/mac/current/en.lproj/dev23aab79b4.html)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/automatic-signing.md --type knowledge`
Expected: `PASS: knowledge/xcode/automatic-signing.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/automatic-signing.md
git commit -m "feat: add automatic-signing knowledge contract"
```

---

## Task 6: Knowledge Contract — `manual-signing-provisioning-profiles`

**Files:**
- Create: `knowledge/xcode/manual-signing-provisioning-profiles.md`

- [ ] **Step 1: Create the file**

```markdown
# Manual Signing & Provisioning Profiles

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.manual-signing-provisioning-profiles
type: knowledge
title: Manual Signing & Provisioning Profiles
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct manual code signing — selecting an explicit certificate and provisioning profile, and matching profile type (Development/Ad Hoc/Enterprise/App Store Connect) to build purpose.
domain: Xcode
tags:
  - xcode
  - code-signing
  - provisioning-profiles
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev1bf96f17e.html
  - https://help.apple.com/xcode/mac/current/en.lproj/devcac6ab5b3.html
  - https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles
depends_on: []
related:
  - knowledge.xcode.automatic-signing
  - knowledge.xcode.entitlements-capabilities
  - knowledge.xcode.export-options
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent selects an explicit
certificate and provisioning profile for manual signing, and how to
match profile type to build purpose so a device install or distribution
export doesn't fail for a mismatch reason unrelated to the actual
signing identity.

## Scope

### Included

-   Certificate types (Development vs. Distribution)
-   Provisioning profile types: Development, Ad Hoc, Enterprise/In-House, App Store Connect
-   Turning off "Automatically manage signing" and selecting a specific profile
-   Common manual-signing failure modes: App ID mismatch, missing device UDID, expired certificate/profile

### Excluded

-   Automatic signing — see `automatic-signing`
-   Entitlements/capabilities that constrain which profile is valid — see `entitlements-capabilities`
-   Selecting a distribution method during export — see `export-options`

## Rules

### Rule 1

Agents MUST match the provisioning profile's type to the build's
purpose: Development for local device testing (must list the device's
UDID), Ad Hoc for testing on a fixed set of registered devices outside
the App Store, Enterprise/In-House for internal distribution under an
Apple Developer Enterprise Program account, and App Store Connect for
submission/TestFlight — using the wrong type either fails to install on
the target device or is rejected downstream, even when the certificate
itself is valid.

### Rule 2

Agents MUST verify a provisioning profile's App ID matches the target's
bundle identifier exactly, or via a matching wildcard App ID, before
assigning it — a profile issued for a different bundle identifier is not
selectable for manual signing, and Xcode reports that the profile
"doesn't match" the target.

### Rule 3

Agents MUST confirm a Development or Ad Hoc profile lists every device's
UDID the build needs to install on before assuming a signing-identity
problem — Apple regenerates the profile when a device is added to the
account's registered device list; a "this app cannot be installed
because its integrity could not be verified" or "device not eligible"
failure is frequently a stale device list, not a certificate issue.

### Rule 4

Agents MUST NOT reuse an expired certificate or provisioning profile —
both carry an expiration date (profiles: one year; Development and
Distribution certificates: typically one year), and Xcode/`codesign`
reject signing with an expired credential outright rather than merely
warning.

## Compliant Example

-   ✓ An Ad Hoc distribution profile is selected manually. Its App ID matches the target's bundle identifier, and every QA device's UDID is confirmed present in the profile before building. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ An App Store Connect profile is used to try installing a build directly on a physical device outside TestFlight. App Store Connect profiles don't authorize direct device installation, so the install fails, and the agent misdiagnoses it as a certificate problem instead of the wrong profile type. (Rule 1)

## Dependencies

None.

## References

-   [Apple — Manually sign an app](https://help.apple.com/xcode/mac/current/en.lproj/dev1bf96f17e.html)
-   [Apple — Manually manage distribution signing](https://help.apple.com/xcode/mac/current/en.lproj/devcac6ab5b3.html)
-   [Apple Developer — TN3125: Inside Code Signing: Provisioning Profiles](https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/manual-signing-provisioning-profiles.md --type knowledge`
Expected: `PASS: knowledge/xcode/manual-signing-provisioning-profiles.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/manual-signing-provisioning-profiles.md
git commit -m "feat: add manual-signing-provisioning-profiles knowledge contract"
```

---

## Task 7: Knowledge Contract — `entitlements-capabilities`

**Files:**
- Create: `knowledge/xcode/entitlements-capabilities.md`

- [ ] **Step 1: Create the file**

```markdown
# Entitlements & Capabilities

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.entitlements-capabilities
type: knowledge
title: Entitlements & Capabilities
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct addition of a capability via Signing & Capabilities and the resulting entitlements file, and how a capability constrains which provisioning profile is valid.
domain: Xcode
tags:
  - xcode
  - entitlements
  - capabilities
references:
  - https://developer.apple.com/documentation/bundleresources/entitlements
  - https://help.apple.com/xcode/mac/current/en.lproj/dev88ff319e7.html
depends_on: []
related:
  - knowledge.xcode.automatic-signing
  - knowledge.xcode.manual-signing-provisioning-profiles
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent adds a capability to a
target so the generated `.entitlements` file, the App ID's registered
capabilities, and the provisioning profile all stay consistent with each
other.

## Scope

### Included

-   Adding a capability via Signing & Capabilities (+ Capability)
-   The generated `.entitlements` file and its keys
-   Why adding or removing a capability can invalidate an existing manually-managed provisioning profile

### Excluded

-   Which capability a feature needs at a design/architecture level — implementation-only here
-   Sign in with Apple UX/flow — see the `authentication` domain

## Rules

### Rule 1

Agents MUST add a capability through Signing & Capabilities (the
+ Capability button), not by hand-editing the `.entitlements` file
directly, when automatic signing is enabled — Xcode also registers the
capability on the App ID in the Developer account and regenerates the
provisioning profile to match; a hand-edited entitlements file
requesting a capability the App ID isn't registered for fails code
signing.

### Rule 2

Agents MUST regenerate (or let Xcode regenerate) the provisioning
profile after adding or removing a capability under manual signing — a
profile issued before the capability was added does not grant it;
building with the stale profile fails with an entitlements-mismatch
signing error.

### Rule 3

Agents MUST keep the `.entitlements` file's keys consistent with what
the target actually uses — a leftover entitlement (e.g. Push
Notifications left in the file after removing the notification code)
still requires App ID registration and profile support, and is a
capability with no observable app behavior to justify it.

### Rule 4

Agents MUST use the exact entitlement key Apple defines for a capability
(e.g. `com.apple.developer.associated-domains`,
`com.apple.security.application-groups`) — a misspelled or incorrect key
is silently ignored by the OS at runtime rather than producing a build
error, so the capability appears configured but does nothing.

## Compliant Example

-   ✓ The App Groups capability is added via Signing & Capabilities. Xcode writes `com.apple.security.application-groups` to `<Target>.entitlements` and registers the group ID on the App ID automatically. (Rule 1)

## Non-Compliant Example

-   ✗ An entitlement key is typed by hand into the `.entitlements` file with a typo (`com.apple.security.aplication-groups`). The build signs successfully, but the app group silently doesn't work at runtime, since the OS doesn't recognize the misspelled key. (Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements)
-   [Apple — Add a capability to a target](https://help.apple.com/xcode/mac/current/en.lproj/dev88ff319e7.html)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/entitlements-capabilities.md --type knowledge`
Expected: `PASS: knowledge/xcode/entitlements-capabilities.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/entitlements-capabilities.md
git commit -m "feat: add entitlements-capabilities knowledge contract"
```

---

## Task 8: Knowledge Contract — `archive-process`

**Files:**
- Create: `knowledge/xcode/archive-process.md`

- [ ] **Step 1: Create the file**

```markdown
# Archive Process

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.archive-process
type: knowledge
title: Archive Process
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct archive workflow — Product > Archive and validating the resulting archive in the Organizer — before it is exported or uploaded.
domain: Xcode
tags:
  - xcode
  - archive
  - organizer
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev1bc569500.html
  - https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases
depends_on: []
related:
  - knowledge.xcode.schemes-and-targets
  - knowledge.xcode.export-options
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent produces a valid archive —
choosing the correct run destination, running Product → Archive, and
validating the result in the Organizer — before any export or upload is
attempted.

## Scope

### Included

-   Run-destination prerequisite for Archive to be enabled (a physical device or "Any iOS Device", not a Simulator)
-   Product → Archive and the Organizer window
-   "Validate App" in the Organizer before "Distribute App"
-   Retaining the `.xcarchive` (and its dSYMs) after upload

### Excluded

-   Export destination/method selection and IPA export — see `export-options`

## Rules

### Rule 1

Agents MUST select a physical-device or "Any iOS Device (arm64)" run
destination before archiving — Product → Archive is disabled when the
active scheme's run destination is a Simulator, since Simulator builds
aren't code-signed for distribution and don't produce a device-slice
binary.

### Rule 2

Agents MUST run "Validate App" in the Organizer before "Distribute App"
for a submission-bound archive — validation checks App Store Connect
requirements (Info.plist keys, icon completeness, entitlement/capability
consistency) locally and surfaces the same class of error App Store
Connect would otherwise reject on upload, but faster and without
consuming an upload attempt.

### Rule 3

Agents MUST NOT delete an archive from the Organizer immediately after a
successful upload — the `.xcarchive` is the only local artifact
containing the dSYMs needed to symbolicate crash reports for that exact
build; Xcode does not retain a separate copy once the archive is
removed.

### Rule 4

Agents SHOULD confirm the scheme's Archive action build configuration is
Release (see `schemes-and-targets`) before archiving for distribution —
an archive built under a Debug configuration is unoptimized and may
include debug-only code paths that shouldn't ship.

## Compliant Example

-   ✓ The run destination is set to "Any iOS Device (arm64)", Product → Archive completes, and "Validate App" is run in the Organizer and passes before "Distribute App" is used. (Rules 1, 2)

## Non-Compliant Example

-   ✗ The scheme's run destination is left on an iOS Simulator when Product → Archive is attempted. The menu item is disabled, and the agent misdiagnoses it as project corruption instead of a destination-selection issue. (Rule 1)

## Dependencies

None.

## References

-   [Apple — About Archives organizer](https://help.apple.com/xcode/mac/current/en.lproj/dev1bc569500.html)
-   [Apple Developer — Distributing your app for beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/archive-process.md --type knowledge`
Expected: `PASS: knowledge/xcode/archive-process.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/archive-process.md
git commit -m "feat: add archive-process knowledge contract"
```

---

## Task 9: Knowledge Contract — `export-options`

**Files:**
- Create: `knowledge/xcode/export-options.md`

- [ ] **Step 1: Create the file**

```markdown
# Export Options

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.export-options
type: knowledge
title: Export Options
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the Organizer's Distribute App export flow — distribution-method selection and signing-option choice — when exporting a signed IPA from an archive.
domain: Xcode
tags:
  - xcode
  - export
  - distribution
references:
  - https://help.apple.com/xcode/mac/current/en.lproj/dev23ea8b877.html
  - https://help.apple.com/xcode/mac/current/en.lproj/devff5ececf8.html
depends_on: []
related:
  - knowledge.xcode.archive-process
  - knowledge.xcode.manual-signing-provisioning-profiles
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent exports a signed `.ipa`
from an archive via the Organizer's Distribute App flow — choosing the
distribution method and signing option that match the archive's intended
destination.

## Scope

### Included

-   Organizer "Distribute App" flow
-   Distribution-method selection: App Store Connect, Ad Hoc, Enterprise, Development
-   Automatic vs. manual re-signing during export
-   Re-validating an archive per distribution method

### Excluded

-   `xcodebuild -exportArchive` / CLI `ExportOptions.plist` authoring for scripted export — CLI is out of v1 scope, see `docs/architecture/domain-map.md`
-   Archiving itself — see `archive-process`

## Rules

### Rule 1

Agents MUST choose the distribution method matching the archive's
intended destination: App Store Connect for submission/TestFlight, Ad
Hoc for a fixed set of registered devices, Enterprise for in-house
distribution under an Enterprise Program account, Development for
installing directly on a connected device without going through
TestFlight — choosing the wrong method produces a correctly-signed but
unusable-for-the-intended-purpose `.ipa` (e.g. an Ad Hoc export won't
install on a device that isn't in the profile).

### Rule 2

Agents MUST select automatic signing during export whenever the archive
itself was built with automatic signing, unless a specific manual
profile is required for that distribution method — mixing an
automatic-signed archive with a manual re-sign step during export
requires a provisioning profile matching the archive's entitlements
exactly, which is easy to get wrong (see
`manual-signing-provisioning-profiles`).

### Rule 3

Agents MUST re-run "Validate App" if the distribution method or signing
option changes between export attempts — a validation pass for one
distribution method (e.g. Development) does not guarantee the same
archive validates for another (e.g. App Store Connect), since
entitlement and capability requirements differ per method.

### Rule 4

Agents SHOULD keep an exported `.ipa` together with its export report
when the export is handed off (e.g. to a QA team distributing via Ad
Hoc) — the export report records exactly which signing identity and
profile were used, which is otherwise hard to reconstruct from the
`.ipa` alone.

## Compliant Example

-   ✓ An archive is exported via Organizer → Distribute App → App Store Connect, with automatic signing selected to match the archive, and "Validate App" is re-run for that specific method before upload. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ An archive intended for App Store submission is exported using the Ad Hoc method, and the resulting `.ipa` is uploaded via Transporter. App Store Connect rejects the upload, since an Ad Hoc-signed `.ipa` isn't signed for App Store distribution. (Rule 1)

## Dependencies

None.

## References

-   [Apple — Export an iOS, tvOS, or watchOS app](https://help.apple.com/xcode/mac/current/en.lproj/dev23ea8b877.html)
-   [Apple — Distribution signing options](https://help.apple.com/xcode/mac/current/en.lproj/devff5ececf8.html)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/xcode/export-options.md --type knowledge`
Expected: `PASS: knowledge/xcode/export-options.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/xcode/export-options.md
git commit -m "feat: add export-options knowledge contract"
```

---

## Task 10: Native Skill — `skills/xcode/SKILL.md`

**Files:**
- Create: `skills/xcode/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: xcode
description: Route Xcode project-configuration implementation tasks to the correct Knowledge Contracts — build configurations, .xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archiving, and export. Use when configuring build settings, authoring an xcconfig file, editing a scheme, setting up code signing, adding a capability, or archiving/exporting an app in Xcode. v1 is Xcode GUI / project-file configuration only — no xcodebuild CLI, no CI signing automation (fastlane/match), no Swift Package Manager build configuration. Triggers on build configuration, Debug configuration, Release configuration, .xcconfig, Build Settings, Xcode scheme, Xcode target, Signing & Capabilities, automatic signing, manual signing, provisioning profile, signing certificate, entitlements, Xcode capability, Product > Archive, Organizer, ExportOptions, distribution method, Ad Hoc, Enterprise, App Store Connect distribution, IPA export.
id: skill.xcode.foundations
title: Xcode — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Xcode
routes: [knowledge.xcode.build-configurations, knowledge.xcode.xcconfig-files, knowledge.xcode.schemes-and-targets, knowledge.xcode.automatic-signing, knowledge.xcode.manual-signing-provisioning-profiles, knowledge.xcode.entitlements-capabilities, knowledge.xcode.archive-process, knowledge.xcode.export-options]
related: []
last_updated: 2026-08-01
---

# Xcode — Foundations Skill

## Purpose

Route Xcode project-configuration implementation tasks to the minimum
required Xcode Knowledge Contracts. v1 scope is Xcode GUI/project-file
configuration only — no `xcodebuild` CLI, no CI signing automation
(fastlane, `match`), no Swift Package Manager build configuration.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/xcode/.

-   Build configuration -> build-configurations.md, xcconfig-files.md, schemes-and-targets.md
-   Signing -> automatic-signing.md, manual-signing-provisioning-profiles.md, entitlements-capabilities.md
-   Archive & distribution -> archive-process.md, export-options.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/xcode/ — do not guess or fall back to general
knowledge. `xcodebuild` CLI usage, CI signing automation (fastlane,
`match`), and Swift Package Manager build configuration are deferred to
future scope, not yet built — report that explicitly rather than
answering from general knowledge (see docs/architecture/domain-map.md).
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/xcode/SKILL.md --type skill`
Expected: `PASS: skills/xcode/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/xcode/SKILL.md
git commit -m "feat: add xcode native skill"
```

---

## Task 11: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`networking` row (the row containing `skills/networking/SKILL.md`):

```markdown
| build configuration, Debug, Release, .xcconfig, Build Settings, scheme, target, Signing & Capabilities, automatic signing, manual signing, provisioning profile, certificate, entitlements, capability, Product > Archive, Organizer, ExportOptions, distribution method, Ad Hoc, Enterprise, App Store Connect distribution, IPA export | skills/xcode/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `10` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui, accessibility, uikit, sf-symbols, networking, xcode)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add xcode to skills index"
```

---

## Task 12: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `xcode` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| Xcode | xcode | Build, signing, archives | Build configuration, signing, and archive/export conventions |
```

Replace with:

```markdown
| Xcode | xcode | Xcode GUI/project-file v1: build configurations & .xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options. No xcodebuild CLI, no CI signing automation, no Swift Package Manager build configuration. | Xcode project-configuration implementation conventions (build settings, xcconfig, schemes, signing, entitlements, archive/export) |
```

- [ ] **Step 2: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt), `xcode` (Tier 1 — Xcode GUI/project-file v1: build configurations & xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; xcodebuild CLI, CI signing automation, and Swift Package Manager build configuration remain unbuilt).
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "xcode" docs/architecture/domain-map.md`
Expected: a number greater than 2 (the file already mentions "xcode" at
least twice before this task — the Tier 1 placeholder row and a mention
in the artifact-layout example — the updated row and Completed line push
the count higher)

- [ ] **Step 4: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope xcode v1 in domain-map"
```

---

## Task 13: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `networking` bullet,
immediately before the `Full routing tables:` line):

```markdown
- **`networking`** — Routes URLSession async/await networking implementation tasks (request construction, data fetching, Codable decoding, error handling, task cancellation, session configuration, App Transport Security, authenticated requests) to Networking Knowledge Contracts.
  Example: `"my JSON response isn't decoding, dates are failing"` → `codable-decoding.md`
  Example: `"how do I retry a request after a 401 without an infinite loop"` → `authenticated-requests.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`networking`** — Routes URLSession async/await networking implementation tasks (request construction, data fetching, Codable decoding, error handling, task cancellation, session configuration, App Transport Security, authenticated requests) to Networking Knowledge Contracts.
  Example: `"my JSON response isn't decoding, dates are failing"` → `codable-decoding.md`
  Example: `"how do I retry a request after a 401 without an infinite loop"` → `authenticated-requests.md`

- **`xcode`** — Routes Xcode project-configuration implementation tasks (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options) to Xcode Knowledge Contracts.
  Example: `"my archive won't export, wrong provisioning profile"` → `manual-signing-provisioning-profiles.md`
  Example: `"Product > Archive is greyed out"` → `archive-process.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a new What's New line**

Find this exact line (the first/topmost line in `## What's New`):

```markdown
- 2026-08-01 — Added `networking` Skill (URL request construction, async data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; async/await URLSession v1) — 8 Knowledge Contracts. Fills the "Authentication networking" gap authentication.md explicitly excludes, and replaces the prior placeholder scope in domain-map.md.
```

Replace with (adds a new topmost line before it):

```markdown
- 2026-08-01 — Added `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `networking` Skill (URL request construction, async data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; async/await URLSession v1) — 8 Knowledge Contracts. Fills the "Authentication networking" gap authentication.md explicitly excludes, and replaces the prior placeholder scope in domain-map.md.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "xcode" README.md`
Expected: a number greater than 0 (the new `xcode` Skills bullet and
What's New line are the first mentions of "xcode" in this file)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add xcode to README Skills + What's New"
```

---

## Task 14: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/xcode.md --type reference
python3 scripts/validate_artifact.py skills/xcode/SKILL.md --type skill
for f in knowledge/xcode/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
```
Expected: `PASS` for all 10 files.

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 4: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 13 prior tasks committed).

- [ ] **Step 5: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire `xcode` domain (all 10 new
files plus the 3 modified docs) to check cross-file consistency: every
`related:`/`depends_on:` KC id resolves to a real file, the Skill's
`routes:` list matches exactly the 8 KC ids, the Reference's "Used By"
list matches exactly the 8 KC files, layer order (References → Knowledge
→ Skills) is respected. The review must specifically check for v1-scope
violations that a per-task review could miss (this class of bug slipped
through per-task review in prior domain builds and was only caught by
the final holistic pass):

-   No content anywhere describing `xcodebuild` CLI flags/invocation
-   No content anywhere describing CI signing automation (fastlane,
    `match`, App Store Connect API keys for CI)
-   No content anywhere describing Swift Package Manager build
    configuration
-   No KC restates `authentication`'s Sign in with Apple UX/terminology
    content
-   Every cited Apple/Apple Developer URL is live (spot-check a sample
    with `curl -s -o /dev/null -w "%{http_code}"`)

Report findings; fix any issues found and re-commit before considering
the domain complete.

---

## Self-Review Notes

-   **Spec coverage:** All 8 topics from the design spec's Decision 3
    table have a task (Tasks 2–9). Decision 5 file layout is covered by
    Tasks 1, 2–9, 10. Decision 6 routing clusters are reflected in
    Task 10's Routing section. Decision 7 domain-map.md updates are
    covered by Task 12 (no new Cross-Domain Notes entry, per the spec's
    Decision 4/7 finding of clean boundaries with no overlap).
-   **Placeholder scan:** No TBD/TODO; every Rule, Example, and
    Reference URL is concrete and was live-verified via `curl` during
    planning (see Task 14 Step 5 for the re-check to run post-hoc).
-   **Type/id consistency:** Every KC `id` (`knowledge.xcode.<slug>`)
    referenced in Task 10's `routes:` list and Task 1's "Used By" list
    matches the `id` defined in that KC's own Task 2–9 Metadata block.
    Every `related:` cross-reference (e.g.
    `knowledge.xcode.entitlements-capabilities` listed in
    `automatic-signing`'s `related:`) points at an id defined in this
    same plan.
