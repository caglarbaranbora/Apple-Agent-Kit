# Materials

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.materials
artifact_type: knowledge
title: Materials
version: 1.0.0
status: Approved
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
last_updated: 2026-08-08
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
