# Local Authentication Domain — Design Spec

Status: Draft
Version: 0.1.0
Date: 2026-08-05

## Purpose

Build the `local-authentication` Tier 1 domain: Face ID, Touch ID, and
device-passcode authentication implementation via Apple's
LocalAuthentication framework, including the Keychain-biometric binding
seam (`SecAccessControl`). This is the 11th of 12 Tier 1 domains and the
second-to-last — only `app-tracking-transparency` remains after this to
close out Tier 1 (see `docs/architecture/domain-map.md`).

## Scope

### Platform

iOS/iPadOS only, matching every prior Tier 1 domain (`swiftui`, `uikit`,
`accessibility`, `sf-symbols`, `networking`, `xcode`). macOS/watchOS-specific
LocalAuthentication behavior (e.g. Touch ID on Mac, no Face ID) is deferred
to future scope.

### Included (v1)

- `LAContext` creation, `canEvaluatePolicy` availability checks
- `LABiometryType` detection (Face ID vs. Touch ID vs. none)
- Policy evaluation: `evaluatePolicy` with
  `.deviceOwnerAuthenticationWithBiometrics` (biometrics-only, no passcode
  fallback) vs. `.deviceOwnerAuthentication` (biometrics-or-passcode)
- `localizedReason` wording rules and the `NSFaceIDUsageDescription`
  Info.plist requirement
- `LAError` codes and the required handling/fallback behavior per code
  (`userCancel`, `userFallback`, `biometryNotAvailable`,
  `biometryNotEnrolled`, `biometryLockout`, `authenticationFailed`, etc.)
- `LAContext` lifecycle: reuse rules, `invalidate()`,
  `evaluatedPolicyDomainState`, and why a context must not be persisted
  across app launches
- Keychain-biometric binding: `SecAccessControl` creation with
  `kSecAttrAccessControl`, the `biometryCurrentSet` vs. `biometryAny`
  distinction, and passing an `LAContext` into a Keychain query via
  `kSecUseAuthenticationContext`
- Fallback UX: when and how to offer an "Enter Passcode" fallback button,
  UX conventions for the fallback path

### Excluded (v1, deferred)

- macOS/watchOS-specific LocalAuthentication behavior
- General Keychain storage (`SecItemAdd`/`SecItemCopyMatching`/
  `SecItemUpdate` for non-biometric-bound items) — owned by the future
  `security` domain (Tier 2, unbuilt); this domain owns only the
  biometric-binding seam (`SecAccessControl` construction), not general
  Keychain CRUD
- Passkeys, Sign in with Apple — already excluded by
  `knowledge.authentication.authentication`'s own Excluded list
