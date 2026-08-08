# FINDINGS — Vertical Slice #0003

Date: 2026-08-08

## Result

Overall Status: PASS WITH ONE ARCHITECTURAL FINDING

Routing and context minimization behaved as specified. The finding is that the
architecture forces one Skill onto a task that two domains answer jointly, and there
is no Workflow for the join.

------------------------------------------------------------------------

### F-003-01 "Exactly one Skill" under-serves tasks the kind-partition splits

Status: **Architectural** — recorded, not fixed in this pull request

Observation:

The routed Contracts give the agent the vocabulary rules for the fix —
`app-state-and-error-terminology` Rule 6 ("error message" belongs only in developer
materials), Rule 1 (neutral, non-alarming phrasing) — and nothing about what the
replacement message should *say*.

That rule exists. It is `human-interface-guidelines`' `feedback` Rule 6:

> Agents MUST explain why a command can't be carried out when blocking or rejecting an
> action, not just that it failed.

"Invalid Entry" fails exactly that rule, and the agent never sees it, because
`AGENTS.md` step 3 says to "select exactly one Skill" and the task's keywords matched
the wording domain.

This is the kind-partition that Phase 5b identified, seen from the routing side:
`human-interface-guidelines` decides what to say, `style-guide` decides how to word it.
Phase 5b established that this partition is correct and is why the two domains
duplicate nothing. What slice #0003 adds is that a task can land squarely on the
partition line, and the Routing Index has no way to express that — its Workflows table
holds three rows, all of them multi-framework build tasks, none of them a
design-plus-wording join.

Why no level caught it:

`check_routing_coverage` proves every Contract is reachable from some Skill.
Reachability is not the same as being reached: `feedback` is reachable from
`human-interface-guidelines-patterns`, and this task does not route there. No
mechanical check can know that a task needs two domains, because no mechanical check
sees a task.

Proposed architectural action, deliberately not taken here:

Two options, and the choice is a design decision rather than a defect fix:

1. A fourth Workflow composing `human-interface-guidelines-patterns` and `style-guide`
   for user-facing message tasks. Consistent with how the other three Workflows work,
   and it makes the join explicit at the point of routing.
2. Amend `AGENTS.md` to let a Skill's Stop Conditions hand off to a named Skill when a
   task crosses the partition. This weakens "a Skill never routes to another Skill,"
   which is a layer-order rule, and should not be done casually.

Option 1 is the smaller change and does not touch the layer order. Neither is in scope
for a promotion pull request; recorded here so the decision is made deliberately rather
than discovered again by the next slice.

------------------------------------------------------------------------

### F-003-02 Routing without API names works

Status: Passed

Observation:

The task named no framework, no type, and no symbol. It still routed in two table
lookups. Most rows in the Skills table are lists of API names, which makes this worth
recording: the design does not silently depend on the task mentioning an API, and the
four domains that are not API domains — design, wording, policy, project configuration
— remain reachable from the language a person actually uses.
