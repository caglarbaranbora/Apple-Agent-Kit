# Style Guide Glossary Curation Proposal

Status: Approved
Version: 0.2.0

Source: https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf (A-Z glossary, 1,706 terms)
Purpose: propose which terms to ingest into knowledge/style-guide/ and how to cluster them, per [[0001-style-guide-domain-and-domain-roadmap]] (../../../rfcs/0001-style-guide-domain-and-domain-roadmap.md) decision 9.

v0.2.0 supersedes v0.1.0's cluster list after an architecture review focused on
AI routing, atomicity, reuse, and long-term scale rather than human-readable
grouping. No terms were re-extracted from the PDF; this is a pure
restructuring of the term lists already gathered. Approved 2026-07-30 —
Task 10 drafting is underway against this cluster list.

---

# Revised Cluster Architecture

Flat directory (`knowledge/style-guide/*.md`, no subfolders — see "Why the
hierarchy stays flat" below), 19 clusters:

| # | Cluster | ~Terms | Reused by (beyond style-guide) |
|---|---|---|---|
| 1 | `capitalization-of-apple-proper-nouns` | 41 | every domain (product/feature names) |
| 2 | `capitalization-style-rules` | 4 | every domain (sentence-vs-title case) |
| 3 | `general-button-labels` | 4 | every domain with buttons |
| 4 | `sign-in-and-authentication-terminology` | 9 | Authentication, AuthenticationServices |
| 5 | `authentication-credentials-and-biometrics` | 9 | Authentication, Security |
| 6 | `presentation-surfaces` | 20 | every domain (alerts/sheets/pickers) |
| 7 | `navigation-controls` | 6 | every domain |
| 8 | `input-controls` | 7 | every domain, esp. Settings/Widgets |
| 9 | `status-and-progress-indicators` | 4 | every domain |
| 10 | `touch-gesture-verbs` | 19 | every domain |
| 11 | `pointer-and-click-terminology` | 10 | iPad/Mac Catalyst domains |
| 12 | `ui-action-verbs` | 50 | every domain (highest-reuse cluster) |
| 13 | `abbreviations-and-acronyms` | 12 | every domain |
| 14 | `numeric-terminology-supplement` | 6 | narrow — numbers not already covered |
| 15 | `app-state-and-error-terminology` | 14 | every domain |
| 16 | `instructional-voice-and-phrasing` | 16 | every domain (tone/POV) |
| 17 | `connectivity-and-media-terminology` | 14 | Notifications, Widgets (future) |
| 18 | `app-chrome-and-window-terminology` | 10 | Settings, Mac Catalyst |
| 19 | `punctuation-and-typography-in-text` | 7 | every domain |

**Content-format note for Task 10:** clusters with 20+ terms (1, 6, 10, 12)
cannot fit the chapter-contract prose format (`### Rule N` + paragraph +
dedicated example pair) under the 150-line cap — 40+ terms at ~3 lines each
already exceeds it before metadata and examples are counted. These clusters
MUST use a compact table-style `## Rules` section (one line per
term: correct form → avoid form → one-clause reason), with example pairs
grouped by sub-theme rather than one pair per term. This is a second,
legitimate content shape for glossary-sourced terminology contracts,
distinct from the prose-rule shape used for the 6 chapter contracts already
built — both are valid `type: knowledge` contracts, they just fit different
source material. If a table-format cluster still can't fit 150 lines once
drafted, split it by sub-theme at that point (e.g. `ui-action-verbs` into
`ui-action-verbs-core` / `ui-action-verbs-avoid`) rather than raising the cap.

---

# Change Log

**Merge: `capitalization-of-product-names` + `capitalization-of-system-features-and-services` → `capitalization-of-apple-proper-nouns`**
Reason: same rule shape (capitalize this Apple noun exactly as styled, don't pluralize/verb/possessive it), different noun lists only. An agent writing "the App Store" vs "iPhone" is asking the identical question — splitting by product-vs-feature is an arbitrary boundary with no natural routing signal (fails the Routing criterion's "obvious ownership" test). Merging also maximizes reuse: this is the one cluster nearly every future domain (StoreKit → "App Store", WidgetKit → "Widget", UserNotifications → "Notification Center") will `related:` against.

**Kept separate: `capitalization-styles-sentence-vs-title` → renamed `capitalization-style-rules`**
Reason: this is not a proper-noun list, it's a generic mechanical rule (when to use sentence-style vs. title-style case) that applies to every button/header an agent writes, Apple-noun or not. Different query shape from #1 ("how do I capitalize *this specific term*" vs "what casing style does *this kind of label* use") — merging would blur two genuinely different routing questions into one file.

**Split: `sign-in-and-general-buttons` → `general-button-labels` + `sign-in-and-authentication-terminology`**
Reason: two distinct reuse profiles. "Button", "OK", "allow", "user name" are needed by every domain with a button (Widgets, StoreKit, Notifications) — a Widget-writing agent shouldn't have to load sign-in vocabulary to get "OK" conventions. Splitting also gives an exact 1:1 target for the plan's Task 11/12 refactor: `knowledge/authentication/button-labels.md` → `depends_on: general-button-labels`, `knowledge/authentication/sign-in-terminology.md` → `depends_on: sign-in-and-authentication-terminology`. The single merged cluster from the original proposal would have forced both auth files to depend on the same over-broad contract.

**Rename + absorb: `dialogs-menus-and-popups` → `presentation-surfaces`, gains `picker`/`color picker`/`date picker` (moved out of the old controls cluster)**
Reason: renamed to match Apple HIG's own vocabulary for this concept (generic "presentation," not just "dialog") since other domains will `related:` against it and should recognize the name. Pickers moved in because a picker is a presentation surface (usually appears in a sheet), not an interactive control in the same sense as a checkbox or slider — grouping it with sheets/popovers/menus gives cleaner ownership than leaving it in a controls grab-bag.

**Split: `buttons-and-controls-naming` (28 terms) → `navigation-controls` + `input-controls` + `status-and-progress-indicators`**
Reason: this was a heterogeneous catch-all (navigation chrome, form inputs, progress UI, plus stray terms) — fails atomicity (an agent building a settings toggle would load Back-button and progress-bar vocabulary it doesn't need) and fails Domain Ownership (no single coherent "when do I load this" story). Split by actual UI role: navigation (`Back button`, `More button`, disclosure arrow/button, up arrow), input (`checkbox`, `radio button`, `slider`, `stepper`, `switch`, adjuster, incrementer), status (progress-indicator variants, badge, index/alphabet column). `library` and `Trash` are reassigned to `capitalization-of-apple-proper-nouns` — they're proper-noun capitalization concerns (Apple system feature names), not control-naming concerns; they were misfiled in the original proposal.

**Merge: `core-ui-action-verbs` + `action-verbs-avoid-list` + `power-and-toggle-state-terminology` → `ui-action-verbs`**
Reason: correct-verb and avoid-verb are two sides of one lookup — every existing contract in this domain already pairs "use X" with "not Y" inside one file's Compliant/Non-Compliant sections (that's the established template shape), so a *separate cluster* for the avoid-list duplicates that pattern at the wrong granularity. `power-and-toggle-state-terminology` (6 terms, all "turn on/off" vs "power on/off"/"enable") is itself just one more verb-pair family — keeping it as a standalone 6-term file violates the Token Efficiency criterion ("prefer one concise contract over three tiny ones when almost always loaded together"). This is now the domain's single highest-reuse cluster (every UI-text-writing task touches action verbs) and, per the content-format note above, must use the compact table format to fit.

**Shrink + rename: `numbers-and-time-in-text` → `numeric-terminology-supplement`, most terms dropped**
Reason: the original 20-term list duplicated three already-built contracts — `GB`, `inch`, `mm`, `percent`, `degrees` duplicate `units-of-measure.md`; `dates`, `time of day`, `time zone`, `a.m./p.m.` duplicate `international-formatting.md` Rule 1; `phone numbers` duplicates `international-style.md` Rule 4. Ingesting them again would violate the "no duplicated rules" rule that Task 6's own review already had to fix once for a similar overlap. Kept only the genuinely uncovered terms: `aspect ratio`, `fractions`, `version number`, `x` (resolution notation), `step` (as in step-by-step instructions), `zip code`. `related:` must point at all three existing numeric contracts so the gap is visibly intentional, not an oversight.

**Split: `general-word-choice-avoid-list` (29 terms) → `app-chrome-and-window-terminology` + `punctuation-and-typography-in-text`, remainder dropped**
Reason: this was the original proposal's junk-drawer cluster — legal/business words, UI chrome, typography, file/window concepts, and symbols had no shared routing story. Split into two coherent clusters: chrome/window (`window`, `document`, `homepage`, `launch`, `Launchpad`, `default`, `mode`, `system`, `tooltip`, `parental controls`) and punctuation/typography (`ampersand`, `exclamation points`, `ellipsis`, `typeface`/`type size`/`type style`). Dropped entirely as low-value for an app-UI-text-writing agent: `grandfathered`, `free`, `professional`, `third-party`, `support`, `resize`, `over`, `new`, `latest`, `localizable`, `one-click` — these are either generic English (no Apple-specific rule) or legal/marketing terms outside this project's stated scope (app UI text, not marketing copy or legal boilerplate).

**Unchanged:** `authentication-credentials-and-biometrics`, `touch-gesture-verbs`, `pointer-and-click-terminology`, `abbreviations-and-acronyms`, `app-state-and-error-terminology`, `instructional-voice-and-phrasing`, `connectivity-and-media-terminology` — each already had a single coherent theme, an obvious routing story, and no overlap with any other cluster or existing contract.

---

# Routing Analysis

**Routing.** Every remaining cluster now answers one unambiguous question. The
biggest prior failure was `buttons-and-controls-naming` and
`general-word-choice-avoid-list` — both required an agent (or the human
routing table in `skills/style-guide/writing.md`) to already know which
grab-bag a term landed in before it could route there. Post-split, "what do I
call this toggle" → `input-controls`, "what do I call this modal" →
`presentation-surfaces`, with no cluster whose name doesn't predict its
contents.

**Token efficiency.** Net effect is roughly cluster-count-neutral (18 → 19)
but that number is misleading: three genuine merges removed real duplication
and consolidated near-certain co-loads (proper-noun capitalization; verbs
correct+avoid+toggle), while the count only grew because two incoherent
grab-bags were split into clusters an agent will *actually load selectively*
instead of always pulling the whole grab-bag. Net token cost per real task
goes down even though file count is flat, because agents now load 1-2
precisely-scoped contracts instead of 1 oversized one.

**Reuse.** Explicitly tagged reuse potential in the architecture table above.
`ui-action-verbs`, `capitalization-of-apple-proper-nouns`,
`capitalization-style-rules`, `presentation-surfaces`, and the three controls
clusters are structured so that Tier 1/2 domains (SwiftUI, UIKit, WidgetKit,
App Intents, UserNotifications) can `related:` against them directly instead
of each domain re-deriving its own terminology rules — this is the payoff of
merging by *rule shape* rather than by *source glossary section*.

**Maintainability.** The two 1:1 splits (`general-button-labels` /
`sign-in-and-authentication-terminology`) remove a future footgun: had the
original merged cluster shipped, both `depends_on` refactors in Task 11/12
would have pointed at the same over-broad file, and any future edit to
sign-in wording would have force-reviewed every button-label consumer too.

---

# Future Impact

**At 40+ contracts** (roughly where `style-guide` lands once these 19
clusters plus the 6 chapter contracts are drafted): the flat directory is
still trivially browsable, and `skills/style-guide/writing.md` (currently
routing to 6 files) will need to grow — but the 60-line Skill cap
(`docs/specifications/skill-spec.md`) will force that growth into multiple
Skill files by itself, e.g. `skills/style-guide/terminology.md`,
`skills/style-guide/controls-and-surfaces.md`,
`skills/style-guide/voice-and-formatting.md`. This is the architecture's
existing, designed scaling mechanism — no new mechanism needs inventing.

**At 80+ contracts** (style-guide fully saturated, plus other domains'
`related:` links pointing back into it): still comfortable per-domain, since
no single domain is likely to individually exceed ~40-50 files even at full
build-out. The place to watch is `skills/index.md`, which is currently one
flat discovery table — at this scale it may need per-domain index files
rather than one growing table, but that's a `skills/index.md` concern, not a
`knowledge/style-guide/` one, and is out of scope for this review.

**At 150+ contracts** (project-wide, across all 27 roadmapped domains): this
scales by design because directory browsing was never the routing mechanism
— `AGENTS.md` already mandates deterministic routing through Skills and
References, never repository-wide search or folder traversal. A domain's
internal file count is irrelevant to how an agent finds a contract; only the
Skill's routing table and the `references/apple/<domain>/` index matter, and
both stay small by construction (60-line and 80-line caps respectively).

**Why the hierarchy stays flat (no `00-foundations`/`10-writing`/etc.
numbered folders):** numbered category folders would improve nothing for AI
routing — agents never browse `knowledge/style-guide/`, they follow the
Skill's explicit file-path table, so folder position carries zero routing
signal. What they *would* cost: every `id:`/`depends_on:`/`related:`
reference and every relative-path + wikilink pair is already tied to a file
path; introducing numbered folders means moving files, breaking every
existing link, and — worse — a renumbering problem the moment a new category
needs to be inserted between two existing numbers (e.g. discovering a
"gestures" category belongs between `20-terminology` and `30-controls` after
`30` is already taken). A flat directory with consistent thematic slug
prefixes (`capitalization-*`, `ui-action-verbs`, `presentation-surfaces`)
already gives humans alphabetical clustering in Obsidian for free, with none
of the churn risk. If per-domain file count ever genuinely becomes
unmanageable, the correct lever is more Skill files (already designed for
this), not a folder taxonomy layered on top of an architecture that
explicitly routes through Skills, not paths.

---

No Knowledge Contracts were created, no Apple documentation was
re-extracted, and no glossary entries were rewritten in this revision — this
document only restructures the term lists already gathered in v0.1.0.
