# SwiftUI — Gestures & Animation Domain Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing `swiftui` domain with 10 Animation/Gestures Knowledge Contracts, closing the "animation, gestures... remain unbuilt" gap named in `docs/architecture/domain-map.md`.

**Architecture:** 10 new Knowledge Contracts land in the existing `knowledge/swiftui/` directory. The Reference (`references/apple/swiftui.md`) stays a single file, extended in place. The routing layer splits in two — the existing `skills/swiftui/SKILL.md` keeps Foundations routing, a new `skills/swiftui-interaction/SKILL.md` (`id: skill.swiftui.interaction`) owns Animation/Gestures routing — because adding 10 routing lines to the existing 47-line Skill would exceed the project's size conventions.

**Tech Stack:** Markdown Knowledge Contracts/Skills/References per this repo's artifact format (`scripts/validate_artifact.py`). No application code — this is documentation-as-data for an AI coding agent. All API facts below were verified against Apple's live documentation JSON API (`developer.apple.com/tutorials/data/documentation/swiftui/...`) during planning, not from general knowledge alone — version numbers and deprecation notices are doc-confirmed.

**Branch:** `feature/swiftui-gestures-animation-domain` off `main`.

---

## Before Starting

```bash
cd "/Users/caglarbaranbora/vault/Apple Agent Kit"
git checkout main
git pull
git checkout -b feature/swiftui-gestures-animation-domain
```

---

### Task 1: Extend the SwiftUI Reference

**Files:**
- Modify: `references/apple/swiftui.md`

- [ ] **Step 1: Replace the file with the extended version**

Replace the entire contents of `references/apple/swiftui.md` with:

```markdown
# SwiftUI

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/swiftui

## Purpose

Reference index for Apple's SwiftUI framework documentation,
implementation-conventions scope (Views, Navigation, Layout, State
management, Animation, Gestures), targeting iOS 17+ APIs. Visual/UX
design guidance for what a screen should look like is owned by
`human-interface-guidelines`, not this domain — see
docs/architecture/domain-map.md Cross-Domain Notes. Previews and custom
`Layout` protocol conformances are out of scope for this pass.

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
- Implicit/explicit animation and timing curves
- View transitions
- matchedGeometryEffect
- The Animatable protocol
- PhaseAnimator and KeyframeAnimator
- Tap and long-press gestures
- Drag gesture
- Magnification and rotation gestures
- Gesture composition
- GestureState

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
- knowledge/swiftui/animation-modifiers.md ([[knowledge/swiftui/animation-modifiers]])
- knowledge/swiftui/transitions.md ([[knowledge/swiftui/transitions]])
- knowledge/swiftui/matched-geometry-effect.md ([[knowledge/swiftui/matched-geometry-effect]])
- knowledge/swiftui/animatable-values.md ([[knowledge/swiftui/animatable-values]])
- knowledge/swiftui/phase-and-keyframe-animators.md ([[knowledge/swiftui/phase-and-keyframe-animators]])
- knowledge/swiftui/tap-and-long-press-gestures.md ([[knowledge/swiftui/tap-and-long-press-gestures]])
- knowledge/swiftui/drag-gesture.md ([[knowledge/swiftui/drag-gesture]])
- knowledge/swiftui/magnification-and-rotation-gestures.md ([[knowledge/swiftui/magnification-and-rotation-gestures]])
- knowledge/swiftui/gesture-composition.md ([[knowledge/swiftui/gesture-composition]])
- knowledge/swiftui/gesture-state.md ([[knowledge/swiftui/gesture-state]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/swiftui.md --type reference`
Expected: `PASS: references/apple/swiftui.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/swiftui.md
git commit -m "docs: extend swiftui reference with animation/gestures topics"
```

---

### Task 2: Create Knowledge Contract — animation-modifiers

**Files:**
- Create: `knowledge/swiftui/animation-modifiers.md`

- [ ] **Step 1: Write the file**

```markdown
# Animation Modifiers

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.animation-modifiers
type: knowledge
title: Animation Modifiers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of implicit (.animation(_:value:)) and explicit (withAnimation) animation triggers, standard timing curves, and the iOS 17+ completion-callback overload.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/view/animation(_:value:)
  - https://developer.apple.com/documentation/swiftui/withanimation(_:_:)
  - https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:)
depends_on: []
related:
  - knowledge.swiftui.transitions
  - knowledge.human-interface-guidelines.motion
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent triggers SwiftUI
animations correctly: scoping implicit animation to a specific value,
wrapping synchronous state changes in `withAnimation`, choosing timing
curves, and detecting animation completion without a guessed-duration
workaround.

## Scope

### Included

-   `.animation(_:value:)` value-scoped implicit animation
-   `withAnimation(_:_:)` explicit animation of synchronous state changes
-   Standard `Animation` timing curves (`.easeInOut`, `.linear`,
    `.spring(response:dampingFraction:blendDuration:)`, convenience
    spring presets)
-   The iOS 17+ `withAnimation(_:completionCriteria:_:completion:)`
    completion-callback overload

### Excluded

-   View insertion/removal transition animation — see `transitions.md`
-   Per-frame custom interpolation for custom shapes/views — see
    `animatable-values.md`
-   Multi-phase or keyframe-timeline animation — see
    `phase-and-keyframe-animators.md`
-   Design-level guidance on when/why to animate — see
    `knowledge.human-interface-guidelines.motion`

## Rules

### Rule 1

Agents MUST NOT use the deprecated `.animation(_:)` modifier (the
overload with no `value:` parameter). Apple deprecated it because it
animates on any upstream state change that touches the view, producing
unpredictable results — use `.animation(_:value:)` scoped to a specific
`Equatable` value, or `withAnimation` around the state mutation.

### Rule 2

Agents MUST scope `.animation(_:value:)` to the exact value whose
change should animate, not an unrelated or overly broad value.

### Rule 3

Agents MUST perform the state mutation to be animated synchronously
inside the `withAnimation` closure — a mutation made after an `await`
inside that closure does not animate.

### Rule 4

Agents SHOULD trigger a `withAnimation` call at the single call site
that changes state, rather than scattering `.animation(_:value:)`
modifiers across multiple views when several properties must animate
together as one transaction.

### Rule 5

Agents MUST use the iOS 17+ `withAnimation(_:completionCriteria:_:completion:)`
overload to run code after an animation completes. Agents MUST NOT use
`DispatchQueue.main.asyncAfter` with a guessed duration to approximate
animation completion.

### Rule 6

Agents SHOULD choose `.logicallyComplete` completion criteria for a
callback that should fire once the animation's target state is
reached (e.g., re-enabling a button), and reserve `.removed` for cases
that must wait until the animation has fully finished rendering.

## Compliant Example

```swift
struct ExpandableCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("Card")
            if isExpanded {
                Text("Extra detail")
            }
        }
        .animation(.easeInOut, value: isExpanded)
        .onTapGesture {
            withAnimation(.spring(response: 0.4, dampingFraction: 0.8), completionCriteria: .logicallyComplete) {
                isExpanded.toggle()
            } completion: {
                print("Card animation reached its target state")
            }
        }
    }
}
```
Value-scoped `.animation(_:value:)`, explicit `withAnimation` with the
iOS 17+ completion callback. (Rules 1, 2, 5, 6)

## Non-Compliant Example

```swift
struct ExpandableCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("Card")
            if isExpanded {
                Text("Extra detail")
            }
        }
        .animation(.easeInOut) // deprecated overload, no value:
        .onTapGesture {
            isExpanded.toggle()
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                print("guessed the animation is probably done")
            }
        }
    }
}
```
Deprecated no-value `.animation(_:)` and a guessed-duration completion
workaround instead of the completion callback. (Rules 1, 5)

## Dependencies

None.

## References

-   [Apple Developer — animation(_:value:)](https://developer.apple.com/documentation/swiftui/view/animation(_:value:))
-   [Apple Developer — withAnimation(_:_:)](https://developer.apple.com/documentation/swiftui/withanimation(_:_:))
-   [Apple Developer — withAnimation(_:completionCriteria:_:completion:)](https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/animation-modifiers.md --type knowledge`
Expected: `PASS: knowledge/swiftui/animation-modifiers.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/animation-modifiers.md
git commit -m "docs: add swiftui animation-modifiers knowledge contract"
```

