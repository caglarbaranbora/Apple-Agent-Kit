# FINDINGS — Vertical Slice #0004

Date: 2026-08-08

## Result

Overall Status: FAIL, FIXED IN THIS PULL REQUEST

------------------------------------------------------------------------

### F-004-01 Nine keywords route to two Skills, and the tiebreak lives one layer too late

Status: **Blocking** — fixed in this pull request

Observation:

| Keyword | Claimed by | Resolved in `domain-map.md` as |
|---|---|---|
| `ObservableObject` | `swiftui`, `combine` | `combine` owns the pattern; `swiftui` owns migrating off it |
| `@Published` | `swiftui`, `combine` | same |
| `in-app purchase` | `app-store-review-guidelines`, `storekit` | policy vs. API |
| `IAP` | `app-store-review-guidelines`, `storekit` | same |
| `restore purchases` | `app-store-review-guidelines`, `storekit` | same |
| `privacy manifest` | `app-store-review-guidelines`, `privacy` | review consequence vs. correct implementation |
| `PrivacyInfo.xcprivacy` | `app-store-review-guidelines`, `privacy` | same |
| `RTL` | `human-interface-guidelines`, `localization` | visual design vs. layout-direction API |
| `SF Symbols` | `human-interface-guidelines`, `sf-symbols` | symbol choice vs. rendering API |

Not one of these is an ownership error. Every pair is an angle-split that
`domain-map.md` states explicitly, each Skill routes its side to a different and
correct Contract, and in several cases the losing Skill's Stop Conditions name the
winner by name — `localization`'s says "RTL visual-design decisions — owned by
`human-interface-guidelines`".

That sentence is the tiebreak, and it is unreachable at the moment it is needed. Stop
Conditions are read *after* a Skill has been selected. An agent that resolves "RTL" to
`human-interface-guidelines` never opens `localization` and never sees it; an agent
that resolves it to `localization` sees a redirect it could have been given one step
earlier. The knowledge was in the repository and not in the table.

Why no level caught it:

`check_routing_index_sync` proves every Skill and Workflow appears in the Index, both
directions. `check_routing_coverage` proves every Knowledge Contract is reachable from
some Skill. Both are about *presence* — one that nothing is missing, the other that
nothing is stranded. Neither is about *uniqueness*, and ambiguity is a uniqueness
property. Sixteen checks, and the gap was the one question nobody had asked of the
table.

This is the same shape as F-002-01 and F-003-01. In all three the lower layers are
right and the Routing Index resolves less than `AGENTS.md` claims it does — a rule
between two correct Excluded lists, a join with no Workflow to express it, and here a
boundary resolved in `domain-map.md` that the Index does not carry. `domain-map.md` is
not in the Startup Procedure; nothing an agent is told to read contains it.

Architectural action taken:

1. The nine keywords are qualified in `skills/index.md` so the table decides, e.g.
   `SF Symbols (choosing one)` on the `human-interface-guidelines` row against
   `SF Symbols (rendering)` on the `sf-symbols` row. No Skill's scope changes; only
   the Index says out loud what the Skills already implement.
2. `check_routing_keywords_unambiguous` is added to `scripts/validate_repo.py`, making
   this the seventeenth repository check. It is cheap, deterministic, and offline,
   which is what earns it a place in Levels 2–3 — and it is exactly the check that
   would have caught nine defects the other sixteen were not shaped to see.

------------------------------------------------------------------------

### F-004-02 Same-Skill duplicates are not ambiguity

Status: Passed, method note

Observation:

`ModelContainer`/`modelContainer` and `ModelContext`/`modelContext` collide under case
normalization and both route to `swiftdata`. They are the type and the view modifier —
two real API names an agent may reasonably type either way.

The check discards same-Skill pairs rather than reporting them. A keyword claimed twice
by one Skill leaves routing perfectly determined, and flagging it would have made the
check's first run 11 findings instead of 9, two of which have no defect behind them.
A check that reports non-defects gets silenced, which `validation-model.md` already
gives as the reason Levels 4–5 have no script.
