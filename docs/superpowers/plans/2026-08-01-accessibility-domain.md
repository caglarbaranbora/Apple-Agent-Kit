# Accessibility Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `accessibility` domain (1 Reference, 12 Knowledge Contracts, 1 native Skill) covering SwiftUI + UIKit Accessibility API implementation conventions, per `docs/superpowers/specs/2026-08-01-accessibility-domain-design.md`, resolving the outstanding `human-interface-guidelines` and `swiftui` forward-references.

**Architecture:** Mirrors the `swiftui` domain exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/accessibility.md`

**Files:**
- Create: `references/apple/accessibility.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/accessibility/

## Purpose

Reference index for Apple's Accessibility API documentation across
SwiftUI and UIKit — implementation-conventions scope (labeling, traits,
value/hint, custom actions, element grouping, navigation order, Dynamic
Type API, reduce-motion/transparency/increase-contrast, keyboard access
and focus, hidden/decorative elements, accessibility audits). Design-level
accessibility guidance (Dynamic Type requirement, contrast ratio,
color-alone prohibition, gesture-alternative rule) is owned by
`human-interface-guidelines`, not this domain — see
docs/architecture/domain-map.md Cross-Domain Notes. General XCTest/UI
testing conventions beyond accessibility audits are out of scope for this
pass.

## Primary Topics

- Accessibility labels
- Accessibility traits
- Accessibility value and hint
- Custom accessibility actions
- Accessibility element grouping
- VoiceOver navigation order
- Dynamic Type API
- Reduce Motion
- Reduce Transparency and Increase Contrast
- Full Keyboard Access and accessibility focus
- Hidden and decorative elements
- Accessibility audits and testing

## Used By

- knowledge/accessibility/accessibility-labels.md ([[knowledge/accessibility/accessibility-labels]])
- knowledge/accessibility/accessibility-traits.md ([[knowledge/accessibility/accessibility-traits]])
- knowledge/accessibility/accessibility-value-and-hint.md ([[knowledge/accessibility/accessibility-value-and-hint]])
- knowledge/accessibility/custom-accessibility-actions.md ([[knowledge/accessibility/custom-accessibility-actions]])
- knowledge/accessibility/accessibility-element-grouping.md ([[knowledge/accessibility/accessibility-element-grouping]])
- knowledge/accessibility/voiceover-navigation-order.md ([[knowledge/accessibility/voiceover-navigation-order]])
- knowledge/accessibility/dynamic-type-api.md ([[knowledge/accessibility/dynamic-type-api]])
- knowledge/accessibility/reduce-motion.md ([[knowledge/accessibility/reduce-motion]])
- knowledge/accessibility/reduce-transparency-increase-contrast.md ([[knowledge/accessibility/reduce-transparency-increase-contrast]])
- knowledge/accessibility/full-keyboard-access-and-focus.md ([[knowledge/accessibility/full-keyboard-access-and-focus]])
- knowledge/accessibility/accessibility-hidden-decorative.md ([[knowledge/accessibility/accessibility-hidden-decorative]])
- knowledge/accessibility/accessibility-audits-testing.md ([[knowledge/accessibility/accessibility-audits-testing]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/accessibility.md --type reference`
Expected: `PASS: references/apple/accessibility.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/accessibility.md
git commit -m "docs: add accessibility reference index"
```

---

## Task 2: Knowledge Contract — `accessibility-labels`

**Files:**
- Create: `knowledge/accessibility/accessibility-labels.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility Labels

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-labels
type: knowledge
title: Accessibility Labels
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to set accessibilityLabel (SwiftUI .accessibilityLabel(), UIKit accessibilityLabel) so VoiceOver announces a concise, meaningful name for every element that needs one.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - labels
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilitylabel
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.accessibility.accessibility-traits
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent sets `accessibilityLabel`
(SwiftUI `.accessibilityLabel()`, UIKit `accessibilityLabel`) so VoiceOver
announces a concise, meaningful name for every element that needs one,
implementing the API-level half of the labeling requirement HIG's
`accessibility.md` sets at the design level.

## Scope

### Included

-   When a custom label is required vs. when the default suffices
-   Concise, noun-phrase label wording
-   Avoiding redundant or state-encoding labels

### Excluded

-   Which trait an element should carry — see `accessibility-traits`
-   Communicating dynamic value/state — see `accessibility-value-and-hint`
-   Whether contrast/text-scaling makes a label legible — owned by `human-interface-guidelines`'s `accessibility.md`

## Rules

### Rule 1

Agents MUST set `accessibilityLabel` (`.accessibilityLabel()` in SwiftUI,
`accessibilityLabel` in UIKit) on every interactive or informative
element whose visible content is an icon, image, or symbol with no
adjacent text — VoiceOver has no other source for that element's name.

### Rule 2

Agents MUST NOT set a custom `accessibilityLabel` on an element that
already displays plain, sufficient text (e.g. a `Text`/`UILabel` showing
its own content) unless the visible text is itself insufficient out of
context — a redundant custom label just duplicates or overrides correct
default behavior.

### Rule 3

Agents MUST write labels as concise noun phrases describing what the
element is, without restating its type ("Delete", not "Delete button" or
"Delete icon") — VoiceOver appends the control's role from its trait
automatically.

### Rule 4

Agents MUST NOT encode dynamic state (selected, on/off, count) inside
`accessibilityLabel` — state belongs in `accessibilityValue` or a trait
like `.isSelected`, so the label stays stable while the value updates
independently.

### Rule 5

Agents SHOULD localize accessibility labels through the same
localization pipeline as visible strings, not hardcode English text that
visible UI already localizes.

## Compliant Example

```swift
Button {
    deleteItem()
} label: {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete")
```
Icon-only button gets a concise, stable label; VoiceOver announces "Delete, button." (Rules 1, 3)

## Non-Compliant Example

```swift
Button {
    toggleFavorite()
} label: {
    Image(systemName: isFavorite ? "star.fill" : "star")
}
.accessibilityLabel(isFavorite ? "Favorited star icon, tap to unfavorite" : "Star icon, tap to favorite")
```
Verbose label restates the control type ("icon") and encodes instructions and state that belong in a trait/value, not the label. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:))
-   [Apple Developer — UIAccessibility accessibilityLabel](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilitylabel)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/accessibility-labels.md --type knowledge`
Expected: `PASS: knowledge/accessibility/accessibility-labels.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/accessibility-labels.md
git commit -m "docs: add accessibility accessibility-labels knowledge contract"
```

---

## Task 3: Knowledge Contract — `accessibility-traits`

**Files:**
- Create: `knowledge/accessibility/accessibility-traits.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility Traits

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-traits
type: knowledge
title: Accessibility Traits
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of accessibilityTraits (SwiftUI .accessibilityAddTraits()/.accessibilityRemoveTraits(), UIKit accessibilityTraits) so VoiceOver announces an element's role and state correctly.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - traits
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilitytraits
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.accessibility.accessibility-labels
  - knowledge.accessibility.accessibility-value-and-hint
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent assigns
`accessibilityTraits` (SwiftUI `.accessibilityAddTraits()`/
`.accessibilityRemoveTraits()`, UIKit `accessibilityTraits`) so VoiceOver
announces an element's role (button, header, selected) correctly,
especially for custom controls built from non-semantic base views.

