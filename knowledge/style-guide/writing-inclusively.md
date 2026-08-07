# Writing Inclusively

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.writing-inclusively
artifact_type: knowledge
title: Writing Inclusively
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines rules for writing gender-neutral, unbiased, and disability-respectful UI text on Apple platforms.
domain: Style Guide
tags:
  - style-guide
  - inclusive-writing
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
last_updated: 2026-07-30
```

## Intent

This contract defines the terminology and phrasing rules an AI coding agent
must follow when writing user-facing text (UI copy, notifications, help
content, example data) for Apple platforms, so that content reflects the
diversity of Apple's audience and avoids harmful, biased, or exclusionary
language.

## Scope

### Included

-   Gender-neutral language and pronoun usage
-   Avoiding violent, oppressive, ableist, or color-coded terminology
-   Inclusive representation in example names, imagery, and scenarios
-   Identity-first and person-first disability terminology

### Excluded

-   Locale-specific adaptation of inclusive language
-   Accessibility implementation (VoiceOver labels, contrast, layout)
-   Legal or compliance requirements
-   Content moderation policy

## Rules

### Rule 1

Agents MUST use gender-neutral language by default. When phrasing would
otherwise imply a gender binary (e.g., "men and women"), reword to a neutral
form (e.g., "people of diverse backgrounds"), unless the content specifically
requires referring to a gender (e.g., "The percentage of women in the
workforce has increased"). When a gender-neutral honorific is needed, agents
SHOULD offer "Mx." alongside "Mr." and "Ms." rather than omitting a
neutral option.

### Rule 2

Agents MUST use `they`, `their`, or `them` as singular, gender-neutral
pronouns when referring to a person of unspecified gender. Agents MUST NOT
use `he or she`, `he/she`, or default to a single gendered pronoun.

### Rule 3

Agents SHOULD prefer rewriting a sentence to avoid pronouns altogether — for
example, using the plural form of the noun, or omitting the pronoun — when
that reads more naturally than a singular `they`.

### Rule 4

Agents MUST NOT assume a specific person's pronouns based on their name or
appearance. When identity is unknown and cannot be confirmed, agents MUST
default to neutral phrasing rather than guessing.

### Rule 5

Agents MUST NOT describe technology using terms that are violent (`kill`,
`hang`), oppressive (`master`/`slave`), or that associate mental health with
malfunction (`sanity check`). Agents SHOULD avoid describing software or
hardware with human or biological attributes generally.

### Rule 6

Agents MUST NOT use color to convey positive or negative qualities (e.g.,
`blacklist`, `whitelist`, `white hat`). Color terms MUST be reserved for
describing actual colors.

### Rule 7

Agents SHOULD avoid idioms and colloquial expressions (e.g., `fall through
the cracks`, `on the same page`, `backseat driver`) in UI text, since they
can be hard to understand for non-native speakers and hard to localize.

### Rule 8

Agents SHOULD use diverse names in example content, reflecting a variety of
ethnicities and genders, and MUST NOT default example families, occupations,
or scenarios to a single cultural or demographic stereotype.

### Rule 9

When writing about a person's disability, agents MUST use identity-first
language (e.g., "a disabled person") or person-first language (e.g., "a
person with a disability") based on the individual's stated preference; when
unknown, agents SHOULD default to person-first language and MUST NOT use
terms such as `handicapped`, `special needs`, `differently abled`,
`confined to a wheelchair`, `wheelchair-bound`, `hearing impaired`,
`deaf and dumb`, `deaf-mute`, `mute` (for a nonspeaking person), or
`a person with autism`/`autism spectrum disorder`/`high-functioning`/
`low-functioning`. When a person identifies with Deaf or Autistic culture as
an identity rather than a medical condition, agents MUST capitalize the term
("a Deaf person," "an Autistic person") per that individual's preference.
Agents MUST NOT describe people with disabilities as `brave`, `courageous`,
or `inspiring` for having a disability, and MUST NOT frame disability as
something to `overcome`.

### Rule 10

In instructional or UI text, agents SHOULD describe what happens directly
(e.g., `A message appears`, `An alert sounds`) rather than assuming a
specific sense (`you see a message`, `you hear an alert`). Common idioms in
general prose (e.g., `I see your point`) are unaffected by this rule.

## Compliant Example

-   ✓ "A subscriber can post their recipes to your shared folder." (Rule 2)
-   ✓ "Hiring people of diverse backgrounds fosters a culture of innovation." (Rule 1)
-   ✓ "A message appears when the download finishes." (Rule 10)
-   ✓ "Priya and Étienne can share files with each other." (Rule 8)

## Non-Compliant Example

-   ✗ "A subscriber can post his or her recipes to your shared folder." (Rule 2)
-   ✗ "Hiring men and women of diverse backgrounds fosters innovation." (Rule 1)
-   ✗ "You'll see a message when the download finishes." (Rule 10)
-   ✗ "Add a user to the blacklist to block them." (Rule 6)

## Dependencies

None.

## References

-   [Apple Style Guide — Writing inclusively (p. 223)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
