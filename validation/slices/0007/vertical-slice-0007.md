# Vertical Slice #0007 — Photo Places

Date: 2026-08-09

## Objective

The Tier 3 pilot's own test. Slice #0006 produced a rule — *a cross-domain boundary
decided in `domain-map.md` before either side is written does not need a slice to find
its gaps; a boundary that emerges from two independently-correct domains does* — and
`core-location` and `photos` were built as its prospective test: nine boundaries
classified in advance, both domains written against those entries.

Until now the pilot's verdict came from the *build*, which is the weaker evidence. An
author reading a boundary entry while writing the Contract it constrains is not the same
reader as an agent routing a task. This slice supplies the missing half.

## Scope

Task:

> Add "Places" to the photo journal: the user picks photos from their library, each
> photo's card shows where it was taken, and when the user comes back to one of those
> places later the app should react even if it isn't running.

Chosen because it lands on four of the nine pre-classified boundaries at once —
`photos` ↔ `uikit-interaction`, `photos` ↔ `app-store-review-guidelines`,
`core-location` ↔ `backgroundtasks`, `core-location` ↔ `app-store-review-guidelines` —
and because it is a SwiftUI build task, which is where the `uikit-interaction` entry was
found wrong at authoring time in Phase 11.

## Observed Routing

Workflows table matched nothing: the three rows are sign-in, App Store submission, and
widgets. Skills table matched two rows, `photos` and `core-location`, and the task
decomposes into three sub-tasks that route independently.

| Sub-task | Skill | Contracts reached |
|---|---|---|
| Pick photos | `photos` | `picker-and-selection-results` |
| Show where each was taken | — | **none** (see F-007-01) |
| React on returning to a place, app not running | `core-location` | `background-monitoring-and-launches`, plus both of its declared dependencies — `authorization-and-usage-strings` and `accuracy-and-precise-location` |

Four Contracts in total. The task never mentions accuracy, and
`accuracy-and-precise-location` is loaded anyway because `depends_on` is binding — which
is correct here rather than over-loading: a geofence radius under `reducedAccuracy` is
exactly the case a background monitoring rule assumes has been settled, and that is what a
declared dependency is for. Recorded because "context is minimized" is measured against
what the task asked for, and a binding dependency is the one legitimate way that count
grows.

Two Skills for one feature is not F-003-01's failure. There the *single* question needed
two domains at once; here each sub-task is separable, and `AGENTS.md`'s "exactly one
Skill" applies per task rather than per feature request. The third sub-task is the one
that is not separable, and it routes nowhere.

## The seams under test

**`photos` ↔ `uikit-interaction` — holds, and the Phase 11 correction is load-bearing.**
The task is SwiftUI, so this is exactly the path that would have produced a wrong
instruction had the pre-classification been implemented as written.
`picker-and-selection-results` Rule 2 tells the agent to use `PhotosPicker` and *not* to
wrap `PHPickerViewController`; `limited-library` Rule 5 requires a `UIViewController` for
`presentLimitedLibraryPicker(from:)` and names `knowledge.uikit.swiftui-view-representable`
Rule 5 for how. The task reaches the first and not the second, and the agent is never
told to bridge something that has a native replacement. The correction survives routing,
not merely review.

**`core-location` ↔ `backgroundtasks` — holds under the task that invites the error.**
"React even if it isn't running" is the phrasing that sends an agent to `BGTaskScheduler`.
`background-monitoring-and-launches` Rule 4 forecloses it before the agent gets there —
Core Location performs the launch itself, so choosing a monitoring service *removes* the
need for a scheduled task — and the Skill's Stop Conditions say the same thing at routing
time, one step earlier. A boundary re-classified as **coupled** in Phase 9 and written to
in Phase 10, confirmed under a task in Phase 12.

**Both domains ↔ `app-store-review-guidelines` — holds, symmetrically.** The task needs
`NSPhotoLibraryUsageDescription` and `NSLocationWhenInUseUsageDescription`. Each domain's
authorization Contract carries the same delegation rule in the same shape —
`authorization-and-access-levels` Rule 6 and `authorization-and-usage-strings` Rule 6 —
each stating that it owns *which* key and *when*, and that the wording standard is
`knowledge.app-store-review-guidelines.permission-usage-strings`. Neither invents a
domain-local wording rule. This is the "live claim to disarm" the pre-classification named
before either domain existed, and it is disarmed on both sides.

**`photos` ↔ `core-location` — the defect, and the one boundary nobody classified.**
See FINDINGS.md. `PHAsset.location` is declared `var location: CLLocation? { get }`; the
photo library returns a Core Location type under the photo-library grant. Neither domain
said so, so the sub-task routes nowhere.

## Results

| Level 5 check | Result |
|---|---|
| Routing succeeds from task to Knowledge without repository search | **PASS** for two sub-tasks, **FAIL** for the third |
| The routed Knowledge is sufficient to complete the task | **FAIL** — F-007-01 |
| Context is minimized | **PASS** — 2 Skills, 4 Contracts, one of them a binding dependency rather than a task match |
| Architecture behaves as specified | **PASS** — the Stop Condition fires rather than the agent guessing |

## Result

Overall Status: **PASS WITH ONE FINDING — fixed in this pull request**

The rule from slice #0006 survives its prospective test. Four pre-classified boundaries
were exercised by a task rather than by an author, and none produced a seam defect. What
the slice found instead is a limit on the *method* that produced them: the classification
pass enumerated each new domain against domains that already existed, so the seam between
two domains built in the same phase was never a candidate for classification at all.

FINDINGS.md records both, and the fix ships with this record.