## Scope

### Included

-   Assigning role traits (`.isButton`, `.isHeader`, `.isImage`) to custom controls
-   Toggling `.isSelected` with selection state
-   `.updatesFrequently` for continuously changing values
-   Avoiding conflicting trait combinations

### Excluded

-   Label wording itself — see `accessibility-labels`
-   Value/hint content — see `accessibility-value-and-hint`

## Rules

### Rule 1

Agents MUST add the matching role trait (e.g. `.isButton`) when building
a custom interactive control from a non-semantic base view (a `Text` or
`Image` wrapped in `.onTapGesture`, or a plain UIKit `UIView` with a tap
gesture recognizer) — without it, VoiceOver announces the element with no
role at all.

### Rule 2

Agents MUST add `.isHeader` to a view acting as a section/screen heading
that isn't a native heading-styled control, so VoiceOver's headings
rotor can navigate to it.

### Rule 3

Agents MUST toggle `.isSelected` (`.accessibilityAddTraits(.isSelected)`/
`.accessibilityRemoveTraits(.isSelected)` in SwiftUI, the `.selected`
trait in UIKit) to match live selection state, rather than encoding
selection only in the visible label or value.

### Rule 4

Agents MUST NOT combine traits that describe conflicting roles on the
same element (e.g. `.isButton` and `.isStaticText` together) — pick the
trait set that matches the element's actual interactive behavior.

### Rule 5

Agents SHOULD add `.updatesFrequently` to elements whose value changes
continuously (live progress, a running timer) so VoiceOver throttles
re-announcements instead of interrupting speech on every update.

## Compliant Example

```swift
Text("Chapter 1")
    .font(.title2)
    .accessibilityAddTraits(.isHeader)

Image(systemName: "checkmark.circle")
    .onTapGesture { toggleDone() }
    .accessibilityLabel("Mark done")
    .accessibilityAddTraits(isDone ? [.isButton, .isSelected] : .isButton)
```
Explicit header trait for a non-native heading; selection trait toggled with state. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
Text("Chapter 1")
    .font(.title2)

Image(systemName: "checkmark.circle")
    .onTapGesture { toggleDone() }
    .accessibilityLabel("Mark done")
```
No `.isHeader` trait, so the headings rotor skips "Chapter 1"; no `.isButton` trait, so VoiceOver announces the tappable checkmark with no role at all. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityAddTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:))
-   [Apple Developer — UIAccessibilityTraits](https://developer.apple.com/documentation/uikit/uiaccessibilitytraits)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/accessibility-traits.md --type knowledge`
Expected: `PASS: knowledge/accessibility/accessibility-traits.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/accessibility-traits.md
git commit -m "docs: add accessibility accessibility-traits knowledge contract"
```

---

## Task 4: Knowledge Contract — `accessibility-value-and-hint`

**Files:**
- Create: `knowledge/accessibility/accessibility-value-and-hint.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility Value and Hint

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-value-and-hint
type: knowledge
title: Accessibility Value and Hint
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of accessibilityValue for a custom control's current state and accessibilityHint for the outcome of an ambiguous action, in SwiftUI and UIKit.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - value
  - hint
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)
  - https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityvalue
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityhint
depends_on: []
related:
  - knowledge.accessibility.accessibility-labels
  - knowledge.accessibility.accessibility-traits
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent communicates a custom
control's live state via `accessibilityValue` and the outcome of a
non-obvious action via `accessibilityHint`, so VoiceOver users get the
same state and outcome information sighted users get visually.

## Scope

### Included

-   `accessibilityValue` for custom sliders/steppers/segmented controls
-   Keeping value live/computed, not a stale literal
-   `accessibilityHint` for non-obvious action outcomes
-   Avoiding label/value/hint duplication

### Excluded

-   Element naming — see `accessibility-labels`
-   Role/state traits — see `accessibility-traits`

## Rules

### Rule 1

Agents MUST set `accessibilityValue` (SwiftUI `.accessibilityValue()`,
UIKit `accessibilityValue`) on any custom control that carries a value
not conveyed by its label — a custom slider, star rating, or segmented
control needs its current selection/level spoken separately from its
name.

### Rule 2

Agents MUST bind `accessibilityValue` to a computed expression that
reflects the current state, not a literal string captured once — a stale
value announces the wrong state after the control changes.

### Rule 3

Agents SHOULD add `accessibilityHint` (SwiftUI `.accessibilityHint()`,
UIKit `accessibilityHint`) only when the result of activating the
element isn't obvious from its label and trait alone (e.g. "Deletes this
message" on a swipe-triggered action with no visible confirmation).

### Rule 4

Agents MUST NOT restate the label's content inside the hint — the hint
describes the *outcome* of interacting with the element, not what the
element already says it is.

### Rule 5

Agents MUST NOT put information required to use the control only in the
hint — hints are supplementary; anything essential belongs in the label
or value so it's never missed.

## Compliant Example

```swift
Slider(value: $volume, in: 0...100)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume)) percent")
```
Live, computed value reflects the current slider position on every read. (Rules 1, 2)

## Non-Compliant Example

```swift
Slider(value: $volume, in: 0...100)
    .accessibilityLabel("Volume, currently 50 percent")
```
The starting value is baked into the label as a one-time string; it never updates as `volume` changes, and the value's role belongs in `accessibilityValue`, not the label. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:))
-   [Apple Developer — accessibilityHint(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:))
-   [Apple Developer — UIAccessibilityElement accessibilityValue](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityvalue)
-   [Apple Developer — UIAccessibilityElement accessibilityHint](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityhint)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/accessibility-value-and-hint.md --type knowledge`
Expected: `PASS: knowledge/accessibility/accessibility-value-and-hint.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/accessibility-value-and-hint.md
git commit -m "docs: add accessibility accessibility-value-and-hint knowledge contract"
```

---

## Task 5: Knowledge Contract — `custom-accessibility-actions`

**Files:**
- Create: `knowledge/accessibility/custom-accessibility-actions.md`

- [ ] **Step 1: Create the file**

