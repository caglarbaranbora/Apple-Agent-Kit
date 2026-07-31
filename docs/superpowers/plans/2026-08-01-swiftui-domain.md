# SwiftUI Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `swiftui` domain (1 Reference, 12 Knowledge Contracts, 1 native Skill) covering Views/Navigation/Layout/State-management implementation conventions at iOS 17+, per `docs/superpowers/specs/2026-08-01-swiftui-domain-design.md`.

**Architecture:** Mirrors the `app-store-review-guidelines` domain exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/swiftui.md`

**Files:**
- Create: `references/apple/swiftui.md`

- [ ] **Step 1: Create the file**

```markdown
# SwiftUI

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/swiftui

## Purpose

Reference index for Apple's SwiftUI framework documentation,
implementation-conventions scope (Views, Navigation, Layout, State
management), targeting iOS 17+ APIs. Visual/UX design guidance for what
a screen should look like is owned by `human-interface-guidelines`, not
this domain — see docs/architecture/domain-map.md Cross-Domain Notes.
Animation, gestures, previews, and custom `Layout` protocol
conformances are out of scope for this pass.

## Primary Topics

- View composition and ViewBuilder
- View identity (ForEach/List, Identifiable)
- Modifier order and view wrapping
- NavigationStack and NavigationPath
- NavigationSplitView
- Stacks and spacing (VStack/HStack/ZStack)
- Safe area (safeAreaInset, ignoresSafeArea)
- Lazy grids and lazy stacks
- GeometryReader
- State and Binding
- The Observable macro
- Environment values

## Used By