- Sign-in UX, entry points, session management — owned by `authentication`
- Custom biometric-prompt visual design guidance — if a HIG-level design
  question arises (e.g. "should Face ID prompt on screen load or on user
  action"), that is `human-interface-guidelines` territory; this domain
  owns API implementation only, same angle-split pattern as
  `accessibility` vs. `human-interface-guidelines`

## Cross-Domain Boundary: `local-authentication` vs. `authentication`

Clean handoff, not an overlap requiring angle-split — same pattern as the
already-resolved `networking` vs. `authentication` boundary.

`knowledge.authentication.authentication`'s Excluded list already omits
biometrics entirely (its exclusions are: StoreKit authentication, passkeys
implementation, Sign in with Apple implementation, authentication
networking, backend architecture). `authentication` owns sign-in
terminology, entry points, and user-facing flow decisions;
`local-authentication` owns the LocalAuthentication framework API surface
a developer reaches for once the decision to use biometrics has already
been made. No content is duplicated between the two domains. This will be
recorded as a new bullet in `docs/architecture/domain-map.md`'s
Cross-Domain Notes, following the exact wording pattern used for the
`networking`/`authentication` entry.

## Knowledge Contracts (7)

All under `knowledge/local-authentication/`:

1. **`availability-and-biometry-type.md`** — `canEvaluatePolicy` to check
   availability before evaluating; `LABiometryType` (`.faceID`, `.touchID`,
   `.none`) to detect which biometry is present, for icon/copy selection.
2. **`policy-evaluation.md`** — the two v1 policies
   (`.deviceOwnerAuthenticationWithBiometrics` vs.
   `.deviceOwnerAuthentication`) and when each applies; `evaluatePolicy`
   async usage.
3. **`reason-strings-and-info-plist.md`** — `localizedReason` copy rules
   (task-specific, no restating "authenticate"); `NSFaceIDUsageDescription`
   is required or Face ID calls crash at runtime.
4. **`error-handling.md`** — the `LAError` code table and the required
   agent behavior per code (e.g. `biometryNotEnrolled` must prompt to set
   up Face ID/Touch ID in Settings, not silently fail).
5. **`context-lifecycle.md`** — one `LAContext` per authentication attempt;
   `invalidate()` after use; `evaluatedPolicyDomainState` for detecting
   enrollment changes; contexts must not be persisted across launches.
6. **`keychain-biometric-binding.md`** — `SecAccessControl` construction
   with `kSecAttrAccessControl`; `biometryCurrentSet` (invalidated on
   re-enrollment) vs. `biometryAny` (survives re-enrollment) tradeoff;
   passing the evaluated `LAContext` into a Keychain query via
   `kSecUseAuthenticationContext`.
7. **`fallback-ux-and-passcode.md`** — when to offer "Enter Passcode"
   (`.deviceOwnerAuthentication`) as a fallback vs. biometrics-only
   (`.deviceOwnerAuthenticationWithBiometrics`); `LAContext
   .localizedFallbackTitle`.

## Reference

`references/apple/local-authentication.md` — index into Apple's
LocalAuthentication framework documentation
(https://developer.apple.com/documentation/localauthentication), scoped
to the topics above, with the same exclusion note as this spec's Excluded
section.

## Skill

`skills/local-authentication/SKILL.md` — one Skill routing all 7 KCs,
following the native Skill format used by every other domain skill (real
YAML frontmatter, `## Purpose`/`## Routing`/`## Stop Conditions`).

Trigger keywords, pre-qualified to avoid the collision risk flagged during
the `xcode` build (bare words like "target" or "scheme" were too broad):
`Face ID`, `Touch ID`, `LAContext`, `LABiometryType`, `biometric
authentication`, `canEvaluatePolicy`, `evaluatePolicy`,
`deviceOwnerAuthentication`, `LAError`, `biometryNotEnrolled`,
`SecAccessControl`, `biometric Keychain`, `Enter Passcode fallback`.

## Documentation Updates

Per `CLAUDE.md`'s "Updating README.md" rule, same commit as the domain:

- `README.md` — new `local-authentication` Skills bullet (after `xcode`),
  new top-of-list "What's New" line (existing 3-item cap keeps the list
  from growing unbounded — oldest of the current 3 rolls off into
  CHANGELOG.md only, as already established by the `xcode` entry landing).
- `CHANGELOG.md` — new entry under `## [Unreleased]`.
- `docs/architecture/domain-map.md` — Tier 1 table row (line 34) Initial
  Scope/Owns cells rewritten from the current placeholder text ("Face ID,
  Touch ID, biometric/passcode auth") to the detailed v1 scope wording
  used by every other completed Tier 1 row, new Cross-Domain Notes bullet
  (see above), "Completed:" line on line 19 gets the `local-authentication`
  clause appended.
- `skills/index.md` — new Discovery Rules row.

## Validation

Same as every prior domain: `scripts/validate_artifact.py` against each
new Knowledge Contract, the Skill, and the Reference; full unit test
suite; `claude plugin validate .`; local CI-step simulation before push.

## Out of Scope for This Spec

- `app-tracking-transparency` (the final remaining Tier 1 domain) — separate
  spec, after this domain ships.
- Any macOS/watchOS LocalAuthentication behavior.
- General Keychain domain build (`security`, Tier 2) — this spec's
  `keychain-biometric-binding.md` KC covers only the biometric-binding
  seam, not a full Keychain domain.