```markdown
# Custom Accessibility Actions

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.custom-accessibility-actions
type: knowledge
title: Custom Accessibility Actions
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of .accessibilityAction() (SwiftUI) and UIAccessibilityCustomAction (UIKit) to give VoiceOver users a reachable alternative to gesture-only interactions like swipe-to-delete or drag-to-reorder.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - actions
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction
depends_on: []
related:
  - knowledge.accessibility.full-keyboard-access-and-focus
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent exposes gesture-only
interactions (swipe-to-delete, drag-to-reorder, long-press) to VoiceOver
via `.accessibilityAction()` (SwiftUI) or `UIAccessibilityCustomAction`
(UIKit), since VoiceOver intercepts standard touch gestures for its own
navigation.

## Scope

### Included

-   `.accessibilityAction(named:_:)` for named custom actions
-   `UIAccessibilityCustomAction`/`accessibilityCustomActions`
-   `.accessibilityAction(.magicTap)` for a screen's primary action
-   Action naming

### Excluded

-   Moving VoiceOver/keyboard focus itself — see `full-keyboard-access-and-focus`

## Rules

### Rule 1

Agents MUST provide an `.accessibilityAction()` (or
`UIAccessibilityCustomAction`) equivalent for any interaction reachable
only through a gesture VoiceOver intercepts (swipe-to-delete on a list
row, drag-to-reorder, long-press context menus) — without one, VoiceOver
users cannot perform that action at all.

### Rule 2

Agents MUST give each custom action a clear, verb-based name ("Delete",
"Move up") describing the action, not the gesture it replaces ("Swipe
left").

### Rule 3

Agents SHOULD implement `.accessibilityAction(.magicTap)` for a screen's
single most common action (e.g. play/pause on a media player) so a
two-finger double-tap performs it without navigating to a specific
element first.

### Rule 4

Agents MUST NOT rely on multi-finger or complex custom gestures
(pinch, multi-finger swipe) as the only way to trigger a feature without
also exposing a custom action or standard control, since VoiceOver
remaps most multi-finger gestures to its own navigation.

## Compliant Example

```swift
RowView(item: item)
    .accessibilityAction(named: "Delete") {
        delete(item)
    }
    .accessibilityAction(named: "Move Up") {
        moveUp(item)
    }
```
Swipe-to-delete and drag-to-reorder both get named VoiceOver-reachable equivalents. (Rules 1, 2)

## Non-Compliant Example

```swift
RowView(item: item)
    .swipeActions {
        Button("Delete", role: .destructive) { delete(item) }
    }
```
`.swipeActions` alone is reachable by touch but not guaranteed to surface to VoiceOver as an activatable action without an explicit `.accessibilityAction()`; a VoiceOver user swiping through the list has no way to trigger the delete. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityAction(named:_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:))
-   [Apple Developer — UIAccessibilityCustomAction](https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/custom-accessibility-actions.md --type knowledge`
Expected: `PASS: knowledge/accessibility/custom-accessibility-actions.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/custom-accessibility-actions.md
git commit -m "docs: add accessibility custom-accessibility-actions knowledge contract"
```

---

## Task 6: Knowledge Contract — `accessibility-element-grouping`

**Files:**
- Create: `knowledge/accessibility/accessibility-element-grouping.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility Element Grouping

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-element-grouping
type: knowledge
title: Accessibility Element Grouping
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of .accessibilityElement(children:) (SwiftUI) and isAccessibilityElement/accessibilityElements (UIKit) to control whether a composite view is one VoiceOver stop or several.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - grouping
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement
depends_on: []
related:
  - knowledge.accessibility.voiceover-navigation-order
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent controls whether a
composite view (icon + title + subtitle row, a card containing an
embedded button) becomes one VoiceOver stop or several, using
`.accessibilityElement(children:)` in SwiftUI and `isAccessibilityElement`/
`accessibilityElements` in UIKit.

## Scope

### Included

-   `.accessibilityElement(children: .combine)` for merging static composite content
-   `.accessibilityElement(children: .contain)` for grouping without merging interactive children
-   `.accessibilityElement(children: .ignore)` with an explicit label
-   UIKit `isAccessibilityElement` and container `accessibilityElements`

### Excluded

-   The order elements are read in — see `voiceover-navigation-order`
-   Hiding purely decorative content — see `accessibility-hidden-decorative`

## Rules

### Rule 1

Agents MUST group a row of purely static, related content (icon +
title + subtitle with no independently interactive children) with
`.accessibilityElement(children: .combine)` so VoiceOver announces it as
one stop instead of three separate swipes.

### Rule 2

Agents MUST use `.accessibilityElement(children: .contain)` — not
`.combine` — when a composite view contains a child that must remain
independently activatable (e.g. a card with body text plus an embedded
button), so the button stays individually reachable while the group
still scopes rotor/frame navigation.

### Rule 3

Agents MUST supply an explicit `.accessibilityLabel()` when using
`.accessibilityElement(children: .ignore)` — `.ignore` hides all child
content from the accessibility tree, so without a label the element
becomes an unannounced blank stop.

### Rule 4

Agents MUST set `isAccessibilityElement = false` on a UIKit container
`UIView` that exists only to lay out already-accessible subviews, so
VoiceOver does not create a duplicate, uninformative stop for the empty
container itself.

### Rule 5

Agents SHOULD populate a UIKit container's `accessibilityElements` array
to scope a composite view to exactly the children that should be
individually exposed — any subview not listed in the array is excluded
from VoiceOver entirely, which is UIKit's equivalent of SwiftUI's
`.combine`/`.contain` grouping choice. Setting the array's *order* (as
opposed to its membership) is covered by `voiceover-navigation-order`.

## Compliant Example

```swift
HStack {
    Image(systemName: "person.crop.circle")
    VStack(alignment: .leading) {
        Text(user.name)
        Text(user.email)
    }
}
.accessibilityElement(children: .combine)
```
Icon, name, and email announce as one combined VoiceOver stop. (Rule 1)

## Non-Compliant Example

```swift
HStack {
    Image(systemName: "person.crop.circle")
    VStack(alignment: .leading) {
        Text(user.name)
        Text(user.email)
    }
}
```
No grouping: VoiceOver treats the icon, name, and email as three separate stops a user must swipe through individually to understand one logical row. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityElement(children:)](https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:))
-   [Apple Developer — UIAccessibility isAccessibilityElement](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/accessibility-element-grouping.md --type knowledge`
Expected: `PASS: knowledge/accessibility/accessibility-element-grouping.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/accessibility-element-grouping.md
git commit -m "docs: add accessibility accessibility-element-grouping knowledge contract"
```

---

## Task 7: Knowledge Contract — `voiceover-navigation-order`

**Files:**
- Create: `knowledge/accessibility/voiceover-navigation-order.md`

- [ ] **Step 1: Create the file**

