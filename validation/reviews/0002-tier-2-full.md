# Level 4 Review #0002 — Tier 2, unsampled L4.1/L4.4, plus Skill routing content

Date: 2026-08-23
Corpus: 78 Knowledge Contracts and 17 Skills across the 17 Tier 2 domains.

## Why

Review #0001 covered L4.2/L4.3 (duplication, coupling) completely by construction —
both checks are inherently bounded to symbols cited in 2+ domains, and #0001 computed
and read that entire set (97 multi-domain symbols, 88 touching Tier 2, Swift-vocabulary
noise discarded). But two of its other checks were not exhaustive:

- **L4.1 (atomicity)** was explicitly a sample. The atomicity heuristic flagged 131 of
  258 Contracts repository-wide; #0001 read a sample of those and rejected the
  heuristic as noisy, but never read the full 131, let alone all 78 Tier 2 Contracts.
- **L4.4 (cross-reference truth)** was checked only mechanically — Bound A confirmed
  every `knowledge.x.y` Rule N citation *resolves* (0 dangling references), which is a
  Level 2 concern. Nobody had opened every citation target and confirmed the citing
  sentence is still *true* there, which is what L4.4 actually asks.

This review closes both gaps: every one of Tier 2's 78 Contracts read in full, not
sampled. It also extends L4.4 to the layer the first two reviews assumed rather than
checked: a Skill's `## Routing` table is itself a set of citations from Skill to
Knowledge, and nothing had confirmed those citations are still content-true — only that
`routes:` ids resolve and the Routing Index stays in sync (Levels 2-3, mechanical).

## Method

No mechanical bound this time — the point was to stop bounding. Each Contract's
frontmatter and body read for:

- **L4.1** — is the `summary` one subject? Are the `## Rules` one coherent API surface,
  or two unrelated concerns wearing one file?
- **L4.4** — for every `depends_on`, `related`, and prose `knowledge.x.y Rule N`
  citation, open the target and confirm the citing sentence is still true there today.

~95 cross-reference instances checked: ~60 intra-domain edges plus edges to 10 targets
outside Tier 2 (`human-interface-guidelines`, `networking`, `style-guide`,
`sf-symbols`, `app-store-review-guidelines`, `xcode`, `app-tracking-transparency`,
`local-authentication`, `uikit`, and StoreKit-internal edges).

A second pass, same date, took each of the 17 Skills' `## Routing` bullets (one per
Contract, ~78 total) and cross-matched the bullet's described trigger against the
target Contract's `### Included`/`### Excluded` scope and `## Rules` — does the Skill
still route on symbols the Contract actually covers, and does it omit nothing
rule-bearing. ~55 Stop-Condition hand-off lines (e.g. `widgetkit`→`app-intents`,
`security`→`local-authentication`, `storekit`→`app-store-review-guidelines`) were
checked the same way as T2-01/T2-02: does the named target actually own the deferred
rule.

## Findings

### T2-06 — A `related` edge pointed at the wrong Contract in the target domain

Status: Minor — fixed

