# SF Symbols Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `sf-symbols` domain (1 Reference, 8 Knowledge Contracts, 1 native Skill) covering SF Symbols API implementation — rendering modes, symbol variants, variable value symbols, weight/scale, color/tinting mechanics, custom symbol usage, and UIKit `SymbolConfiguration` — per `docs/superpowers/specs/2026-08-01-sf-symbols-domain-design.md`, replacing the placeholder `sf-symbols` row in `docs/architecture/domain-map.md`.

**Architecture:** Mirrors the `uikit` and `accessibility` domains exactly — References → Knowledge → Skills layer order, atomic Knowledge Contracts validated by `scripts/validate_artifact.py`, one native `SKILL.md` with deterministic keyword routing. No code, no tests in the TDD sense — every task creates or edits a markdown artifact; the "test" for each is `scripts/validate_artifact.py` plus (for the final task) the full unit test suite and plugin validation.

**Tech Stack:** Markdown artifacts, Python validator (`scripts/validate_artifact.py`), `claude plugin validate`.

---

## Task 1: Reference — `references/apple/sf-symbols.md`

**Files:**
- Create: `references/apple/sf-symbols.md`

- [ ] **Step 1: Create the file**

```markdown
# SF Symbols

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/uikit/configuring-and-displaying-symbol-images-in-your-ui

## Purpose

Reference index for Apple's SF Symbols API documentation, scoped to this
domain's v1: core rendering (`Image(systemName:)`/`UIImage(systemName:)`),
rendering modes (monochrome, hierarchical, palette, multicolor), symbol
variants (fill/circle/square/slash), variable value symbols, weight/scale
configuration, color/tinting mechanics, custom symbol usage, and UIKit
`SymbolConfiguration` object composition — across SwiftUI and UIKit.
Symbol effects/animations (`SymbolEffect`, iOS 17+) and Symbol Composer /
custom symbol authoring are deferred to a future pass. Design-level symbol
*selection* (which symbol fits a meaning, fill vs. outline as a design
choice) is owned by the `human-interface-guidelines` domain's
`sf-symbols.md` Knowledge Contract, not this one — see
docs/architecture/domain-map.md Cross-Domain Notes.

## Primary Topics

- Symbol basics
- Rendering modes
- Symbol variants
- Variable value symbols
- Symbol weight and scale
- Symbol color and tinting
- Custom symbol usage
- UIKit symbol configuration

## Used By

- knowledge/sf-symbols/symbol-basics.md ([[knowledge/sf-symbols/symbol-basics]])
- knowledge/sf-symbols/rendering-modes.md ([[knowledge/sf-symbols/rendering-modes]])
- knowledge/sf-symbols/symbol-variants.md ([[knowledge/sf-symbols/symbol-variants]])
- knowledge/sf-symbols/variable-value-symbols.md ([[knowledge/sf-symbols/variable-value-symbols]])
- knowledge/sf-symbols/symbol-weight-and-scale.md ([[knowledge/sf-symbols/symbol-weight-and-scale]])
- knowledge/sf-symbols/symbol-color-and-tinting.md ([[knowledge/sf-symbols/symbol-color-and-tinting]])
- knowledge/sf-symbols/custom-symbol-usage.md ([[knowledge/sf-symbols/custom-symbol-usage]])
- knowledge/sf-symbols/uikit-symbol-configuration.md ([[knowledge/sf-symbols/uikit-symbol-configuration]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/sf-symbols.md --type reference`
Expected: `PASS: references/apple/sf-symbols.md`

- [ ] **Step 3: Commit**

```bash
git add references/apple/sf-symbols.md
git commit -m "docs: add sf-symbols reference index"
```

---

## Task 2: Knowledge Contract — `symbol-basics`

**Files:**
- Create: `knowledge/sf-symbols/symbol-basics.md`

- [ ] **Step 1: Create the file**

```markdown
# Symbol Basics

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-basics
type: knowledge
title: Symbol Basics
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of Image(systemName:) and UIImage(systemName:) to render a system SF Symbol, including safe existence-checking and OS-version availability guarding.
domain: SF Symbols
tags:
  - sf-symbols
  - symbol-basics
  - image
references:
  - https://developer.apple.com/documentation/swiftui/image/init(systemname:)
  - https://developer.apple.com/documentation/uikit/uiimage/init(systemname:)
depends_on: []
related:
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent renders a system SF Symbol
by name and guards against the two ways that name lookup can silently
fail — an invalid name and a name not yet available on the app's minimum
supported OS version — so a broken icon doesn't ship unnoticed.

## Scope

### Included

-   `Image(systemName:)` (SwiftUI) and `UIImage(systemName:)` (UIKit)
-   Existence-checking a symbol name before shipping it
-   OS-version availability guarding for newer symbol names

### Excluded

-   Rendering mode, variant, weight/scale, and color configuration — see
    `rendering-modes`, `symbol-variants`, `symbol-weight-and-scale`,
    `symbol-color-and-tinting`
-   Custom (non-system) symbol usage — see `custom-symbol-usage`

## Rules

### Rule 1

Agents MUST use `Image(systemName:)` / `UIImage(systemName:)` for any
icon that has an SF Symbol equivalent, rather than bundling a custom icon
asset — the system symbol gets automatic weight/scale/rendering-mode
adaptation and Dynamic Type behavior for free.

### Rule 2

Agents MUST verify a system symbol name resolves before shipping it
(`UIImage(systemName: "name") != nil`, or confirm in the SF Symbols app)
— an invalid or unavailable name resolves to `nil` / no image, not a
crash, so the failure is silent unless explicitly checked.

### Rule 3

Agents SHOULD guard symbol names introduced after the app's minimum
deployment target with `if #available(...)`, providing an older
fallback symbol name — a symbol that doesn't exist yet on an older OS
returns `nil` the same as a typo'd name, with no automatic fallback.