```markdown
# VoiceOver Navigation Order

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.voiceover-navigation-order
type: knowledge
title: VoiceOver Navigation Order
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of accessibilitySortPriority (SwiftUI) and an explicit accessibilityElements order (UIKit) to fix VoiceOver reading order when it diverges from visual/z-order layout.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - navigation-order
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilitycontainer
depends_on: []
related:
  - knowledge.accessibility.accessibility-element-grouping
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent controls VoiceOver's
reading order using `.accessibilitySortPriority()` (SwiftUI) or an
explicit `accessibilityElements` array (UIKit), for layouts where
default visual/z-order traversal produces the wrong reading order.

## Scope

### Included

-   `.accessibilitySortPriority()` for overlapping/`ZStack` layouts
-   UIKit's `accessibilityElements` explicit ordering
-   When default order is already correct (no action needed)

### Excluded

-   Whether elements are merged into one stop — see `accessibility-element-grouping`

## Rules

### Rule 1

Agents MUST set `.accessibilitySortPriority()` explicitly on elements
inside a `ZStack` or other overlapping layout whose intended reading
order doesn't match declaration order — SwiftUI's default reading order
follows visual layout, which is ambiguous for overlapping content.

### Rule 2

Agents MUST NOT rely on default left-to-right, top-to-bottom traversal
for absolutely positioned or manually offset elements where that
traversal would read content out of logical order.

### Rule 3

Agents MUST populate a UIKit container's `accessibilityElements` array
explicitly, in the desired reading order, whenever the default
view-hierarchy order produces an incorrect sequence.

### Rule 4

Agents SHOULD keep sort-priority overrides local and minimal — reorder
only the specific elements that are wrong rather than assigning priority
values across an entire screen, which becomes fragile as the layout
changes.

## Compliant Example

```swift
ZStack {
    BackgroundImage()
        .accessibilityHidden(true)
    VStack {
        Text("Title").accessibilitySortPriority(2)
        Text("Subtitle").accessibilitySortPriority(1)
    }
}
```
Explicit priority guarantees "Title" is read before "Subtitle" regardless of z-order. (Rule 1)

## Non-Compliant Example

```swift
ZStack(alignment: .bottomLeading) {
    Text("Subtitle")
    Text("Title").offset(y: -40)
}
```
No sort priority: VoiceOver's traversal of the overlapping, offset content is unpredictable and may read "Subtitle" before "Title" despite the intended visual hierarchy. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilitySortPriority(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:))
-   [Apple Developer — UIAccessibilityContainer](https://developer.apple.com/documentation/uikit/uiaccessibilitycontainer)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/voiceover-navigation-order.md --type knowledge`
Expected: `PASS: knowledge/accessibility/voiceover-navigation-order.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/voiceover-navigation-order.md
git commit -m "docs: add accessibility voiceover-navigation-order knowledge contract"
```

---

## Task 8: Knowledge Contract — `dynamic-type-api`

**Files:**
- Create: `knowledge/accessibility/dynamic-type-api.md`

- [ ] **Step 1: Create the file**

```markdown
# Dynamic Type API

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.dynamic-type-api
type: knowledge
title: Dynamic Type API
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of @ScaledMetric (SwiftUI) and UIFontMetrics (UIKit) to scale custom spacing/sizing with Dynamic Type, and text-style-based fonts instead of fixed point sizes — the API-implementation half of HIG's Dynamic Type requirement.
domain: Accessibility
tags:
  - accessibility
  - dynamic-type
references:
  - https://developer.apple.com/documentation/swiftui/scaledmetric
  - https://developer.apple.com/documentation/uikit/uifontmetrics
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent implements Dynamic Type
support at the API level — `@ScaledMetric` (SwiftUI) and
`UIFontMetrics.scaledFont(for:)` (UIKit) for custom numeric
spacing/sizing, and text-style-based fonts instead of fixed point sizes —
implementing the requirement HIG's `accessibility.md` Rule 1 sets at the
design level (text must scale to at least 200% without loss of content).

## Scope

### Included

-   `@ScaledMetric` for custom spacing/icon-size constants
-   `UIFontMetrics.scaledFont(for:)` and `adjustsFontForContentSizeCategory`
-   Text-style fonts (`.font(.body)`, `UIFont.preferredFont(forTextStyle:)`) vs fixed point sizes
-   Capping unconstrained scaling where it breaks layout

### Excluded

-   Layout not breaking/truncating at large sizes — owned by `human-interface-guidelines`'s `accessibility.md`/`layout.md`

## Rules

### Rule 1

Agents MUST use `@ScaledMetric` (SwiftUI) or
`UIFontMetrics(forTextStyle:).scaledFont(for:)` (UIKit) for any custom
fixed-point spacing or sizing value that is visually tied to text (icon
size next to a label, padding around a text block), instead of a
hardcoded constant that ignores the user's text-size setting.

### Rule 2

Agents MUST use Dynamic Type text styles (`.font(.body)`,
`.font(.headline)` in SwiftUI; `UIFont.preferredFont(forTextStyle:)` in
UIKit) for body and label text, not a fixed pixel/point size
(`.font(.system(size: 14))`, `UIFont(name:size:)`), so text scales with
the user's preferred content size category.

### Rule 3

Agents MUST set `adjustsFontForContentSizeCategory = true` on any UIKit
`UILabel`/`UIButton`/`UITextField` configured with
`UIFont.preferredFont(forTextStyle:)`, so the control's font updates live
when the user changes their preferred text size in Settings.

### Rule 4

Agents SHOULD cap unconstrained `@ScaledMetric`/Dynamic Type growth with
`.dynamicTypeSize(...upTo:)` on the specific view where uncapped scaling
would break the layout, rather than disabling Dynamic Type support
entirely for that screen.

## Compliant Example

```swift
struct BadgeView: View {
    @ScaledMetric private var iconSize: CGFloat = 16

    var body: some View {
        Label("New", systemImage: "bell.fill")
            .font(.subheadline)
            .imageScale(.small)
            .frame(width: iconSize, height: iconSize)
    }
}
```
Icon size scales alongside the text via `@ScaledMetric`, and the label uses a Dynamic Type text style. (Rules 1, 2)

## Non-Compliant Example

```swift
struct BadgeView: View {
    var body: some View {
        Label("New", systemImage: "bell.fill")
            .font(.system(size: 12))
            .frame(width: 16, height: 16)
    }
}
```
Fixed point font size and hardcoded icon frame ignore the user's Dynamic Type setting entirely. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — ScaledMetric](https://developer.apple.com/documentation/swiftui/scaledmetric)
-   [Apple Developer — UIFontMetrics](https://developer.apple.com/documentation/uikit/uifontmetrics)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/dynamic-type-api.md --type knowledge`
Expected: `PASS: knowledge/accessibility/dynamic-type-api.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/dynamic-type-api.md
git commit -m "docs: add accessibility dynamic-type-api knowledge contract"
```

---

## Task 9: Knowledge Contract — `reduce-motion`

**Files:**
- Create: `knowledge/accessibility/reduce-motion.md`

- [ ] **Step 1: Create the file**

