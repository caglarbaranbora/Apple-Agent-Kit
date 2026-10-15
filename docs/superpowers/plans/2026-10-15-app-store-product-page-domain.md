# App Store Product Page Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a new `app-store-product-page` domain (Reference, 9 Knowledge Contracts, 1 Skill, ADR-0002) that encodes Apple's App Store asset specs and asset best practices, and close the matching App Review gaps (2.3.3 majority rule, 2.3.8, 2.3.10) inside `app-store-review-guidelines`.

**Architecture:** Angle split, same pattern as `privacy` ↔ `app-store-review-guidelines`: `app-store-review-guidelines` owns *what gets rejected* (MUST, guideline-backed), `app-store-product-page` owns *asset specs and how to make assets effective* (spec MUSTs + checkable SHOULDs). `references/apple/app-store-review-guidelines.md` is at its 98-line cap, so every new App Review URL (2.3.3 help page, `#2.3.4`, `#2.3.7`, `#2.3.8`, `#2.3.10`) is indexed in the **new** Reference — legal because indexing is many-to-many and matched by URL (`scripts/validate_repo.py::check_used_by_is_complete`).

**Tech Stack:** Markdown artifacts with YAML metadata; Python 3 validators (`scripts/validate_artifact.py`, `scripts/validate_repo.py`, `scripts/check_links.py`, `scripts/check_transitions.py`); `unittest`.

**Source of every fact below:** `docs/research/2026-10-app-store-asset-best-practices.md` (live-fetched 2026-10-15). Decisions: the 14-question grilling session of 2026-10-15, summarised in "Decisions" below.

---

## Decisions (locked 2026-10-15)

| # | Decision |
|---|---|
| 1 | New domain + normative fixes in ASRG |
| 2 | Name `app-store-product-page`; v1 visual assets only; text fields (subtitle, promotional text, keywords) Deferred |
| 3 | iOS/iPadOS + iPhone Duo; Mac/TV/Vision/Watch Excluded (pointer) |
| 4 | Required sizes + limits + scaling rule + pointer; no full device table |
| 5 | Duo April 2027: MUST per ASC spec page (iOS 27.1 SDK+); SHOULD for all submissions per What's New; conflict noted |
| 6 | Duo preview: encode accepted 886×1920 / 1920×886; do not encode the "19.5:9" device-resolution label |
| 7 | Asset-page "Don't" items → MUST NOT, Intent says asset guidance, not a rejection reason |
| 8 | Craft: only checkable items as SHOULD; subjective ones Excluded |
| 9 | ASRG: amend `screenshots-accuracy`; new `metadata-age-rating` (2.3.8), `other-platform-references` (2.3.10) |
| 10 | New App Review URLs indexed in the product-page Reference; ASRG Reference stays at 98 lines |
| 11 | `app-store-submission` workflow: no new step; pointer in Excluded |
| 12 | 9 KCs (4 spec, 1 content, 4 craft); content KC extends, never restates, 2.3.8/2.3.10 (via `related`) |
| 13 | One feature PR (commit 1 domain, commit 2 ASRG) + separate `chore/release-2.5.0` PR |
| 14 | Apple-side link issues: record only; post-redirect URLs only |

Choices made while planning (veto at plan review):
- **Tier 1** placement in `domain-map.md` — every App Store app ships screenshots ("needed by nearly every iOS app").
- **ADR-0002** is written: decision 10 (cross-domain indexing) and decision 7 pass `adr-spec.md`'s "surprising without context" test.
- Product page optimization and custom product pages → **Deferred** alongside text fields.
- `npx/package.json` `version` is bumped in the release PR only (six-file version rule). No `npm publish`.

## Global rules for the executor

- Work in a worktree: `.worktrees/app-store-product-page`, branch `feature/app-store-product-page`.
- **Quote verification:** before writing any KC, fetch its cited URLs live (`curl -sL <url> | python3 -c "import sys,html,re;print(re.sub(r'<[^>]+>',' ',html.unescape(sys.stdin.read())))"`) and confirm every quoted string appears verbatim. If Apple's wording differs, use Apple's wording and adjust the rule to match the source — never keep a quote the page doesn't contain. If a number differs from this plan, the live page wins; record the difference in the commit message.
- Every KC: ≤150 lines. Reference: ≤98 lines. Skill: ≤80 lines. ADR: ≤150 lines. Check with `wc -l`.
- Never edit `references/apple/app-store-review-guidelines.md` (98/98).
- Don't commit `docs/research/2026-09-claude-plugin-marketplace-submission.md` (unrelated untracked file).
- Push / PR creation: ask the user first.

## File map

Commit 1 — domain slice:
- Create: `docs/research/2026-10-app-store-asset-best-practices.md` (copy from main working tree)
- Create: `docs/adr/0002-app-store-product-page-scope.md`
- Create: `references/apple/app-store-product-page.md`
- Create: `knowledge/app-store-product-page/{screenshot-specifications,app-preview-specifications,creative-assets,in-app-event-media,asset-content-restrictions,header-and-search-result-messaging,image-asset-design,video-asset-design,asset-sequencing-and-story}.md`
- Create: `skills/app-store-product-page/SKILL.md`
- Modify: `skills/index.md`, `docs/architecture/domain-map.md`, `workflows/app-store-submission/WORKFLOW.md`, `README.md`, `npx/README.md` (Skill count only), `CHANGELOG.md`

Commit 2 — ASRG slice:
- Modify: `knowledge/app-store-review-guidelines/screenshots-accuracy.md`
- Create: `knowledge/app-store-review-guidelines/metadata-age-rating.md`, `knowledge/app-store-review-guidelines/other-platform-references.md`
- Modify: `skills/app-store-review-guidelines/SKILL.md`, `references/apple/app-store-product-page.md` (Source + Used By), `knowledge/app-store-product-page/asset-content-restrictions.md` (`related`), `skills/index.md`, `docs/architecture/domain-map.md`, `CHANGELOG.md`, `docs/adr/0002-app-store-product-page-scope.md` (Verification Log)

Release PR:
- Modify: `README.md`, `npx/README.md`, `npx/package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `CHANGELOG.md`

---

### Task 0: Worktree and baseline

**Files:** none

- [ ] **Step 1: Create worktree**

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git worktree add .worktrees/app-store-product-page -b feature/app-store-product-page main
cp docs/research/2026-10-app-store-asset-best-practices.md .worktrees/app-store-product-page/docs/research/
cp docs/superpowers/plans/2026-10-15-app-store-product-page-domain.md .worktrees/app-store-product-page/docs/superpowers/plans/
cd .worktrees/app-store-product-page
```

- [ ] **Step 2: Baseline — all validators green before any change**

```bash
python3 scripts/validate_artifact.py . --all
python3 scripts/validate_repo.py .
python3 -m unittest discover tests/ -v 2>&1 | tail -3
```

Expected: no findings; unittest ends `OK`. If baseline is red, stop and report — don't build on a red tree.

---

### Task 1: Reference `app-store-product-page`

**Files:**
- Create: `references/apple/app-store-product-page.md`

- [ ] **Step 1: Verify each Source URL returns 200 with zero redirects**

```bash
for u in \
  https://developer.apple.com/app-store/asset-best-practices/ \
  https://developer.apple.com/app-store/whats-new/ \
  https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications \
  https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications \
  https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications \
  https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets \
  "https://developer.apple.com/app-store/review/guidelines/#2.3.7"; do
  printf '%s ' "$u"; curl -s -o /dev/null -w '%{http_code} redirects=%{num_redirects}\n' -L "$u"; done
```

Expected: every line `200 redirects=0`. Any redirect → use the final URL (`curl -sIL`), per `reference-spec.md`.

- [ ] **Step 2: Write the Reference** (commit-1 sources only; App Review URLs for ASRG KCs arrive in Task 13)

```markdown
# App Store Product Page

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.app-store-product-page
artifact_type: reference
title: App Store Product Page
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index behind skill.app-store-product-page.foundations -- Apple's App Store asset best practices page, the App Store Connect Help specification pages for screenshots, app previews and creative assets (product page header, search results, In-App Event media), the Asset Library page, and the App Review anchors that govern what those assets may show.
domain: App Store Product Page
last_updated: 2026-10-15
```

## Source

https://developer.apple.com/app-store/asset-best-practices/
https://developer.apple.com/app-store/whats-new/
https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
https://developer.apple.com/app-store/review/guidelines/#2.3.7

## Purpose