### Rule 4

Agents MUST NOT force-unwrap `UIImage(systemName:)` (`!`) in production
code — an unrecognized or unavailable name crashes the app at runtime
instead of failing safely to a placeholder or logged warning.

## Compliant Example

```swift
func statusImage(named name: String) -> UIImage {
    guard let image = UIImage(systemName: name) else {
        assertionFailure("Missing SF Symbol: \(name)")
        return UIImage(systemName: "questionmark.circle") ?? UIImage()
    }
    return image
}

struct StarRating: View {
    var body: some View {
        Image(systemName: "star.fill")
    }
}
```
Existence-checked with a safe fallback instead of force-unwrapping; direct SwiftUI use of a known-valid literal name. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
let icon = UIImage(systemName: "start.fill")!
imageView.image = icon
```
Typo'd symbol name (`start.fill` instead of `star.fill`) force-unwrapped — crashes at runtime instead of failing safely. (Rules 2, 4)

## Dependencies

None.

## References

-   [Apple Developer — Image(systemName:)](https://developer.apple.com/documentation/swiftui/image/init(systemname:))
-   [Apple Developer — UIImage(systemName:)](https://developer.apple.com/documentation/uikit/uiimage/init(systemname:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/symbol-basics.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/symbol-basics.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/symbol-basics.md
git commit -m "feat: add symbol-basics knowledge contract"
```

---

## Task 3: Knowledge Contract — `rendering-modes`

**Files:**
- Create: `knowledge/sf-symbols/rendering-modes.md`

- [ ] **Step 1: Create the file**

```markdown
# Rendering Modes

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.rendering-modes
type: knowledge
title: Rendering Modes
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of SF Symbols rendering modes (monochrome, hierarchical, palette, multicolor) via symbolRenderingMode in SwiftUI and UIImage.SymbolConfiguration in UIKit.
domain: SF Symbols
tags:
  - sf-symbols
  - rendering-modes
  - symbolrenderingmode
references:
  - https://developer.apple.com/documentation/swiftui/symbolrenderingmode
  - https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.sf-symbols.symbol-color-and-tinting
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent selects and applies one of
the four SF Symbols rendering modes — monochrome, hierarchical, palette,
multicolor — in code, so a symbol's layered structure renders the way its
design intends instead of defaulting to whatever automatic mode picks.

## Scope

### Included

-   `.symbolRenderingMode(_:)` in SwiftUI
-   `UIImage.SymbolConfiguration` rendering-mode equivalents in UIKit
-   Matching a rendering mode to a symbol's layered/multicolor capability

### Excluded

-   Which specific colors to apply — see `symbol-color-and-tinting`
-   Which rendering mode best expresses a given design meaning — a design
    decision owned by `human-interface-guidelines`'s `sf-symbols.md`

## Rules

### Rule 1

Agents MUST set an explicit `.symbolRenderingMode(_:)` (SwiftUI) or a
`UIImage.SymbolConfiguration` with a matching mode (UIKit) rather than
relying on the automatic default when a symbol's layered structure
carries meaning (e.g. a palette-colored status icon) — automatic mode may
not select the layered rendering that conveys per-part color.

### Rule 2

Agents MUST pair `.multicolor` rendering only with a symbol whose SF
Symbols definition is authored as multicolor-capable — applying
`.multicolor` to a plain monochrome-only symbol has no visible effect
beyond default rendering.

### Rule 3

Agents MUST pair `.palette` rendering with explicit per-layer colors
(`.foregroundStyle(_:_:_:)` in SwiftUI, `UIImage.SymbolConfiguration(paletteColors:)`
in UIKit) — palette mode with no explicit colors supplied falls back to
default coloring, which may not match design intent.

### Rule 4

Agents SHOULD prefer `.hierarchical` over manually recoloring layers with
`.palette` when a single-color symbol just needs depth (e.g. a filled
shape with a brighter accent on one part) — hierarchical derives shades
from one base color automatically, without specifying per-layer colors.

## Compliant Example

```swift
struct StatusBadge: View {
    var body: some View {
        Image(systemName: "checkmark.seal.fill")
            .symbolRenderingMode(.hierarchical)
            .foregroundStyle(.green)
    }
}

// UIKit
let config = UIImage.SymbolConfiguration(hierarchicalColor: .systemGreen)
let imageView = UIImageView(image: UIImage(systemName: "checkmark.seal.fill"))
imageView.preferredSymbolConfiguration = config
```
Explicit hierarchical mode with one base color, applied consistently in both frameworks. (Rules 1, 4)

## Non-Compliant Example

```swift
Image(systemName: "star.fill")
    .symbolRenderingMode(.multicolor)
```
`star.fill` has no multicolor-authored definition, so `.multicolor` here renders identically to the default — no visible effect, misleading to a reader expecting distinct layer colors. (Rule 2)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — rendering modes apply to a symbol already resolved by name.

## References

-   [Apple Developer — SymbolRenderingMode](https://developer.apple.com/documentation/swiftui/symbolrenderingmode)
-   [Apple Developer — UIImage.SymbolConfiguration](https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/rendering-modes.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/rendering-modes.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/rendering-modes.md
git commit -m "feat: add rendering-modes knowledge contract"
```

---

## Task 4: Knowledge Contract — `symbol-variants`

**Files:**
- Create: `knowledge/sf-symbols/symbol-variants.md`

- [ ] **Step 1: Create the file**

