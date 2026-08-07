# Build Configurations

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.build-configurations
artifact_type: knowledge
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
last_updated: 2026-08-01
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