Records where the `app-store-product-page` domain's authority comes from: the
specifications App Store Connect enforces on upload, and the asset guidance Apple
publishes for product page headers, search results, screenshots, app previews and
In-App Events. Rejection-level compliance for the same assets stays with
`app-store-review-guidelines`; App Review anchors are indexed here only because
that domain's Reference is at its size limit.

## Primary Topics

- Screenshot specifications: counts, formats, required sizes, scaling, iPhone Duo
- App preview specifications: count, length, encoding, accepted resolutions, placement
- Creative assets: product page header, search results, universal asset, playback
- In-App Event media: event card and event details page
- Asset content restrictions: pricing, URLs, recognitions, other platforms, 4+
- Asset craft: header and search messaging, image and video design, sequencing

## Used By

- knowledge/app-store-product-page/screenshot-specifications.md ([[knowledge/app-store-product-page/screenshot-specifications]])
- knowledge/app-store-product-page/app-preview-specifications.md ([[knowledge/app-store-product-page/app-preview-specifications]])
- knowledge/app-store-product-page/creative-assets.md ([[knowledge/app-store-product-page/creative-assets]])
- knowledge/app-store-product-page/in-app-event-media.md ([[knowledge/app-store-product-page/in-app-event-media]])
- knowledge/app-store-product-page/asset-content-restrictions.md ([[knowledge/app-store-product-page/asset-content-restrictions]])
- knowledge/app-store-product-page/header-and-search-result-messaging.md ([[knowledge/app-store-product-page/header-and-search-result-messaging]])
- knowledge/app-store-product-page/image-asset-design.md ([[knowledge/app-store-product-page/image-asset-design]])
- knowledge/app-store-product-page/video-asset-design.md ([[knowledge/app-store-product-page/video-asset-design]])
- knowledge/app-store-product-page/asset-sequencing-and-story.md ([[knowledge/app-store-product-page/asset-sequencing-and-story]])
```

(The inner fence is three backticks + ` yaml`, exactly like `references/apple/app-store-review-guidelines.md`.)

- [ ] **Step 3: Validate (Used By targets don't exist yet — expect only wiki-link findings)**

```bash
python3 scripts/validate_artifact.py references/apple/app-store-product-page.md --type reference
wc -l references/apple/app-store-product-page.md
```

Expected: Level 1 passes; ≤98 lines. (`validate_repo.py` will report unresolved `[[...]]` until Tasks 2–10 land — expected.)

---

### Task 2: KC `screenshot-specifications`

**Files:**
- Create: `knowledge/app-store-product-page/screenshot-specifications.md`

- [ ] **Step 1: Verify quotes** against `.../screenshot-specifications` and `/app-store/whats-new/` (Global rules). Also confirm whether the landscape forms of the iPhone/iPad required sizes are listed; if they are, add them to Rule 2.

- [ ] **Step 2: Write the file**

```markdown
# Screenshot Specifications

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.screenshot-specifications
artifact_type: knowledge
title: Screenshot Specifications
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the App Store Connect screenshot specifications an agent must meet for iOS and iPadOS apps -- count, formats, required sizes, the scaling rule, alpha, and the iPhone Duo requirement.
domain: App Store Product Page
tags:
  - app-store-product-page
  - screenshots
  - specifications
  - iphone-duo
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
  - https://developer.apple.com/app-store/whats-new/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.asset-sequencing-and-story
last_updated: 2026-10-15
```

## Intent

This contract defines what App Store Connect accepts as a screenshot set for
an iOS or iPadOS app, so an agent producing or reviewing screenshots never
ships a size, count, or format the upload rejects.

## Scope

### Included

-   Count and file formats per device size
-   Required iPhone and iPad sizes
-   The scaling rule (highest required resolution)
-   Alpha channels
-   iPhone Duo sizes and the April 2027 requirement

### Excluded

-   What screenshots must depict (guideline 2.3.3) — see `screenshots-accuracy`
-   Mac, Apple TV, Apple Vision Pro and Apple Watch sizes — Excluded from v1;
    use the specification page directly
-   Device sizes other than those named here — the specification page is the
    only source; see Rule 6

## Rules

### Rule 1

Agents MUST provide at least one and at most 10 screenshots per device size,
in .jpeg, .jpg, or .png. "You must include at least one screenshot and can
upload up to 10 screenshots per device size in .jpeg, .jpg, or .png formats."

### Rule 2

Agents MUST include the required sizes: for iPhone, at least one screenshot
for "iPhone with Dynamic Island (medium display)" (1179 x 2556 or
1206 x 2622 portrait); for an app that supports iPadOS, at least one for
"iPad 13-inch display" (2064 x 2752 or 2048 x 2732).

### Rule 3

Agents MAY provide only the highest required resolution when the interface is
the same across device sizes and localizations. "If your app's user interface
is consistent across multiple device sizes and localizations, you only need to
provide screenshots for the highest required resolution."

### Rule 4

Agents MUST NOT upload screenshots with an alpha channel or transparency.
"Images can't include alpha channels or transparencies."

### Rule 5

Agents MUST provide iPhone Duo screenshots, starting April 2027, for any app
built with the iOS 27.1 SDK or later: outer display 1398 x 2034 or
2034 x 1398, inner display 2007 x 2853 or 2853 x 2007. "Starting in April
2027, screenshots will be required for any app using the iOS 27.1 SDK or
later."

### Rule 6

Agents SHOULD provide iPhone Duo screenshots for every iPhone app submitted
from April 2027, whatever its SDK. Apple's What's New page states the
requirement for "any apps or games submitted", which is broader than the
specification page's SDK condition in Rule 5; Rule 5 is the enforced minimum,
and this rule removes the risk of the broader reading.

### Rule 7

Agents MUST take any device size not named in this contract from the
specification page itself, and MUST NOT infer one from a device's display
resolution or aspect ratio.

## Compliant Example

-   ✓ An iPhone and iPad app uploads six 1206 x 2622 .png screenshots and
    six 2048 x 2732 .png screenshots, no alpha, and lets App Store Connect
    scale them down. (Rules 1–4)
-   ✓ An app built with the iOS 27.1 SDK adds 1398 x 2034 and
    2007 x 2853 iPhone Duo screenshots before April 2027. (Rule 5)

## Non-Compliant Example

-   ✗ Twelve screenshots for one device size, exported as transparent .png
    files. (Rules 1, 4)
-   ✗ An agent derives a 6.1-inch size from a phone's spec sheet instead of
    the specification page. (Rule 7)

## Dependencies

None.

## References

-   [App Store Connect Help — Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)
-   [App Store — What's New](https://developer.apple.com/app-store/whats-new/)
```

- [ ] **Step 3: Validate**

```bash
python3 scripts/validate_artifact.py knowledge/app-store-product-page/screenshot-specifications.md --type knowledge && wc -l knowledge/app-store-product-page/screenshot-specifications.md
```

Expected: pass; ≤150 lines.

---

### Task 3: KC `app-preview-specifications`

**Files:**
- Create: `knowledge/app-store-product-page/app-preview-specifications.md`

- [ ] **Step 1: Verify quotes** against `.../app-preview-specifications`.

- [ ] **Step 2: Write the file**

