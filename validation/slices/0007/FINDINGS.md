# FINDINGS — Vertical Slice #0007

Date: 2026-08-09

## Result

Overall Status: **PASS WITH ONE FINDING**

One unowned rule, at the one boundary in the Tier 3 pilot that was never classified. The
four pre-classified boundaries the task exercised all held.

------------------------------------------------------------------------

### F-007-01 A rule falls between `photos` and `core-location`

Status: **Fixed in this pull request**

Observation:

`PHAsset.location` is declared `var location: CLLocation? { get }`. Apple describes it as
"The location information for the asset" and notes that "Typically, an asset's location
metadata identifies the place where the asset was captured." The Photos framework returns
a Core Location type, delivered under the photo-library grant, with no Core Location
authorization involved at any point.

Before this pull request, neither domain said so. `photos` never mentioned the property:
`asset-fetching` owned `PHAsset` as a fetch result and stopped at the object. `core-location`
never mentioned photos: its authorization Contract is correct and complete about the
device's current location, which is a different fact about a different subject.

Two failure modes, and the task in this slice reaches one or the other depending on which
Skill the Routing Index picks:

1. The agent selects `photos`, finds no routing line for asset metadata, and the Skill's
   Stop Conditions correctly fire — *do not guess or fall back to general knowledge*. The
   architecture behaves as specified and the task cannot be completed. This is the good
   outcome.
2. The agent matches `location permission` on the `core-location` row, is routed to
   `authorization-and-usage-strings`, and ships `requestWhenInUseAuthorization()` for a
   feature whose data is already in hand. That is a permission prompt for data the app
   never uses, which HIG's `privacy` Rule 1 forbids on design grounds and which is a
   plausible App Review finding besides.

Why no level caught it:

Every mechanical check passed, and would pass on a corpus where this rule never exists.
Level 2 proves ids resolve, not that a needed rule was written. `check_routing_coverage`
proves every Contract is reachable; a rule that no Contract states is reachable from
nothing and invisible to it. This is the same shape as slices #0002 and #0005 — a rule
left unowned between two Contracts that are each correct within their own scope — and it
is the third instance of that shape, which is why it is already a checklist item (L4.3)
and still needed a slice to be found. L4.3's question — *does this rule constrain a choice
made in another Contract?* — could not reach it: there was no rule to ask the question of.
Both prior instances were two Contracts each deferring half of a decision; this one is two
Contracts saying nothing at all. The checklist gains the question that would have found
it.

Fix, as shipped:

`photos` owns it. The precedent is `core-location` ↔ `backgroundtasks`: the domain that
owns the coupling rule is the one where the question can be asked at all, and "where was
this photo taken" only exists once an asset is in hand. `knowledge.photos.asset-fetching`
Rule 5 states the rule and the authorization it does not require;
`knowledge.core-location.authorization-and-usage-strings` excludes it by name and states
nothing about it; both Skills carry the split in their Stop Conditions so it is resolvable
at routing time and not only after a Contract is loaded; and the Routing Index gains
`PHAsset.location`, `where a photo was taken`, and `photo capture location` on the `photos`
row, since `domain-map.md`'s own Rules require a resolved boundary to reach the Index.

### F-007-02 The classification pass could not have found it

Status: Passed — recorded because the reason generalizes, and it is now a rule

Observation:

The Tier 3 pilot classified nine boundaries before either domain was written, and this is
not one of the nine. That is not an oversight in the sense of a missed entry: the pass
enumerated **each new domain against domains that already existed**. `photos` ↔
`core-location` was not a candidate for classification under that method, because when
each was being classified the other did not exist.

This sharpens #0006's rule rather than weakening it. The rule says a boundary decided in
advance holds and an emergent one costs a slice. Both halves are confirmed here: the four
pre-classified boundaries this task exercised held, and the one emergent boundary cost
exactly one slice. What the rule does not say — and now does, in `domain-map.md`'s Rules —
is that **a phase building more than one domain must classify the new domains against each
other**, because the method that produces pre-classified boundaries has a blind spot
exactly the size of a multi-domain phase.

### F-007-03 The Phase 11 correction holds at routing time

Status: Passed

Observation:

Phase 11 found the `photos` ↔ `uikit-interaction` entry named the right neighbour and the
wrong symbol, and replaced one wrong rule with two deliberately opposed ones. This slice
is the first test of that correction by a task rather than by its author, and it is a
SwiftUI task — the exact path the wrong entry would have damaged.

The agent reaches `picker-and-selection-results` Rule 2 (use `PhotosPicker`, do not wrap)
and does not reach `limited-library` Rule 5 (obtain a `UIViewController`, and
`knowledge.uikit.swiftui-view-representable` Rule 5 owns how), because the task does not
touch the limited-library grant. Two rules that contradict each other on the same technique
did not produce an ambiguous instruction, because each names the symbol it governs and the
Skill states the split before either is loaded.

### F-007-04 A coupled boundary holds under the task that invites the error

Status: Passed

Observation:

"React even if it isn't running" is the phrasing that produces a `BGAppRefreshTask` polling
loop. `background-monitoring-and-launches` Rule 4 forbids it and explains why — Core
Location performs the relaunch itself, so a monitoring service *removes* the scheduled task
rather than sitting beside it — and `skills/core-location/SKILL.md` says so in its Stop
Conditions, one step before any Contract is loaded.

Worth recording separately from F-007-02 because it tests a different thing: this boundary
was re-classified from *clean handoff* to *coupled* in Phase 9, after the Tier 2 review
showed that "do they overlap?" is the wrong question for a seam. A slice now confirms the
re-classification was right, under the task it was predicted to matter for.
