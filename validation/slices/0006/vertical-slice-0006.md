# Vertical Slice #0006 — App Store Submission

Date: 2026-08-08

## Objective

The last untested Workflow, and the control for slice #0005. Every slice so far has
found something; a suite that only ever reports defects cannot distinguish a seam that
is broken from a seam nobody looked at hard enough.

## Scope

Task:

> Submit the app. It bundles a third-party analytics SDK and offers Sign in with
> Google.

Chosen because it lands on the seam `domain-map.md` calls "a clean handoff, not an
angle-split" — the two privacy disclosure surfaces — and because it makes two Skills
answer about the same third-party SDK from different sides.

## Observed Routing

Workflows table matched; `workflows/app-store-submission/WORKFLOW.md` sequenced three
Skills, cheapest-check-first.

| Step | Skill | Reached |
|---|---|---|
| 1 | `app-store-review-guidelines` | `login-services-equivalent-option` (4.8), `privacy-manifest`, `privacy-nutrition-label` |
| 2 | `privacy` | `manifest-file-structure-and-scope`, `collected-data-types-declaration`, `tracking-domains-and-third-party-sdk-signatures`, `required-reason-api-declarations` |
| 3 | `xcode` | signing, entitlements, archive, export |

## The seam under test

`app-store-review-guidelines`' `privacy-nutrition-label` (the App Store Connect web
form) and `privacy`'s `collected-data-types-declaration` (the `PrivacyInfo.xcprivacy`
file) ask similar substantive questions about the same data. The failure mode would be
either domain answering for the other, or neither telling the agent the two surfaces
are distinct.

Neither happens:

- Each names the other in `related:`, in both directions.
- Each Excluded list names the other surface explicitly —
  `collected-data-types-declaration` excludes "App Store Connect 'App Privacy'
  nutrition-label questionnaire (the web-form disclosure)", and `privacy-manifest`
  excludes the questionnaire in the same terms.
- The aggregation instrument is named rather than left implicit:
  `manifest-file-structure-and-scope` directs the agent to Xcode's archive-based
  Privacy Report, which "aggregates the app's manifest with every linked third-party
  SDK's manifest and is organized like the App Store Connect Privacy Nutrition Label"
  — and forbids fabricating a summary instead.
- Where the two genuinely diverge, the divergence is owned. `privacy-nutrition-label`
  Rule 5 permits omitting a data type from the web-form disclosure under four
  simultaneous conditions; the manifest has no such carve-out. That asymmetry belongs
  to the disclosure surface that has it, and neither Contract implies otherwise.

The third-party SDK is handled from both sides without overlap:
`privacy-nutrition-label` Rule 1 makes the developer answer for the SDK's collection,
`tracking-domains-and-third-party-sdk-signatures` covers the SDK's own manifest and
signature. Two different obligations about one SDK, one owner each.

## Results

| Level 5 check | Result |
|---|---|
| Routing succeeds from task to Knowledge without repository search | **PASS** |
| The routed Knowledge is sufficient to complete the task | **PASS** |
| Context is minimized | **PASS** — 3 Skills, no Contract loaded that the task did not need |
| Architecture behaves as specified | **PASS** |

## Result

Overall Status: **PASS — no findings**

The gate-before-archive ordering does what it claims: steps 1 and 2 both complete
before step 3 produces anything, so every finding costs a re-read rather than a
rebuild. The privacy seam is the cleanest cross-domain boundary examined by any slice
so far, and it is clean for a reason worth naming — `domain-map.md` classified it as a
handoff rather than an angle-split *before* either domain was written, and both
Contracts were authored to that classification.

FINDINGS.md records the negative result.