```markdown
# App Preview Specifications

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.app-preview-specifications
artifact_type: knowledge
title: App Preview Specifications
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the App Store Connect app preview specifications for iOS and iPadOS apps -- count, length, file size, frame rate, encoding, accepted resolutions, unsupported targets, and where previews appear.
domain: App Store Product Page
tags:
  - app-store-product-page
  - app-previews
  - specifications
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.video-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines what App Store Connect accepts as an app preview, and
where a preview is shown, so an agent never renders a preview the upload
rejects or one that lands somewhere other than intended.

## Scope

### Included

-   Count, length, size, frame rate, video and audio encoding
-   Accepted iPhone (including iPhone Duo) and iPad resolutions
-   Unsupported targets
-   Placement relative to screenshots

### Excluded

-   What a preview may show (guideline 2.3.4) — see `screenshots-accuracy`
-   Poster frame, pacing, looping and audio choices — see `video-asset-design`
-   Mac, Apple TV and Apple Vision Pro previews — Excluded from v1
-   iPhone Duo device resolutions labelled "19.5:9" on the specification page
    — not encoded; the label does not match those sizes (about 1.45:1)

## Rules

### Rule 1

Agents MAY add up to three app previews per supported device size and
language; previews are optional. "App previews are optional. You can upload up
to three app previews per supported device size and language".

### Rule 2

Agents MUST deliver each preview at 15–30 seconds, at most 500 MB, at most
30 fps, as H.264 at 10–12 Mbps or ProRes 422 (HQ only) at about 220 Mbps VBR,
with stereo audio at 256 kbps AAC (or PCM for ProRes) at 44.1 or 48 kHz.

### Rule 3

Agents MUST use an accepted resolution: iPhone, iPhone Duo included,
886 x 1920 or 1920 x 886; iPad 13-inch 1200 x 1600 or 1600 x 1200.

### Rule 4

Agents MUST NOT plan an app preview for a 3.5-inch iPhone ("App previews
aren't supported") or for an app on the App Store for iMessage ("App previews
are not available for apps on the App Store for iMessage").

### Rule 5

Agents MUST plan for previews appearing before screenshots on iPhone and
iPad whatever the upload order, and for a preview whose aspect ratio differs
from the screenshots appearing in "A Closer Look" instead. "App previews
always appear before screenshots on iPhone, iPad, Mac, and Apple TV — even if
you reorder them… If a preview video uses an aspect ratio different from your
screenshots, it appears in the 'A Closer Look' section".

### Rule 6

Agents MUST allow up to 24 hours between upload and availability. "Up to 24
hours after upload."

## Compliant Example

-   ✓ Two 25-second 886 x 1920 H.264 previews at 30 fps with stereo AAC audio,
    matching the portrait screenshots. (Rules 1–3, 5)

## Non-Compliant Example

-   ✗ A 45-second 60 fps preview. (Rule 2)
-   ✗ A landscape preview alongside portrait screenshots, expected to lead the
    screenshot row. (Rule 5)

## Dependencies

None.

## References

-   [App Store Connect Help — App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 4: KC `creative-assets`

**Files:**
- Create: `knowledge/app-store-product-page/creative-assets.md`

- [ ] **Step 1: Verify quotes** against `.../creative-assets-specifications` and `.../manage-your-app-store-assets`.

- [ ] **Step 2: Write the file**

```markdown
# Creative Assets

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.creative-assets
artifact_type: knowledge
title: Creative Assets
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines App Store creative assets -- what they are, their exemption from the in-use requirement, product page header and search result specifications, the universal asset, playback behaviour, fallback, and how they are reviewed.
domain: App Store Product Page
tags:
  - app-store-product-page
  - creative-assets
  - product-page-header
  - search-results
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
  - https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.header-and-search-result-messaging
  - knowledge.app-store-product-page.asset-content-restrictions
  - knowledge.app-store-review-guidelines.screenshots-accuracy
last_updated: 2026-10-15
```

## Intent

This contract defines creative assets — the optional product page header,
search result, and In-App Event card images and videos available from iOS 27
and iPadOS 27 — so an agent builds them to specification and does not confuse
them with screenshots and app previews, which carry different rules.

## Scope

### Included

-   Definition, optionality, OS availability
-   Exemption from the in-use requirement
-   Header and search result image and video specifications
-   Universal asset, playback behaviour, fallback, review

### Excluded

-   In-App Event card and details page media — see `in-app-event-media`
-   Messaging for header and search assets — see
    `header-and-search-result-messaging`

## Rules

### Rule 1

Agents MUST treat creative assets as optional and separate from screenshots
and app previews, available for apps "running iOS 27 or iPadOS 27 or later".
"Creative assets are optional and separate from your app's screenshots, app
previews, In-App Purchase and Subscription images, and any promotional artwork
requested by editorial teams."

### Rule 2

Agents MAY show brand, seasonal offerings, or new content in a creative asset
rather than the app in use: creative assets are "distinct from the in-use
functionality requirement in app previews and screenshots."

### Rule 3

Agents MUST build a product page header as a 21:9 image at 3840 x 1646
(.jpeg, .jpg, .png) or a 16:9 .png at 5244 x 2950, or as a 21:9 video at
3840 x 1646, 30 or 60 fps, 5–30 seconds (.mov, .m4v, .mp4).

### Rule 4

Agents MUST build a search result asset as a 3:2 image between 1920 x 1280
and 3840 x 2560 (.jpeg, .jpg, .png) or a 16:9 .png at 5244 x 2950, or as a
3:2 video within the same bounds, 30 or 60 fps, 5–30 seconds.

### Rule 5

Agents MUST NOT include an alpha channel or transparency. "Images can't
include alpha channels or transparencies."

### Rule 6

Agents MAY upload one universal creative asset for both placements. "If you
upload a universal creative asset, you can use it for both your product page
header and search results placement." Agents MUST NOT assume which
specification row is the universal one; the specification page does not label
it.

### Rule 7

Agents MUST NOT rely on audio in a search result video. "Videos are muted by
default in search results and can't currently be unmuted. On your product
page, videos are also muted by default, but people can unmute them. Videos
loop continuously in both placements."

### Rule 8

Agents MUST expect In-App Events, app previews, and screenshots to appear in
search results when no search result creative asset is provided. "If you
choose to not use a search result creative asset, your In-App Events, app
previews, and screenshots will appear."

### Rule 9

Agents MUST check a creative asset submitted on its own against the app's
current release. "Standalone assets are reviewed against your app's latest
version."

## Compliant Example

-   ✓ A 3840 x 1646 .jpeg header showing a seasonal campaign, plus a
    1920 x 1280 search result video whose message reads without sound.
    (Rules 2, 3, 4, 7)

## Non-Compliant Example

-   ✗ A 16:9 3840 x 2160 header image. (Rule 3)
-   ✗ A search result video whose call to action is spoken voice-over only.
    (Rule 7)

## Dependencies

None.

## References

-   [App Store Connect Help — Creative assets specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications)
-   [App Store Connect Help — Manage your App Store assets](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets)
-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 5: KC `in-app-event-media`

**Files:**
- Create: `knowledge/app-store-product-page/in-app-event-media.md`

- [ ] **Step 1: Verify quotes** against `.../creative-assets-specifications` and `/app-store/asset-best-practices/` (badge list).

- [ ] **Step 2: Write the file**

```markdown
# In-App Event Media

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.in-app-event-media
artifact_type: knowledge
title: In-App Event Media
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the media an In-App Event needs -- the 16:9 event card and the 9:16 event details page, their image and video specifications -- and how it relates to the event badge.
domain: App Store Product Page
tags:
  - app-store-product-page
  - in-app-events
  - creative-assets
references:
  - https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on:
  - knowledge.app-store-product-page.creative-assets
related: []
last_updated: 2026-10-15
```

## Intent

This contract defines the two pieces of media every In-App Event needs, so an
agent produces both orientations to specification. In-App Event cards are
creative assets, so the general creative-asset rules (alpha, review) load with
this contract through its dependency.

## Scope

### Included

-   Event card and event details page media
-   Their image and video specifications
-   Relationship to the event badge

### Excluded

-   In-App Event metadata accuracy (guideline 2.3.13) — not covered; App
    Review compliance is `app-store-review-guidelines`'s angle

## Rules

### Rule 1

Agents MUST provide both media for an event. "You need media for the event
card (16:9 landscape) and the event details page (9:16 portrait)."

### Rule 2

Agents MUST build the event card at 16:9 between 1920 x 1080 and
3840 x 2160, at most 500 MB, with any video at 30 or 60 fps and 15–30
seconds.

### Rule 3

Agents MUST build the event details page media at 9:16 between 1080 x 1920
and 2160 x 3840, at most 500 MB, with any video at 30 or 60 fps and 15–30
seconds.

### Rule 4

Agents SHOULD design the media to complement the event's badge (Challenge,
Competition, Live Event, Major Update, New Season, Premiere, Special Event)
rather than repeat it. "Design your media to complement the badge rather than
duplicate it."

## Compliant Example

-   ✓ A 1920 x 1080 card and a 1080 x 1920 details video (20 seconds) for a
    "New Season" event, neither of which prints "New Season". (Rules 1–4)

## Non-Compliant Example

-   ✗ One 16:9 image reused for both the card and the details page. (Rule 1)
-   ✗ A 10-second event card video. (Rule 2)

## Dependencies

-   `knowledge.app-store-product-page.creative-assets`

## References

-   [App Store Connect Help — Creative assets specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications)
-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 6: KC `asset-content-restrictions`

**Files:**
- Create: `knowledge/app-store-product-page/asset-content-restrictions.md`

- [ ] **Step 1: Verify quotes** against `/app-store/asset-best-practices/` and `review/guidelines/#2.3.7`.