---

### Task 3: Create Knowledge Contract — transitions

**Files:**
- Create: `knowledge/swiftui/transitions.md`

- [ ] **Step 1: Write the file**

```markdown
# Transitions

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.transitions
type: knowledge
title: Transitions
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of AnyTransition and .transition(_:) for view insertion/removal animation tied to view-identity changes.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/view/transition(_:)
  - https://developer.apple.com/documentation/swiftui/anytransition
depends_on: []
related:
  - knowledge.swiftui.animation-modifiers
  - knowledge.swiftui.view-identity
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent animates a view's
insertion into or removal from the hierarchy using `AnyTransition` and
`.transition(_:)`, and the common mistake of applying a transition
without an animation to trigger it.

## Scope

### Included

-   `.transition(_:)` modifier
-   `AnyTransition` statics: `.opacity`, `.slide`, `.move(edge:)`,
    `.scale`, `.asymmetric(insertion:removal:)`, `.combined(with:)`
-   Pairing a transition with `withAnimation`/`.animation(_:value:)`
    and a view-identity change (`if` branch, `ForEach` membership)

### Excluded

-   Shared-element transitions between two co-present views — see
    `matched-geometry-effect.md`
-   Custom per-frame interpolation — see `animatable-values.md`

## Rules

### Rule 1

Agents MUST pair `.transition(_:)` with a `withAnimation` call (or an
ancestor `.animation(_:value:)`) around the state change that inserts
or removes the view. `.transition` only declares how a view animates
in/out — it does not itself trigger the animation.

### Rule 2

Agents MUST apply `.transition(_:)` to a view whose presence in the
hierarchy is conditionally toggled (an `if` branch, or `ForEach`
membership changing) — applying it to a view that never leaves the
hierarchy has no visible effect.

### Rule 3

Agents SHOULD use `.asymmetric(insertion:removal:)` when the visual
effect for appearing should differ from disappearing (e.g., slide in
from an edge, fade out in place).

### Rule 4

Agents SHOULD use `.combined(with:)` to layer multiple transitions
(e.g., `.opacity.combined(with: .scale)`) rather than adding extra
wrapper views to fake a combined effect.

### Rule 5

Agents MUST NOT rely on `.transition(_:)` to animate a view that
remains present in the hierarchy but changes an internal property
(position, size, color) without an identity change — use
`.animation(_:value:)`/`withAnimation` directly on that property
instead.

## Compliant Example

```swift
struct ToastView: View {
    @State private var showToast = false

