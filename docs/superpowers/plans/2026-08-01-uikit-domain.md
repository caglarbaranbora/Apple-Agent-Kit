# UIKit Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `uikit` domain (1 Reference, 12 Knowledge Contracts, 1 native Skill) covering programmatic UIKit screen-scaffolding conventions — view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation — per `docs/superpowers/specs/2026-08-01-uikit-domain-design.md`, replacing the placeholder `uikit` row in `docs/architecture/domain-map.md`.

**Architecture:** Mirrors the `accessibility` domain exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/uikit.md`

**Files:**
- Create: `references/apple/uikit.md`

- [ ] **Step 1: Create the file**

```markdown
# UIKit

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/uikit

## Purpose

Reference index for Apple's UIKit documentation, scoped to this domain's
v1: programmatic (no Storyboard/XIB) screen-scaffolding conventions — view
controller lifecycle and composition, Auto Layout (constraints, stack
views, safe area), navigation (UINavigationController, UITabBarController,
modal presentation), and modern diffable table/collection views. UIKit
accessibility API implementation (accessibilityLabel, traits, VoiceOver,
Dynamic Type, etc.) is owned by the `accessibility` domain, not this one —
see docs/architecture/domain-map.md Cross-Domain Notes. Gesture
recognizers, Core Animation/CALayer, custom transitions, and UIKit-SwiftUI
interop (UIHostingController/UIViewRepresentable) are deferred to a future
pass.

## Primary Topics

- View controller lifecycle
- View controller composition
- Auto Layout constraints
- Auto Layout stack views
- Safe area and layout guides
- Navigation controller
- Tab bar controller
- Table view diffable data source
- Collection view compositional layout
- Collection view diffable data source
- Cell configuration
- Modal presentation

## Used By