```markdown
# Symbol Variants

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-variants
type: knowledge
title: Symbol Variants
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of SF Symbols variant suffixes (.fill/.circle/.square/.slash) and the symbolVariant(_:) modifier for applying a variant across a view hierarchy.
domain: SF Symbols
tags:
  - sf-symbols
  - symbol-variants
  - symbolvariants
references:
  - https://developer.apple.com/documentation/swiftui/symbolvariants
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent selects a symbol variant —
fill, circle, square, or slash — either per symbol name or app-wide via
the `.symbolVariant(_:)` environment modifier, so selected/emphasized
states render consistently without duplicating variant logic at every
call site.

## Scope

### Included

-   Variant name suffixes (`.fill`, `.circle`, `.square`, `.slash`)
-   `.symbolVariant(_:)` environment modifier
-   Verifying a requested variant exists for a given base symbol

### Excluded

-   Rendering mode (monochrome/hierarchical/palette/multicolor) — see `rendering-modes`
-   Which variant best expresses selected vs. unselected state as a design choice

## Rules

### Rule 1

Agents MUST use the `.symbolVariant(_:)` modifier to switch a variant
across an entire view hierarchy (e.g. all icons in a toolbar becoming
filled together) rather than string-concatenating suffixes onto
`systemName` at each call site — one environment value stays the single
source of truth instead of scattering the same suffix logic everywhere.

### Rule 2

Agents MUST verify a requested variant suffix actually exists for a
given base symbol name before manually building it into a `systemName`
string (e.g. `"heart.fill"`) — not every SF Symbol ships every variant;
a nonexistent suffixed name resolves to `nil` the same as any other
invalid name (see `symbol-basics` Rule 2). This applies to string
suffixes specifically; `.symbolVariant(_:)` behaves differently — it
falls back to the symbol's base rendering rather than producing `nil`
when the requested variant isn't available.

### Rule 3

Agents SHOULD use the `.fill` variant for selected/active/emphasized
states and the unsuffixed (outline) form for default/unselected states,
matching the convention used throughout system UI (e.g. tab bar
selection) — which variant best expresses a given state remains a
design decision owned by `human-interface-guidelines`'s `sf-symbols.md`;
this is a fallback convention, not a design mandate.

### Rule 4

Agents MUST NOT combine the `.slash` variant with `.multicolor`
rendering without visually verifying the result — the slash overlay can
visually conflict with a multicolor symbol's authored layer coloring.

## Compliant Example

```swift
struct SelectableIcon: View {
    let isSelected: Bool

    var body: some View {
        Image(systemName: "heart")
            .symbolVariant(isSelected ? .fill : .none)
    }
}
```
A single environment-driven variant toggle instead of building two separate `systemName` strings. (Rules 1, 3)

## Non-Compliant Example

```swift
Image(systemName: isSelected ? "heart.fill" : "heart")
    .symbolVariant(.circle)
```
Manually building the fill/outline suffix in the `systemName` string while also applying `.symbolVariant(.circle)` on top — the two mechanisms compound unpredictably rather than using one consistent variant strategy. (Rule 1)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — variants apply to a symbol already resolved by name.

## References

-   [Apple Developer — SymbolVariants](https://developer.apple.com/documentation/swiftui/symbolvariants)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/symbol-variants.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/symbol-variants.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/symbol-variants.md
git commit -m "feat: add symbol-variants knowledge contract"
```

---

## Task 5: Knowledge Contract — `variable-value-symbols`

**Files:**
- Create: `knowledge/sf-symbols/variable-value-symbols.md`

- [ ] **Step 1: Create the file**

```markdown
# Variable Value Symbols

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.variable-value-symbols
type: knowledge
title: Variable Value Symbols
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the variableValue parameter on Image(systemName:variableValue:) and UIImage(systemName:variableValue:) to represent a continuous quantity, such as signal or battery strength.
domain: SF Symbols
tags:
  - sf-symbols
  - variable-value
  - image
references:
  - https://developer.apple.com/documentation/swiftui/image/init(systemname:variablevalue:)
  - https://developer.apple.com/documentation/uikit/uiimage/init(systemname:variablevalue:configuration:)
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent represents a continuous
quantity (signal strength, battery level, volume) using a variable-value
SF Symbol, so the rendered symbol always reflects the current numeric
state instead of a fixed appearance.

## Scope

### Included

-   `variableValue:` parameter on `Image(systemName:variableValue:)` and
    `UIImage(systemName:variableValue:configuration:)`
-   Clamping and normalizing the input value to the expected `0...1` range
-   Driving the value from state that updates over time

### Excluded

-   Which symbols are semantically appropriate to pair with a variable
    value — see `human-interface-guidelines`'s `sf-symbols.md`
-   Animated transitions between variable-value levels — deferred,
    symbol-effects/animation scope is out of v1

## Rules

### Rule 1

Agents MUST pass a value in the closed range `0...1` to `variableValue:`
— out-of-range values are clamped rather than rejected, which can
silently mask a data bug (e.g. passing an unconverted `0...100`
percentage instead of normalizing it first).

### Rule 2

Agents MUST use `variableValue:` only with a symbol Apple has authored
with a variable-value representation (e.g. `"wifi"`, cellular- and
battery-style indicator symbols) — passing it to a symbol without one is
a silent no-op, not an error, so the symbol renders as if the parameter
were never supplied.

### Rule 3

Agents SHOULD drive `variableValue` from state that updates as the
underlying quantity changes (e.g. a computed property backed by
`@State`/`@Published`), not a value computed once at view construction,
so the rendered symbol always reflects current data.

### Rule 4

Agents MUST NOT use `variableValue` as a substitute for
`.symbolVariant`/`.fill` boolean state toggling — variable value
represents a continuous quantity, not a selected/unselected state; see
`symbol-variants` for boolean state.

## Compliant Example

```swift
struct SignalIndicator: View {
    @State private var rawSignalPercent: Double

    private var normalizedValue: Double {
        min(max(rawSignalPercent / 100, 0), 1)
    }

