# Review Checklist

Status: Approved
Version: 1.1.0

## Purpose

The instrument for Validation Levels 4 and 5. `validation-model.md`
[[validation-model]] marks both blocking and names "review checklist" as what
enforces Level 4; until 2026-08-08 that checklist did not exist, so the level was
blocking nothing. This is it.

Every semantic defect this repository has found was found by a phase that happened to
look — eight duplicated rules by a read-through scoped to two domains, a mis-scoped
cross-reference as a side effect of that, an unowned widget rule by the first slice run
against the Workflow layer. Each was a Level 4 or 5 item. None was caught by Level 4,
because there was nothing to catch it with. The checks below are written from those
failures rather than from first principles, and each one names the failure that earned
it.

## How to use this

Work the checks against the **diff**, not the repository. A pull request is
responsible for what it changes and for what its change makes false elsewhere — the
second half is where this repository's defects have lived.

Levels 1-3 are mechanical and must already be green; this checklist assumes that and
never repeats it. A check here that could be mechanical is a defect in the validator,
not a line in this file — three checks graduated to code that way, and any future one
should.

## Level 4 — Domain

### L4.1 — Each Knowledge Contract is atomic

One responsibility. A Contract an agent must load to get two unrelated answers is two
Contracts.

Ask: can this Contract's `summary` be written as one sentence with one subject? If the
honest summary needs an "and" joining two topics, split it.

### L4.2 — No rule is stated twice

The check that finds the most, and the one no script can do: no mechanical check can
know that two differently-worded paragraphs state the same requirement.

Ask, for every rule the diff adds or edits: **is this rule already stated somewhere
else?** Search the neighbouring domain by concept, not by wording. If it is, delete
one and have the other point at it — one Contract owns the rule, the neighbour points
and says it defines none, in as many words:

> `branding` Rule 3: "…defined in `typography` Rule 5 — branding does not define
> separate font-accessibility rules"

Why it matters more than a missing rule: both copies are correct the day they are
written. The failure arrives when Apple changes the guidance and one copy is updated.
This repository has already had that failure, in two Contracts that contradicted each
other on "Log In".

Found by hand: 8 instances, Phase 5b.

### L4.3 — No coupling is left unowned

Two Contracts can each be correct and still leave a rule between them, because each
Excluded list defers it to the other. This is not duplication and L4.2 will not find
it.

Ask: **does this rule constrain a choice made in another Contract?** If applying rule
A changes what is legal under rule B, one of them must say so.

`domain-map.md`'s Cross-Domain Notes carry three values — angle-split, clean handoff,
and **coupled**. The third exists because the first two both answer *do these overlap?*,
and two boundaries classified correctly as clean handoffs produced defects anyway. A
coupled boundary must name which side owns the coupling rule.

Found by hand, twice:

- A widget's interactive intent guarantees a timeline reload. `widgetkit` defers
  authoring the intent, `app-intents` defers the wiring, and the general reload rule
  the agent then reaches gives the *opposite* instruction (slice #0002).
- Binding a Keychain item to biometrics fixes the accessibility constant. Two
  Contracts each owned half of one coupled decision and neither said it was coupled
  (slice #0005).

### L4.4 — Every cross-reference is true at the far end

Level 2 proves the id resolves. Nothing proves the rule at the other end says what the
citing sentence claims it says.

Ask: **open the target and read it.** Does it cover the case being cited for it? A
reference to "the general prohibition in `icons` Rule 6" is wrong if `icons` is scoped
to interface icons and Apple states the prohibition per surface — there was no general
rule to point at.

Found by hand: 1 instance, Phase 5b.

### L4.5 — Every citation authorizes its rule

The cited page must contain the rule, not merely the topic. **URL shape does not prove
specificity** — a hub page and a real framework landing page sit at the same path
depth.

Ask: does the quoted sentence appear on the cited page? If a rule is stated without a
quotation, say why the page supports it.

`check_links.py` proves a URL resolves and is the address Apple currently serves. It
cannot read the page.

### L4.6 — Skills contain no domain knowledge

A Skill routes. The moment it states a rule, that rule is unroutable, untested, and
invisible to every check that walks Knowledge Contracts.

Ask: delete every routing line from the Skill. Is any *rule* left?

### L4.7 — Every scope statement is true today

`### Excluded`, `## Stop Conditions`, and `## Purpose` claim what a domain does not own.
Those claims rot: every domain that ships turns every "future `<that domain>`" into a
lie, in files nobody is editing.

The reality half of this is now `check_scope_vocabulary` and needs no human. What
remains for review is the part a script cannot judge: **is the boundary the Excluded
list draws the real one?** A boundary invented to justify not writing something is the
failure this check exists for.

Found by hand: 9 Contracts calling seven built domains "future", slice #0005 — the
third time that class surfaced, after Skills and References.

## Level 5 — Vertical Slice

Not a checklist item. A slice is required when a pull request changes **routing, a
Workflow, or a layer boundary** — the three things a per-file review cannot see.

Record it under `validation/slices/NNNN/`, with the task, the expected routing, the
observed routing, the four Level 5 checks, and a FINDINGS.md. A slice that finds
nothing is still a record; slice #0006 is one, and it is the reason the Workflow
sequencing is known to work rather than assumed to.

A slice record is evidence only for the architecture it was run against. When a
pull request deletes an artifact a slice tested, that slice is void and must be marked
superseded — see slice #0001, which certified a login flow whose five artifacts had all
been removed.

## Recording a review

A Level 4 review of an existing corpus — as opposed to a diff — is recorded under
`validation/reviews/NNNN-<scope>.md`, so that a level marked blocking leaves the same
evidentiary trail Level 5 does. Record the mechanical bounds used, the findings, **and
the passes**: a review that reports only defects cannot be told apart from one that
stopped early. Record rejected checks too — review #0001 rejected an atomicity heuristic
that flagged half the corpus, and that rejection is why L4.1 stays a reading check.

## Pull request

The template at `.github/PULL_REQUEST_TEMPLATE.md` carries these as checkboxes. Ticking
a box you did not perform is worse than leaving it blank: the next reviewer reads a
ticked box as evidence, which is exactly how slice #0001 stayed the repository's Level 5
record for four phases after it stopped being true.
