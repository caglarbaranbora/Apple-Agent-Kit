Status: Research note (not a normative artifact — does not define, alter, or supersede any Knowledge Contract, Skill, Reference, or Workflow in this repo)

# What makes a developer-tool README genuinely good, vs. the boring/skippable kind

Date: 2026-09-10
Researcher: Claude (session for caglarbaranbora)
Purpose: ground a rewrite of this repo's own `README.md` (called "boring" / "cok sikici,
direkt kapatirim" by the project owner) in primary sources — real, live READMEs and the
two platforms that render this one (GitHub repo page, npmjs.com package page) — rather
than generic "how to write a README" advice.

This is pure research: no other file in this repo was modified. `README.md` itself is
untouched; rewriting it is separate follow-up work.

## Context: what's actually wrong with THIS repo's README

Read in full: `README.md` (115 lines) and `npx/README.md` (114 lines, near-duplicate).

Concrete problems, not generic ones:

- **No tagline, no hook, no image.** Line 1 is `# Apple Agent Kit`, line 2 is three
  badges, and the first sentence a reader hits is: *"Apple Agent Kit is a
  source-available, spec-first knowledge system for AI coding agents developing Apple
  platform applications."* This is accurate but it is a definition, not a pitch — it
  reads like the opening line of a spec document, not something written to make a
  stranger keep scrolling. There is nothing visual anywhere in the file — no
  screenshot, no terminal capture of a Skill actually routing and answering a real
  question, nothing that shows the thing working.
