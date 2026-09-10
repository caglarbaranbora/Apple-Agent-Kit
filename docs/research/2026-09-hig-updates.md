# HIG "New and Updated" Research — September 2026

Status: Research note (not a normative artifact — not a Reference/Knowledge/Skill/Workflow)

## Context

Apple held a launch event on 2026-09-09. The HIG landing page
(https://developer.apple.com/design/human-interface-guidelines) currently lists
a "New and updated" section with six entries: **Branding, SharePlay, Layout,
Menus, Siri, Snippets**. This note investigates what changed on each of those
six pages, live-fetched via browser on 2026-09-10.

A seventh new page, "Designing for iPhone Duo" (foldable iPhone), also appears
on the landing page under "Design fundamentals" but is explicitly **out of
scope** for this note — it's being handled separately.

## Headline finding

Only **half** of the six pages actually carry a change-log entry dated
2026-09-09/10. **Branding, SharePlay, and Layout** have a Change log row dated
**September 9, 2026**. **Menus, Siri, and Snippets**, despite appearing in the
landing page's "New and updated" module, have no change-log entry newer than
**June 8, 2026** — verified by fetching each page twice. This is worth flagging
to whoever maintains the "New and updated" copy on Apple's side, and it means
readers should not assume everything in that module reflects the Sept 9 launch
event specifically. Reported per-page below regardless — the module still
signals "look at this page," even where the change log doesn't confirm a
launch-day edit.

---

## Branding — EDIT

- URL: https://developer.apple.com/design/human-interface-guidelines/branding
- Change log (verbatim): **September 9, 2026 — "Refined guidance for using brand color."**
- Type: EDIT to an existing, long-standing page.

### What changed

The "Best practices" section's brand-color guidance now reads as more
restrictive/nuanced than a simple "apply your accent color" instruction. The
live page currently says:

> "Apply your app's accent color judiciously. Using your brand color too
> broadly can overwhelm your interface and dilute its impact. Minimize its use
> on controls and instead use it intentionally for primary actions or status
> indicators, like badges for unread content or an icon for the selected tab
> in a tab bar. To express your brand through color, consider moving it into
> the content layer, where it scrolls beneath Liquid Glass controls and gets
> picked up dynamically."

That's the "refined" guidance called out in the change log: brand color should
be minimized on controls, reserved for primary actions/status indicators, and
ideally pushed into the content layer so it's picked up dynamically beneath
Liquid Glass controls — a materially more specific rule than "apply an accent
color to icons/buttons/text."

### Repo coverage

`knowledge/human-interface-guidelines/branding.md` exists and covers this
topic (Rule 2: "Agents MAY specify an app accent color applied to interface
icons, buttons, and text"). This rule is now stale relative to the live page:
it doesn't capture the "minimize use on controls," "reserve for primary
actions/status indicators," or "move brand color into the content layer
beneath Liquid Glass" guidance. `references/apple/human-interface-guidelines.md`
lists Branding as a Primary Topic and cites the same source URL.
**Gap: Rule 2 needs updating to reflect the new color-restraint guidance.**

---

## SharePlay — EDIT (to a page that pre-dates this repo's coverage entirely)

- URL: https://developer.apple.com/design/human-interface-guidelines/shareplay
- Change log (verbatim): **September 9, 2026 — "Reorganized best practices, expanded visionOS guidance, and added a section on custom templates."** (Prior entries: Dec 5 2023, Jun 21 2023, Dec 19 2022 — this page has existed since at least 2022.)
- Type: EDIT to a long-standing page, not a new page.

### What changed

Per the change log itself: best practices were reorganized, visionOS guidance
was expanded, and a **new "Custom templates" subsection** was added. The live
page's "Custom templates" section is new content covering: defining a custom
spatial-Persona seat arrangement when none of the system templates
(side-by-side, surround, conversational) fit; accounting for people physically
together in the same room; seat orientation control; supporting up to five
spatial Personas; minimum 1-meter seat spacing; seat-fill ordering; and keeping
app roles independent of seat assignments (citing `isSpatial` and
`isNearbyWithLocalParticipant`). The "Spatial templates" section (describing
the three system templates) also reads as expanded/reorganized relative to
what a "expanded visionOS guidance" note implies.

### Repo coverage

`grep -ril -i shareplay references/ knowledge/ skills/` returns **zero
results**. SharePlay has no Reference file, no Knowledge Contract, and no
Skill anywhere in this repo. This is a full coverage gap, independent of
today's edit — SharePlay as a domain (real-time shared activities, Group
Activities framework, spatial templates, visionOS Personas) isn't modeled at
all in Apple Agent Kit.

---

## Layout — EDIT

- URL: https://developer.apple.com/design/human-interface-guidelines/layout
- Change log (verbatim): **September 9, 2026 — "Updated guidance to reflect current best practices."** (Prior entries date back to Sept 2022, including device-spec additions and a June 9 2025 "Added guidance for Liquid Glass" entry.)
- Type: EDIT to existing, well-established page.

### What changed

The change-log wording is generic ("current best practices") rather than
naming a specific new subsection, so no clean diff is available from Apple's
own log. Reading the live page in full, the following content is present that
is **not** reflected in the repo's Knowledge Contract:

- A "Differentiate controls from content" best practice: use the Liquid Glass
  material to distinguish controls from content instead of a solid/semi-opaque
  background; use a scroll edge effect to visually elevate controls above
  content; and a **background extension effect**
  (`backgroundExtensionEffect()` / `UIBackgroundExtensionView`) that flips and
  blurs a background image to make it appear to extend beneath sidebars/
  inspectors/toolbars.
- An explicit "Guides and safe areas" section defining layout guides
  (`UILayoutGuide`/`NSLayoutGuide`) and safe areas as distinct formal concepts.
- A formal "Size classes" section (compact/regular horizontal & vertical,
  `UITraitChangeObservable`, `UserInterfaceSizeClass`) with explicit guidance
  to design for size-class combinations, not device type/orientation.
- Platform-specific subsections for macOS (avoid controls at window bottom,
  camera-housing safe-area compatibility mode), tvOS (60pt/80pt safe-area
  insets, grid-column pixel specs), visionOS (window/volume resizing, 3D
  content placement, ornament vs. adjacent-window guidance, 60pt control
  spacing), and watchOS (2-3 control limit, autorotation).

Note: because the Liquid Glass material itself was introduced via a June 9,
2025 change-log entry (pre-dating this research window), the Liquid Glass
*mention* isn't new as of Sept 9 — but since the KC has never been updated to
mention Liquid Glass at all, it's still a gap either way.

### Repo coverage

`knowledge/human-interface-guidelines/layout.md` exists (6 rules: safe areas,
Dynamic Type layout adaptability, reading-order placement, grouping,
iPad-multitasking-size testing, full-bleed background extension). It covers
the broad strokes (Rules 1, 5, 6 map to safe areas / multitasking sizes /
full-bleed) but has **no rule addressing**: Liquid Glass control
differentiation, the background extension effect API, formal size-class
terminology/APIs, or any of the per-platform specifics (tvOS grid specs,
visionOS window/ornament guidance, watchOS control-count limit). Given the
change-log note is a general refresh rather than a single new feature, this
reads as the KC having fallen behind the source page over time rather than one
discrete new item to add.

---

## Menus — no Sept 2026 change-log entry found (see headline finding)

- URL: https://developer.apple.com/design/human-interface-guidelines/menus
- Change log (verbatim, most recent row): **June 8, 2026 — "Updated guidance for menu item icons."** No 2026-09-09 or 2026-09-10 entry exists on this page as fetched (checked twice).
- Type: N/A for this research window — nothing to report as a Sept 2026 content change on Apple's own change log, despite the page's inclusion in the landing page's "New and updated" module.

### Repo coverage (for context)

`knowledge/human-interface-guidelines/menus.md` exists and is reasonably
current with the live page's June 8, 2026 icon-consistency guidance (Rule 5:
"apply icons consistently within a group"). `references/apple/
human-interface-guidelines-components.md` lists Menus as a Primary Topic. No
action needed from this research pass since no Sept-dated change was found.

