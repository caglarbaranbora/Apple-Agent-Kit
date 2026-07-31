# App Store Review Guidelines Domain — Design

Status: Draft (pending user review)
Version: 0.1.0

## Purpose

Add `app-store-review-guidelines` as the second Tier 1 domain built after
`human-interface-guidelines` (Foundations subset, shipped in PR #5).
Delivers agent-actionable rules for the App Store submission requirements
that cause the most real-world review rejections — closing the gap between
"code that works" and "code that ships."

## Context

Apple's App Review Guidelines (`developer.apple.com/app-store/review/guidelines`)
cover five top-level sections: Safety, Performance, Business, Design,
Legal — each with many numbered sub-rules. Design (4.0) is already owned by
`human-interface-guidelines`; most of Legal and Safety are non-technical
(content policy, not implementation) and out of scope for an agent that
writes code. This domain focuses on the subset that is both (a) a frequent
real-world rejection cause and (b) actionable from application code or
App Store Connect metadata.

## Decisions

### 1. Scope: 7 guideline areas, most-frequently-violated subset, v1

Selected guideline sections (confirmed with user during brainstorming):

- **2.1** App Completeness
- **2.3** Accurate Metadata
- **3.1.1** In-App Purchase
- **4.2** Minimum Functionality
- **4.3** Spam / Duplicate Apps
- **5.1.1** Data Collection and Storage
- **5.1.2** Data Use and Sharing

Excluded from v1 (future pass, not dropped): Safety section (age ratings,
UGC moderation — non-technical), most of Legal (export compliance,
licensing — non-technical), Design 4.0 (owned by
`human-interface-guidelines`), Guideline 4.8 Sign in with Apple (overlaps
`authentication`/`authenticationservices` — boundary already flagged as
unresolved in `domain-map.md` Cross-Domain Notes, not reopened here).

### 2. Knowledge Contract breakdown: atomic, one rule per file

Mirrors `human-interface-guidelines`'s resolution (atomic KCs, not one file
per guideline number) — a single guideline number often bundles multiple
independent implementation rules, which would violate `domain-map.md`'s
"Knowledge Contracts remain atomic" rule if merged.

**Final v1 scope: 12 Knowledge Contracts**, all under
`knowledge/app-store-review-guidelines/`:

1. `app-completeness` (2.1) — no crashes/bugs/placeholder content/broken links
2. `demo-account` (2.1) — test credentials required for login-gated review
3. `screenshots-accuracy` (2.3) — screenshots must reflect actual app UI
4. `description-accuracy` (2.3) — description/keywords must not mislead
5. `digital-goods-iap` (3.1.1) — digital content/features must use IAP
6. `external-payment-links` (3.1.1) — no external purchase links for digital goods
7. `restore-purchases` (3.1.1) — non-consumable/subscription IAP needs a restore mechanism
8. `minimum-functionality` (4.2) — app must offer lasting value beyond a website wrapper
9. `spam-duplicate-apps` (4.3) — no templated/duplicate submissions
10. `permission-usage-strings` (5.1.1) — Info.plist NSUsageDescription strings must be specific and accurate
11. `privacy-manifest` (5.1.1) — PrivacyInfo.xcprivacy required for reviewable submission
12. `privacy-nutrition-label` (5.1.1 + 5.1.2) — App Store privacy label must match actual data collection and sharing

`privacy-nutrition-label` intentionally merges 5.1.1 and 5.1.2: both
guideline numbers describe the same actionable rule from an implementation
angle — declared data practices must match actual behavior — so splitting
them would create two files answering the same question.

### 3. Cross-domain overlap: `privacy-manifest` and `privacy-nutrition-label`

Both overlap the future Tier 2 `privacy` domain (`domain-map.md` Owns:
"Privacy manifest and data-use disclosure requirements"). Resolved with the
same angle-split pattern already established for
`human-interface-guidelines`'s `privacy.md` vs. the future `privacy`
domain: this domain's angle is **review consequence** (submission gets
rejected if the manifest/label is missing or inaccurate), the future
`privacy` domain's angle is **correct implementation** (how to write the
manifest and disclosures correctly). One new Cross-Domain Notes entry
records this — boundary resolved when `privacy` is actually built, per the
existing pattern for the three `human-interface-guidelines` overlaps.

### 4. File layout: mirrors `human-interface-guidelines`, no new pattern

- **Reference:** one file,
  `references/apple/app-store-review-guidelines.md` — same shape as
  `references/apple/human-interface-guidelines.md` (Source, Purpose,
  Primary Topics, Used By listing all 12 knowledge contracts). Source URL:
  `https://developer.apple.com/app-store/review/guidelines/`.
