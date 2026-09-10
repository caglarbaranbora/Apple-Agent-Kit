Status: Research note (not a normative artifact — does not define, alter, or supersede any Knowledge Contract, Skill, Reference, or Workflow in this repo)

# Why mattpocock/skills works: architecture and design principles

Date: 2026-09-10
Researcher: Claude (session for caglarbaranbora)
Primary source: https://github.com/mattpocock/skills (branch `main`, as fetched 2026-09-10)

## Context

This session has `mattpocock-skills` installed as a Claude Code plugin
(`~/.claude/plugins/cache/mattpocock/mattpocock-skills/`) and has used several of
its skills (research, tdd, grilling, code-review, domain-modeling, codebase-design)
successfully. The goal of this note is to understand *why* that system works, purely
from primary sources (the repo's own README, docs, and skill files — no secondary
write-ups), so the underlying principles can be compared against Apple Agent Kit's
own Skill / Knowledge Contract system (References → Knowledge → Skills → Workflows;
see `/CLAUDE.md` and `docs/specifications/*.md` in this repo).

This is pure research: no other file in this repo was modified.

## 1. What the repo actually is

Per the README (https://github.com/mattpocock/skills/blob/main/README.md):

> "My agent skills that I use every day to do real engineering, not vibe coding."

> "These skills are designed to be small, easy to adapt, and composable. They work
> with any model. They're based on decades of engineering experience."

The README frames the whole project as a response to four named failure modes in
agent-assisted development, each with a named fix:

1. **Misalignment** ("the agent didn't do what I want") → grilling (`/grill-me`,
   `/grill-with-docs`): an interview loop run *before* implementation.
2. **Verbosity** ("the agent is way too verbose") → a shared vocabulary document
   (`CONTEXT.md`), quoting Eric Evans on ubiquitous language: "conversations among
   developers and expressions of the code are all derived from the same domain
   model."
3. **Poor code quality** ("the code doesn't work") → tight feedback loops: TDD
   (`/tdd`) and a disciplined debugging loop (`/diagnosing-bugs`), quoting *The
   Pragmatic Programmer*: "The rate of feedback is your speed limit."
4. **Architectural decay** ("we built a ball of mud") → deliberate module design
   (`/codebase-design`, `/improve-codebase-architecture`), quoting Kent Beck
   ("Invest in the design of the system every day") and Ousterhout ("The best
   modules are deep").

Source: https://github.com/mattpocock/skills/blob/main/README.md

## 2. Directory structure and the promoted/non-promoted split

Fetched via `https://api.github.com/repos/mattpocock/skills/git/trees/main?recursive=1`.
Top level:

```
.agents/            — ADRs and cross-cutting agent-facing docs (invocation rules, install text, doc-writing conventions)
.changeset/          — changesets for versioning
.claude-plugin/       — plugin.json + marketplace.json (Claude Code plugin manifest)
.github/workflows/    — release CI
.out-of-scope/        — explicit "we deliberately don't do this" notes
AGENTS.md             — very short: points to CONTEXT.md-style domain terms for the *skills repo itself*
CHANGELOG.md, CLAUDE.md, CONTEXT.md, README.md, LICENSE
docs/engineering/      — one human-facing docs page per engineering skill
docs/productivity/     — one human-facing docs page per productivity skill
scripts/               — link-skills.sh, list-skills.sh, sync-plugin-version.mjs
skills/
  engineering/          — promoted, daily code-work skills
  productivity/          — promoted, daily non-code workflow skills
  misc/                  — kept around, not promoted, not shipped in plugin
  in-progress/           — public beta, feedback wanted, not shipped in plugin
  deprecated/            — no longer used
```

Every promoted skill directory (`skills/engineering/*`, `skills/productivity/*`)
has the same shape:

```
skills/engineering/<name>/
  SKILL.md                — the skill itself (frontmatter + body)
  <SUPPORTING-FILE>.md     — optional disclosed-reference files (e.g. tests.md, mocking.md)
  agents/openai.yaml       — Codex-harness metadata (display name, and for user-invoked
                             skills, the policy block that mirrors disable-model-invocation)
```

`CLAUDE.md` (https://github.com/mattpocock/skills/blob/main/CLAUDE.md) is the
normative statement of this structure. Key rules quoted verbatim:

> "Every skill in `engineering/` or `productivity/` (the **promoted** buckets) must
> have a reference in the top-level `README.md` and an entry in
> `.claude-plugin/plugin.json`'s `skills` array (the Claude Code plugin ships
> exactly the promoted set). Skills in `misc/`, `in-progress/`, and `deprecated/`
> must not appear in either."

> "Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus
> `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only
> by the human) or model-invoked (model- or user-reachable)."

> "No em-dashes anywhere in this repo's prose... Where a sentence reaches for one,
> rewrite it instead with a comma, colon, period, parentheses, or a conjunction."

This is a repo that treats its own skills as a maintained product: promotion status
gates what ships, a docs page is required per promoted skill, and a style rule
(no em-dashes) is enforced repo-wide, including inside skill prose itself.

Why a Claude Code plugin exists but a native Codex plugin is deferred is explained
in an ADR, not asserted as a given — see §6 below.

## 3. The user-invoked / model-invoked split (the core invocation mechanism)

This is the single most load-bearing architectural decision in the repo, and it is
written up explicitly in `.agents/invocation.md`
(https://github.com/mattpocock/skills/blob/main/.agents/invocation.md):

> "**User-invoked**: reachable only by the human typing its name. Set
> `disable-model-invocation: true` in the frontmatter (Claude Code) and
> `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex). The
> `description` is human-facing... Strip trigger lists."

> "**Model-invoked**: reachable by model or user. The default... The `description`
> is model-facing and keeps rich trigger phrasing... so auto-invocation fires. The
> test for whether a skill should stay model-invoked: *could the model usefully
> reach for this autonomously?* (Reuse is the reason to extract a skill, not the
> test.)"

> "Each harness excludes a user-invoked skill from the model's reach in its own
> way, so nothing but the human can fire it: no other skill can. A user-invoked
> skill may invoke model-invoked skills, but it can never reach another
> user-invoked one."

This gives the system two clean invocation lanes instead of one blurred one:

- **User-invoked skills are orchestrators / entry points** (`/grill-with-docs`,
  `/to-spec`, `/implement`, `/ask-matt`). They compose model-invoked skills, and the
  invariant that a user-invoked skill can never reach another user-invoked skill
  prevents orchestration chains from becoming tangled or ambiguous about who's
  driving.
- **Model-invoked skills are the reusable disciplines** (`/tdd`, `/research`,
  `/domain-modeling`, `/codebase-design`, `/code-review`, `/diagnosing-bugs`,
  `/grilling`, `/prototype`, `/resolving-merge-conflicts`, `/wizard`). These can be
  reached autonomously by the agent mid-task, or invoked directly by name, or
  called by an orchestrator.

Crucially, dependency between skills is not implicit prose or a cross-file link, it
is a named, singular action, per `.agents/invocation.md`:

> "Dependencies are expressed as an explicit instruction to **call the Skill tool**
> with the named skill (`Call the Skill tool with "grilling"`), not deep
> `../other-skill/FILE.md` cross-references, and not a bare `/skill`-style mention
> left for the model to interpret. Naming the tool is what gets it fired... The
> Skill tool takes one skill per call. A step that needs two skills is two calls,
> not one call with two names."

This is the repo's version of "how do you stop an agent from skipping the skill":
by making skill invocation an explicit tool call rather than a suggestion in prose,
and by keeping the description (the "context pointer") the single mechanism that
decides whether the model reaches for it autonomously at all.

## 4. Representative skill files, read in full

### `/tdd` (model-invoked)
https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md

- Frontmatter description carries the trigger: *"Use when the user wants to build
  features or fix bugs test-first, mentions 'red-green-refactor', or wants
  integration tests."*
- Body opens by stating exactly what it is a reference *for*: "the reference that
  makes that loop produce tests worth keeping... Every section applies on every
  cycle: consult them before and during the loop, not after." This forecloses the
  common failure of an agent reading a skill once at the start and then drifting.
- Defines a **seam** ("the public boundary you test at") and states a hard rule:
  "Test only at pre-agreed seams. Before writing any test, write down the seams
  under test and confirm them with the user. No test is written at an unconfirmed
  seam." This is a concrete anti-scope-creep mechanism: it stops an agent from
  testing everything reachable instead of what matters.
- Names anti-patterns by a diagnostic *tell*, not just a definition, e.g.
  "Implementation-coupled... The tell: the test breaks when you refactor but
  behavior hasn't changed." Tells make the rule checkable by an agent mid-task,
  not just quotable.
- Delegates out rather than duplicating: when the seam/interface question itself is
  unresolved, it says "call the Skill tool with 'codebase-design'" instead of
  re-explaining deep-module theory inline.
- Ends with three unambiguous rules of the loop: "Red before green," "One slice at
  a time," "Refactoring is not part of the loop" (explicitly pushed to
  `/code-review` instead).