    var body: some View {
        VStack {
            Button("Show") {
                withAnimation(.easeInOut) {
                    showToast = true
                }
            }
            if showToast {
                Text("Saved")
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
    }
}
```
`.transition` paired with `withAnimation`, applied to a conditionally
present view, combining two transitions. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
struct ToastView: View {
    @State private var showToast = false

    var body: some View {
        VStack {
            Button("Show") {
                showToast = true // no withAnimation
            }
            if showToast {
                Text("Saved")
                    .transition(.opacity)
            }
        }
    }
}
```
Transition declared but the state change isn't wrapped in
`withAnimation`, so the toast appears instantly instead of fading in.
(Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — transition(_:)](https://developer.apple.com/documentation/swiftui/view/transition(_:))
-   [Apple Developer — AnyTransition](https://developer.apple.com/documentation/swiftui/anytransition)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/transitions.md --type knowledge`
Expected: `PASS: knowledge/swiftui/transitions.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/transitions.md
git commit -m "docs: add swiftui transitions knowledge contract"
```

---

### Task 4: Create Knowledge Contract — matched-geometry-effect

**Files:**
- Create: `knowledge/swiftui/matched-geometry-effect.md`

- [ ] **Step 1: Write the file**

```markdown
# Matched Geometry Effect

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.matched-geometry-effect
type: knowledge
title: Matched Geometry Effect
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of matchedGeometryEffect and @Namespace for shared-element transitions between two co-present views.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)
  - https://developer.apple.com/documentation/swiftui/namespace
depends_on: []
related:
  - knowledge.swiftui.transitions
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent builds shared-element
("hero") transitions with `matchedGeometryEffect`, including the
`@Namespace` requirement and the exactly-one-source rule.

## Scope

### Included

-   `matchedGeometryEffect(id:in:properties:anchor:isSource:)` signature
    and usage
-   `@Namespace` / `Namespace.ID` requirement
-   The exactly-one-`isSource: true`-per-id rule
-   Co-presence requirement (both linked views present during the
    transaction)

### Excluded

-   Transitions without shared geometry (`AnyTransition`-only) — see
    `transitions.md`

## Rules

### Rule 1

Agents MUST declare a `@Namespace private var` and pass its `.id`
namespace to every `matchedGeometryEffect(id:in:)` call that should be
visually linked — views declared in different namespaces never match.

### Rule 2

Agents MUST ensure exactly one view with a given `id` has
`isSource: true` at any time the effect is active. Apple's own
documentation states results are undefined if the count of
`isSource: true` views sharing that id is not exactly one.

### Rule 3

Agents MUST keep both the source view (`isSource: true`) and the
non-source view (`isSource: false`) co-present in the hierarchy (for
example, both branches of a `ZStack`) during the animated transaction —
`matchedGeometryEffect` interpolates between two views' frames, it does
not move a single view.

### Rule 4

Agents SHOULD wrap the state change that swaps which id is active in
`withAnimation` — the effect participates in the ambient animation
transaction like any other animatable property.

### Rule 5

Agents SHOULD scope `properties:` to `.position` or `.size` only
(instead of the default `.frame`, which matches both) when just one
dimension should morph, to avoid unwanted stretching.

## Compliant Example

```swift
struct HeroTransition: View {
    @Namespace private var animation
    @State private var isExpanded = false

    var body: some View {
        ZStack {
            if !isExpanded {
                RoundedRectangle(cornerRadius: 12)
                    .matchedGeometryEffect(id: "card", in: animation)
                    .frame(width: 80, height: 80)
            } else {
                RoundedRectangle(cornerRadius: 0)
                    .matchedGeometryEffect(id: "card", in: animation)
                    .frame(width: 300, height: 300)
            }
        }
        .onTapGesture {
            withAnimation(.spring()) {
                isExpanded.toggle()
            }
        }
    }
}
```
Single namespace, one matched id, exactly one view present per state
(the two branches never coexist, so `isSource` defaults correctly),
wrapped in `withAnimation`. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
struct BrokenHeroTransition: View {
    @Namespace private var animationA
    @Namespace private var animationB // second, unrelated namespace

    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: 12)
                .matchedGeometryEffect(id: "card", in: animationA)
            RoundedRectangle(cornerRadius: 12)
                .matchedGeometryEffect(id: "card", in: animationB) // never matches
        }
    }
}
```
Two views share the same `id` but live in different namespaces, so
they never link. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — matchedGeometryEffect(id:in:properties:anchor:isSource:)](https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:))
-   [Apple Developer — Namespace](https://developer.apple.com/documentation/swiftui/namespace)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/matched-geometry-effect.md --type knowledge`
Expected: `PASS: knowledge/swiftui/matched-geometry-effect.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/matched-geometry-effect.md
git commit -m "docs: add swiftui matched-geometry-effect knowledge contract"
```

---

### Task 5: Create Knowledge Contract — animatable-values

**Files:**
- Create: `knowledge/swiftui/animatable-values.md`

- [ ] **Step 1: Write the file**

```markdown
# Animatable Values

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.animatable-values
type: knowledge
title: Animatable Values
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when and how to conform a custom Shape or View to Animatable using animatableData and AnimatablePair for per-frame interpolation.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/animatable
  - https://developer.apple.com/documentation/swiftui/animatablepair
depends_on: []
related:
  - knowledge.swiftui.animation-modifiers
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should conform a custom
`Shape` or `View` to `Animatable`, and how to combine multiple
animatable properties with `AnimatablePair`, as distinct from relying
on the built-in `.animation(_:value:)` engine.

## Scope

### Included

-   The `Animatable` protocol and `animatableData` requirement
-   `AnimatablePair` for combining two (or, nested, more) animatable
    values
-   When custom interpolation is needed vs. when a built-in modifier
    already handles it

### Excluded

-   Triggering built-in animatable modifiers (`.offset`, `.scaleEffect`,
    `.animation(_:value:)`) — see `animation-modifiers.md`
-   Multi-phase/keyframe animation — see `phase-and-keyframe-animators.md`

## Rules

### Rule 1

Agents MUST conform a custom `Shape` or `View` to `Animatable`
(implementing `animatableData`) when it needs SwiftUI to interpolate a
custom internal parameter (a corner radius, a progress fraction, a
path-defining value) frame-by-frame during an animation — a plain
stored property is not interpolated on its own.

### Rule 2

Agents MUST back `animatableData` with a type that conforms to
`VectorArithmetic` — a custom struct without arithmetic operations
cannot be interpolated.

### Rule 3

Agents MUST use `AnimatablePair` (nesting `AnimatablePair<A, AnimatablePair<B, C>>`
for three or more values) to combine multiple independently animatable
properties into a single `animatableData` value when they must move
together as one visual change. Agents MUST NOT animate each such
property with a separate, unsynchronized `.animation(_:value:)` when
the effect depends on them changing in lockstep.

### Rule 4

Agents MUST NOT reach for a custom `Animatable` conformance to animate
a value that a built-in modifier (`.animation(_:value:)`, `.offset`,
`.scaleEffect`) already animates correctly — custom conformance is
only for custom-drawn `Shape`/`View` internals that SwiftUI has no
built-in animatable property for.

## Compliant Example

```swift
struct ProgressArc: Shape {
    var progress: Double // 0...1

    var animatableData: Double {
        get { progress }
        set { progress = newValue }
    }

    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.addArc(
            center: CGPoint(x: rect.midX, y: rect.midY),
            radius: rect.width / 2,
            startAngle: .degrees(-90),
            endAngle: .degrees(-90 + 360 * progress),
            clockwise: false
        )
        return path
    }
}
```
Custom `Shape` conforms to `Animatable` via `animatableData` so
`.animation(.linear, value: progress)` applied by a caller interpolates
the arc frame-by-frame. (Rules 1, 2)

## Non-Compliant Example

```swift
struct ProgressArc: Shape {
    var progress: Double // 0...1, not Animatable

    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.addArc(
            center: CGPoint(x: rect.midX, y: rect.midY),
            radius: rect.width / 2,
            startAngle: .degrees(-90),
            endAngle: .degrees(-90 + 360 * progress),
            clockwise: false
        )
        return path
    }
}
```
No `Animatable` conformance — wrapping this shape in
`.animation(_:value:)` snaps instantly between progress values instead
of interpolating, since SwiftUI has no per-frame value to read. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — Animatable](https://developer.apple.com/documentation/swiftui/animatable)
-   [Apple Developer — AnimatablePair](https://developer.apple.com/documentation/swiftui/animatablepair)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/animatable-values.md --type knowledge`
Expected: `PASS: knowledge/swiftui/animatable-values.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/animatable-values.md
git commit -m "docs: add swiftui animatable-values knowledge contract"
```

---

### Task 6: Create Knowledge Contract — phase-and-keyframe-animators

**Files:**
- Create: `knowledge/swiftui/phase-and-keyframe-animators.md`

- [ ] **Step 1: Write the file**

```markdown
# Phase and Keyframe Animators

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.phase-and-keyframe-animators
type: knowledge
title: Phase and Keyframe Animators
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when to use iOS 17+ PhaseAnimator for discrete repeating/triggered phase cycling versus KeyframeAnimator for independent per-property animation timelines.
domain: SwiftUI
tags:
  - swiftui
  - animation
references:
  - https://developer.apple.com/documentation/swiftui/phaseanimator
  - https://developer.apple.com/documentation/swiftui/keyframeanimator
depends_on: []
related:
  - knowledge.swiftui.animation-modifiers
updated: 2026-08-06
```

## Intent

This contract defines when an AI coding agent should use `PhaseAnimator`
versus `KeyframeAnimator` (both iOS 17+) instead of chaining multiple
`withAnimation` calls or using a manual `Timer`, for multi-step or
timeline-based animation.

## Scope

### Included

-   `PhaseAnimator` — discrete phase cycling, repeating or
    `trigger`-replayed
-   `KeyframeAnimator` — independent per-property timelines
    (`KeyframeTrack`, `LinearKeyframe`, `CubicKeyframe`,
    `SpringKeyframe`, `MoveKeyframe`)
-   Choosing between `PhaseAnimator`, `KeyframeAnimator`, and plain
    `withAnimation`

### Excluded

-   Single state-change animation — see `animation-modifiers.md`
-   View insertion/removal transitions — see `transitions.md`

## Rules

### Rule 1

Agents MUST use `PhaseAnimator` (not a manual `Timer` or a recursive
chain of `withAnimation` calls) when a view needs to cycle through a
fixed sequence of discrete visual phases, either continuously repeating
or replayed once when a `trigger` value changes.

### Rule 2

Agents MUST use `KeyframeAnimator` (not multiple staggered
`withAnimation` calls) when independent properties — for example scale
and rotation — need their own timing curve on a shared timeline; use a
separate `KeyframeTrack` per property.

### Rule 3

Agents SHOULD avoid expensive work directly inside a `PhaseAnimator`/
`KeyframeAnimator` content closure. Apple's own `KeyframeAnimator`
documentation states the content closure updates every frame while
animating.

### Rule 4

Agents MUST use the iOS 17+ `withAnimation(_:completionCriteria:_:completion:)`
overload (see `animation-modifiers.md`) rather than a fixed-duration
`DispatchQueue.asyncAfter` call when code must run after an animation
external to a `PhaseAnimator`/`KeyframeAnimator` completes.

### Rule 5

Agents SHOULD use the `trigger:` initializer of `PhaseAnimator`/
`KeyframeAnimator` when the phase sequence or keyframe timeline should
play exactly once in response to a specific event (a success
checkmark), and reserve the non-trigger, continuously repeating
initializer for looping effects (a pulsing indicator).

## Compliant Example

```swift
struct SuccessCheckmark: View {
    enum Phase: CaseIterable {
        case initial, popped, settled
    }
    let trigger: Bool

    var body: some View {
        Image(systemName: "checkmark.circle.fill")
            .phaseAnimator(Phase.allCases, trigger: trigger) { content, phase in
                content
                    .scaleEffect(phase == .popped ? 1.3 : 1.0)
            } animation: { phase in
                switch phase {
                case .initial: .default
                case .popped: .spring(response: 0.3, dampingFraction: 0.5)
                case .settled: .easeOut
                }
            }
    }
}
```
`PhaseAnimator` with a `trigger:` initializer plays the pop-and-settle
sequence exactly once per trigger change. (Rules 1, 5)

## Non-Compliant Example

```swift
struct SuccessCheckmark: View {
    @State private var scale: CGFloat = 1.0

    func animateSequence() {
        withAnimation(.spring(response: 0.3, dampingFraction: 0.5)) {
            scale = 1.3
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            withAnimation(.easeOut) {
                self.scale = 1.0
            }
        }
    }

    var body: some View {
        Image(systemName: "checkmark.circle.fill")
            .scaleEffect(scale)
            .onAppear { animateSequence() }
    }
}
```
Manually chained `withAnimation` calls glued together with a guessed
`DispatchQueue.asyncAfter` delay instead of `PhaseAnimator`. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — PhaseAnimator](https://developer.apple.com/documentation/swiftui/phaseanimator)
-   [Apple Developer — KeyframeAnimator](https://developer.apple.com/documentation/swiftui/keyframeanimator)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/phase-and-keyframe-animators.md --type knowledge`
Expected: `PASS: knowledge/swiftui/phase-and-keyframe-animators.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/phase-and-keyframe-animators.md
git commit -m "docs: add swiftui phase-and-keyframe-animators knowledge contract"
```

---

### Task 7: Create Knowledge Contract — tap-and-long-press-gestures

**Files:**
- Create: `knowledge/swiftui/tap-and-long-press-gestures.md`

- [ ] **Step 1: Write the file**

```markdown
# Tap and Long-Press Gestures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.tap-and-long-press-gestures
type: knowledge
title: Tap and Long-Press Gestures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of TapGesture, LongPressGesture, and their onTapGesture/onLongPressGesture shorthand modifiers, including count and maximumDistance configuration.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/tapgesture
  - https://developer.apple.com/documentation/swiftui/longpressgesture
  - https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:)
  - https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:)
depends_on: []
related:
  - knowledge.swiftui.gesture-composition
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent implements tap and
long-press interactions in SwiftUI using `TapGesture`, `LongPressGesture`,
and their `.onTapGesture`/`.onLongPressGesture` shorthand modifiers.

## Scope

### Included

-   `TapGesture(count:)` and `.onTapGesture(count:perform:)`
-   `LongPressGesture(minimumDuration:maximumDistance:)` and
    `.onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)`

### Excluded

-   Drag, magnification, and rotation gestures — see `drag-gesture.md`,
    `magnification-and-rotation-gestures.md`
-   Composing these gestures with others — see `gesture-composition.md`

## Rules

### Rule 1

Agents MUST use the `.onTapGesture(count:perform:)` shorthand modifier
for a plain tap action on a view, reserving the standalone
`TapGesture(count:)` gesture value for cases where it must be combined
with other gestures via `.simultaneously`/`.sequenced`/`.exclusively`.

### Rule 2

Agents MUST pass `count:` explicitly (default is `1`) when a double- or
multi-tap is required — SwiftUI does not expose a separate configurable
timing window for multi-tap recognition beyond the `count` value.

### Rule 3

Agents MUST set `maximumDistance` on `LongPressGesture`/
`.onLongPressGesture` deliberately, rather than relying on the
10-point default, when the target is a small control. The gesture
fails outright — it does not partial-recognize — if the touch moves
beyond `maximumDistance` before `minimumDuration` elapses.

### Rule 4

Agents MUST NOT assume `onPressingChanged` only fires on a successful
long press. It fires `true` on press-down and `false` on
release/cancel/failure, so success MUST be detected from the `perform`
closure, not from `onPressingChanged` alone.

### Rule 5

Agents SHOULD prefer `.onLongPressGesture` over composing a raw
`LongPressGesture` with `.updating` gesture state when only a simple
press/hold action is needed, not a value derived from the press.

## Compliant Example

```swift
struct DeletableRow: View {
    @State private var isPressed = false

    var body: some View {
        Text("Swipe or hold to delete")
            .onLongPressGesture(
                minimumDuration: 0.5,
                maximumDistance: 20,
                perform: { deleteRow() },
                onPressingChanged: { pressing in isPressed = pressing }
            )
            .onTapGesture(count: 2) { editRow() }
    }

    func deleteRow() {}
    func editRow() {}
}
```
Explicit `maximumDistance`, success handled in `perform` (not
`onPressingChanged`), explicit `count: 2` for double-tap. (Rules 2, 3, 4)

## Non-Compliant Example

```swift
struct DeletableRow: View {
    var body: some View {
        Text("Swipe or hold to delete")
            .onLongPressGesture(
                perform: { deleteRow() },
                onPressingChanged: { pressing in
                    if pressing { deleteRow() } // fires on press-down too, not just success
                }
            )
    }

    func deleteRow() {}
}
```
Treats `onPressingChanged`'s `true` case as success, so the delete
action fires on press-down instead of after the long-press completes.
(Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — TapGesture](https://developer.apple.com/documentation/swiftui/tapgesture)
-   [Apple Developer — LongPressGesture](https://developer.apple.com/documentation/swiftui/longpressgesture)
-   [Apple Developer — onTapGesture(count:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:))
-   [Apple Developer — onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/tap-and-long-press-gestures.md --type knowledge`
Expected: `PASS: knowledge/swiftui/tap-and-long-press-gestures.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/tap-and-long-press-gestures.md
git commit -m "docs: add swiftui tap-and-long-press-gestures knowledge contract"
```

---

### Task 8: Create Knowledge Contract — drag-gesture

**Files:**
- Create: `knowledge/swiftui/drag-gesture.md`

- [ ] **Step 1: Write the file**

```markdown
# Drag Gesture

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.drag-gesture
type: knowledge
title: Drag Gesture
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of DragGesture, its Value properties, and the choice between .updating and .onChanged/.onEnded for handling drag state.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/draggesture
  - https://developer.apple.com/documentation/swiftui/draggesture/value
  - https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:)
depends_on: []
related:
  - knowledge.swiftui.gesture-state
  - knowledge.swiftui.gesture-composition
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent implements drag
interactions with `DragGesture`, including which initializer overload
to use, which `Value` properties to read, and when to use `.updating`
versus `.onChanged`/`.onEnded`.

## Scope

### Included

-   `DragGesture(minimumDistance:coordinateSpace:)`, both the current
    and deprecated initializer overloads
-   `DragGesture.Value` properties: `translation`, `location`,
    `predictedEndLocation`, `startLocation`
-   `.updating($gestureState)` vs. `.onChanged`/`.onEnded`

### Excluded

-   The `@GestureState` property wrapper's general mechanics (this file
    covers drag-specific usage only) — see `gesture-state.md`
-   Composing drag with other gestures — see `gesture-composition.md`

## Rules

### Rule 1

Agents MUST use the current `DragGesture(minimumDistance:coordinateSpace:)`
overload, which takes a `CoordinateSpaceProtocol` (`.local`, `.global`,
`.named(_:)`), for iOS 17+ deployment targets. The older overload
taking a `CoordinateSpace` enum directly is deprecated — its
replacement note reads "Use overload that accepts a
CoordinateSpaceProtocol instead." Agents MUST only use the deprecated
overload when the deployment target is below iOS 17.

### Rule 2

Agents MUST read `translation` for movement relative to where the drag
began, and `location`/`predictedEndLocation` for absolute or projected
positions. Agents MUST NOT compute translation manually from raw touch
deltas.

### Rule 3

Agents MUST use `.updating($gestureState)` with `@GestureState` for
transient drag state that should automatically reset when the drag
ends or is cancelled by the system (for example, an interrupting
system alert).

### Rule 4

Agents MUST use `.onChanged`/`.onEnded` with a plain `@State` when the
value needs to persist after the gesture ends, such as a final
committed offset. `@GestureState` is already reset by the time
`.onEnded` runs, so it cannot be read there to persist a final value.

### Rule 5

Agents SHOULD set `minimumDistance` above `0` on a view that also
recognizes a tap gesture, to avoid the drag gesture eating single-point
taps.

## Compliant Example

```swift
struct DraggableCard: View {
    @GestureState private var dragTranslation: CGSize = .zero
    @State private var committedOffset: CGSize = .zero

    var body: some View {
        Color.blue
            .frame(width: 100, height: 100)
            .offset(x: committedOffset.width + dragTranslation.width,
                    y: committedOffset.height + dragTranslation.height)
            .gesture(
                DragGesture(minimumDistance: 10, coordinateSpace: .local)
                    .updating($dragTranslation) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        committedOffset.width += value.translation.width
                        committedOffset.height += value.translation.height
                    }
            )
    }
}
```
Modern `CoordinateSpaceProtocol` overload, `@GestureState` for
transient translation (auto-resets), plain `@State` commits the final
value in `.onEnded`. (Rules 1, 3, 4)

## Non-Compliant Example

```swift
struct DraggableCard: View {
    @GestureState private var dragTranslation: CGSize = .zero

