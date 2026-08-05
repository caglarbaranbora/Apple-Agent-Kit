# App Tracking Transparency Domain — Design Spec

Status: Draft
Version: 0.1.0
Date: 2026-08-05

## Purpose

Build the `app-tracking-transparency` Tier 1 domain: the ATT authorization
prompt and IDFA access implementation via Apple's AppTrackingTransparency
and AdSupport frameworks. This is the 12th and final Tier 1 domain — once
this ships, Tier 1 is fully complete (see `docs/architecture/domain-map.md`).

## Scope

### Platform

iOS/iPadOS only, matching every prior Tier 1 domain. tvOS-specific ATT
behavior is deferred to future scope.

### Included (v1)

- `ATTrackingManager.requestTrackingAuthorization(completionHandler:)`:
  one-time-only semantics (the system remembers the user's decision and
  never re-prompts unless the app is uninstalled and reinstalled), the
  `UIApplicationState.active` requirement for the prompt to display,
  behavior when another permission prompt is already pending, why
  concurrent calls aren't preserved, why app extensions never prompt, and
  checking `trackingAuthorizationStatus == .notDetermined` before calling
  again
- `ATTrackingManagerAuthorizationStatus`
  (`.notDetermined`/`.restricted`/`.denied`/`.authorized`) and the correct
  agent behavior to gate on each value
- `ASIdentifierManager.advertisingIdentifier` (IDFA) access: the
  zeroed-UUID (`00000000-0000-0000-0000-000000000000`) fallback behavior
  when not authorized, and the requirement to read it live rather than
  cache/store it, since authorization can change in Settings at any time
  without an app relaunch
- `NSUserTrackingUsageDescription` Info.plist requirement and wording
  rules (specific, explains the actual tracking use — the same
  crash-on-missing-key pattern as `NSFaceIDUsageDescription` in
  `local-authentication`)

### Excluded (v1, deferred)

- tvOS-specific ATT behavior
- SKAdNetwork (conversion values, postbacks) — a separate advertising
  attribution framework, not part of AppTrackingTransparency/AdSupport;
  future domain if warranted
- AdServices attribution API — same reasoning, separate framework
- Custom pre-permission screen design, timing-of-request UX judgment, and
  purpose-string design conventions — owned by `human-interface-guidelines`
  (`privacy.md`), see Cross-Domain Boundary below
- App Store Connect "App Privacy" nutrition-label disclosure and tracking-use
  marking — already owned by `app-store-review-guidelines`
  (`privacy-nutrition-label.md`); this domain covers the runtime API only
- General Info.plist permission-string conventions not specific to ATT —
  owned by `app-store-review-guidelines` (`permission-usage-strings.md`);
  this domain owns `NSUserTrackingUsageDescription` wording specifically,
  same non-overlapping precedent as `local-authentication`'s
  `NSFaceIDUsageDescription` KC

## Cross-Domain Boundary: `app-tracking-transparency` vs. `human-interface-guidelines`

Angle-split, not a clean handoff — `knowledge.human-interface-guidelines.privacy`
already has content that names this exact topic. Its Included list has
"Tracking-permission-alert integrity rules," and its Rules 3–4 cover
custom pre-permission screens preceding the system tracking alert (one
button, must open the system alert, no deceptive/dismissable screens).

Split: `human-interface-guidelines` keeps the design/UX layer — whether
and how to show a custom pre-permission screen, its button/copy
constraints, and the anti-deception rule. `app-tracking-transparency` owns
the API layer — the actual `requestTrackingAuthorization` call mechanics,
the status enum, and IDFA access. Neither domain restates the other's
Rules; `app-tracking-transparency`'s `authorization-request.md` KC
cross-references `knowledge.human-interface-guidelines.privacy` via
`related:`, following the precedent already set by `sf-symbols` KCs
cross-referencing `human-interface-guidelines` via `related:` across
domain boundaries.

Two secondary boundaries, both clean handoffs (no content overlap, no new
Rules on the other side):

