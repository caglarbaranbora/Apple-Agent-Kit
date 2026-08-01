# SF Symbols Domain Design

Status: Draft Version: 0.1.0

## Purpose

Replace the placeholder `sf-symbols` entry in `docs/architecture/domain-map.md`
(Initial Scope: "Iconography", Owns: "Icon selection and SF Symbols usage
rules") with a real Tier 1 domain covering SF Symbols API implementation —
how an AI coding agent renders, configures, and styles SF Symbols in code,
across SwiftUI and UIKit.

## Context

`human-interface-guidelines` (shipped, PR #5) already owns a
`sf-symbols.md` Knowledge Contract, but its angle is design-level: which
rendering mode to *choose*, which weight/scale to *match*, when to use
fill vs. outline. Its own Intent section explicitly defers "API-level
rendering/animation implementation" to "the future dedicated `sf-symbols`
domain" — this spec is that domain.

`domain-map.md`'s Cross-Domain Notes (line 103) already flags this
boundary as unresolved:

> `human-interface-guidelines` (`sf-symbols` Foundations topic) and the
> future `sf-symbols` domain (Tier 1, unbuilt) overlap: HIG's angle is
> symbol selection/composition in a design, the dedicated domain's angle
> is API usage and rendering modes. Boundary not yet resolved — decide
> when `sf-symbols` is built.

This spec resolves that boundary and confirms it in `domain-map.md`.

## Decisions

### Decision 1: v1 scope — "core + rendering + variants"

v1 covers: basic symbol rendering (`Image(systemName:)` /
`UIImage(systemName:)`), the four rendering modes (monochrome,
hierarchical, palette, multicolor), symbol variants (`.fill`, `.circle`,
`.square`, `.slash`), variable value symbols (`variableValue`), weight/scale
configuration, and color/tinting mechanics.

**Out of scope for v1** (explicit, not silent):
- Symbol effects/animations (`SymbolEffect`, `.bounce`, `.pulse`,
  `.variableColor`, iOS 17+) — deferred, unassigned owner
- Symbol Composer / custom symbol *authoring* (`.svg` export, drawing
  custom symbols) — asset-authoring work, not code implementation
- Design-level symbol *selection* (which symbol fits a given meaning,
  when to use fill vs. outline as a design decision) — owned by
  `human-interface-guidelines`'s existing `sf-symbols.md`

### Decision 2: Framework coverage — SwiftUI + UIKit together

Each Knowledge Contract covers both `Image(systemName:)`
(SwiftUI) and `UIImage(systemName:)`/`UIImageView` (UIKit) where the
underlying concept applies to both, mirroring the pattern established by
the `accessibility` domain (each KC crosses both frameworks rather than
splitting by platform). One topic — `uikit-symbol-configuration` — is
UIKit-specific because `UIImage.SymbolConfiguration` object composition
has no SwiftUI equivalent (SwiftUI uses modifiers instead).

### Decision 3: Custom symbol *usage* is in scope, *authoring* is not

Using a custom symbol that's already been added to `Assets.xcassets` in
code (`Image("customSymbolName")`, rendered the same way as a system
symbol) is in scope. Creating that custom symbol file (Symbol Composer
workflow, `.svg` export/preparation) is out of scope — that's a design
asset pipeline, not something an agent implements in Swift code.

### Decision 4: 8-topic atomic breakdown

| # | Slug | Covers |
|---|---|---|
| 1 | `symbol-basics` | `Image(systemName:)` / `UIImage(systemName:)`, checking whether a system symbol name exists |
| 2 | `rendering-modes` | Monochrome, hierarchical, palette, multicolor — `.symbolRenderingMode(_:)` and `UIImage.SymbolConfiguration` equivalents |
| 3 | `symbol-variants` | `.fill`/`.circle`/`.square`/`.slash` name suffixes, `.symbolVariant(_:)` modifier |
| 4 | `variable-value-symbols` | `variableValue:` parameter, symbols that support a continuous value (e.g. Wi-Fi strength, battery level) |
| 5 | `symbol-weight-and-scale` | `.fontWeight(_:)`/`.imageScale(_:)` in SwiftUI, `UIImage.SymbolConfiguration(weight:scale:pointSize:)` in UIKit |
| 6 | `symbol-color-and-tinting` | `.foregroundStyle(_:_:_:)` with palette/multicolor rendering, `tintColor` mechanics — code-level API, not the design decision of *which* color (that's HIG's) |
| 7 | `custom-symbol-usage` | Using a custom symbol already in the asset catalog the same way as a system symbol |
| 8 | `uikit-symbol-configuration` | `UIImage.SymbolConfiguration` object composition and `withConfiguration(_:)`, applying a config without re-fetching the base image |

Each KC's `related:` cross-references `knowledge.human-interface-guidelines.sf-symbols`
for the design-decision angle, and does not restate its Rules.

### Decision 5: Cross-domain resolution

- **`sf-symbols` ↔ `human-interface-guidelines`**: resolved via the
  angle-split already stated in HIG's `sf-symbols.md` Intent — HIG owns
  symbol *selection*/composition as a design decision, this domain owns
  API *usage*/rendering mechanics. Confirmed, not re-litigated, in this
  spec.
- **`sf-symbols` ↔ `uikit`**: `uikit`'s KCs (e.g. `cell-configuration`,
  `tab-bar-controller`) may use symbols in examples, but don't own symbol
  rendering rules — they'd cross-reference `sf-symbols` via `related:` if
  a future KC needs it. No existing `uikit` KC requires updating for this
  domain's launch.
- **`sf-symbols` ↔ `swiftui`**: same pattern — `swiftui`'s KCs own view
  composition, not symbol rendering. No existing `swiftui` KC requires
  updating.

### Decision 6: File layout

```
references/apple/sf-symbols.md
knowledge/sf-symbols/symbol-basics.md
knowledge/sf-symbols/rendering-modes.md
knowledge/sf-symbols/symbol-variants.md
knowledge/sf-symbols/variable-value-symbols.md
knowledge/sf-symbols/symbol-weight-and-scale.md
knowledge/sf-symbols/symbol-color-and-tinting.md
knowledge/sf-symbols/custom-symbol-usage.md
knowledge/sf-symbols/uikit-symbol-configuration.md
skills/sf-symbols/SKILL.md
```

### Decision 7: Skill routing clusters

`skills/sf-symbols/SKILL.md` routes across 3 clusters:
- **Rendering**: `rendering-modes`, `symbol-variants`, `variable-value-symbols`, `symbol-weight-and-scale`, `symbol-color-and-tinting`
- **Usage**: `symbol-basics`, `custom-symbol-usage`
- **UIKit-specific**: `uikit-symbol-configuration`

`related:` lists `skill.human-interface-guidelines.foundations` (design
angle), `skill.swiftui.foundations` and `skill.uikit.foundations`
(symbols are used inside views built by both).

### Decision 8: domain-map.md update

- `sf-symbols` row: Initial Scope replaced with the real v1 scope from
  Decision 1; Owns updated to "SF Symbols API implementation: rendering
  modes, variants, variable value, weight/scale, color/tinting, custom
  symbol usage, UIKit SymbolConfiguration"
- Build Order "Completed" line: append `sf-symbols` entry with its scope
  and explicitly-deferred items (symbol effects/animations, Symbol
  Composer authoring)
- Cross-Domain Notes: replace the existing unresolved line (103) with a
  resolved statement confirming the angle-split, matching the pattern
  used for `uikit`↔`accessibility` and `uikit`↔`human-interface-guidelines`

## Consequences

- Agents asking "how do I render this symbol with a specific color" get
  routed to `sf-symbols`, not forced to dig through HIG's design-level
  content or guess at API syntax.
- Symbol effects/animations remain a documented gap — flagged in
  Build Order, not silently missing.
- `README.md` gets a new `## Skills` bullet and a new `## What's New`
  top line, per `CLAUDE.md`'s same-PR requirement.

## Testing / Validation Plan

- `python3 scripts/validate_artifact.py <path> --type knowledge` for
  each of the 8 KCs and the Reference (`--type reference`)
- `python3 scripts/validate_artifact.py skills/sf-symbols/SKILL.md --type skill`
- `python3 -m unittest tests/test_validate_artifact.py -v`
- Every cited Apple Developer URL live-verified (`curl`/JSON endpoint,
  not WebFetch's summarized output) to resolve, per this session's
  established practice after catching a broken/ambiguous overload URL in
  the `uikit` domain build
- Final holistic review pass across all 8 KCs for v1-scope consistency
  (no symbol-effects/animation content, no custom-symbol-authoring
  content, no restated HIG design-decision Rules) — this class of issue
  was only caught by the holistic pass, not per-task review, during the
  `uikit` domain build (`table-view-diffable.md`'s `@IBOutlet` violation)

## Out of Scope

- Symbol effects/animations (`SymbolEffect`) — future work, unassigned owner
- Symbol Composer / custom symbol authoring — asset-authoring, not this project's domain (code implementation conventions)
- Design-level symbol selection — owned by `human-interface-guidelines`
