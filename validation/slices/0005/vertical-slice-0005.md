# Vertical Slice #0005 — Sign-In Feature

Date: 2026-08-08

## Objective

Exercise `workflows/authentication`, the highest-risk artifact in the repository and
the only one never tested. It survived the retirement of the domain it is named after,
and Phase 5 had to bolt `app-store-review-guidelines` onto its front after discovering
it could otherwise produce a screen App Review rejects. Neither the survival nor the
repair had ever been checked against a task.

## Scope

Task:

> Build a sign-in screen offering Sign in with Apple, and let returning users
> re-authenticate with Face ID.

Six Skills — the longest chain in the repository, and the one where a seam is most
likely to be left unowned.

## Procedure

`AGENTS.md`'s Startup Procedure, followed literally.

## Observed Routing

Workflows table matched on the sign-in row; `workflows/authentication/WORKFLOW.md`
sequenced six Skills, of which the task made all six applicable.

| Step | Skill | Reached |
|---|---|---|
| 1 | `app-store-review-guidelines` | `login-services-equivalent-option` (4.8) |
| 2 | `style-guide` | `sign-in-and-authentication-terminology`, `authentication-credentials-and-biometrics`, `general-button-labels` |
| 3 | `accessibility` | labels, traits, value/hint, VoiceOver order, focus, announcements |
| 4 | `authenticationservices` | request/controller, nonce, credential state, session persistence |
| 5 | `local-authentication` | availability, policy evaluation, reason strings, errors, Keychain binding |
| 6 | `security` | Keychain CRUD, accessibility levels |

**The Phase 4 retirement holds.** The three Contracts the deleted `authentication`
domain used to own are all reachable under their new owners: sign-in terminology and
button labels via step 2, form accessibility via step 3. Nothing was stranded by the
retirement, which no check could have told us and no previous slice had asked.

**The Phase 5 repair holds.** Step 1 runs first and reaches guideline 4.8 before any
view exists, which is the whole point of putting it first.

## Results

| Level 5 check | Result |
|---|---|
| Routing succeeds from task to Knowledge without repository search | **PASS** |
| The routed Knowledge is sufficient to complete the task | **FAIL** — see F-005-01 |
| Context is minimized | **PASS** — every Skill in the chain was applicable |
| Architecture behaves as specified | **FAIL** — see F-005-02 |

## Result

Overall Status: **PASS WITH TWO BLOCKING FINDINGS**

The Workflow itself is sound: the sequencing is right, the retirement left nothing
stranded, and the six Skills hand off cleanly. Both findings are in the Contracts the
chain reaches, and the second is a defect class rather than an instance.

See FINDINGS.md.