- **vs. `app-store-review-guidelines` (`privacy-nutrition-label.md`)** —
  that KC's Rule 3 already states tracking-use marking "additionally
  requires App Tracking Transparency permission" without describing the
  API; this domain is the implementation the nutrition-label KC points at.
- **vs. `app-store-review-guidelines` (`permission-usage-strings.md`)** —
  that KC's own Excluded/Included scope is generic Info.plist strings
  using `NSCameraUsageDescription`/`NSLocationWhenInUseUsageDescription`
  as its examples; it never names `NSUserTrackingUsageDescription`. Same
  non-overlap precedent as `local-authentication`'s
  `reason-strings-and-info-plist.md`.

All three will be recorded as new bullets in `docs/architecture/domain-map.md`'s
Cross-Domain Notes.

## Knowledge Contracts (3)

All under `knowledge/app-tracking-transparency/`:

1. **`authorization-request.md`** — `requestTrackingAuthorization`
   mechanics: one-time-only semantics, the `.active`-state requirement,
   pending-prompt/concurrent-call/app-extension edge cases, checking
   `.notDetermined` before calling again, dispatching the completion
   handler's UI work back to the main queue. Cross-references
   `knowledge.human-interface-guidelines.privacy` via `related:` for the
   UX/timing layer this KC does not cover.
2. **`status-and-idfa-access.md`** — the `ATTrackingManagerAuthorizationStatus`
   enum and required gating behavior per value; `advertisingIdentifier`'s
   zeroed-UUID fallback and the cases that trigger it; the
   don't-cache-status-or-IDFA rule, since the user can change authorization
   in Settings at any time without relaunching the app.
3. **`usage-string-and-info-plist.md`** — `NSUserTrackingUsageDescription`
   requirement (missing key crashes the app the same way missing
   `NSFaceIDUsageDescription` does) and wording rules (specific, explains
   the actual tracking use, not a generic placeholder).

## Reference

`references/apple/app-tracking-transparency.md` — index into Apple's
AppTrackingTransparency
(https://developer.apple.com/documentation/apptrackingtransparency) and
AdSupport (https://developer.apple.com/documentation/adsupport)
framework documentation, scoped to the topics above, with the same
exclusion note as this spec's Excluded section.

## Skill

`skills/app-tracking-transparency/SKILL.md` — one Skill routing all 3 KCs,
following the native Skill format used by every other domain skill (real
YAML frontmatter, `## Purpose`/`## Routing`/`## Stop Conditions`).

Trigger keywords: `ATTrackingManager`, `requestTrackingAuthorization`,
`trackingAuthorizationStatus`, `ATTrackingManagerAuthorizationStatus`,
`ASIdentifierManager`, `advertisingIdentifier`, `IDFA`,
`NSUserTrackingUsageDescription`, `App Tracking Transparency`, `tracking
authorization`.

## Documentation Updates

Per `CLAUDE.md`'s "Updating README.md" rule, same commit as the domain:

- `README.md` — new `app-tracking-transparency` Skills bullet (after
  `local-authentication`), new top-of-list "What's New" line (existing
  3-item cap — oldest of the current 3 rolls off into CHANGELOG.md only).
- `CHANGELOG.md` — new entry under `## [Unreleased]`.
- `docs/architecture/domain-map.md` — Tier 1 table row (line 35) Initial
  Scope/Owns cells rewritten from the current placeholder text ("ATT
  prompt, IDFA access") to the detailed v1 scope wording used by every
  other completed Tier 1 row, three new Cross-Domain Notes bullets (see
  above), "Completed:" line on line 19 gets the
  `app-tracking-transparency` clause appended — this closes out all 12
  Tier 1 domains.
- `skills/index.md` — new Discovery Rules row.

## Validation

Same as every prior domain: `scripts/validate_artifact.py` against each
new Knowledge Contract, the Skill, and the Reference; full unit test
suite; `claude plugin validate .`; local CI-step simulation before push.

## Out of Scope for This Spec

- SKAdNetwork and AdServices attribution frameworks.
- Any tvOS-specific ATT behavior.
- The final Tier 1 holistic review and v1 release — happens after this
  domain ships and merges, per the user's stated end goal.