- **Knowledge:** 12 files under `knowledge/app-store-review-guidelines/`,
  one per topic above, existing knowledge-contract format (`## Metadata`
  fenced YAML block — id/type/title/version/status/owner/summary/domain/
  tags/references/depends_on/related/updated — plus `## Intent`,
  `## Rules`, `## Compliant Example`, `## Non-Compliant Example`; 150-line
  cap). `domain: App Store Review Guidelines` in each.
- **Skill:** one native skill,
  `skills/app-store-review-guidelines/SKILL.md`, hardened format
  (frontmatter `name`/`description`/`id:
  skill.app-store-review-guidelines.submission`/`title`/`version`/`status`/
  `artifact_type`/`domain`/`routes:` [12 ids]/`related:` []/
  `last_updated`; body `## Purpose`, `## Routing`, `## Stop Conditions`;
  80-line cap). No `related:` domain exists yet for this one (no wording or
  visual-design overlap the way `authentication`/`human-interface-
  guidelines` cross-reference `style-guide`) — left empty.

No per-topic reference files, no directory nesting beyond the established
`knowledge/<domain>/<slug>.md` and `skills/<domain>/SKILL.md` conventions.

### 5. Routing: keyword-clustered, deterministic, load-minimum

Mirrors `skills/human-interface-guidelines/SKILL.md`'s `## Routing`
section: frontmatter `routes:` is the full flat set (all 12), body groups
into task-keyword clusters so the agent loads only what a specific question
needs.

Proposed clusters:
- Submission completeness → `app-completeness.md`, `demo-account.md`
- Metadata accuracy → `screenshots-accuracy.md`, `description-accuracy.md`
- In-app purchase → `digital-goods-iap.md`, `external-payment-links.md`, `restore-purchases.md`
- App value / originality → `minimum-functionality.md`, `spam-duplicate-apps.md`
- Privacy compliance → `permission-usage-strings.md`, `privacy-manifest.md`, `privacy-nutrition-label.md`

### 6. `domain-map.md` updates (part of this project, not a separate pass)

- `app-store-review-guidelines` row's **Initial Scope** cell updated from
  the current broad text to: "2.1 App Completeness, 2.3 Accurate Metadata,
  3.1.1 In-App Purchase, 4.2 Minimum Functionality, 4.3 Spam/Duplicate,
  5.1.1/5.1.2 Privacy (data collection & sharing). Safety, most of Legal,
  and Design 4.0 (owned by `human-interface-guidelines`) out of scope —
  see Cross-Domain Notes."
- One new Cross-Domain Notes entry (Decision 3 above).
- **Build Order** section's "Completed" line gets
  `app-store-review-guidelines` (critical-subset v1) appended once this
  ships.

## Consequences

- Third full domain under the hardened native-skill pipeline (after
  `style-guide`/`authentication` and `human-interface-guidelines`).
- Safety, most of Legal, Guideline 4.8 (Sign in with Apple), and Design 4.0
  remain explicitly unbuilt. Not silently dropped: `domain-map.md`'s
  Initial Scope cell and this spec both record the boundary.
- Adds 1 new Cross-Domain Notes entry that must be checked when `privacy`
  is eventually built.
- No changes to `scripts/validate_artifact.py`, `docs/specifications/*`, or
  any hardening-project file — this project only produces new
  reference/knowledge/skill content on top of the already-hardened schema.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py references/apple/app-store-review-guidelines.md --type reference` — `PASS`.
- `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/<slug>.md --type knowledge` for all 12 files — all `PASS`.
- `python3 scripts/validate_artifact.py skills/app-store-review-guidelines/SKILL.md --type skill` — `PASS`.
- `python3 -m unittest tests/test_validate_artifact.py -v` — full pass (no regressions).
- `claude plugin validate .` — confirms the new `SKILL.md` is discovered.
- `skills/index.md` Discovery Rules table gets a new row for
  `app-store-review-guidelines`.
- `README.md` `## Skills` and `## What's New` sections updated per
  `CLAUDE.md`'s standing rule.
- Manual invocation check in a fresh session (same caveat as prior
  domains — the harness enumerates skills at session start, so this can't
  be verified same-session).

## Out of Scope

- Safety section, most of Legal section, Design 4.0 (owned by
  `human-interface-guidelines`), Guideline 4.8 Sign in with Apple — future
  passes, already tracked in `domain-map.md`.
- Resolving the `privacy-manifest`/`privacy-nutrition-label` overlap with
  the future `privacy` domain — deferred until `privacy` is built.
- Any change to already-hardened schema/validator/spec files.
