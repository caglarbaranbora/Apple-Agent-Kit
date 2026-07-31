# App Store Review Guidelines Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `app-store-review-guidelines` domain — 1 Reference, 12 Knowledge Contracts, 1 native Skill — plus `domain-map.md`, `skills/index.md`, and `README.md` updates, per `docs/superpowers/specs/2026-07-31-app-store-review-guidelines-domain-design.md`.

**Architecture:** Mirrors the `human-interface-guidelines` domain exactly: one umbrella Reference file, one atomic Knowledge Contract per implementation rule under `knowledge/app-store-review-guidelines/`, one native Skill with keyword-clustered routing under `skills/app-store-review-guidelines/`. Every artifact validated with `scripts/validate_artifact.py` before commit.

**Tech Stack:** Markdown artifacts only. No code, no runtime. Validation via `python3 scripts/validate_artifact.py` and `python3 -m unittest tests/test_validate_artifact.py`.

---

## Content sourcing note

All rule text below is sourced from `https://developer.apple.com/app-store/review/guidelines/` (guideline sections 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2), `https://developer.apple.com/documentation/bundleresources/privacy_manifest_files`, and `https://developer.apple.com/app-store/app-privacy-details/`, fetched during brainstorming/planning. Each task embeds the exact file content to write — no paraphrasing needed at execution time.

---

### Task 1: Reference — app-store-review-guidelines.md

**Files:**
- Create: `references/apple/app-store-review-guidelines.md`

- [ ] **Step 1: Write the reference file**

```markdown
# App Store Review Guidelines

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/app-store/review/guidelines/

## Purpose

Reference index for Apple's App Store Review Guidelines — the subset of
sections most frequently responsible for real-world app rejections and
actionable from application code or App Store Connect metadata: App
Completeness (2.1), Accurate Metadata (2.3), In-App Purchase (3.1.1),
Minimum Functionality (4.2), Spam (4.3), and Privacy (5.1.1, 5.1.2). Safety,
most of Legal, and Design (4.0, owned by `human-interface-guidelines`) are
out of scope for this pass — see docs/architecture/domain-map.md.

## Primary Topics

- App Completeness
- Demo Account
- Screenshots Accuracy
- Description Accuracy
- Digital Goods In-App Purchase
- External Payment Links
- Restore Purchases
- Minimum Functionality
- Spam / Duplicate Apps
- Permission Usage Strings
- Privacy Manifest
- Privacy Nutrition Label

## Used By

- knowledge/app-store-review-guidelines/app-completeness.md ([[knowledge/app-store-review-guidelines/app-completeness]])
- knowledge/app-store-review-guidelines/demo-account.md ([[knowledge/app-store-review-guidelines/demo-account]])
- knowledge/app-store-review-guidelines/screenshots-accuracy.md ([[knowledge/app-store-review-guidelines/screenshots-accuracy]])
- knowledge/app-store-review-guidelines/description-accuracy.md ([[knowledge/app-store-review-guidelines/description-accuracy]])
- knowledge/app-store-review-guidelines/digital-goods-iap.md ([[knowledge/app-store-review-guidelines/digital-goods-iap]])
- knowledge/app-store-review-guidelines/external-payment-links.md ([[knowledge/app-store-review-guidelines/external-payment-links]])
- knowledge/app-store-review-guidelines/restore-purchases.md ([[knowledge/app-store-review-guidelines/restore-purchases]])
- knowledge/app-store-review-guidelines/minimum-functionality.md ([[knowledge/app-store-review-guidelines/minimum-functionality]])
- knowledge/app-store-review-guidelines/spam-duplicate-apps.md ([[knowledge/app-store-review-guidelines/spam-duplicate-apps]])
- knowledge/app-store-review-guidelines/permission-usage-strings.md ([[knowledge/app-store-review-guidelines/permission-usage-strings]])
- knowledge/app-store-review-guidelines/privacy-manifest.md ([[knowledge/app-store-review-guidelines/privacy-manifest]])
- knowledge/app-store-review-guidelines/privacy-nutrition-label.md ([[knowledge/app-store-review-guidelines/privacy-nutrition-label]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/app-store-review-guidelines.md --type reference`
Expected: `PASS: references/apple/app-store-review-guidelines.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/app-store-review-guidelines.md
git commit -m "docs: add App Store Review Guidelines reference"
```

---

### Task 2: Knowledge Contract — app-completeness

**Files:**
- Create: `knowledge/app-store-review-guidelines/app-completeness.md`

- [ ] **Step 1: Write the file**

```markdown
# App Completeness

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.app-completeness
type: knowledge
title: App Completeness
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requirements for submitting a final, fully tested, non-placeholder app build to App Review, including functional in-app purchase items at submission time.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - app-completeness
  - submission
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.demo-account
updated: 2026-07-31
```

## Intent

This contract defines what makes an app submission "complete" for App
Review purposes: no placeholder content, no on-device crashes, and fully
functional in-app purchase items at submission time (guideline 2.1).

## Scope

### Included

-   Prohibition on placeholder/temporary content in the submitted build
-   Prohibition on broken/non-functional URLs referenced by the app
-   On-device crash/stability testing before submission
-   Functional, reviewer-visible in-app purchase items at submission

### Excluded