- **The payoff is buried past two abstract sections.** `## Overview` and `## Why` both
  restate the same idea ("pre-digests Apple docs into atomic Knowledge Contracts routed
  via Skills") in slightly different words before `## Installation` ever appears at
  line 28. A skimming developer's first-10-seconds question — "what do I run, and what
  do I get" — isn't answerable until after ~27 lines of throat-clearing.
- **`## Goals` is dead weight.** Five bullets ("Reduce token usage," "Improve routing
  accuracy," …) that restate `## Why` in list form and give the reader nothing
  concrete — no number, no example, no before/after. This is the single most skippable
  block in the file: it could be deleted with zero information loss because `## Why`
  already said it in prose.
- **The wall-of-text problem is worst in `## Skills`.** 32 near-identical bullet lines,
  each `**name** — description → link`, with no grouping, no visual break, no sense of
  which ones matter most or where to start. It is a flat, undifferentiated list a
  reader has to either read in full or bounce off of. Compare to how the real-world
  examples below handle a list this long (they don't put it in the README body at all,
  or they group/collapse it).
- **The ASCII architecture diagram is the closest thing to a visual, and it undersells
  itself.** `Apple Documentation ↓ References ↓ Knowledge Contracts ↓ Skills ↓
  Workflows` is a legitimate, distinctive idea (a whole pipeline, not just "we have
  skills") but rendered as five plain lines with down-arrows it looks like a stray
  outline, not a diagram worth pausing on.
- **No demonstration of the actual value proposition.** The core sell — "an agent asks a
  concrete question, gets routed to exactly the right atomic rule instead of
  hallucinating or re-reading everything" — is asserted in prose (`## Why`) but never
  *shown*. There's no before/after, no sample prompt, no "here's what a Skill actually
  returns." A reader has to take the pitch on faith.
- **What's present that nobody needs, at the top:** the license badge and changelog
  badge sit above literally everything else a reader needs to decide whether to keep
  reading. `Status: Stable` / `Version: 2.4.0` as bare text lines (not even part of a
  sentence) between the badges and `## Overview` is metadata that belongs at the bottom
  or in a badge, not competing for the reader's first glance.
- **`npx/README.md` is a near-verbatim duplicate** of the root README (only the "What's
  New" section and one Skill description line differ) — this means whatever gets fixed
  in tone/structure has to be decided once and propagated, not treated as two separate
  writing problems.

## 1. Primary source: five live developer-tool READMEs, read in full

### 1a. `junegunn/fzf` — https://raw.githubusercontent.com/junegunn/fzf/master/README.md (fetched 2026-09-10)

Structure, in order: centered logo image + 5 badges → a merchandise call-to-action
block (unrelated to install, deliberately fun/human) → **one-sentence tagline as plain
prose**, no heading:

> "fzf is a general-purpose command-line fuzzy finder and an interactive terminal
> toolkit."

— immediately followed by a screenshot image (`fzf-preview.png`), then two more
sentences of "why you'd use it," then a `Highlights` section (not `##`, a setext-style
underlined heading) of exactly 4 bullets, each with a bolded one-word label and a
terse justification, using `//` as an inline separator instead of an em dash or colon:

```
- **Portable** // Distributed as a single binary for easy installation
- **Fast** // Optimized to process millions of items in milliseconds
- **Programmable** // Event-driven architecture for building custom terminal interfaces and workflows
- **Batteries-included** // Comes with integrations for Bash, Zsh, Fish, Nushell, Vim, and Neovim
```

Only *after* the tagline, screenshot, and highlights does a `Table of Contents` appear
(auto-generated by a vim plugin, `<!-- vim-markdown-toc GFM -->`), and only after the
ToC does `## Installation` — as the first real content section, before `## Usage`.
The file is 1,153 lines total; the ToC is the load-bearing device that makes that
tolerable — a reader never scrolls past content irrelevant to them, they jump.

### 1b. `BurntSushi/ripgrep` — https://raw.githubusercontent.com/BurntSushi/ripgrep/master/README.md (fetched 2026-09-10)

No image or badge above the fold — the tagline comes first, as the very first line
after a setext `ripgrep (rg)` heading:

> "ripgrep is a line-oriented search tool that recursively searches the current
> directory for a regex pattern. By default, ripgrep will respect gitignore rules and
> automatically skip hidden files/directories and binary files. (To disable all
> automatic filtering by default, use `rg -uuu`.)"

That one paragraph does three jobs at once: says what it is, states the default
behavior a user needs to know before trying it, and shows the flag to override that
default — an actual usage fact, not marketing. Badges (build, crates.io, packaging)
come *after* that paragraph, then a `### Documentation quick links` list (8 links,
each pointing to a `#anchor` or a separate file like `GUIDE.md`/`FAQ.md` — long-form
docs are explicitly *not* in the README body), then a real screenshot, then a full
benchmark table comparing itself to grep/ag/ack/ugrep with exact numbers and a caveat
("a single benchmark is never enough!" with a link to the full blog post). Section
order before `### Installation` (which starts at line 233 of 541):
`### Why should I use ripgrep?` immediately followed by **`### Why shouldn't I use
ripgrep?`** — an honest anti-pitch section listing ripgrep's actual weaknesses (worse
at some non-line-oriented searches, e.g.) before ever asking the reader to install
anything. This is a distinct, citable technique: credibility bought by admitting
limitations before the install command.

### 1c. `cli/cli` (GitHub CLI, `gh`) — https://raw.githubusercontent.com/cli/cli/trunk/README.md (fetched 2026-09-10)

The shortest and sparsest of the five (122 lines). Structure: `# GitHub CLI` → one
`[!IMPORTANT]` GitHub-flavored-markdown admonition (a live operational notice, not
marketing) → **one tagline sentence**:

> "`gh` is GitHub on the command line. It brings pull requests, issues, and other
> GitHub concepts to the terminal next to where you are already working with `git` and
> your code."

— immediately followed by one screenshot (`gh pr status`), then one sentence on
supported platforms. Notably, `## Installation` here is *not* a single visible command
— it's four collapsed-by-OS subsections (`macOS`, `Linux & Unix`, `Windows`, `Build
from source`), each just 2-3 links out to a dedicated `docs/install_*.md` file. This is
the counter-example to "always show the command inline": when install genuinely
differs by platform/package-manager, `gh` chooses to route rather than dump every
package-manager command into the README body. Everything past "why + screenshot +
where to install" is demoted: a `## Documentation` section that is literally one
sentence pointing to an external manual site, an `## Agent skills` section with two
copy-pasteable commands, `## Contributing` (one link), then binary-verification detail
and a `## Comparison with hub` section — both placed *last*, after everything a new
user needs.

### 1d. `sharkdp/bat` — https://raw.githubusercontent.com/sharkdp/bat/master/README.md (fetched 2026-09-10)

Centered logo SVG + 3 badges + a one-line tagline *inside the same centered block*:

> "A *cat(1)* clone with syntax highlighting and Git integration."

— then, distinctively, a **second-line nav bar of anchor links** right under the
tagline, acting as a miniature table of contents before any content:

```
Key Features • How To Use • Installation • Customization • Project goals, alternatives
```

plus locale links to translated READMEs (zh/ja/ko/ru). The load-bearing structural
choice: **`## How to use` comes before `## Installation`** (confirmed by heading line
numbers: `## How to use` at line 54, `## Installation` at line 243). Before either,
three `###` feature subsections (`Syntax highlighting`, `Git integration`, `Show
non-printable characters`) each pair one sentence of prose with one screenshot image —
show, then tell, three times, before asking for an install. `## Installation` itself is
the single longest section (lines 243–456, ~213 lines) — 15+ per-OS/per-package-manager
subsections — but it's positioned *after* the reader has already seen the tool work,
and a `Packaging status` badge (repology) sits at the top of that section as a visual
index of "is this on your OS's package manager" before the per-OS prose begins.

### 1e. `mattpocock/skills` — https://raw.githubusercontent.com/mattpocock/skills/main/README.md (fetched 2026-09-10)

The most directly comparable example (an "AI agent skills package" README, same
category as this repo). Structure: `# Skills For Real Engineers` → one badge → tagline
as a **value judgment, not a feature list**:

> "My agent skills that I use every day to do real engineering - not vibe coding."

— then a short paragraph that names competitors and explicitly rejects their approach
before explaining its own:

> "Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to
> help by owning the process. But while doing so, they take away your control and make
> bugs in the process hard to resolve."

then one more sentence of positioning ("small, easy to adapt, composable... based on
decades of engineering experience"), then a newsletter call-to-action, **then**
`## Installation (30-second setup)` — with the "30-second" promise stated directly in
the heading. Installation is presented as *"Two ways in, two philosophies"* and uses
`<details><summary>` collapsible blocks per install method (Claude Code plugin vs.
`skills.sh` vs. "for tinkerers") — each collapsed block hides its own command until
clicked, keeping the visible README short while still holding three install paths.
After installation, `## Why These Skills Exist` reframes the whole tool as **the fix
for four named failure modes**, each anchored with a real book quote (Pragmatic
Programmer, Eric Evans' DDD, Kent Beck, Ousterhout) — turning an abstract "why" into
four concrete problem→fix pairs, each with a one-line "Problem" and one-line "Fix" and
a link to the specific skill that solves it. The 30+-item skill catalogue (comparable
to this repo's own 32-Skill list) is pushed to the very bottom under `## Reference`,
split first by an axis the reader actually cares about (**user-invoked** vs.
**model-invoked** skills, explained in one paragraph before the split), then by
category (`### Engineering`, `### Productivity`) — never one flat 32-line list.

## 2. Platform primary sources: how this README is actually rendered

### 2a. GitHub — "About READMEs"

https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
(fetched 2026-09-10)

- GitHub auto-surfaces a README only from specific locations, in a fixed priority
  order: *"the file shown is chosen from locations in the following order: the
  `.github` directory, then the repository's root directory, and finally the `docs`
  directory."* (This repo's README is at root — correct placement, no action needed.)
- What a README is expected to cover, per GitHub's own guidance: *"What the project
  does," "Why the project is useful," "How users can get started with the project,"
  "Where users can get help with your project," "Who maintains and contributes to
  your project."* — five questions, not a prescribed section list.
- **GitHub renders a table of contents automatically** from heading structure
  ("GitHub will automatically generate a table of contents based on section
  headings," reachable via the outline icon on the rendered page) — so a repo does not
  need to hand-maintain a ToC the way `fzf` does; headings alone are enough for GitHub
  to expose navigation. This repo's README currently has no ToC at all (hand-written or
  auto) and 8 top-level `##` sections — short enough that GitHub's built-in outline icon
  is sufficient; a hand-rolled ToC (`fzf`'s technique) is warranted at `fzf`-scale
  (1,153 lines), not at this file's current ~115.
- **Link hygiene**: *"Relative links are easier for users who clone your
  repository — absolute links may not work in clones of your repository."* This repo's
  README already does this correctly (e.g. `[CHANGELOG.md](CHANGELOG.md)`,
  `[SKILL.md](skills/style-guide/SKILL.md)`).
- **Explicit scope boundary, directly relevant to the Skills-list bloat problem**: *"A
  README should only contain information necessary for developers to get started using
  and contributing to your project. Longer documentation is best suited for wikis."*
  This is GitHub's own authority for demoting the full 32-Skill catalogue and long
  routing detail to `skills/index.md` (which this repo already has) rather than
  growing it in the README body.
- Hard technical ceiling: *"When your README is viewed on GitHub, any content beyond
  500 KiB will be truncated."* Not a binding constraint for this repo today, but a
  reason not to inline large content (e.g. a big architecture diagram as raw ASCII
  art repeated per-domain) directly into the README.

### 2b. npm — "About package README files"

https://docs.npmjs.com/about-package-readme-files (fetched 2026-09-10)

- *"An npm package `README.md` file **must** be in the root-level directory of the
  package."* This repo's `npx/README.md` already satisfies this (it's `npx/`'s
  package root, matching `npx/package.json`).
- *"the `README.md` is rendered as GitHub Flavored Markdown via GitHub's API"* — so
  anything valid in the GitHub-rendered root README (badges, GFM tables, relative
  image links resolved against the *published* package, not the monorepo) is safe to
  reuse in `npx/README.md`, but relative links to files outside the `npx/` package
  directory (e.g. `../CHANGELOG.md` or root `skills/`) will not resolve the same way
  on the npm package page as they do on the GitHub repo page — worth flagging for the
  eventual rewrite since both READMEs currently link to files like `CLAUDE.md`,
  `LICENSE`, `.codex/INSTALL.md` that live outside `npx/`.
- *"The `README.md` file will only be updated on the package page when you publish a
  new version of your package."* Directly relevant to this repo's own convention (per
  `CLAUDE.md`: *"Shipping a new domain or Skill does NOT require an npm publish"*) —
  it means `npx/README.md` on npmjs.com will visibly drift from the GitHub root
  README between npm publishes, reinforcing why `npx/README.md` should be written as
  a deliberately short, install-focused document rather than a synced copy of the
  full root README (which is what it currently is — a near-verbatim duplicate, per
  the Context section above).
- Suggested content for a package README, per npm's docs: installation directions,
  configuration instructions, usage information — npm's own framing is narrower and
  more install/usage-focused than GitHub's five-question framing, which supports
  giving `npx/README.md` a tighter, install-first scope than the root README.

## 3. Synthesis: concrete structural principles for this repo's README rewrite

Each principle below is grounded in a specific example above, not generic advice.

1. **Open with one sentence that is a pitch, not a definition — and put it before the
   badges compete for attention.** Every one of the 5 examples leads with a single,
   punchy sentence a stranger can parse in under 5 seconds (`fzf`: "a general-purpose
   command-line fuzzy finder and an interactive terminal toolkit"; `ripgrep`: what it
   searches + its one distinguishing default; `gh`: "GitHub on the command line";
   `bat`: "A cat(1) clone with syntax highlighting and Git integration";
   `mattpocock/skills`: "agent skills... to do real engineering — not vibe coding").
   This repo's current line 12 ("Apple Agent Kit is a source-available, spec-first
   knowledge system for AI coding agents developing Apple platform applications") is
   accurate but reads as a definition for a glossary, not a pitch. Rewrite it as what
   it *does for the reader* in one line, in the shape those five use.

2. **Show the thing working before explaining the architecture that makes it work.**
   `bat` and `fzf` put screenshots directly under the tagline; `ripgrep` puts a
   screenshot *and* a benchmark table before `### Installation`. This repo's README has
   zero screenshots/transcripts and instead opens with two prose sections (`## Overview`,
   `## Why`) that assert the value rather than demonstrate it. The highest-leverage
   single addition: a short, real transcript — an agent asking a concrete Apple-platform
   question, the Skill routing it, the Knowledge Contract answer coming back — shown as
   a code block near the top, before `## Installation`. That is the one thing none of
   `## Overview`/`## Why`/`## Goals` currently do: prove the routing claim instead of
   stating it.

3. **Cut `## Goals` entirely; it duplicates `## Why` with zero new information.**
   None of the 5 examples carry a bullet list that just restates the pitch a second
   time in list form. Where an example does use a short bulleted list near the top
   (`fzf`'s 4-item "Highlights"), each bullet adds a *new*, distinct, concrete claim
   with its own justification — not a rephrasing of the sentence above it. If this
   repo keeps a "why" bullet list at all, it should read like `fzf`'s Highlights
   (one bold word + one concrete justification each) or like `mattpocock/skills`'
   four Problem→Fix pairs (each anchored to a specific, real failure mode and the
   specific Skill/Workflow that addresses it) — not restated goals.

4. **Never inline a 30+-item flat catalogue in the README body — GitHub says so
   directly, and every comparable example agrees in practice.** GitHub's own guidance
   ("Longer documentation is best suited for wikis") and `mattpocock/skills`'
   real-world handling (splits its 30+ skills by an axis the reader cares about —
   user-invoked vs. model-invoked — *before* subdividing by category, and only at the
   very bottom, under `## Reference`) both point the same direction: this repo's
   32-line flat `## Skills` bullet list (the single worst wall-of-text in the current
   file) should either (a) move fully to `skills/index.md` (which already exists) with
   only a 4-6 item "start here" sample staying in the README, or (b) stay but grouped
   by the same kind of reader-relevant axis `mattpocock/skills` uses (e.g. by Apple
   framework area) rather than one undifferentiated list.

5. **Installation placement should match how uniform the install command actually is —
   don't default to "always show it inline."** `fzf`, `ripgrep`, and
   `mattpocock/skills` all show (or link straight to) one clear command early because
   their install genuinely is close to one command. `gh` deliberately does *not* inline
   per-OS commands — it routes to `docs/install_*.md` because install legitimately
   varies by platform/package-manager. This repo's actual install is already a single
   line (`npx apple-agent-kit`) with one caveat (Codex users get different
   instructions) — closer to the `fzf`/`mattpocock/skills` case — so it's correct to
   keep it visible early and inline (as it already is, at README.md line 30-34), but
   `mattpocock/skills`' `<details><summary>` collapsible-per-method pattern is worth
   adopting once/if this repo needs to show *both* the Claude Code path and the Codex
   path as equally-weighted options instead of the current "primary path, Codex
   mentioned as an aside" framing.

6. **An honest limitations/non-goals line builds more trust than another benefit
   bullet.** `ripgrep`'s `### Why shouldn't I use ripgrep?` section, placed *before*
   installation, is a distinct, deliberate technique: it spends space on the tool's
   real weaknesses before ever asking for a commitment, and that section exists
   *alongside*, not instead of, the "why you should" section. This repo has
   architecture/scope material that could support an equivalent move (e.g. this repo
   already has `docs/architecture/domain-map.md` describing what's in/out of scope by
   domain) — a short, honest "what this doesn't do yet" line near the top would be a
   novel-for-this-repo trust signal none of the current sections attempt.

7. **`Status:`/`Version:` metadata and badges are back-of-the-file material, not
   first-glance material.** None of the 5 examples put bare "Status: X / Version: Y"
   text lines between the badges and the pitch the way this repo's README does at
   lines 7-8. Badges in the strong examples either sit inline with the tagline (`bat`)
   or immediately after it (`ripgrep`), never as a standalone metadata block a reader
   has to get past before reaching a single sentence about what the tool does.

8. **`npx/README.md` should stop being a near-duplicate of the root README.** Per npm's
   own docs, the npm package page only updates on `npm publish` (which, per this repo's
   own `CLAUDE.md`, happens far less often than content ships to `main`), and its
   relative links resolve against the published `npx/` package directory, not the
   monorepo root — so links like `CLAUDE.md`, `LICENSE`, `.codex/INSTALL.md` (which live
   outside `npx/`) are a real risk of rendering as dead links on npmjs.com even though
   they work fine on GitHub. `npx/README.md` should be rewritten as a short,
   install-focused document (per npm's own narrower "installation, configuration,
   usage" framing) rather than carrying the full pitch/architecture/Skills-catalogue
   content that belongs on the GitHub-rendered root README.