- knowledge/uikit/view-controller-lifecycle.md ([[knowledge/uikit/view-controller-lifecycle]])
- knowledge/uikit/view-controller-composition.md ([[knowledge/uikit/view-controller-composition]])
- knowledge/uikit/auto-layout-constraints.md ([[knowledge/uikit/auto-layout-constraints]])
- knowledge/uikit/auto-layout-stack-views.md ([[knowledge/uikit/auto-layout-stack-views]])
- knowledge/uikit/safe-area-and-layout-guides.md ([[knowledge/uikit/safe-area-and-layout-guides]])
- knowledge/uikit/navigation-controller.md ([[knowledge/uikit/navigation-controller]])
- knowledge/uikit/tab-bar-controller.md ([[knowledge/uikit/tab-bar-controller]])
- knowledge/uikit/table-view-diffable.md ([[knowledge/uikit/table-view-diffable]])
- knowledge/uikit/collection-view-compositional-layout.md ([[knowledge/uikit/collection-view-compositional-layout]])
- knowledge/uikit/collection-view-diffable.md ([[knowledge/uikit/collection-view-diffable]])
- knowledge/uikit/cell-configuration.md ([[knowledge/uikit/cell-configuration]])
- knowledge/uikit/modal-presentation.md ([[knowledge/uikit/modal-presentation]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/uikit.md --type reference`
Expected: `PASS: references/apple/uikit.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/uikit.md
git commit -m "docs: add uikit reference index"
```

---

## Task 2: Knowledge Contract — `view-controller-lifecycle`

**Files:**
- Create: `knowledge/uikit/view-controller-lifecycle.md`

- [ ] **Step 1: Create the file**

```markdown
# View Controller Lifecycle

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.view-controller-lifecycle
type: knowledge
title: View Controller Lifecycle
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct placement of setup and teardown work across UIViewController's viewDidLoad, viewWillAppear, viewDidAppear, viewWillDisappear, and viewDidDisappear.
domain: UIKit
tags:
  - uikit
  - view-controller
  - lifecycle
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidload()
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwillappear(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidappear(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwilldisappear(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdiddisappear(_:)
depends_on: []
related:
  - knowledge.uikit.view-controller-composition
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent places one-time setup work,
per-appearance refresh work, animation-dependent work, and cleanup work
across `UIViewController`'s lifecycle methods, so view controllers don't
duplicate work or start/stop resources at the wrong time.

## Scope

### Included

-   One-time view hierarchy/constraint setup in `viewDidLoad()`
-   State refresh that must happen every appearance in `viewWillAppear(_:)`
-   Starting animations/timers/live updates in `viewDidAppear(_:)`
-   Pausing/stopping work in `viewWillDisappear(_:)`/`viewDidDisappear(_:)`

### Excluded

-   Child view controller add/remove — see `view-controller-composition`
-   Auto Layout constraint authoring — see `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST perform one-time view hierarchy construction and constraint
setup in `viewDidLoad()`, not in `viewWillAppear(_:)` — `viewDidLoad()`
runs exactly once per view controller instance; repeating it in an appear
method wastes work and can duplicate subviews on every appearance.

### Rule 2

Agents MUST refresh data-dependent UI state (a value that may have
changed while this screen was off-screen) in `viewWillAppear(_:)`, not
`viewDidLoad()` — `viewDidLoad()` only runs once, so state changed by
another screen would never be reflected on return.

### Rule 3

Agents MUST start animations, timers, or other work that requires the
view to already be in the window hierarchy in `viewDidAppear(_:)`, never
in `viewWillAppear(_:)` — the view isn't guaranteed to be in the window
yet at `viewWillAppear`, so animations timed against it can be dropped or
glitch.

### Rule 4

Agents MUST stop timers, remove notification observers, and pause
ongoing work started in `viewDidAppear(_:)` inside `viewWillDisappear(_:)`
(or `viewDidDisappear(_:)`) — leaving them running after the view leaves
the screen wastes resources and can update UI that's no longer visible.

### Rule 5

Agents MUST call the corresponding `super` lifecycle method first, before
doing any subclass work in the override — per Apple's documented override
contract, so the base class's own setup runs before the subclass depends
on it.

## Compliant Example

```swift
final class ProfileViewController: UIViewController {
    private let nameLabel = UILabel()
    private var refreshTimer: Timer?

    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(nameLabel)
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        nameLabel.text = currentUser.name
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        refreshTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.reloadStatus()
        }
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        refreshTimer?.invalidate()
        refreshTimer = nil
    }
}
```
One-time setup in `viewDidLoad`, per-appearance refresh in `viewWillAppear`, timer started only once visible and stopped on disappearance. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
final class ProfileViewController: UIViewController {
    private let nameLabel = UILabel()

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        view.addSubview(nameLabel)
        nameLabel.text = currentUser.name
    }
}
```
Subview construction runs on every appearance instead of once, duplicating the label into the view hierarchy on a second visit. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — viewDidLoad()](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidload())
-   [Apple Developer — viewWillAppear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwillappear(_:))
-   [Apple Developer — viewDidAppear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidappear(_:))
-   [Apple Developer — viewWillDisappear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwilldisappear(_:))
-   [Apple Developer — viewDidDisappear(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdiddisappear(_:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/view-controller-lifecycle.md --type knowledge`
Expected: `PASS: knowledge/uikit/view-controller-lifecycle.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/view-controller-lifecycle.md
git commit -m "docs: add uikit view-controller-lifecycle knowledge contract"
```

---

## Task 3: Knowledge Contract — `view-controller-composition`

**Files:**
- Create: `knowledge/uikit/view-controller-composition.md`

- [ ] **Step 1: Create the file**

```markdown
# View Controller Composition

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.view-controller-composition
type: knowledge
title: View Controller Composition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the child view controller container pattern — addChild(_:), view hierarchy insertion, and didMove(toParent:)/willMove(toParent:) — for embedding one view controller's content inside another.
domain: UIKit
tags:
  - uikit
  - view-controller
  - composition
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/didmove(toparent:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/willmove(toparent:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/removefromparent()
depends_on: []
related:
  - knowledge.uikit.view-controller-lifecycle
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent embeds a child view
controller's view inside a parent so both view controllers' lifecycles
and event forwarding stay correct, instead of adding a child's view as a
bare subview with no containment relationship.

## Scope

### Included

-   `addChild(_:)` + view hierarchy insertion + `didMove(toParent:)` sequence
-   Removing a child view controller (`willMove(toParent: nil)` + `removeFromParent()`)

### Excluded

-   `UINavigationController`/`UITabBarController` (system containers) — see `navigation-controller`, `tab-bar-controller`

## Rules

### Rule 1

Agents MUST call `addChild(_:)` on the parent before adding the child's
`view` as a subview — adding the view first without registering
containment breaks the child's `parent`/`didMove` lifecycle callbacks and
any layout-guide/trait propagation the system provides to properly
contained children.

### Rule 2

Agents MUST call `child.didMove(toParent: self)` immediately after adding
the child's view to the parent's view hierarchy — this is Apple's
documented completion step of the containment sequence; skipping it
leaves the child view controller unaware it's now installed.

### Rule 3

Agents MUST call `child.willMove(toParent: nil)` before removing a
child's view from the hierarchy, and `child.removeFromParent()` after —
in that order — so the child gets a chance to react before removal and
the parent-child relationship is torn down cleanly afterward.

### Rule 4

Agents MUST set the child's view `frame` (or constraints) explicitly
after insertion — a child view controller's view has no inherent size or
position in the parent; forgetting this produces a zero-frame or
misplaced child view.

## Compliant Example

```swift
final class DashboardViewController: UIViewController {
    private let summaryVC = SummaryViewController()

    override func viewDidLoad() {
        super.viewDidLoad()
        addChild(summaryVC)
        view.addSubview(summaryVC.view)
        summaryVC.view.frame = view.bounds
        summaryVC.didMove(toParent: self)
    }

    func removeSummary() {
        summaryVC.willMove(toParent: nil)
        summaryVC.view.removeFromSuperview()
        summaryVC.removeFromParent()
    }
}
```
Full four-step containment sequence on install; correctly ordered teardown on removal. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
final class DashboardViewController: UIViewController {
    private let summaryVC = SummaryViewController()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(summaryVC.view)
    }
}
```
The child's view is added directly without `addChild(_:)` or `didMove(toParent:)` — `summaryVC.parent` stays `nil` and the child never receives correct containment callbacks. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — addChild(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:))
-   [Apple Developer — didMove(toParent:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/didmove(toparent:))
-   [Apple Developer — willMove(toParent:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/willmove(toparent:))
-   [Apple Developer — removeFromParent()](https://developer.apple.com/documentation/uikit/uiviewcontroller/removefromparent())
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/view-controller-composition.md --type knowledge`
Expected: `PASS: knowledge/uikit/view-controller-composition.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/view-controller-composition.md
git commit -m "docs: add uikit view-controller-composition knowledge contract"
```

---

## Task 4: Knowledge Contract — `auto-layout-constraints`

**Files:**
- Create: `knowledge/uikit/auto-layout-constraints.md`

- [ ] **Step 1: Create the file**

```markdown
# Auto Layout Constraints

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.auto-layout-constraints
type: knowledge
title: Auto Layout Constraints
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of NSLayoutConstraint and layout anchors, plus translatesAutoresizingMaskIntoConstraints, to position views programmatically without ambiguous or conflicting layout.
domain: UIKit
tags:
  - uikit
  - auto-layout
  - constraints
references:
  - https://developer.apple.com/documentation/uikit/nslayoutconstraint
  - https://developer.apple.com/documentation/uikit/nslayoutanchor
  - https://developer.apple.com/documentation/uikit/uiview/translatesautoresizingmaskintoconstraints
depends_on: []
related:
  - knowledge.uikit.safe-area-and-layout-guides
  - knowledge.uikit.auto-layout-stack-views
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent authors programmatic Auto
Layout with anchors so views position correctly across size classes
without ambiguous or conflicting constraints.

## Scope

### Included

-   Setting `translatesAutoresizingMaskIntoConstraints = false` on programmatically added views
-   Anchor-based constraint creation and `NSLayoutConstraint.activate`
-   Avoiding ambiguous or unsatisfiable constraints

### Excluded

-   `UIStackView` — see `auto-layout-stack-views`
-   Safe area / layout margin guides — see `safe-area-and-layout-guides`

## Rules

### Rule 1

Agents MUST set `translatesAutoresizingMaskIntoConstraints = false` on
every view added programmatically before applying Auto Layout
constraints to it — leaving the default `true` makes the system generate
an autoresizing-mask-derived constraint that conflicts with explicit
constraints.

### Rule 2

Agents MUST use layout anchors (`leadingAnchor`, `topAnchor`,
`widthAnchor`, `centerXAnchor`, etc.) with
`NSLayoutConstraint.activate([...])` rather than the older
`NSLayoutConstraint(item:attribute:relatedBy:toItem:attribute:multiplier:constant:)`
initializer — anchors are type-safe (can't accidentally constrain a
horizontal anchor to a vertical one) and read closer to the resulting
layout.

### Rule 3

Agents MUST batch-activate a view's full constraint set in one
`NSLayoutConstraint.activate([...])` call rather than setting
`.isActive = true` on each constraint individually — batching lets Auto
Layout resolve the whole set together instead of potentially hitting a
transient ambiguous state between individual activations.

### Rule 4

Agents MUST give every added view a complete constraint set (position
plus size, whether explicit or derived from content/intrinsic size) — a
view with only, say, a leading and top anchor has an ambiguous width and
height, and Auto Layout will place it at zero size or log an ambiguity
warning.

## Compliant Example

```swift
let avatarImageView = UIImageView()
avatarImageView.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(avatarImageView)

NSLayoutConstraint.activate([
    avatarImageView.topAnchor.constraint(equalTo: view.topAnchor, constant: 16),
    avatarImageView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    avatarImageView.widthAnchor.constraint(equalToConstant: 44),
    avatarImageView.heightAnchor.constraint(equalToConstant: 44),
])
```
Autoresizing mask disabled, anchors batch-activated, full position and size constraint set. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
let avatarImageView = UIImageView()
view.addSubview(avatarImageView)

avatarImageView.topAnchor.constraint(equalTo: view.topAnchor, constant: 16).isActive = true
avatarImageView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16).isActive = true
```
`translatesAutoresizingMaskIntoConstraints` left `true` (conflicts with the explicit constraints) and no width/height, leaving the image view's size ambiguous. (Rules 1, 4)

## Dependencies

None.

## References

-   [Apple Developer — NSLayoutConstraint](https://developer.apple.com/documentation/uikit/nslayoutconstraint)
-   [Apple Developer — NSLayoutAnchor](https://developer.apple.com/documentation/uikit/nslayoutanchor)
-   [Apple Developer — translatesAutoresizingMaskIntoConstraints](https://developer.apple.com/documentation/uikit/uiview/translatesautoresizingmaskintoconstraints)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/auto-layout-constraints.md --type knowledge`
Expected: `PASS: knowledge/uikit/auto-layout-constraints.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/auto-layout-constraints.md
git commit -m "docs: add uikit auto-layout-constraints knowledge contract"
```

---

## Task 5: Knowledge Contract — `auto-layout-stack-views`

**Files:**
- Create: `knowledge/uikit/auto-layout-stack-views.md`

- [ ] **Step 1: Create the file**

```markdown
# Auto Layout Stack Views

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.auto-layout-stack-views
type: knowledge
title: Auto Layout Stack Views
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UIStackView (axis, distribution, alignment, spacing) to lay out a linear sequence of views without hand-written inter-view constraints.
domain: UIKit
tags:
  - uikit
  - auto-layout
  - stack-view
references:
  - https://developer.apple.com/documentation/uikit/uistackview
  - https://developer.apple.com/documentation/uikit/uistackview/distribution-swift.property
  - https://developer.apple.com/documentation/uikit/uistackview/alignment-swift.property
depends_on: []
related:
  - knowledge.uikit.auto-layout-constraints
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent uses `UIStackView` to
arrange a linear row or column of views, picking a correct axis,
distribution, alignment, and spacing instead of hand-writing inter-view
constraints for a case `UIStackView` already solves.

## Scope

### Included

-   Axis, distribution, alignment, spacing configuration
-   Nesting stack views for two-dimensional layouts
-   When a stack view is the right tool vs. plain constraints

### Excluded

-   Constraining the stack view itself to its superview — see `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST use `UIStackView` instead of hand-written leading/trailing
constraints between sibling views when laying out a linear (horizontal
or vertical) sequence of views — the stack view manages inter-view
spacing and distribution automatically, avoiding N-1 manually authored
constraints.

### Rule 2

Agents MUST set an explicit `distribution` (`.fill`, `.fillEqually`,
`.fillProportionally`, `.equalSpacing`, `.equalCentering`) rather than
leaving the default — the default `.fill` silently relies on each
arranged subview's content-hugging/compression-resistance priorities,
which is often not the intended layout.

### Rule 3

Agents MUST still constrain the stack view itself to its superview (or
use it as an arranged subview of an outer stack) — `UIStackView` only
manages its own arranged subviews' internal layout, not its own
position, so it needs standard constraints per `auto-layout-constraints`.

### Rule 4

Agents SHOULD nest stack views (a horizontal stack of vertical stacks, or
vice versa) for two-dimensional layouts rather than falling back to raw
constraints, when the layout is still fundamentally row/column-based.

## Compliant Example

```swift
let titleLabel = UILabel()
let subtitleLabel = UILabel()
let textStack = UIStackView(arrangedSubviews: [titleLabel, subtitleLabel])
textStack.axis = .vertical
textStack.distribution = .fill
textStack.alignment = .leading
textStack.spacing = 4
textStack.translatesAutoresizingMaskIntoConstraints = false
```
Explicit axis, distribution, alignment, and spacing on a vertical text stack. (Rules 1, 2)

## Non-Compliant Example

```swift
let titleLabel = UILabel()
let subtitleLabel = UILabel()
view.addSubview(titleLabel)
view.addSubview(subtitleLabel)

NSLayoutConstraint.activate([
    titleLabel.topAnchor.constraint(equalTo: view.topAnchor),
    subtitleLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 4),
])
```
Hand-written inter-view constraint for a plain vertical sequence that `UIStackView` would express in three configuration lines. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — UIStackView](https://developer.apple.com/documentation/uikit/uistackview)
-   [Apple Developer — UIStackView.distribution](https://developer.apple.com/documentation/uikit/uistackview/distribution-swift.property)
-   [Apple Developer — UIStackView.alignment](https://developer.apple.com/documentation/uikit/uistackview/alignment-swift.property)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/auto-layout-stack-views.md --type knowledge`
Expected: `PASS: knowledge/uikit/auto-layout-stack-views.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/auto-layout-stack-views.md
git commit -m "docs: add uikit auto-layout-stack-views knowledge contract"
```

---

## Task 6: Knowledge Contract — `safe-area-and-layout-guides`

**Files:**
- Create: `knowledge/uikit/safe-area-and-layout-guides.md`

- [ ] **Step 1: Create the file**

```markdown
# Safe Area and Layout Guides

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.safe-area-and-layout-guides
type: knowledge
title: Safe Area and Layout Guides
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of safeAreaLayoutGuide and layoutMarginsGuide to anchor content clear of system chrome and respect consistent view margins.
domain: UIKit
tags:
  - uikit
  - auto-layout
  - safe-area
references:
  - https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide
  - https://developer.apple.com/documentation/uikit/uiview/layoutmarginsguide
depends_on: []
related:
  - knowledge.uikit.auto-layout-constraints
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent anchors content to
`safeAreaLayoutGuide`/`layoutMarginsGuide` instead of a view's raw edges,
so content stays clear of system chrome and respects consistent margins.

## Scope

### Included

-   Constraining to `safeAreaLayoutGuide` anchors instead of view edge anchors
-   `layoutMarginsGuide` for consistent inset content
-   When to intentionally extend content under the safe area (backgrounds)

### Excluded

-   General anchor-based constraint mechanics — see `auto-layout-constraints`

## Rules

### Rule 1

Agents MUST anchor top-level content (navigation bars, primary text,
interactive controls) to `view.safeAreaLayoutGuide` anchors, not
`view.topAnchor`/`view.bottomAnchor` directly — anchoring to the raw view
edge places content under the status bar, notch/Dynamic Island, or home
indicator on devices where those obstruct the edge.

### Rule 2

Agents MUST NOT apply `safeAreaLayoutGuide` to background or decorative
views meant to fill the entire screen (a full-bleed background image or
color) — constrain those to `view`'s edges directly so they extend under
the status bar/home indicator area as visually intended.

### Rule 3

Agents SHOULD use `view.layoutMarginsGuide` instead of hand-picked
constant insets when a screen's content should respect the system's
standard content margins — this keeps horizontal insets consistent with
other UIKit screens and adapts automatically to size class and device.

### Rule 4

Agents MUST re-verify safe area insets after rotation or size class
changes for any manual (non-constraint) frame math involving
`safeAreaInsets` — these values change with device orientation and
windowing, and stale cached values misplace content.

## Compliant Example

```swift
let scrollView = UIScrollView()
scrollView.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(scrollView)

NSLayoutConstraint.activate([
    scrollView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
    scrollView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor),
    scrollView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor),
    scrollView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
])
```
Content scroll view anchored to the safe area guide, clear of the notch and home indicator. (Rule 1)

## Non-Compliant Example

```swift
let scrollView = UIScrollView()
view.addSubview(scrollView)
NSLayoutConstraint.activate([
    scrollView.topAnchor.constraint(equalTo: view.topAnchor),
    scrollView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
])
```
Anchored to the view's raw top/bottom edges — on notched devices the first row of content renders under the status bar or Dynamic Island. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — safeAreaLayoutGuide](https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide)
-   [Apple Developer — layoutMarginsGuide](https://developer.apple.com/documentation/uikit/uiview/layoutmarginsguide)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/safe-area-and-layout-guides.md --type knowledge`
Expected: `PASS: knowledge/uikit/safe-area-and-layout-guides.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/safe-area-and-layout-guides.md
git commit -m "docs: add uikit safe-area-and-layout-guides knowledge contract"
```

---

## Task 7: Knowledge Contract — `navigation-controller`

**Files:**
- Create: `knowledge/uikit/navigation-controller.md`

- [ ] **Step 1: Create the file**

```markdown
# Navigation Controller

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.navigation-controller
type: knowledge
title: Navigation Controller
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UINavigationController push/pop navigation and navigationItem configuration for a stack-based UIKit screen flow.
domain: UIKit
tags:
  - uikit
  - navigation
  - navigation-controller
references:
  - https://developer.apple.com/documentation/uikit/uinavigationcontroller
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/navigationitem
depends_on: []
related:
  - knowledge.uikit.tab-bar-controller
  - knowledge.uikit.modal-presentation
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent pushes and pops screens
onto a `UINavigationController` stack and configures each screen's
`navigationItem`, so back navigation and bar content behave correctly
without manual view controller stacking.

## Scope

### Included

-   `pushViewController(_:animated:)`/`popViewController(animated:)`/`popToRootViewController(animated:)`
-   `navigationItem.title`, `backButtonTitle`, `leftBarButtonItem`/`rightBarButtonItem`

### Excluded

-   Modal present/dismiss — see `modal-presentation`
-   `UITabBarController` — see `tab-bar-controller`

## Rules

### Rule 1

Agents MUST push a new screen onto an existing `UINavigationController`
stack with `navigationController?.pushViewController(_:animated:)`
rather than presenting it modally, whenever the new screen is a
drill-down/detail continuation of the current stack — pushing preserves
the back-stack and the standard back-swipe gesture; modal presentation
does not.

### Rule 2

Agents MUST set `navigationItem.title` (or a custom `titleView`) on each
pushed view controller rather than on the navigation controller itself —
`UINavigationController` displays whichever pushed view controller's own
`navigationItem` is currently on top; setting a title on the navigation
controller has no per-screen effect.

### Rule 3

Agents SHOULD set `navigationItem.backButtonTitle` when the previous
screen's title is too long or unsuitable as a back-button label — the
default back button title is the *previous* screen's `title`, which can
be visually cramped.

### Rule 4

Agents MUST NOT call `popViewController(animated:)` from a view
controller that is not currently the top of the navigation stack —
popping from a non-top controller is undefined/no-op behavior; pop is
only valid from the currently visible screen.

## Compliant Example

```swift
final class InboxViewController: UIViewController {
    func showDetail(for message: Message) {
        let detailVC = MessageDetailViewController(message: message)
        detailVC.navigationItem.title = message.subject
        navigationController?.pushViewController(detailVC, animated: true)
    }
}
```
Push (not modal present) for a drill-down detail screen; title set on the pushed controller's own `navigationItem`. (Rules 1, 2)

## Non-Compliant Example

```swift
final class InboxViewController: UIViewController {
    func showDetail(for message: Message) {
        let detailVC = MessageDetailViewController(message: message)
        title = message.subject
        present(detailVC, animated: true)
    }
}
```
Modal `present` used for a drill-down continuation (loses the back-swipe/back-stack), and the title is set on the wrong view controller (`self`, not `detailVC`). (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — UINavigationController](https://developer.apple.com/documentation/uikit/uinavigationcontroller)
-   [Apple Developer — navigationItem](https://developer.apple.com/documentation/uikit/uiviewcontroller/navigationitem)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/navigation-controller.md --type knowledge`
Expected: `PASS: knowledge/uikit/navigation-controller.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/navigation-controller.md
git commit -m "docs: add uikit navigation-controller knowledge contract"
```

---

## Task 8: Knowledge Contract — `tab-bar-controller`

**Files:**
- Create: `knowledge/uikit/tab-bar-controller.md`

- [ ] **Step 1: Create the file**

```markdown
# Tab Bar Controller

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.tab-bar-controller
type: knowledge
title: Tab Bar Controller
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UITabBarController and per-view-controller tabBarItem configuration to present sibling top-level screens behind a persistent tab bar.
domain: UIKit
tags:
  - uikit
  - navigation
  - tab-bar
references:
  - https://developer.apple.com/documentation/uikit/uitabbarcontroller
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/tabbaritem
depends_on: []
related:
  - knowledge.uikit.navigation-controller
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent assembles a
`UITabBarController`'s `viewControllers` array and configures each
child's `tabBarItem`, so top-level sibling screens are reachable behind a
persistent tab bar with correct icons and titles.

## Scope

### Included

-   Setting `viewControllers` on a `UITabBarController`
-   `tabBarItem` title/image per child, badge value
-   Embedding a `UINavigationController` per tab

### Excluded

-   Push/pop within a given tab's stack — see `navigation-controller`

## Rules

### Rule 1

Agents MUST set each child view controller's `tabBarItem` (title and
image) before assigning it into the `UITabBarController.viewControllers`
array — `UITabBarController` reads each child's own `tabBarItem` to build
the tab bar; an unset item shows a blank/untitled tab.

### Rule 2

Agents MUST wrap any tab whose content needs its own push/pop navigation
in a `UINavigationController` before adding it to `viewControllers` — the
tab bar controller does not provide stack navigation itself; embedding a
`UINavigationController` per tab is the standard way to get both a
persistent tab bar and per-tab navigation stacks.

### Rule 3

Agents MUST set `UITabBarController.viewControllers` in the exact order
tabs should appear left-to-right — the array order is the display order,
not the badge or selection order.

### Rule 4

Agents SHOULD use `tabBarItem.badgeValue` for a per-tab unread or
notification count instead of embedding a custom badge view —
`badgeValue` is the system-provided mechanism and matches platform
conventions automatically.

## Compliant Example

```swift
let inboxVC = UINavigationController(rootViewController: InboxViewController())
inboxVC.tabBarItem = UITabBarItem(title: "Inbox", image: UIImage(systemName: "tray"), tag: 0)

let settingsVC = UINavigationController(rootViewController: SettingsViewController())
settingsVC.tabBarItem = UITabBarItem(title: "Settings", image: UIImage(systemName: "gear"), tag: 1)

let tabBarController = UITabBarController()
tabBarController.viewControllers = [inboxVC, settingsVC]
```
Each tab wrapped in its own navigation controller with a configured `tabBarItem` before assignment. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
let tabBarController = UITabBarController()
tabBarController.viewControllers = [InboxViewController(), SettingsViewController()]
```
Neither child has a configured `tabBarItem` (both show blank tabs), and neither is wrapped in a navigation controller, so pushing a detail screen from either tab has no stack to push onto. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — UITabBarController](https://developer.apple.com/documentation/uikit/uitabbarcontroller)
-   [Apple Developer — tabBarItem](https://developer.apple.com/documentation/uikit/uiviewcontroller/tabbaritem)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/tab-bar-controller.md --type knowledge`
Expected: `PASS: knowledge/uikit/tab-bar-controller.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/tab-bar-controller.md
git commit -m "docs: add uikit tab-bar-controller knowledge contract"
```

---

## Task 9: Knowledge Contract — `table-view-diffable`

**Files:**
- Create: `knowledge/uikit/table-view-diffable.md`

- [ ] **Step 1: Create the file**

```markdown
# Table View Diffable Data Source

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.table-view-diffable
type: knowledge
title: Table View Diffable Data Source
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UITableViewDiffableDataSource and NSDiffableDataSourceSnapshot to drive a UITableView's content from applied snapshots instead of manual reloadData or index-path bookkeeping.
domain: UIKit
tags:
  - uikit
  - table-view
  - diffable-data-source
references:
  - https://developer.apple.com/documentation/uikit/uitableviewdiffabledatasource
  - https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot
depends_on: []
related:
  - knowledge.uikit.cell-configuration
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent drives a `UITableView`'s
rows from a `UITableViewDiffableDataSource` and applied snapshot, so row
insert/delete/reorder animations are computed automatically instead of
hand-managed index paths.

## Scope

### Included

-   Constructing `UITableViewDiffableDataSource` with a cell provider
-   Building and applying `NSDiffableDataSourceSnapshot` (sections and items)
-   `animatingDifferences` on apply

### Excluded

-   Cell dequeue/registration mechanics — see `cell-configuration`
-   Classic `UITableViewDataSource` `cellForRowAt` pattern — permanently out of scope for this domain

## Rules

### Rule 1

Agents MUST drive a `UITableView`'s content through
`UITableViewDiffableDataSource` and `NSDiffableDataSourceSnapshot` rather
than implementing `UITableViewDataSource`'s `cellForRowAt`/
`numberOfRowsInSection` directly — the diffable data source computes
correct insert/delete/move animations from snapshot differences
automatically, which manual `reloadData()` cannot do.

### Rule 2

Agents MUST build a complete `NSDiffableDataSourceSnapshot` (append all
sections, then append all items per section) and apply it via
`dataSource.apply(snapshot, animatingDifferences:)` rather than mutating
the table view's rows directly — the snapshot is the single source of
truth the diffable data source diffs against.

### Rule 3

Agents MUST assign the constructed `UITableViewDiffableDataSource` to the
table view's `dataSource` property and retain a strong reference to it on
the owning view controller — `UITableView.dataSource` is a weak
reference, so a data source with no other owner is deallocated
immediately and rows silently stop appearing.

### Rule 4

Agents SHOULD pass `animatingDifferences: false` only for the first
snapshot applied after the table view loads — animating the initial
population produces an unwanted animation of rows appearing from
nothing; subsequent updates should animate (`true`) so changes are
visible to the user.

## Compliant Example

```swift
enum Section { case main }

final class InboxViewController: UIViewController {
    private let tableView = UITableView()
    private var dataSource: UITableViewDiffableDataSource<Section, Message>!

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(tableView)
        NSLayoutConstraint.activate([
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ])
        dataSource = UITableViewDiffableDataSource<Section, Message>(tableView: tableView) { tableView, indexPath, message in
            let cell = tableView.dequeueReusableCell(withIdentifier: "MessageCell", for: indexPath)
            cell.textLabel?.text = message.subject
            return cell
        }
        applySnapshot(animatingDifferences: false)
    }

    func applySnapshot(animatingDifferences: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Message>()
        snapshot.appendSections([.main])
        snapshot.appendItems(messages, toSection: .main)
        dataSource.apply(snapshot, animatingDifferences: animatingDifferences)
    }
}
```
Diffable data source retained as a stored property, snapshot built and applied, first population unanimated. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
final class InboxViewController: UIViewController, UITableViewDataSource {
    private let tableView = UITableView()

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        messages.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "MessageCell", for: indexPath)
        cell.textLabel?.text = messages[indexPath.row].subject
        return cell
    }
}
```
Classic `UITableViewDataSource` implementation — any row change requires a manual `reloadData()` with no automatic diff-based animation. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — UITableViewDiffableDataSource](https://developer.apple.com/documentation/uikit/uitableviewdiffabledatasource)
-   [Apple Developer — NSDiffableDataSourceSnapshot](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/table-view-diffable.md --type knowledge`
Expected: `PASS: knowledge/uikit/table-view-diffable.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/table-view-diffable.md
git commit -m "docs: add uikit table-view-diffable knowledge contract"
```

---

## Task 10: Knowledge Contract — `collection-view-compositional-layout`

**Files:**
- Create: `knowledge/uikit/collection-view-compositional-layout.md`

- [ ] **Step 1: Create the file**

```markdown
# Collection View Compositional Layout

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.collection-view-compositional-layout
type: knowledge
title: Collection View Compositional Layout
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines composing UICollectionViewCompositionalLayout from NSCollectionLayoutItem, NSCollectionLayoutGroup, and NSCollectionLayoutSection to describe a collection view's visual arrangement.
domain: UIKit
tags:
  - uikit
  - collection-view
  - compositional-layout
references:
  - https://developer.apple.com/documentation/uikit/uicollectionviewcompositionallayout
  - https://developer.apple.com/documentation/uikit/nscollectionlayoutsection
  - https://developer.apple.com/documentation/uikit/nscollectionlayoutgroup
  - https://developer.apple.com/documentation/uikit/nscollectionlayoutitem
depends_on: []
related:
  - knowledge.uikit.collection-view-diffable
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent builds a
`UICollectionViewCompositionalLayout` by composing item, group, and
section, so a collection view's grid/list/multi-column arrangement is
declared structurally instead of via manual `UICollectionViewLayout`
subclassing.

## Scope

### Included

-   `NSCollectionLayoutItem` sizing (estimated/absolute/fractional dimensions)
-   `NSCollectionLayoutGroup` horizontal/vertical composition
-   `NSCollectionLayoutSection` assembly, `interGroupSpacing`, `contentInsets`

### Excluded

-   Binding data to the layout — see `collection-view-diffable`
-   Cell registration — see `cell-configuration`

## Rules

### Rule 1

Agents MUST build collection view layouts with
`UICollectionViewCompositionalLayout` (item → group → section) rather
than subclassing `UICollectionViewLayout` or using the legacy
`UICollectionViewFlowLayout` for any new v1 screen — compositional layout
expresses nested/multi-column arrangements declaratively without manual
`layoutAttributesForElements` overrides.

### Rule 2

Agents MUST use `.fractionalWidth`/`.fractionalHeight` dimensions for
items/groups that should scale with the collection view's own size (for
example, "half the section width") rather than `.absolute` — absolute
dimensions don't adapt across device sizes or size classes.

### Rule 3

Agents MUST set `NSCollectionLayoutSection.contentInsets` and
`interGroupSpacing` explicitly on every section rather than relying on
layout defaults — the system defaults produce zero spacing, which
usually isn't the intended visual result.

### Rule 4

Agents SHOULD compose nested groups (a horizontal group of vertical
groups, or vice versa) for multi-column/grid arrangements rather than
falling back to a single flat group — nesting is how compositional
layout expresses two-dimensional arrangements.

## Compliant Example

```swift
func makeLayout() -> UICollectionViewCompositionalLayout {
    let itemSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .fractionalHeight(1.0))
    let item = NSCollectionLayoutItem(layoutSize: itemSize)

    let groupSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(0.5), heightDimension: .absolute(120))
    let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

    let section = NSCollectionLayoutSection(group: group)
    section.contentInsets = NSDirectionalEdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16)
    section.interGroupSpacing = 12

    return UICollectionViewCompositionalLayout(section: section)
}
```
Fractional item/group sizing for a two-column grid, explicit content insets and inter-group spacing. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
let layout = UICollectionViewFlowLayout()
layout.itemSize = CGSize(width: 160, height: 120)
collectionView.collectionViewLayout = layout
```
Legacy `UICollectionViewFlowLayout` with an absolute item size that won't adapt across device widths, instead of a compositional layout with fractional sizing. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — UICollectionViewCompositionalLayout](https://developer.apple.com/documentation/uikit/uicollectionviewcompositionallayout)
-   [Apple Developer — NSCollectionLayoutSection](https://developer.apple.com/documentation/uikit/nscollectionlayoutsection)
-   [Apple Developer — NSCollectionLayoutGroup](https://developer.apple.com/documentation/uikit/nscollectionlayoutgroup)
-   [Apple Developer — NSCollectionLayoutItem](https://developer.apple.com/documentation/uikit/nscollectionlayoutitem)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/collection-view-compositional-layout.md --type knowledge`
Expected: `PASS: knowledge/uikit/collection-view-compositional-layout.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/collection-view-compositional-layout.md
git commit -m "docs: add uikit collection-view-compositional-layout knowledge contract"
```

---

## Task 11: Knowledge Contract — `collection-view-diffable`

**Files:**
- Create: `knowledge/uikit/collection-view-diffable.md`

- [ ] **Step 1: Create the file**

```markdown
# Collection View Diffable Data Source

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.collection-view-diffable
type: knowledge
title: Collection View Diffable Data Source
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UICollectionViewDiffableDataSource and NSDiffableDataSourceSnapshot to bind data to a collection view built with UICollectionViewCompositionalLayout.
domain: UIKit
tags:
  - uikit
  - collection-view
  - diffable-data-source
references:
  - https://developer.apple.com/documentation/uikit/uicollectionviewdiffabledatasource
  - https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot
depends_on: []
related:
  - knowledge.uikit.collection-view-compositional-layout
  - knowledge.uikit.cell-configuration
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent binds data to a collection
view via `UICollectionViewDiffableDataSource` and an applied snapshot,
mirroring `table-view-diffable`'s split between layout structure
(`collection-view-compositional-layout`) and data binding (this
contract).

## Scope

### Included

-   Constructing `UICollectionViewDiffableDataSource` with a cell provider
-   Building and applying `NSDiffableDataSourceSnapshot` (sections and items)
-   Reloading vs. reconfiguring items on data change

### Excluded

-   Layout structure (item/group/section sizing) — see `collection-view-compositional-layout`
-   Cell registration mechanics — see `cell-configuration`

## Rules

### Rule 1

Agents MUST bind a `UICollectionView`'s content through
`UICollectionViewDiffableDataSource` and `NSDiffableDataSourceSnapshot`,
not `UICollectionViewDataSource`'s `cellForItemAt`/
`numberOfItemsInSection` — same rationale as `table-view-diffable`:
correct insert/delete/move animations computed from snapshot diffs.

### Rule 2

Agents MUST retain a strong reference to the constructed
`UICollectionViewDiffableDataSource` on the owning view controller —
`UICollectionView.dataSource` is a weak reference; an unretained data
source is deallocated immediately and the collection view renders empty.

### Rule 3

Agents MUST use `snapshot.reconfigureItems([...])` (not `reloadItems`)
when only an existing item's *content* changed and its identity is
unchanged — `reconfigureItems` updates the cell in place, while
`reloadItems` triggers a full dequeue/configure cycle and a visible
reload animation even when the item didn't move.

### Rule 4

Agents MUST ensure the item type used as the snapshot's item identifier
conforms to `Hashable` with a stable identity (a model's unique ID, not a
value that changes when unrelated fields update) — the diffable data
source uses this identity to compute which items are the "same" item
across snapshots; an unstable identity produces spurious insert/delete
pairs instead of in-place updates.

## Compliant Example

```swift
enum Section { case main }

final class GalleryViewController: UIViewController {
    private var collectionView: UICollectionView!
    private var dataSource: UICollectionViewDiffableDataSource<Section, Photo>!

    override func viewDidLoad() {
        super.viewDidLoad()
        dataSource = UICollectionViewDiffableDataSource<Section, Photo>(collectionView: collectionView) { collectionView, indexPath, photo in
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "PhotoCell", for: indexPath) as! PhotoCell
            cell.configure(with: photo)
            return cell
        }
        applySnapshot(animatingDifferences: false)
    }

    func applySnapshot(animatingDifferences: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Photo>()
        snapshot.appendSections([.main])
        snapshot.appendItems(photos, toSection: .main)
        dataSource.apply(snapshot, animatingDifferences: animatingDifferences)
    }
}
```
Diffable data source retained as a stored property; `Photo` provides stable `Hashable` identity via its unique ID. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
func updateCaption(for photo: Photo) {
    var snapshot = dataSource.snapshot()
    snapshot.reloadItems([photo])
    dataSource.apply(snapshot)
}
```
Uses `reloadItems` for an in-place content-only change — triggers a full dequeue/configure and reload animation when `reconfigureItems` would update the existing cell in place. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — UICollectionViewDiffableDataSource](https://developer.apple.com/documentation/uikit/uicollectionviewdiffabledatasource)
-   [Apple Developer — NSDiffableDataSourceSnapshot](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/collection-view-diffable.md --type knowledge`
Expected: `PASS: knowledge/uikit/collection-view-diffable.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/collection-view-diffable.md
git commit -m "docs: add uikit collection-view-diffable knowledge contract"
```

---

## Task 12: Knowledge Contract — `cell-configuration`

**Files:**
- Create: `knowledge/uikit/cell-configuration.md`

- [ ] **Step 1: Create the file**

```markdown
# Cell Configuration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.cell-configuration
type: knowledge
title: Cell Configuration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UICollectionView.CellRegistration and UITableView cell registration, reuse identifiers, and prepareForReuse to configure reusable table and collection view cells correctly.
domain: UIKit
tags:
  - uikit
  - cell
  - reuse
references:
  - https://developer.apple.com/documentation/uikit/uicollectionview/cellregistration
  - https://developer.apple.com/documentation/uikit/uitableview/register(_:forcellreuseidentifier:)-3l3ct
  - https://developer.apple.com/documentation/uikit/uitableviewcell/prepareforreuse()
depends_on: []
related:
  - knowledge.uikit.table-view-diffable
  - knowledge.uikit.collection-view-diffable
  - knowledge.accessibility.accessibility-labels
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent registers and configures
reusable table and collection view cells so recycled cells never leak
stale content from a previous item. Accessibility properties on a cell's
content are cross-referenced to the `accessibility` domain, not
duplicated here.

## Scope

### Included

-   `UICollectionView.CellRegistration` typed cell registration
-   `UITableView.register(_:forCellReuseIdentifier:)` and `dequeueReusableCell`
-   Resetting per-item state in `prepareForReuse()`

### Excluded

-   Accessibility labeling of cell content — see `knowledge.accessibility.accessibility-labels`
-   Data binding / snapshot apply — see `table-view-diffable`, `collection-view-diffable`

## Rules

### Rule 1

Agents MUST register cell classes/reuse identifiers before the table or
collection view attempts to dequeue them —
`UICollectionView.CellRegistration` (used with
`dequeueConfiguredReusableCell(using:for:item:)`) or
`UITableView.register(_:forCellReuseIdentifier:)`, done once (typically
in `viewDidLoad`), not per-dequeue.

### Rule 2

Agents SHOULD prefer `UICollectionView.CellRegistration` over a raw
string reuse identifier plus a forced downcast when constructing a
collection view's cell provider — `CellRegistration` is generic over the
concrete cell type, so the compiler catches a mismatched cell type
instead of a runtime crash on `as!`.

### Rule 3

Agents MUST reset any per-item mutable state that isn't overwritten
unconditionally by the next configuration (an image loaded
asynchronously, a highlight/selection flag) in `prepareForReuse()` —
reused cells retain their previous subview state unless explicitly
cleared, so a slow image load for item A can visually appear on a
recycled cell now showing item B.

### Rule 4

Agents MUST configure every visible property of a cell unconditionally
from the current item's data on every dequeue, not just properties that
differ from some assumed default — a cell instance is reused across
arbitrary prior items, so any property set conditionally (only when a
flag is true) can carry over stale state from a previous item when the
condition is now false.

## Compliant Example

```swift
final class PhotoCell: UICollectionViewCell {
    let imageView = UIImageView()
    private var loadTask: Task<Void, Never>?

    func configure(with photo: Photo) {
        loadTask?.cancel()
        imageView.image = nil
        loadTask = Task {
            let image = await ImageLoader.load(photo.url)
            if !Task.isCancelled { imageView.image = image }
        }
    }

    override func prepareForReuse() {
        super.prepareForReuse()
        loadTask?.cancel()
        imageView.image = nil
    }
}

let registration = UICollectionView.CellRegistration<PhotoCell, Photo> { cell, indexPath, photo in
    cell.configure(with: photo)
}
```
Typed `CellRegistration`, unconditional per-item configuration, in-flight async load cancelled and image cleared in `prepareForReuse()`. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
final class PhotoCell: UICollectionViewCell {
    let imageView = UIImageView()

    func configure(with photo: Photo) {
        if photo.hasCustomImage {
            imageView.image = photo.thumbnail
        }
    }
}
```
No `prepareForReuse()` reset and conditional configuration — a recycled cell that previously showed a custom image keeps showing it when the new item's `hasCustomImage` is `false`. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — UICollectionView.CellRegistration](https://developer.apple.com/documentation/uikit/uicollectionview/cellregistration)
-   [Apple Developer — register(_:forCellReuseIdentifier:)](https://developer.apple.com/documentation/uikit/uitableview/register(_:forcellreuseidentifier:)-3l3ct)
-   [Apple Developer — prepareForReuse()](https://developer.apple.com/documentation/uikit/uitableviewcell/prepareforreuse())
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/cell-configuration.md --type knowledge`
Expected: `PASS: knowledge/uikit/cell-configuration.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/cell-configuration.md
git commit -m "docs: add uikit cell-configuration knowledge contract"
```

---

## Task 13: Knowledge Contract — `modal-presentation`

**Files:**
- Create: `knowledge/uikit/modal-presentation.md`

- [ ] **Step 1: Create the file**

```markdown
# Modal Presentation

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.modal-presentation
type: knowledge
title: Modal Presentation
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of present(_:animated:completion:), dismiss(animated:completion:), and UIModalPresentationStyle to show a screen modally, including sheet-style presentation.
domain: UIKit
tags:
  - uikit
  - presentation
  - modal
references:
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/present(_:animated:completion:)
  - https://developer.apple.com/documentation/uikit/uiviewcontroller/dismiss(animated:completion:)
  - https://developer.apple.com/documentation/uikit/uimodalpresentationstyle
depends_on: []
related:
  - knowledge.uikit.navigation-controller
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent presents a screen modally
with `present(_:animated:completion:)`/`dismiss(animated:completion:)`
and an explicit `UIModalPresentationStyle`, for content that interrupts
the current flow rather than continuing it.

## Scope

### Included

-   `present(_:animated:completion:)` / `dismiss(animated:completion:)`
-   `UIModalPresentationStyle` selection (`.pageSheet`/`.formSheet`/`.fullScreen`, etc.)
-   Who calls dismiss (presenting vs. presented view controller)

### Excluded

-   Push/pop stack navigation — see `navigation-controller`

## Rules

### Rule 1

Agents MUST present a screen modally (`present(_:animated:completion:)`)
rather than pushing it, when the content is a self-contained task that
interrupts the current flow and has its own explicit completion (a
compose sheet, a settings flow, an onboarding step) — modal presentation
communicates "this is a separate task," matching the system's own use of
modals.

### Rule 2

Agents MUST set an explicit `modalPresentationStyle` on the presented
view controller rather than relying on the default — the default is
`.automatic`, which resolves to `.pageSheet` in most contexts; if the
design calls for `.fullScreen` (a sheet that must not be dismissed by a
downward swipe mid-task), it must be set explicitly.

### Rule 3

Agents MUST call `dismiss(animated:completion:)` on the *presenting*
view controller, or use `self.dismiss` from the presented one (which
forwards to its presenter) — dismissing is a paired operation with
`present`; calling it on an unrelated view controller in the hierarchy
has no effect.

### Rule 4

Agents SHOULD pass a completion handler to `dismiss(animated:completion:)`
for any work that must happen strictly after the dismissal animation
finishes (presenting a second modal, showing a toast) — starting that
work immediately after calling `dismiss` without the completion handler
races the still-running dismissal animation.

## Compliant Example

```swift
final class InboxViewController: UIViewController {
    func showCompose() {
        let composeVC = ComposeViewController()
        composeVC.modalPresentationStyle = .pageSheet
        present(composeVC, animated: true)
    }
}

final class ComposeViewController: UIViewController {
    func send() {
        submitDraft()
        presentingViewController?.dismiss(animated: true) {
            // safe to present another modal here
        }
    }
}
```
Explicit `.pageSheet` style, dismissal via the presenting controller with a completion handler. (Rules 2, 3, 4)

## Non-Compliant Example

```swift
final class ComposeViewController: UIViewController {
    func send() {
        submitDraft()
        navigationController?.popViewController(animated: true)
    }
}
```
A modally presented screen is torn down with `popViewController` instead of `dismiss` — since it was never pushed, this has no effect and the modal stays on screen. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — present(_:animated:completion:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/present(_:animated:completion:))
-   [Apple Developer — dismiss(animated:completion:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/dismiss(animated:completion:))
-   [Apple Developer — UIModalPresentationStyle](https://developer.apple.com/documentation/uikit/uimodalpresentationstyle)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/uikit/modal-presentation.md --type knowledge`
Expected: `PASS: knowledge/uikit/modal-presentation.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/uikit/modal-presentation.md
git commit -m "docs: add uikit modal-presentation knowledge contract"
```

---

## Task 14: Native Skill — `skills/uikit/SKILL.md`

**Files:**
- Create: `skills/uikit/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: uikit
description: Route UIKit screen-scaffolding implementation tasks to the correct Knowledge Contracts — view controller lifecycle and composition, programmatic Auto Layout (constraints, stack views, safe area), navigation (UINavigationController, UITabBarController, modal presentation), and diffable table/collection views. Use when writing or reviewing UIKit screens, layout code, navigation flow, or list/grid UI. v1 is programmatic UI only (no Storyboard/XIB) and diffable data sources only (no classic cellForRowAt). Accessibility API implementation is out of scope here — see the accessibility skill. Triggers on UIViewController, viewDidLoad, viewWillAppear, addChild, NSLayoutConstraint, layout anchors, UIStackView, safeAreaLayoutGuide, UINavigationController, UITabBarController, UITableViewDiffableDataSource, UICollectionViewCompositionalLayout, UICollectionViewDiffableDataSource, CellRegistration, prepareForReuse, present, dismiss, UIModalPresentationStyle.
id: skill.uikit.foundations
title: UIKit — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: UIKit
routes: [knowledge.uikit.view-controller-lifecycle, knowledge.uikit.view-controller-composition, knowledge.uikit.auto-layout-constraints, knowledge.uikit.auto-layout-stack-views, knowledge.uikit.safe-area-and-layout-guides, knowledge.uikit.navigation-controller, knowledge.uikit.tab-bar-controller, knowledge.uikit.table-view-diffable, knowledge.uikit.collection-view-compositional-layout, knowledge.uikit.collection-view-diffable, knowledge.uikit.cell-configuration, knowledge.uikit.modal-presentation]
related:
  - skill.accessibility.foundations
  - skill.swiftui.foundations
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-01
---

# UIKit — Foundations Skill

## Purpose

Route UIKit screen-scaffolding implementation tasks to the minimum
required UIKit Knowledge Contracts. v1 scope is programmatic UI only (no
Storyboard/XIB) and diffable data sources only (no classic
`cellForRowAt`).

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/uikit/.

-   Screen lifecycle & composition -> view-controller-lifecycle.md, view-controller-composition.md
-   Layout -> auto-layout-constraints.md, auto-layout-stack-views.md, safe-area-and-layout-guides.md
-   Navigation & presentation -> navigation-controller.md, tab-bar-controller.md, modal-presentation.md
-   Lists & grids -> table-view-diffable.md, collection-view-compositional-layout.md, collection-view-diffable.md, cell-configuration.md

Never load more than the contracts relevant to the specific question.
For accessibility API tasks (accessibilityLabel, traits, VoiceOver,
Dynamic Type, etc.), route to `skill.accessibility.foundations` instead.
For SwiftUI view/state/navigation tasks, route to
`skill.swiftui.foundations` instead. For design-level guidance (when to
use a tab bar vs. a navigation stack, list vs. grid layout choice), route
to `skill.human-interface-guidelines.foundations` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/uikit/ — do not guess or fall back to general
knowledge. Storyboard/XIB and `IBOutlet`/`IBAction` workflow are
permanently out of scope for this domain. Gesture recognizers, Core
Animation/CALayer, custom transitions, and UIKit-SwiftUI interop
(`UIHostingController`/`UIViewRepresentable`) are deferred to future
scope, not yet built — report that explicitly rather than answering from
general knowledge (see docs/architecture/domain-map.md).
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/uikit/SKILL.md --type skill`
Expected: `PASS: skills/uikit/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/uikit/SKILL.md
git commit -m "feat: add uikit native skill"
```

---

## Task 15: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`accessibility` row (the row containing `skills/accessibility/SKILL.md`):

```markdown
| UIKit, UIViewController, viewDidLoad, viewWillAppear, addChild, NSLayoutConstraint, layout anchors, UIStackView, safeAreaLayoutGuide, UINavigationController, UITabBarController, UITableViewDiffableDataSource, UICollectionViewCompositionalLayout, UICollectionViewDiffableDataSource, CellRegistration, prepareForReuse, present, dismiss, UIModalPresentationStyle | skills/uikit/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `7` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui, accessibility, uikit)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add uikit to skills index"
```

---

## Task 16: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `uikit` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| UIKit | uikit | UIKit components | UIKit component implementation conventions |
```

Replace with:

```markdown
| UIKit | uikit | Programmatic screen-scaffolding v1: view controller lifecycle and composition, Auto Layout (constraints, stack views, safe area), navigation (UINavigationController, UITabBarController, modal presentation), diffable table/collection views. No Storyboard/XIB, no classic data source pattern. Accessibility APIs owned by `accessibility` — see Cross-Domain Notes. | UIKit programmatic screen-scaffolding implementation conventions (view controllers, Auto Layout, navigation, diffable lists/grids) |
```

- [ ] **Step 2: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt).
```

- [ ] **Step 3: Add three new Cross-Domain Notes entries**

Find this exact line (the last bullet in `## Cross-Domain Notes`):

```markdown
- `accessibility` (`accessibility-audits-testing` topic) and the future `testing` domain (Tier 2, unbuilt) overlap: this domain's angle is accessibility-specific audit APIs (`performAccessibilityAudit`, Accessibility Inspector), `testing`'s future angle is general XCTest/Swift Testing/UI-testing conventions. Boundary not yet resolved — decide when `testing` is built.
```

Replace with (adds three new bullets after it):

```markdown
- `accessibility` (`accessibility-audits-testing` topic) and the future `testing` domain (Tier 2, unbuilt) overlap: this domain's angle is accessibility-specific audit APIs (`performAccessibilityAudit`, Accessibility Inspector), `testing`'s future angle is general XCTest/Swift Testing/UI-testing conventions. Boundary not yet resolved — decide when `testing` is built.
- `uikit` and `accessibility` overlap: `accessibility` owns all UIKit accessibility API implementation (labels, traits, value/hint, custom actions, element grouping/order, Dynamic Type, reduce-motion/transparency, focus, hidden/decorative, audits) across both SwiftUI and UIKit; `uikit` owns non-accessibility screen-scaffolding APIs (lifecycle, layout, navigation, lists/grids). Resolved via angle-split — `uikit` KCs cross-reference `accessibility` KCs via `related:` rather than restating Rules.
- `uikit` and `swiftui` overlap: both cover screen-building but on separate API surfaces (imperative vs. declarative); neither depends on the other for v1. The interop boundary (`UIHostingController`/`UIViewRepresentable`) is future scope for whichever domain builds it — not yet assigned.
- `uikit` and `human-interface-guidelines` overlap: HIG owns design guidance (when to use a tab bar vs. navigation stack, list vs. grid layout choice, modal vs. push presentation), `uikit` owns API implementation (the *how*). Same angle-split pattern as `accessibility` vs. `human-interface-guidelines`.
```

- [ ] **Step 4: Validate manually**

Run: `grep -c "uikit" docs/architecture/domain-map.md`
Expected: a number greater than 2 (the file already mentions "uikit" at least twice before this task — the Tier 1 row and the artifact-layout example — the updated row, Completed line, and three new Cross-Domain Notes entries push the count well above that baseline)

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope uikit v1, add uikit cross-domain notes"
```

---

## Task 17: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `accessibility` bullet, immediately before the `Full routing tables:` line):

```markdown
- **`accessibility`** — Routes Accessibility API implementation tasks (labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion/Transparency/Increase Contrast, Full Keyboard Access, hidden/decorative elements, accessibility audits) to Accessibility Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this icon-only button has no VoiceOver label"` → `accessibility-labels.md`
  Example: `"swipe-to-delete row needs a VoiceOver alternative"` → `custom-accessibility-actions.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`accessibility`** — Routes Accessibility API implementation tasks (labels, traits, value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, Reduce Motion/Transparency/Increase Contrast, Full Keyboard Access, hidden/decorative elements, accessibility audits) to Accessibility Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this icon-only button has no VoiceOver label"` → `accessibility-labels.md`
  Example: `"swipe-to-delete row needs a VoiceOver alternative"` → `custom-accessibility-actions.md`

- **`uikit`** — Routes UIKit screen-scaffolding implementation tasks (view controller lifecycle/composition, programmatic Auto Layout, navigation, diffable table/collection views, modal presentation) to UIKit Knowledge Contracts.
  Example: `"my child view controller's view isn't showing up correctly"` → `view-controller-composition.md`
  Example: `"how do I animate row insertion in a UITableView"` → `table-view-diffable.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a new What's New line**

Find this exact line (the first/topmost line in `## What's New`):

```markdown
- 2026-08-01 — Added `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contracts. Resolves the human-interface-guidelines and swiftui accessibility forward-references.
```

Replace with (adds a new topmost line before it):

```markdown
- 2026-08-01 — Added `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation; programmatic UI v1) — 12 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contracts. Resolves the human-interface-guidelines and swiftui accessibility forward-references.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "uikit" README.md`
Expected: a number greater than 0 (the new `uikit` Skills bullet and What's New line are the first mentions of "uikit" in this file)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add uikit to README Skills + What's New"
```

---

## Task 18: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/uikit.md --type reference
python3 scripts/validate_artifact.py skills/uikit/SKILL.md --type skill
for f in knowledge/uikit/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
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

Use `superpowers:code-reviewer` on the entire `uikit` domain (all 14 new
files plus the 3 modified docs) to check cross-file consistency: every
`related:` KC id resolves to a real file (including the cross-domain
`knowledge.accessibility.accessibility-labels` reference in
`cell-configuration.md`), the Skill's `routes:` list matches exactly the
12 KC ids, the Reference's "Used By" list matches exactly the 12 KC
files, layer order (References → Knowledge → Skills) is respected, the
three new Cross-Domain Notes entries read correctly, the
`table-view-diffable`/`collection-view-diffable`+
`collection-view-compositional-layout` structure-vs-data split is
internally consistent (same pattern as `accessibility-element-grouping`/
`voiceover-navigation-order`), no v1 scope violations (no Storyboard/XIB,
no classic data source pattern, no accessibility API rules, no gesture/
Core Animation/interop content), and each commit is one artifact per the
established history pattern. Also live-verify (WebFetch/curl) every cited
Apple documentation URL returns HTTP 200 — established practice after the
`accessibility` domain review caught a broken link and a fabricated
symbol name.