- [ ] **Step 2: Write the file** (`related` gains the two ASRG KCs in Task 15 — they don't exist yet)

```markdown
# Asset Content Restrictions

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.asset-content-restrictions
artifact_type: knowledge
title: Asset Content Restrictions
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines what Apple's asset guidance forbids in any App Store asset -- pricing and discounts, URLs and copyright symbols, unearned or Apple-designated recognitions, other platforms, content above 4+, graphic violence -- and the relation-to-functionality limit on content outside the app.
domain: App Store Product Page
tags:
  - app-store-product-page
  - content-restrictions
  - creative-assets
  - screenshots
references:
  - https://developer.apple.com/app-store/asset-best-practices/
  - https://developer.apple.com/app-store/review/guidelines/#2.3.7
depends_on: []
related:
  - knowledge.app-store-review-guidelines.description-accuracy
  - knowledge.app-store-review-guidelines.apple-trademarks-and-product-confusion
  - knowledge.app-store-product-page.creative-assets
last_updated: 2026-10-15
```

## Intent

This contract defines what no App Store asset — screenshot, app preview, or
creative asset — may contain, per Apple's asset best practices page. Apart
from pricing (guideline 2.3.7), these rules come from Apple's asset guidance,
not the App Review Guidelines: agents apply them as written but MUST NOT
present a breach as a stated rejection reason.

## Scope

### Included

-   Pricing, discounts, URLs, copyright symbols
-   Unearned awards and Apple-designated recognitions
-   Other platforms and 4+ suitability, extended to creative assets
-   Violence limits; content outside the app

### Excluded

-   Guideline 2.3.8 and 2.3.10 as review rules for screenshots and previews
    — `app-store-review-guidelines` owns them
-   Misleading marketing claims in text metadata — see `description-accuracy`

## Rules

### Rule 1

Agents MUST NOT show specific pricing or discounts in any asset. "Don't
include specific pricing, discounts, website URLs, copyright symbols."
Guideline 2.3.7 says the same for screenshots and previews, which "should not
include prices, terms, or descriptions that are not specific to the metadata
type".

### Rule 2

Agents MUST NOT show website URLs or copyright symbols in any asset.

### Rule 3

Agents MUST NOT claim awards or recognition the app has not received. "Avoid
claims that can't be verified, such as awards or recognition that your app or
game hasn't actually received."

### Rule 4

Agents MUST NOT show Apple-designated recognitions. "Please don't include any
Apple-designated recognitions — such as Editor's Choice, App of the Day, Game
of the Day, or Apple Design Award winner".

### Rule 5

Agents MUST keep logos and references to other platforms or marketplaces out
of creative assets as well as screenshots and previews. "Don't include logos
or references to other platforms or marketplaces."

### Rule 6

Agents MUST hold creative assets to 4+ as well. "Assets displayed on the App
Store must meet a 4+ age rating, even if your app's rating is higher",
refraining from "explicit or harmful imagery, profanity, illegal drugs,
self-harm, hate speech, stereotypes, sexually suggestive content,
inflammatory religious commentary, or inaccurate and misleading quotations of
religious texts."

### Rule 7

Agents MAY use action imagery for a game with violence but MUST NOT show
"gore, graphic imagery, or weapons that are pointed directly at a person or
the audience."

### Rule 8

Agents MUST keep content from outside the app related to what the app does.
"While you may depict content outside of your app or game in use, it must
still relate to its general functionality."

## Compliant Example

-   ✓ A search result asset with the game's characters mid-action, no price,
    no URL, no platform logos. (Rules 1, 2, 5, 7)

## Non-Compliant Example

-   ✗ A header reading "50% off this week — example.com". (Rules 1, 2)
-   ✗ A screenshot captioned "App of the Day". (Rule 4)
-   ✗ A creative asset with a rifle aimed at the viewer. (Rule 7)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
-   [Apple App Review Guidelines — 2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 7: KC `header-and-search-result-messaging`

**Files:**
- Create: `knowledge/app-store-product-page/header-and-search-result-messaging.md`

- [ ] **Step 1: Verify quotes** against `/app-store/asset-best-practices/`.

- [ ] **Step 2: Write the file**

```markdown
# Header and Search Result Messaging

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.header-and-search-result-messaging
artifact_type: knowledge
title: Header and Search Result Messaging
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable messaging guidance for product page header and search result creative assets -- one idea per header, purpose obvious at a glance, the firsthand experience in search, and testing header variants.
domain: App Store Product Page
tags:
  - app-store-product-page
  - product-page-header
  - search-results
  - messaging
references:
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.creative-assets
  - knowledge.app-store-product-page.image-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines what a product page header and a search result asset
should say, using only guidance an agent can check against the finished
asset.

## Scope

### Included

-   Header focus
-   Search result clarity and firsthand experience
-   Testing header variants

### Excluded

-   Specifications — see `creative-assets`
-   Subjective guidance ("Design with a first-time visitor in mind",
    "compelling visuals") — Excluded; not checkable

## Rules

### Rule 1

Agents SHOULD build each product page header around one idea, without dense or
cluttered visuals. "Focus on a single, clear idea. Visually dense or cluttered
assets dilute your impact."

### Rule 2

Agents SHOULD make the app's purpose readable from a search result asset alone.
"State the obvious. … be sure your app or game's purpose is obvious at a
glance."

### Rule 3

Agents SHOULD show the app or game experience itself in a search result asset.
"Showcase the firsthand experience."

### Rule 4

Agents SHOULD test alternative header visuals with product page optimization
rather than choosing one untested. "…you can use product page optimization to
test alternative header visuals…"

## Compliant Example

-   ✓ A recipe app's header shows one plated dish under the line "Dinner in
    20 minutes"; its search result asset shows the cooking-mode screen. (Rules 1–3)

## Non-Compliant Example

-   ✗ A header packing six feature callouts and a collage of screens. (Rule 1)
-   ✗ A search result asset of an abstract gradient and the app's logo, with
    no hint of what the app does. (Rules 2, 3)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 8: KC `image-asset-design`

**Files:**
- Create: `knowledge/app-store-product-page/image-asset-design.md`

- [ ] **Step 1: Verify quotes** against `/app-store/asset-best-practices/`.

- [ ] **Step 2: Write the file**

```markdown
# Image Asset Design

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.image-asset-design
artifact_type: knowledge
title: Image Asset Design
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable design guidance for App Store image assets -- centered focal point and safe area against clipping, previewing in App Store Connect, short text that adds to the visual, and localized text.
domain: App Store Product Page
tags:
  - app-store-product-page
  - images
  - design
  - localization
references:
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.video-asset-design
  - knowledge.app-store-product-page.header-and-search-result-messaging
last_updated: 2026-10-15
```

## Intent

This contract defines how to compose an App Store image — screenshot or image
creative asset — so it survives cropping on every device and reads in every
language the app supports.

## Scope

### Included

-   Focal point, safe area, clipping
-   App Store Connect Preview tool
-   Text length and role; text localization

### Excluded

-   Video assets — see `video-asset-design`
-   Subjective guidance ("Choose compelling visuals") — Excluded; not checkable

## Rules

### Rule 1

Agents SHOULD keep key elements inside a safe area and the focal point in the
center of the composition. "Design key elements with a safe area in mind to
accommodate different devices and orientations. Be sure your focal point
artwork is within the center of your composition to prevent any unwanted
clipping."

### Rule 2

Agents SHOULD check the result in App Store Connect's Preview tool before
submitting. "You can use the Preview tool in App Store Connect…"

### Rule 3

Agents SHOULD limit image text to a short phrase that adds to the visual
rather than describes it. "…use a short phrase that enhances your visual
rather than describes it."

### Rule 4

Agents SHOULD localize image text into every language the app supports. "Be
sure to localize for all languages your app supports."

## Compliant Example

-   ✓ A header with the subject centered, the headline well inside the safe
    area, and German and Japanese variants of the headline. (Rules 1, 4)

## Non-Compliant Example

-   ✗ A product shot pushed to the right edge, clipped on iPhone. (Rule 1)
-   ✗ The caption "This screenshot shows the timer screen" over the timer
    screen. (Rule 3)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 9: KC `video-asset-design`

**Files:**
- Create: `knowledge/app-store-product-page/video-asset-design.md`

- [ ] **Step 1: Verify quotes** against `/app-store/asset-best-practices/`, `.../manage-your-app-store-assets` and `.../app-preview-specifications` (5-second default poster frame).

- [ ] **Step 2: Write the file**

```markdown
# Video Asset Design

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.video-asset-design
artifact_type: knowledge
title: Video Asset Design
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable design guidance for App Store videos -- choosing the poster frame before approval, leading with the value proposition, avoiding quick cuts, looping seamlessly, and working without sound.
domain: App Store Product Page
tags:
  - app-store-product-page
  - video
  - app-previews
  - design
references:
  - https://developer.apple.com/app-store/asset-best-practices/
  - https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
  - https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
depends_on: []
related:
  - knowledge.app-store-product-page.app-preview-specifications
  - knowledge.app-store-product-page.creative-assets
  - knowledge.app-store-product-page.image-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines how to cut an App Store video — app preview or video
creative asset — for a placement that autoplays, loops, and starts muted.

## Scope

### Included

-   Poster frame
-   Opening, pacing, looping
-   Audio

### Excluded

-   Encoding, length, resolution — see `app-preview-specifications` and
    `creative-assets`
-   Subjective guidance ("Consider compelling visuals") — Excluded; not checkable

## Rules

### Rule 1

Agents MUST choose the poster frame deliberately before the asset is approved:
it is "the first image someone sees before your video plays", an app preview
defaults to the frame at 5 seconds, and "Poster frames can't be edited after
assets have been approved."

### Rule 2

Agents SHOULD open with the value proposition or the strongest feature. "Start
strong. Lead with your value proposition or most compelling feature."

### Rule 3

Agents SHOULD avoid quick cuts and fast motion. "Avoid quick cuts and
fast-moving visuals, as these can be difficult for people to follow and may
not be accessible for everyone."

### Rule 4

Agents SHOULD make the last frame flow into the first. "Loop seamlessly.
Videos autoplay and repeat…"

### Rule 5

Agents SHOULD make the video understandable with the sound off, and keep any
audio a short, clean-looping music bed without sudden loud moments. "In most
cases, audio is muted by default, so your creative must work silently first. …
Favor a short music loop over heavy sound effects, avoid sudden loud moments,
and ensure the audio loops cleanly".

## Compliant Example

-   ✓ A preview that opens on the core feature, holds each shot for several
    seconds, carries captions, and ends where it began. (Rules 2–5)

## Non-Compliant Example

-   ✗ A preview whose 5-second default poster frame is a blurred transition,
    left unchanged until after approval. (Rule 1)
-   ✗ A trailer cut at two cuts per second with the key message in voice-over
    only. (Rules 3, 5)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
-   [App Store Connect Help — Manage your App Store assets](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets)
-   [App Store Connect Help — App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 10: KC `asset-sequencing-and-story`

**Files:**
- Create: `knowledge/app-store-product-page/asset-sequencing-and-story.md`

- [ ] **Step 1: Verify quotes** against `/app-store/asset-best-practices/`.

- [ ] **Step 2: Write the file**

```markdown
# Asset Sequencing and Story

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-product-page.asset-sequencing-and-story
artifact_type: knowledge
title: Asset Sequencing and Story
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the checkable guidance for ordering and unifying a product page's assets -- best features in the first three screenshots, a cohesive sequence, no screenshot spent on accolades or calls to action, one visual system, and previews with a beginning, middle, and end.
domain: App Store Product Page
tags:
  - app-store-product-page
  - screenshots
  - app-previews
  - sequencing
references:
  - https://developer.apple.com/app-store/asset-best-practices/
depends_on: []
related:
  - knowledge.app-store-product-page.screenshot-specifications
  - knowledge.app-store-product-page.video-asset-design
last_updated: 2026-10-15
```

## Intent

This contract defines how a product page's screenshots and previews are
ordered and unified, so that what search results show first and what the
product page shows together tell one story.

## Scope

### Included

-   Screenshot order and the search-results window
-   Screenshot content focus
-   Visual consistency across assets
-   Preview story structure

### Excluded

-   Counts and sizes — see `screenshot-specifications`

## Rules

### Rule 1

Agents SHOULD put the strongest features in the first three screenshots:
"Depending on orientation, up to three screenshots can appear in search
results." "Lead with your best features."

### Rule 2

Agents SHOULD order screenshots so that, read in sequence, they tell one
story. "…sequence them so they tell a cohesive story…"

### Rule 3

Agents SHOULD NOT spend a whole screenshot on accolades or a call to action.
"…avoid using the entire asset to highlight general accolades or
call-to-action statements."

### Rule 4

Agents SHOULD share one visual system across every asset. "…consider using
similar visual style, such as color palette, iconography, fonts, message, and
tone."

### Rule 5

Agents SHOULD give each app preview a beginning, middle, and end. "Tell a
complete story. Consider having a beginning, middle, and end…"

## Compliant Example

-   ✓ Screenshots 1–3 show the three headline features in one type family
    and palette; 4–8 continue the same flow. (Rules 1, 2, 4)

## Non-Compliant Example

-   ✗ Screenshot 1 is a full-frame "Download now!" banner. (Rules 1, 3)

## Dependencies

None.

## References

-   [App Store asset best practices and resources](https://developer.apple.com/app-store/asset-best-practices/)
```

- [ ] **Step 3: Validate** — same command as Task 2 Step 3 with this path. Expected: pass; ≤150 lines.

---

### Task 11: Skill, index, ADR, domain-map, workflow, README, CHANGELOG — then commit 1

**Files:**
- Create: `skills/app-store-product-page/SKILL.md`, `docs/adr/0002-app-store-product-page-scope.md`
- Modify: `skills/index.md`, `docs/architecture/domain-map.md`, `workflows/app-store-submission/WORKFLOW.md`, `README.md`, `npx/README.md`, `CHANGELOG.md`

- [ ] **Step 1: Write the Skill**

```markdown
---
name: app-store-product-page
description: Route App Store product page asset tasks to the correct Knowledge Contracts — screenshot specifications, app preview specifications, creative assets (product page header, search results, universal asset), In-App Event media, asset content restrictions, header and search result messaging, image and video asset design, and asset sequencing. Use when sizing or exporting screenshots or app previews, designing a product page header or search result creative asset, preparing In-App Event media, choosing a poster frame, or ordering screenshots for the App Store. v1 is iOS/iPadOS visual assets only — no product page text fields, no Mac/TV/Vision/Watch asset specs. Whether a screenshot passes App Review is owned by app-store-review-guidelines. Triggers on screenshot specifications, screenshot sizes, App Store screenshot size, app preview specifications, app preview video, product page header, search result creative asset, creative assets, universal creative asset, In-App Event media, event card, poster frame, Asset Library, product page preview tool, App Store asset best practices, iPhone Duo screenshots.
id: skill.app-store-product-page.foundations
title: App Store Product Page — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: App Store Product Page
routes: [knowledge.app-store-product-page.screenshot-specifications, knowledge.app-store-product-page.app-preview-specifications, knowledge.app-store-product-page.creative-assets, knowledge.app-store-product-page.in-app-event-media, knowledge.app-store-product-page.asset-content-restrictions, knowledge.app-store-product-page.header-and-search-result-messaging, knowledge.app-store-product-page.image-asset-design, knowledge.app-store-product-page.video-asset-design, knowledge.app-store-product-page.asset-sequencing-and-story]
related:
  - skill.app-store-review-guidelines.submission
  - skill.human-interface-guidelines.foundations
last_updated: 2026-10-15
---

# App Store Product Page — Foundations Skill

## Purpose

Route App Store product page asset tasks to the minimum required App Store
Product Page Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-store-product-page/.

-   Screenshot sizes and counts -> screenshot-specifications.md
-   App preview encoding and placement -> app-preview-specifications.md
-   Product page header, search result, universal asset -> creative-assets.md
-   In-App Event card and details media -> in-app-event-media.md
-   What no asset may show -> asset-content-restrictions.md
-   What a header or search asset should say -> header-and-search-result-messaging.md
-   Composing an image -> image-asset-design.md
-   Cutting a video, poster frame -> video-asset-design.md
-   Ordering and unifying the set -> asset-sequencing-and-story.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-store-product-page/ — do not guess or
fall back to general knowledge.

-   Whether screenshots and previews pass App Review (guideline 2.3) — owned by
    `app-store-review-guidelines`
-   App icon design — owned by `human-interface-guidelines`
-   Product page text fields (subtitle, promotional text, keywords), product
    page optimization setup, and custom product pages — Deferred
-   Mac, Apple TV, Apple Vision Pro and Apple Watch asset specifications;
    App Store Connect upload mechanics and API — Excluded
```

- [ ] **Step 2: Add the Routing Index row** — in `skills/index.md`, `## Skills` table, insert directly after the `skills/app-store-review-guidelines/SKILL.md` row:

```markdown
| screenshot specifications, screenshot sizes, App Store screenshot size, app preview specifications, app preview video, product page header, search result creative asset, creative assets, universal creative asset, In-App Event media, event card, poster frame, Asset Library, product page preview tool, App Store asset best practices, iPhone Duo screenshots | skills/app-store-product-page/SKILL.md |
```

- [ ] **Step 3: Write ADR-0002**

```markdown
# ADR-0002: App Store Product Page Domain Scope

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: adr.0002
artifact_type: adr
title: App Store Product Page Domain Scope
version: 1.0.0
status: Approved
domain: App Store Product Page
related: []
last_updated: 2026-10-15
```

## Context

Apple's "App Store asset best practices and resources" page
(https://developer.apple.com/app-store/asset-best-practices/), introduced on
2026-08-05, and the App Store Connect Help pages that went live with creative
assets on 2026-10-05 (header, search results, In-App Event media; iPhone Duo
screenshot sizes) had no coverage in this repository. The research is in
`docs/research/2026-10-app-store-asset-best-practices.md`; the decisions were
made in a maintainer review on 2026-10-15 and are listed in
`docs/superpowers/plans/2026-10-15-app-store-product-page-domain.md`.

Two constraints shaped the scope. `app-store-review-guidelines` already owned
screenshot and preview accuracy (2.3.3, 2.3.4), and its Reference was at the
98-line limit `reference-spec.md` sets. And most of Apple's asset guidance is
advice, not a review rule.

## Decision

Create `app-store-product-page` as its own domain: App Store Connect asset
specifications and Apple's asset guidance for iOS and iPadOS visual assets
(screenshots, app previews, creative assets, In-App Event media), as
`domain-map.md`'s Tier 1 row states. Product page text fields are Deferred;
other platforms' asset specifications are Excluded.

## Consequences

- Angle split with `app-store-review-guidelines`: it owns what gets rejected,
  this domain owns specifications and how to make assets effective.
- `references/apple/app-store-product-page.md` indexes the App Review URLs that
  `app-store-review-guidelines` Contracts cite for 2.3.3 (help page), 2.3.4,
  2.3.8 and 2.3.10, because the other Reference has no room. Indexing is by URL
  and many-to-many, so this is valid; a reader looking for those URLs in
  `references/apple/app-store-review-guidelines.md` will not find them there.
- "Don't" items on the asset page that no guideline states (URLs, copyright
  symbols, discounts) are encoded as MUST NOT, following Apple's wording, with
  each Contract's Intent saying they are asset guidance, not rejection reasons.
- Only craft guidance an agent can check is encoded (SHOULD); subjective
  guidance is Excluded.
- The iPhone Duo April 2027 requirement is encoded as the specification page's
  SDK-bound MUST plus a SHOULD for the broader What's New wording.
- `workflow.app-store-submission` gains no step; its Excluded list points here.

## Verification Log

- 2026-10-15: initial scope recorded; 9 Knowledge Contracts and
  `skill.app-store-product-page.foundations` shipped.
```

- [ ] **Step 4: domain-map.md** (four edits; bump the header `Version: 1.26.0` → `Version: 1.27.0`)

(a) Tier 1 table — insert after the `| App Store Review Guidelines | app-store-review-guidelines | ...` row:

```markdown
| App Store Product Page | app-store-product-page | iOS/iPadOS visual asset v1 — **built 2026-10-15**: screenshot specifications (counts, formats, required sizes, scaling, iPhone Duo), app preview specifications, creative assets (product page header, search results, universal asset), In-App Event media, asset content restrictions, and checkable asset craft (header and search messaging, image design, video design, sequencing). Product page text fields (subtitle, promotional text, keywords), product page optimization setup and custom product pages Deferred; Mac/TV/Vision/Watch asset specs and App Store Connect upload mechanics Excluded. | App Store asset specifications and asset guidance; App Review compliance of the same assets owned by app-store-review-guidelines | [ADR-0002](../adr/0002-app-store-product-page-scope.md) |
```

(b) In the `Completed:` paragraph (line ~30), append before its final period: `, `app-store-product-page` (Tier 1 — scope in ADR-0002)`.

(c) `## Cross-Domain Notes` — append after the bullet that begins `` - `app-store-review-guidelines` (`privacy-manifest`/`privacy-nutrition-label` topics) and `privacy` ``:

```markdown
- `app-store-review-guidelines` and `app-store-product-page` (Tier 1, 2026-10-15) split by angle, same pattern as `privacy` above: `app-store-review-guidelines` owns what App Review rejects in screenshots and previews (2.3.3 majority-in-use, 2.3.4, 2.3.8, 2.3.10), `app-store-product-page` owns the App Store Connect specifications and Apple's asset guidance. `references/apple/app-store-product-page.md` indexes the App Review URLs both domains cite because `references/apple/app-store-review-guidelines.md` is at its 98-line limit — see ADR-0002. Creative assets are exempt from the in-use rule; `creative-assets.md` Rule 2 and `screenshots-accuracy.md` state that boundary from each side.
```

(d) No separate gap list exists in `domain-map.md` — domains record Deferred topics in their own row. The row in (a) already names the three Deferred topics (`skill-spec.md`: every `Deferred` topic appears as a gap against its domain), so no further edit.

- [ ] **Step 5: workflow pointer** — in `workflows/app-store-submission/WORKFLOW.md`, replace

```markdown
- App Store Connect metadata, pricing, and phased release — outside this repository
```

with

```markdown
- App Store Connect metadata, pricing, and phased release — outside this repository; screenshot, app preview and creative asset specifications and design are owned by `app-store-product-page`
```

and bump the workflow's `Version:` line and metadata `version:` `1.0.0` → `1.0.1`, `last_updated: 2026-10-15`.

- [ ] **Step 6: README.md** — in `## Skills`, insert after the `app-store-review-guidelines` bullet:

```markdown
- **`app-store-product-page`** — screenshots, app previews, header and search creative assets. → [SKILL.md](skills/app-store-product-page/SKILL.md)
```

Change `34 Skills total` → `35 Skills total`. In `## What's New`, add at the top:

```markdown
- 2026-10-15 — **App Store product page assets landed.** A new `app-store-product-page` Skill routes 9 Knowledge Contracts built from Apple's App Store asset best practices and the App Store Connect specifications: screenshot and app preview specs (including iPhone Duo), the new product page header and search result creative assets, In-App Event media, content restrictions, and checkable design guidance. `app-store-review-guidelines` now encodes App Review's "more than half of screenshots show the app in use" rule and guidelines 2.3.8 and 2.3.10. See `CHANGELOG.md` for details.
```

then delete the oldest bullet (the `2026-08-23 — Codex CLI support landed.` one) so exactly 3 remain. In `npx/README.md`, change `34 Skills` → `35 Skills` (count only; no npm publish — `npx/` code is unchanged).

- [ ] **Step 7: CHANGELOG.md** — under `## [Unreleased]`:

```markdown
### Added
- **New `app-store-product-page` domain.** `references/apple/app-store-product-page.md`, 9 Knowledge Contracts (`screenshot-specifications`, `app-preview-specifications`, `creative-assets`, `in-app-event-media`, `asset-content-restrictions`, `header-and-search-result-messaging`, `image-asset-design`, `video-asset-design`, `asset-sequencing-and-story`) and `skill.app-store-product-page.foundations`, built from Apple's App Store asset best practices page and the App Store Connect specification pages that went live with creative assets on 2026-10-05. Scope and the cross-domain indexing decision: `docs/adr/0002-app-store-product-page-scope.md`. Research: `docs/research/2026-10-app-store-asset-best-practices.md`.
```

- [ ] **Step 8: Full validation**

```bash
python3 scripts/validate_artifact.py . --all
python3 scripts/validate_repo.py .
python3 -m unittest discover tests/ -v 2>&1 | tail -3
python3 scripts/check_links.py . --files references/apple/app-store-product-page.md knowledge/app-store-product-page/*.md
wc -l skills/app-store-product-page/SKILL.md references/apple/app-store-product-page.md references/apple/app-store-review-guidelines.md docs/adr/0002-app-store-product-page-scope.md
```

Expected: no findings from either validator (watch for `routing-ambiguous`, `used-by-complete`, `scope-vocabulary`, `domain-map-adr-link`); unittest `OK`; check_links reports no 404 and no redirect; Skill ≤80, Reference ≤98, ASRG Reference exactly 98, ADR ≤150. Fix any finding before committing.

- [ ] **Step 9: Commit 1**

```bash
git add docs/research/2026-10-app-store-asset-best-practices.md docs/superpowers/plans/2026-10-15-app-store-product-page-domain.md docs/adr/0002-app-store-product-page-scope.md references/apple/app-store-product-page.md knowledge/app-store-product-page skills/app-store-product-page skills/index.md docs/architecture/domain-map.md workflows/app-store-submission/WORKFLOW.md README.md npx/README.md CHANGELOG.md
git commit -m "$(cat <<'EOF'
feat: add app-store-product-page domain

New vertical slice built from Apple's App Store asset best practices page
and the App Store Connect specification pages for screenshots, app
previews and creative assets (product page header, search results,
In-App Event media). 9 Knowledge Contracts, one Skill, ADR-0002.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 12: Amend `screenshots-accuracy`

**Files:**
- Modify: `knowledge/app-store-review-guidelines/screenshots-accuracy.md`

- [ ] **Step 1: Verify quotes** against `https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots` and `review/guidelines/#2.3.4`; check both with the Task 1 Step 1 curl loop (expect `200 redirects=0`).

- [ ] **Step 2: Edit metadata** — `version: 1.1.0`, `last_updated: 2026-10-15`, header line `Status: Approved Version: 1.1.0`; replace `references:` and `related:` with:

```yaml
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.3
  - https://developer.apple.com/app-store/review/guidelines/#2.3.4
  - https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
depends_on: []
related:
  - knowledge.app-store-review-guidelines.description-accuracy
  - knowledge.app-store-product-page.screenshot-specifications
  - knowledge.app-store-product-page.creative-assets
```

- [ ] **Step 3: Replace Rule 1** with:

```markdown
### Rule 1

Agents MUST ensure that, for each supported device and each localization,
more than half of the screenshots show the app in use; the rest MAY show the
app's benefits with marketing material, splash screens, or marketing text. App
Review "will approve only those submissions where more than half of
screenshots show the app in use." One screenshot is enough when it shows the
app in use, and one image of the app in use MAY span several screenshots.
```

- [ ] **Step 4: Add Rules 5 and 6** after Rule 4:

```markdown
### Rule 5

Agents MUST NOT let overlays or marketing visuals crowd out the app, and MUST
NOT submit a screenshot that shows only hardware, or an overlay with no app
interface behind it. "Don't let overlays or marketing visuals crowd out your
app." "Don't show only the hardware or an overlay with no app interface behind
it."

### Rule 6

Agents SHOULD update screenshots with each new version so they match the
current interface. "Update your screenshots with each new version so they
match the current user interface."
```

- [ ] **Step 5: Scope, examples, references**
  - `### Included`: add `-   The majority-in-use rule per device and localization` and `-   Overlay and hardware-only limits`.
  - `### Excluded`: add `-   Creative assets (product page header, search results) — exempt from the in-use rule; see `creative-assets``, and `-   Screenshot sizes and counts — see `screenshot-specifications``.
  - Intent: replace "must show: the app in actual use" sentence with "must show — a majority of the app in actual use per device and localization — and what App Preview videos may contain (guideline 2.3.3, 2.3.4)."
  - Compliant Example: add `-   ✓ Four screenshots per device: three show real app screens, the fourth is a marketing panel. (Rule 1)`
  - Non-Compliant Example: replace the splash bullet with `-   ✗ Four screenshots per device, two of them marketing panels with no app UI — exactly half, not more than half, show the app. (Rule 1)` and add `-   ✗ A screenshot of the bare device frame with a tagline. (Rule 5)`
  - `## References`: add `-   [Apple App Review Guidelines — 2.3.4](https://developer.apple.com/app-store/review/guidelines/#2.3.4)` and `-   [App Review — Guideline 2.3.3 Screenshots](https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots)`

- [ ] **Step 6: Validate** — `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/screenshots-accuracy.md --type knowledge && wc -l knowledge/app-store-review-guidelines/screenshots-accuracy.md`. Expected: pass; ≤150. (`validate_repo.py` now reports `reference-indexes-citations` for the two new URLs — fixed in Task 15.)

---

### Task 13: New KC `metadata-age-rating` (2.3.8)

**Files:**
- Create: `knowledge/app-store-review-guidelines/metadata-age-rating.md`

- [ ] **Step 1: Fetch guideline 2.3.8 verbatim** from `https://developer.apple.com/app-store/review/guidelines/` (the `2.3.8` paragraph). The rules below follow the research note's quote ("icons, screenshots, and previews adhere to a 4+ age rating") plus the rest of the paragraph as last published; **rewrite Rules 2–3 to match the live text** if it differs, and drop any rule the live text doesn't support.

- [ ] **Step 2: Write the file**

```markdown
# Metadata Age Rating

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.metadata-age-rating
artifact_type: knowledge
title: Metadata Age Rating
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 2.3.8 -- app and in-app purchase icons, screenshots, and previews must suit a 4+ audience whatever the app's rating, violent games choose non-graphic images, and "For Kids"/"For Children" is reserved for the Kids Category.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - metadata
  - age-rating
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.8
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.asset-content-restrictions
last_updated: 2026-10-15
```

## Intent

This contract defines guideline 2.3.8: App Store metadata is seen by every
audience, so its imagery is held to a 4+ rating even when the app is not.

## Scope

### Included

-   4+ suitability of app and in-app purchase icons, screenshots, previews
-   Violent games' metadata imagery
-   "For Kids" / "For Children" wording

### Excluded

-   Creative assets and the asset page's objectionable-content list — see
    `asset-content-restrictions`
-   The app's own age rating questionnaire — not covered

## Rules

### Rule 1

Agents MUST keep app and in-app purchase icons, screenshots, and previews
suitable for a 4+ age rating, even when the app is rated higher. Metadata
should "adhere to a 4+ age rating even if your app is rated higher."

### Rule 2

Agents MUST, for a game that includes violence, choose metadata images that
"don't depict a gruesome death or a gun pointed at a specific character."

### Rule 3

Agents MUST NOT use "For Kids" or "For Children" in app metadata unless the
app is in the Kids Category; those terms are "reserved for the Kids Category."

## Compliant Example

-   ✓ A 17+ horror game's screenshots show its atmosphere and puzzles, with
    no gore. (Rules 1, 2)

## Non-Compliant Example

-   ✗ A shooter's first screenshot frames a gun aimed at a character's head.
    (Rule 2)
-   ✗ A general-audience drawing app subtitled "For Kids". (Rule 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3.8](https://developer.apple.com/app-store/review/guidelines/#2.3.8)
```

- [ ] **Step 3: Validate** — `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/metadata-age-rating.md --type knowledge`. Expected: pass.

---

### Task 14: New KC `other-platform-references` (2.3.10)

**Files:**
- Create: `knowledge/app-store-review-guidelines/other-platform-references.md`

- [ ] **Step 1: Fetch guideline 2.3.10 verbatim** (same page) and confirm the 2.3.3 help page's status-bar sentence. Adjust Rule 1's wording and exception to the live text.

- [ ] **Step 2: Write the file**

```markdown
# Other Platform References

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.other-platform-references
artifact_type: knowledge
title: Other Platform References
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 2.3.10 -- no names, icons, or imagery of other mobile platforms or alternative app marketplaces in the app or its metadata, including a third-party status bar in a screenshot.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - metadata
  - screenshots
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.3.10
  - https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
  - knowledge.app-store-product-page.asset-content-restrictions
last_updated: 2026-10-15
```

## Intent

This contract defines guideline 2.3.10: an App Store app and its metadata stay
focused on Apple platforms and do not show other mobile platforms or
alternative app marketplaces.

## Scope

### Included

-   Names, icons, imagery of other mobile platforms and marketplaces
-   Third-party status bars in screenshots

### Excluded

-   Creative assets — see `asset-content-restrictions`

## Rules

### Rule 1

Agents MUST NOT include "names, icons, or imagery of other mobile platforms or
alternative app marketplaces" in the app or its metadata, unless the app has
specific, approved interactive functionality that requires it.

### Rule 2

Agents MUST capture screenshots on an Apple device or Simulator so no
third-party platform appears, status bar included. "Screenshots that reference
third-party platforms, such as in a status bar, are assessed under App Review
Guideline 2.3.10."

## Compliant Example

-   ✓ Screenshots captured in the iOS Simulator with a clean status bar.
    (Rule 2)

## Non-Compliant Example

-   ✗ A screenshot taken on an Android build, its status bar visible. (Rule 2)
-   ✗ A description line "Also on Google Play". (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3.10](https://developer.apple.com/app-store/review/guidelines/#2.3.10)
-   [App Review — Guideline 2.3.3 Screenshots](https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots)
```

- [ ] **Step 3: Validate** — `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/other-platform-references.md --type knowledge`. Expected: pass.

---

### Task 15: Wire ASRG slice — Reference, Skill, index, map, ADR, CHANGELOG — then commit 2

**Files:**
- Modify: `references/apple/app-store-product-page.md`, `knowledge/app-store-product-page/asset-content-restrictions.md`, `skills/app-store-review-guidelines/SKILL.md`, `skills/index.md`, `docs/architecture/domain-map.md`, `docs/adr/0002-app-store-product-page-scope.md`, `CHANGELOG.md`

- [ ] **Step 1: Reference** — add to `## Source` (keep sorted as in Task 1, App Review URLs last):

```text
https://developer.apple.com/app-store/review/guidelines/#2.3.4
https://developer.apple.com/app-store/review/guidelines/#2.3.8
https://developer.apple.com/app-store/review/guidelines/#2.3.10
https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
```

add to `## Used By`:

```markdown
- knowledge/app-store-review-guidelines/screenshots-accuracy.md ([[knowledge/app-store-review-guidelines/screenshots-accuracy]])
- knowledge/app-store-review-guidelines/metadata-age-rating.md ([[knowledge/app-store-review-guidelines/metadata-age-rating]])
- knowledge/app-store-review-guidelines/other-platform-references.md ([[knowledge/app-store-review-guidelines/other-platform-references]])
```

bump `version: 1.1.0` / `Version: 1.1.0`. Confirm `wc -l` ≤98.

- [ ] **Step 2: asset-content-restrictions `related`** — add `knowledge.app-store-review-guidelines.metadata-age-rating` and `knowledge.app-store-review-guidelines.other-platform-references`; bump to `1.0.1` (header + metadata).

- [ ] **Step 3: ASRG Skill** (`skills/app-store-review-guidelines/SKILL.md`):
  - `routes:` append `knowledge.app-store-review-guidelines.metadata-age-rating, knowledge.app-store-review-guidelines.other-platform-references`.
  - Routing line `-   Metadata accuracy -> screenshots-accuracy.md, description-accuracy.md` → `-   Metadata accuracy -> screenshots-accuracy.md (2.3.3 majority in use, 2.3.4), description-accuracy.md, metadata-age-rating.md (2.3.8), other-platform-references.md (2.3.10)`.
  - Stop Conditions: add `-   Screenshot, app preview and creative asset specifications and design — owned by `app-store-product-page``.
  - `description:` after "screenshot/description accuracy," insert "metadata age rating, other-platform references in metadata,"; append triggers `screenshots show app in use, metadata age rating, 4+ screenshots, For Kids metadata, other platform in screenshots, Android status bar screenshot` before the final period.
  - `version: 1.1.0`, `last_updated: 2026-10-15`. Confirm `wc -l` ≤80.

- [ ] **Step 4: Routing Index** — append to the ASRG row's keyword cell: `, screenshots show app in use, metadata age rating, 4+ screenshots, For Kids metadata, other platform in screenshots, Android status bar screenshot`.

- [ ] **Step 5: domain-map** — ASRG Tier 1 row: change `2.3 Accurate Metadata` to `2.3 Accurate Metadata (incl. 2.3.3 majority-in-use, 2.3.8 metadata age rating, 2.3.10 other platforms — added 2026-10-15)`. Version `1.27.0` → `1.28.0`.

- [ ] **Step 6: ADR-0002 Verification Log** — append:

```markdown
- 2026-10-15: `app-store-review-guidelines` slice — `screenshots-accuracy`
  1.1.0 (majority-in-use), new `metadata-age-rating` (2.3.8) and
  `other-platform-references` (2.3.10); their App Review URLs indexed in
  `references/apple/app-store-product-page.md` per Consequences.
```

- [ ] **Step 7: CHANGELOG** — under `## [Unreleased]`, add to `### Added`:

```markdown
- **`app-store-review-guidelines`: guidelines 2.3.8 and 2.3.10.** New `metadata-age-rating` and `other-platform-references` Knowledge Contracts, routed by `skill.app-store-review-guidelines.submission` (1.1.0).
```

and a new `### Changed`:

```markdown
### Changed
- **`screenshots-accuracy` (1.1.0) follows App Review's new 2.3.3 guidance.** Rule 1 now requires *more than half* of each device's and each localization's screenshots to show the app in use (it read as "all"), and new rules forbid overlays that crowd out the app or hardware-only screenshots. Source: https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots, indexed in `references/apple/app-store-product-page.md` because the App Review Guidelines Reference is at its 98-line limit (ADR-0002).
```

- [ ] **Step 8: Full validation** — Task 11 Step 8 commands, plus:

```bash
python3 scripts/check_links.py . --files knowledge/app-store-review-guidelines/screenshots-accuracy.md knowledge/app-store-review-guidelines/metadata-age-rating.md knowledge/app-store-review-guidelines/other-platform-references.md references/apple/app-store-product-page.md
python3 scripts/check_transitions.py .
wc -l references/apple/app-store-review-guidelines.md
```

Expected: no findings; transitions clean (no `status:` changed); ASRG Reference still 98.

- [ ] **Step 9: Commit 2**

```bash
git add knowledge/app-store-review-guidelines references/apple/app-store-product-page.md knowledge/app-store-product-page/asset-content-restrictions.md skills/app-store-review-guidelines/SKILL.md skills/index.md docs/architecture/domain-map.md docs/adr/0002-app-store-product-page-scope.md CHANGELOG.md
git commit -m "$(cat <<'EOF'
feat: encode App Review 2.3.3 majority rule, 2.3.8, 2.3.10

screenshots-accuracy now requires more than half of each device's
screenshots to show the app in use, per App Review's new 2.3.3 page.
New metadata-age-rating (2.3.8) and other-platform-references (2.3.10).
Their URLs are indexed in the app-store-product-page Reference because
the App Review Guidelines Reference is at its 98-line limit (ADR-0002).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 10: Review, then ask the user before pushing / opening the PR.** Request review (superpowers:requesting-code-review), including a Level 4–5 read: does each rule say only what its source says? PR body ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

---

### Task 16: Release 2.5.0 (after the feature PR merges)

**Files:**
- Modify: `README.md`, `npx/README.md`, `npx/package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `CHANGELOG.md`

- [ ] **Step 1:** `git switch main && git pull && git switch -c chore/release-2.5.0`
- [ ] **Step 2:** `Version: 2.4.2` → `Version: 2.5.0` in `README.md` and `npx/README.md`; `"version": "2.4.2"` → `"version": "2.5.0"` in `npx/package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` (version field only — `npx/package.json` is touched under the six-file release rule; no `npm publish`).
- [ ] **Step 3:** `CHANGELOG.md`: rename `## [Unreleased]` content into `## [2.5.0] - <merge date>`, leaving an empty `## [Unreleased]` above it.
- [ ] **Step 4: Check all six match**

```bash
grep -h "^Version:" README.md npx/README.md; grep -h '"version"' npx/package.json .claude-plugin/plugin.json .codex-plugin/plugin.json; grep -m2 "^## \[" CHANGELOG.md
claude plugin validate .
```

Expected: six × `2.5.0`; plugin validate passes.

- [ ] **Step 5:** Commit `chore: release 2.5.0 — app-store-product-page domain` (with Co-Authored-By line); ask the user before pushing / opening the PR.

---

## Self-review (done at authoring)

- Decision coverage: 1→Tasks 1–11/12–15; 2→Skill Stop Conditions + map row; 3→KC Excluded lines; 4→Task 2 Rules 2, 3, 7; 5→Task 2 Rules 5–6; 6→Task 3 Rule 3 + Excluded; 7→Task 6 Intent; 8→Tasks 7–10 Excluded lines; 9→Tasks 12–14; 10→Tasks 1, 15 + ADR; 11→Task 11 Step 5; 12→Tasks 2–10 + Task 15 Step 2; 13→commits in Tasks 11, 15 + Task 16; 14→Task 1 Step 1, Task 3 Excluded.
- Ordering hazards handled: `related` edges to ASRG KCs added only in commit 2 (Task 15 Step 2); the ASRG Reference is never edited.
- Unverified inference from the research note (5244 x 2950 = universal asset) is explicitly not encoded (Task 4 Rule 6).
