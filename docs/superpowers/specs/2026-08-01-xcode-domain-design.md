# Xcode Domain Design

Status: Draft
Version: 0.1.0

## Purpose

Replace the placeholder `xcode` entry in `docs/architecture/domain-map.md`
(Initial Scope: "Build, signing, archives", Owns: "Build configuration,
signing, and archive/export conventions") with a real Tier 1 domain
covering Xcode project configuration for iOS/iPadOS apps — build
configurations and `.xcconfig` files, schemes/targets, code signing
(automatic and manual), entitlements/capabilities, and the
archive-to-export workflow.

This is the ninth domain built this session, and the first that is not
Swift API-surface knowledge — it covers Xcode project-file and GUI
conventions (`.pbxproj`-level settings, Organizer workflow, signing UI)
rather than code written inside a `.swift` file.

## Context

No prior domain touches build configuration, signing, or archiving.
A grep across `knowledge/app-store-review-guidelines/*.md` and
`knowledge/authentication/*.md` for archive/provisioning/code
signing/export-options/xcconfig/build-setting terms returned no hits —
no existing content to deduplicate against.

## Decisions

### Decision 1: v1 surface — Xcode GUI / project-file config, no CLI/CI

v1 covers what an agent edits directly in Xcode or in project files:
Build Settings, `.xcconfig`, schemes, the Signing & Capabilities tab,
entitlements files, and the Organizer archive/export flow.
`xcodebuild` command-line invocation, CI signing automation (fastlane,
`match`), and Swift Package Manager build configuration are out of v1 —
each is a distinct CLI/DevOps-tooling concern, not project configuration,
and would break this domain's atomicity the same way completion-handler
APIs were kept out of `networking` v1.

### Decision 2: Signing scope — automatic and manual both included

Both Xcode-managed (automatic) signing and manual signing with explicit
certificates/provisioning profiles are in v1. Real projects hit both:
automatic for day-to-day development, manual for ad hoc/enterprise
distribution where a specific profile must be selected. Narrowing to
automatic-only would leave the domain unable to answer the
"why did my archive/export fail to find a matching profile" question,
which is one of the highest-friction Xcode problems for agents to
reason about without this Knowledge Contract.

### Decision 3: 8-topic atomic breakdown

| # | Slug | Covers |
|---|---|---|
| 1 | `build-configurations` | Debug/Release build configurations, adding custom configurations, Build Settings basics (target-level vs project-level, per-configuration overrides) |
| 2 | `xcconfig-files` | Authoring `.xcconfig` files, attaching them to a configuration, `#include`-based inheritance, xcconfig vs Build Settings UI precedence |
| 3 | `schemes-and-targets` | Scheme structure (Run/Test/Archive/Analyze actions each map to a build configuration), shared vs user schemes, basic multi-target setup |
| 4 | `automatic-signing` | Xcode-managed signing: Team selection, automatically-generated certificates/profiles, when Xcode re-provisions |
| 5 | `manual-signing-provisioning-profiles` | Manual signing: certificate types (Development/Distribution), provisioning profile types (Development/Ad Hoc/Enterprise/App Store), matching a profile to a build |
| 6 | `entitlements-capabilities` | The entitlements file, adding a capability via Signing & Capabilities, how capabilities constrain which provisioning profile is valid |
| 7 | `archive-process` | Product → Archive, the Organizer window, archive validation before export |
| 8 | `export-options` | `ExportOptions.plist` keys, distribution-method selection (App Store Connect/Ad Hoc/Enterprise/Development), exporting an IPA from the Organizer |

Topics 4–6 are sequenced so `entitlements-capabilities` (6) can
cross-reference both signing topics (4, 5) without a forward reference,
mirroring how `networking`'s `authenticated-requests` (8) was placed
after its prerequisite topics.

### Decision 4: Cross-domain resolution

- **`xcode` ↔ `app-store-review-guidelines`**: no overlap. ASRG's 2.1
  App Completeness and 5.1.1/5.1.2 Privacy are submission-content
  correctness concerns (does the build run, is data-use disclosed
  accurately); `xcode` owns getting a correctly-signed archive built in
  the first place. No shared terms found in Decision-context grep.
- **`xcode` ↔ `authentication`**: no overlap. Entitlements for
  Sign in with Apple (`com.apple.developer.applesignin`) are a capability
  *name* `entitlements-capabilities` can reference, but the sign-in UX/flow
  itself stays entirely in `authentication` — same clean-handoff pattern
  as `networking` ↔ `authentication`.
- **`xcode` ↔ `networking`**: no overlap. ATS (`networking`'s
  `app-transport-security.md`) is an `Info.plist` key, not a signing or
  build-configuration concern.

### Decision 5: File layout

```
references/apple/xcode.md
knowledge/xcode/build-configurations.md
knowledge/xcode/xcconfig-files.md
knowledge/xcode/schemes-and-targets.md
knowledge/xcode/automatic-signing.md
knowledge/xcode/manual-signing-provisioning-profiles.md
knowledge/xcode/entitlements-capabilities.md
knowledge/xcode/archive-process.md
knowledge/xcode/export-options.md
skills/xcode/SKILL.md
```

### Decision 6: Skill routing clusters

`skills/xcode/SKILL.md` routes across 3 clusters:
- **Build configuration**: `build-configurations`, `xcconfig-files`, `schemes-and-targets`
- **Signing**: `automatic-signing`, `manual-signing-provisioning-profiles`, `entitlements-capabilities`
- **Archive & distribution**: `archive-process`, `export-options`

No `related:` cross-links to other Skills — Decision 4 found no
implementation-level overlap requiring one (unlike `networking`'s link
to `skill.authentication.login`).

### Decision 7: `domain-map.md` update

- `xcode` row: Initial Scope replaced with the real v1 scope from
  Decision 1/3; Owns updated to reflect the 8-topic breakdown
- Build Order "Completed" line: append `xcode` entry with its scope and
  explicitly-deferred items (`xcodebuild` CLI, CI signing automation,
  Swift Package Manager build configuration)
- No new Cross-Domain Notes entries needed — Decision 4 found clean
  boundaries, not overlaps requiring documentation

## Consequences

- Agents asking "why won't my archive export" or "which provisioning
  profile do I need" get routed to `xcode`, with explicit
  automatic-vs-manual signing coverage instead of only the common-case
  automatic path.
- `xcodebuild`/CI signing remains a documented gap (Build Order,
  Skill's Stop Conditions) rather than silently missing — same pattern
  used for `networking`'s deferred completion-handler APIs.
- `README.md` gets a new `## Skills` bullet and a new `## What's New`
  top line, per `CLAUDE.md`'s same-PR requirement.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py <path> --type knowledge` for
  each of the 8 KCs and the Reference (`--type reference`)
- `python3 scripts/validate_artifact.py skills/xcode/SKILL.md --type skill`
- `python3 -m unittest tests/test_validate_artifact.py -v`
- Every cited Apple Developer URL live-verified (`curl`, not WebFetch's
  summarized output) to resolve
- Final holistic review pass across all 8 KCs for v1-scope consistency
  (no `xcodebuild` CLI content, no CI/fastlane content, no SPM build
  content, no duplicated ASRG/authentication content)

## Out of Scope

- `xcodebuild` command-line build/archive/export — future work, unassigned owner
- CI signing automation (fastlane, `match`, App Store Connect API keys for CI) — future work, unassigned owner
- Swift Package Manager build configuration — future work, unassigned owner
- macOS-specific signing/notarization — this domain is iOS/iPadOS-scoped, consistent with every prior domain this session
- Xcode Cloud — future work, unassigned owner