### `/research` (model-invoked)
https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md

Full body (it is intentionally tiny, 13 lines):

> "Spin up a **background agent** to do the research, so you keep working while it
> reads.
>
> Its job:
> 1. Investigate the question against **primary sources** (official docs, source
>    code, specs, first-party APIs), not a secondary write-up of them. Follow every
>    claim back to the source that owns it.
> 2. Write the findings to a single Markdown file, citing each claim's source.
> 3. Save it where the repo already keeps such notes; match the existing
>    convention, and if there is none, put it somewhere sensible and say where."

This is the exact skill that generated the task instructions this session was
given (dispatch a background agent, cite primary sources, follow the repo's
existing note convention or say where you put it otherwise) — confirming the
"skills are followed literally, including by the delegating agent that reads them
to write the very instructions handed to a sub-agent" loop is by design, not
accidental. Its brevity is itself a design choice: nothing here needs disclosure
into a second file, so it stays a single in-file step-list.

### `/grilling` (model-invoked, the shared interview primitive)
https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md

- Defines a concrete mental model, the **design tree** and **frontier** ("every
  decision whose prerequisites are already settled"), and a strict process: "Work
  the tree in rounds... Ask the whole frontier in one round... Then wait for the
  user's answers before the next round."
- Draws a hard line on who does what: "Finding facts is your job, never the user's.
  ...The decisions are the user's: put each to them and wait." This is a clean
  division of labor that prevents two common failure modes at once: an agent
  guessing at facts it could look up, and an agent making decisions on the user's
  behalf.
- Defines its own completion criterion precisely: "The session is done when the
  frontier is empty... Do not act on it until the user confirms."
- This single primitive is reused, not re-implemented, by five other skills
  (`grill-me`, `grill-with-docs`, `triage`, `wayfinder`,
  `improve-codebase-architecture`), per the README's Reference section — one
  canonical implementation, five call sites.

### `/codebase-design` (model-invoked, shared vocabulary reference)
https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md

- Opens with an explicit terminology contract: "Use these terms exactly: don't
  substitute 'component,' 'service,' 'API,' or 'boundary.' Consistent language is
  the whole point," then defines Module, Interface, Implementation, Depth, Seam,
  Adapter, Leverage, Locality, each with an explicit "_Avoid_" list of near-synonym
  terms not to use.
- Gives operational heuristics rather than only definitions, e.g. "The deletion
  test. Imagine deleting the module. If complexity vanishes, it was a pass-through.
  If complexity reappears across N callers, it was earning its keep," and "One
  adapter means a hypothetical seam. Two adapters means a real one."
- Has a **Rejected framings** section that names alternatives it deliberately did
  not adopt (Ousterhout's implementation/interface line-count ratio for depth,
  "boundary" as a synonym) and says why. This is a recurring pattern across the
  repo: skills document what they chose *not* to do, which stops the model from
  reintroducing a discarded framing later.

### `/code-review` (model-invoked, two parallel sub-agents)
https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md

- Splits review into two named, independently-run axes, **Standards** and **Spec**,
  and states explicitly why: "A change can pass one axis and fail the other...
  Reporting them separately stops one axis from masking the other."
- Runs both as literal parallel sub-agents with fully specified prompts (diff
  command, commit list, source files, and a word cap: "Under 400 words") so each
  sub-agent's context is isolated and its output is bounded and comparable.
- Carries a fixed Fowler smell baseline (12 named smells, each phrased as *what it
  is* → *how to fix*) that applies "even when a repo documents nothing," but is
  explicitly subordinate to repo-specific standards: "The repo overrides. A
  documented repo standard always wins... Always a judgement call."
- Step 5 explicitly forbids re-merging what step 4 deliberately kept apart: "Do
  not merge or rerank findings, because the two axes are deliberately separate...
  Don't pick a single winner across axes: that's the reranking the separation
  exists to prevent." The skill defends its own design decision against drift
  inside its own instructions.

### `/diagnosing-bugs` (model-invoked, phase-gated with hard stops)
https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md

- States its thesis up front: "This is the skill. Everything else is mechanical. If
  you have a tight pass/fail signal for the bug... you will find the cause;
  bisection, hypothesis-testing, and instrumentation all just consume it."
- Gives 10 ranked concrete ways to build that feedback loop (failing test → curl
  script → CLI+snapshot → headless browser → replayed trace → throwaway harness →
  fuzz loop → bisection harness → differential loop → human-in-the-loop script as
  last resort).
- Enforces the gate explicitly rather than trusting good judgment: "If you catch
  yourself reading code to build a theory before this command exists, stop: jumping
  straight to a hypothesis is the exact failure this skill prevents. No
  red-capable command, no Phase 2." Each phase ends in an explicit checklist (e.g.
  Phase 1's four checkboxes: red-capable, deterministic, fast, agent-runnable)
  rather than a prose description of "done."
- Phase 3 mandates breadth before depth: "Generate 3-5 ranked hypotheses before
  testing any of them. Single-hypothesis generation anchors on the first plausible
  idea," and each must be falsifiable in an explicit template: "If \<X> is the
  cause, then \<changing Y> will make the bug disappear."
- Phase 6 closes the loop back to the artifact created in Phase 1 ("re-run the
  Phase 1 feedback loop against the original... scenario") rather than trusting
  that the fix worked.

### `ask-matt` (user-invoked router)
https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md

Not a skill with domain content of its own; it is a map of every other
user-reachable skill and how they connect ("main flow," "on-ramps," "standalone"),
explicitly kept in sync per `CLAUDE.md`: "whenever you add, rename, remove, or
change how a user-reachable skill fits the flows, re-read `ask-matt`'s `SKILL.md`
and update it so the map stays accurate: a new skill it never mentions, or a stale
one it still routes to, is a router that lies." It also names an explicit resource
budget (the "smart zone," ~150k tokens, linked to
https://www.aihero.dev/ai-coding-dictionary/smart-zone) as the trigger for when to
`/compact` mid-flow, and defers the finer-grained phase-boundary decision to its own
sibling file (`PHASE-BOUNDARIES.md`) rather than inlining it.

## 5. `writing-for-agents`: the repo's explicit theory of its own skill-writing

https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md
and its sibling https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md

This is the most important document for understanding *why* the skills read the
way they do, because it is the repo's own stated theory of instruction design, not
an inference from reading the skills. Selected claims, quoted directly:

- **Context pointers are the unit that matters, not the content behind them:**
  "The pointer's *wording*, not its target, decides when the agent reaches the
  material, and how reliably. A must-have target behind a weakly worded pointer is
  a variance bug: sharpen the wording first, and inline the material only if
  sharpening fails."
- **Two budgets, spent deliberately:** "Context load is the cost of always-loaded
  material on the agent's window... Cognitive load is the cost on the human: which
  documents exist and when to reach for each... Not a cost to minimise: it is the
  price of human agency; spend it where human judgement matters, remove it where it
  does not." This is the theoretical basis for the user-invoked/model-invoked
  split: a user-invoked skill spends zero context load and asks the human to be
  the index; a model-invoked skill spends permanent context load (its always-on
  description) to buy autonomous discoverability.
- **A three-tier information hierarchy:** in-file step (primary, what the agent
  does in order) → in-file reference (consulted on demand, "often a legitimately
  flat peer-set... a fine arrangement, not a smell") → disclosed reference (pushed
  to a separate file behind a pointer). "Branching is the cleanest disclosure test:
  inline what every branch needs, and push behind a pointer what only some
  branches reach." This is exactly why `tdd/SKILL.md` keeps its loop rules inline
  but pushes worked test examples out to `tests.md` and `mocking.md`.
- **Completion criteria as a lever, not decoration:** "A vague bound... invites
  premature completion: ending the step before it is genuinely done." This is
  visibly the mechanism behind `diagnosing-bugs`' checklist-style phase gates and
  `code-review`'s explicit word caps and "do not merge findings" instruction.
- **Leading words** ("a compact concept already living in the model's pretraining
  that the agent thinks with while running the document") are named as a
  deliberate compression technique used throughout the repo: *seam*, *frontier*,
  *tracer bullet*, *tight* (loop), *deep* (module) are all reused, defined-once
  terms that recur across multiple skills rather than being re-explained each
  time.
- **Negation is explicitly flagged as a failure mode to avoid:** "steering by
  prohibition drags the forbidden behaviour into context and makes it more
  available, not less... Prompt the positive." (This is a claim about instruction
  design generally, and it is visibly followed: skill prose in this repo is
  written almost entirely as positive imperatives, e.g. "Test only at pre-agreed
  seams," rather than "don't test untested seams.")
- **Router-skill mechanics**, in `SKILL-MECHANICS.md`: "When user-invoked skills
  multiply past what you can remember, that piled-up cognitive load is cured by a
  router skill: one user-invoked skill that names the others and when to reach for
  each... It can only hint, never fire them: user-invoked skills have no
  description, so nothing but the human can reach them." This is `ask-matt`,
  documented as a named pattern rather than a one-off.

## 6. The plugin-shipping ADR: an example of the repo's own decision-recording discipline

https://github.com/mattpocock/skills/blob/main/.agents/adr/0002-ship-as-a-claude-code-plugin.md

Not directly about skill *content*, but relevant to "why this system works
reliably": the repo applies its own `domain-modeling` discipline (ADRs for
hard-to-reverse, non-obvious, genuinely-traded-off decisions) to itself. The ADR
records a concrete constraint (Claude Code's plugin manifest accepts an explicit
array of skill directory paths; Codex's manifest accepts only a single path string
and doesn't survive symlinks on install) and the decision it forced (ship a native
Claude Code plugin now, defer a native Codex plugin, keep `skills.sh` as the
universal installer), plus a dated verification log entry ("Verified 2026-08-05, on
Claude Code 2.1.222, against the live listing...") rather than an unverified
claim. It is a working example of `docs/engineering/domain-modeling.md`'s own
three-part test for when an ADR is warranted ("hard to reverse," "surprising
without context," "the result of a real trade-off") being applied to the
maintainers' own tooling choice.

## 7. Synthesis: the design principles that make this system work

Grounded in the citations above, not speculation:

1. **One invocation axis, two lanes, hard-separated.** User-invoked skills orchestrate
   and are found only by a human who already knows the name; model-invoked skills
   are the reusable discipline, discoverable by an always-loaded description. The
   invariant "a user-invoked skill can never reach another user-invoked skill"
   (only a human can) prevents ambiguous, agent-decided orchestration chains.
   (`.agents/invocation.md`)

2. **Invocation of a sub-skill is a real tool call, never a hope.** "Call the Skill
   tool with 'X'," one skill per call, is stated as a repo-wide rule, specifically
   because a bare `/name` mention in prose gets a lower hit rate. This is the
   concrete answer to "how do you stop the agent from skipping the skill":
   compliance is engineered into the invocation mechanism, not left to the model
   reading carefully. (`.agents/invocation.md`)

3. **Skills state their own completion criteria as checkable conditions, not
   prose feelings.** `diagnosing-bugs` phase gates, `tdd`'s "no test at an
   unconfirmed seam," `code-review`'s explicit "do not merge the two axes" are all
   instances of the general claim in `writing-for-agents/SKILL.md`: "a vague bound
   invites premature completion." Every representative skill read for this note
   has at least one such explicit, checkable gate.

4. **Reusable vocabulary and reusable process primitives are factored out once and
   called from many places, never re-explained.** `grilling` is one primitive
   reused by five skills; `codebase-design`'s glossary is one primitive reused by
   `tdd` and `improve-codebase-architecture`. This keeps definitions from drifting
   between call sites and keeps each individual skill file short.

5. **Progressive disclosure is a stated design law, not an incidental file
   layout.** The three-tier hierarchy (in-file step → in-file reference →
   disclosed reference behind a pointer) and the "branching is the cleanest
   disclosure test" rule explain, concretely, why `tdd` keeps loop rules inline but
   pushes worked examples to `tests.md`/`mocking.md`, and why `codebase-design`
   keeps its glossary inline but pushes "how to deepen a cluster" to
   `DEEPENING.md`.

6. **Instructions are phrased positively, because negation is explicitly held to
   backfire.** `writing-for-agents/SKILL.md`'s stated reasoning ("the forbidden
   behaviour... becomes more available, not less") is visibly followed across the
   skills read: rules read as "test only at X" rather than "don't test Y."

7. **Every skill names what it deliberately excludes or rejected, not just what it
   does.** `codebase-design`'s "Rejected framings," `code-review`'s "the repo
   overrides" caveat on its own smell baseline, and `.out-of-scope/` at the repo
   root all forestall the model quietly reintroducing a discarded approach.

8. **The system treats itself as a maintained product, with the same rigor it
   asks of the code it helps write.** Promoted vs. non-promoted skill buckets, a
   required docs page per promoted skill, a repo-wide prose style rule (no
   em-dashes), and an ADR-with-verification-log for its own packaging decision are
   all instances of "eat your own dog food": the skills that tell users to write
   tight feedback loops, keep a glossary current, and record hard-to-reverse
   decisions are themselves built and maintained that way.

## 8. Brief comparison with Apple Agent Kit's own architecture

Kept secondary, per the task brief; grounded in `/CLAUDE.md` and
`docs/specifications/skill-spec.md` / `knowledge-spec.md` in this repo.

**Similar in spirit:**
- Both systems separate *routing/process* from *domain content* and forbid a
  routing layer from embedding content directly. Apple Agent Kit: "A Skill routes a
  task to the minimum set of Knowledge Contracts it needs. It holds no domain
  knowledge and no orchestration" (`docs/specifications/skill-spec.md:10-11`).
  mattpocock/skills achieves a related separation differently: model-invoked
  skills like `codebase-design` and `grilling` *are* themselves reusable
  reference/process content, invoked by name from other skills via the Skill tool,
  rather than being forbidden from holding content. The two repos draw the
  "routing vs. content" line in different places: Apple Agent Kit puts all domain
  content in a separate artifact type (Knowledge Contracts) that Skills may never
  embed; mattpocock/skills lets a model-invoked skill *be* the shared reference,
  and only forbids a *user-invoked* skill (a pure orchestrator) from holding
  content of its own.
- Both explicitly forbid routing-type artifacts from calling each other laterally
  in an unstructured way. Apple Agent Kit: "A Skill routes Knowledge Contracts
  only. A Skill never routes to another Skill" (`skill-spec.md:104`).
  mattpocock/skills: a user-invoked skill "can never reach another user-invoked
  one" — the same shape of constraint, but scoped to the user-invoked half only;
  model-invoked skills *do* call each other by design (`tdd` → `codebase-design`,
  `implement` → `tdd` → `code-review`).
- Both cap artifact size to force splitting rather than sprawl. Apple Agent Kit:
  Knowledge Contracts must not exceed 150 lines (`knowledge-spec.md:79`).
  mattpocock/skills has no stated numeric cap, but reaches the same outcome via
  the progressive-disclosure rule in `writing-for-agents/SKILL.md` ("Sprawl is the
  failure mode... The cure is the ladder: disclose reference behind pointers, and
  split by branch or sequence") plus a concrete resource trigger, the "smart zone"
  (~150k tokens) named in `ask-matt/SKILL.md` as the point to `/compact`.

**Different:**
- Apple Agent Kit's four-layer model (References → Knowledge → Skills → Workflows)
  is a strict content pipeline where only Workflows may compose multiple Skills.
  mattpocock/skills has no equivalent fourth "compose-many-skills" layer as a
  distinct artifact type; composition of skills happens *inside* user-invoked
  skills themselves (`implement` invoking `tdd` then `code-review`; `ask-matt`
  describing the whole "main flow" as a path through several skills). The
  discipline that keeps this from becoming spaghetti is the invocation-axis
  invariant (§3 above) rather than a separate Workflow artifact type.
- mattpocock/skills' user/model-invoked split is a distinction Apple Agent Kit's
  spec doesn't currently draw (every Apple Agent Kit skill appears to be
  model-invoked/routing-style); it might be worth asking whether any Apple Agent
  Kit skill is better modeled as a pure human-typed entry point that composes
  others, the way `ask-matt` or `implement` do.
- mattpocock/skills' "leading words" technique (repo-defined, pretraining-anchored
  vocabulary like *seam*, *tight*, *frontier*, reused verbatim across skills) is a
  named compression device that doesn't have a direct analogue described in Apple
  Agent Kit's specs, though Knowledge Contract IDs (`knowledge.<domain>.<slug>`)
  serve a related but more structural (less prose-compression) purpose.