    var body: some View {
        Color.blue
            .frame(width: 100, height: 100)
            .offset(dragTranslation)
            .gesture(
                DragGesture(minimumDistance: 10, coordinateSpace: .local)
                    .updating($dragTranslation) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        // tries to persist the final offset from @GestureState,
                        // but it has already reset to .zero by the time onEnded runs
                        print("final offset: \(dragTranslation)")
                    }
            )
    }
}
```
Reads `dragTranslation` inside `.onEnded` expecting the in-progress
value, but `@GestureState` has already reset to its initial value —
the card snaps back instead of staying where it was dropped. (Rule 4)

## Dependencies

None.

## References

-   [Apple Developer — DragGesture](https://developer.apple.com/documentation/swiftui/draggesture)
-   [Apple Developer — DragGesture.Value](https://developer.apple.com/documentation/swiftui/draggesture/value)
-   [Apple Developer — Gesture.updating(_:body:)](https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/drag-gesture.md --type knowledge`
Expected: `PASS: knowledge/swiftui/drag-gesture.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/drag-gesture.md
git commit -m "docs: add swiftui drag-gesture knowledge contract"
```

---

### Task 9: Create Knowledge Contract — magnification-and-rotation-gestures

**Files:**
- Create: `knowledge/swiftui/magnification-and-rotation-gestures.md`