    var body: some View {
        Image(systemName: "wifi", variableValue: normalizedValue)
    }
}
```
Percentage explicitly normalized into `0...1` and re-derived from live state on every render. (Rules 1, 3)

## Non-Compliant Example

```swift
Image(systemName: "wifi", variableValue: 85)
```
Raw percentage (`85`) passed directly — silently clamped to `1.0`, indistinguishable from a true 100% signal, losing the actual quantity the symbol was meant to represent. (Rule 1)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — variable value applies to a symbol already resolved by name.

## References

-   [Apple Developer — Image(systemName:variableValue:)](https://developer.apple.com/documentation/swiftui/image/init(systemname:variablevalue:))
-   [Apple Developer — UIImage(systemName:variableValue:configuration:)](https://developer.apple.com/documentation/uikit/uiimage/init(systemname:variablevalue:configuration:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/variable-value-symbols.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/variable-value-symbols.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/variable-value-symbols.md
git commit -m "feat: add variable-value-symbols knowledge contract"
```

---

## Task 6: Knowledge Contract — `symbol-weight-and-scale`

**Files:**
- Create: `knowledge/sf-symbols/symbol-weight-and-scale.md`

- [ ] **Step 1: Create the file**

```markdown
# Symbol Weight and Scale

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-weight-and-scale
type: knowledge
title: Symbol Weight and Scale
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of fontWeight/imageScale in SwiftUI and UIImage.SymbolConfiguration(pointSize:weight:scale:) in UIKit to size and weight-match SF Symbols against adjacent content.
domain: SF Symbols
tags:
  - sf-symbols
  - weight
  - scale
references:
  - https://developer.apple.com/documentation/swiftui/view/imagescale(_:)
  - https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class/init(pointsize:weight:scale:)
depends_on:
  - knowledge.sf-symbols.symbol-basics
related: []
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent sizes and weight-matches an
SF Symbol relative to adjacent text or a control's Dynamic Type size,
using scale and weight APIs rather than resizing the rendered image
directly, so the glyph stays crisp and visually consistent.

## Scope

### Included

-   `.imageScale(_:)` and `.fontWeight(_:)` in SwiftUI
-   `UIImage.SymbolConfiguration(pointSize:weight:scale:)` in UIKit
-   Matching symbol weight to adjacent text weight

### Excluded

-   Rendering mode and color — see `rendering-modes`, `symbol-color-and-tinting`
-   Dynamic Type text-sizing mechanics unrelated to symbols specifically

## Rules

### Rule 1

Agents MUST set `.imageScale(_:)` (SwiftUI) or
`UIImage.SymbolConfiguration(scale:)` (UIKit) to resize a symbol rather
than resizing its containing frame directly — frame-resizing stretches
or distorts the glyph, while scale re-renders it at the correct weight
for that size.

### Rule 2

Agents SHOULD match a symbol's `.fontWeight(_:)` to the weight of
adjacent text (e.g. both `.semibold`) so the symbol doesn't read as
visually heavier or lighter than the label next to it.

### Rule 3

Agents MUST supply `pointSize`, `weight`, and `scale` together in a
single `UIImage.SymbolConfiguration(pointSize:weight:scale:)` call when
precise UIKit sizing matters, rather than chaining several
single-parameter configurations — combining separately constructed
configurations can produce an unpredictable merged result depending on
application order.

### Rule 4

Agents MUST NOT apply a `.font(_:)` modifier to control a symbol's point
size when that symbol sits inside a control (e.g. `Label`) that also
derives its size from Dynamic Type — the explicit size can fight the
control's automatic Dynamic Type scaling. Use `.imageScale(_:)` instead.

## Compliant Example

```swift
HStack {
    Image(systemName: "bolt.fill")
        .imageScale(.medium)
        .fontWeight(.semibold)
    Text("Fast Charging")
        .fontWeight(.semibold)
}

// UIKit
let config = UIImage.SymbolConfiguration(pointSize: 20, weight: .semibold, scale: .medium)
imageView.preferredSymbolConfiguration = config
```
Symbol and text weight explicitly matched; UIKit sizing set in one combined configuration call. (Rules 2, 3)

## Non-Compliant Example

```swift
imageView.image = UIImage(systemName: "bolt.fill")
imageView.frame.size = CGSize(width: 40, height: 40)
```
Resizing the image view's frame directly instead of using a scale configuration — stretches the glyph rather than re-rendering it at the correct weight. (Rule 1)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — weight/scale apply to a symbol already resolved by name.

## References

-   [Apple Developer — imageScale(_:)](https://developer.apple.com/documentation/swiftui/view/imagescale(_:))
-   [Apple Developer — SymbolConfiguration(pointSize:weight:scale:)](https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration-swift.class/init(pointsize:weight:scale:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/symbol-weight-and-scale.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/symbol-weight-and-scale.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/symbol-weight-and-scale.md
git commit -m "feat: add symbol-weight-and-scale knowledge contract"
```

---

## Task 7: Knowledge Contract — `symbol-color-and-tinting`

**Files:**
- Create: `knowledge/sf-symbols/symbol-color-and-tinting.md`

- [ ] **Step 1: Create the file**

```markdown
# Symbol Color and Tinting

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.symbol-color-and-tinting
type: knowledge
title: Symbol Color and Tinting
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the code-level mechanics of coloring an SF Symbol with foregroundStyle in SwiftUI and tintColor in UIKit, matched to the active rendering mode.
domain: SF Symbols
tags:
  - sf-symbols
  - color
  - tinting
references:
  - https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:)
  - https://developer.apple.com/documentation/uikit/uiview/tintcolor
depends_on:
  - knowledge.sf-symbols.rendering-modes
related:
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-08-01
```

## Intent

This contract defines the code-level mechanics of applying color to an SF
Symbol — `.foregroundStyle(_:_:_:)` in SwiftUI, `tintColor` in UIKit —
matched correctly to the symbol's active rendering mode, so a color
override actually takes visible effect instead of being silently ignored
by an incompatible mode.

## Scope

### Included

-   `.foregroundStyle(_:_:_:)` argument count matched to rendering mode
-   `UIImageView.tintColor` inheritance and system color usage
-   Why `.multicolor` rendering may ignore foreground color overrides,
    and why that behavior is symbol-dependent