```markdown
# Reduce Motion

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.reduce-motion
type: knowledge
title: Reduce Motion
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines checking accessibilityReduceMotion (SwiftUI environment value) / UIAccessibility.isReduceMotionEnabled (UIKit) before playing large-scale motion animations, substituting a simpler alternative instead of disabling feedback entirely.
domain: Accessibility
tags:
  - accessibility
  - motion
  - reduce-motion
references:
  - https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion
  - https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled
depends_on: []
related:
  - knowledge.accessibility.reduce-transparency-increase-contrast
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent checks the user's Reduce
Motion setting (`@Environment(\.accessibilityReduceMotion)` in SwiftUI,
`UIAccessibility.isReduceMotionEnabled` in UIKit) and substitutes a
simpler alternative for large-scale motion, rather than either ignoring
the setting or removing state-communicating feedback entirely.

## Scope

### Included

-   Reading `accessibilityReduceMotion`/`isReduceMotionEnabled`
-   Substituting motion with a crossfade or static alternative
-   Reacting to the setting changing at runtime

### Excluded

-   Transparency/contrast settings — see `reduce-transparency-increase-contrast`

## Rules

### Rule 1

Agents MUST check `@Environment(\.accessibilityReduceMotion)` (SwiftUI)
or `UIAccessibility.isReduceMotionEnabled` (UIKit) before playing
large-scale motion — parallax effects, zoom/scale transitions,
auto-playing motion backgrounds — and substitute a simple crossfade or
static presentation when the setting is on.

### Rule 2

Agents MUST NOT remove state-communicating feedback entirely when Reduce
Motion is on — replace the motion-heavy animation with a reduced-motion
alternative (opacity fade, instant state change) rather than silence.

### Rule 3

Agents SHOULD let the SwiftUI environment value drive recomputation (it
updates automatically when the setting changes) or, in UIKit, observe
`UIAccessibility.reduceMotionStatusDidChangeNotification` so the app
reacts to the user toggling the setting live in Settings without
requiring a relaunch.

### Rule 4

Agents MUST NOT gate accessibility semantics (labels, values, traits)
behind the Reduce Motion check — it governs animation and motion only,
not VoiceOver content.

## Compliant Example

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

var body: some View {
    CardView()
        .transition(reduceMotion ? .opacity : .scale.combined(with: .opacity))
}
```
Falls back to a simple opacity transition when Reduce Motion is enabled. (Rule 1)

## Non-Compliant Example