- [ ] **Step 1: Write the file**

```markdown
# Magnification and Rotation Gestures

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.magnification-and-rotation-gestures
type: knowledge
title: Magnification and Rotation Gestures
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the iOS 17+ MagnifyGesture and RotateGesture, and when the deprecated MagnificationGesture/RotationGesture are still required.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/magnifygesture
  - https://developer.apple.com/documentation/swiftui/rotategesture
  - https://developer.apple.com/documentation/swiftui/magnificationgesture
  - https://developer.apple.com/documentation/swiftui/rotationgesture
depends_on: []
related:
  - knowledge.swiftui.gesture-composition
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent implements pinch-to-zoom
and rotate interactions using the current `MagnifyGesture`/
`RotateGesture` APIs, and explicitly flags that the older
`MagnificationGesture`/`RotationGesture` types are deprecated.

## Scope

### Included

-   `MagnifyGesture` (`minimumScaleDelta`, `Value.magnification`)
-   `RotateGesture` (`minimumAngleDelta`, `Value.rotation`)
-   The deprecated `MagnificationGesture`/`RotationGesture` as a
    pre-iOS-17 fallback only

### Excluded

-   Drag and tap gestures — see `drag-gesture.md`,
    `tap-and-long-press-gestures.md`
-   Composing these with other gestures — see `gesture-composition.md`

## Rules

### Rule 1

Agents MUST use `MagnifyGesture` (not the deprecated
`MagnificationGesture`) and `RotateGesture` (not the deprecated
`RotationGesture`) for iOS 17+ deployment targets. Apple's
documentation marks both older gesture types deprecated with explicit
replacement notes: "Use MagnifyGesture instead" and "Use RotateGesture
instead."

### Rule 2

Agents MUST only use `MagnificationGesture`/`RotationGesture` when the
deployment target is below iOS 17 — `MagnifyGesture`/`RotateGesture`
require iOS 17+/macOS 14+.

### Rule 3

Agents MUST read pinch scale from `MagnifyGesture.Value.magnification`
and rotation from `RotateGesture.Value.rotation` (an `Angle`). Agents
MUST NOT assume these property names are interchangeable with the
deprecated types' value properties in generically-typed code — the
underlying value container types differ.

### Rule 4

Agents SHOULD set `minimumScaleDelta`/`minimumAngleDelta` above the
default when the view also recognizes a drag or tap gesture, to reduce
accidental multi-gesture conflicts from small incidental finger
movement during a pinch or rotate.

### Rule 5

Agents SHOULD compose `MagnifyGesture` and `RotateGesture` with
`.simultaneously(with:)` (see `gesture-composition.md`) when a view
must support pinch-to-zoom and rotate at the same time, rather than
nesting two separate `.gesture(...)` modifiers.

## Compliant Example

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0
    @State private var angle: Angle = .zero

    var body: some View {
        Image("photo")
            .scaleEffect(scale)
            .rotationEffect(angle)
            .gesture(
                MagnifyGesture()
                    .simultaneously(with: RotateGesture())
                    .onChanged { value in
                        if let magnify = value.first {
                            scale = magnify.magnification
                        }
                        if let rotate = value.second {
                            angle = rotate.rotation
                        }
                    }
            )
    }
}
```
Current `MagnifyGesture`/`RotateGesture` composed with
`.simultaneously(with:)`, reading `.magnification`/`.rotation` from
each gesture's `Value`. (Rules 1, 3, 5)

## Non-Compliant Example

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Image("photo")
            .scaleEffect(scale)
            .gesture(
                MagnificationGesture() // deprecated on iOS 17+ targets
                    .onChanged { value in
                        scale = value
                    }
            )
    }
}
```
Uses the deprecated `MagnificationGesture` on a project targeting
iOS 17+ instead of `MagnifyGesture`. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — MagnifyGesture](https://developer.apple.com/documentation/swiftui/magnifygesture)
-   [Apple Developer — RotateGesture](https://developer.apple.com/documentation/swiftui/rotategesture)
-   [Apple Developer — MagnificationGesture (deprecated)](https://developer.apple.com/documentation/swiftui/magnificationgesture)
-   [Apple Developer — RotationGesture (deprecated)](https://developer.apple.com/documentation/swiftui/rotationgesture)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/magnification-and-rotation-gestures.md --type knowledge`
Expected: `PASS: knowledge/swiftui/magnification-and-rotation-gestures.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/magnification-and-rotation-gestures.md
git commit -m "docs: add swiftui magnification-and-rotation-gestures knowledge contract"
```

---

### Task 10: Create Knowledge Contract — gesture-composition

**Files:**
- Create: `knowledge/swiftui/gesture-composition.md`

- [ ] **Step 1: Write the file**

```markdown
# Gesture Composition

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.gesture-composition
type: knowledge
title: Gesture Composition
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of Gesture.simultaneously/sequenced/exclusively combinators and the .gesture/.highPriorityGesture/.simultaneousGesture view modifier priority semantics.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/gesture/simultaneously(with:)
  - https://developer.apple.com/documentation/swiftui/gesture/sequenced(before:)
  - https://developer.apple.com/documentation/swiftui/gesture/exclusively(before:)
  - https://developer.apple.com/documentation/swiftui/view/gesture(_:including:)
  - https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:)
  - https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:)
depends_on: []
related:
  - knowledge.swiftui.gesture-state
  - knowledge.swiftui.drag-gesture
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent combines multiple
gestures on one view — either two gestures composed into one via
`Gesture` combinators, or a view's own gesture against its children's
gestures via the three priority-differentiated view modifiers.

## Scope

### Included

-   `Gesture.simultaneously(with:)`, `.sequenced(before:)`,
    `.exclusively(before:)`
-   `.gesture(_:)`, `.highPriorityGesture(_:)`, `.simultaneousGesture(_:)`
    view modifiers and their precedence differences

### Excluded

-   The individual gesture types themselves — see the respective
    per-gesture Knowledge Contracts

## Rules

### Rule 1

Agents MUST use `.sequenced(before:)` (not `.simultaneously(with:)`)
when the second gesture should only begin recognizing after the first
gesture succeeds — for example, long-press-then-drag.

### Rule 2

Agents MUST use `.exclusively(before:)` when exactly one of two
gestures should win, with the first-listed gesture taking precedence.
Agents MUST NOT use `.simultaneously(with:)` when both gestures firing
together would produce conflicting behavior.

### Rule 3

Agents MUST choose the correct view modifier for parent/child gesture
conflicts: `.gesture(_:)` gives a view's children's own gestures
higher precedence than this one; `.highPriorityGesture(_:)` gives this
gesture precedence over the view's children's gestures, suppressing
them; `.simultaneousGesture(_:)` lets both this gesture and a child's
own gesture fire together.

### Rule 4

Agents MUST NOT default to `.highPriorityGesture` just to "make a
gesture work" without confirming child views don't also need their own
gesture to fire — it explicitly suppresses child gesture recognition.

### Rule 5

Agents SHOULD compose gestures via the `Gesture` protocol's
`.simultaneously`/`.sequenced`/`.exclusively` combinators into a single
composed gesture passed to one `.gesture(_:)` call, rather than
stacking multiple independent `.gesture(_:)` modifiers on the same
view — independent modifiers do not share recognition state.

## Compliant Example

```swift
struct LongPressThenDragView: View {
    @State private var isReady = false
    @State private var offset: CGSize = .zero