### Excluded

-   Which specific color to choose for a given design context — a design
    decision owned by `human-interface-guidelines`'s `sf-symbols.md`
-   Selecting the rendering mode itself — see `rendering-modes`

## Rules

### Rule 1

Agents MUST supply exactly as many colors to `.foregroundStyle(_:_:_:)`
as the active rendering mode expects — one for monochrome/hierarchical's
base color, up to three for `.palette` (one per layer) — supplying fewer
leaves the remaining layers at their default color, and supplying more is
ignored.

### Rule 2

Agents MUST use `UIImageView.tintColor` (inherited from the view
hierarchy when left unset) for monochrome/hierarchical UIKit symbols,
rather than baking a fixed color into the image itself — `tintColor`
responds to view-hierarchy overrides and system appearance changes
automatically.

### Rule 3

Agents MUST NOT assume `.foregroundStyle` or `tintColor` will recolor a
`.multicolor`-rendered symbol's built-in layers — most multicolor
symbols use fully fixed authored colors that ignore overrides entirely,
but some are authored with a dynamic layer that does pick up the current
foreground/tint color. Verify a specific symbol's actual behavior (SF
Symbols app or an empirical check) rather than assuming either outcome
universally.

### Rule 4

Agents SHOULD use system colors (`Color.primary`/`.secondary`,
`UIColor.label`/`.secondaryLabel`) rather than fixed RGB values so a
symbol's tint adapts automatically to Dark Mode and increased-contrast
settings — deciding *which* system color fits a given context remains a
design decision owned by `human-interface-guidelines`'s `sf-symbols.md`.

## Compliant Example

```swift
Image(systemName: "flag.fill")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.white, .red)
```
Two colors supplied for a two-layer palette symbol, matching the rendering mode's expected color count. (Rule 1)

## Non-Compliant Example

```swift
let imageView = UIImageView(image: multicolorFlagSymbol)
imageView.tintColor = .red
```
`tintColor` set on a `.multicolor`-rendered symbol without first checking whether that symbol's layers are fixed or dynamic — for a fully fixed-color multicolor symbol this has no visible effect, and assuming that universally risks missing symbols authored with a dynamic layer that would actually respond. (Rule 3)

## Dependencies

- `knowledge.sf-symbols.rendering-modes` — color application depends on the active rendering mode.

## References

-   [Apple Developer — foregroundStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:))
-   [Apple Developer — UIView.tintColor](https://developer.apple.com/documentation/uikit/uiview/tintcolor)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/symbol-color-and-tinting.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/symbol-color-and-tinting.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/symbol-color-and-tinting.md
git commit -m "feat: add symbol-color-and-tinting knowledge contract"
```

---

## Task 8: Knowledge Contract — `custom-symbol-usage`

**Files:**
- Create: `knowledge/sf-symbols/custom-symbol-usage.md`

- [ ] **Step 1: Create the file**

```markdown
# Custom Symbol Usage

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.custom-symbol-usage
type: knowledge
title: Custom Symbol Usage
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how to reference an already-authored custom symbol asset in code so it renders with the same rendering-mode/weight/scale/tinting behavior as a system SF Symbol. Excludes authoring the symbol artwork itself.
domain: SF Symbols
tags:
  - sf-symbols
  - custom-symbol
  - asset-catalog
references:
  - https://developer.apple.com/documentation/swiftui/image/init(_:bundle:)
  - https://developer.apple.com/documentation/uikit/uiimage/init(named:)
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.sf-symbols.rendering-modes
  - knowledge.sf-symbols.symbol-weight-and-scale
  - knowledge.sf-symbols.symbol-color-and-tinting
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent references a custom symbol
that has already been added to the asset catalog as a Symbol Image
template, so it behaves identically to a system SF Symbol at the API
level. It covers usage only — authoring the symbol's artwork (Symbol
Composer, `.svg` preparation) is a design/asset-pipeline task outside
this contract's scope.

## Scope

### Included

-   Referencing a custom symbol by asset name (`Image("name")`,
    `UIImage(named:)`)
-   Confirming the asset is configured as a Symbol Image template, not a
    static bitmap
-   Applying the same rendering/variant/weight/color rules that apply to
    system symbols

### Excluded

-   Symbol Composer workflow, `.svg` export/preparation, or any other
    artwork-authoring step
-   Adding the asset to the asset catalog in Xcode (a project-configuration
    step, not a code-implementation rule)

## Rules

### Rule 1

Agents MUST reference a custom symbol added to the asset catalog by its
asset name via `Image("customName")` (SwiftUI) or `UIImage(named:
"customName")` (UIKit) — the same call pattern as any other named image
asset, with no symbol-specific initializer required.

### Rule 2

Agents MUST confirm the custom symbol asset is configured as a "Symbol
Image" template (not a static bitmap) before relying on
rendering-mode/weight/scale/tinting modifiers on it — those modifiers
only affect template-rendered images; a plain bitmap asset ignores them
silently, with no error.

### Rule 3

Agents MUST apply the same rendering-mode, weight/scale, and tinting
rules that apply to system symbols (see `rendering-modes`,
`symbol-weight-and-scale`, `symbol-color-and-tinting`) to a correctly
configured custom symbol — a template-configured custom symbol behaves
identically to a system symbol at the API level once imported.

### Rule 4

Agents MUST NOT author, edit, or export a custom symbol's artwork (Symbol
Composer workflow, `.svg` preparation) as part of an implementation task
— that is a design/asset-pipeline task outside this contract's scope;
implementation only consumes an already-prepared symbol asset.

## Compliant Example

```swift
Image("app.custom.badge")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.blue)
```
A custom symbol referenced by asset name and styled with the same rendering-mode API used for system symbols, because the asset is configured as a Symbol Image template. (Rules 1, 3)