`localization/layout-direction-and-rtl-apis` frontmatter `related:` and its
`## Dependencies` prose both pointed the "general SF Symbols usage beyond mirroring"
cross-reference at `knowledge.sf-symbols.symbol-variants` — a Contract narrowly scoped
to the `.fill`/`.circle`/`.square`/`.slash` variant-suffix mechanic and
`symbolVariant(_:)`, which does not cover general symbol usage. The Contract's own
`### Excluded` list already stated the boundary correctly and generically ("owned by
the `sf-symbols` domain"); only the machine-checked `related:` edge and its prose
narrowed it to one wrong Contract.

Every other `sf-symbols` Contract (`custom-symbol-usage`, `rendering-modes`,
`uikit-symbol-configuration`, `symbol-weight-and-scale`, `symbol-variants`,
`variable-value-symbols`) carries a `depends_on` edge to `symbol-basics`, which is the
domain's actual entry point. Fixed by repointing the edge to
`knowledge.sf-symbols.symbol-basics` and rewording the Dependencies prose to say why:
it is the hub every other Contract in that domain depends on.

This is the L4.4 failure mode the checklist names but had not yet produced an instance
for: Level 2 proved the id resolved (`symbol-variants` exists), and nothing checked
whether it was the *right* id.

## Passes

- **L4.1 — atomicity: 0 findings, all 78 Contracts.** Every summary is one subject with
  one coherent API surface; multi-clause summaries describe facets of one mechanic
  (e.g. `widgetkit/widget-interactivity-and-deep-links` covers `widgetURL`, `Link`,
  intent-wiring, and deep-link routing — all one topic: widget navigation). This
  confirms, on the full population rather than a sample, #0001's conclusion that the
  atomicity heuristic over-flags and Tier 2 Contracts are genuinely atomic. No second
  instance of the heuristic's noise problem, and no reason to revisit the decision to
  keep L4.1 a reading check rather than code.
- **L4.4 — cross-reference truth: 1 finding (T2-06) out of ~95 checked; the rest hold.**
  Notably: `passkit/adding-passes-ui` and `eventkit/recurrence-rules-and-eventkitui-handoff`
  both cite `knowledge.uikit.swiftui-view-representable` Rule 5 — confirmed that Rule 5
  still says exactly what both citations claim (the T2-01 fix from review #0001 holds).
  `authenticationservices/nonce-and-identity-token-verification` cites
  `storekit/transaction-verification-and-entitlements`'s server-side-exclusion pattern by
  analogy — confirmed. `passkit/apple-pay-payment-request`'s claim that
  `PayWithApplePayButton` is SwiftUI-native, unlike the Wallet-UI wrapping case — confirmed
  against its own quoted Apple text. All `privacy` ↔ `app-store-review-guidelines`,
  `storekit` ↔ `app-store-review-guidelines`, `usernotifications` ↔
  `human-interface-guidelines.notifications`, and `security` ↔
  `local-authentication.keychain-biometric-binding` cross-domain edges: target summaries
  match the deferred claim.
- **Skill routing content: 0 findings, 17/17 Skills, ~78 routing bullets, ~55
  Stop-Condition hand-offs.** Every routing bullet's named symbols/scenarios match its
  target Contract's current `### Included` list; no bullet routes on a symbol the target
  no longer covers or omits a rule-bearing topic the target states. Every Stop-Condition
  hand-off names the domain or Contract that actually owns the deferred rule, confirmed
  on the Knowledge side (this is the same relationship #0001's T2-01 fixed and this pass
  re-confirmed holds: `passkit`/`eventkit` Stop Conditions naming `uikit`'s
  `swiftui-view-representable` are content-true today). No "future"/"not yet built"
  claim in any Tier 2 Skill calls a now-built domain unbuilt, consistent with
  `check_scope_vocabulary` already passing.

## Not covered

**L4.5 (citation authorizes its rule)** stays out of scope for this review. Verifying
that every quoted rule actually appears on its cited Apple page requires fetching each
citation's live content, not just reading the repository — a materially larger and
differently-shaped task (closer to `check_links.py`'s territory than to a reading
review), tracked separately rather than folded in here. Closed in review #0003.

## Conclusion

Tier 2 conforms. The one defect this pass found (T2-06) is the same *shape* as T2-01/
T2-02 from review #0001 — a cross-reference edge, not a duplicated or unowned rule —
which is consistent with #0001's read that Tier 2's remaining exposure is in edge
bookkeeping rather than in the rules themselves. The Skill-routing pass found nothing,
which closes the one dependency direction (Skill→Knowledge) neither prior review had
separately verified as content-true rather than merely structurally resolvable.
Combined with #0001, Tier 2's 78 Contracts and 17 Skills have now had every L4.1-L4.4
check run against the full corpus at least once, with L4.5 explicitly named as the one
still-open check rather than silently skipped.