    var body: some View {
        Circle()
            .fill(isReady ? Color.green : Color.gray)
            .frame(width: 60, height: 60)
            .offset(offset)
            .gesture(
                LongPressGesture(minimumDuration: 0.3)
                    .onEnded { _ in isReady = true }
                    .sequenced(before: DragGesture())
                    .onEnded { value in
                        if case .second(true, let drag?) = value {
                            offset = drag.translation
                        }
                        isReady = false
                    }
            )
    }
}
```
`.sequenced(before:)` so the drag only recognizes after the long press
succeeds — a single composed gesture on one `.gesture(_:)` call.
(Rules 1, 5)

## Non-Compliant Example

```swift
struct ButtonWithBackgroundTap: View {
    var body: some View {
        VStack {
            Button("Tap me") { print("button tapped") }
        }
        .highPriorityGesture(
            TapGesture().onEnded { print("background tapped") }
        )
    }
}
```
`.highPriorityGesture` on the container suppresses the `Button`'s own
tap recognition entirely — the button never fires. Should have used
`.simultaneousGesture` (if both should fire) or reconsidered whether a
background tap gesture belongs on a container that also has a
tappable child. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — Gesture.simultaneously(with:)](https://developer.apple.com/documentation/swiftui/gesture/simultaneously(with:))
-   [Apple Developer — Gesture.sequenced(before:)](https://developer.apple.com/documentation/swiftui/gesture/sequenced(before:))
-   [Apple Developer — Gesture.exclusively(before:)](https://developer.apple.com/documentation/swiftui/gesture/exclusively(before:))
-   [Apple Developer — gesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:including:))
-   [Apple Developer — highPriorityGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:))
-   [Apple Developer — simultaneousGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/gesture-composition.md --type knowledge`
Expected: `PASS: knowledge/swiftui/gesture-composition.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/gesture-composition.md
git commit -m "docs: add swiftui gesture-composition knowledge contract"
```

---

### Task 11: Create Knowledge Contract — gesture-state

**Files:**
- Create: `knowledge/swiftui/gesture-state.md`

- [ ] **Step 1: Write the file**

```markdown
# Gesture State

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.gesture-state
type: knowledge
title: Gesture State
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the @GestureState property wrapper and .updating(_:body:), including its automatic reset semantics on gesture end or cancellation.
domain: SwiftUI
tags:
  - swiftui
  - gestures
references:
  - https://developer.apple.com/documentation/swiftui/gesturestate
  - https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:)
depends_on: []
related:
  - knowledge.swiftui.drag-gesture
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent uses `@GestureState` and
`.updating(_:body:)` for transient, gesture-scoped state that
automatically resets — as distinct from a plain `@State` that requires
manual reset logic.

## Scope

### Included

-   `@GestureState` property wrapper declaration
-   `.updating(_:body:)` gesture modifier
-   Automatic reset on gesture end or system cancellation

### Excluded

-   Gesture-specific usage walkthroughs (drag, magnify, rotate) — see
    the respective per-gesture Knowledge Contracts, which use
    `@GestureState` in context

## Rules

### Rule 1

Agents MUST declare transient, gesture-scoped state with
`@GestureState` (not a plain `@State`) when the value should
automatically reset once the gesture ends or is cancelled. Apple's
documentation states it "resets the state to its initial value when
the user or the system ends or cancels the gesture."

### Rule 2

Agents MUST attach a `@GestureState` value to a gesture via
`.updating(_:body:)`, whose `body` closure's first parameter is the
gesture's own `Value` type (for example, `DragGesture.Value`), not the
`GestureState`'s wrapped type. Agents MUST NOT confuse the two when
writing the closure signature.

### Rule 3

Agents MUST copy any `@GestureState` value that must survive past
gesture completion into a separate, persistent `@State` inside the
gesture's `.onEnded` closure before the reset happens. Agents MUST NOT
attempt to read a `@GestureState` value inside `.onEnded` expecting the
in-progress value — it is already reset by then.

### Rule 4

Agents SHOULD prefer `@GestureState` over manually resetting a plain
`@State` in every gesture's `onEnded`/cancellation path, since
`@GestureState` also resets automatically on system-initiated
cancellation (an interrupting alert, for example), which manual
`onEnded`-only reset code does not cover.

## Compliant Example

```swift
struct PressableButton: View {
    @GestureState private var isPressing = false

    var body: some View {
        Text("Hold")
            .padding()
            .background(isPressing ? Color.gray : Color.blue)
            .gesture(
                LongPressGesture(minimumDuration: .infinity)
                    .updating($isPressing) { _, state, _ in
                        state = true
                    }
            )
    }
}
```
`@GestureState` tied to `.updating` — `isPressing` automatically
resets to `false` if the press is released or cancelled, with no
manual reset code. (Rules 1, 4)

## Non-Compliant Example

```swift
struct DraggableCard: View {
    @GestureState private var dragOffset: CGSize = .zero

    var body: some View {
        Color.blue
            .frame(width: 100, height: 100)
            .offset(dragOffset)
            .gesture(
                DragGesture()
                    .updating($dragOffset) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { _ in
                        // dragOffset already reset to .zero here — this print
                        // never shows the dropped position
                        print("dropped at \(dragOffset)")
                    }
            )
    }
}
```
Reads `dragOffset` inside `.onEnded`, but `@GestureState` has already
reset it to `.zero` by the time the closure runs. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — GestureState](https://developer.apple.com/documentation/swiftui/gesturestate)
-   [Apple Developer — Gesture.updating(_:body:)](https://developer.apple.com/documentation/swiftui/gesture/updating(_:body:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/swiftui/gesture-state.md --type knowledge`
Expected: `PASS: knowledge/swiftui/gesture-state.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/swiftui/gesture-state.md
git commit -m "docs: add swiftui gesture-state knowledge contract"
```

---

### Task 12: Create Skill — swiftui-interaction

**Files:**
- Create: `skills/swiftui-interaction/SKILL.md`

- [ ] **Step 1: Write the file**

```markdown
---
name: swiftui-interaction
description: Route SwiftUI Animation and Gesture implementation tasks to the correct Knowledge Contracts — implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, and GestureState. Use when writing or reviewing SwiftUI animation code, building custom transitions, implementing drag/pinch/rotate interactions, or combining multiple gestures on a view. This is implementation-code guidance (iOS 17+), not visual design — for when/why to animate or which gesture to use, see human-interface-guidelines. Triggers on withAnimation, .animation, AnyTransition, matchedGeometryEffect, Animatable, animatableData, PhaseAnimator, KeyframeAnimator, TapGesture, LongPressGesture, DragGesture, MagnifyGesture, RotateGesture, MagnificationGesture, RotationGesture, GestureState, simultaneously, sequenced, exclusively, highPriorityGesture, simultaneousGesture.
id: skill.swiftui.interaction
title: SwiftUI — Interaction (Animation & Gestures)
version: 0.1.0
status: Draft
artifact_type: skill
domain: SwiftUI
routes: [knowledge.swiftui.animation-modifiers, knowledge.swiftui.transitions, knowledge.swiftui.matched-geometry-effect, knowledge.swiftui.animatable-values, knowledge.swiftui.phase-and-keyframe-animators, knowledge.swiftui.tap-and-long-press-gestures, knowledge.swiftui.drag-gesture, knowledge.swiftui.magnification-and-rotation-gestures, knowledge.swiftui.gesture-composition, knowledge.swiftui.gesture-state]
related:
  - skill.swiftui.foundations
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-06
---

# SwiftUI — Interaction Skill

## Purpose

Route SwiftUI Animation and Gesture implementation-code tasks to the
minimum required Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/swiftui/.

-   Animation start/state -> animation-modifiers.md
-   View transitions -> transitions.md, matched-geometry-effect.md
-   Custom animatable values -> animatable-values.md
-   Multi-phase/keyframe animation -> phase-and-keyframe-animators.md
-   Tap/long-press -> tap-and-long-press-gestures.md
-   Drag -> drag-gesture.md
-   Pinch/rotate -> magnification-and-rotation-gestures.md
-   Combining gestures -> gesture-composition.md, gesture-state.md

Never load more than the contracts relevant to the specific question.
For Foundations topics (view/navigation/layout/state), route to
`skill.swiftui.foundations` instead. For visual/UX design questions
(when/why to animate, which gesture to use), route to
`skill.human-interface-guidelines.foundations` or
`skill.human-interface-guidelines.components`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/swiftui/ — do not guess or fall back to general
knowledge. Previews, custom `Layout` protocol conformances, legacy
`ObservableObject`/`NavigationView` migration guidance,
`UIGestureRecognizer`/Core Animation (UIKit), and accessibility APIs
(owned by `accessibility`) are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/swiftui-interaction/SKILL.md --type skill`
Expected: `PASS: skills/swiftui-interaction/SKILL.md`