## Non-Compliant Example

```swift
Image("app.custom.badge")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.white, .blue)
```
Applied to an asset that was imported as a plain bitmap (not a Symbol Image template) — the rendering-mode and multi-color foreground styling have no effect, producing an unstyled flat image with no error to indicate why. (Rule 2)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — custom symbols are referenced by name the same way system symbols are.

## References

-   [Apple Developer — Image(_:bundle:)](https://developer.apple.com/documentation/swiftui/image/init(_:bundle:))
-   [Apple Developer — UIImage(named:)](https://developer.apple.com/documentation/uikit/uiimage/init(named:))
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/custom-symbol-usage.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/custom-symbol-usage.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/custom-symbol-usage.md
git commit -m "feat: add custom-symbol-usage knowledge contract"
```

---

## Task 9: Knowledge Contract — `uikit-symbol-configuration`

**Files:**
- Create: `knowledge/sf-symbols/uikit-symbol-configuration.md`

- [ ] **Step 1: Create the file**

```markdown
# UIKit Symbol Configuration

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.uikit-symbol-configuration
type: knowledge
title: UIKit Symbol Configuration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines composing and applying UIImage.SymbolConfiguration objects in UIKit — withConfiguration(_:), preferredSymbolConfiguration, and combining configurations with applying(_:).
domain: SF Symbols
tags:
  - sf-symbols
  - uikit
  - symbolconfiguration
references:
  - https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration
  - https://developer.apple.com/documentation/uikit/uiimage/withconfiguration(_:)
  - https://developer.apple.com/documentation/uikit/uiimageview/preferredsymbolconfiguration
depends_on:
  - knowledge.sf-symbols.symbol-basics
related:
  - knowledge.sf-symbols.rendering-modes
  - knowledge.sf-symbols.symbol-weight-and-scale
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent composes and applies
`UIImage.SymbolConfiguration` objects in UIKit — setting a reusable
configuration on a `UIImageView`, updating an existing image's
configuration without re-fetching it by name, and combining
configuration aspects built separately — so symbol styling in UIKit stays
consistent and correctly applied.

## Scope

### Included

-   `UIImageView.preferredSymbolConfiguration`
-   `UIImage.withConfiguration(_:)`
-   Combining `UIImage.SymbolConfiguration` values with `.applying(_:)`

### Excluded

-   What each configuration parameter should be set to (weight, scale,
    rendering mode) — see `rendering-modes`, `symbol-weight-and-scale`
-   SwiftUI equivalents — SwiftUI uses view modifiers, not this object,
    see `rendering-modes` and `symbol-weight-and-scale`

## Rules

### Rule 1

Agents MUST set `UIImageView.preferredSymbolConfiguration` rather than
pre-configuring each individual `UIImage` when the same image view will
display different symbol names over its lifetime — the view applies the
stored configuration to every symbol image assigned afterward, so
weight/scale/rendering-mode logic isn't repeated per assignment.

### Rule 2

Agents MUST use `UIImage.withConfiguration(_:)` to get a differently
configured version of an already-resolved symbol image, rather than
calling `UIImage(systemName:)` again with a new configuration — reusing
the resolved image avoids a redundant name lookup.

### Rule 3

Agents SHOULD compose configuration aspects that come from separate
sources (e.g. a size configuration from one place, a color configuration
from another) with `UIImage.SymbolConfiguration.applying(_:)` rather than
one large combined initializer call — this keeps each aspect's origin
clear and combinable independently.

### Rule 4

Agents MUST NOT assume `withConfiguration(_:)` mutates its receiver — it
returns a new `UIImage`; discarding the return value and expecting the
original image or an image view's current image to have changed is a
no-op bug.

## Compliant Example

```swift
let sizeConfig = UIImage.SymbolConfiguration(pointSize: 20, weight: .semibold)
let colorConfig = UIImage.SymbolConfiguration(hierarchicalColor: .systemBlue)
let combined = sizeConfig.applying(colorConfig)

imageView.preferredSymbolConfiguration = combined
imageView.image = UIImage(systemName: "star.fill")
```
Two independently built configurations combined via `applying(_:)`, then set once on the image view so every later symbol assignment inherits it. (Rules 1, 3)

## Non-Compliant Example

```swift
let image = UIImage(systemName: "star.fill")!
image.withConfiguration(UIImage.SymbolConfiguration(pointSize: 30, weight: .bold))
imageView.image = image
```
The return value of `withConfiguration(_:)` is discarded — `image` and the assigned `imageView.image` remain unconfigured, so the intended size/weight change never takes effect. (Rule 4)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — configuration applies to a symbol already resolved by name.

## References

-   [Apple Developer — UIImage.SymbolConfiguration](https://developer.apple.com/documentation/uikit/uiimage/symbolconfiguration)
-   [Apple Developer — withConfiguration(_:)](https://developer.apple.com/documentation/uikit/uiimage/withconfiguration(_:))
-   [Apple Developer — preferredSymbolConfiguration](https://developer.apple.com/documentation/uikit/uiimageview/preferredsymbolconfiguration)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/sf-symbols/uikit-symbol-configuration.md --type knowledge`
Expected: `PASS: knowledge/sf-symbols/uikit-symbol-configuration.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/sf-symbols/uikit-symbol-configuration.md
git commit -m "feat: add uikit-symbol-configuration knowledge contract"
```

---

## Task 10: Native Skill — `skills/sf-symbols/SKILL.md`

**Files:**
- Create: `skills/sf-symbols/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: sf-symbols
description: Route SF Symbols API implementation tasks to the correct Knowledge Contracts — symbol basics (Image(systemName:)/UIImage(systemName:)), rendering modes, symbol variants, variable value symbols, weight/scale, color/tinting mechanics, custom symbol usage, and UIKit SymbolConfiguration composition. Use when writing or reviewing code that renders, styles, or configures an SF Symbol in SwiftUI or UIKit. v1 excludes symbol effects/animations (SymbolEffect) and Symbol Composer/custom symbol authoring. Design-level symbol selection (which symbol, which color, as a design decision) is out of scope here — see the human-interface-guidelines skill. Triggers on SF Symbols, Image(systemName:), UIImage(systemName:), symbolRenderingMode, SymbolVariants, variableValue, imageScale, fontWeight on a symbol, SymbolConfiguration, preferredSymbolConfiguration, withConfiguration, hierarchical rendering, palette rendering, multicolor rendering.
id: skill.sf-symbols.foundations
title: SF Symbols — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: SF Symbols
routes: [knowledge.sf-symbols.symbol-basics, knowledge.sf-symbols.rendering-modes, knowledge.sf-symbols.symbol-variants, knowledge.sf-symbols.variable-value-symbols, knowledge.sf-symbols.symbol-weight-and-scale, knowledge.sf-symbols.symbol-color-and-tinting, knowledge.sf-symbols.custom-symbol-usage, knowledge.sf-symbols.uikit-symbol-configuration]
related:
  - skill.human-interface-guidelines.foundations
  - skill.swiftui.foundations
  - skill.uikit.foundations
last_updated: 2026-08-01
---

# SF Symbols — Foundations Skill

## Purpose

Route SF Symbols API implementation tasks to the minimum required SF
Symbols Knowledge Contracts. v1 scope is core rendering, rendering
modes, variants, variable value, weight/scale, color/tinting, custom
symbol usage, and UIKit `SymbolConfiguration` composition — across
SwiftUI and UIKit.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/sf-symbols/.

-   Usage -> symbol-basics.md, custom-symbol-usage.md
-   Rendering -> rendering-modes.md, symbol-variants.md, variable-value-symbols.md, symbol-weight-and-scale.md, symbol-color-and-tinting.md
-   UIKit-specific -> uikit-symbol-configuration.md

Never load more than the contracts relevant to the specific question.
For which symbol to choose, which color fits a design, or fill vs.
outline as a design decision, route to
`skill.human-interface-guidelines.foundations` instead. For view
composition/state/navigation questions unrelated to symbol rendering
itself, route to `skill.swiftui.foundations` or `skill.uikit.foundations`.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/sf-symbols/ — do not guess or fall back to general
knowledge. Symbol effects/animations (`SymbolEffect`, `.bounce`,
`.pulse`, `.variableColor`) and Symbol Composer / custom symbol
authoring are deferred to future scope, not yet built — report that
explicitly rather than answering from general knowledge (see
docs/architecture/domain-map.md).
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/sf-symbols/SKILL.md --type skill`
Expected: `PASS: skills/sf-symbols/SKILL.md`

- [ ] **Step 3: Commit**

```bash
git add skills/sf-symbols/SKILL.md
git commit -m "feat: add sf-symbols native skill"
```

---

## Task 11: Update `skills/index.md`

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a new Discovery Rules row**

In the `## Discovery Rules` table, add this row immediately after the
`uikit` row (the row containing `skills/uikit/SKILL.md`):

```markdown
| SF Symbols, Image(systemName:), UIImage(systemName:), symbolRenderingMode, SymbolVariants, variableValue, imageScale, SymbolConfiguration, preferredSymbolConfiguration, hierarchical rendering, palette rendering, multicolor rendering, symbol variant | skills/sf-symbols/SKILL.md |
```

- [ ] **Step 2: Validate manually**

Run: `grep -c "skills/.*SKILL.md" skills/index.md`
Expected: `8` (authentication, style-guide, human-interface-guidelines, app-store-review-guidelines, swiftui, accessibility, uikit, sf-symbols)

- [ ] **Step 3: Commit**

```bash
git add skills/index.md
git commit -m "docs: add sf-symbols to skills index"
```

---

## Task 12: Update `docs/architecture/domain-map.md`

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the `sf-symbols` row's Initial Scope and Owns cells**

Find this exact row in the Tier 1 table:

```markdown
| SF Symbols | sf-symbols | Iconography | Icon selection and SF Symbols usage rules |
```

Replace with:

```markdown
| SF Symbols | sf-symbols | SF Symbols API implementation v1: symbol basics (Image(systemName:)/UIImage(systemName:)), rendering modes (monochrome/hierarchical/palette/multicolor), symbol variants (fill/circle/square/slash), variable value symbols, weight/scale configuration, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration. Symbol effects/animations and Symbol Composer authoring deferred — see Cross-Domain Notes. | SF Symbols API implementation across SwiftUI and UIKit (rendering, variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration) |
```

- [ ] **Step 2: Update the Build Order Completed line**

Find this exact line:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt).
```

Replace with:

```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt).
```

- [ ] **Step 3: Resolve the sf-symbols Cross-Domain Note in place**

Find this exact line:

```markdown
- `human-interface-guidelines` (`sf-symbols` Foundations topic) and the future `sf-symbols` domain (Tier 1, unbuilt) overlap: HIG's angle is symbol selection/composition in a design, the dedicated domain's angle is API usage and rendering modes. Boundary not yet resolved — decide when `sf-symbols` is built.
```

Replace with (resolves the boundary in place, then adds two new bullets
after it):

```markdown
- `human-interface-guidelines` (`sf-symbols` Foundations topic) and `sf-symbols` overlap: HIG owns symbol selection/composition as a design decision (which symbol, which color, fill vs. outline as a design choice), `sf-symbols` owns API implementation (rendering modes, variants, variable value, weight/scale, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration). Resolved via angle-split — `sf-symbols` KCs cross-reference `human-interface-guidelines`'s `sf-symbols.md` via `related:` rather than restating its Rules.
- `sf-symbols` and `uikit` overlap: `uikit` KCs may display symbols inside their examples but don't own symbol-rendering rules — a future `uikit` KC needing symbol-specific guidance should cross-reference `sf-symbols` via `related:` rather than duplicating rendering-mode/weight/scale content. No existing `uikit` KC required updating for this domain's launch.
- `sf-symbols` and `swiftui` overlap: same pattern as `sf-symbols` vs. `uikit` — `swiftui` owns view composition, not symbol rendering. No existing `swiftui` KC required updating for this domain's launch.
```

- [ ] **Step 4: Validate manually**

Run: `grep -c "sf-symbols" docs/architecture/domain-map.md`
Expected: a number greater than 3 (the file already mentions "sf-symbols"
at least three times before this task — the Tier 1 row, the artifact-layout
example, and the pre-existing HIG Cross-Domain Note — the updated row,
Completed line, and three-bullet Cross-Domain Notes block push the count
well above that baseline)

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: scope sf-symbols v1, resolve HIG cross-domain note"
```

---

## Task 13: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a new Skills bullet**

Find this exact block in `## Skills` (the `uikit` bullet, immediately
before the `Full routing tables:` line):

```markdown
- **`uikit`** — Routes UIKit screen-scaffolding implementation tasks (view controller lifecycle/composition, programmatic Auto Layout, navigation, diffable table/collection views, modal presentation) to UIKit Knowledge Contracts.
  Example: `"my child view controller's view isn't showing up correctly"` → `view-controller-composition.md`
  Example: `"how do I animate row insertion in a UITableView"` → `table-view-diffable.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

Replace with:

```markdown
- **`uikit`** — Routes UIKit screen-scaffolding implementation tasks (view controller lifecycle/composition, programmatic Auto Layout, navigation, diffable table/collection views, modal presentation) to UIKit Knowledge Contracts.
  Example: `"my child view controller's view isn't showing up correctly"` → `view-controller-composition.md`
  Example: `"how do I animate row insertion in a UITableView"` → `table-view-diffable.md`

- **`sf-symbols`** — Routes SF Symbols API implementation tasks (rendering modes, symbol variants, variable value, weight/scale, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration) to SF Symbols Knowledge Contracts, across SwiftUI and UIKit.
  Example: `"this status icon should use two colors, one per layer"` → `rendering-modes.md`
  Example: `"how do I show wifi signal strength as a symbol"` → `variable-value-symbols.md`

Full routing tables: [skills/index.md](skills/index.md). Domain build order and scope: [docs/architecture/domain-map.md](docs/architecture/domain-map.md).
```

- [ ] **Step 2: Add a new What's New line**

Find this exact line (the first/topmost line in `## What's New`):

```markdown
- 2026-08-01 — Added `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation; programmatic UI v1) — 12 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
```

Replace with (adds a new topmost line before it):

```markdown
- 2026-08-01 — Added `sf-symbols` Skill (symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contracts. Resolves the human-interface-guidelines sf-symbols forward-reference and replaces the prior placeholder scope in domain-map.md.
- 2026-08-01 — Added `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation; programmatic UI v1) — 12 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.
```

- [ ] **Step 3: Validate manually**

Run: `grep -c "sf-symbols" README.md`
Expected: a number greater than 0 (the new `sf-symbols` Skills bullet and
What's New line are the first mentions of "sf-symbols" in this file)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add sf-symbols to README Skills + What's New"
```

---

## Task 14: Final Validation

**Files:** None created or modified — verification only.

- [ ] **Step 1: Validate every new artifact**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/sf-symbols.md --type reference
python3 scripts/validate_artifact.py skills/sf-symbols/SKILL.md --type skill
for f in knowledge/sf-symbols/*.md; do python3 scripts/validate_artifact.py "$f" --type knowledge; done
```
Expected: `PASS` for all 10 files.

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: passes (only the pre-existing, unrelated warning if present).

- [ ] **Step 4: Confirm clean git status**

Run: `git status`
Expected: `nothing to commit, working tree clean` (all 13 prior tasks committed).

- [ ] **Step 5: Dispatch a final holistic code-reviewer subagent**

Use `superpowers:code-reviewer` on the entire `sf-symbols` domain (all 10
new files plus the 3 modified docs) to check cross-file consistency:
every `related:`/`depends_on:` KC id resolves to a real file (including
the cross-domain `knowledge.human-interface-guidelines.sf-symbols`
reference used across multiple KCs), the Skill's `routes:` list matches
exactly the 8 KC ids, the Reference's "Used By" list matches exactly the
8 KC files, layer order (References → Knowledge → Skills) is respected,
the new Cross-Domain Notes block reads correctly. The review must
specifically check for v1-scope violations that a per-task review could
miss (this class of bug slipped through per-task review in the `uikit`
domain build and was only caught by the final holistic pass):

-   No content anywhere describing `SymbolEffect`, `.bounce`, `.pulse`,
    `.variableColor`, or any other symbol-effects/animation API
-   No content anywhere describing Symbol Composer workflow, `.svg`
    export, or custom-symbol *authoring* steps (only *usage* of an
    already-authored custom symbol is in scope)
-   No KC restates `human-interface-guidelines`'s `sf-symbols.md` Rules
    about which symbol/color/variant to choose as a design decision —
    every KC that touches color, rendering-mode, or variant selection
    cross-references it via `related:` instead
-   Live-verify (`curl`/JSON endpoint, not WebFetch's summarized output)
    every Apple Developer URL cited across all 10 files actually
    resolves — this is standard practice for every task in this domain,
    not just the final one, per the broken-URL findings in the prior
    `accessibility` and `uikit` domain builds

If the reviewer finds issues, fix them, re-validate the affected file(s),
commit the fix, and re-run Steps 1–4 to confirm no regressions.

- [ ] **Step 6: Report final status**

Report the total commit count for this domain, confirm all validations
pass, and hand off to `superpowers:finishing-a-development-branch` for
shipping (branch + PR, per this session's established pattern).
