# Human Interface Guidelines — Patterns & Components Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing `human-interface-guidelines` domain with a curated 18-Knowledge-Contract subset of Apple's HIG Patterns and Components sections (plus one Inputs topic) — 2 new References, 18 new Knowledge Contracts, 2 new native Skills — per `docs/superpowers/specs/2026-08-05-hig-patterns-components-domain-design.md`. This closes the highest-priority named Tier 1 gap (`docs/architecture/domain-map.md` line 19: "Foundations subset only; Patterns/Components/Inputs remain unbuilt").

**Architecture:** References → Knowledge → Skills layer order, same as every prior domain. Because the existing Foundations Reference (50/80 lines) and Skill (48/60 lines) are already close to their project-wide size caps at 15 topics, adding 18 more topics at the same density would exceed both caps — so the Reference and Skill layers split along Apple's own Foundations/Patterns/Components information architecture into two new Reference+Skill pairs (`human-interface-guidelines-components`, `human-interface-guidelines-patterns`), while all 33 Knowledge Contracts (15 existing + 18 new) share one `knowledge/human-interface-guidelines/` directory since the domain itself is unchanged. This is the first domain in the kit with more than one Skill — a deliberate, documented exception to the informal one-skill-per-domain pattern, driven by the size caps. All 18 Knowledge Contracts' content was researched and drafted by two dispatched subagents (per RFC 0001 decision 5 — PDF/web ingestion delegated to subagents, never read by the main thread directly) that pulled real content from Apple's own HIG data API (`developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`, since the HIG site itself is a client-rendered SPA that plain fetching can't see through), then were spot-verified independently (URL redirects confirmed live via `curl`, cross-referenced `related:` ids confirmed to exist as real files) before this plan was written. Content is design-level only — no Swift/SwiftUI/UIKit code — matching the existing Foundations Knowledge Contracts' style (prose-based Compliant/Non-Compliant bullet examples, not code blocks).

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Update `references/apple/human-interface-guidelines.md`

**Files:**
- Modify: `references/apple/human-interface-guidelines.md`

- [ ] **Step 1: Replace the outdated Purpose section**

Find this exact block:

```markdown
## Purpose

Reference index for Apple's Human Interface Guidelines — Foundations
section, iOS/iPadOS scope. Patterns, Components, and Inputs sections
are out of scope for this pass — see docs/architecture/domain-map.md.
```

Replace with:

```markdown
## Purpose

Reference index for Apple's Human Interface Guidelines — Foundations
section, iOS/iPadOS scope. A curated subset of Patterns and Components
(plus one Inputs topic) is covered separately by
`references/apple/human-interface-guidelines-patterns.md` and
`references/apple/human-interface-guidelines-components.md` — see
docs/architecture/domain-map.md for full scope and what remains
unbuilt.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/human-interface-guidelines.md --type reference`
Expected: `PASS: references/apple/human-interface-guidelines.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/human-interface-guidelines.md
git commit -m "docs: scope HIG Foundations reference to sibling Patterns/Components references"
```

---

## Task 2: Update `skills/human-interface-guidelines/SKILL.md`

**Files:**
- Modify: `skills/human-interface-guidelines/SKILL.md`

- [ ] **Step 1: Add the two new sibling skills to `related:`**

Find this exact block:

```markdown
related:
  - skill.style-guide.writing
```

Replace with:

```markdown
related:
  - skill.style-guide.writing
  - skill.human-interface-guidelines.components
  - skill.human-interface-guidelines.patterns
```

- [ ] **Step 2: Update Stop Conditions to route instead of report-as-gap**

Find this exact block:

```markdown
## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. HIG Patterns, Components, and Inputs
sections are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

Replace with:

```markdown
## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. For Components/Inputs topics (lists,
buttons, sheets, alerts, action sheets, navigation, tab bars, pickers,
toggles, text fields, menus, gestures), route to
`skill.human-interface-guidelines.components` instead. For Patterns
topics (onboarding, searching, settings, notifications, feedback,
undo/redo), route to `skill.human-interface-guidelines.patterns`
instead. Any other HIG Patterns, Components, or Inputs topic not
covered by those two sibling skills remains out of scope (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py skills/human-interface-guidelines/SKILL.md --type skill`
Expected: `PASS: skills/human-interface-guidelines/SKILL.md`

- [ ] **Step 4: Commit**

```bash
git add skills/human-interface-guidelines/SKILL.md
git commit -m "docs: cross-link HIG Foundations skill to new Components/Patterns siblings"
```

---

## Task 3: Reference — `references/apple/human-interface-guidelines-components.md`

**Files:**
- Create: `references/apple/human-interface-guidelines-components.md`

- [ ] **Step 1: Create the file**

```markdown
# Human Interface Guidelines — Components

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/design/human-interface-guidelines/components
https://developer.apple.com/design/human-interface-guidelines/inputs

## Purpose

Reference index for a curated subset of Apple's Human Interface
Guidelines Components section (plus one Inputs topic), iOS/iPadOS
scope: lists and tables, buttons, sheets, alerts, action sheets,
navigation bars, tab bars, pickers, toggles, text fields, menus, and
touchscreen gestures. The remaining Components/Inputs topics (Column
Views, Disclosure Controls, Sliders, Steppers, Toolbars beyond the
navigation-bar subset, Popovers, Context Menus, Apple Pencil, Game
Controllers, Keyboards, and others) are out of scope for this pass —
see docs/architecture/domain-map.md.

## Primary Topics

- Lists and Tables
- Buttons
- Sheets
- Alerts
- Action Sheets
- Navigation Bars
- Tab Bars
- Pickers
- Toggles
- Text Fields
- Menus
- Touchscreen Gestures (Inputs)

## Used By

- knowledge/human-interface-guidelines/lists-and-tables.md ([[knowledge/human-interface-guidelines/lists-and-tables]])
- knowledge/human-interface-guidelines/buttons.md ([[knowledge/human-interface-guidelines/buttons]])
- knowledge/human-interface-guidelines/sheets.md ([[knowledge/human-interface-guidelines/sheets]])
- knowledge/human-interface-guidelines/alerts.md ([[knowledge/human-interface-guidelines/alerts]])
- knowledge/human-interface-guidelines/action-sheets.md ([[knowledge/human-interface-guidelines/action-sheets]])
- knowledge/human-interface-guidelines/navigation-bars.md ([[knowledge/human-interface-guidelines/navigation-bars]])
- knowledge/human-interface-guidelines/tab-bars.md ([[knowledge/human-interface-guidelines/tab-bars]])
- knowledge/human-interface-guidelines/pickers.md ([[knowledge/human-interface-guidelines/pickers]])
- knowledge/human-interface-guidelines/toggles.md ([[knowledge/human-interface-guidelines/toggles]])
- knowledge/human-interface-guidelines/text-fields.md ([[knowledge/human-interface-guidelines/text-fields]])
- knowledge/human-interface-guidelines/menus.md ([[knowledge/human-interface-guidelines/menus]])
- knowledge/human-interface-guidelines/touchscreen-gestures.md ([[knowledge/human-interface-guidelines/touchscreen-gestures]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/human-interface-guidelines-components.md --type reference`
Expected: `PASS: references/apple/human-interface-guidelines-components.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/human-interface-guidelines-components.md
git commit -m "docs: add human-interface-guidelines-components reference index"
```

---

## Task 4: Reference — `references/apple/human-interface-guidelines-patterns.md`

**Files:**
- Create: `references/apple/human-interface-guidelines-patterns.md`

- [ ] **Step 1: Create the file**

```markdown
# Human Interface Guidelines — Patterns

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/design/human-interface-guidelines/patterns

## Purpose

Reference index for a curated subset of Apple's Human Interface
Guidelines Patterns section, iOS/iPadOS scope: onboarding, searching,
settings, notifications, feedback, and undo/redo. The remaining
Patterns topics (Charts, Drag and Drop, Entering Data, Full-Screen
Experiences, Launching, Loading, Managing Accounts, Modality,
Multitasking, Playing Audio, Printing, Ratings and Reviews, Sharing,
Status, Syncing, Workouts, and others) are out of scope for this pass
— see docs/architecture/domain-map.md.

## Primary Topics

- Onboarding
- Searching
- Settings
- Notifications
- Feedback
- Undo and Redo

## Used By

- knowledge/human-interface-guidelines/onboarding.md ([[knowledge/human-interface-guidelines/onboarding]])
- knowledge/human-interface-guidelines/searching.md ([[knowledge/human-interface-guidelines/searching]])
- knowledge/human-interface-guidelines/settings.md ([[knowledge/human-interface-guidelines/settings]])
- knowledge/human-interface-guidelines/notifications.md ([[knowledge/human-interface-guidelines/notifications]])
- knowledge/human-interface-guidelines/feedback.md ([[knowledge/human-interface-guidelines/feedback]])
- knowledge/human-interface-guidelines/undo-and-redo.md ([[knowledge/human-interface-guidelines/undo-and-redo]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/human-interface-guidelines-patterns.md --type reference`
Expected: `PASS: references/apple/human-interface-guidelines-patterns.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/human-interface-guidelines-patterns.md
git commit -m "docs: add human-interface-guidelines-patterns reference index"
```

---

## Task 5: Knowledge Contract — `lists-and-tables`

**Files:**
- Create: `knowledge/human-interface-guidelines/lists-and-tables.md`

- [ ] **Step 1: Create the file**

```markdown
# Lists and Tables

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.lists-and-tables
type: knowledge
title: Lists and Tables
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for structuring list and table rows, columns, selection feedback, and edit-mode gating on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - lists-and-tables
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
depends_on: []
related:
  - knowledge.human-interface-guidelines.typography
  - knowledge.human-interface-guidelines.layout
  - knowledge.accessibility.voiceover-navigation-order
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent structures list and table
content on iOS/iPadOS: row/column content conventions, edit-mode gating
for selection and reordering, selection feedback, and disclosure/info
control usage.

## Scope

### Included

-   List vs. table vs. grid selection for a given content type
-   Row and column content/text conventions
-   Edit-mode gating for select/reorder/delete
-   Selection feedback conventions (persistent vs. transient highlight)
-   Info button vs. disclosure indicator usage in rows

### Excluded

-   SwiftUI `List`/`Table` or UIKit `UITableView`/`UICollectionView`
    implementation — see `swiftui`/`uikit` domains
-   VoiceOver row announcement mechanics — see `accessibility` domain
-   Row/header copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST keep row/item text succinct to minimize truncation and
wrapping, keeping rows comfortable to scan and read.

### Rule 2

Agents SHOULD preserve readability of text that would otherwise be
clipped in a narrow table — for example, truncating in the middle of a
string rather than the end when that keeps both the start and end of
the content recognizable.

### Rule 3

Agents MUST use descriptive, noun-phrase column headings (no ending
punctuation) in a multicolumn table, and MUST provide a label or
header for context when a single-column table view has no visible
column heading.

### Rule 4

Agents MUST require people to enter an explicit edit mode before they
can select, reorder, add, or delete rows in an iOS/iPadOS list or
table.

### Rule 5

Agents MUST choose selection feedback appropriate to purpose:
persistently highlight the selected row when the list/table supports
hierarchical navigation; use a brief highlight plus a state indicator
(such as a checkmark) when the row toggles an option rather than
navigating.

### Rule 6

Agents MUST NOT use an info/detail-disclosure button to support
navigation into a row's subviews — use it only to reveal more
information about the row's content; use a disclosure indicator
accessory control for drill-down navigation.

### Rule 7

Agents SHOULD prefer a list or table for primarily text-based,
scannable content, and prefer a grid instead when items vary widely in
size or the content is mostly images.

## Compliant Example

-   ✓ A Settings-style list enters edit mode before showing reordering handles and delete controls. (Rule 4)
-   ✓ A hierarchy-navigation list keeps the tapped row highlighted while its detail view is shown. (Rule 5)
-   ✓ A multicolumn productivity table labels each column with a short noun phrase like "Date" and "Amount." (Rule 3)

## Non-Compliant Example

-   ✗ Rows can be reordered and deleted directly from the default (non-edit) list state. (Rule 4)
-   ✗ A row's info button is wired to push a new hierarchy screen instead of showing more detail about that row. (Rule 6)
-   ✗ Table rows contain multiple long, unbounded paragraphs of body text with no truncation strategy. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Lists and Tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/lists-and-tables.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/lists-and-tables.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/lists-and-tables.md
git commit -m "feat: add lists-and-tables knowledge contract"
```

---

## Task 6: Knowledge Contract — `buttons`

**Files:**
- Create: `knowledge/human-interface-guidelines/buttons.md`

- [ ] **Step 1: Create the file**

```markdown
# Buttons

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.buttons
type: knowledge
title: Buttons
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for button hit targets, press states, prominence, role assignment, and content on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - buttons
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/buttons
depends_on: []
related:
  - knowledge.style-guide.general-button-labels
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.human-interface-guidelines.color
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent sizes, styles, and assigns
semantic roles to buttons on iOS/iPadOS so their function, prominence,
and destructive/primary status are visually unambiguous.

## Scope

### Included

-   Minimum hit-target sizing
-   Press/highlight state requirements
-   Prominent-style usage and limits
-   Style vs. size for distinguishing preferred choices
-   Role assignment (normal, primary, cancel, destructive)
-   Icon vs. text content selection
-   Inline activity indicator for delayed actions

### Excluded

-   SwiftUI `Button`/UIKit `UIButton` implementation — see `swiftui`/`uikit` domains
-   Exact button label wording/capitalization — see `style-guide`
-   Symbol rendering/configuration API — see `sf-symbols` domain

## Rules

### Rule 1

Agents MUST provide a hit region of at least 44x44 pt for every
button, with enough surrounding space to visually distinguish it from
neighboring content and controls.

### Rule 2

Agents MUST provide a distinct press/highlighted state for any custom
button so it doesn't feel unresponsive to input.

### Rule 3

Agents SHOULD reserve a prominent (accent-colored/filled) style for
the single most likely action in a view, keeping prominent buttons to
one or two per view.

### Rule 4

Agents MUST use style — not size — to distinguish the preferred option
among a set of same-purpose buttons; buttons that form a coherent set
of choices MUST share the same size.

### Rule 5

Agents MUST NOT assign the primary/default role to a button that
performs a destructive action, even when that action is the most
likely choice.

### Rule 6

Agents SHOULD associate familiar system actions with familiar SF
Symbols icons, and use a short, verb-first text label when a label
communicates the action more clearly than an icon alone.

### Rule 7

Agents SHOULD configure a button to show an inline activity indicator
(optionally with an updated label) when its action doesn't complete
instantly, rather than leaving the button static during the delay.

## Compliant Example

-   ✓ A destructive "Delete Account" button uses the destructive/normal role, not primary, even though it's the likely next step in that flow. (Rule 5)
-   ✓ A "Checkout" button switches to an inline spinner plus a "Checking Out…" label during a network delay. (Rule 7)
-   ✓ Two same-purpose buttons share identical size; the preferred one is differentiated only by a prominent style. (Rule 4)

## Non-Compliant Example

-   ✗ A 30x30 pt icon button has no surrounding padding, making it hard to tap accurately. (Rule 1)
-   ✗ A destructive "Erase All Content" button is styled and assigned as the primary/default button. (Rule 5)
-   ✗ Three buttons in the same view all use the prominent, accent-colored style. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/buttons.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/buttons.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/buttons.md
git commit -m "feat: add buttons knowledge contract"
```

---

## Task 7: Knowledge Contract — `sheets`

**Files:**
- Create: `knowledge/human-interface-guidelines/sheets.md`

- [ ] **Step 1: Create the file**

```markdown
# Sheets

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.sheets
type: knowledge
title: Sheets
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for presenting, sizing, and dismissing sheets on iOS/iPadOS, including detents, grabbers, and button placement.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - sheets
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/sheets
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.human-interface-guidelines.materials
  - knowledge.human-interface-guidelines.alerts
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent presents, sizes, and
dismisses sheets on iOS/iPadOS: single-sheet stacking, dismissal
buttons, detents/grabbers, and when a sheet is the right surface versus
a full-screen presentation.

## Scope

### Included

-   Single-sheet-at-a-time stacking rule
-   Cancel/Done/Back button placement and pairing
-   Swipe-to-dismiss and unsaved-changes confirmation
-   Detents, grabber, and progressive disclosure
-   Page/form sheet presentation style on iPadOS
-   Sheet vs. full-screen presentation for scoped vs. prolonged tasks

### Excluded

-   SwiftUI `.sheet`/UIKit presentation-controller implementation — see `swiftui`/`uikit` domains
-   Sheet button copy wording — see `style-guide`
-   Blur/material rendering mechanics — see `materials`

## Rules

### Rule 1

Agents MUST display only one sheet at a time from the main interface;
if an action inside a sheet needs to present another sheet, the first
MUST be dismissed before the second appears.

### Rule 2

Agents MUST pair a Done button with a Cancel (or Back) button rather
than relying on Done alone as the only way to leave the sheet, and
MUST NOT show Cancel, Done, and Back together at once.

### Rule 3

Agents MUST support swipe-to-dismiss on an iOS/iPadOS sheet, and MUST
present a confirmation (such as an action sheet) if dismissing would
discard unsaved changes.

### Rule 4

Agents MUST place the Cancel/Close button on the leading edge and the
Done button on the trailing edge of a single-view sheet's top toolbar.

### Rule 5

Agents SHOULD include a grabber on a resizable sheet and support the
medium detent for progressive disclosure, unless the sheet's content
is only useful at full height.

### Rule 6

Agents SHOULD prefer the page or form sheet presentation style on
iPadOS for a consistent, centered, default-sized sheet rather than a
custom size.

### Rule 7

Agents SHOULD reserve a sheet for a scoped, closely related task tied
to the current context, and use a full-screen presentation instead for
prolonged or complex multistep flows such as document or photo
editing.

## Compliant Example

-   ✓ A share sheet supports the medium detent so its most relevant items are visible without full expansion. (Rule 5)
-   ✓ Swiping down on a sheet with unsaved edits triggers a confirming action sheet before dismissing. (Rule 3)
-   ✓ A compose sheet shows Cancel on the leading edge and Send/Done on the trailing edge. (Rule 4)

## Non-Compliant Example

-   ✗ A sheet displays Cancel, Done, and Back buttons simultaneously. (Rule 2)
-   ✗ Closing one sheet immediately reveals a second, previously hidden sheet stacked behind it. (Rule 1)
-   ✗ A multistep photo-editing flow is crammed into a single fixed-height sheet instead of a full-screen presentation. (Rule 7)

## Dependencies

None.

## References

-   [Apple HIG — Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/sheets.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/sheets.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/sheets.md
git commit -m "feat: add sheets knowledge contract"
```

---

## Task 8: Knowledge Contract — `alerts`

**Files:**
- Create: `knowledge/human-interface-guidelines/alerts.md`

- [ ] **Step 1: Create the file**

```markdown
# Alerts

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.alerts
type: knowledge
title: Alerts
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for when to show an alert, its structure, and button placement/role on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - alerts
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/alerts
depends_on: []
related:
  - knowledge.human-interface-guidelines.action-sheets
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
  - knowledge.human-interface-guidelines.color
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use an alert on
iOS/iPadOS, its structural limits, and button placement/role/style
conventions, so alerts stay reserved for genuinely critical,
actionable interruptions.

## Scope

### Included

-   When an alert is/isn't appropriate (critical + actionable only)
-   Title/message/button count limits
-   Button placement, default button, and destructive-style rules
-   Cancel-button requirement for destructive choices
-   Alert vs. action sheet decision (iOS/iPadOS)

### Excluded

-   SwiftUI `.alert`/UIKit `UIAlertController` implementation — see `swiftui`/`uikit` domains
-   Alert title/message copy wording — see `style-guide`
-   Destructive-red exact color value — see `color`

## Rules

### Rule 1

Agents MUST use alerts sparingly and only for information that's both
important and actionable — an alert MUST NOT be purely informational
with no meaningful choice attached.

### Rule 2

Agents MUST NOT show an alert for common, undoable destructive actions
(such as deleting a single email); alerts are reserved for uncommon,
non-undoable destructive actions someone might trigger unintentionally.

### Rule 3

Agents MUST NOT show an alert automatically at app launch; startup
issues (such as no network) MUST be surfaced through a non-interrupting
in-context indicator instead.

### Rule 4

Agents MUST limit an alert to a title, an optional short informative
message, and up to three buttons.

### Rule 5

Agents MUST place the button people are most likely to choose on the
trailing side of a button row (or top of a stack) and Cancel on the
leading side (or bottom of a stack); Cancel MUST NOT be the default
button.

### Rule 6

Agents MUST apply the destructive style only to a button whose action
the person did not deliberately/originally choose — not to a button
that confirms an action they intentionally initiated.

### Rule 7

Agents MUST include a Cancel button whenever the alert offers a
destructive choice, giving people a clear, safe way out.

### Rule 8

Agents MUST use an action sheet instead of an alert when the situation
calls for multiple choices related to an intentional action, reserving
alerts for confirming/canceling a single action or communicating a
problem.

## Compliant Example

-   ✓ A "Delete Photo" alert (uncommon, non-undoable) asks for confirmation with Delete and Cancel buttons. (Rule 2, Rule 7)
-   ✓ Deleting a single email produces no alert since the action is common and undoable. (Rule 2)
-   ✓ A network-unavailable state at launch is shown via a non-intrusive indicator, not a startup alert. (Rule 3)

## Non-Compliant Example

-   ✗ An alert appears on every app launch to announce a new feature. (Rule 3)
-   ✗ A deliberately chosen "Empty Trash" alert styles its confirm button as destructive even though the person intentionally chose that action. (Rule 6)
-   ✗ An alert offers three unrelated choices about how to proceed with an action instead of using an action sheet. (Rule 8)

## Dependencies

None.

## References

-   [Apple HIG — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/alerts.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/alerts.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/alerts.md
git commit -m "feat: add alerts knowledge contract"
```

---

## Task 9: Knowledge Contract — `action-sheets`

**Files:**
- Create: `knowledge/human-interface-guidelines/action-sheets.md`

- [ ] **Step 1: Create the file**

```markdown
# Action Sheets

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.action-sheets
type: knowledge
title: Action Sheets
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using an action sheet to offer choices related to an intentionally initiated action on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - action-sheets
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/action-sheets
depends_on: []
related:
  - knowledge.human-interface-guidelines.alerts
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use an action
sheet on iOS/iPadOS rather than an alert or a menu, and how to
structure its title, buttons, and destructive-choice styling.

## Scope

### Included

-   Action sheet vs. alert decision
-   Action sheet vs. menu decision (iOS/iPadOS)
-   Title/message brevity
-   Cancel button placement, destructive-button styling and position
-   Scroll avoidance / button-count limits

### Excluded

-   SwiftUI `.confirmationDialog`/UIKit `UIAlertController` (`.actionSheet`) implementation — see `swiftui`/`uikit` domains
-   Action sheet title/button copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST use an action sheet — not an alert — to offer choices
related to an action people intentionally initiated; alerts are
reserved for unexpected problems or confirming/canceling a single
action.

### Rule 2

Agents MUST use an action sheet — not a menu — when the choices are a
direct clarification of an action someone just performed; menus are
for choices people open deliberately, not responses to a triggered
action.

### Rule 3

Agents SHOULD keep the action sheet title short enough to fit on a
single line, and add a message only when the title plus context isn't
enough to convey the choices.

### Rule 4

Agents MUST place a Cancel button (when the sheet needs one) at the
bottom of the action sheet, and MUST style destructive choices with
the destructive style, positioned at the top where they're most
noticeable.

### Rule 5

Agents MUST NOT let an action sheet scroll — keep the number of
buttons small enough to avoid scrolling and reduce the risk of
mis-tapping a button while scrolling.

### Rule 6

Agents MUST use action sheets sparingly, interrupting the current task
only when a clarifying choice is genuinely necessary.

## Compliant Example

-   ✓ Canceling an in-progress email draft shows an action sheet with Delete Draft / Save Draft / Cancel choices. (Rule 1)
-   ✓ The destructive "Delete Draft" choice uses the destructive style and appears at the top of the sheet. (Rule 4)

## Non-Compliant Example

-   ✗ A five-button action sheet requires scrolling to see all choices. (Rule 5)
-   ✗ An unrelated confirmation ("Turn on Notifications?") is presented as an action sheet instead of an alert. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Action Sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/action-sheets.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/action-sheets.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/action-sheets.md
git commit -m "feat: add action-sheets knowledge contract"
```

---

## Task 10: Knowledge Contract — `navigation-bars`

**Files:**
- Create: `knowledge/human-interface-guidelines/navigation-bars.md`

- [ ] **Step 1: Create the file**

```markdown
# Navigation Bars

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.navigation-bars
type: knowledge
title: Navigation Bars
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for the iOS/iPadOS top navigation bar — titles, back/close controls, and leading/trailing item placement.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - navigation-bars
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/toolbars
depends_on: []
related:
  - knowledge.human-interface-guidelines.tab-bars
  - knowledge.style-guide.navigation-controls
  - knowledge.human-interface-guidelines.layout
updated: 2026-08-06
```

## Intent

Apple has merged its former standalone "Navigation Bars" page into the
"Toolbars" HIG page (the `navigation-bars` URL now redirects there; the
page states "In iOS, a navigation-specific toolbar is sometimes called
a navigation bar"). This contract scopes strictly to that
navigation-specific subset for iOS/iPadOS: screen titles, back/close
controls, and leading/center/trailing item placement — not general
toolbar action-button guidance.

## Scope

### Included

-   Screen/window title conventions
-   Standard Back/Close control usage
-   Large title behavior on scroll (iOS)
-   Leading/trailing edge content placement
-   Combining a navigation bar with a tab bar (iPadOS)

### Excluded

-   General toolbar action-item selection/grouping (non-navigation) — out of scope for this contract
-   SwiftUI `NavigationStack`/UIKit `UINavigationController` implementation — see `swiftui`/`uikit` domains
-   Title copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST give each screen a concise, useful title — not the app's
own name — so people can confirm their location and distinguish
between windows.

### Rule 2

Agents MUST use the standard Back and Close symbols and behavior for
hierarchical and modal dismissal respectively, without replacing them
with custom "Back"/"Close" text labels.

### Rule 3

Agents SHOULD use a large title on iOS that automatically transitions
to a standard/compact title as content scrolls, and back again at the
top, to reinforce location during scrolling.

### Rule 4

Agents MUST reserve the leading edge of the navigation bar for
back/sidebar navigation controls and the title, and reserve the
trailing edge for the primary action and any controls that must stay
available regardless of window width.

### Rule 5

Agents SHOULD move less-essential actions into a More menu rather than
crowding the visible bar, prioritizing only the most important actions
for direct placement.

### Rule 6

Agents SHOULD apply a single prominent (tinted) style to one key
trailing action (such as Done or Submit) rather than tinting multiple
bar items, to keep a clear focal point.

### Rule 7

Agents SHOULD allow a navigation bar to share horizontal space with a
tab bar on iPadOS when navigating between a few top-level areas while
keeping full width available for content.

## Compliant Example

-   ✓ A detail screen's title is a short noun phrase describing content, not the app's name. (Rule 1)
-   ✓ The Back button uses the standard chevron symbol with no "Back" text label. (Rule 2)
-   ✓ On iPadOS, a compact top bar combines navigation controls and a tab bar in the same row without crowding. (Rule 7)

## Non-Compliant Example

-   ✗ Every screen's title bar reads the app's own name. (Rule 1)
-   ✗ A custom "Back" text button replaces the system back control. (Rule 2)
-   ✗ Six equally weighted actions are crammed into the trailing edge with no More menu. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) (the former `navigation-bars` URL now redirects here)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/navigation-bars.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/navigation-bars.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/navigation-bars.md
git commit -m "feat: add navigation-bars knowledge contract"
```

---

## Task 11: Knowledge Contract — `tab-bars`

**Files:**
- Create: `knowledge/human-interface-guidelines/tab-bars.md`

- [ ] **Step 1: Create the file**

```markdown
# Tab Bars

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.tab-bars
type: knowledge
title: Tab Bars
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using a tab bar for top-level app navigation on iOS/iPadOS, including visibility, tab count, and labeling.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - tab-bars
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/tab-bars
depends_on: []
related:
  - knowledge.human-interface-guidelines.navigation-bars
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.style-guide.navigation-controls
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use a tab bar on
iOS/iPadOS, how many tabs to show, and conventions for visibility,
labeling, and badges, so top-level navigation stays predictable.

## Scope

### Included

-   Tab bar vs. toolbar (navigation vs. action) decision
-   Tab bar visibility persistence
-   Tab count and overflow guidance
-   Tab labeling and SF Symbols icon usage
-   Badge usage
-   iPadOS sidebar-convertible tab bar

### Excluded

-   SwiftUI `TabView`/UIKit `UITabBarController` implementation — see `swiftui`/`uikit` domains
-   Tab label copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST use a tab bar for top-level navigation between sections,
not for actions that operate on the current view's content — use a
toolbar instead for those.

### Rule 2

Agents MUST keep the tab bar visible as people move between top-level
sections; hiding it (other than a temporary modal covering it) causes
people to lose track of where they are in the app.

### Rule 3

Agents MUST NOT disable or hide a tab bar button when its section's
content is unavailable — the tab MUST remain reachable, with the empty
state explained within that section.

### Rule 4

Agents SHOULD choose the smallest number of tabs that adequately
covers the app's top-level sections, since fewer tabs are easier to
navigate; consider a sidebar-convertible tab bar on iPadOS for complex
hierarchies.

### Rule 5

Agents SHOULD include a short (ideally one-word) label beneath or
beside each tab's icon to aid navigation, and prefer SF Symbols so
icons adapt automatically between compact and regular layouts.

### Rule 6

Agents SHOULD avoid relying on an overflow ("More") tab where
possible — content behind it is harder to discover — by prioritizing
which tabs are visible instead of overloading the bar.

### Rule 7

Agents SHOULD reserve badges for genuinely critical, attention-worthy
information rather than routine updates, to preserve their meaning.

## Compliant Example

-   ✓ Five or fewer top-level sections are represented in the tab bar with SF Symbols icons and one-word labels. (Rule 4, Rule 5)
-   ✓ An empty "Downloads" tab remains selectable and explains why it's empty instead of being disabled. (Rule 3)

## Non-Compliant Example

-   ✗ The tab bar disappears when navigating into a section, leaving no persistent orientation cue. (Rule 2)
-   ✗ A tab is grayed out and untappable because its content is currently empty. (Rule 3)
-   ✗ Eight top-level tabs push several items into a "More" overflow list by default. (Rule 6)

## Dependencies

None.

## References

-   [Apple HIG — Tab Bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/tab-bars.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/tab-bars.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/tab-bars.md
git commit -m "feat: add tab-bars knowledge contract"
```

---

## Task 12: Knowledge Contract — `pickers`

**Files:**
- Create: `knowledge/human-interface-guidelines/pickers.md`

- [ ] **Step 1: Create the file**

```markdown
# Pickers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.pickers
type: knowledge
title: Pickers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for choosing and configuring pickers versus other selection controls on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - pickers
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/pickers
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.human-interface-guidelines.lists-and-tables
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use a picker
rather than another selection control on iOS/iPadOS, and conventions
for value ordering, in-context presentation, and date/time picker
style/granularity.

## Scope

### Included

-   Picker vs. segmented control vs. list-with-index decision
-   Value ordering predictability
-   In-context (inline/popover) presentation
-   Compact date-picker style for constrained space
-   Minute-interval granularity for time pickers

### Excluded

-   SwiftUI `Picker`/`DatePicker` or UIKit `UIPickerView`/`UIDatePicker` implementation — see `swiftui`/`uikit` domains
-   Picker item copy wording — see `style-guide`

## Rules

### Rule 1

Agents SHOULD use a picker for medium-to-long lists of selectable
values, preferring a smaller control (such as a segmented control) for
very short option sets, and a list/table with an index for very large
sets.

### Rule 2

Agents MUST order picker values predictably (for example,
alphabetically or chronologically) so people can anticipate hidden
values before interacting.

### Rule 3

Agents SHOULD present a picker in context — inline or in a popover near
the field it edits — rather than navigating to a separate screen to
show it.

### Rule 4

Agents MUST use the compact date-picker style when screen space is
constrained, opening a modal editor only on demand rather than
consuming persistent space.

### Rule 5

Agents SHOULD allow a coarser minute interval in a date/time picker
(any divisor of 60, such as 15-minute steps) instead of always
requiring all 60 discrete minute values, when fine-grained precision
isn't needed.

## Compliant Example

-   ✓ A country picker lists countries in alphabetical order matching device locale. (Rule 2)
-   ✓ A time picker offers 15-minute increments for a scheduling feature that doesn't need per-minute precision. (Rule 5)

## Non-Compliant Example

-   ✗ A picker with unordered, randomly arranged values makes it hard to predict where a value is. (Rule 2)
-   ✗ Selecting a date pushes to an entirely new screen instead of showing an inline/popover picker. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/pickers.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/pickers.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/pickers.md
git commit -m "feat: add pickers knowledge contract"
```

---

## Task 13: Knowledge Contract — `toggles`

**Files:**
- Create: `knowledge/human-interface-guidelines/toggles.md`

- [ ] **Step 1: Create the file**

```markdown
# Toggles

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.toggles
type: knowledge
title: Toggles
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using switch-style toggles on iOS/iPadOS, including state legibility and list-row vs. standalone usage.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - toggles
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/toggles
depends_on: []
related:
  - knowledge.style-guide.input-controls
  - knowledge.human-interface-guidelines.color
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use a toggle on
iOS/iPadOS, how its on/off state must be legible, and the difference
between the in-row switch style and a standalone toggle-behaving
button.

## Scope

### Included

-   Toggle vs. other selection controls (picker, list) decision
-   On/off state legibility beyond color alone
-   Switch style restricted to list rows
-   Standalone toggle-behaving button conventions
-   Accent color changes and contrast

### Excluded

-   SwiftUI `Toggle`/UIKit `UISwitch` implementation — see `swiftui`/`uikit` domains
-   Toggle/label copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST use a toggle only to represent a pair of opposing states
(such as on/off) that affect content or a view's state — not for
choosing among a list of items, which should use a picker or list
instead.

### Rule 2

Agents MUST make a toggle's on/off states visually distinguishable
through more than color alone (such as fill, shape, or inner-detail
changes), since not everyone can perceive color differences.

### Rule 3

Agents MUST use the switch style only within a list row, relying on
the row's own content to supply context rather than adding a redundant
label.

### Rule 4

Agents SHOULD use a button that behaves like a toggle — rather than a
switch control — for toggle-like state outside of a list row, and MUST
NOT pair that button with an explanatory text label, since its icon
and appearance changes alone communicate purpose.

### Rule 5

Agents SHOULD change a switch's default accent color only when
necessary, and only to a color that still provides sufficient contrast
against the off state.

### Rule 6

Agents MUST clearly identify what setting, view, or content a toggle
affects, either via surrounding context or an explicit label.

## Compliant Example

-   ✓ A list-row switch for "Wi-Fi" relies on the row's own label; no redundant caption is added beside the switch. (Rule 3)
-   ✓ A toggle's on state changes both fill color and an internal checkmark, not color alone. (Rule 2)

## Non-Compliant Example

-   ✗ A filter toggle button outside a list row includes an explanatory text label next to its icon. (Rule 4)
-   ✗ A toggle communicates on/off using only a color change with no shape/fill difference. (Rule 2)
-   ✗ A toggle is used to let someone pick one of four options. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/toggles.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/toggles.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/toggles.md
git commit -m "feat: add toggles knowledge contract"
```

---

## Task 14: Knowledge Contract — `text-fields`

**Files:**
- Create: `knowledge/human-interface-guidelines/text-fields.md`

- [ ] **Step 1: Create the file**

```markdown
# Text Fields

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.text-fields
type: knowledge
title: Text Fields
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for sizing, spacing, validating, and securing single-line text field input on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - text-fields
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/text-fields
depends_on: []
related:
  - knowledge.style-guide.authentication-credentials-and-biometrics
  - knowledge.human-interface-guidelines.layout
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent sizes, spaces, validates,
and secures text field input on iOS/iPadOS for short, specific pieces
of text such as names, emails, or passwords.

## Scope

### Included

-   Field sizing relative to expected input length
-   Secure text field usage for sensitive data
-   Placeholder/label pairing
-   Multi-field form spacing and consistency
-   Validation timing
-   iOS/iPadOS Clear button and leading/trailing accessory placement

### Excluded

-   SwiftUI `TextField`/UIKit `UITextField` implementation — see `swiftui`/`uikit` domains
-   Placeholder/label copy wording — see `style-guide`
-   Dynamic Type scaling API — see `accessibility` domain

## Rules

### Rule 1

Agents MUST size a text field to roughly match the expected quantity
of input text, so its size visually communicates how much information
to provide.

### Rule 2

Agents MUST use a secure text field for sensitive input such as
passwords.

### Rule 3

Agents SHOULD provide placeholder/hint text describing a field's
purpose, and pair it with a persistent label when the placeholder
alone won't be remembered once typing starts, since placeholder text
disappears on input.

### Rule 4

Agents MUST evenly space and consistently size multiple text fields in
a form so each field is clearly associated with its label, stacking
fields vertically where possible.

### Rule 5

Agents SHOULD validate input at a contextually appropriate time — for
example, when focus leaves the field for something like an email
address, but before advancing for values like a chosen username or
password — and clearly communicate invalid input.

### Rule 6

Agents MUST show a Clear button at the trailing end of a text field to
let people erase input without repeated deletions.

### Rule 7

Agents SHOULD reserve the leading end of a text field for
purpose-indicating imagery and the trailing end for supplementary
actions (such as bookmarking).

## Compliant Example

-   ✓ A password field renders as a secure field and hides entered characters. (Rule 2)
-   ✓ An email field validates format only after the person moves to the next field, not on every keystroke. (Rule 5)
-   ✓ A one-line name field is sized for a short name, not full-paragraph width. (Rule 1)

## Non-Compliant Example

-   ✗ A password field displays entered characters in plain text. (Rule 2)
-   ✗ A short numeric field is drawn wide enough for a paragraph of text. (Rule 1)
-   ✗ Multiple fields in a form are inconsistently sized and spaced so labels are ambiguous. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Text Fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/text-fields.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/text-fields.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/text-fields.md
git commit -m "feat: add text-fields knowledge contract"
```

---

## Task 15: Knowledge Contract — `menus`

**Files:**
- Create: `knowledge/human-interface-guidelines/menus.md`

- [ ] **Step 1: Create the file**

```markdown
# Menus

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.menus
type: knowledge
title: Menus
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for menu item availability, ordering/grouping, icon consistency, submenu depth, and iOS/iPadOS menu layout.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - menus
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/menus
depends_on: []
related:
  - knowledge.style-guide.presentation-surfaces
  - knowledge.style-guide.general-button-labels
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent structures menus on
iOS/iPadOS: item availability and clarity, ordering and grouping, icon
consistency, submenu limits, toggled-item state, and menu layout
choice.

## Scope

### Included

-   Unavailable item presentation (dimmed, not hidden)
-   Item label clarity (one item = one action)
-   Ellipsis-style affordance for items needing further input
-   Priority ordering and logical grouping with separators
-   Icon consistency within a group
-   Submenu depth/length limits
-   Toggled-item state representation
-   iOS/iPadOS small/medium/large menu layout choice

### Excluded

-   SwiftUI `Menu`/UIKit `UIMenu` implementation — see `swiftui`/`uikit` domains
-   Menu item copy wording/capitalization — see `style-guide`

## Rules

### Rule 1

Agents MUST show an unavailable menu item in a dimmed/disabled state
rather than hiding it, so the menu itself remains discoverable and
openable even when all its items are unavailable.

### Rule 2

Agents MUST ensure each menu item's label clearly and succinctly
describes exactly one action or state.

### Rule 3

Agents SHOULD visually indicate when choosing a menu item requires
further input before the action completes (such as an
ellipsis-style affordance).

### Rule 4

Agents SHOULD order menu items with the most important/frequently used
items first, and group logically related items together, separated
visually from unrelated groups.

### Rule 5

Agents MUST apply icons consistently within a group — either all items
in a group have an icon or none do.

### Rule 6

Agents SHOULD restrict submenus to a single level of depth and to
roughly five or fewer items, using a submenu instead of indenting
related items.

### Rule 7

Agents on iOS/iPadOS SHOULD choose a menu layout — small (icon row),
medium (icon+label row), or large (default list) — appropriate to how
many high-priority actions the context has, reserving small/medium
layouts for closely related or especially frequent actions.

## Compliant Example

-   ✓ A disabled "Merge Duplicates" menu item appears dimmed rather than being removed from the menu. (Rule 1)
-   ✓ Cut, Copy, and Paste are grouped together and separated from unrelated commands. (Rule 4)
-   ✓ A notes app uses the medium layout for its three most common actions. (Rule 7)

## Non-Compliant Example

-   ✗ A "Sort By" menu item silently disappears instead of appearing dimmed when sorting is unavailable. (Rule 1)
-   ✗ A submenu nests three levels deep to organize export formats. (Rule 6)
-   ✗ Only some items in the Edit group have icons while others in the same group don't. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/menus.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/menus.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/menus.md
git commit -m "feat: add menus knowledge contract"
```

---

## Task 16: Knowledge Contract — `touchscreen-gestures`

**Files:**
- Create: `knowledge/human-interface-guidelines/touchscreen-gestures.md`

- [ ] **Step 1: Create the file**

```markdown
# Touchscreen Gestures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.touchscreen-gestures
type: knowledge
title: Touchscreen Gestures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using standard vs. custom touch gestures on iOS/iPadOS, including alternate-input and feedback requirements.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - touchscreen-gestures
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/gestures
depends_on: []
related:
  - knowledge.style-guide.touch-gesture-verbs
  - knowledge.accessibility.full-keyboard-access-and-focus
updated: 2026-08-06
```

## Intent

Apple renamed this page from "Touchscreen gestures" to "Gestures" (the
`touchscreen-gestures` URL now redirects there) when it broadened scope
to cover indirect/direct input across platforms. This contract keeps
the original filename per the touch-focused scope requested, and
restricts its Rules to the iOS/iPadOS touchscreen subset: when to use
standard vs. custom gestures, feedback, and alternate-input
availability.

## Scope

### Included

-   Alternate-input availability for gesture-driven actions
-   Standard gesture consistency (don't repurpose or reinvent)
-   In-progress gesture feedback
-   Unavailable-gesture communication
-   Custom gesture design criteria
-   iOS/iPadOS standard system gestures (three-finger swipe/pinch, four-finger swipe)

### Excluded

-   `UIGestureRecognizer`/SwiftUI gesture modifier implementation — see `swiftui`/`uikit` domains
-   VoiceOver/Switch Control gesture mechanics — see `accessibility` domain
-   Gesture-verb copy wording — see `style-guide`

## Rules

### Rule 1

Agents MUST offer more than one way to perform any given task — a
specific gesture MUST NOT be the only way to accomplish something.

### Rule 2

Agents MUST respond to standard gestures (tap, swipe, drag,
touch-and-hold, pinch/zoom) consistently with their system-wide
meaning, MUST NOT repurpose a standard gesture to perform an
app-unique action, and MUST NOT invent a custom gesture to perform a
standard action such as activating a button or scrolling.

### Rule 3

Agents MUST provide immediate, responsive feedback while a gesture is
in progress so people can predict its result.

### Rule 4

Agents MUST clearly indicate when a gesture isn't currently available,
rather than leaving the interaction silently unresponsive.

### Rule 5

Agents SHOULD add a custom gesture only for a frequent, specialized
task not covered by standard gestures, and only when it is
discoverable, easy to perform, distinct from other gestures, and not
the only way to perform an important action.

### Rule 6

Agents SHOULD use a custom/shortcut gesture only as a supplement to —
never a replacement for — the standard tappable control it accelerates.

### Rule 7

Agents MUST support the standard iOS three-finger swipe (undo/redo)
and three-finger pinch (copy/paste) system gestures without conflict,
and on iPadOS MUST avoid conflicting with the four-finger swipe
app-switching gesture.

## Compliant Example

-   ✓ A drawing app adds a custom two-finger tap to undo, but a visible Undo button and the standard three-finger swipe still work. (Rule 6)
-   ✓ Dragging a locked item shows a resistance animation instead of silently doing nothing. (Rule 4)

## Non-Compliant Example

-   ✗ Swiping right on a list item performs a unique, app-specific action instead of the expected reveal-actions behavior. (Rule 2)
-   ✗ A key action is reachable only via a custom three-finger rotate gesture with no button alternative. (Rule 1, Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) (the former `touchscreen-gestures` URL now redirects here)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/touchscreen-gestures.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/touchscreen-gestures.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/touchscreen-gestures.md
git commit -m "feat: add touchscreen-gestures knowledge contract"
```

---

## Task 17: Knowledge Contract — `onboarding`

**Files:**
- Create: `knowledge/human-interface-guidelines/onboarding.md`

- [ ] **Step 1: Create the file**

```markdown
# Onboarding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.onboarding
type: knowledge
title: Onboarding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for structuring an optional, fast, and focused first-run onboarding flow on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - onboarding
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/onboarding
depends_on: []
related:
  - knowledge.human-interface-guidelines.privacy
  - knowledge.human-interface-guidelines.settings
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent structures a first-run
onboarding experience on iOS/iPadOS: when it appears relative to
launch, how much it asks of people, and how it stays optional and
easy to skip or revisit.

## Scope

### Included

-   Timing of onboarding relative to app launch
-   Interactive vs. static teaching approach
-   Making onboarding flows optional, skippable, and re-discoverable
-   Splash-screen brevity and avoiding download-blocked onboarding
-   Placement of legal/licensing content relative to onboarding
-   Sequencing of setup steps, permission requests, and ratings/purchase prompts

### Excluded

-   Onboarding screen implementation code
-   Onboarding copy/wording — see `style-guide`
-   Permission purpose-string wording and system-alert mechanics — see `privacy`
-   Custom in-app settings area structure — see `settings`

## Rules

### Rule 1

Agents MUST present onboarding only after app launch has completed —
it is not part of the launch experience.

### Rule 2

Agents MUST make any prerequisite onboarding/tutorial flow optional
to skip, MUST NOT re-present it automatically on subsequent launches
once skipped, and SHOULD keep it easy to find later (e.g., in a help,
account, or settings area).

### Rule 3

Agents SHOULD favor an interactive, hands-on onboarding experience —
letting people actually perform an action or try a feature — over
static instructional screens.

### Rule 4

Agents SHOULD prefer contextual, in-place tips shown near the
relevant part of the interface over a single upfront onboarding flow,
when the app's structure supports it.

### Rule 5

Agents MUST NOT block onboarding on large downloads and MUST NOT
include licensing/legal agreement text within the onboarding flow.

### Rule 6

Agents SHOULD postpone nonessential setup or customization steps
during onboarding, relying on sensible defaults, and SHOULD defer
ratings or purchase prompts until after people have experienced core
functionality.

### Rule 7

Agents SHOULD integrate a permission request into onboarding only
when doing so helps explain its benefit in context; otherwise defer
the request to the point where the person first uses the feature that
needs it (see `privacy` Rule 1).

## Compliant Example

-   ✓ A photo-editing app skips straight into the editor and offers a "Show me around" tip the first time someone opens a tool, instead of a mandatory multi-screen tutorial. (Rules 3, 4)
-   ✓ A fitness app's onboarding flow can be skipped, and the skipped tutorial remains available later from Settings. (Rule 2)
-   ✓ A navigation app explains and requests location access during onboarding, since the benefit is obvious in context. (Rule 7)

## Non-Compliant Example

-   ✗ A splash-screen-and-slideshow onboarding sequence plays before the app has finished launching. (Rule 1)
-   ✗ Onboarding re-appears every time the app launches even after being skipped once. (Rule 2)
-   ✗ Onboarding requests camera, contacts, and location access up front, before any feature needs them. (Rule 7)

## Dependencies

None.

## References

-   [Apple HIG — Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/onboarding.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/onboarding.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/onboarding.md
git commit -m "feat: add onboarding knowledge contract"
```

---

## Task 18: Knowledge Contract — `searching`

**Files:**
- Create: `knowledge/human-interface-guidelines/searching.md`

- [ ] **Step 1: Create the file**

```markdown
# Searching

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.searching
type: knowledge
title: Searching
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for in-app search placement, scope, and suggestions, and for making app content discoverable through systemwide Spotlight search on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - searching
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/searching
depends_on: []
related: []
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent places and structures
search on iOS/iPadOS: where the search field lives, how scope is
communicated, what suggestions to offer, and how app content should
participate in systemwide Spotlight search.

## Scope

### Included

-   Placement and prominence of an in-app search field
-   Single vs. per-section (local) search locations
-   Communicating current search scope
-   Recent searches and predictive suggestions
-   Search-history privacy
-   Making app content indexable by systemwide Spotlight search

### Excluded

-   Search field/result implementation code
-   Search suggestion copy/wording — see `style-guide`
-   Core Spotlight indexing API implementation

## Rules

### Rule 1

Agents MUST give search a primary, prominent position (e.g., a
toolbar search field or a dedicated tab) when search is important to
the app's purpose.

### Rule 2

Agents SHOULD consolidate app-wide search into a single, clearly
identified location; a local, section-scoped search that acts as a
filter on the current view is acceptable for apps with clearly
distinct sections.

### Rule 3

Agents MUST clearly communicate the current scope of a search —
through placeholder text, a scope bar, or a title — so people know
what they're searching.

### Rule 4

Agents SHOULD personalize search with recent searches shown before
typing and predictive suggestions, completions, or corrections shown
while typing.

### Rule 5

Agents MUST provide a way to clear search history if search history
is displayed, since people may not want it visible to others.

### Rule 6

Agents SHOULD make the app's content indexable by Spotlight, with
descriptive metadata, so people can find it systemwide without
opening the app first.

## Compliant Example

-   ✓ A notes app puts a search field in its bottom toolbar alongside other primary actions. (Rule 1)
-   ✓ A mail app's search always shows which mailbox is currently being searched. (Rule 3)
-   ✓ A music app shows recent searches before typing and narrows suggestions as the person types. (Rule 4)

## Non-Compliant Example

-   ✗ Search is buried two menus deep in an app where finding content is a primary task. (Rule 1)
-   ✗ A search field gives no indication of whether it's searching the whole app or just the current folder. (Rule 3)
-   ✗ Search history is shown with no way to clear it. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Searching](https://developer.apple.com/design/human-interface-guidelines/searching)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/searching.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/searching.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/searching.md
git commit -m "feat: add searching knowledge contract"
```

---

## Task 19: Knowledge Contract — `settings`

**Files:**
- Create: `knowledge/human-interface-guidelines/settings.md`

- [ ] **Step 1: Create the file**

```markdown
# Settings

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.settings
type: knowledge
title: Settings
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for where a setting belongs — the system Settings app, a custom in-app settings area, or inline with the task it affects — on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - settings
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/settings
depends_on: []
related:
  - knowledge.human-interface-guidelines.privacy
  - knowledge.human-interface-guidelines.onboarding
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent decides where a given
setting belongs on iOS/iPadOS — inline with the task, in a custom
in-app settings area, or in the system-provided Settings app — and
how to avoid duplicating systemwide options.

## Scope

### Included

-   Choosing between task-inline options, a custom settings area, and the system Settings app
-   Default-value selection to minimize required configuration
-   Avoiding duplication of systemwide/global options
-   Avoiding settings for information the app can detect automatically
-   Deciding what belongs in the system-provided Settings app

### Excluded

-   Settings screen implementation code
-   Settings label/copy wording — see `style-guide`
-   Per-app permission toggle mechanics — see `privacy`
-   macOS settings-window and watchOS-specific patterns (out of scope for this iOS/iPadOS contract)

## Rules

### Rule 1

Agents MUST place task-specific, frequently adjusted options (e.g.,
showing/hiding parts of a view, reordering items, filtering a list)
within the screen or task they affect, not in a separate settings
area.

### Rule 2

Agents SHOULD reserve a custom in-app settings area for general,
infrequently changed options that affect the overall app experience
(e.g., interface style, save behavior, account details).

### Rule 3

Agents MUST NOT duplicate systemwide options — such as accessibility
accommodations, scrolling behavior, or authentication methods —
inside a custom settings area; read and respect the system-level
value instead.

### Rule 4

Agents MUST choose default settings that give the best experience to
the largest number of people, so most people never need to open a
settings area at all.

### Rule 5

Agents SHOULD minimize the total number of settings exposed, since
too many settings make an app feel less approachable and make any
one setting harder to find.

### Rule 6

Agents MUST NOT ask people to manually configure something the app
can detect automatically (e.g., a connected controller, the current
Dark Mode state).

### Rule 7

Agents SHOULD add an option to the system-provided Settings app only
when it is among the most rarely changed options, and SHOULD provide
a button within the app that opens that system Settings entry
directly when doing so.

## Compliant Example

-   ✓ A reading app's font size and view-density controls live inline in the reading view, not in a separate settings screen. (Rule 1)
-   ✓ An app's custom settings area omits a "Reduce Motion" toggle and instead reads the system-wide accessibility setting. (Rule 3)
-   ✓ A game auto-detects a connected controller instead of asking the player to select one. (Rule 6)

## Non-Compliant Example

-   ✗ Changing a list's sort order requires leaving the list and opening a separate settings screen. (Rule 1)
-   ✗ A custom in-app "Contrast" toggle duplicates the system's Increase Contrast accessibility setting. (Rule 3)
-   ✗ The settings area has dozens of rarely used toggles with no clear default behavior. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Settings](https://developer.apple.com/design/human-interface-guidelines/settings)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/settings.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/settings.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/settings.md
git commit -m "feat: add settings knowledge contract"
```

---

## Task 20: Knowledge Contract — `notifications`

**Files:**
- Create: `knowledge/human-interface-guidelines/notifications.md`

- [ ] **Step 1: Create the file**

```markdown
# Notifications

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.notifications
type: knowledge
title: Notifications
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for notification content, timing, foreground handling, actions, and badging on iOS/iPadOS — not the UserNotifications API.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - notifications
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/notifications
depends_on: []
related:
  - knowledge.human-interface-guidelines.privacy
  - knowledge.human-interface-guidelines.feedback
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-06
```

## Intent

This contract defines the design-level rules an AI coding agent
applies when designing notification content and behavior on
iOS/iPadOS: what a notification should say, when to avoid sending
one, how to behave while the app is foregrounded, and how to use
actions and badges. It does not cover `UNUserNotificationCenter`,
`UNAuthorizationOptions`, or any UserNotifications framework API,
which belong to a future dedicated `usernotifications` domain.

## Scope

### Included

-   Notification content structure (title, body, fallback preview text)
-   When to send vs. withhold a notification
-   Foreground-app notification handling
-   Notification action design (count, labels, destructiveness, icons)
-   Badge usage conventions
-   Consent timing (design-level: request before sending, at an appropriate point)

### Excluded

-   `UNUserNotificationCenter`/`UNAuthorizationOptions` implementation — future `usernotifications` domain
-   Notification and action copy/wording specifics — see `style-guide`
-   Permission purpose-string wording and system-alert mechanics — see `privacy`
-   Interface-icon rendering mechanics for action icons — see `sf-symbols`
-   watchOS-specific short-look/long-look/double-tap patterns (out of scope for this iOS/iPadOS contract)

## Rules

### Rule 1

Agents MUST obtain consent before sending notifications and MUST NOT
design a flow that sends notifications prior to that consent (see
`privacy` for permission-request timing and wording).

### Rule 2

Agents MUST write concise, informative notification content: a short,
title-case title with no ending punctuation (or no title, letting the
system show the app name), and succinct sentence-case body text as a
complete sentence, without manually truncating it.

### Rule 3

Agents MUST provide generically descriptive fallback body text (e.g.,
"Friend request," "New comment") for when the person has hidden
notification previews in Settings, without revealing sensitive
details.

### Rule 4

Agents MUST NOT send multiple notifications for the same event, MUST
NOT instruct people to perform an in-app task via notification text
(offer a notification action instead when feasible), and MUST NOT
include sensitive, personal, or confidential information in
notification content.

### Rule 5

Agents MUST use an alert, not a notification, to display an error
message (see `feedback`).

### Rule 6

Agents MUST handle notifications gracefully when the app is
foregrounded by not displaying the notification UI, instead
reflecting the update unobtrusively within the interface (e.g.,
incrementing a badge or inserting new data into the current view).

### Rule 7

Agents SHOULD provide notification actions only for beneficial,
time-saving tasks (up to four), MUST NOT provide an action that
merely opens the app, and SHOULD prefer nondestructive actions,
giving people enough context before any destructive one.

### Rule 8

Agents MUST use a badge (the numbered oval on the app icon) only to
represent the count of unread notifications, keep it current as
notifications are addressed, and MUST NOT rely on badging as the
only way to communicate essential information.

## Compliant Example

-   ✓ A messaging app's notification shows the sender's name and a one-line message preview, with no manual truncation. (Rule 2)
-   ✓ When the app is open and a new message arrives in the currently viewed conversation, no notification is shown — the message simply appears in the list. (Rule 6)
-   ✓ A calendar-event notification offers a "Snooze" action button instead of telling people to open the app and dismiss the alarm. (Rule 4, 7)

## Non-Compliant Example

-   ✗ The app sends a separate notification every few minutes for the same unread message. (Rule 4)
-   ✗ A notification's body reads "Open the app and update your payment method," instructing an in-app task. (Rule 4)
-   ✗ An error is shown as a notification banner instead of an in-app alert. (Rule 5)
-   ✗ The badge count shows the number of items in a shopping cart instead of unread notifications. (Rule 8)

## Dependencies

None.

## References

-   [Apple HIG — Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/notifications.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/notifications.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/notifications.md
git commit -m "feat: add notifications knowledge contract"
```

---

## Task 21: Knowledge Contract — `feedback`

**Files:**
- Create: `knowledge/human-interface-guidelines/feedback.md`

- [ ] **Step 1: Create the file**

```markdown
# Feedback

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.feedback
type: knowledge
title: Feedback
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for matching the form and interruption level of interface feedback to the significance of the information it communicates on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - feedback
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/feedback
depends_on: []
related:
  - knowledge.human-interface-guidelines.notifications
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent designs feedback on
iOS/iPadOS — status, success/failure, warnings, and error
explanations — matching the delivery mechanism to the significance of
the information.

## Scope

### Included

-   Matching feedback interruption level to information significance
-   Passive/inline status feedback placement
-   When to use alerts vs. passive feedback
-   Data-loss warning timing
-   Success/failure confirmation timing
-   Explaining why a command can't be carried out
-   Multi-channel (accessible) feedback delivery

### Excluded

-   Feedback UI implementation code
-   Alert/feedback copy wording — see `style-guide`
-   Haptic feedback implementation
-   Notification-specific content rules — see `notifications`
-   Accessibility API implementation for non-visual feedback channels — see `accessibility` domain

## Rules

### Rule 1

Agents MUST deliver feedback through more than one channel (e.g.,
text or shape paired with color, plus optional sound/haptics) so it
reaches people regardless of how they perceive the device (see
`accessibility`).

### Rule 2

Agents SHOULD integrate passive status feedback into the interface
near the content it describes (e.g., an unread count in a toolbar)
rather than requiring people to take an action to check it.

### Rule 3

Agents MUST match the interruption level of feedback to the
significance of the information: reserve alerts for critical,
ideally actionable information, and avoid using alerts so often that
they lose impact.

### Rule 4

Agents MUST warn people before an action causes data loss that is
unexpected and irreversible, and MUST NOT warn when data loss is the
obvious, expected result of the action.

### Rule 5

Agents SHOULD confirm completion only for significant actions whose
success can't be assumed; avoid adding confirmation feedback for
routine actions people already expect to succeed.

### Rule 6

Agents MUST explain why a command can't be carried out when blocking
or rejecting an action, not just that it failed.

## Compliant Example

-   ✓ A mail app shows the unread-message count directly in the mailbox toolbar rather than requiring a manual refresh check. (Rule 2)
-   ✓ Deleting a file to the Trash produces no warning (expected, recoverable), while permanently erasing it produces a warning alert. (Rule 4)
-   ✓ A directions request with the same start and end location shows an explanation instead of a silent failure. (Rule 6)

## Non-Compliant Example

-   ✗ Success or failure is communicated with a color change alone, with no text or icon. (Rule 1)
-   ✗ An alert interrupts the person for a routine, always-successful action. (Rule 3, 5)
-   ✗ An action silently fails with no explanation of why it couldn't be completed. (Rule 6)

## Dependencies

None.

## References

-   [Apple HIG — Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/feedback.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/feedback.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/feedback.md
git commit -m "feat: add feedback knowledge contract"
```

---

## Task 22: Knowledge Contract — `undo-and-redo`

**Files:**
- Create: `knowledge/human-interface-guidelines/undo-and-redo.md`

- [ ] **Step 1: Create the file**

```markdown
# Undo and Redo

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.undo-and-redo
type: knowledge
title: Undo and Redo
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for predictable, discoverable undo and redo behavior on iOS/iPadOS, including standard gesture and alert conventions.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - undo-and-redo
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/undo-and-redo
depends_on: []
related:
  - knowledge.human-interface-guidelines.feedback
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent designs undo and redo on
iOS/iPadOS so people can predict and see the outcome of reversing
their actions, using standard system-supported triggers rather than
redefined gestures or unlimited custom UI.

## Scope

### Included

-   Making undo/redo outcomes predictable (descriptive labels)
-   Surfacing the visible result of an undo/redo
-   Undo depth (how many actions back people can go)
-   Batch/revert-all options
-   Standard iOS/iPadOS undo/redo triggers (shake-to-undo alert, three-finger swipe, keyboard shortcut)
-   When dedicated undo/redo buttons are appropriate

### Excluded

-   Undo/redo implementation code (undo manager, command stack)
-   Undo/redo alert and menu-item copy wording — see `style-guide`
-   macOS Edit-menu placement and keyboard-shortcut conventions (out of scope for this iOS/iPadOS contract)
-   Toolbar button icon rendering mechanics — see `sf-symbols`

## Rules

### Rule 1

Agents MUST help people predict the outcome of an undo or redo action
— for example, a descriptive shake-to-undo alert or a menu item that
names the action (e.g., "Undo Typing") — rather than a bare,
unqualified "Undo"/"Redo" label.

### Rule 2

Agents MUST make the result of an undo or redo visible, scrolling to
or otherwise surfacing off-screen content so people can see that the
action took effect.

### Rule 3

Agents SHOULD NOT impose an artificial limit on the number of
sequential undo/redo actions; support undoing back through every
action taken since the last logical checkpoint (e.g., opening or
saving a document).

### Rule 4

Agents SHOULD consider offering a way to revert a batch of related
changes at once, or all changes since the last open/save, when that
fits the task.

### Rule 5

Agents MUST NOT redefine the standard iOS/iPadOS undo/redo gestures
(three-finger swipe, shake-to-undo) for a different purpose.

### Rule 6

Agents SHOULD rely on system-supported undo/redo triggers
(shake-to-undo alert, three-finger swipe, a hardware keyboard
shortcut on iPad) rather than adding dedicated undo/redo buttons; if
buttons are necessary, use the standard system-provided symbols in a
toolbar.

## Compliant Example

-   ✓ Shaking the device on iPhone shows an alert reading "Undo Typing" with Undo and Cancel options. (Rule 1)
-   ✓ Undoing the deletion of an off-screen paragraph scrolls the document to show the restored text. (Rule 2)
-   ✓ A drawing app lets people undo every stroke back to when the canvas was opened, with no fixed step limit. (Rule 3)

## Non-Compliant Example

-   ✗ The undo alert reads only "Undo" with no indication of what will be reversed. (Rule 1)
-   ✗ Undo is capped at the last 5 actions regardless of how many changes were made. (Rule 3)
-   ✗ The three-finger swipe gesture is repurposed for page navigation instead of undo/redo. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Undo and Redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/undo-and-redo.md --type knowledge`
Expected: `PASS: knowledge/human-interface-guidelines/undo-and-redo.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/undo-and-redo.md
git commit -m "feat: add undo-and-redo knowledge contract"
```

---

## Task 23: Native Skill — `skills/human-interface-guidelines-components/SKILL.md`

**Files:**
- Create: `skills/human-interface-guidelines-components/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: human-interface-guidelines-components
description: Route Human Interface Guidelines Components/Inputs design tasks to the correct Knowledge Contracts -- lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, and touchscreen gestures. Use when designing or reviewing iOS/iPadOS list/table layout, button hierarchy, modal presentation (sheets/alerts/action sheets), navigation chrome, form controls, or touch gesture usage. This is design-level guidance, not implementation code -- for SwiftUI/UIKit component code see swiftui/uikit; for component label wording see style-guide. Triggers on lists and tables, buttons, sheets, alerts, action sheet, navigation bar, tab bar, pickers, toggles, text fields, menus, touchscreen gestures, HIG components.
id: skill.human-interface-guidelines.components
title: Human Interface Guidelines — Components
version: 0.1.0
status: Draft
artifact_type: skill
domain: Human Interface Guidelines
routes: [knowledge.human-interface-guidelines.lists-and-tables, knowledge.human-interface-guidelines.buttons, knowledge.human-interface-guidelines.sheets, knowledge.human-interface-guidelines.alerts, knowledge.human-interface-guidelines.action-sheets, knowledge.human-interface-guidelines.navigation-bars, knowledge.human-interface-guidelines.tab-bars, knowledge.human-interface-guidelines.pickers, knowledge.human-interface-guidelines.toggles, knowledge.human-interface-guidelines.text-fields, knowledge.human-interface-guidelines.menus, knowledge.human-interface-guidelines.touchscreen-gestures]
related:
  - skill.human-interface-guidelines.foundations
  - skill.human-interface-guidelines.patterns
  - skill.style-guide.writing
last_updated: 2026-08-06
---

# Human Interface Guidelines — Components Skill

## Purpose

Route iOS/iPadOS Components and Inputs design-guidance tasks to the
minimum required Human Interface Guidelines Knowledge Contracts. v1
scope is a curated subset — 11 Components topics plus 1 Inputs topic
(Touchscreen Gestures) — not the full HIG Components/Inputs sections.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/human-interface-guidelines/.

-   List/table structure -> lists-and-tables.md
-   Buttons and menu actions -> buttons.md, menus.md
-   Modal presentation -> sheets.md, alerts.md, action-sheets.md
-   Navigation chrome -> navigation-bars.md, tab-bars.md
-   Form/input controls -> pickers.md, toggles.md, text-fields.md
-   Touch gestures -> touchscreen-gestures.md

Never load more than the contracts relevant to the specific question.
For component label/copy wording, route to `skill.style-guide.writing`
instead. For SwiftUI/UIKit implementation code, route to the `swiftui`
or `uikit` Skill instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. Foundations topics (layout, color,
typography, etc.) route to `skill.human-interface-guidelines.foundations`;
Patterns topics (onboarding, searching, settings, notifications,
feedback, undo/redo) route to `skill.human-interface-guidelines.patterns`.
Any other HIG Components/Inputs topic (e.g. Column Views, Disclosure
Controls, Sliders, Steppers, Toolbars beyond the navigation-bar subset,
Popovers, Context Menus, Apple Pencil, Game Controllers, Keyboards) is
out of scope (see docs/architecture/domain-map.md) — report that
explicitly rather than answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/human-interface-guidelines-components/SKILL.md --type skill`
Expected: `PASS: skills/human-interface-guidelines-components/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/human-interface-guidelines-components/SKILL.md
git commit -m "feat: add human-interface-guidelines-components native skill"
```

---

## Task 24: Native Skill — `skills/human-interface-guidelines-patterns/SKILL.md`

**Files:**
- Create: `skills/human-interface-guidelines-patterns/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: human-interface-guidelines-patterns
description: Route Human Interface Guidelines Patterns design tasks to the correct Knowledge Contracts -- onboarding, searching, settings, notifications, feedback, and undo/redo. Use when designing or reviewing an iOS/iPadOS first-run flow, in-app search placement, settings-screen structure, notification content/timing, status/error feedback, or undo/redo affordances. This is design-level guidance, not implementation code -- for UserNotifications/UIKit/SwiftUI implementation see the respective implementation domain; for copy wording see style-guide. Triggers on onboarding, first-run experience, searching, search UI, settings screen, notification design, feedback, error feedback, undo, redo, HIG patterns.
id: skill.human-interface-guidelines.patterns
title: Human Interface Guidelines — Patterns
version: 0.1.0
status: Draft
artifact_type: skill
domain: Human Interface Guidelines
routes: [knowledge.human-interface-guidelines.onboarding, knowledge.human-interface-guidelines.searching, knowledge.human-interface-guidelines.settings, knowledge.human-interface-guidelines.notifications, knowledge.human-interface-guidelines.feedback, knowledge.human-interface-guidelines.undo-and-redo]
related:
  - skill.human-interface-guidelines.foundations
  - skill.human-interface-guidelines.components
  - skill.style-guide.writing
last_updated: 2026-08-06
---

# Human Interface Guidelines — Patterns Skill

## Purpose

Route iOS/iPadOS Patterns design-guidance tasks to the minimum
required Human Interface Guidelines Knowledge Contracts. v1 scope is a
curated 6-topic subset of HIG Patterns, not the full section.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/human-interface-guidelines/.

-   First-run flow -> onboarding.md
-   Search UI -> searching.md
-   Settings screen structure -> settings.md
-   Notification design -> notifications.md
-   System/status feedback -> feedback.md
-   Undo/redo affordances -> undo-and-redo.md

Never load more than the contracts relevant to the specific question.
For pattern copy/wording, route to `skill.style-guide.writing` instead.
Notification *design* is covered here; the UserNotifications API
belongs to a future Tier 2 domain, not yet built.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. Foundations topics route to
`skill.human-interface-guidelines.foundations`; Components/Inputs
topics route to `skill.human-interface-guidelines.components`. Any
other HIG Patterns topic (e.g. Charts, Drag and Drop, Entering Data,
Full-Screen Experiences, Launching, Loading, Managing Accounts,
Modality, Multitasking, Playing Audio, Printing, Ratings and Reviews,
Sharing, Status, Syncing, Workouts) is out of scope (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/human-interface-guidelines-patterns/SKILL.md --type skill`
Expected: `PASS: skills/human-interface-guidelines-patterns/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/human-interface-guidelines-patterns/SKILL.md
git commit -m "feat: add human-interface-guidelines-patterns native skill"
```

---

## Task 25: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add two new Discovery Rules rows**

In the `## Discovery Rules` table, find this exact row:

```markdown
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |
```

Replace with (original row plus two new rows immediately after it):

```markdown
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |
| lists and tables, buttons, sheets, alerts, action sheet, navigation bar, tab bar, pickers, toggles, text fields, menus, touchscreen gestures, HIG components | skills/human-interface-guidelines-components/SKILL.md |
| onboarding, first-run experience, searching, search UI, settings screen, notification design, feedback, error feedback, undo, redo, HIG patterns | skills/human-interface-guidelines-patterns/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `14` (authentication, style-guide, human-interface-guidelines,
human-interface-guidelines-components, human-interface-guidelines-patterns,
app-store-review-guidelines, swiftui, accessibility, uikit, sf-symbols,
networking, xcode, local-authentication, app-tracking-transparency)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add human-interface-guidelines-components/patterns to skills index"
```

---

## Task 26: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `human-interface-guidelines` clause in the Build Order Completed line**

Find this exact substring within the "Completed:" line (line 19):

```markdown
`human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt),
```

Replace with:

```markdown
`human-interface-guidelines` (Tier 1 — Foundations v1 (15 KCs) plus a curated Patterns/Components/Inputs v1 (18 KCs): Patterns (onboarding, searching, settings, notifications, feedback, undo/redo), Components (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus), and one Inputs topic (touchscreen gestures); remaining Patterns/Components/Inputs topics (e.g. Charts, Drag and Drop, Multitasking, Column Views, Sliders, Toolbars beyond navigation, Apple Pencil, Game Controllers) remain unbuilt),
```

Also update the trailing tally at the end of the same line. Find:

```markdown
**All 11 Tier 1 domains complete** (12 domains completed total, including `authentication` cross-cutting/unscheduled).
```

Replace with:

```markdown
**All 11 Tier 1 domains complete** (12 domains completed total, including `authentication` cross-cutting/unscheduled); `human-interface-guidelines` expanded post-completion to add its Patterns/Components v1.
```

- [ ] **Step 2: Add one new Cross-Domain Notes bullet**

Add this bullet at the end of the `## Cross-Domain Notes` list (after the
`app-tracking-transparency`/`permission-usage-strings` bullet, which is
currently the last one):

```markdown
- `human-interface-guidelines` (`notifications` Patterns topic) and the future `usernotifications` domain (Tier 2, unbuilt) overlap: this domain's angle is notification *design* (content structure, when/how to request permission, foreground handling, action design, badging), the future domain's angle will be `UNUserNotificationCenter`/`UNAuthorizationOptions` API implementation. Flagged proactively (before `usernotifications` is built) so the boundary is pre-decided, same practice already used for the `privacy`/`testing`/`security` Tier 2 boundaries above. `notifications.md`'s Excluded section already names this boundary explicitly.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "human-interface-guidelines-components\|human-interface-guidelines-patterns" docs/architecture/domain-map.md`
Expected: a number greater than 0

- [ ] **Step 4: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope HIG Patterns/Components v1, add usernotifications cross-domain note"
```

---

## Task 27: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add two new Skills bullets**

Find this exact block in `## Skills` (the `human-interface-guidelines`
bullet, immediately before the `app-store-review-guidelines` bullet):

```markdown
- **`human-interface-guidelines`** — Routes iOS/iPadOS visual design tasks (layout, color, typography, dark mode, materials, motion, icons, branding, accessibility-design, privacy UI, RTL) to HIG Foundations Knowledge Contracts.
```

Replace with:

```markdown
- **`human-interface-guidelines`** — Routes iOS/iPadOS visual design tasks (layout, color, typography, dark mode, materials, motion, icons, branding, accessibility-design, privacy UI, RTL) to HIG Foundations Knowledge Contracts.

- **`human-interface-guidelines-components`** — Routes iOS/iPadOS Components/Inputs design tasks (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures) to HIG Components Knowledge Contracts.
  Example: `"review this list screen's layout against HIG"` → `lists-and-tables.md`
  Example: `"when should I use an action sheet instead of an alert"` → `action-sheets.md`

- **`human-interface-guidelines-patterns`** — Routes iOS/iPadOS Patterns design tasks (onboarding, searching, settings, notifications, feedback, undo/redo) to HIG Patterns Knowledge Contracts.
  Example: `"design an onboarding flow for a fitness app"` → `onboarding.md`
  Example: `"how should notification content be worded and when should we send one"` → `notifications.md`
```

- [ ] **Step 2: Update the What's New section (3-item cap)**

Find this exact block (the current `## What's New` section — 3 dated
lines plus the CHANGELOG.md link):

```markdown
## What's New

- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- 2026-08-05 — Added `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication` (which excludes biometrics entirely), replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

Replace with (new line added at top, oldest of the 3 — the `xcode`
line — drops off since the cap stays at 3 dated lines):

```markdown
## What's New

- 2026-08-06 — Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap (Foundations-only HIG coverage). First domain with more than one Skill, split by Apple's own information architecture to stay under the project's Reference/Skill size caps. Flags a new `usernotifications` (Tier 2) cross-domain boundary in domain-map.md.
- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- 2026-08-05 — Added `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication` (which excludes biometrics entirely), replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "human-interface-guidelines-components\|human-interface-guidelines-patterns" README.md`
Expected: a number greater than 0

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add human-interface-guidelines-components/patterns to README Skills + What's New"
```

---

## Task 28: Update `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add a new Unreleased entry**

Find this exact block (the current `## [Unreleased]` section — empty
since v1.0.2 shipped):

```markdown
## [Unreleased]

## [1.0.2] - 2026-08-05
```

Replace with:

```markdown
## [Unreleased]
### Added
- Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap. First domain with more than one Skill, split by Apple's own Foundations/Patterns/Components information architecture to stay under the project's Reference (≤80 lines) and Skill (≤60 lines) size caps.

## [1.0.2] - 2026-08-05
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "human-interface-guidelines-components" CHANGELOG.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add HIG Patterns/Components changelog entry"
```

---

## Task 29: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new and modified artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/human-interface-guidelines.md --type reference
python3 scripts/validate_artifact.py references/apple/human-interface-guidelines-components.md --type reference
python3 scripts/validate_artifact.py references/apple/human-interface-guidelines-patterns.md --type reference
python3 scripts/validate_artifact.py skills/human-interface-guidelines/SKILL.md --type skill
python3 scripts/validate_artifact.py skills/human-interface-guidelines-components/SKILL.md --type skill
python3 scripts/validate_artifact.py skills/human-interface-guidelines-patterns/SKILL.md --type skill
for f in lists-and-tables buttons sheets alerts action-sheets navigation-bars tab-bars pickers toggles text-fields menus touchscreen-gestures onboarding searching settings notifications feedback undo-and-redo; do
  python3 scripts/validate_artifact.py "knowledge/human-interface-guidelines/$f.md" --type knowledge
done
```
Expected: `PASS` for all 24 files (3 references + 3 skills + 18 knowledge contracts).

- [ ] **Step 2: Confirm line-cap compliance on the two new Reference and two new Skill files**

Run: `wc -l references/apple/human-interface-guidelines-components.md references/apple/human-interface-guidelines-patterns.md skills/human-interface-guidelines-components/SKILL.md skills/human-interface-guidelines-patterns/SKILL.md`
Expected: both Reference files ≤80 lines, both Skill files ≤60 lines.

- [ ] **Step 3: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 4: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 5: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 28 prior tasks committed).

- [ ] **Step 6: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire HIG Patterns/Components
expansion (all 22 new files plus the 6 modified files: the Foundations
Reference and Skill, `skills/index.md`, `domain-map.md`, `README.md`,
`CHANGELOG.md`) to check cross-file consistency: every `related:`/
`depends_on:` KC id resolves to a real file (including the
cross-domain ones into `style-guide` and `accessibility`), each new
Skill's `routes:` list matches exactly its Reference's "Used By" list,
layer order (References → Knowledge → Skills) is respected, and the
Foundations Skill's `related:`/Stop Conditions edits from Task 2 are
internally consistent with the two new sibling skills. Specifically
check for:

-   No KC content anywhere describing implementation code (SwiftUI/
    UIKit/UserNotifications APIs) — this expansion is design-level only
-   No KC restates `style-guide` or `accessibility` domain Rules
    beyond a `related:` cross-reference — verify the angle-split
    boundary actually holds, not just that it's described correctly
-   `navigation-bars.md` and `touchscreen-gestures.md` correctly
    explain their source-URL redirects (to `toolbars` and `gestures`
    respectively) in their `## Intent` sections without this reading
    as an unexplained scope inconsistency
-   Every cited Apple Developer HIG URL is live (spot-check a sample
    with `curl -s -o /dev/null -w "%{http_code}" -L <url>`)
-   Check whether any existing Skill's `description`/trigger-word list
    now collides with the two new Skills' trigger words, the way
    `skills/authentication/SKILL.md` collided with
    `local-authentication`'s trigger words in a prior domain build

Report findings; fix any issues found and re-commit before considering
this expansion complete.

- [ ] **Step 7: Merge to main**

Once Step 6 passes, use `superpowers:finishing-a-development-branch`
to decide how to integrate `feature/hig-patterns-components-domain`
into `main` (merge, PR, or cleanup) — matching how every prior domain
branch in this repo's history was integrated via PR.

---

## Self-Review Notes

-   **Spec coverage:** All 18 KC topics from the design spec's
    "Knowledge Contracts (18 new)" section have a task (Tasks 5–22),
    matching titles and scope exactly, including the two source-URL
    corrections discovered during content drafting (`navigation-bars`
    → `toolbars`, `touchscreen-gestures` → `gestures`) and the
    confirmation that `action-sheets` survived as a separate page
    (18 total, not the spec's fallback 17). The spec's File Layout
    section is Tasks 1–4 (existing Reference/Skill updates) and Tasks
    3–4/23–24 (new Reference/Skill pairs). The spec's Cross-Domain
    Boundaries section (`usernotifications`) is reflected in Task 26
    Step 2. The spec's Documentation Updates section is covered by
    Tasks 25, 26, 27, 28. The spec's "Router Update:
    `skills/apple-agent-kit/SKILL.md`" section was dropped from this
    plan after inspecting the actual file — it's a generic pointer to
    `skills/index.md` with no per-skill routing table to update, unlike
    what the spec assumed; `skills/index.md` (Task 25) is the correct
    and only routing-table file, consistent with how every prior
    domain plan (e.g. the `app-tracking-transparency` plan) actually
    updated it instead.
-   **Placeholder scan:** No TBD/TODO; every Rule, Example, and
    Reference URL is concrete. All 18 KCs were drafted by two
    dispatched research subagents that pulled real content from
    Apple's HIG data API (not the model's prior knowledge), and their
    claims (URL redirects, cross-referenced KC ids) were independently
    spot-verified via `curl` and `ls` against the actual repo before
    this plan was written.
-   **Type/id consistency:** Every KC `id`
    (`knowledge.human-interface-guidelines.<slug>`) referenced in Task
    23/24's `routes:` lists and Task 3/4's "Used By" lists matches the
    `id` defined in that KC's own Task 5–22 Metadata block. Every
    `related:` cross-reference within the domain (e.g. `alerts.md` ↔
    `action-sheets.md`, `notifications.md` ↔ `feedback.md`) points at
    an id defined in this same plan or the existing 15 Foundations
    KCs. Every cross-domain `related:` reference (into `style-guide`
    and `accessibility`) points at a filename confirmed to exist in
    `knowledge/style-guide/` or `knowledge/accessibility/` (checked
    directly against the repo before this plan was written, not
    assumed from the subagents' reports).
