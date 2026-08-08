# Icons (Interface Icons)

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.icons
artifact_type: knowledge
title: Icons (Interface Icons)
version: 1.0.0
status: Approved
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
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.app-icons
  - knowledge.human-interface-guidelines.right-to-left
  - knowledge.human-interface-guidelines.sf-symbols
last_updated: 2026-08-08
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
icon so VoiceOver can announce its purpose (see also `accessibility`
Rule 4).

### Rule 5

Agents MUST use a vector format (PDF/SVG) for custom interface icons
so the system can scale them for all resolutions and Dynamic Type
sizes.

### Rule 6

Agents MUST NOT depict replicas of Apple hardware products in
interface icons. The same prohibition applies to the app icon under
`app-icons` Rule 4 — Apple states it per surface, and neither rule
generalizes to the other.

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
