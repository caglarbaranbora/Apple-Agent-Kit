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