```swift
var body: some View {
    CardView()
        .transition(.scale.combined(with: .opacity))
        .animation(.spring(response: 0.4, dampingFraction: 0.6), value: isVisible)
}
```
Large-scale spring/scale animation plays unconditionally regardless of the user's Reduce Motion setting. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityReduceMotion](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion)
-   [Apple Developer — UIAccessibility isReduceMotionEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/reduce-motion.md --type knowledge`
Expected: `PASS: knowledge/accessibility/reduce-motion.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/reduce-motion.md
git commit -m "docs: add accessibility reduce-motion knowledge contract"
```

---

## Task 10: Knowledge Contract — `reduce-transparency-increase-contrast`

**Files:**
- Create: `knowledge/accessibility/reduce-transparency-increase-contrast.md`

- [ ] **Step 1: Create the file**

```markdown
# Reduce Transparency and Increase Contrast

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.reduce-transparency-increase-contrast
type: knowledge
title: Reduce Transparency and Increase Contrast
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines checking accessibilityReduceTransparency/colorSchemeContrast (SwiftUI) and UIAccessibility.isReduceTransparencyEnabled/isDarkerSystemColorsEnabled (UIKit) to replace translucent materials and fixed low-contrast colors when these settings are on.
domain: Accessibility
tags:
  - accessibility
  - contrast
  - transparency
references:
  - https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency
  - https://developer.apple.com/documentation/uikit/uiaccessibility/isreducetransparencyenabled
  - https://developer.apple.com/documentation/uikit/uiaccessibility/isdarkersystemcolorsenabled
depends_on: []
related:
  - knowledge.accessibility.reduce-motion
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent responds to the Reduce
Transparency and Increase Contrast settings — replacing translucent
materials with opaque backgrounds and preferring system colors (which
auto-adjust) over fixed custom colors — implementing at the API level
the contrast requirement HIG's `accessibility.md` Rule 2 sets at the
design level.

## Scope

### Included

-   `accessibilityReduceTransparency`/`isReduceTransparencyEnabled`
-   `colorSchemeContrast`/`isDarkerSystemColorsEnabled`
-   Preferring system colors over fixed custom colors
-   Custom-drawn content (Core Graphics/Canvas) not adapting automatically

### Excluded

-   Motion/animation settings — see `reduce-motion`
-   The 4.5:1 contrast ratio requirement itself — owned by `human-interface-guidelines`'s `accessibility.md`

## Rules

### Rule 1

Agents MUST replace translucent materials (`.ultraThinMaterial`,
`.regularMaterial`, a blurred `UIVisualEffectView`) with an opaque
background when `accessibilityReduceTransparency` (SwiftUI) or
`UIAccessibility.isReduceTransparencyEnabled` (UIKit) is true.

### Rule 2

Agents MUST check `colorSchemeContrast == .increased` (SwiftUI) or
`UIAccessibility.isDarkerSystemColorsEnabled` (UIKit) and prefer
system-provided colors for text/borders/dividers, which automatically
increase contrast under this setting, rather than fixed custom colors
that don't respond to it.

### Rule 3

Agents SHOULD avoid adding bespoke contrast-boosting logic on top of
system colors/materials — system colors and materials already respond
to Reduce Transparency and Increase Contrast automatically, so custom
overrides are only needed for custom-drawn content.

### Rule 4

Agents MUST NOT ignore these settings for custom-drawn content (Core
Graphics, `Canvas`, `CAShapeLayer`) that doesn't automatically adapt —
read the settings directly and adjust fill/stroke colors and opacity in
the drawing code.

## Compliant Example

```swift
@Environment(\.accessibilityReduceTransparency) private var reduceTransparency

var body: some View {
    ToolbarContent()
        .background(reduceTransparency ? AnyShapeStyle(Color(.systemBackground)) : AnyShapeStyle(.ultraThinMaterial))
}
```
Falls back to an opaque system background instead of a translucent material. (Rule 1)

## Non-Compliant Example

```swift
var body: some View {
    ToolbarContent()
        .background(.ultraThinMaterial)
}
```
Translucent material is applied unconditionally, ignoring the user's Reduce Transparency setting. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityReduceTransparency](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency)
-   [Apple Developer — UIAccessibility isReduceTransparencyEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/isreducetransparencyenabled)
-   [Apple Developer — UIAccessibility isDarkerSystemColorsEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/isdarkersystemcolorsenabled)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/reduce-transparency-increase-contrast.md --type knowledge`
Expected: `PASS: knowledge/accessibility/reduce-transparency-increase-contrast.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/reduce-transparency-increase-contrast.md
git commit -m "docs: add accessibility reduce-transparency-increase-contrast knowledge contract"
```

---

## Task 11: Knowledge Contract — `full-keyboard-access-and-focus`

**Files:**
- Create: `knowledge/accessibility/full-keyboard-access-and-focus.md`

- [ ] **Step 1: Create the file**

```markdown
# Full Keyboard Access and Accessibility Focus

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.full-keyboard-access-and-focus
type: knowledge
title: Full Keyboard Access and Accessibility Focus
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines making custom controls reachable via .focusable() and UIFocusEnvironment for Full Keyboard Access, and moving VoiceOver focus programmatically with @AccessibilityFocusState / UIAccessibility.post(.screenChanged).
domain: Accessibility
tags:
  - accessibility
  - focus
  - keyboard
references:
  - https://developer.apple.com/documentation/swiftui/accessibilityfocusstate
  - https://developer.apple.com/documentation/uikit/uifocusenvironment
depends_on: []
related:
  - knowledge.accessibility.custom-accessibility-actions
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent makes custom controls
reachable by Full Keyboard Access / external keyboard navigation
(`.focusable()`, `UIFocusEnvironment`), and moves VoiceOver's focus
programmatically (`@AccessibilityFocusState`, UIKit's
`UIAccessibility.post(notification: .screenChanged, argument:)`) when new
content needs the user's immediate attention.

## Scope

### Included

-   `.focusable()` for custom interactive views
-   `@AccessibilityFocusState` for programmatic VoiceOver focus
-   `UIAccessibility.post(notification: .screenChanged, argument:)`
-   Not trapping focus with no way out

### Excluded

-   Providing an activation alternative for gestures — see `custom-accessibility-actions`

## Rules

### Rule 1

Agents MUST mark custom tappable views `.focusable()` (SwiftUI) or
ensure they participate in `UIFocusEnvironment` (UIKit) so Full Keyboard
Access and external-keyboard/switch-control users can reach them by
navigating focus, not only by touch.

### Rule 2

Agents MUST move VoiceOver focus programmatically — bind
`@AccessibilityFocusState` to `true` on the relevant element, or in
UIKit call `UIAccessibility.post(notification: .screenChanged,
argument: view)` — when content appears that the user needs to know
about immediately (a validation error, a newly presented sheet's title).

### Rule 3

Agents MUST NOT trap keyboard or VoiceOver focus inside a subview with
no reachable way out — every modal or focus-scoped view (a sheet, an
alert-like overlay) must expose a focusable/actionable dismiss control.

### Rule 4

Agents SHOULD set an explicit accessibility focus target when presenting
a sheet or full-screen cover so VoiceOver announces its content
immediately, instead of leaving focus on whatever was focused
underneath.

## Compliant Example

```swift
@AccessibilityFocusState private var errorFieldFocused: Bool

TextField("Email", text: $email)
    .accessibilityFocused($errorFieldFocused)

func submit() {
    if !isValidEmail(email) {
        errorFieldFocused = true
    }
}
```
VoiceOver focus moves directly to the invalid field on submission failure. (Rule 2)

## Non-Compliant Example

```swift
func submit() {
    if !isValidEmail(email) {
        showErrorBanner = true
    }
}
```
An error banner appears, but VoiceOver focus stays wherever it was — a VoiceOver user isn't told a validation error occurred unless they happen to swipe past the banner. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — AccessibilityFocusState](https://developer.apple.com/documentation/swiftui/accessibilityfocusstate)
-   [Apple Developer — UIFocusEnvironment](https://developer.apple.com/documentation/uikit/uifocusenvironment)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/full-keyboard-access-and-focus.md --type knowledge`
Expected: `PASS: knowledge/accessibility/full-keyboard-access-and-focus.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/full-keyboard-access-and-focus.md
git commit -m "docs: add accessibility full-keyboard-access-and-focus knowledge contract"
```

---

## Task 12: Knowledge Contract — `accessibility-hidden-decorative`

**Files:**
- Create: `knowledge/accessibility/accessibility-hidden-decorative.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility Hidden and Decorative Elements

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-hidden-decorative
type: knowledge
title: Accessibility Hidden and Decorative Elements
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of .accessibilityHidden(true) (SwiftUI) and isAccessibilityElement = false (UIKit) to exclude purely decorative or duplicate content from VoiceOver, without hiding elements that carry unique information.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - decorative
references:
  - https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:)
  - https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.accessibility.accessibility-labels
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent excludes purely decorative
or duplicate content from the accessibility tree with
`.accessibilityHidden(true)` (SwiftUI) or `isAccessibilityElement = false`
(UIKit), so VoiceOver skips visual noise without ever hiding an element
that carries unique information.

## Scope

### Included

-   Hiding purely decorative images/shapes/backgrounds
-   Hiding duplicate elements that repeat already-announced information
-   Hiding a decorative sublayer without hiding its interactive parent

### Excluded

-   Providing a label instead of hiding informative content — see `accessibility-labels`

## Rules

### Rule 1

Agents MUST hide purely decorative images, background shapes, and
illustrations with `.accessibilityHidden(true)` (SwiftUI) or
`isAccessibilityElement = false` (UIKit) so VoiceOver doesn't stop on
content that conveys no information.

### Rule 2

Agents MUST NOT hide an image or icon that conveys unique information
(an icon-only button, a status illustration with no accompanying text) —
give it a label per `accessibility-labels` instead of hiding it.

### Rule 3

Agents MUST hide only the decorative sublayer of a control, not the
interactive control itself, when a button's background image or icon is
decorative but the button as a whole must remain accessible — apply
`.accessibilityHidden(true)` (SwiftUI) or `isAccessibilityElement = false`
(UIKit) to the decorative image/icon subview, never to its tappable
parent (`Button`/`UIButton`/`UIControl`).

### Rule 4

Agents SHOULD hide a decorative element that visually duplicates
information already announced elsewhere — via `.accessibilityHidden(true)`
(SwiftUI) or `isAccessibilityElement = false` (UIKit) — such as a
disclosure chevron next to a row that already carries the
`.isButton`/navigation trait, to avoid a redundant, uninformative stop.

## Compliant Example

```swift
ZStack {
    Image("hero-background")
        .accessibilityHidden(true)
    Text("Welcome back")
        .font(.largeTitle)
}
```
The decorative background image is hidden; the informative title text remains. (Rule 1)

## Non-Compliant Example

```swift
Button {
    openDetail()
} label: {
    HStack {
        Text(item.title)
        Image(systemName: "chevron.right")
    }
}
.accessibilityHidden(true)
```
Hiding the entire button (including its title text) instead of just the decorative chevron makes the whole row unreachable by VoiceOver. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityHidden(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:))
-   [Apple Developer — UIAccessibility isAccessibilityElement](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/accessibility-hidden-decorative.md --type knowledge`
Expected: `PASS: knowledge/accessibility/accessibility-hidden-decorative.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/accessibility-hidden-decorative.md
git commit -m "docs: add accessibility accessibility-hidden-decorative knowledge contract"
```

---

## Task 13: Knowledge Contract — `accessibility-audits-testing`

**Files:**
- Create: `knowledge/accessibility/accessibility-audits-testing.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility Audits and Testing

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-audits-testing
type: knowledge
title: Accessibility Audits and Testing
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of Xcode's Accessibility Inspector and XCTest's performAccessibilityAudit() to catch missing labels, low contrast, and undersized hit targets automatically, alongside required manual VoiceOver verification.
domain: Accessibility
tags:
  - accessibility
  - testing
  - audits
references:
  - https://developer.apple.com/documentation/xctest/xcuiapplication/performaccessibilityaudit(_:issuehandler:)
  - https://developer.apple.com/documentation/xctest/xctaccessibilityaudittype
depends_on: []
related: []
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent verifies accessibility
implementation using Xcode's Accessibility Inspector and XCTest's
`performAccessibilityAudit()`, and why automated audits alone are
insufficient — reading order and gesture-alternative correctness still
require a manual VoiceOver walkthrough.

## Scope

### Included

-   `XCUIApplication().performAccessibilityAudit()` in UI tests
-   `XCTAccessibilityAuditType` scoping
-   Xcode's Accessibility Inspector for manual inspection
-   Limits of automated audits

### Excluded

-   General XCTest/Swift Testing/UI-testing conventions beyond accessibility audits — owned by the future `testing` domain

## Rules

### Rule 1

Agents MUST call `app.performAccessibilityAudit()` in UI test suites for
primary/representative screens, so missing labels, insufficient
contrast, and undersized hit targets are caught automatically in CI
rather than only by manual review.

### Rule 2

Agents MUST inspect an audit failure with Xcode's Accessibility
Inspector before dismissing it as a false positive — the inspector shows
exactly which element and property triggered the issue.

### Rule 3

Agents SHOULD scope audits with `XCTAccessibilityAuditType` (e.g.
excluding a specific category that's a known, accepted exception for one
screen) rather than disabling `performAccessibilityAudit()` entirely
when one category proves noisy for that screen.

### Rule 4

Agents MUST NOT treat a passing automated audit as sufficient
verification on its own — `performAccessibilityAudit()` does not check
VoiceOver reading order or whether gesture-only interactions have a
custom-action alternative; a manual VoiceOver walkthrough is still
required for those.

## Compliant Example

```swift
func testProfileScreenAccessibility() throws {
    let app = XCUIApplication()
    app.launch()
    app.buttons["Profile"].tap()

    try app.performAccessibilityAudit()
}
```
Automated audit runs against the Profile screen as part of the UI test suite. (Rule 1)

## Non-Compliant Example

```swift
func testProfileScreenLoads() throws {
    let app = XCUIApplication()
    app.launch()
    app.buttons["Profile"].tap()

    XCTAssertTrue(app.staticTexts["Profile"].exists)
}
```
UI test verifies the screen loads but never runs an accessibility audit, so missing labels or low-contrast issues on this screen go undetected until manual review, if ever. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — performAccessibilityAudit(_:issuehandler:)](https://developer.apple.com/documentation/xctest/xcuiapplication/performaccessibilityaudit(_:issuehandler:))
-   [Apple Developer — XCTAccessibilityAuditType](https://developer.apple.com/documentation/xctest/xctaccessibilityaudittype)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/accessibility/accessibility-audits-testing.md --type knowledge`
Expected: `PASS: knowledge/accessibility/accessibility-audits-testing.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/accessibility/accessibility-audits-testing.md
git commit -m "docs: add accessibility accessibility-audits-testing knowledge contract"
```

---

## Task 14: Native Skill — `skills/accessibility/SKILL.md`

**Files:**
- Create: `skills/accessibility/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: accessibility
description: Route Accessibility API implementation tasks to the correct Knowledge Contracts — accessibility labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion, Reduce Transparency/Increase Contrast, Full Keyboard Access and accessibility focus, hidden/decorative elements, and accessibility audits. Use when writing or reviewing VoiceOver support, custom-control accessibility, Dynamic Type handling, or accessibility test coverage in SwiftUI or UIKit. This is API-implementation guidance, not visual design — for the underlying design requirement (contrast ratio, text-scaling requirement, color-alone prohibition), see human-interface-guidelines. Triggers on VoiceOver, accessibilityLabel, accessibilityTraits, accessibilityValue, accessibilityHint, accessibilityAction, UIAccessibilityCustomAction, accessibilityElement, isAccessibilityElement, accessibilitySortPriority, Dynamic Type, ScaledMetric, UIFontMetrics, Reduce Motion, Reduce Transparency, Increase Contrast, Full Keyboard Access, AccessibilityFocusState, accessibilityHidden, performAccessibilityAudit, Accessibility Inspector.
id: skill.accessibility.foundations
title: Accessibility — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Accessibility
routes: [knowledge.accessibility.accessibility-labels, knowledge.accessibility.accessibility-traits, knowledge.accessibility.accessibility-value-and-hint, knowledge.accessibility.custom-accessibility-actions, knowledge.accessibility.accessibility-element-grouping, knowledge.accessibility.voiceover-navigation-order, knowledge.accessibility.dynamic-type-api, knowledge.accessibility.reduce-motion, knowledge.accessibility.reduce-transparency-increase-contrast, knowledge.accessibility.full-keyboard-access-and-focus, knowledge.accessibility.accessibility-hidden-decorative, knowledge.accessibility.accessibility-audits-testing]
related:
  - skill.human-interface-guidelines.foundations
  - skill.swiftui.foundations
last_updated: 2026-08-01
---

# Accessibility — Foundations Skill

## Purpose

Route Accessibility API implementation tasks to the minimum required
Accessibility Knowledge Contracts, across both SwiftUI and UIKit.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/accessibility/.

-   Labeling & description -> accessibility-labels.md, accessibility-traits.md, accessibility-value-and-hint.md
-   Interaction -> custom-accessibility-actions.md, full-keyboard-access-and-focus.md
-   Structure & navigation -> accessibility-element-grouping.md, voiceover-navigation-order.md, accessibility-hidden-decorative.md
-   User preferences -> dynamic-type-api.md, reduce-motion.md, reduce-transparency-increase-contrast.md
-   Verification -> accessibility-audits-testing.md

Never load more than the contracts relevant to the specific question.
For the underlying design requirement (why a 4.5:1 contrast ratio, why
text must scale to 200%, why color can't be the only differentiator),
route to `skill.human-interface-guidelines.foundations` instead. For
SwiftUI view/state/navigation questions unrelated to accessibility,
route to `skill.swiftui.foundations` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/accessibility/ — do not guess or fall back to
general knowledge. Design-level accessibility guidance (owned by
`human-interface-guidelines`) and general XCTest/Swift Testing/UI-testing
conventions beyond accessibility audits (owned by a future `testing`
domain) are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/accessibility/SKILL.md --type skill`
Expected: `PASS: skills/accessibility/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/accessibility/SKILL.md
git commit -m "feat: add accessibility native skill"
```

---

## Task 15: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`swiftui` row (the row containing `skills/swiftui/SKILL.md`):

```markdown
| VoiceOver, accessibilityLabel, accessibilityTraits, accessibilityValue, accessibilityHint, accessibilityAction, UIAccessibilityCustomAction, accessibilityElement, isAccessibilityElement, accessibilitySortPriority, Dynamic Type, ScaledMetric, UIFontMetrics, Reduce Motion, Reduce Transparency, Increase Contrast, Full Keyboard Access, AccessibilityFocusState, accessibilityHidden, performAccessibilityAudit, Accessibility Inspector | skills/accessibility/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `6` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui, accessibility)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add accessibility to skills index"
```

---

## Task 16: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `accessibility` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| Accessibility | accessibility | Accessibility APIs and UX | Accessibility API usage and accessible UX requirements |
```

Replace with:

```markdown
| Accessibility | accessibility | SwiftUI + UIKit accessibility API implementation: labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits. Design-level accessibility guidance owned by human-interface-guidelines — see Cross-Domain Notes. | SwiftUI + UIKit accessibility API implementation, VoiceOver/Dynamic Type/reduce-motion support, and accessibility audit conventions |
```

- [ ] **Step 2: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits).
```

- [ ] **Step 3: Resolve the existing `human-interface-guidelines` ↔ `accessibility` Cross-Domain Notes entry**

Find this exact line:

```markdown
- `human-interface-guidelines` (`accessibility` Foundations topic) and the future `accessibility` domain (Tier 1, unbuilt) overlap: HIG's angle is design guidance (Dynamic Type, contrast, VoiceOver-friendly layout), the dedicated domain's angle is API implementation. Boundary not yet resolved — decide when `accessibility` is built.
```

Replace with:

```markdown
- `human-interface-guidelines` (`accessibility` Foundations topic) and `accessibility` overlap: HIG's angle is design guidance (Dynamic Type requirement, contrast ratio, not conveying state by color alone, gesture alternatives — the *what* and *why*), `accessibility`'s angle is API implementation (the *how* — `accessibilityLabel`, `accessibilityTraits`, `@ScaledMetric`, `accessibilityReduceMotion`, etc.). Resolved via angle-split, the same pattern as the `swiftui` vs. `human-interface-guidelines` layout overlap.
```

- [ ] **Step 4: Add a new Cross-Domain Notes entry for `accessibility` ↔ future `testing`**

Find this exact line (the last bullet in `## Cross-Domain Notes`):

```markdown
- `app-store-review-guidelines` (`privacy-manifest`/`privacy-nutrition-label` topics) and the future `privacy` domain (Tier 2, unbuilt) overlap: this domain's angle is review consequence (submission gets rejected if the manifest/label is missing or inaccurate), the future `privacy` domain's angle is correct implementation (how to write the manifest and disclosures correctly). Boundary not yet resolved — decide when `privacy` is built.
```

Replace with (adds a new bullet after it):

```markdown
- `app-store-review-guidelines` (`privacy-manifest`/`privacy-nutrition-label` topics) and the future `privacy` domain (Tier 2, unbuilt) overlap: this domain's angle is review consequence (submission gets rejected if the manifest/label is missing or inaccurate), the future `privacy` domain's angle is correct implementation (how to write the manifest and disclosures correctly). Boundary not yet resolved — decide when `privacy` is built.
- `accessibility` (`accessibility-audits-testing` topic) and the future `testing` domain (Tier 2, unbuilt) overlap: this domain's angle is accessibility-specific audit APIs (`performAccessibilityAudit`, Accessibility Inspector), `testing`'s future angle is general XCTest/Swift Testing/UI-testing conventions. Boundary not yet resolved — decide when `testing` is built.
```

- [ ] **Step 5: Validate manually**

Run: `grep -c "accessibility" docs/architecture/domain-map.md`
Expected: a number greater than 3 (the file already mentions "accessibility" 3 times before this task; the updated row, Completed line, resolved Cross-Domain Notes entry, and new Cross-Domain Notes entry push the count well above that baseline)

- [ ] **Step 6: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: mark accessibility v1 complete, resolve HIG cross-domain note, add testing cross-domain note"
```

---

## Task 17: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `swiftui` bullet, immediately before the `Full routing tables:` line):

```markdown
- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`

- **`accessibility`** — Routes Accessibility API implementation tasks (labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion/Transparency/Increase Contrast, Full Keyboard Access, hidden/decorative elements, accessibility audits) to Accessibility Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this icon-only button has no VoiceOver label"` → `accessibility-labels.md`
  Example: `"swipe-to-delete row needs a VoiceOver alternative"` → `custom-accessibility-actions.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a new What's New line**

Find this exact line (the first/topmost line in `## What's New`):

```markdown
- 2026-08-01 — Added `swiftui` Skill (Views: composition/identity/modifier order; Navigation: NavigationStack/NavigationSplitView; Layout: stacks/safe-area/lazy-grids/GeometryReader; State: @State/@Binding/@Observable/@Environment) — 12 Knowledge Contracts.
```

Replace with (adds a new topmost line before it):

```markdown
- 2026-08-01 — Added `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contracts. Resolves the human-interface-guidelines and swiftui accessibility forward-references.
- 2026-08-01 — Added `swiftui` Skill (Views: composition/identity/modifier order; Navigation: NavigationStack/NavigationSplitView; Layout: stacks/safe-area/lazy-grids/GeometryReader; State: @State/@Binding/@Observable/@Environment) — 12 Knowledge Contracts.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "accessibility" README.md`
Expected: a number greater than 3 (the file already mentions "accessibility" 3 times before this task, in the `authentication` and `human-interface-guidelines` Skills bullets and the HIG What's New line — the new `accessibility` Skills bullet and What's New line push the count well above that baseline)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add accessibility to README Skills + What's New"
```

---

## Task 18: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/accessibility.md --type reference
python3 scripts/validate_artifact.py skills/accessibility/SKILL.md --type skill
for f in knowledge/accessibility/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
```
Expected: `PASS` for all 14 files.

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 4: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 17 prior tasks committed).

- [ ] **Step 5: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire `accessibility` domain (all
14 new files plus the 3 modified docs) to check cross-file consistency:
every `related:` KC id resolves to a real file (including the
cross-domain `knowledge.human-interface-guidelines.accessibility`
references), the Skill's `routes:` list matches exactly the 12 KC ids,
the Reference's "Used By" list matches exactly the 12 KC files, layer
order (References → Knowledge → Skills) is respected, the
`human-interface-guidelines` Cross-Domain Notes entry now reads as
resolved rather than "not yet resolved", and each commit is one artifact
per the established history pattern.
