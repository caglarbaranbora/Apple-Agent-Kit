# Human Interface Guidelines Domain (Foundations) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `human-interface-guidelines` as a new native domain — 1 Reference, 15 Knowledge Contracts (HIG Foundations, iOS/iPadOS scope), 1 native Skill — following the layer order and file conventions established by `style-guide`/`authentication`.

**Architecture:** References → Knowledge → Skills. One flat reference file indexes 15 Knowledge Contracts (one per HIG Foundations topic, iOS/iPadOS-scoped content sourced from Apple's own HIG documentation). One native `SKILL.md` routes to all 15 via keyword clusters, mirroring `skills/style-guide/SKILL.md`.

**Tech Stack:** Markdown artifacts validated by `scripts/validate_artifact.py` (`--type knowledge|skill|reference`); no application code.

**Source spec:** `docs/superpowers/specs/2026-07-31-human-interface-guidelines-domain-design.md`

---

## Task 1: Reference file

**Files:**
- Create: `references/apple/human-interface-guidelines.md`

- [ ] **Step 1: Create the reference file**

```markdown
# Human Interface Guidelines

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/design/human-interface-guidelines/foundations

## Purpose

Reference index for Apple's Human Interface Guidelines — Foundations
section, iOS/iPadOS scope. Patterns, Components, and Inputs sections
are out of scope for this pass — see docs/architecture/domain-map.md.

## Primary Topics

- Accessibility (design-level)
- App Icons
- Branding
- Color
- Dark Mode
- Icons
- Images
- Inclusion
- Layout
- Materials
- Motion
- Privacy (design-level)
- Right to Left
- SF Symbols (design-level)
- Typography

## Used By

- knowledge/human-interface-guidelines/accessibility.md ([[knowledge/human-interface-guidelines/accessibility]])
- knowledge/human-interface-guidelines/app-icons.md ([[knowledge/human-interface-guidelines/app-icons]])
- knowledge/human-interface-guidelines/branding.md ([[knowledge/human-interface-guidelines/branding]])
- knowledge/human-interface-guidelines/color.md ([[knowledge/human-interface-guidelines/color]])
- knowledge/human-interface-guidelines/dark-mode.md ([[knowledge/human-interface-guidelines/dark-mode]])
- knowledge/human-interface-guidelines/icons.md ([[knowledge/human-interface-guidelines/icons]])
- knowledge/human-interface-guidelines/images.md ([[knowledge/human-interface-guidelines/images]])
- knowledge/human-interface-guidelines/inclusion.md ([[knowledge/human-interface-guidelines/inclusion]])
- knowledge/human-interface-guidelines/layout.md ([[knowledge/human-interface-guidelines/layout]])
- knowledge/human-interface-guidelines/materials.md ([[knowledge/human-interface-guidelines/materials]])
- knowledge/human-interface-guidelines/motion.md ([[knowledge/human-interface-guidelines/motion]])
- knowledge/human-interface-guidelines/privacy.md ([[knowledge/human-interface-guidelines/privacy]])
- knowledge/human-interface-guidelines/right-to-left.md ([[knowledge/human-interface-guidelines/right-to-left]])
- knowledge/human-interface-guidelines/sf-symbols.md ([[knowledge/human-interface-guidelines/sf-symbols]])
- knowledge/human-interface-guidelines/typography.md ([[knowledge/human-interface-guidelines/typography]])
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py references/apple/human-interface-guidelines.md --type reference`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add references/apple/human-interface-guidelines.md
git commit -m "feat: add human-interface-guidelines reference index"
```

---

## Task 2: Knowledge Contract — accessibility

**Files:**
- Create: `knowledge/human-interface-guidelines/accessibility.md`

- [ ] **Step 1: Create the file**

```markdown
# Accessibility (Design)

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.accessibility
type: knowledge
title: Accessibility (Design)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design-level accessibility requirements for iOS/iPadOS interfaces — text scaling, contrast, VoiceOver labeling, alternatives to gesture and color-only cues.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - accessibility
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/accessibility
depends_on: []
related:
  - knowledge.style-guide.writing-inclusively
  - knowledge.human-interface-guidelines.inclusion
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.typography
updated: 2026-07-31
```

## Intent

This contract defines the design-level accessibility rules an AI coding
agent must apply when laying out or reviewing an iOS/iPadOS interface —
text scaling, contrast, labeling, and non-visual/non-gesture
alternatives. It covers design decisions, not Accessibility API
implementation (VoiceOver traits, UIAccessibility properties), which
belongs to the future dedicated `accessibility` domain (see
docs/architecture/domain-map.md Cross-Domain Notes).

## Scope

### Included

-   Dynamic Type / text-scaling support in layout
-   Minimum color-contrast requirements
-   Not conveying information through color alone
-   Accessibility labels for custom icon-only controls
-   Alternatives to custom gestures
-   Avoiding time-boxed auto-dismissing UI

### Excluded

-   Accessibility API implementation details (VoiceOver traits, UIAccessibility) — future `accessibility` domain
-   Inclusive language/imagery — see `inclusion`
-   Color palette definition — see `color`

## Rules

### Rule 1

Agents MUST design layouts that support Dynamic Type / text scaling to
at least 200% without truncating or breaking primary content.

### Rule 2

Agents MUST ensure a minimum 4.5:1 contrast ratio between foreground
text/icons and their background; prefer system-defined colors, which
provide accessible variants automatically.

### Rule 3

Agents MUST NOT convey status, state, or differentiation using color
alone — pair color with a text label, icon, or shape.

### Rule 4

Agents MUST provide a meaningful accessibility label for every
custom icon-only control so VoiceOver can announce its purpose.

### Rule 5

Agents SHOULD provide a non-gesture alternative for any custom
gesture-based interaction (e.g., a visible button alongside a
swipe-to-dismiss action).

### Rule 6

Agents SHOULD avoid time-boxed UI elements that auto-dismiss on a
timer; prefer an explicit dismissal action instead.

## Compliant Example

-   ✓ An icon-only delete button has accessibility label "Delete." (Rule 4)
-   ✓ Success/failure state shown with both a color change and a checkmark/X icon. (Rule 3)
-   ✓ Body text reflows without truncation at the largest Dynamic Type size. (Rule 1)

## Non-Compliant Example

-   ✗ Icon-only button with no accessibility label — VoiceOver reads only "button." (Rule 4)
-   ✗ Success/failure indicated by a red or green dot alone. (Rule 3)
-   ✗ Fixed-size label that truncates at larger accessibility text sizes. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/accessibility.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/accessibility.md
git commit -m "feat: add human-interface-guidelines accessibility knowledge contract"
```

---

## Task 3: Knowledge Contract — app-icons

**Files:**
- Create: `knowledge/human-interface-guidelines/app-icons.md`

- [ ] **Step 1: Create the file**

```markdown
# App Icons

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.app-icons
type: knowledge
title: App Icons
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design requirements for iOS/iPadOS app icons — layered composition, unmasked shape, simplicity, and light/dark/tinted appearance variants.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - app-icon
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/app-icons
depends_on: []
related:
  - knowledge.human-interface-guidelines.icons
  - knowledge.human-interface-guidelines.branding
  - knowledge.human-interface-guidelines.color
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent designs or reviews an
iOS/iPadOS app icon: layer composition, shape/masking, simplicity, and
appearance variants. It is distinct from `icons` (in-UI interface
icons/glyphs) and `branding` (broader brand identity).

## Scope

### Included

-   Layered icon composition (background/foreground layers)
-   Unmasked square layer shape (the system applies corner masking)
-   Simplicity and optical centering
-   Prohibition on replicating Apple hardware
-   Text-in-icon guidance
-   Light/dark/tinted appearance variant consistency

### Excluded

-   In-UI interface icons/glyphs — see `icons`
-   SF Symbols selection/rendering — see `sf-symbols`
-   Broader brand voice/accent color — see `branding`

## Rules

### Rule 1

Agents MUST specify square, unmasked foreground/background layers for
iOS/iPadOS app icons — the system applies corner-radius masking; the
icon source MUST NOT pre-apply rounded corners.

### Rule 2

Agents MUST keep primary icon content optically centered so it isn't
truncated when the system applies masking.

### Rule 3

Agents SHOULD design a simple icon using a minimal number of shapes —
fine detail becomes illegible at small icon sizes.

### Rule 4

Agents MUST NOT depict replicas of Apple hardware products in an app
icon.

### Rule 5

Agents SHOULD avoid nonessential text in an app icon — text doesn't
localize or scale, and is often unreadable at small sizes.

### Rule 6

Agents SHOULD keep the icon's core visual features consistent across
default, dark, and tinted appearance variants rather than swapping
elements between them.

## Compliant Example

-   ✓ Icon uses one simple centered shape, square unmasked layers imported to Icon Composer. (Rules 1, 2, 3)
-   ✓ Dark and tinted variants use the same silhouette as the default icon, just recolored. (Rule 6)

## Non-Compliant Example

-   ✗ Icon source has corners pre-rounded before being handed to the system. (Rule 1)
-   ✗ Icon is packed with fine detail and includes the app's full name as text. (Rules 3, 5)
-   ✗ Dark variant uses an entirely different graphic than the default variant. (Rule 6)

## Dependencies

None.

## References

-   [Apple HIG — App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/app-icons.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/app-icons.md
git commit -m "feat: add human-interface-guidelines app-icons knowledge contract"
```

---

## Task 4: Knowledge Contract — branding

**Files:**
- Create: `knowledge/human-interface-guidelines/branding.md`

- [ ] **Step 1: Create the file**

```markdown
# Branding

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.branding
type: knowledge
title: Branding
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how an app's brand identity (voice, accent color, custom fonts, logo) appears in iOS/iPadOS UI without overriding platform conventions.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - branding
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/branding
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.typography
  - knowledge.style-guide.copyright-and-trademarks
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent expresses brand identity
in an iOS/iPadOS app — voice, accent color, custom fonts, logo
placement — while deferring to platform conventions and content.

## Scope

### Included

-   Brand voice/tone consistency (pointer to style-guide for exact wording)
-   Accent color usage
-   Custom font legibility/accessibility requirements
-   Logo placement restraint
-   Launch-screen branding restrictions
-   Apple trademark restrictions

### Excluded

-   Exact wording/copy rules — see style-guide domain
-   Color palette mechanics — see `color`
-   Font legibility/Dynamic Type mechanics — see `typography`

## Rules

### Rule 1

Agents SHOULD express brand voice/tone consistently in written copy
(defer exact wording rules to the `style-guide` domain).

### Rule 2

Agents MAY specify an app accent color applied to interface icons,
buttons, and text.

### Rule 3

If a custom font is used, agents MUST ensure it remains legible at all
sizes and supports Bold Text / Dynamic Type accessibility features.

### Rule 4

Agents MUST NOT use screen space purely to display a brand asset
(logo) at the expense of content and controls people care about.

### Rule 5

Agents MUST NOT use the launch screen as a branding surface. A
welcome/onboarding screen shown after launch is acceptable; the launch
screen itself is not.

### Rule 6

Agents MUST NOT display Apple trademarks in the app name or images.

## Compliant Example

-   ✓ Custom accent color applied to buttons and icons throughout the app. (Rule 2)
-   ✓ Logo appears once, in an About/Settings screen. (Rule 4)

## Non-Compliant Example

-   ✗ Logo repeated in every navigation bar as a persistent header element. (Rule 4)
-   ✗ Launch screen decorated with marketing copy and animation. (Rule 5)
-   ✗ Custom font ships with no Bold Text / Dynamic Type support. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Branding](https://developer.apple.com/design/human-interface-guidelines/branding)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/branding.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/branding.md
git commit -m "feat: add human-interface-guidelines branding knowledge contract"
```

---

## Task 5: Knowledge Contract — color

**Files:**
- Create: `knowledge/human-interface-guidelines/color.md`

- [ ] **Step 1: Create the file**

```markdown
# Color

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.color
type: knowledge
title: Color
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using system and custom color in iOS/iPadOS interfaces — consistency, contrast, semantic meaning, and wide-color support.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - color
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/color
depends_on: []
related:
  - knowledge.human-interface-guidelines.dark-mode
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.materials
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent selects and applies color
in an iOS/iPadOS interface: consistency of meaning, contrast, semantic
system colors, and avoiding color as the sole information channel.

## Scope

### Included

-   Consistent meaning of a given color across the interface
-   Light/dark/increased-contrast variants for custom colors
-   Avoiding hard-coded system color values
-   Semantic meaning of dynamic system colors
-   Color as a non-exclusive information channel
-   iOS/iPadOS background-color hierarchy (system vs. grouped)

### Excluded

-   Dark Mode-specific contrast ratios and base/elevated backgrounds — see `dark-mode`
-   Color-blindness/contrast accessibility minimums — see `accessibility`
-   Liquid Glass material color behavior — see `materials`

## Rules

### Rule 1

Agents MUST use a given color consistently for the same meaning
throughout the interface (don't reuse a status color for decoration
elsewhere).

### Rule 2

Agents MUST supply light, dark, and increased-contrast variants for
any custom color; prefer system-provided dynamic colors, which already
define these variants.

### Rule 3

Agents MUST NOT hard-code system color values — reference them via
platform APIs (e.g., SwiftUI `Color`, UIKit `UIColor`) so they track
OS updates.

### Rule 4

Agents MUST NOT redefine the semantic meaning of a dynamic system
color (e.g., don't use the separator color as body text color).

### Rule 5

Agents MUST NOT rely on color alone to convey information — pair with
text, shape, or icon (see `accessibility` Rule 3).

### Rule 6

Agents SHOULD use the grouped background-color set for grouped table
views, and the system background-color set otherwise, using
primary/secondary/tertiary variants to convey hierarchy.

## Compliant Example

-   ✓ A custom brand color ships with light, dark, and increased-contrast variants. (Rule 2)
-   ✓ A status indicator uses color plus an icon together. (Rule 5)

## Non-Compliant Example

-   ✗ A `UIColor` value is hard-coded as a hex literal in code. (Rule 3)
-   ✗ The system separator color is reused as a body text color. (Rule 4)
-   ✗ Success/failure is shown via a colored dot with no accompanying icon or text. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/color.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/color.md
git commit -m "feat: add human-interface-guidelines color knowledge contract"
```

---

## Task 6: Knowledge Contract — dark-mode

**Files:**
- Create: `knowledge/human-interface-guidelines/dark-mode.md`

- [ ] **Step 1: Create the file**

```markdown
# Dark Mode

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.dark-mode
type: knowledge
title: Dark Mode
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requirements for supporting the systemwide Dark Mode appearance setting on iOS/iPadOS, including contrast minimums and background-color layering.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - dark-mode
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/dark-mode
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.materials
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent supports the systemwide
Dark Mode appearance setting on iOS/iPadOS: mandatory systemwide
adherence, contrast minimums in both appearances, and iOS/iPadOS's
base/elevated background-color layering.

## Scope

### Included

-   Prohibition on app-specific appearance overrides
-   Legibility in both Light and Dark, including Increase Contrast / Reduce Transparency
-   Minimum contrast ratios in both appearances
-   iOS/iPadOS base/elevated background-color layering
-   Icon/image adaptation across appearances

### Excluded

-   General color-consistency rules — see `color`
-   Material/vibrancy mechanics — see `materials`
-   Non-color-related accessibility rules — see `accessibility`

## Rules

### Rule 1

Agents MUST NOT offer an app-specific appearance override that ignores
the systemwide Light/Dark/Auto setting.

### Rule 2

Agents MUST ensure content remains legible in both Light and Dark
appearance, including with Increase Contrast and Reduce Transparency
turned on.

### Rule 3

Agents MUST maintain at least a 4.5:1 contrast ratio between
foreground and background in both appearances, targeting 7:1 for small
custom text.

### Rule 4

Agents SHOULD use semantic/dynamic colors (e.g., `label`,
`secondaryLabel`) that adapt automatically rather than defining
separate hard-coded light/dark palettes.

### Rule 5

Agents SHOULD prefer system background colors (base/elevated) on
iOS/iPadOS so the system can convey correct depth between layered
interfaces (popovers, sheets).

### Rule 6

Agents SHOULD use SF Symbols and vibrancy for icons so they adapt
automatically between appearances, rather than shipping separate
light/dark icon assets unless a design genuinely requires it.

## Compliant Example

-   ✓ App uses `Color(.label)` / system background colors and renders correctly when the system switches Light→Dark automatically. (Rules 1, 4)

## Non-Compliant Example

-   ✗ App ships its own in-app Light/Dark toggle that ignores the system setting. (Rule 1)
-   ✗ A white content-background image glows against the surrounding Dark Mode context because it wasn't adjusted. (Rule 2)

## Dependencies

None.

## References

-   [Apple HIG — Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/dark-mode.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/dark-mode.md
git commit -m "feat: add human-interface-guidelines dark-mode knowledge contract"
```

---

## Task 7: Knowledge Contract — icons

**Files:**
- Create: `knowledge/human-interface-guidelines/icons.md`

- [ ] **Step 1: Create the file**

```markdown
# Icons (Interface Icons)

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.icons
type: knowledge
title: Icons (Interface Icons)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design rules for in-UI interface icons/glyphs (toolbars, tab bars, buttons) on iOS/iPadOS, distinct from the app icon itself.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - icons
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/icons
depends_on: []
related:
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.right-to-left
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent designs or chooses
in-UI interface icons/glyphs on iOS/iPadOS — consistency, symbol
preference, accessibility labeling, and vector format. It is distinct
from `app-icons` (the Home Screen app icon).

## Scope

### Included

-   Recognizability and simplicity of interface icons
-   Visual consistency (size, stroke weight, perspective) across an app's icon set
-   Preference for SF Symbols over fully custom icons
-   Accessibility labels for custom icons
-   Vector-format requirement for custom icons

### Excluded

-   The Home Screen app icon — see `app-icons`
-   SF Symbols rendering modes/animation — see `sf-symbols`
-   RTL-specific icon flipping rules — see `right-to-left`

## Rules

### Rule 1

Agents SHOULD design interface icons using simple, highly recognizable
shapes based on familiar visual metaphors.

### Rule 2

Agents MUST maintain consistent size, stroke weight, and perspective
across all interface icons within one app.

### Rule 3

Agents SHOULD prefer SF Symbols over fully custom icons where an
appropriate symbol exists, for automatic weight/scale matching with
adjacent text.

### Rule 4

Agents MUST provide an accessibility label for every custom interface
icon so VoiceOver can announce its purpose.

### Rule 5

Agents MUST use a vector format (PDF/SVG) for custom interface icons
so the system can scale them for all resolutions and Dynamic Type
sizes.

### Rule 6

Agents MUST NOT depict replicas of Apple hardware products in
interface icons.

## Compliant Example

-   ✓ All toolbar icons share the same stroke weight and use SF Symbols where possible, each with an accessibility label. (Rules 2, 3, 4)

## Non-Compliant Example

-   ✗ A mixed icon set has inconsistent stroke weights between custom and system icons. (Rule 2)
-   ✗ A raster-only custom icon pixelates at large Dynamic Type sizes. (Rule 5)
-   ✗ A custom icon has no accessibility label. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Icons](https://developer.apple.com/design/human-interface-guidelines/icons)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/icons.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/icons.md
git commit -m "feat: add human-interface-guidelines icons knowledge contract"
```

---

## Task 8: Knowledge Contract — images

**Files:**
- Create: `knowledge/human-interface-guidelines/images.md`

- [ ] **Step 1: Create the file**

```markdown
# Images

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.images
type: knowledge
title: Images
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for delivering bitmap image assets at the correct resolution and color profile across iOS/iPadOS devices.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - images
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/images
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.icons
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent delivers bitmap image
assets for iOS/iPadOS — scale-factor variants, color profiles, and
device testing — so images render correctly across the full range of
display densities.

## Scope

### Included

-   @1x/@2x/@3x scale-factor asset delivery
-   Designing at low resolution and scaling up
-   Embedded color profiles
-   Wide-color (Display P3) usage
-   On-device testing of image assets

### Excluded

-   Color palette/profile selection rationale — see `color`
-   Vector interface icon format rules — see `icons`

## Rules

### Rule 1

Agents MUST provide @1x/@2x/@3x scale-factor variants (as applicable)
for every bitmap image asset, named accordingly in the asset catalog.

### Rule 2

Agents SHOULD design at the lowest resolution and scale up to produce
higher-resolution variants, aligning vector control points to whole
values at 1x.

### Rule 3

Agents MUST embed a color profile with each image so colors render
correctly across displays.

### Rule 4

Agents SHOULD use the Display P3 color profile for wide-color images
on compatible displays, exporting as PNG for lossless quality.

### Rule 5

Agents MUST test images on actual devices — an image that looks
correct at design time can appear pixelated or stretched on-device.

## Compliant Example

-   ✓ An image asset ships @1x/@2x/@3x variants with an embedded sRGB or P3 color profile as appropriate. (Rules 1, 3, 4)

## Non-Compliant Example

-   ✗ A single-resolution PNG is reused for all scale factors, appearing blurry on high-density displays. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Images](https://developer.apple.com/design/human-interface-guidelines/images)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/images.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/images.md
git commit -m "feat: add human-interface-guidelines images knowledge contract"
```

---

## Task 9: Knowledge Contract — inclusion

**Files:**
- Create: `knowledge/human-interface-guidelines/inclusion.md`

- [ ] **Step 1: Create the file**

```markdown
# Inclusion

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.inclusion
type: knowledge
title: Inclusion
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines requirements for inclusive language, imagery, and representation in iOS/iPadOS app content, distinct from style-guide's word-level inclusive-writing rules.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - inclusion
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/inclusion
depends_on: []
related:
  - knowledge.style-guide.writing-inclusively
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent designs inclusive app
content — plain and direct language, gender-neutral phrasing,
non-stereotypical representation, and localization-friendly copy — as
a design/content-strategy concern. Word-level inclusive-writing rules
(specific banned/preferred terms) belong to
`knowledge.style-guide.writing-inclusively`.

## Scope

### Included

-   Plain, direct address ("you"/"your" vs. "the user")
-   Avoiding unnecessary gender references in copy, avatars, glyphs
-   Avoiding stereotypical representation of people/occupations
-   Range of human characteristics in imagery
-   Avoiding colloquial/untranslatable expressions
-   Treating accessibility support as part of inclusion

### Excluded

-   Specific banned/preferred terminology — see `knowledge.style-guide.writing-inclusively`
-   Accessibility API/contrast mechanics — see `accessibility`

## Rules

### Rule 1

Agents MUST use plain, direct language and address people as
"you"/"your" rather than "the user."

### Rule 2

Agents MUST avoid unnecessary gender references in copy, avatars, and
glyphs; prefer gender-neutral phrasing and SF Symbols' nongendered
figures.

### Rule 3

Agents MUST NOT rely on stereotypical representations (e.g., only male
doctors, only female nurses) when depicting people or occupations.

### Rule 4

Agents SHOULD portray a range of human characteristics (age, race,
body type, ability) when representing people in imagery.

### Rule 5

Agents MUST avoid colloquial expressions and undefined technical
jargon that don't translate or localize well.

### Rule 6

Agents MUST treat support for Apple accessibility features (VoiceOver,
Switch Control, Display Accommodations) as part of inclusive design,
not a separate concern.

## Compliant Example

-   ✓ Copy reads "Subscribers can post recipes to your shared folder" instead of gendered pronouns. (Rule 2)
-   ✓ A security-question prompt uses a universal question like "What's your favorite activity?" (Rule 5)

## Non-Compliant Example

-   ✗ Copy uses "he or she" pronouns throughout. (Rule 2)
-   ✗ A security question assumes a specific cultural context ("What was the make of your first car?"). (Rule 5)
-   ✗ Imagery depicting a task shows only one demographic performing it. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/inclusion.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/inclusion.md
git commit -m "feat: add human-interface-guidelines inclusion knowledge contract"
```

---

## Task 10: Knowledge Contract — layout

**Files:**
- Create: `knowledge/human-interface-guidelines/layout.md`

- [ ] **Step 1: Create the file**

```markdown
# Layout

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.layout
type: knowledge
title: Layout
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for structuring and adapting iOS/iPadOS interface layout — grouping, hierarchy, safe areas, and adaptability to size/orientation changes.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - layout
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/layout
depends_on: []
related:
  - knowledge.human-interface-guidelines.typography
  - knowledge.human-interface-guidelines.right-to-left
  - knowledge.human-interface-guidelines.materials
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent structures and adapts
iOS/iPadOS interface layout: safe areas, visual hierarchy, grouping,
and responding to device size, orientation, and multitasking changes.

## Scope

### Included

-   Safe-area and system-chrome respect
-   Dynamic Type-driven layout adaptability
-   Reading-order/visual-hierarchy placement
-   Grouping related content with spacing/materials
-   iPad multitasking size adaptability
-   Full-bleed background/content extension

### Excluded

-   RTL-specific mirroring rules — see `right-to-left`
-   Material/blur mechanics used for grouping — see `materials`
-   Typographic hierarchy mechanics — see `typography`

## Rules

### Rule 1

Agents MUST respect system-defined safe areas so content doesn't
collide with device features (Dynamic Island, camera housing) or
system chrome (toolbars, tab bars).

### Rule 2

Agents MUST support Dynamic Type text-size changes without truncating
or breaking the layout of primary content.

### Rule 3

Agents SHOULD place the most important content near the top/leading
edge, respecting reading order (including RTL contexts — see
`right-to-left`).

### Rule 4

Agents SHOULD group related items visually (spacing, separators,
materials) while keeping content and controls clearly distinct.

### Rule 5

Agents MUST test layout at all standard iPad multitasking sizes
(halves, thirds, quadrants) and both iPhone orientations if supported,
ensuring smooth transitions between sizes.

### Rule 6

Agents SHOULD extend backgrounds and scrollable content to the edges
of the display, layering controls (sidebars, tab bars) on top rather
than sharing the same plane as content.

## Compliant Example

-   ✓ Layout adapts from full iPad width down to compact Slide Over width without clipping content. (Rule 5)
-   ✓ Content respects safe areas around the Dynamic Island. (Rule 1)

## Non-Compliant Example

-   ✗ A fixed-width layout clips content in iPad Slide Over. (Rule 5)
-   ✗ Custom UI is drawn underneath the status bar / Dynamic Island. (Rule 1)

## Dependencies

None.

## References

-   [Apple HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/layout.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/layout.md
git commit -m "feat: add human-interface-guidelines layout knowledge contract"
```

---

## Task 11: Knowledge Contract — materials

**Files:**
- Create: `knowledge/human-interface-guidelines/materials.md`

- [ ] **Step 1: Create the file**

```markdown
# Materials

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.materials
type: knowledge
title: Materials
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when and how to use Liquid Glass and standard materials (blur/vibrancy) to create visual hierarchy between controls and content on iOS/iPadOS.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - materials
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/materials
depends_on: []
related:
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.layout
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent applies Liquid Glass and
standard materials on iOS/iPadOS: which layer (controls vs. content)
each belongs to, variant selection, and vibrant-color pairing.

## Scope

### Included

-   Liquid Glass vs. standard-material layer boundaries (controls vs. content)
-   Liquid Glass variant selection (regular vs. clear)
-   Vibrant color usage on top of materials
-   Standard material (ultra-thin/thin/regular/thick) selection

### Excluded

-   Color definition/contrast rules themselves — see `color`
-   Layout grouping mechanics beyond material choice — see `layout`

## Rules

### Rule 1

Agents MUST NOT use Liquid Glass in the content layer — reserve it for
the controls/navigation layer (tab bars, sidebars, toolbars).

### Rule 2

Agents SHOULD use Liquid Glass effects sparingly on custom controls —
limit to the most important functional elements.

### Rule 3

Agents SHOULD choose the "regular" Liquid Glass variant when
background content risks legibility issues, and the "clear" variant
only over visually rich media backgrounds (photos/video).

### Rule 4

Agents MUST use vibrant, system-defined colors on top of materials
rather than arbitrary colors, so contrast remains correct
automatically.

### Rule 5

Agents SHOULD select a standard material (ultra-thin/thin/regular/
thick) based on semantic meaning and required contrast, not its
apparent tint.

## Compliant Example

-   ✓ A tab bar uses Liquid Glass while content scrolls beneath it. (Rule 1)
-   ✓ A photo viewer's floating controls use the clear Liquid Glass variant over rich media. (Rule 3)

## Non-Compliant Example

-   ✗ Liquid Glass is applied to a content-layer card, competing visually with the tab bar. (Rule 1)
-   ✗ An arbitrary non-vibrant color is used for text drawn on a blurred material. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/materials.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/materials.md
git commit -m "feat: add human-interface-guidelines materials knowledge contract"
```

---

## Task 12: Knowledge Contract — motion

**Files:**
- Create: `knowledge/human-interface-guidelines/motion.md`

- [ ] **Step 1: Create the file**

```markdown
# Motion

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.motion
type: knowledge
title: Motion
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for using animation and motion purposefully in iOS/iPadOS interfaces, including Reduce Motion accessibility support.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - motion
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/motion
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.sf-symbols
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent uses motion/animation
purposefully on iOS/iPadOS: pairing motion with non-motion cues,
supporting Reduce Motion, and keeping feedback animations brief,
interruptible, and gesture-consistent.

## Scope

### Included

-   Motion as a non-exclusive information channel
-   Reduce Motion accessibility-setting response
-   Brevity and precision of feedback animation
-   Interruptibility of animation
-   Gesture-consistent motion physics

### Excluded

-   SF Symbol-specific animation types — see `sf-symbols`
-   General accessibility rules unrelated to motion — see `accessibility`

## Rules

### Rule 1

Agents MUST NOT use motion as the only way to communicate important
information — pair it with a visual or textual cue.

### Rule 2

Agents MUST respond to the Reduce Motion accessibility setting by
reducing or removing automatic/repetitive animation (zooming, scaling,
peripheral motion) when it's turned on.

### Rule 3

Agents SHOULD keep feedback animations brief and precise rather than
long or elaborate.

### Rule 4

Agents MUST let people cancel or interrupt an animation rather than
blocking interaction until it completes.

### Rule 5

Agents SHOULD make motion follow realistic, gesture-consistent physics
(e.g., a view dismissed by swiping down shouldn't be reopened by
swiping sideways).

## Compliant Example

-   ✓ A card transition responds to Reduce Motion by cross-fading instead of scaling/zooming. (Rule 2)
-   ✓ People can tap through an in-progress animation to proceed immediately. (Rule 4)

## Non-Compliant Example

-   ✗ A decorative parallax animation plays regardless of the Reduce Motion setting. (Rule 2)
-   ✗ An animated onboarding sequence can't be skipped or interrupted. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/motion.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/motion.md
git commit -m "feat: add human-interface-guidelines motion knowledge contract"
```

---

## Task 13: Knowledge Contract — privacy

**Files:**
- Create: `knowledge/human-interface-guidelines/privacy.md`

- [ ] **Step 1: Create the file**

```markdown
# Privacy (Design)

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.privacy
type: knowledge
title: Privacy (Design)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines design-level rules for requesting permissions and communicating data use in iOS/iPadOS interfaces — UI and consent-flow patterns, not the Privacy Manifest/data-use-disclosure implementation.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - privacy
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/privacy
depends_on: []
related: []
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent designs permission-request
UI and consent flows on iOS/iPadOS: when to ask, what the purpose
string must say, and what custom pre-permission screens may and may
not do. It does not cover the Privacy Manifest / data-use-disclosure
implementation, which belongs to the future dedicated `privacy` domain
(see docs/architecture/domain-map.md Cross-Domain Notes).

## Scope

### Included

-   Timing of permission requests (just-in-time vs. launch-time)
-   Purpose-string wording requirements
-   Custom pre-permission screen constraints
-   Tracking-permission-alert integrity rules
-   Lightweight permission surfaces (e.g., location button)

### Excluded

-   Privacy Manifest file contents / data-use disclosure — future `privacy` domain
-   Keychain/credential storage — future `security` domain

## Rules

### Rule 1

Agents MUST request access only to data a specific feature actually
needs, and only when the person is about to use that feature (not at
launch, unless the launch-time need is obvious, e.g. a navigation
app's location access).

### Rule 2

Agents MUST write a purpose string that clearly and specifically
explains why the app needs the requested access, in sentence case,
ending with a period.

### Rule 3

If showing a custom pre-permission screen, agents MUST include only
one button that clearly opens the system alert (label it "Continue" or
"Next," never "Allow") and MUST NOT offer a way to dismiss the screen
without seeing the system alert.

### Rule 4

Agents MUST NOT precede the system tracking-permission alert with a
custom screen designed to confuse or mislead — App Store review
rejects this pattern.

### Rule 5

Agents SHOULD prefer a one-time, lightweight permission surface (e.g.,
the Core Location location button) over the full system prompt when
the use case fits.

## Compliant Example

-   ✓ A maps feature requests location only after the person taps "Share my location," with a purpose string explaining the specific use. (Rules 1, 2)
-   ✓ A custom pre-permission screen has one "Continue" button that opens the system alert. (Rule 3)

## Non-Compliant Example

-   ✗ The app requests camera, contacts, and location access at first launch before any feature needs them. (Rule 1)
-   ✗ A custom pre-permission screen includes a "Skip" option that bypasses the system alert. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/privacy.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/privacy.md
git commit -m "feat: add human-interface-guidelines privacy knowledge contract"
```

---

## Task 14: Knowledge Contract — right-to-left

**Files:**
- Create: `knowledge/human-interface-guidelines/right-to-left.md`

- [ ] **Step 1: Create the file**

```markdown
# Right to Left

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.right-to-left
type: knowledge
title: Right to Left
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for adapting iOS/iPadOS interfaces to right-to-left (RTL) languages such as Arabic and Hebrew — layout mirroring, numerals, and icon flipping.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - right-to-left
  - rtl
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/right-to-left
depends_on: []
related:
  - knowledge.human-interface-guidelines.layout
  - knowledge.human-interface-guidelines.sf-symbols
  - knowledge.style-guide.international-style
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent adapts an iOS/iPadOS
interface for right-to-left (RTL) languages: layout mirroring, numeral
ordering, and which icons/images flip versus stay fixed.

## Scope

### Included

-   Layout direction mirroring
-   Digit-order preservation within a number
-   Flipping of directional controls
-   Non-flipping of images, logos, universal symbols
-   Interface-icon flip rules (text/motion vs. real-world objects)
-   Paragraph vs. short-text alignment rules

### Excluded

-   General layout/hierarchy rules unrelated to direction — see `layout`
-   SF Symbols' built-in RTL variant mechanics — see `sf-symbols`
-   Locale-specific number/date formatting text rules — see style-guide `international-style`/`international-formatting`

## Rules

### Rule 1

Agents MUST mirror layout direction for RTL languages when not already
using system-provided components that flip automatically.

### Rule 2

Agents MUST NOT reverse the digit order within a specific number
(phone numbers, "541") regardless of language direction.

### Rule 3

Agents MUST flip directional controls (back button, progress bars,
next/previous) to match RTL reading order.

### Rule 4

Agents MUST NOT flip images, logos, or universal symbols (e.g.,
checkmarks) — flipping can change or violate their meaning.

### Rule 5

Agents SHOULD flip interface icons that represent text/reading
direction or forward/backward motion, but MUST NOT flip icons that
depict real-world objects (e.g., a clock) unless directionality is the
point of the icon.

### Rule 6

Agents SHOULD align a paragraph (3+ lines) to match its language, while
short 1–2 line text blocks may follow the current UI context direction.

## Compliant Example

-   ✓ The back button points right in an RTL layout. (Rule 3)
-   ✓ A phone number's digits stay in their original order under RTL. (Rule 2)

## Non-Compliant Example

-   ✗ An app logo is mirrored in an RTL locale. (Rule 4)
-   ✗ A "541" balance is reversed to "145" under RTL. (Rule 2)
-   ✗ The back button still points left in an RTL layout. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — Right to Left](https://developer.apple.com/design/human-interface-guidelines/right-to-left)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/right-to-left.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/right-to-left.md
git commit -m "feat: add human-interface-guidelines right-to-left knowledge contract"
```

---

## Task 15: Knowledge Contract — sf-symbols

**Files:**
- Create: `knowledge/human-interface-guidelines/sf-symbols.md`

- [ ] **Step 1: Create the file**

```markdown
# SF Symbols (Design)

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.sf-symbols
type: knowledge
title: SF Symbols (Design)
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when and how to choose, compose, and style SF Symbols within an iOS/iPadOS design — rendering modes, weights/scales, and variants.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - sf-symbols
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/sf-symbols
depends_on: []
related:
  - knowledge.human-interface-guidelines.icons
  - knowledge.human-interface-guidelines.color
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent selects and styles SF
Symbols within an iOS/iPadOS design — rendering mode, weight/scale
matching, and fill vs. outline variant choice. It covers the design
angle; API-level rendering/animation implementation belongs to the
future dedicated `sf-symbols` domain (see docs/architecture/domain-map.md
Cross-Domain Notes).

## Scope

### Included

-   Rendering-mode selection (monochrome/hierarchical/palette/multicolor)
-   System color usage with symbols for automatic adaptation
-   Weight/scale matching with adjacent text
-   Fill vs. outline variant selection by context
-   Custom-symbol restrictions (no Apple product replicas)
-   Accessibility labeling for custom symbols

### Excluded

-   API-level rendering/animation implementation — future `sf-symbols` domain
-   General interface-icon consistency rules unrelated to SF Symbols specifically — see `icons`

## Rules

### Rule 1

Agents SHOULD choose a rendering mode (monochrome, hierarchical,
palette, multicolor) based on the symbol's meaning and context, and
verify legibility at the actual display size rather than assuming the
automatic setting is always correct.

### Rule 2

Agents MUST use system-provided colors with symbols so they adapt
automatically to accessibility settings and Dark Mode.

### Rule 3

Agents SHOULD match a symbol's weight to adjacent text weight, and use
scale (small/medium/large) to adjust emphasis without breaking that
weight match.

### Rule 4

Agents SHOULD choose the fill variant for higher-emphasis contexts
(selected tab bar items, swipe actions) and the outline variant when
the symbol appears alongside text in lists or toolbars.

### Rule 5

Agents MUST NOT design a custom symbol that replicates an Apple
product, or customize a symbol SF Symbols already marks as
representing an Apple feature.

### Rule 6

Agents MUST provide an accessibility label for any custom symbol, same
as for a custom interface icon (see `icons` Rule 4).

## Compliant Example

-   ✓ A tab bar uses filled SF Symbol variants for the selected state and outline variants for unselected, all tinted with the system accent color. (Rules 2, 4)

## Non-Compliant Example

-   ✗ A custom symbol hard-codes a non-adaptive color that doesn't respond to Dark Mode. (Rule 2)
-   ✗ Two icons in the same toolbar use mismatched stroke weights because one is a raster import instead of an SF Symbol. (Rule 3)

## Dependencies

None.

## References

-   [Apple HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/sf-symbols.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/sf-symbols.md
git commit -m "feat: add human-interface-guidelines sf-symbols knowledge contract"
```

---

## Task 16: Knowledge Contract — typography

**Files:**
- Create: `knowledge/human-interface-guidelines/typography.md`

- [ ] **Step 1: Create the file**

```markdown
# Typography

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.typography
type: knowledge
title: Typography
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for typographic choices in iOS/iPadOS interfaces — legibility, hierarchy, system fonts, and Dynamic Type support.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - typography
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/typography
depends_on: []
related:
  - knowledge.human-interface-guidelines.layout
  - knowledge.human-interface-guidelines.accessibility
updated: 2026-07-31
```

## Intent

This contract defines how an AI coding agent makes typographic
choices in an iOS/iPadOS interface: legibility, text-style hierarchy,
system vs. custom fonts, and Dynamic Type support.

## Scope

### Included

-   Font-size/weight legibility minimums
-   Use of built-in text styles for hierarchy
-   Typeface-count minimization
-   Custom font accessibility parity with system fonts
-   Dynamic Type layout adaptability
-   Prioritizing which content scales at large accessibility sizes

### Excluded

-   Exact copy wording — see style-guide domain
-   Layout adaptability beyond text — see `layout`
-   Contrast/color rules for text — see `color`, `accessibility`

## Rules

### Rule 1

Agents MUST support Dynamic Type so people can scale visible text via
system text-size settings; layout MUST remain legible at the largest
accessibility sizes.

### Rule 2

Agents SHOULD use built-in text styles (body, headline, etc.) rather
than fixed point sizes, so hierarchy and scaling stay consistent
automatically.

### Rule 3

Agents MUST avoid ultralight/thin font weights for any text that must
stay legible at small sizes; prefer Regular, Medium, Semibold, or Bold.

### Rule 4

Agents SHOULD minimize the number of typefaces used in one interface
to preserve a clear information hierarchy.

### Rule 5

If a custom font is used, agents MUST implement the same Dynamic Type
/ Bold Text accessibility behavior that system fonts provide
automatically.

### Rule 6

Agents SHOULD prioritize which content actually needs to grow at
larger text sizes (e.g., primary content) rather than scaling every
element uniformly.

## Compliant Example

-   ✓ Body text uses the system `body` text style and reflows correctly at the largest accessibility text size. (Rules 1, 2)
-   ✓ A custom display font still responds to Bold Text. (Rule 5)

## Non-Compliant Example

-   ✗ An interface hard-codes a fixed 14pt label that doesn't grow with Dynamic Type. (Rule 1)
-   ✗ A custom font ships without Dynamic Type support and truncates at larger sizes. (Rule 5)

## Dependencies

None.

## References

-   [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/typography.md --type knowledge`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add knowledge/human-interface-guidelines/typography.md
git commit -m "feat: add human-interface-guidelines typography knowledge contract"
```

---

## Task 17: Native Skill

**Files:**
- Create: `skills/human-interface-guidelines/SKILL.md`

- [ ] **Step 1: Create the file**

```markdown
---
name: human-interface-guidelines
description: Route Human Interface Guidelines (Foundations) design tasks to the correct Knowledge Contracts — layout, color, typography, dark mode, materials, motion, app icons, interface icons, images, branding, accessibility design, inclusion, privacy-design permission UI, SF Symbols usage, and right-to-left support. Use when designing or reviewing iOS/iPadOS UI, choosing colors or fonts, laying out a screen, picking icons or symbols, supporting Dark Mode or RTL, or designing permission-request flows (design pattern, not the wording itself — see style-guide for wording). Triggers on HIG, human interface guidelines, layout, color, dark mode, typography, materials, Liquid Glass, motion, animation, app icon, interface icon, SF Symbols, branding, accent color, accessibility design, inclusive design, RTL, right-to-left, permission prompt design, safe area, Dynamic Type.
id: skill.human-interface-guidelines.foundations
title: Human Interface Guidelines — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Human Interface Guidelines
routes: [knowledge.human-interface-guidelines.accessibility, knowledge.human-interface-guidelines.app-icons, knowledge.human-interface-guidelines.branding, knowledge.human-interface-guidelines.color, knowledge.human-interface-guidelines.dark-mode, knowledge.human-interface-guidelines.icons, knowledge.human-interface-guidelines.images, knowledge.human-interface-guidelines.inclusion, knowledge.human-interface-guidelines.layout, knowledge.human-interface-guidelines.materials, knowledge.human-interface-guidelines.motion, knowledge.human-interface-guidelines.privacy, knowledge.human-interface-guidelines.right-to-left, knowledge.human-interface-guidelines.sf-symbols, knowledge.human-interface-guidelines.typography]
related:
  - skill.style-guide.writing
last_updated: 2026-07-31
---

# Human Interface Guidelines — Foundations Skill

## Purpose

Route iOS/iPadOS design-guidance tasks to the minimum required Human
Interface Guidelines Foundations Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/human-interface-guidelines/.

-   Visual identity, iconography assets -> branding.md, app-icons.md, icons.md, images.md
-   Color & appearance -> color.md, dark-mode.md
-   Layout & structure -> layout.md, right-to-left.md
-   Typography -> typography.md
-   Materials & motion -> materials.md, motion.md
-   Accessibility & inclusion (design-level) -> accessibility.md, inclusion.md
-   Privacy (design-level, permission-request UI patterns) -> privacy.md
-   Symbol design system -> sf-symbols.md

Never load more than the contracts relevant to the specific question.
For UI copy wording (not visual design), route to
`skill.style-guide.writing` instead.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/human-interface-guidelines/ — do not guess or
fall back to general knowledge. HIG Patterns, Components, and Inputs
sections are out of scope for this skill (see
docs/architecture/domain-map.md) — report that explicitly rather than
answering from general knowledge.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate_artifact.py skills/human-interface-guidelines/SKILL.md --type skill`
Expected: `PASS`

- [ ] **Step 3: Commit**

```bash
git add skills/human-interface-guidelines/SKILL.md
git commit -m "feat: add human-interface-guidelines native skill"
```

---

## Task 18: Update skills/index.md

**Files:**
- Modify: `skills/index.md`

- [ ] **Step 1: Add a Discovery Rules row**

In the `## Discovery Rules` table, add this row after the existing
`style-guide` row:

```markdown
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design | skills/human-interface-guidelines/SKILL.md |
```

The full table becomes:

```markdown
| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/SKILL.md |
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/SKILL.md |
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design | skills/human-interface-guidelines/SKILL.md |
```

- [ ] **Step 2: Commit**

```bash
git add skills/index.md
git commit -m "docs: register human-interface-guidelines skill in skills index"
```

---

## Task 19: Update domain-map.md

**Files:**
- Modify: `docs/architecture/domain-map.md`

- [ ] **Step 1: Update the Initial Scope cell for the human-interface-guidelines row**

In the `## Tier 1 — Must-Have` table, replace the
`human-interface-guidelines` row's **Initial Scope** and **Owns** cells:

Old:
```markdown
| Human Interface Guidelines | human-interface-guidelines | Visual/UX design patterns, layout, interaction | Layout patterns, interaction conventions, visual design guidance |
```

New:
```markdown
| Human Interface Guidelines | human-interface-guidelines | Foundations (iOS/iPadOS): layout, color, typography, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL. Patterns/Components/Inputs deferred — see Cross-Domain Notes. | Foundations-layer visual/UX design guidance for iOS/iPadOS (layout, color, typography, materials, motion, iconography, branding, accessibility-design, privacy-design, RTL) |
```

- [ ] **Step 2: Add three Cross-Domain Notes entries**

At the end of the `## Cross-Domain Notes` list, add:

```markdown
- `human-interface-guidelines` (`accessibility` Foundations topic) and the future `accessibility` domain (Tier 1, unbuilt) overlap: HIG's angle is design guidance (Dynamic Type, contrast, VoiceOver-friendly layout), the dedicated domain's angle is API implementation. Boundary not yet resolved — decide when `accessibility` is built.
- `human-interface-guidelines` (`privacy` Foundations topic) and the future `privacy` domain (Tier 2, unbuilt) overlap: HIG's angle is permission-request UI/consent-flow design, the dedicated domain's angle is Privacy Manifest / data-use disclosure implementation. Boundary not yet resolved — decide when `privacy` is built.
- `human-interface-guidelines` (`sf-symbols` Foundations topic) and the future `sf-symbols` domain (Tier 1, unbuilt) overlap: HIG's angle is symbol selection/composition in a design, the dedicated domain's angle is API usage and rendering modes. Boundary not yet resolved — decide when `sf-symbols` is built.
```

- [ ] **Step 3: Update the Build Order "Completed" line**

Replace:
```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision).
```

With:
```markdown
Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt).
```

- [ ] **Step 4: Bump the version**

Change `Version: 0.4.0` to `Version: 0.5.0`.

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/domain-map.md
git commit -m "docs: mark human-interface-guidelines Foundations complete, add cross-domain overlap notes"
```

---

## Task 20: Full validation pass

**Files:** None created/modified — verification only.

- [ ] **Step 1: Run the full unit test suite**

Run: `python3 -m unittest tests/test_validate_artifact.py -v`
Expected: all tests pass, no regressions (same count as before this
project — this project doesn't touch the validator or its tests).

- [ ] **Step 2: Validate every new artifact individually**

Run:
```bash
python3 scripts/validate_artifact.py references/apple/human-interface-guidelines.md --type reference
for f in accessibility app-icons branding color dark-mode icons images inclusion layout materials motion privacy right-to-left sf-symbols typography; do
  python3 scripts/validate_artifact.py knowledge/human-interface-guidelines/$f.md --type knowledge
done
python3 scripts/validate_artifact.py skills/human-interface-guidelines/SKILL.md --type skill
```
Expected: `PASS` for all 17 files.

- [ ] **Step 3: Validate the plugin manifest**

Run: `claude plugin validate .`
Expected: success, `human-interface-guidelines` discovered as a skill.

- [ ] **Step 4: Check for dangling references**

Run: `grep -rn "human-interface-guidelines" skills/index.md docs/architecture/domain-map.md | grep -v "^Binary"`
Expected: entries in both files reference existing paths (no typos in
the 15 knowledge-contract slugs or the skill path).

- [ ] **Step 5: Manual invocation check (best-effort)**

In a fresh Claude Code session (new skill files aren't enumerated
mid-session — same caveat as the authentication/style-guide
migration), invoke `/apple-agent-kit:human-interface-guidelines` and
confirm it loads only the contracts relevant to a sample task (e.g.,
ask about Dark Mode support and confirm only `dark-mode.md` — and
maybe `color.md`/`accessibility.md` — load, not all 15).