Also check the line cap manually since this is the tightest file in the plan:
Run: `wc -l skills/swiftui-interaction/SKILL.md`
Expected: under 60 lines (matching the project's Skill size convention; the
validator's own hard cap is 80).

- [ ] **Step 3: Commit**

```bash
git add skills/swiftui-interaction/SKILL.md
git commit -m "feat: add swiftui-interaction skill for animation/gestures routing"
```

---

### Task 13: Update Skill — swiftui (Foundations)

**Files:**
- Modify: `skills/swiftui/SKILL.md`

- [ ] **Step 1: Add the new skill to `related:`**

Find this block (lines 1-11 of the current file):

```yaml
related:
  - skill.human-interface-guidelines.foundations
last_updated: 2026-08-01
---
```

Replace with:

```yaml
related:
  - skill.human-interface-guidelines.foundations
  - skill.swiftui.interaction
last_updated: 2026-08-06
---
```

- [ ] **Step 2: Rewrite the Stop Conditions section**

Find:

```markdown
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

Replace with:

```markdown
## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/swiftui/ — do not guess or fall back to general
knowledge. Animation and gesture questions route to
`skill.swiftui.interaction` instead of being reported as a gap.
Previews, custom `Layout` protocol conformances, legacy
`ObservableObject`/`NavigationView` migration guidance, and
accessibility APIs (owned by `accessibility`) are out of scope for
this skill (see docs/architecture/domain-map.md) — report that
explicitly rather than answering from general knowledge.
```

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate_artifact.py skills/swiftui/SKILL.md --type skill`
Expected: `PASS: skills/swiftui/SKILL.md`

- [ ] **Step 4: Commit**

```bash
git add skills/swiftui/SKILL.md
git commit -m "docs: route swiftui foundations skill's animation/gesture stop condition to swiftui-interaction"
```

---

### Task 14: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add the new Skills bullet**

Find (the existing `swiftui` bullet, currently lines 76-78):

```markdown
- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`
```

Replace with:

```markdown
- **`swiftui`** — Routes SwiftUI implementation-code tasks (view composition, view identity, modifier order, NavigationStack/NavigationSplitView, layout, safe area, lazy grids, GeometryReader pitfalls, state management) to SwiftUI Knowledge Contracts.
  Example: `"why did my list row selection reset after reordering the array"` → `view-identity.md`
  Example: `"should I use @State or @Binding here"` → `state-and-binding.md`

- **`swiftui-interaction`** — Routes SwiftUI Animation and Gesture implementation tasks (implicit/explicit animation, transitions, matchedGeometryEffect, Animatable, PhaseAnimator/KeyframeAnimator, tap/long-press, drag, magnification/rotation, gesture composition, GestureState) to SwiftUI Interaction Knowledge Contracts.
  Example: `"why isn't my view fading in smoothly"` → `animation-modifiers.md`
  Example: `"how do I make a card draggable and snap back if released early"` → `drag-gesture.md`
```

- [ ] **Step 2: Rotate the What's New section**

Find (the current three-item list, lines 110-115):

```markdown
## What's New

- 2026-08-06 — Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap (Foundations-only HIG coverage). First domain with more than one Skill, split by Apple's own information architecture to stay under the project's Reference/Skill size caps. Flags a new `usernotifications` (Tier 2) cross-domain boundary in domain-map.md.
- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- 2026-08-05 — Added `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication` (which excludes biometrics entirely), replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

Replace with (new entry added at top, oldest of the three dropped to hold
the 3-item cap):

```markdown
## What's New

- 2026-08-06 — Expanded `swiftui` with a new Skill, `swiftui-interaction` (implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState) — 10 Knowledge Contracts. Closes the second of the two named Tier 1 priority gaps (after HIG Patterns/Components). Second domain with more than one Skill, split to stay under the project's Skill size cap.
- 2026-08-06 — Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap (Foundations-only HIG coverage). First domain with more than one Skill, split by Apple's own information architecture to stay under the project's Reference/Skill size caps. Flags a new `usernotifications` (Tier 2) cross-domain boundary in domain-map.md.
- 2026-08-05 — Added `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains. Angle-split with `human-interface-guidelines` on tracking-alert UX, clean handoff with `app-store-review-guidelines` on privacy-label/permission-string topics, replaces the prior placeholder scope in domain-map.md.
- See [CHANGELOG.md](CHANGELOG.md) for the full release history.
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add swiftui-interaction skill to README, rotate What's New"
```

---

### Task 15: Update `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add the new Unreleased entry**

Find:

```markdown
## [Unreleased]
### Added
- Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap. First domain with more than one Skill, split by Apple's own Foundations/Patterns/Components information architecture to stay under the project's Reference (≤80 lines) and Skill (≤60 lines) size caps.
```

Replace with:

```markdown
## [Unreleased]
### Added
- Expanded `swiftui` with a new Skill, `swiftui-interaction` (implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState) — 10 Knowledge Contracts. Closes the second of the two named Tier 1 priority gaps (after HIG Patterns/Components). Second domain with more than one Skill, split by the project's Skill (≤60 lines) size cap.
- Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap. First domain with more than one Skill, split by Apple's own Foundations/Patterns/Components information architecture to stay under the project's Reference (≤80 lines) and Skill (≤60 lines) size caps.
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add swiftui gestures/animation changelog entry"
```

---

### Task 16: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the Tier 1 "Completed:" prose line (line 19)**

Find this exact substring within line 19:

```
`swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt)
```

Replace with:

```
`swiftui` (Tier 1 — Views/Navigation/Layout/State v1 plus Animation/Gestures v1, iOS 17+ conventions: implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState; previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt)
```

Also update the trailing summary sentence at the end of line 19. Find:

```
**All 11 Tier 1 domains complete** (12 domains completed total, including `authentication` cross-cutting/unscheduled); `human-interface-guidelines` expanded post-completion to add its Patterns/Components v1.
```

Replace with:

```
**All 11 Tier 1 domains complete** (12 domains completed total, including `authentication` cross-cutting/unscheduled); `human-interface-guidelines` and `swiftui` each expanded post-completion — `human-interface-guidelines` to add its Patterns/Components v1, `swiftui` to add its Animation/Gestures v1.
```

- [ ] **Step 2: Update the Tier 1 table row (line 28, `swiftui`)**

Find this exact row:

```
| SwiftUI | swiftui | Views (composition, identity, modifier order), Navigation (NavigationStack, NavigationSplitView), Layout (stacks/spacing, safe area, lazy grids, GeometryReader), State management (@State/@Binding, @Observable, @Environment). Targets iOS 17+ conventions; legacy ObservableObject/NavigationView out of scope — see Cross-Domain Notes. | SwiftUI view, navigation, layout, and state-management implementation conventions |
```

Replace with:

```
| SwiftUI | swiftui | Views (composition, identity, modifier order), Navigation (NavigationStack, NavigationSplitView), Layout (stacks/spacing, safe area, lazy grids, GeometryReader), State management (@State/@Binding, @Observable, @Environment). Plus Animation (implicit/explicit, timing curves, transitions, matchedGeometryEffect, Animatable, PhaseAnimator/KeyframeAnimator) and Gestures (tap/long-press, drag, magnification/rotation, gesture composition, GestureState). Targets iOS 17+ conventions; legacy ObservableObject/NavigationView, previews, and custom Layout protocol conformances out of scope — see Cross-Domain Notes. | SwiftUI view, navigation, layout, state-management, animation, and gesture implementation conventions |
```

- [ ] **Step 3: Extend the existing layout Cross-Domain Note (line 98) for discoverability**

Find this exact substring within line 98:

```
- `swiftui` and `human-interface-guidelines` overlap on layout (`swiftui`'s `stacks-and-spacing`/`safe-area`/`lazy-grids` vs. `human-interface-guidelines`'s `layout.md`). Resolved via angle-split: `swiftui`'s angle is code-implementation (which API, correct syntax, performance), `human-interface-guidelines`'s angle is visual-design (spacing/alignment as a design decision). Same pattern as the `app-store-review-guidelines` privacy KCs vs. the future `privacy` domain.
```

Replace with:

```
- `swiftui` and `human-interface-guidelines` overlap on layout (`swiftui`'s `stacks-and-spacing`/`safe-area`/`lazy-grids` vs. `human-interface-guidelines`'s `layout.md`) and, since `swiftui`'s Animation/Gestures v1, on motion and touch interaction too (`swiftui`'s `animation-modifiers.md`/`phase-and-keyframe-animators.md` vs. `human-interface-guidelines`'s `motion.md`; `swiftui`'s gesture KCs vs. `human-interface-guidelines`'s `touchscreen-gestures.md`, whose own Excluded section already names this handoff). Resolved via angle-split: `swiftui`'s angle is code-implementation (which API, correct syntax, performance), `human-interface-guidelines`'s angle is visual-design (spacing/alignment, when/why to animate, which gesture to use — a design decision). Same pattern as the `app-store-review-guidelines` privacy KCs vs. the future `privacy` domain.
```

- [ ] **Step 4: Validate the changes landed**

Run: `grep -c "Animation/Gestures v1" docs/architecture/domain-map.md`
Expected: `2` (the "Completed:" line and the Tier 1 table row)

Run: `grep -c "touchscreen-gestures.md" docs/architecture/domain-map.md`
Expected: `1`

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: record swiftui animation/gestures v1 scope in domain-map"
```

