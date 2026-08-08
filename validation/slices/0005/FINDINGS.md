# FINDINGS — Vertical Slice #0005

Date: 2026-08-08

## Result

Overall Status: PASS WITH TWO BLOCKING FINDINGS, both fixed in this pull request

------------------------------------------------------------------------

### F-005-01 A coupled decision split across two Contracts, with neither saying it was coupled

Status: **Blocking** — fixed

Observation:

Step 5 reaches `local-authentication`'s `keychain-biometric-binding` Rule 1, which
required a biometry flag "combined with an accessibility constant restricted to the
device (**e.g.** `.whenUnlockedThisDeviceOnly`)" — an example inside a family, phrased
as a free choice.

Step 6 reaches `security`'s `keychain-accessibility-levels`, which owns the constants
and organizes them by sensitivity. Its Rule 3 covers
`kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` and never mentions biometry; its
Excluded list correctly defers `SecAccessControl` and the biometry flags to
`local-authentication`.

Apple couples the two. From "Accessing keychain items with Face ID or Touch ID", which
`keychain-biometric-binding` already cited:

> `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly, .userPresence, nil`

> the `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` setting prevents items from
> being stored if the device has no passcode.

An agent following the chain makes two independently reasonable choices that Apple
treats as one, and lands on the weaker guarantee: a biometry-bound item that remains on
a device whose passcode was later removed, rather than one that could never have been
written without a passcode. The biometric prompt still appears, so nothing looks wrong.

The Contract's own Compliant Example used the weaker constant too — the rule and its
example were consistent with each other and both wrong.

Source: [Accessing keychain items with Face ID or Touch ID](https://developer.apple.com/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id)

Why no level caught it:

Both Contracts are atomic, both cite Apple, both Excluded lists name a real neighbour,
and no rule is stated twice. Level 4 as written asks about *duplication*; this is the
inverse — a rule that exists in neither place because each owns half of one decision.
This is the second instance of that shape, after slice #0002's widget reload, and it is
now Level 4 check **L4.3** in `docs/contributing/review-checklist.md` rather than
something the next phase has to rediscover.

Action taken:

`keychain-biometric-binding` Rule 1 now names the constant, quotes Apple, and points at
`knowledge.security.keychain-accessibility-levels` Rule 3 for its semantics. The
Compliant Example is corrected. `security` is unchanged — its Excluded list already
assigned this correctly, and it sits at the 150-line cap besides.

------------------------------------------------------------------------

### F-005-02 Nine Contracts call a built domain "future", and the check that exists for this had never looked at Contracts

Status: **Blocking** — fixed

Observation:

`keychain-biometric-binding`'s Excluded list read:

> General Keychain item storage/retrieval for non-biometric-bound items — **future
> `security` domain**

`security` is built, complete, and is step 6 of the very Workflow that reaches this
Contract. Sweeping the repository found nine Contracts making the same claim about
seven built domains:

| Contract | calls future |
|---|---|
| `accessibility/accessibility-audits-testing` | `testing` |
| `foundation/date-time-formatting` | `localization` |
| `foundation/measurement-and-unit-formatting` | `localization` |
| `human-interface-guidelines/motion` | `sf-symbols` |
| `human-interface-guidelines/notifications` | `usernotifications` |
| `human-interface-guidelines/privacy` | `privacy`, `security` |
| `local-authentication/keychain-biometric-binding` | `security` |
| `widgetkit/timeline-provider-and-entries` | `app-intents` |
| `widgetkit/widget-declaration-and-families` | `app-intents` |

Why no level caught it:

`check_scope_vocabulary` exists precisely for this and had never read a Knowledge
Contract. It was written for Skills, then widened to a Reference's `## Purpose` when
the identical claim turned up one layer away. Both times the fix added one artifact
type. **That was the wrong shape of fix.** The question was never which type states
scope — it is where the claim is *false*, and it is false anywhere it appears. The 258
Knowledge Contracts, which hold by far the most scope statements because every one has
an `### Excluded` list, were the largest uncovered surface and were uncovered for that
reason alone.

This class matters more than its nine instances. **It scales with exactly what the
repository is built to do.** Every domain that ships turns every "future `<that
domain>`" into a lie, silently, in files nobody is editing — which is why it has now
appeared three times, once per expansion. With 19 Tier 3 domains queued, a per-type fix
would guarantee a fourth.

Action taken:

The reality half of `check_scope_vocabulary` now reads the whole prose body of every
artifact, fenced code excluded. `name not in domains` is what keeps that safe: a Tier 3
domain that has not shipped is legitimately future, and saying so still passes. All
nine Contracts are corrected to name the owner. Seven tests added, including the three
negative controls — an unbuilt domain, a domain referring to itself, and a fenced code
block.

------------------------------------------------------------------------

### F-005-03 The Phase 4 retirement and the Phase 5 repair both hold

Status: Passed

Observation:

Two structural changes made in earlier phases had never been checked against a task.
The retired `authentication` domain's three Contracts are all reachable under their new
owners — terminology and button labels in step 2, form accessibility in step 3 — so the
retirement stranded nothing. And `skill.app-store-review-guidelines.submission` really
does run before any view exists, which is the entire reason Phase 5 moved it to the
front.

Worth recording because neither is provable mechanically. `check_no_orphans` shows every
Contract is reachable from *some* Skill; only a task shows the right ones are reached in
the right order.