-   Demo account / demo mode requirement for login-gated apps — see `demo-account`
-   In-app purchase implementation rules beyond submission-time visibility — see `digital-goods-iap`

## Rules

### Rule 1

Agents MUST NOT include placeholder text, empty websites, or temporary
content in the submitted build.

### Rule 2

Agents MUST test the app on-device for bugs and stability before
submission; App Review rejects binaries that crash or exhibit obvious
technical problems.

### Rule 3

Agents MUST ensure any in-app purchase items configured for the app are
complete, up-to-date, visible to the reviewer, and functional at
submission time. If a configured IAP item cannot be found or reviewed,
the review notes must explain why.

### Rule 4

Agents SHOULD ensure all URLs referenced by the app or its metadata are
fully functional, not broken or placeholder links.

## Compliant Example

-   ✓ Submitted build has all placeholder Lorem Ipsum content replaced with real copy, was tested on a real device with zero reproduced crashes, and its configured IAP items are purchasable in the reviewer's sandbox account. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ App ships with a "Coming Soon" placeholder screen in place of a promised feature. (Rule 1)
-   ✗ App crashes on first launch during reviewer testing. (Rule 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.1 App Completeness](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/app-completeness.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/app-completeness.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/app-completeness.md
git commit -m "docs: add app-completeness knowledge contract"
```

---

### Task 3: Knowledge Contract — demo-account

**Files:**
- Create: `knowledge/app-store-review-guidelines/demo-account.md`

- [ ] **Step 1: Write the file**

```markdown
# Demo Account

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.demo-account
type: knowledge
title: Demo Account
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement to provide App Review with working demo credentials or an Apple-approved built-in demo mode for any app that gates functionality behind login.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - demo-account
  - submission
  - login
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.app-completeness
updated: 2026-07-31
```

## Intent

This contract defines how an agent ensures App Review can actually reach
login-gated functionality: working demo credentials, or an
Apple-approved built-in demo mode as a substitute (guideline 2.1(a)).

## Scope

### Included

-   Demo account credentials in App Store Connect review notes
-   Backend/server-side availability of the demo account at submission time
-   Built-in demo mode as an Apple-approved substitute
-   Feature parity requirement for demo mode vs. real account

### Excluded

-   General build-completeness/crash requirements — see `app-completeness`

## Rules

### Rule 1

Agents MUST include demo account credentials in the App Store Connect
review notes if the app requires login to access reviewable
functionality.

### Rule 2

Agents MUST ensure the demo account's backend dependency is active and
reachable at submission time — a demo account that fails to
authenticate is treated as an incomplete submission.

### Rule 3

Agents MAY substitute a built-in demo mode for a demo account only when
a demo account cannot be provided for legal or security reasons, and
only with Apple's prior approval.

### Rule 4

Agents MUST ensure a substitute demo mode exhibits the app's full
features and functionality, not a reduced subset.

## Compliant Example

-   ✓ Review notes include a working username/password; reviewer logs in successfully and reaches gated content. (Rules 1, 2)

## Non-Compliant Example

-   ✗ Review notes contain no demo credentials for a login-gated app. (Rule 1)
-   ✗ The demo account was disabled after internal testing and returns invalid-credentials errors during review. (Rule 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.1 App Completeness](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/demo-account.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/demo-account.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/demo-account.md
git commit -m "docs: add demo-account knowledge contract"
```

---

### Task 4: Knowledge Contract — screenshots-accuracy

**Files:**
- Create: `knowledge/app-store-review-guidelines/screenshots-accuracy.md`

- [ ] **Step 1: Write the file**

```markdown
# Screenshots Accuracy

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.screenshots-accuracy
type: knowledge
title: Screenshots Accuracy
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines what App Store screenshots and preview videos must and must not depict, per guideline 2.3.3 and 2.3.4.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - screenshots
  - metadata
  - previews
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.description-accuracy
updated: 2026-07-31
```

## Intent

This contract defines what App Store screenshots and App Preview videos
must show: the app in actual use, not marketing art or unrelated
footage (guideline 2.3.3, 2.3.4).

## Scope

### Included

-   Screenshot content requirements (in-app-use vs. title/login/splash art)
-   Permitted overlays on screenshots
-   App Preview video source-material restrictions
-   Permitted narration/overlays on preview videos

### Excluded

-   App description/keyword accuracy — see `description-accuracy`

## Rules

### Rule 1

Agents MUST ensure screenshots show the app in actual use — not merely
title art, a login page, or a splash screen.

### Rule 2

Agents MAY include text/image overlays on screenshots that demonstrate
input mechanisms (e.g., an animated touch point, Apple Pencil) or
extended on-device functionality (e.g., Touch Bar).

### Rule 3

Agents MUST limit App Preview videos to screen captures of the app
itself; Stickers/iMessage extensions may additionally show the Messages
app experience.

### Rule 4

Agents MAY add narration or textual/video overlays to preview videos to
clarify content not obvious from the video alone.

## Compliant Example

-   ✓ Screenshots show real in-app screens with actual content, with one overlay demonstrating a swipe gesture. (Rules 1, 2)

## Non-Compliant Example

-   ✗ All screenshots are variations of the app's logo splash screen. (Rule 1)
-   ✗ Preview video is a marketing reel with stock footage unrelated to the app UI. (Rule 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3 Accurate Metadata](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/screenshots-accuracy.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/screenshots-accuracy.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/screenshots-accuracy.md
git commit -m "docs: add screenshots-accuracy knowledge contract"
```

---

### Task 5: Knowledge Contract — description-accuracy

**Files:**
- Create: `knowledge/app-store-review-guidelines/description-accuracy.md`

- [ ] **Step 1: Write the file**

```markdown
# Description Accuracy

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.description-accuracy
type: knowledge
title: Description Accuracy
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requirements for accurate, non-misleading App Store descriptions and keywords, and prohibits hidden/undocumented functionality, per guidelines 2.3, 2.3.1(a), and 2.3.7.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - description
  - metadata
  - keywords
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.screenshots-accuracy
updated: 2026-07-31
```

## Intent

This contract defines the accuracy bar for an app's textual App Store
metadata: no hidden features, no misleading marketing, and no
keyword-stuffing (guideline 2.3, 2.3.1(a), 2.3.7).

## Scope

### Included

-   Prohibition on hidden/dormant/undocumented app functionality
-   Review-notes specificity requirement for new features
-   Prohibition on misleading marketing claims
-   App name/keyword accuracy and length limits

### Excluded

-   Screenshot/preview content accuracy — see `screenshots-accuracy`

## Rules

### Rule 1

Agents MUST NOT ship hidden, dormant, or undocumented features — all
functionality must be clear to end users and to App Review.

### Rule 2

Agents MUST describe all new features, functionality, and product
changes with specificity in the App Store Connect "Notes for Review"
field — generic descriptions are rejected.

### Rule 3

Agents MUST NOT market the app in a misleading way, such as promoting
functionality the app does not actually provide, or a false price.

### Rule 4

Agents MUST choose a unique app name of 30 characters or fewer, and
accurate keywords; agents MUST NOT pack metadata with trademarked
terms, competitor app names, pricing information, or irrelevant phrases
to game search ranking.

## Compliant Example

-   ✓ App description matches shipped functionality exactly; review notes explain a newly added feature in specific, testable terms. (Rules 1, 2)

## Non-Compliant Example

-   ✗ App description advertises "AI-powered virus scanning" that the app doesn't perform. (Rule 3)
-   ✗ Keyword field is stuffed with competitor brand names. (Rule 4)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.3 Accurate Metadata](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/description-accuracy.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/description-accuracy.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/description-accuracy.md
git commit -m "docs: add description-accuracy knowledge contract"
```

---

### Task 6: Knowledge Contract — digital-goods-iap

**Files:**
- Create: `knowledge/app-store-review-guidelines/digital-goods-iap.md`

- [ ] **Step 1: Write the file**

```markdown
# Digital Goods In-App Purchase

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.digital-goods-iap
type: knowledge
title: Digital Goods In-App Purchase
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement to use Apple's in-app purchase system to unlock digital content or functionality, per guideline 3.1.1.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - in-app-purchase
  - monetization
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.external-payment-links
  - knowledge.app-store-review-guidelines.restore-purchases
updated: 2026-07-31
```

## Intent

This contract defines when an agent must use StoreKit in-app purchase
to unlock digital content or functionality, and which alternative
unlock mechanisms are explicitly disallowed (guideline 3.1.1).

## Scope

### Included

-   Requirement to use IAP for unlocking features/content/currency
-   Prohibited alternative unlock mechanisms
-   Permitted IAP-based tipping
-   Loot-box odds disclosure requirement

### Excluded

-   External payment link/button restrictions — see `external-payment-links`
-   Restore-purchases mechanism requirement — see `restore-purchases`

## Rules

### Rule 1

Agents MUST use in-app purchase (StoreKit) to unlock any feature,
functionality, subscription, in-game currency, level, or premium
content within the app.

### Rule 2

Agents MUST NOT implement an app-owned mechanism to unlock
content/functionality instead of IAP — license keys, AR markers, QR
codes, cryptocurrency, and cryptocurrency wallets are explicitly
disallowed as unlock mechanisms.

### Rule 3

Agents MAY use IAP currencies to let users "tip" the developer or a
digital content provider inside the app.

### Rule 4

Agents MUST disclose the odds of receiving each item type, before
purchase, for any app offering loot boxes or other randomized
virtual-item purchases.

## Compliant Example

-   ✓ Premium tier is unlocked via a StoreKit non-consumable purchase. (Rule 1)

## Non-Compliant Example

-   ✗ App sells a "premium unlock" QR code on the developer's website that users scan in-app to unlock paid features, bypassing IAP. (Rule 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 3.1.1 In-App Purchase](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/digital-goods-iap.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/digital-goods-iap.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/digital-goods-iap.md
git commit -m "docs: add digital-goods-iap knowledge contract"
```

---

### Task 7: Knowledge Contract — external-payment-links

**Files:**
- Create: `knowledge/app-store-review-guidelines/external-payment-links.md`

- [ ] **Step 1: Write the file**

```markdown
# External Payment Links

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.external-payment-links
type: knowledge
title: External Payment Links
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the prohibition on in-app buttons, links, or calls to action that direct users to purchase digital goods outside of in-app purchase, per guideline 3.1.1(a).
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - in-app-purchase
  - external-links
  - monetization
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.digital-goods-iap
updated: 2026-07-31
```

## Intent

This contract defines when an app's UI may or may not include a call
to action directing users to purchase digital goods outside of IAP
(guideline 3.1.1(a)), and the narrower US-storefront exception.

## Scope

### Included

-   Prohibition on in-app external-purchase calls to action (non-US storefronts)
-   US storefront External Purchase Link Entitlement exception
-   Outside-app communications about alternative purchasing methods

### Excluded

-   Underlying IAP-usage requirement itself — see `digital-goods-iap`

## Rules

### Rule 1

Agents MUST NOT include buttons, external links, or other calls to
action in the app or its metadata that direct customers to a purchasing
mechanism other than in-app purchase, for storefronts outside the
United States.

### Rule 2

Agents MAY include such external purchase links only on the United
States storefront, and only through Apple's StoreKit External Purchase
Link Entitlement where applicable.

### Rule 3

Agents MAY send communications outside the app (e.g., email, SMS) to
the existing user base about alternative purchasing methods — this is
distinct from an in-app call to action and is not restricted by Rule 1.

## Compliant Example

-   ✓ iOS app sold globally has no "Buy on our website" button in its UI; the developer emails existing subscribers about a website discount. (Rules 1, 3)

## Non-Compliant Example

-   ✗ App shown on a non-US storefront includes an in-app "Subscribe on our site and save 10%" button linking out to a web checkout. (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 3.1.1 In-App Purchase](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/external-payment-links.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/external-payment-links.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/external-payment-links.md
git commit -m "docs: add external-payment-links knowledge contract"
```

---

### Task 8: Knowledge Contract — restore-purchases

**Files:**
- Create: `knowledge/app-store-review-guidelines/restore-purchases.md`

- [ ] **Step 1: Write the file**

```markdown
# Restore Purchases

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.restore-purchases
type: knowledge
title: Restore Purchases
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement to provide a restore mechanism for restorable in-app purchases, and the non-expiration rule for purchased credits/currencies, per guideline 3.1.1.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - in-app-purchase
  - restore
  - monetization
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.digital-goods-iap
updated: 2026-07-31
```

## Intent

This contract defines how an agent must let users recover previously
purchased non-consumable/subscription IAP items, and the rule against
letting purchased in-game currency expire (guideline 3.1.1).

## Scope

### Included

-   Restore-mechanism requirement for non-consumable/subscription IAP
-   Non-expiration rule for purchased credits/currencies
-   Discoverability of the restore action

### Excluded

-   Initial purchase/unlock requirement itself — see `digital-goods-iap`

## Rules

### Rule 1

Agents MUST implement a restore-purchases mechanism for any
non-consumable or auto-renewable/non-renewing subscription IAP so users
can recover purchases after reinstall or a device change.

### Rule 2

Agents MUST NOT cause credits or in-game currencies purchased via IAP
to expire.

### Rule 3

Agents SHOULD expose the restore action from a discoverable location in
the app's purchase/settings UI, not only triggered implicitly on
launch.

## Compliant Example

-   ✓ Settings screen has a "Restore Purchases" button that calls the platform's restore-completed-transactions API and re-unlocks owned non-consumables. (Rules 1, 3)

## Non-Compliant Example

-   ✗ App offers a non-consumable "remove ads" purchase with no way to restore it after reinstalling the app. (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 3.1.1 In-App Purchase](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/restore-purchases.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/restore-purchases.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/restore-purchases.md
git commit -m "docs: add restore-purchases knowledge contract"
```

---

### Task 9: Knowledge Contract — minimum-functionality

**Files:**
- Create: `knowledge/app-store-review-guidelines/minimum-functionality.md`

- [ ] **Step 1: Write the file**

```markdown
# Minimum Functionality

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.minimum-functionality
type: knowledge
title: Minimum Functionality
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement that an app provide functionality, content, and UI beyond a repackaged website or template-generated wrapper, per guideline 4.2.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - minimum-functionality
  - quality
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.spam-duplicate-apps
updated: 2026-07-31
```

## Intent

This contract defines the "app-like" bar an agent must clear: real
utility or lasting value beyond a repackaged website, and a prohibition
on unmodified template-generated apps (guideline 4.2, 4.2.2, 4.2.6).

## Scope

### Included

-   Requirement for native functionality beyond a website wrapper
-   Prohibition on marketing/aggregator-only apps
-   Prohibition on unmodified commercialized-template submissions
-   Aggregated "picker"-model exception for template providers

### Excluded

-   Duplicate/near-identical app submissions — see `spam-duplicate-apps`

## Rules

### Rule 1

Agents MUST include features, content, or UI that elevate the app
beyond a repackaged website; App Review rejects apps that are not
"app-like."

### Rule 2

Agents MUST ensure the app provides lasting entertainment value or
adequate utility — a thin marketing/advertising/content-aggregation
wrapper is not acceptable.

### Rule 3

Agents MUST NOT generate the app from a commercialized app-template or
app-generation service unless it is submitted directly by the content
provider itself; template-generation services must not submit apps on
behalf of their clients.

### Rule 4

Agents MAY use an aggregated/"picker" binary model (one binary hosting
many clients' customized content, e.g. a restaurant-finder app with
per-restaurant entries) as an acceptable alternative to per-client app
submissions.

## Compliant Example

-   ✓ App wraps a website's content but adds a native offline mode, push notifications, and platform-specific UI not present on the web. (Rule 1)

## Non-Compliant Example

-   ✗ App is a WebView pointed at the company's marketing site with no native functionality added. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 4.2 Minimum Functionality](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/minimum-functionality.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/minimum-functionality.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/minimum-functionality.md
git commit -m "docs: add minimum-functionality knowledge contract"
```

---

### Task 10: Knowledge Contract — spam-duplicate-apps

**Files:**
- Create: `knowledge/app-store-review-guidelines/spam-duplicate-apps.md`

- [ ] **Step 1: Write the file**

```markdown
# Spam / Duplicate Apps

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.spam-duplicate-apps
type: knowledge
title: Spam / Duplicate Apps
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the prohibition on submitting multiple near-identical apps (per-location/per-team variants) or apps indistinguishable from existing App Store listings, per guideline 4.3.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - spam
  - duplicate-apps
  - quality
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.minimum-functionality
updated: 2026-07-31
```

## Intent

This contract defines when a family of near-identical apps must be
consolidated into a single app with in-app variation instead of
separate Bundle IDs, and the bar for originality versus existing App
Store listings (guideline 4.3(a), 4.3(b)).

## Scope

### Included

-   Prohibition on multiple Bundle IDs for one underlying app
-   IAP-based variation as the preferred alternative
-   Originality bar relative to existing App Store listings

### Excluded

-   General "app-like" minimum-functionality bar — see `minimum-functionality`

## Rules

### Rule 1

Agents MUST NOT create multiple Bundle IDs of the same app for what
should be a single app with variant data (e.g., a separate app per city
instead of one app with in-app search/selection).

### Rule 2

Agents SHOULD use in-app purchase to deliver location/team/university-
specific variations from a single app binary, rather than submitting a
separate app per variation.

### Rule 3

Agents MUST NOT submit an app that is indistinguishable from apps
already widely available on the App Store without offering a
meaningfully different or improved experience.

## Compliant Example

-   ✓ A single "City Guides" app lets users search/select any city inside the app via IAP-unlocked city packs. (Rules 1, 2)

## Non-Compliant Example

-   ✗ Developer submits "City Guide: Paris", "City Guide: Berlin", and "City Guide: Tokyo" as separate apps built from a shared codebase with only the city name changed. (Rule 1)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 4.3 Spam](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/spam-duplicate-apps.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/spam-duplicate-apps.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/spam-duplicate-apps.md
git commit -m "docs: add spam-duplicate-apps knowledge contract"
```

---

### Task 11: Knowledge Contract — permission-usage-strings

**Files:**
- Create: `knowledge/app-store-review-guidelines/permission-usage-strings.md`

- [ ] **Step 1: Write the file**

```markdown
# Permission Usage Strings

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.permission-usage-strings
type: knowledge
title: Permission Usage Strings
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement for accurate, specific Info.plist usage-description strings and informed user consent before collecting user or usage data, per guideline 5.1.1(ii) and 5.1.1(iv).
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - privacy
  - permissions
  - info-plist
references:
  - https://developer.apple.com/app-store/review/guidelines/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-manifest
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
updated: 2026-07-31
```

## Intent

This contract defines how an agent writes `Info.plist` permission-usage
strings and gates data-dependent functionality: specific, accurate
strings, informed consent, and a fallback path when a permission is
declined (guideline 5.1.1(ii), 5.1.1(iv)).

## Scope

### Included

-   Consent requirement before collecting user/usage data
-   `Info.plist` usage-description string accuracy
-   Prohibition on gating unrelated paid functionality behind a permission
-   Prohibition on bundling unrelated permission requests
-   Fallback-path expectation when a permission is declined
-   Consent-withdrawal accessibility

### Excluded

-   Privacy manifest (`PrivacyInfo.xcprivacy`) declarations — see `privacy-manifest`
-   App Store Connect privacy label accuracy — see `privacy-nutrition-label`

## Rules

### Rule 1

Agents MUST secure user consent before collecting user or usage data,
even data considered anonymous at or immediately after collection.

### Rule 2

Agents MUST write each `Info.plist` usage-description string (e.g.
`NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`) to
clearly and completely describe the actual use of the requested data —
generic or vague strings are a rejection risk.

### Rule 3

Agents MUST NOT make paid functionality dependent on a user granting a
data-access permission that isn't required for that functionality.

### Rule 4

Agents MUST NOT request an unrelated permission as a prerequisite for
an unrelated feature (e.g., requiring microphone access before allowing
a photo upload).

### Rule 5

Agents SHOULD offer an alternative path when a user declines a
permission (e.g., manual address entry when Location is declined)
rather than blocking the feature entirely.

### Rule 6

Agents MUST provide an easily accessible, understandable way for the
user to withdraw previously granted consent.

## Compliant Example

-   ✓ `NSContactsUsageDescription` reads "Used to let you invite friends already in your contacts — we don't upload or store your contacts."; the invite feature still works via manual entry if Contacts is declined. (Rules 2, 5)

## Non-Compliant Example

-   ✗ `NSCameraUsageDescription` reads "This app needs camera access." with no explanation of use. (Rule 2)
-   ✗ App blocks all functionality until Contacts permission is granted, even though contacts aren't used anywhere else in the app. (Rule 4)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 5.1.1 Data Collection and Storage](https://developer.apple.com/app-store/review/guidelines/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/permission-usage-strings.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/permission-usage-strings.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/permission-usage-strings.md
git commit -m "docs: add permission-usage-strings knowledge contract"
```

---

### Task 12: Knowledge Contract — privacy-manifest

**Files:**
- Create: `knowledge/app-store-review-guidelines/privacy-manifest.md`

- [ ] **Step 1: Write the file**

```markdown
# Privacy Manifest

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.privacy-manifest
type: knowledge
title: Privacy Manifest
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the requirement to ship an accurate PrivacyInfo.xcprivacy privacy manifest declaring data collection and required-reason API usage, and the App Store Connect rejection risk of a missing or incomplete manifest.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - privacy
  - privacy-manifest
  - xcprivacy
references:
  - https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
  - knowledge.app-store-review-guidelines.permission-usage-strings
updated: 2026-07-31
```

## Intent

This contract defines what an agent must declare in a
`PrivacyInfo.xcprivacy` file so App Store Connect accepts the binary:
collected data types, required-reason API justifications, and
third-party SDK coverage.

## Scope

### Included

-   `PrivacyInfo.xcprivacy` file requirement and applicable OS versions
-   Collected-data-type declarations
-   Required-reason API justification-code declarations
-   Third-party SDK privacy-manifest coverage
-   Manifest-update obligation on functionality change

### Excluded

-   `Info.plist` runtime permission-prompt strings — see `permission-usage-strings`
-   App Store Connect privacy questionnaire ("nutrition label") — see `privacy-nutrition-label`

## Rules

### Rule 1

Agents MUST include a `PrivacyInfo.xcprivacy` file in the app bundle
for any app or SDK targeting iOS 17+, iPadOS 17+, tvOS 17+, or
watchOS 10+.

### Rule 2

Agents MUST declare every collected user-data category (e.g. contacts,
location, health, financial info, browsing/search history, purchase
history, user IDs) in `NSPrivacyCollectedDataTypes`.

### Rule 3

Agents MUST declare an approved `NSPrivacyAccessedAPITypeReasons`
justification code for every use of a required-reason API (e.g.
`NSUserDefaults`, `FileProvider`, `URLSessionConfiguration`,
`NSFileManager`) — custom or unlisted justifications are rejected.

### Rule 4

Agents MUST account for third-party SDK dependencies' data use in the
app's own manifest when a bundled SDK does not ship its own privacy
manifest.

### Rule 5

Agents MUST update the manifest whenever app functionality that changes
data collection or required-reason API usage changes — a stale manifest
is treated as inaccurate, not merely outdated.

## Compliant Example

-   ✓ App bundles `PrivacyInfo.xcprivacy` declaring `NSUserDefaults` access with an approved reason code, and lists Location as a collected data type matching actual behavior. (Rules 1, 2, 3)

## Non-Compliant Example

-   ✗ App uses `UserDefaults` but ships no `PrivacyInfo.xcprivacy` file — App Store Connect rejects the binary at upload. (Rules 1, 3)

## Dependencies

None.

## References

-   [Apple Developer — Privacy Manifest Files](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/privacy-manifest.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/privacy-manifest.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/privacy-manifest.md
git commit -m "docs: add privacy-manifest knowledge contract"
```

---

### Task 13: Knowledge Contract — privacy-nutrition-label

**Files:**
- Create: `knowledge/app-store-review-guidelines/privacy-nutrition-label.md`

- [ ] **Step 1: Write the file**

```markdown
# Privacy Nutrition Label

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.privacy-nutrition-label
type: knowledge
title: Privacy Nutrition Label
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the App Store Connect "App Privacy" nutrition-label disclosure requirements — declared data types, identity linkage, and tracking use — and the accuracy bar relative to actual app behavior, per guideline 5.1.1 and 5.1.2.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - privacy
  - nutrition-label
  - app-privacy-details
references:
  - https://developer.apple.com/app-store/app-privacy-details/
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-manifest
  - knowledge.app-store-review-guidelines.permission-usage-strings
updated: 2026-07-31
```

## Intent

This contract defines how an agent fills out the App Store Connect
"App Privacy" questionnaire accurately: which data types to declare,
how to mark identity linkage and tracking use, and when a data type may
be omitted (guideline 5.1.1, 5.1.2).

## Scope

### Included

-   Data-type disclosure scope (first-party and third-party SDK collection)
-   Identity-linkage marking
-   Tracking-use marking and its relationship to App Tracking Transparency
-   Data-use-purpose accuracy and update obligation
-   Conditions for optional (omittable) disclosure

### Excluded

-   `PrivacyInfo.xcprivacy` bundle-level declarations — see `privacy-manifest`
-   Runtime `Info.plist` permission-prompt strings — see `permission-usage-strings`

## Rules

### Rule 1

Agents MUST declare, in App Store Connect, every data type collected by
the app itself or by any bundled third-party SDK/partner (analytics, ad
networks) — not only first-party collection.

### Rule 2

Agents MUST correctly mark each declared data type as linked or not
linked to user identity (account, device, or other identifying
detail).

### Rule 3

Agents MUST correctly mark whether each data type is used for tracking
(linking app data with third-party data for targeted ads/measurement,
or sharing with data brokers) — tracking additionally requires App
Tracking Transparency permission.

### Rule 4

Agents MUST keep declared data uses (third-party advertising, developer
marketing, analytics, product personalization, app functionality,
other) in sync with actual app behavior, updating App Store Connect
answers whenever practices change.

### Rule 5

Agents MAY omit a data type from disclosure only if it meets every
"optional disclosure" condition simultaneously: not used for tracking,
not used for third-party/developer advertising or "Other Purposes,"
collected only in an optional non-primary flow, and explicitly
user-provided with disclosed consent each time.

## Compliant Example

-   ✓ Privacy label declares "Precise Location — linked to identity — used for App Functionality," matching the app's actual location-based feature. (Rules 1, 2, 4)

## Non-Compliant Example

-   ✗ App's privacy label declares "Data Not Collected" while a bundled analytics SDK silently transmits device identifiers to a third-party ad network. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/app-store-review-guidelines/privacy-nutrition-label.md --type knowledge`
Expected: `PASS: knowledge/app-store-review-guidelines/privacy-nutrition-label.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/app-store-review-guidelines/privacy-nutrition-label.md
git commit -m "docs: add privacy-nutrition-label knowledge contract"
```

---

### Task 14: Skill — app-store-review-guidelines/SKILL.md

**Files:**
- Create: `skills/app-store-review-guidelines/SKILL.md`

- [ ] **Step 1: Write the file**

```markdown
---
name: app-store-review-guidelines
description: Route App Store submission-compliance tasks to the correct Knowledge Contracts — app completeness, demo accounts, screenshot/description accuracy, in-app purchase requirements, external payment link restrictions, restore purchases, minimum functionality, spam/duplicate-app avoidance, permission usage strings, privacy manifest, and privacy nutrition label accuracy. Use when preparing an app for App Store submission, implementing in-app purchase, writing Info.plist usage descriptions, building a PrivacyInfo.xcprivacy manifest, filling out the App Store Connect privacy questionnaire, or reviewing App Store metadata before submitting. Triggers on App Store review, App Review guidelines, app rejected, in-app purchase, IAP, restore purchases, demo account, screenshot requirements, app description, privacy manifest, PrivacyInfo.xcprivacy, privacy nutrition label, App Store Connect privacy, spam app, duplicate app, minimum functionality, NSUsageDescription, permission usage string.
id: skill.app-store-review-guidelines.submission
title: App Store Review Guidelines — Submission Compliance
version: 0.1.0
status: Draft
artifact_type: skill
domain: App Store Review Guidelines
routes: [knowledge.app-store-review-guidelines.app-completeness, knowledge.app-store-review-guidelines.demo-account, knowledge.app-store-review-guidelines.screenshots-accuracy, knowledge.app-store-review-guidelines.description-accuracy, knowledge.app-store-review-guidelines.digital-goods-iap, knowledge.app-store-review-guidelines.external-payment-links, knowledge.app-store-review-guidelines.restore-purchases, knowledge.app-store-review-guidelines.minimum-functionality, knowledge.app-store-review-guidelines.spam-duplicate-apps, knowledge.app-store-review-guidelines.permission-usage-strings, knowledge.app-store-review-guidelines.privacy-manifest, knowledge.app-store-review-guidelines.privacy-nutrition-label]
related: []
last_updated: 2026-07-31
---

# App Store Review Guidelines — Submission Compliance Skill

## Purpose

Route App Store submission-compliance tasks to the minimum required
App Store Review Guidelines Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-store-review-guidelines/.

-   Submission completeness -> app-completeness.md, demo-account.md
-   Metadata accuracy -> screenshots-accuracy.md, description-accuracy.md
-   In-app purchase -> digital-goods-iap.md, external-payment-links.md, restore-purchases.md
-   App value & originality -> minimum-functionality.md, spam-duplicate-apps.md
-   Privacy compliance -> permission-usage-strings.md, privacy-manifest.md, privacy-nutrition-label.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-store-review-guidelines/ — do not guess or
fall back to general knowledge. Safety, most of Legal, Design (4.0,
owned by `human-interface-guidelines`), and Guideline 4.8 Sign in with
Apple are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/app-store-review-guidelines/SKILL.md --type skill`
Expected: `PASS: skills/app-store-review-guidelines/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/app-store-review-guidelines/SKILL.md
git commit -m "feat: add app-store-review-guidelines native skill"
```

---

### Task 15: Update skills/index.md

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a Discovery Rules row**

In `skills/index.md`, find this exact table row block (currently the last
row of the Discovery Rules table):

```
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |
```

Replace it with (adds a new row immediately after):

```
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |
| App Store submission, App Review rejection, in-app purchase, IAP, restore purchases, demo account, screenshot requirements, app description accuracy, privacy manifest, PrivacyInfo.xcprivacy, privacy nutrition label, spam app, duplicate app, minimum functionality, permission usage string | skills/app-store-review-guidelines/SKILL.md |
```

- [ ] **Step 2: Verify the file still parses as valid markdown**

Run: `python3 -c "import pathlib; print(len(pathlib.Path('skills/index.md').read_text().splitlines()))"`
Expected: prints a line count greater than the pre-edit count (sanity check the write succeeded; `skills/index.md` has no `validate_artifact.py` type of its own).

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: register app-store-review-guidelines skill in skills index"
```

---

### Task 16: Update domain-map.md

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the Completed line in Build Order**

Find:

```
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt).
```

Replace with:

```
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt).
```

- [ ] **Step 2: Update the Tier 1 table row's Initial Scope cell**

Find:

```
| App Store Review Guidelines | app-store-review-guidelines | Review, metadata, distribution rules | App Store submission, metadata, and distribution compliance rules |
```

Replace with:

```
| App Store Review Guidelines | app-store-review-guidelines | 2.1 App Completeness, 2.3 Accurate Metadata, 3.1.1 In-App Purchase, 4.2 Minimum Functionality, 4.3 Spam/Duplicate, 5.1.1/5.1.2 Privacy (data collection & sharing). Safety, most of Legal, and Design 4.0 (owned by human-interface-guidelines) out of scope — see Cross-Domain Notes. | App Store submission, metadata, and distribution compliance rules |
```

- [ ] **Step 3: Add a new Cross-Domain Notes entry**

Find the last bullet of the Cross-Domain Notes section:

```
- `human-interface-guidelines` (`sf-symbols` Foundations topic) and the future `sf-symbols` domain (Tier 1, unbuilt) overlap: HIG's angle is symbol selection/composition in a design, the dedicated domain's angle is API usage and rendering modes. Boundary not yet resolved — decide when `sf-symbols` is built.
```

Replace with (adds a new bullet immediately after):

```
- `human-interface-guidelines` (`sf-symbols` Foundations topic) and the future `sf-symbols` domain (Tier 1, unbuilt) overlap: HIG's angle is symbol selection/composition in a design, the dedicated domain's angle is API usage and rendering modes. Boundary not yet resolved — decide when `sf-symbols` is built.
- `app-store-review-guidelines` (`privacy-manifest`/`privacy-nutrition-label` topics) and the future `privacy` domain (Tier 2, unbuilt) overlap: this domain's angle is review consequence (submission gets rejected if the manifest/label is missing or inaccurate), the future `privacy` domain's angle is correct implementation (how to write the manifest and disclosures correctly). Boundary not yet resolved — decide when `privacy` is built.
```

- [ ] **Step 4: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: mark app-store-review-guidelines v1 complete, add privacy cross-domain note"
```

---

### Task 17: Update README.md (Skills + What's New)

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a Skills bullet**

Find this exact block (the end of the `## Skills` section, immediately
before the closing routing-tables line):

```
- **`human-interface-guidelines`** — Routes iOS/iPadOS visual design tasks (layout, color, typography, dark mode, materials, motion, icons, branding, accessibility-design, privacy UI, RTL) to HIG Foundations Knowledge Contracts.
  Example: `"check this screen's layout against HIG"` → `layout.md` (+ `right-to-left.md` if relevant)
  Example: `"does my dark mode palette meet contrast guidance"` → `dark-mode.md`, `color.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```
- **`human-interface-guidelines`** — Routes iOS/iPadOS visual design tasks (layout, color, typography, dark mode, materials, motion, icons, branding, accessibility-design, privacy UI, RTL) to HIG Foundations Knowledge Contracts.
  Example: `"check this screen's layout against HIG"` → `layout.md` (+ `right-to-left.md` if relevant)
  Example: `"does my dark mode palette meet contrast guidance"` → `dark-mode.md`, `color.md`

- **`app-store-review-guidelines`** — Routes App Store submission-compliance tasks (app completeness, metadata accuracy, in-app purchase, spam/duplicate-app avoidance, privacy manifest and nutrition label accuracy) to App Store Review Guidelines Knowledge Contracts.
  Example: `"why would this in-app subscription get rejected"` → `digital-goods-iap.md`, `restore-purchases.md`
  Example: `"what needs to go in my PrivacyInfo.xcprivacy"` → `privacy-manifest.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a What's New line**

Find:

```
## What's New

- 2026-07-31 — Added `human-interface-guidelines` Skill (Foundations: layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL) — 15 Knowledge Contracts.
```

Replace with:

```
## What's New

- 2026-07-31 — Added `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contracts.
- 2026-07-31 — Added `human-interface-guidelines` Skill (Foundations: layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL) — 15 Knowledge Contracts.
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add app-store-review-guidelines to README Skills + What's New"
```

---

### Task 18: Full validation pass

**Files:** None created/modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/app-store-review-guidelines.md --type reference
for f in knowledge/app-store-review-guidelines/*.md; do
  python3 scripts/validate_artifact.py "$f" --type knowledge
done
python3 scripts/validate_artifact.py skills/app-store-review-guidelines/SKILL.md --type skill
```
Expected: `PASS` for all 14 invocations (1 reference + 12 knowledge + 1 skill).

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all 16 existing tests still `ok` (no regressions — this task adds no new validator code, so the test count doesn't change).

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: confirms `skills/app-store-review-guidelines/SKILL.md` is discovered alongside the existing skills, no errors.

- [ ] **Step 4: Confirm no stray files**

Run: `git status --short`
Expected: empty (everything from Tasks 1-17 already committed).
```