---

## Siri — no Sept 2026 change-log entry found (see headline finding); large scope gap regardless

- URL: https://developer.apple.com/design/human-interface-guidelines/siri
- Change log (verbatim, most recent row): **June 8, 2026 — "Revised for Siri AI."** No 2026-09-09 or 2026-09-10 entry exists on this page as fetched (checked twice).
- Type: N/A for this research window as far as Apple's change log is concerned — the most recent substantive change (the Siri AI / Apple Intelligence revision) is dated June 8, 2026, not September.

### Content, for scope-gap purposes

The live page describes Siri as powered by Apple Intelligence, covers
exposing app actions/content via App Intents and "app schemas" (preset
templates for common domains like email/music/photos), donating entities to
the on-device Spotlight index, donating actions/intents so Siri can anticipate
future requests, and links out to "Snippets" for the interactive-response UI.

### Repo coverage

`references/apple/app-intents.md` explicitly excludes, in its "Out of scope
for v1" note: "legacy SiriKit donation-based intents," "custom Siri vocabulary
and AppShortcutOptionsCollection/negative-phrase authoring beyond basic phrase
rules," and "Interactive Snippets and other visual intent-response UI
customization beyond ProvidesDialog." `knowledge/app-intents/
app-shortcuts-and-siri-phrases.md` covers only `AppShortcutsProvider`/
`AppShortcut` phrase authoring — not app schemas, Spotlight entity donation,
or Apple Intelligence/"Siri AI" contextual features. **This is a real scope
gap**, independent of whether the June 8 revision counts as "this launch's"
change: app schemas, Spotlight donation, and Siri AI contextual annotation are
all currently unmodeled in this repo.

---

## Snippets — NEW PAGE, but dated June 8 2026 not Sept 2026 (see headline finding)

- URL: https://developer.apple.com/design/human-interface-guidelines/snippets
- Change log (verbatim, only row): **June 8, 2026 — "New page."**
- Type: **NEW page** (first appearance) — confirmed by the single change-log entry reading "New page" with no prior history. However the date is June 8, 2026, not September 9/10 2026, despite its presence in the landing page's "New and updated" module today.

### What the page covers

Snippets are "compact views that appear in response to an action that someone
takes using Siri, Spotlight, or the Shortcuts app." Two types: **confirmation**
snippets (confirm/cancel an action, optional) and **result** snippets (show an
outcome, always shown). Anatomy: dialogue text, a custom view (up to 400pt
tall), and system-provided buttons (Cancel + customizable primary button for
confirmation; a single Done button for result). Best practices cover
legibility/contrast, conciseness, primary-button labeling, and not relying on
dialogue text alone to convey purpose. Not supported on tvOS, visionOS, or
watchOS. Links to a "Design interactive snippets" video and to developer
guidance "Displaying static and interactive snippets."

### Repo coverage

This maps directly to what `references/apple/app-intents.md` names as
explicitly out of scope: "Interactive Snippets and other visual intent-response
UI customization beyond ProvidesDialog." **Zero existing coverage** —
confirmed via `grep -ril -i snippet references/ knowledge/ skills/`, which
only returns files that use "snippet" informally (code-snippet examples,
`technical-notation.md`) or the app-intents exclusion note itself, not any
Knowledge Contract about the Snippets UI. Standing up a Snippets Knowledge
Contract (and deciding whether it belongs under `app-intents` or under
`human-interface-guidelines`) would be new-domain work, not an edit to
existing coverage.

---

## Summary table

| Topic | NEW or EDIT | Change-log date found | Repo coverage today |
|---|---|---|---|
| Branding | EDIT | Sept 9, 2026 | `knowledge/human-interface-guidelines/branding.md` — Rule 2 stale re: brand-color restraint |
| SharePlay | EDIT (page itself is old; repo coverage is the gap) | Sept 9, 2026 | No coverage anywhere (`grep` confirmed zero hits) |
| Layout | EDIT | Sept 9, 2026 | `knowledge/human-interface-guidelines/layout.md` — missing Liquid Glass/background-extension, size-class terminology, per-platform specifics |
| Menus | N/A this window | June 8, 2026 (no Sept entry) | `knowledge/human-interface-guidelines/menus.md` — reasonably current |
| Siri | N/A this window | June 8, 2026 (no Sept entry) | Explicitly out-of-scope per `references/apple/app-intents.md`; app schemas / Spotlight donation / Siri AI unmodeled |
| Snippets | NEW page | June 8, 2026 (not Sept, despite landing-page listing) | Zero coverage; explicitly excluded from `app-intents` v1 scope |

## Most significant finding

Half the pages the landing page currently promotes as "New and updated"
(Menus, Siri, Snippets) do not actually carry a September 9/10, 2026
change-log entry — their latest logged change is June 8, 2026 — while the
other half (Branding, SharePlay, Layout) do. Anyone treating the "New and
updated" module as a reliable pointer to *this specific launch's* documentation
changes should instead check each page's own Change log section, since the
module and the per-page logs disagree for three of six entries here.