- knowledge/swiftui/view-composition.md ([[knowledge/swiftui/view-composition]])
- knowledge/swiftui/view-identity.md ([[knowledge/swiftui/view-identity]])
- knowledge/swiftui/modifier-order.md ([[knowledge/swiftui/modifier-order]])
- knowledge/swiftui/navigation-stack.md ([[knowledge/swiftui/navigation-stack]])
- knowledge/swiftui/navigation-split-view.md ([[knowledge/swiftui/navigation-split-view]])
- knowledge/swiftui/stacks-and-spacing.md ([[knowledge/swiftui/stacks-and-spacing]])
- knowledge/swiftui/safe-area.md ([[knowledge/swiftui/safe-area]])
- knowledge/swiftui/lazy-grids.md ([[knowledge/swiftui/lazy-grids]])
- knowledge/swiftui/geometry-reader-anti-pattern.md ([[knowledge/swiftui/geometry-reader-anti-pattern]])
- knowledge/swiftui/state-and-binding.md ([[knowledge/swiftui/state-and-binding]])
- knowledge/swiftui/observable-macro.md ([[knowledge/swiftui/observable-macro]])
- knowledge/swiftui/environment-values.md ([[knowledge/swiftui/environment-values]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/swiftui.md --type reference`
Expected: `PASS: references/apple/swiftui.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/swiftui.md
git commit -m "docs: add swiftui reference index"
```

---

## Task 2: Knowledge Contract — `view-composition`

**Files:**
- Create: `knowledge/swiftui/view-composition.md`

- [ ] **Step 1: Create the file**

```markdown
# View Composition

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.view-composition
type: knowledge
title: View Composition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to break SwiftUI UI into small, single-responsibility views using ViewBuilder and extracted view types instead of monolithic body implementations.
domain: SwiftUI
tags:
  - swiftui
  - views
  - composition
references:
  - https://developer.apple.com/documentation/swiftui/view
depends_on: []
related:
  - knowledge.swiftui.view-identity
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent structures SwiftUI view
code: extracting focused subviews, keeping `body` declarative, and
choosing between computed properties, `@ViewBuilder` helpers, and
extracted view structs.

## Scope

### Included

-   When to extract a subview vs. keep inline
-   `@ViewBuilder` usage for conditional view-returning helpers
-   Keeping `body` free of non-trivial logic
-   Computed property vs. extracted `View` struct trade-off

### Excluded

-   Stable identity for extracted/repeated views in collections — see `view-identity`
-   Order of modifiers applied to a composed view — see `modifier-order`

## Rules

### Rule 1

Agents MUST extract a subview (or `@ViewBuilder` helper) when `body`
mixes multiple independent concerns (e.g., header + list + footer)
instead of writing one large `body`.

### Rule 2

Agents MUST NOT place non-trivial business logic (parsing, formatting
chains, network calls) inside `body` — compute values in properties or
methods outside `body`, keeping `body` declarative.

### Rule 3

Agents SHOULD use `@ViewBuilder` for helper functions or computed
properties that conditionally return different view content, instead of
type-erasing with `AnyView` by default.

### Rule 4

Agents SHOULD extract a private `View` struct (not a computed property)
when the subview needs its own `@State` or is reused across multiple
parents — a computed property recomputes on every access and cannot
hold state.

## Compliant Example

```swift
struct ProfileScreen: View {
    let profile: Profile

    var body: some View {
        VStack {
            ProfileHeader(profile: profile)
            ProfileDetailsList(profile: profile)
        }
    }
}

private struct ProfileHeader: View {
    let profile: Profile
    var body: some View {
        Text(profile.name).font(.title)
    }
}
```
Small, single-responsibility views composed together. (Rules 1, 4)

## Non-Compliant Example

```swift
struct ProfileScreen: View {
    let profile: Profile
    var body: some View {
        VStack {
            Text(profile.name).font(.title)
            Text(profile.bio.trimmingCharacters(in: .whitespaces).uppercased())
            ForEach(profile.posts) { post in
                // dozens more lines of unrelated list-rendering logic
                Text(post.title)
            }
        }
    }
}
```
One monolithic `body` mixing header formatting logic and list rendering. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — View](https://developer.apple.com/documentation/swiftui/view)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/view-composition.md --type knowledge`
Expected: `PASS: knowledge/swiftui/view-composition.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/view-composition.md
git commit -m "docs: add swiftui view-composition knowledge contract"
```

---

## Task 3: Knowledge Contract — `view-identity`

**Files:**
- Create: `knowledge/swiftui/view-identity.md`

- [ ] **Step 1: Create the file**

```markdown
# View Identity

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.view-identity
type: knowledge
title: View Identity
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to give ForEach/List content stable, correct identity to avoid state loss, animation glitches, and wrong-row bugs after data mutation.
domain: SwiftUI
tags:
  - swiftui
  - views
  - identity
references:
  - https://developer.apple.com/documentation/swiftui/foreach
  - https://developer.apple.com/documentation/swift/identifiable
depends_on: []
related:
  - knowledge.swiftui.view-composition
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent assigns identity to
`ForEach`/`List` content and understands SwiftUI's structural identity
rules, so that state and animations stay attached to the correct
logical item as data changes.

## Scope

### Included

-   Stable `id`/`Identifiable` requirement for `ForEach`/`List`
-   Index-based identity pitfalls for mutable collections
-   Structural identity (`if`/`switch` branches) and the `.id()` modifier

### Excluded

-   General view decomposition — see `view-composition`
-   `@State` ownership rules themselves — see `state-and-binding`

## Rules

### Rule 1

Agents MUST supply a stable, unique identity for `ForEach`/`List`
content — via `Identifiable` conformance or an explicit `id:` parameter
— that stays attached to the same logical item across re-renders.

### Rule 2

Agents MUST NOT use array index as the identity (`id: \.self` on
`.indices`) for a collection whose order or membership can change
(insert/delete/reorder) — this attaches a row's state/animation to the
wrong item after mutation.

### Rule 3

Agents MUST NOT generate an id inline in `body` (e.g., `UUID()` created
during view evaluation) — this creates a new identity every render,
defeating diffing and causing state loss or flicker.

### Rule 4

Agents SHOULD use the `.id(_:)` modifier deliberately when the intent is
to force a view's identity to reset (e.g., clearing internal `@State`
when navigating to a different item), understanding that changing which
`if`/`switch` branch renders also creates a new identity and resets any
`@State` inside that branch.

## Compliant Example

```swift
struct Item: Identifiable {
    let id: UUID
    var title: String
}

ForEach(items) { item in
    ItemRow(item: item)
}
```
Stable `Identifiable` conformance keeps each row's identity attached to its item. (Rule 1)

## Non-Compliant Example

```swift
ForEach(items.indices, id: \.self) { index in
    ItemRow(item: items[index])
}
```
Index identity: deleting item 0 makes every subsequent row's identity shift, losing per-row state and mis-animating the delete. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — ForEach](https://developer.apple.com/documentation/swiftui/foreach)
-   [Apple Developer — Identifiable](https://developer.apple.com/documentation/swift/identifiable)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/view-identity.md --type knowledge`
Expected: `PASS: knowledge/swiftui/view-identity.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/view-identity.md
git commit -m "docs: add swiftui view-identity knowledge contract"
```

---

## Task 4: Knowledge Contract — `modifier-order`

**Files:**
- Create: `knowledge/swiftui/modifier-order.md`

- [ ] **Step 1: Create the file**

```markdown
# Modifier Order

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.modifier-order
type: knowledge
title: Modifier Order
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines that SwiftUI view modifiers apply in the order written, each wrapping the view in a new view, and that order changes the rendered result.
domain: SwiftUI
tags:
  - swiftui
  - views
  - modifiers
references:
  - https://developer.apple.com/documentation/swiftui/viewmodifier
depends_on: []
related:
  - knowledge.swiftui.view-composition
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent orders chained view
modifiers (`.padding()`, `.background()`, `.frame()`, `.clipShape()`,
etc.) so the rendered result matches intent, since each modifier wraps
the view rather than mutating it in place.

## Scope

### Included

-   `.padding()` vs `.background()` ordering
-   `.frame()` vs `.background()` ordering
-   Non-commutativity of sizing/appearance modifiers
-   `.clipShape()`/`.overlay()` ordering for matching borders

### Excluded

-   Which stack/alignment to use — see `stacks-and-spacing`
-   View decomposition itself — see `view-composition`

## Rules

### Rule 1

Agents MUST apply `.background()` after `.padding()` when the
background is meant to cover the padded area — `.background()` only
fills the view's bounds at the point it's applied in the chain.

### Rule 2

Agents MUST apply `.frame()` before `.background()` when the background
should fill the frame's size — a `.background()` applied before
`.frame()` only fills the pre-frame size.

### Rule 3

Agents MUST NOT assume modifier order is commutative — `.padding()`
followed by `.frame(width:)` adds padding inside a fixed frame, while
`.frame(width:)` followed by `.padding()` adds padding outside the
frame, growing the total size.

### Rule 4

Agents SHOULD apply `.clipShape()` after `.frame()` and before
`.overlay()` when adding a border stroke that must match the clip
shape's edge.

## Compliant Example

```swift
Text("Hello")
    .padding()
    .background(Color.blue)
    .clipShape(RoundedRectangle(cornerRadius: 8))
```
Padding is applied first, so the background fills the padded area. (Rule 1)

## Non-Compliant Example

```swift
Text("Hello")
    .background(Color.blue)
    .padding()
```
Background applied before padding only colors the text's own bounds; the padding area around it stays uncolored. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — ViewModifier](https://developer.apple.com/documentation/swiftui/viewmodifier)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/modifier-order.md --type knowledge`
Expected: `PASS: knowledge/swiftui/modifier-order.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/modifier-order.md
git commit -m "docs: add swiftui modifier-order knowledge contract"
```

---

## Task 5: Knowledge Contract — `navigation-stack`

**Files:**
- Create: `knowledge/swiftui/navigation-stack.md`

- [ ] **Step 1: Create the file**

```markdown
# Navigation Stack

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.navigation-stack
type: knowledge
title: Navigation Stack
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the use of NavigationStack and NavigationPath for stack-based push/pop navigation, including programmatic and deep-link navigation.
domain: SwiftUI
tags:
  - swiftui
  - navigation
references:
  - https://developer.apple.com/documentation/swiftui/navigationstack
  - https://developer.apple.com/documentation/swiftui/navigationpath
depends_on: []
related:
  - knowledge.swiftui.navigation-split-view
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent implements stack-based
(push/pop) navigation in SwiftUI using `NavigationStack` and
`NavigationPath`, including programmatic and deep-link navigation.

## Scope

### Included

-   `NavigationStack` as the stack-based navigation container
-   `NavigationPath`-driven programmatic navigation
-   `.navigationDestination(for:)` type-keyed destinations
-   Nesting restrictions

### Excluded

-   Multi-column sidebar/detail navigation — see `navigation-split-view`
-   Legacy `NavigationView` migration guidance — out of scope for v1

## Rules

### Rule 1

Agents MUST use `NavigationStack` (not the deprecated `NavigationView`)
as the root container for stack-based push/pop navigation.

### Rule 2

Agents MUST drive programmatic navigation through a bound
`NavigationPath` (or a typed `[Value]` path) rather than wiring manual
boolean `isActive` flags per destination.

### Rule 3

Agents MUST declare destinations with `.navigationDestination(for:)`
keyed by the pushed data type, not by manually toggling per-destination
view state.

### Rule 4

Agents MUST NOT nest a `NavigationStack` inside another
`NavigationStack` within the same navigation hierarchy — nested stacks
produce ambiguous back-stack behavior.

### Rule 5

Agents SHOULD keep the `NavigationPath` state at the point in the view
hierarchy that owns the navigation flow (e.g., a `@State` on the
stack's root), so a deep link can push directly by appending to the
path.

## Compliant Example

```swift
@State private var path = NavigationPath()

NavigationStack(path: $path) {
    RootView()
        .navigationDestination(for: Item.self) { item in
            DetailView(item: item)
        }
}
```
Programmatic push via `NavigationPath`, type-keyed destination. (Rules 2, 3)

## Non-Compliant Example

```swift
NavigationView {
    NavigationLink(destination: DetailView(), isActive: $showDetail) {
        EmptyView()
    }
}
```
Deprecated `NavigationView` with a manual `isActive` boolean per destination. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)
-   [Apple Developer — NavigationPath](https://developer.apple.com/documentation/swiftui/navigationpath)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/navigation-stack.md --type knowledge`
Expected: `PASS: knowledge/swiftui/navigation-stack.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/navigation-stack.md
git commit -m "docs: add swiftui navigation-stack knowledge contract"
```

---

## Task 6: Knowledge Contract — `navigation-split-view`

**Files:**
- Create: `knowledge/swiftui/navigation-split-view.md`

- [ ] **Step 1: Create the file**

```markdown
# Navigation Split View

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.navigation-split-view
type: knowledge
title: Navigation Split View
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the use of NavigationSplitView for adaptive multi-column sidebar/content/detail navigation.
domain: SwiftUI
tags:
  - swiftui
  - navigation
references:
  - https://developer.apple.com/documentation/swiftui/navigationsplitview
depends_on: []
related:
  - knowledge.swiftui.navigation-stack
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent implements adaptive
multi-column (sidebar/content/detail) navigation using
`NavigationSplitView`, and how it composes with `NavigationStack`.

## Scope

### Included

-   `NavigationSplitView` for sidebar/detail or sidebar/content/detail layouts
-   Selection-state binding across columns
-   Two-column vs three-column initializer choice
-   Composition with `NavigationStack` inside a column

### Excluded

-   Single-column push/pop navigation — see `navigation-stack`

## Rules

### Rule 1

Agents MUST use `NavigationSplitView` (not a manually built `HStack` of
columns) for sidebar–detail layouts that need to adapt between compact
and regular size classes.

### Rule 2

Agents MUST bind a single selection state to drive both the sidebar's
selected row and the detail column's content — not separate,
unsynchronized state per column.

### Rule 3

Agents MUST NOT use `NavigationSplitView` and `NavigationStack` as
siblings for the same navigational concern — nest a `NavigationStack`
inside the detail column only if that column itself needs push/pop
within the selected item.

### Rule 4

Agents SHOULD use the two-column initializer (`sidebar:detail:`) when
there is no distinct middle "content" list, and the three-column
initializer (`sidebar:content:detail:`) only when a genuine middle list
exists.

### Rule 5

Agents SHOULD rely on `NavigationSplitView`'s default adaptive/balanced
column behavior and only override width or style when the default does
not fit the design.

## Compliant Example

```swift
@State private var selection: Item?

NavigationSplitView {
    List(items, selection: $selection) { item in
        Text(item.title)
    }
} detail: {
    if let selection {
        DetailView(item: selection)
    } else {
        Text("Select an item")
    }
}
```
Single selection state drives both sidebar and detail. (Rule 2)

## Non-Compliant Example

```swift
HStack {
    SidebarView(onSelect: { selectedID = $0 })
    DetailView(id: detailID)
}
```
Hand-rolled columns with two unsynchronized selection variables and no adaptive collapsing on compact width. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/navigation-split-view.md --type knowledge`
Expected: `PASS: knowledge/swiftui/navigation-split-view.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/navigation-split-view.md
git commit -m "docs: add swiftui navigation-split-view knowledge contract"
```

---

## Task 7: Knowledge Contract — `stacks-and-spacing`

**Files:**
- Create: `knowledge/swiftui/stacks-and-spacing.md`

- [ ] **Step 1: Create the file**

```markdown
# Stacks and Spacing

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.stacks-and-spacing
type: knowledge
title: Stacks and Spacing
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of VStack/HStack/ZStack, Spacer, alignment, and the spacing parameter for arranging views — the code-implementation angle, distinct from human-interface-guidelines' visual-design angle on layout.
domain: SwiftUI
tags:
  - swiftui
  - layout
references:
  - https://developer.apple.com/documentation/swiftui/vstack
  - https://developer.apple.com/documentation/swiftui/hstack
  - https://developer.apple.com/documentation/swiftui/zstack
depends_on: []
related:
  - knowledge.swiftui.safe-area
  - knowledge.swiftui.lazy-grids
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent arranges views with
`VStack`/`HStack`/`ZStack`, `Spacer`, alignment, and the `spacing:`
parameter — the SwiftUI code-implementation angle. Whether a given
spacing/alignment choice is HIG-compliant is a separate, visual-design
question owned by `human-interface-guidelines`'s `layout.md` (see
docs/architecture/domain-map.md Cross-Domain Notes).

## Scope

### Included

-   Choosing the correct stack axis
-   `Spacer()` vs fixed-size gaps
-   Stack `alignment:` and `spacing:` parameters

### Excluded

-   Whether a layout is HIG-compliant (visual-design angle) — see `human-interface-guidelines`'s `layout.md`
-   Safe-area edge handling — see `safe-area`
-   Lazy/grid layout for large data sets — see `lazy-grids`

## Rules

### Rule 1

Agents MUST choose the stack axis (`VStack` for vertical, `HStack` for
horizontal) that matches the intended layout direction rather than
faking linear layout with a `ZStack` and manual offsets.

### Rule 2

Agents MUST use `Spacer()` (optionally with `minLength:`) to distribute
remaining space, not a hard-coded `Spacer().frame(height:)`-style
magic-number gap meant to push content.

### Rule 3

Agents MUST NOT use `Spacer(minLength: 0)` when the intent is a fixed
gap between two elements — use `.padding()` or a sized `Color.clear`
spacer for a deliberate fixed gap instead.

### Rule 4

Agents SHOULD set a stack's `alignment:` parameter explicitly when the
default (`.center`) doesn't match the design, instead of nesting extra
`HStack { content; Spacer() }` wrappers to fake leading alignment.

### Rule 5

Agents SHOULD use the stack initializer's `spacing:` parameter for
uniform gaps between all children rather than adding `.padding(.bottom:)`
to each child individually.

## Compliant Example

```swift
VStack(alignment: .leading, spacing: 12) {
    Text("Title")
    Text("Subtitle")
}
```
Explicit alignment and uniform spacing via the initializer. (Rules 4, 5)

## Non-Compliant Example

```swift
VStack {
    Text("Title")
    Spacer().frame(height: 12)
    Text("Subtitle")
}
```
A `Spacer` constrained to a fixed height is really just a magic-number gap; `.padding()` or `spacing:` expresses the same intent directly. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — VStack](https://developer.apple.com/documentation/swiftui/vstack)
-   [Apple Developer — HStack](https://developer.apple.com/documentation/swiftui/hstack)
-   [Apple Developer — ZStack](https://developer.apple.com/documentation/swiftui/zstack)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/stacks-and-spacing.md --type knowledge`
Expected: `PASS: knowledge/swiftui/stacks-and-spacing.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/stacks-and-spacing.md
git commit -m "docs: add swiftui stacks-and-spacing knowledge contract"
```

---

## Task 8: Knowledge Contract — `safe-area`

**Files:**
- Create: `knowledge/swiftui/safe-area.md`

- [ ] **Step 1: Create the file**

```markdown
# Safe Area

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.safe-area
type: knowledge
title: Safe Area
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of safeAreaInset for persistent chrome versus ignoresSafeArea for edge-to-edge content, and the risks of misapplying either.
domain: SwiftUI
tags:
  - swiftui
  - layout
  - safe-area
references:
  - https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:)
  - https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:)
depends_on: []
related:
  - knowledge.swiftui.stacks-and-spacing
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent handles the safe area:
using `.safeAreaInset(edge:)` for persistent UI chrome that should
reserve space, and `.ignoresSafeArea()` only for content meant to bleed
to the physical screen edge.

## Scope

### Included

-   `.safeAreaInset(edge:)` for chrome that reserves space
-   `.ignoresSafeArea()` scope and edge targeting
-   Risk of covering interactive controls or content

### Excluded

-   General stack/spacing layout — see `stacks-and-spacing`

## Rules

### Rule 1

Agents MUST use `.safeAreaInset(edge:)` to add persistent chrome (e.g.,
a bottom toolbar or input bar) that reserves space and pushes
scrollable content, rather than overlaying it with `.overlay()` and
manually guessed padding.

### Rule 2

Agents MUST use `.ignoresSafeArea()` only for content meant to extend to
the physical screen edge (backgrounds, full-bleed images/media).

### Rule 3

Agents MUST NOT apply `.ignoresSafeArea()` to interactive controls or
primary content that would then sit under the notch, Dynamic Island, or
home indicator.

### Rule 4

Agents MUST NOT apply `.ignoresSafeArea()` to an entire screen's root
view when only a background layer needs edge-to-edge extension — scope
it to the specific background view instead.

### Rule 5

Agents SHOULD specify the `edges:` parameter on `.ignoresSafeArea(edges:)`
(e.g., `.top`) rather than ignoring all edges when only one edge needs
to bleed.

## Compliant Example

```swift
ScrollView {
    content
}
.safeAreaInset(edge: .bottom) {
    InputBar()
}
```
`InputBar` reserves its own space; scroll content never renders underneath it. (Rule 1)

## Non-Compliant Example

```swift
ZStack(alignment: .bottom) {
    ScrollView { content }
    InputBar()
}
```
`InputBar` overlays the scroll content with no reserved space, obscuring the last row. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — safeAreaInset](https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:))
-   [Apple Developer — ignoresSafeArea](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/safe-area.md --type knowledge`
Expected: `PASS: knowledge/swiftui/safe-area.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/safe-area.md
git commit -m "docs: add swiftui safe-area knowledge contract"
```

---

## Task 9: Knowledge Contract — `lazy-grids`

**Files:**
- Create: `knowledge/swiftui/lazy-grids.md`

- [ ] **Step 1: Create the file**

```markdown
# Lazy Grids

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.lazy-grids
type: knowledge
title: Lazy Grids
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when to use LazyVGrid/LazyHGrid and LazyVStack/LazyHStack instead of eager stacks or List, for large or dynamic content inside a ScrollView.
domain: SwiftUI
tags:
  - swiftui
  - layout
  - performance
references:
  - https://developer.apple.com/documentation/swiftui/lazyvgrid
  - https://developer.apple.com/documentation/swiftui/lazyvstack
depends_on: []
related:
  - knowledge.swiftui.stacks-and-spacing
  - knowledge.swiftui.geometry-reader-anti-pattern
updated: 2026-08-01
```

## Intent

This contract defines when an AI coding agent must use lazy containers
(`LazyVStack`/`LazyHStack`, `LazyVGrid`/`LazyHGrid`) instead of eager
stacks or a `ScrollView`-wrapped `List`, for correctness and
performance with large or dynamic data.

## Scope

### Included

-   `LazyVStack`/`LazyHStack` vs `VStack`/`HStack` in a `ScrollView`
-   `LazyVGrid`/`LazyHGrid` with `GridItem` specs
-   `List` vs `ScrollView` + lazy stack trade-off
-   `GridItem` sizing strategies

### Excluded

-   Stack alignment/spacing fundamentals — see `stacks-and-spacing`

## Rules

### Rule 1

Agents MUST use `LazyVStack`/`LazyHStack` (not `VStack`/`HStack`) inside
a `ScrollView` when rendering a data-driven list of unbounded or large
size — non-lazy stacks instantiate every child view immediately.

### Rule 2

Agents MUST use `LazyVGrid`/`LazyHGrid` with `GridItem` column/row specs
for grid layouts of dynamic collections, rather than manually chunking
data into rows of `HStack`s inside a `VStack`.

### Rule 3

Agents MUST NOT wrap a `List` inside a `ScrollView` — `List` is already
scrollable, and nesting causes scroll-gesture conflicts.

### Rule 4

Agents SHOULD prefer `List` over `LazyVStack` in a `ScrollView` when
default list styling (swipe actions, section headers, platform chrome)
is acceptable — `List` already includes lazy loading.

### Rule 5

Agents SHOULD size `GridItem` with `.adaptive(minimum:)` for content
that should reflow its column count by available width, and
`.fixed(_:)`/`.flexible()` when a specific fixed or proportional column
count is required.

## Compliant Example

```swift
ScrollView {
    LazyVGrid(columns: [GridItem(.adaptive(minimum: 120))], spacing: 16) {
        ForEach(items) { item in
            ItemCell(item: item)
        }
    }
}
```
Lazy grid with adaptive columns for a dynamic collection. (Rules 2, 5)

## Non-Compliant Example

```swift
ScrollView {
    VStack {
        ForEach(items) { item in
            ItemCell(item: item)
        }
    }
}
```
Eager `VStack` inside `ScrollView` builds every row immediately, regardless of visibility. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid)
-   [Apple Developer — LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/lazy-grids.md --type knowledge`
Expected: `PASS: knowledge/swiftui/lazy-grids.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/lazy-grids.md
git commit -m "docs: add swiftui lazy-grids knowledge contract"
```

---

## Task 10: Knowledge Contract — `geometry-reader-anti-pattern`

**Files:**
- Create: `knowledge/swiftui/geometry-reader-anti-pattern.md`

- [ ] **Step 1: Create the file**

```markdown
# GeometryReader Anti-Pattern

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.geometry-reader-anti-pattern
type: knowledge
title: GeometryReader Anti-Pattern
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the pitfalls of GeometryReader's greedy size-filling behavior and when it should and should not be used in a SwiftUI layout tree.
domain: SwiftUI
tags:
  - swiftui
  - layout
  - performance
references:
  - https://developer.apple.com/documentation/swiftui/geometryreader
depends_on: []
related:
  - knowledge.swiftui.lazy-grids
updated: 2026-08-01
```

## Intent

This contract defines when an AI coding agent may use `GeometryReader`
and when it must avoid it, since `GeometryReader` always greedily fills
all available space and frequently breaks the intrinsic sizing of
siblings or parents.

## Scope

### Included

-   Why `GeometryReader` breaks intrinsic content sizing
-   Nesting `GeometryReader` inside stacks
-   Scoped alternatives (`.background()`/`.overlay()`, `.frame()`, `.aspectRatio()`)
-   Legitimate direct uses

### Excluded

-   Lazy loading of large data sets — see `lazy-grids`

## Rules

### Rule 1

Agents MUST NOT wrap a view in `GeometryReader` solely to read a size
for a computation unrelated to that view's own layout — `GeometryReader`
greedily fills all available space, which breaks the intrinsic sizing
of the view it wraps.

### Rule 2

Agents MUST NOT nest a `GeometryReader` inside a `VStack`/`HStack`
expecting it to size to its content — it expands to fill the stack's
available cross-axis space instead, distorting sibling layout.

### Rule 3

Agents SHOULD use `.frame(maxWidth:maxHeight:)`, `.aspectRatio()`, or a
size read scoped to `.background()`/`.overlay()` of an already-correctly
laid-out view when only a specific measured value is needed, rather
than placing a `GeometryReader` directly in the layout tree.

### Rule 4

Agents MAY use `GeometryReader` directly in the layout tree only when
the view genuinely needs to size or position itself relative to the
full available space it's given (e.g., a custom paginated carousel), and
the surrounding layout is designed to accommodate a greedy-filling
child.

## Compliant Example

```swift
Text("Title")
    .background(
        GeometryReader { proxy in
            Color.clear.preference(key: SizeKey.self, value: proxy.size)
        }
    )
```
`GeometryReader` scoped to `.background()` reads size without affecting `Text`'s own layout. (Rule 3)

## Non-Compliant Example

```swift
GeometryReader { proxy in
    VStack {
        Text("Title")
        Text("Subtitle")
    }
}
```
The `VStack` now stretches to `GeometryReader`'s full greedy size instead of hugging its content. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — GeometryReader](https://developer.apple.com/documentation/swiftui/geometryreader)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/geometry-reader-anti-pattern.md --type knowledge`
Expected: `PASS: knowledge/swiftui/geometry-reader-anti-pattern.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/geometry-reader-anti-pattern.md
git commit -m "docs: add swiftui geometry-reader-anti-pattern knowledge contract"
```

---

## Task 11: Knowledge Contract — `state-and-binding`

**Files:**
- Create: `knowledge/swiftui/state-and-binding.md`

- [ ] **Step 1: Create the file**

```markdown
# State and Binding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.state-and-binding
type: knowledge
title: State and Binding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct ownership of local view state with @State versus propagating a parent-owned value for read/write access to a child with @Binding.
domain: SwiftUI
tags:
  - swiftui
  - state
references:
  - https://developer.apple.com/documentation/swiftui/state
  - https://developer.apple.com/documentation/swiftui/binding
depends_on: []
related:
  - knowledge.swiftui.observable-macro
  - knowledge.swiftui.environment-values
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent chooses between `@State`
(local, view-owned, value-type data) and `@Binding` (read/write access
to a value owned by a parent), avoiding duplicated or unsynchronized
sources of truth.

## Scope

### Included

-   `@State` ownership rules
-   `@Binding` for child mutation of parent-owned values
-   Avoiding duplicated state
-   Mutating bindings only through the normal update cycle

### Excluded

-   Reference-type observable models — see `observable-macro`
-   Environment-injected shared state — see `environment-values`

## Rules

### Rule 1

Agents MUST mark local, view-owned, mutable value-type data with
`@State`, declared `private` since it belongs to that view instance
only.

### Rule 2

Agents MUST use `@Binding` (not a plain parameter plus callback pair,
and not a duplicated `@State`) when a child view needs to read and
mutate a value owned by a parent or ancestor.

### Rule 3

Agents MUST NOT declare `@State` for a value that is actually owned by a
parent and merely passed down for display — that creates two
independent sources of truth that drift out of sync.

### Rule 4

Agents MUST NOT mutate a `@Binding`'s wrapped value outside SwiftUI's
normal update cycle (e.g., during `init`) — mutate only through normal
event handlers such as button actions or `onChange`.

### Rule 5

Agents SHOULD initialize `@State` with a default value at declaration,
overriding via a custom `init` parameter only when the initial value
genuinely depends on injected data, treated as a one-time seed rather
than a live sync point with the caller.

## Compliant Example

```swift
struct ParentView: View {
    @State private var isOn = false
    var body: some View {
        ToggleRow(isOn: $isOn)
    }
}

struct ToggleRow: View {
    @Binding var isOn: Bool
    var body: some View {
        Toggle("Enabled", isOn: $isOn)
    }
}
```
`@State` owned by the parent, propagated for mutation via `@Binding`. (Rules 1, 2)

## Non-Compliant Example

```swift
struct ToggleRow: View {
    var isOn: Bool
    var body: some View {
        Toggle("Enabled", isOn: .constant(isOn))
    }
}
```
A plain `Bool` parameter wrapped in `.constant()` cannot propagate changes back to the parent. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — State](https://developer.apple.com/documentation/swiftui/state)
-   [Apple Developer — Binding](https://developer.apple.com/documentation/swiftui/binding)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/state-and-binding.md --type knowledge`
Expected: `PASS: knowledge/swiftui/state-and-binding.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/state-and-binding.md
git commit -m "docs: add swiftui state-and-binding knowledge contract"
```

---

## Task 12: Knowledge Contract — `observable-macro`

**Files:**
- Create: `knowledge/swiftui/observable-macro.md`

- [ ] **Step 1: Create the file**

```markdown
# Observable Macro

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.observable-macro
type: knowledge
title: Observable Macro
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of the @Observable macro (iOS 17+) for reference-type model objects, as the default replacement for ObservableObject/@Published in new code.
domain: SwiftUI
tags:
  - swiftui
  - state
  - observation
references:
  - https://developer.apple.com/documentation/observation/observable()
  - https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app
depends_on: []
related:
  - knowledge.swiftui.state-and-binding
  - knowledge.swiftui.environment-values
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent models reference-type
(class) app state for SwiftUI observation, using the `@Observable`
macro (iOS 17+) as the default for new code instead of
`ObservableObject`/`@Published`.

## Scope

### Included

-   `@Observable` as the default for new iOS 17+ reference-type models
-   Ownership with `@State` instead of `@StateObject`
-   Passing an `@Observable` model to children without a property wrapper
-   Not mixing `@Observable` and `ObservableObject` on one type

### Excluded

-   `@State`/`@Binding` for local value-type state — see `state-and-binding`
-   `@Environment` injection of an `@Observable` model — see `environment-values`

## Rules

### Rule 1

Agents MUST mark reference-type (class) model objects that a SwiftUI
view observes with the `@Observable` macro rather than conforming to
`ObservableObject` with individual `@Published` properties, for new code
targeting iOS 17+.

### Rule 2

Agents MUST hold an `@Observable` model that a view creates and owns
with `@State` (not `@StateObject`, which is specific to
`ObservableObject`) — `@State` correctly manages the lifetime of
`@Observable` reference types.

### Rule 3

Agents MUST pass an `@Observable` model down to child views as a plain
stored property (no property wrapper needed) when the child only reads
or observes it — `@Observable`'s tracking works automatically via
property access inside `body`.

### Rule 4

Agents MUST NOT mix `@Observable` and `ObservableObject`/`@Published` on
the same type — pick one observation mechanism per type.

### Rule 5

Agents SHOULD use `@Environment` (not a manually threaded stored
property through every intermediate view) to inject an `@Observable`
model that many descendant views need, avoiding prop-drilling.

## Compliant Example

```swift
@Observable
final class CartModel {
    var items: [Item] = []
}

struct CartView: View {
    @State private var model = CartModel()
    var body: some View {
        CartList(model: model)
    }
}

struct CartList: View {
    var model: CartModel
    var body: some View {
        List(model.items) { item in Text(item.name) }
    }
}
```
`@Observable` model owned via `@State`, passed to a child as a plain property. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
final class CartModel: ObservableObject {
    @Published var items: [Item] = []
}

struct CartView: View {
    @StateObject private var model = CartModel()
    var body: some View {
        CartList(model: model)
    }
}

struct CartList: View {
    @ObservedObject var model: CartModel
    var body: some View {
        List(model.items) { item in Text(item.name) }
    }
}
```
Legacy `ObservableObject`/`@Published`/`@StateObject`/`@ObservedObject` pattern for new iOS 17+ code, where `@Observable` is the recommended default. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Observable()](https://developer.apple.com/documentation/observation/observable())
-   [Apple Developer — Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/observable-macro.md --type knowledge`
Expected: `PASS: knowledge/swiftui/observable-macro.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/observable-macro.md
git commit -m "docs: add swiftui observable-macro knowledge contract"
```

---

## Task 13: Knowledge Contract — `environment-values`

**Files:**
- Create: `knowledge/swiftui/environment-values.md`

- [ ] **Step 1: Create the file**

```markdown
# Environment Values

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.environment-values
type: knowledge
title: Environment Values
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of @Environment for dependency injection of shared app state and custom environment values, instead of manually threading dependencies through view initializers.
domain: SwiftUI
tags:
  - swiftui
  - state
  - environment
references:
  - https://developer.apple.com/documentation/swiftui/environment
  - https://developer.apple.com/documentation/swiftui/environmentkey
depends_on: []
related:
  - knowledge.swiftui.observable-macro
  - knowledge.swiftui.state-and-binding
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent injects shared or
cross-cutting values (custom values, or an `@Observable` model many
descendants need) using SwiftUI's environment, instead of manually
threading dependencies through every intermediate view's initializer.

## Scope

### Included

-   `@Environment` reads for custom and built-in environment values
-   Defining custom environment values (`EnvironmentKey`, or the `@Entry` macro)
-   Injecting an `@Observable` model with `.environment(_:)`
-   When environment injection is overkill

### Excluded

-   `@Observable` model definition itself — see `observable-macro`
-   Local `@State`/`@Binding` — see `state-and-binding`

## Rules

### Rule 1

Agents MUST use `@Environment` to read a value injected via
`.environment(_:)` (custom `@Observable` models) or a built-in
environment key (e.g., `\.dismiss`, `\.colorScheme`), rather than
passing the same dependency through every intermediate view's
initializer.

### Rule 2

Agents MUST define custom environment values as a type conforming to
`EnvironmentKey` (or, using Xcode 16's `@Entry` macro) with an explicit
default value, not force-unwrap a missing environment value at the read
site.

### Rule 3

Agents MUST inject an `@Observable` model into the environment with
`.environment(model)` — not `.environmentObject(model)`, which is the
`ObservableObject`-specific API — to stay consistent with the
`@Observable` convention.

### Rule 4

Agents MUST NOT overuse `@Environment` for values that are only needed
by one or two direct children — a plain stored-property parameter
remains simpler and more explicit for shallow dependency passing.

### Rule 5

Agents SHOULD scope the `.environment(_:)` injection call site to the
smallest subtree that actually needs the value, not always the app
root, so previews and tests can override it with a narrower substitute.

## Compliant Example

```swift
@Observable
final class SessionModel {
    var user: User?
}

RootView()
    .environment(SessionModel())

struct ProfileView: View {
    @Environment(SessionModel.self) private var session
    var body: some View {
        Text(session.user?.name ?? "Guest")
    }
}
```
`@Observable` model injected once, read via `@Environment` without prop-drilling. (Rules 1, 3)

## Non-Compliant Example

```swift
struct RootView: View {
    let session: SessionModel
    var body: some View {
        MiddleView(session: session)
    }
}

struct MiddleView: View {
    let session: SessionModel
    var body: some View {
        ProfileView(session: session)
    }
}
```
`session` threaded manually through `MiddleView`, which never uses it itself, just to reach `ProfileView`. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Environment](https://developer.apple.com/documentation/swiftui/environment)
-   [Apple Developer — EnvironmentKey](https://developer.apple.com/documentation/swiftui/environmentkey)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/environment-values.md --type knowledge`
Expected: `PASS: knowledge/swiftui/environment-values.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/environment-values.md
git commit -m "docs: add swiftui environment-values knowledge contract"
```

---

## Task 14: Native Skill — `skills/swiftui/SKILL.md`

**Files:**
- Create: `skills/swiftui/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: swiftui
description: Route SwiftUI implementation tasks to the correct Knowledge Contracts — view composition, view identity in ForEach/List, modifier order, NavigationStack/NavigationPath, NavigationSplitView, stack/spacing layout, safe area handling, lazy grids/stacks, GeometryReader pitfalls, @State/@Binding, the @Observable macro, and @Environment values. Use when writing or reviewing SwiftUI view code, structuring navigation, laying out a screen in code, choosing a state-management approach, or debugging view-identity/layout bugs. This is implementation-code guidance (iOS 17+), not visual design — for what a screen should look like, see human-interface-guidelines. Triggers on SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea.
id: skill.swiftui.foundations
title: SwiftUI — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: SwiftUI
routes: [knowledge.swiftui.view-composition, knowledge.swiftui.view-identity, knowledge.swiftui.modifier-order, knowledge.swiftui.navigation-stack, knowledge.swiftui.navigation-split-view, knowledge.swiftui.stacks-and-spacing, knowledge.swiftui.safe-area, knowledge.swiftui.lazy-grids, knowledge.swiftui.geometry-reader-anti-pattern, knowledge.swiftui.state-and-binding, knowledge.swiftui.observable-macro, knowledge.swiftui.environment-values]
related:
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-01
---

# SwiftUI — Foundations Skill

## Purpose

Route SwiftUI implementation-code tasks to the minimum required
SwiftUI Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/swiftui/.

-   Views -> view-composition.md, view-identity.md, modifier-order.md
-   Navigation -> navigation-stack.md, navigation-split-view.md
-   Layout -> stacks-and-spacing.md, safe-area.md, lazy-grids.md, geometry-reader-anti-pattern.md
-   State management -> state-and-binding.md, observable-macro.md, environment-values.md

Never load more than the contracts relevant to the specific question.
For visual/UX design guidance (what a screen should look like, not how
it's coded), route to `skill.human-interface-guidelines.foundations`
instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/swiftui/ — do not guess or fall back to general
knowledge. Animation, gestures, previews, custom `Layout` protocol
conformances, legacy `ObservableObject`/`NavigationView` migration
guidance, and accessibility APIs (owned by a future `accessibility`
domain) are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/swiftui/SKILL.md --type skill`
Expected: `PASS: skills/swiftui/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/swiftui/SKILL.md
git commit -m "feat: add swiftui native skill"
```

---

## Task 15: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`app-store-review-guidelines` row (the row containing `skills/app-store-review-guidelines/SKILL.md`):

```markdown
| SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea | skills/swiftui/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `5` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add swiftui to skills index"
```

---

## Task 16: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `swiftui` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| SwiftUI | swiftui | Views, navigation, layout | SwiftUI view/navigation/layout implementation conventions |
```

Replace with:

```markdown
| SwiftUI | swiftui | Views (composition, identity, modifier order), Navigation (NavigationStack, NavigationSplitView), Layout (stacks/spacing, safe area, lazy grids, GeometryReader), State management (@State/@Binding, @Observable, @Environment). Targets iOS 17+ conventions; legacy ObservableObject/NavigationView out of scope — see Cross-Domain Notes. | SwiftUI view, navigation, layout, and state-management implementation conventions |
```

- [ ] **Step 2: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt).
```

- [ ] **Step 3: Add two new Cross-Domain Notes entries**

Find this exact line (the last bullet in `## Cross-Domain Notes`):

```markdown
- `arkit` and `realitykit` overlap (AR/3D rendering, RealityKit often layers on ARKit sessions). Boundary not yet resolved — decide when either is reached.
```

Replace with (adds two new bullets after it):

```markdown
- `arkit` and `realitykit` overlap (AR/3D rendering, RealityKit often layers on ARKit sessions). Boundary not yet resolved — decide when either is reached.
- `swiftui` and `human-interface-guidelines` overlap on layout (`swiftui`'s `stacks-and-spacing`/`safe-area`/`lazy-grids` vs. `human-interface-guidelines`'s `layout.md`). Resolved via angle-split: `swiftui`'s angle is code-implementation (which API, correct syntax, performance), `human-interface-guidelines`'s angle is visual-design (spacing/alignment as a design decision). Same pattern as the `app-store-review-guidelines` privacy KCs vs. the future `privacy` domain.
- `swiftui` and `combine` (Tier 2, unbuilt) overlap on state management — `combine`'s Owns line already covers "SwiftUI interop." Resolved via angle-split: `swiftui`'s `observable-macro.md` teaches `@Observable` as the modern, non-Combine replacement for `ObservableObject`; `combine`'s angle (when built) is Combine-specific publisher/subscriber patterns. Boundary confirmed when `combine` is reached.
```

- [ ] **Step 4: Validate manually**

Run: `grep -c "swiftui" docs/architecture/domain-map.md`
Expected: a number greater than 1 (row + Completed line + 2 Cross-Domain Notes entries)

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: mark swiftui v1 complete, add layout/combine cross-domain notes"
```

---

## Task 17: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `app-store-review-guidelines` bullet, immediately before the `Full routing tables:` line):

```markdown
- **`app-store-review-guidelines`** — Routes App Store submission-compliance tasks (app completeness, metadata accuracy, in-app purchase, spam/duplicate-app avoidance, privacy manifest and nutrition label accuracy) to App Store Review Guidelines Knowledge Contracts.
  Example: `"why would this in-app subscription get rejected"` → `digital-goods-iap.md`, `restore-purchases.md`
  Example: `"what needs to go in my PrivacyInfo.xcprivacy"` → `privacy-manifest.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`app-store-review-guidelines`** — Routes App Store submission-compliance tasks (app completeness, metadata accuracy, in-app purchase, spam/duplicate-app avoidance, privacy manifest and nutrition label accuracy) to App Store Review Guidelines Knowledge Contracts.
  Example: `"why would this in-app subscription get rejected"` → `digital-goods-iap.md`, `restore-purchases.md`
  Example: `"what needs to go in my PrivacyInfo.xcprivacy"` → `privacy-manifest.md`

- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a new What's New line**

Find this exact line (the first/topmost line in `## What's New`):

```markdown
- 2026-07-31 — Added `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contracts.
```

Replace with (adds a new topmost line before it):

```markdown
- 2026-08-01 — Added `swiftui` Skill (Views: composition/identity/modifier order; Navigation: NavigationStack/NavigationSplitView; Layout: stacks/safe-area/lazy-grids/GeometryReader; State: @State/@Binding/@Observable/@Environment) — 12 Knowledge Contracts.
- 2026-07-31 — Added `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contracts.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "swiftui" README.md`
Expected: a number greater than 1 (Skills bullet + What's New line)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add swiftui to README Skills + What's New"
```

---

## Task 18: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/swiftui.md --type reference
python3 scripts/validate_artifact.py skills/swiftui/SKILL.md --type skill
for f in knowledge/swiftui/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
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

Use `superpowers:code-reviewer` on the entire `swiftui` domain (all 14 new
files plus the 3 modified docs) to check cross-file consistency: every
`related:` KC id resolves to a real file, the Skill's `routes:` list
matches exactly the 12 KC ids, the Reference's "Used By" list matches
exactly the 12 KC files, layer order (References → Knowledge → Skills)
is respected, and each commit is one artifact per the established
history pattern.
