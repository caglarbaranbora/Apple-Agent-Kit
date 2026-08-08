# Vertical Slice #0004 — Routing Determinism

Date: 2026-08-08

## Objective

Slices #0002 and #0003 each followed one task to a correct answer. Neither could show
that *every* task routes to one place, because a slice exercises the path it takes, not
the paths it doesn't. This slice tests the property directly, over the whole Routing
Index, rather than sampling it.

## Scope

Claim under test — `AGENTS.md`, Startup Procedure step 3:

> Match the Workflows table first; a match names the Skills to run in order. Otherwise
> match the Skills table and select **exactly one** Skill.

For that instruction to be executable, no keyword may appear in two rows of the Skills
table. If one does, the table does not decide, and the agent must fall back on judgment
— which is the repository search the architecture exists to eliminate.

## Method

Mechanical, and re-runnable. Parse the Skills table of `skills/index.md`, split each
row's keyword cell on commas, normalize case, and count the distinct Skills claiming
each keyword.

Case is normalized deliberately, then same-Skill pairs are discarded: `ModelContainer`
(the type) and `modelContainer` (the view modifier) are two real API names that
normalize to one string, and both route to `swiftdata`. A keyword claimed twice by the
same Skill is never ambiguous, whatever its case.

This became `check_routing_keywords_unambiguous` in `scripts/validate_repo.py` — see
F-004-01.

## Results

    32 Skill rows
    622 keywords, 611 distinct
    11 claimed more than once
      2 by the same Skill (case-normalization artifacts — not ambiguous)
      9 by two different Skills

| Level 5 check | Result |
|---|---|
| Routing succeeds from task to Knowledge without repository search | **FAIL** at 9 keywords — see F-004-01 |
| The routed Knowledge is sufficient to complete the task | not exercised |
| Context is minimized | not exercised |
| Architecture behaves as specified | **FAIL** — the Index under-determines what `AGENTS.md` says it determines |

## Result

Overall Status: **FAIL, FIXED IN THIS PULL REQUEST**

9 of 622 keywords sent an agent to two Skills with no tiebreak at the point of routing.
Every one of them is a boundary `domain-map.md` had already resolved correctly; none is
an ownership error. The Index simply did not carry the resolution.

See FINDINGS.md.
