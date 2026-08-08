## What changed?

<!-- Briefly describe: a new Skill, a Knowledge Contract update, a routing fix? -->

## Why?

<!-- What problem/gap does this solve? If there's a related issue: Closes #... -->

## Process checklist

- [ ] Change follows the guidelines in [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Knowledge Contract format follows the layer order in [CLAUDE.md](../CLAUDE.md)
- [ ] Validation scripts were run locally and passed — all four, see CONTRIBUTING.md
- [ ] `domain-map.md` was updated, if relevant
- [ ] README.md "What's New" section was updated, if relevant
- [ ] If this is a new Skill, it was added to the `skills/index.md` routing table

## Level 4 review

Levels 1-3 are the scripts above. These are the semantic checks no script decides —
the full procedure for each is in
[docs/contributing/review-checklist.md](../docs/contributing/review-checklist.md).
Tick only what you actually performed.

- [ ] **L4.1** Each new/changed Contract is atomic — one responsibility
- [ ] **L4.2** No rule this PR adds is already stated in another Contract
- [ ] **L4.3** No coupling left unowned — if this rule constrains a choice another Contract makes, one of them says so
- [ ] **L4.4** Every cross-reference was opened and read; the target's scope covers the case cited for it
- [ ] **L4.5** Every citation contains the rule, not merely the topic
- [ ] **L4.6** No Skill gained a rule — Skills route, they do not state
- [ ] **L4.7** Every `Excluded`/`Stop Conditions` boundary this PR writes is a real one

## Level 5 — required if this PR changes routing, a Workflow, or a layer boundary

- [ ] A vertical slice was run and recorded under `validation/slices/NNNN/`, or N/A
- [ ] No existing slice was invalidated by this PR (an artifact a slice tests was deleted)