---

### Task 17: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add the new Discovery Rules row**

Find:

```markdown
| SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea | skills/swiftui/SKILL.md |
```

Replace with:

```markdown
| SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea | skills/swiftui/SKILL.md |
| withAnimation, .animation, AnyTransition, matchedGeometryEffect, Animatable, animatableData, PhaseAnimator, KeyframeAnimator, TapGesture, LongPressGesture, DragGesture, MagnifyGesture, RotateGesture, MagnificationGesture, RotationGesture, GestureState, simultaneously, sequenced, exclusively, highPriorityGesture, simultaneousGesture | skills/swiftui-interaction/SKILL.md |
```

- [ ] **Step 2: Commit**

```bash
git add skills/index.md
git commit -m "docs: add swiftui-interaction to skills index"
```

---

### Task 18: Final Validation

**Files:** None (validation only)

- [ ] **Step 1: Validate every new/modified artifact**

```bash
for f in knowledge/swiftui/animation-modifiers.md \
         knowledge/swiftui/transitions.md \
         knowledge/swiftui/matched-geometry-effect.md \
         knowledge/swiftui/animatable-values.md \
         knowledge/swiftui/phase-and-keyframe-animators.md \
         knowledge/swiftui/tap-and-long-press-gestures.md \
         knowledge/swiftui/drag-gesture.md \
         knowledge/swiftui/magnification-and-rotation-gestures.md \
         knowledge/swiftui/gesture-composition.md \
         knowledge/swiftui/gesture-state.md; do
  python3 scripts/validate_artifact.py "$f" --type knowledge
done
python3 scripts/validate_artifact.py skills/swiftui-interaction/SKILL.md --type skill
python3 scripts/validate_artifact.py skills/swiftui/SKILL.md --type skill
python3 scripts/validate_artifact.py references/apple/swiftui.md --type reference
```
Expected: `PASS` for all 13 files, no `FAIL` lines.

- [ ] **Step 2: Line-cap check on the tightest files**

```bash
wc -l references/apple/swiftui.md skills/swiftui-interaction/SKILL.md skills/swiftui/SKILL.md
```
Expected: reference under 80, both skills under 60 (project convention;
validator hard cap is 80 for both).

- [ ] **Step 3: Run the full unit test suite**

```bash
python3 -m unittest tests/test_validate_artifact.py -v
```
Expected: all tests pass, 0 failures.

- [ ] **Step 4: Validate the plugin manifest**

```bash
claude plugin validate .
```
Expected: validation passes.

- [ ] **Step 5: Confirm git status is clean**

```bash
git status
```
Expected: working tree clean, all 18 tasks' commits present on
`feature/swiftui-gestures-animation-domain`.

- [ ] **Step 6: Dispatch a final holistic code-reviewer subagent**

Before finishing, dispatch one subagent (not part of the per-task
spec/quality review pairs) to review the entire branch end-to-end for
issues that only show up across files, not within a single task's diff.
Ask it to check, and report PASS/FAIL with specifics for each:

1. Referential integrity — every `related:`/`depends_on:` id in the 10
   new Knowledge Contracts and 2 Skills (new + modified) resolves to a
   real artifact id in the repo.
2. `routes:` in `skills/swiftui-interaction/SKILL.md` matches exactly
   the 10 `id:` values of the new Knowledge Contracts — no missing, no
   extra.
3. Layer order respected — no Skill embeds domain knowledge directly
   (all substantive rules live in Knowledge Contracts, Skills only route).
4. The three-way cross-link is correct: `skills/swiftui/SKILL.md` and
   `skills/swiftui-interaction/SKILL.md` reference each other via
   `related:`, and both are consistent with
   `skill.human-interface-guidelines.foundations` being named as the
   design-layer handoff.
5. No SwiftUI/Swift code appears inside any `human-interface-guidelines`
   Knowledge Contract as a result of this branch (this branch should
   only touch `swiftui`-domain and cross-cutting doc files).
6. No new Knowledge Contract restates a Rule that already lives in
   `knowledge.human-interface-guidelines.motion` or
   `knowledge.human-interface-guidelines.touchscreen-gestures` — only
   `related:` cross-references are allowed.
7. `docs/architecture/domain-map.md`'s "Completed:" prose line and its
   Tier 1 table row for `swiftui` are both updated and consistent with
   each other (this exact category of bug — updating only one of the
   two — was caught post-hoc in the prior HIG expansion; confirm it
   didn't recur here).
8. Every deprecation claim in the new Knowledge Contracts
   (`.animation(_:)`, the `DragGesture` `CoordinateSpace` overload,
   `MagnificationGesture`, `RotationGesture`) is stated consistently
   across the file that owns it and any file that cross-references it.
9. Release-version invariant unaffected — this branch does not touch
   `README.md`'s `Version:` line, `npx/README.md`, `npx/package.json`,
   or `.claude-plugin/plugin.json` version fields (only `CHANGELOG.md`'s
   `[Unreleased]` section, which doesn't require the five files to match
   until an actual version bump).
10. Every SF Symbol / API name used in a Swift code example (e.g.
    `checkmark.circle.fill`) is not obviously fictitious.

If the reviewer finds issues, fix them directly (controller-level fix,
same pattern as the two defects caught and fixed in the prior HIG
expansion) and re-verify with a second pass of the specific check that
failed.

- [ ] **Step 7: Use superpowers:finishing-a-development-branch**

Once Step 6 reports no remaining issues, invoke the
`finishing-a-development-branch` skill to present the 4 standard
completion options to the user.

---

## Self-Review Notes

**Spec coverage:** All spec sections have a corresponding task —
File Layout (Tasks 1, 12, 13), the 10 KCs (Tasks 2-11), Skill routing
(Task 12), Skill update (Task 13), Documentation Updates (Tasks 14-17),
Validation (Task 18). The spec's "Cross-Domain Boundaries" section
required no new Knowledge Contract changes on the `human-interface-guidelines`
side (both `motion.md` and `touchscreen-gestures.md` already establish
the handoff from their side) — confirmed by reading both files during
planning; only a discoverability extension to the existing domain-map.md
Cross-Domain Note (Task 16, Step 3) was needed, matching the spec's
"Optionally extend line 98's note" language.

**Placeholder scan:** No TBD/TODO markers. Every code example is
complete, compilable-looking Swift reflecting the doc-verified API
surface from planning research (not guessed signatures).

**Type/id consistency:** Verified every `id:` declared in Tasks 2-11
appears verbatim in Task 12's `routes:` list (10 of 10) and in the
`related:` fields of sibling KCs where cross-referenced
(`transitions.md` <-> `animation-modifiers.md`, `drag-gesture.md` <->
`gesture-state.md`/`gesture-composition.md`, etc.) — no drift between
an id used in one file's `related:` and its actual declared `id:` in
the file that owns it.

**Deviation from the prior HIG plan's task-granularity:** This plan
lists each of the 10 Knowledge Contracts as its own task (Tasks 2-11)
rather than pre-batching them into two cluster tasks the way the HIG
plan's Tasks 5-16/17-22 did. The controller executing this plan via
subagent-driven-development MAY still batch the 5 Animation tasks and
5 Gesture tasks into two implementer dispatches each (one per cluster,
matching RFC 0001 decision 5's per-topic-cluster batch review) — this
is an execution-time efficiency choice, not a plan defect, same as the
efficiency adjustment made during the HIG expansion.
