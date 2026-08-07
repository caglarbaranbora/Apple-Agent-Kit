# Capitalization Style Rules

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.capitalization-style-rules
artifact_type: knowledge
title: Capitalization Style Rules
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines when to use sentence-style vs. title-style capitalization, and the word-by-word rules for applying title-style capitalization.
domain: Style Guide
tags:
  - style-guide
  - capitalization
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.capitalization-of-apple-proper-nouns
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.punctuation-and-typography-in-text
last_updated: 2026-07-30
```

## Intent

This contract defines the generic capitalization system an AI coding agent
uses for UI text, command names, and prose — independent of any specific
Apple product or feature name — so that title-style and sentence-style case
are applied consistently and correctly.

## Scope

### Included

-   The two capitalization styles used at Apple (sentence-style, title-style)
-   Word-by-word rules for what to capitalize in title-style text
-   Capitalization of command names
-   Capitalizing onscreen element names to match their exact onscreen form

### Excluded

-   Capitalization of specific Apple product/platform/feature proper nouns (see `capitalization-of-apple-proper-nouns`)
-   Button label wording and punctuation (see `general-button-labels`)

## Rules

### Rule 1

Agents MUST use one of two styles: sentence-style capitalization (only the
first word and proper nouns capitalized, e.g. "This line provides an
example of sentence-style capitalization") or title-style capitalization
(most words capitalized, e.g. "This Line Provides an Example of
Title-Style Capitalization"). Except for user interface text, the choice
between the two is a matter of document/department style, but MUST be
applied consistently within a document.

### Rule 2

Agents MUST capitalize onscreen element names exactly as they appear
onscreen. If an onscreen element is rendered in all caps or all lowercase,
agents MUST use title-style capitalization when writing that element's
name in documentation or UI-adjacent text.

### Rule 3

When using title-style capitalization, agents MUST capitalize: the first
and last word regardless of part of speech; all nouns, pronouns, verbs,
adjectives, and adverbs regardless of length (It, This, You, Is, Are, Be);
conjunctions other than coordinating conjunctions (e.g. If); prepositions
of five or more letters (About, Between, Through); prepositions of any
length used as part of a phrasal verb or another part of speech (Start Up,
Turn On, Log In); and the second word of a hyphenated compound, except
"Built-in" and "Plug-in."

### Rule 4

When using title-style capitalization, agents MUST NOT capitalize:
articles (a, an, the) unless first word or following a colon; coordinating
conjunctions (and, but, or, nor, for, yet, so); "to" in infinitives;
"as" regardless of part of speech; words that always begin lowercase (iPad,
macOS); and prepositions of four letters or fewer (at, by, for, from, in,
into, of, off, on, onto, out, over, to, up, with) — except when one of
those short prepositions is part of a phrasal verb (Rule 3).

### Rule 5

Agents MUST use title-style capitalization for command names and MUST NOT
capitalize the word "command" itself (the Find command, the Make Alias
command). Agents MUST NOT capitalize a command name when it's used as an
ordinary English verb rather than as a reference to the command.

## Compliant Example

-   ✓ "Skip This Backup" / "Apple News Is Offline" (Rule 3)
-   ✓ "What to Do If Your iPhone Is Lost" (Rule 3)
-   ✓ "Restore iPhone from a Backup" (Rule 4)
-   ✓ "High-Level Events" / "64-Bit Addressing" (Rule 3)
-   ✓ "the Find command" / "the Make Alias command" (Rule 5)
-   ✓ "Cut and paste the selected text." as a plain verb (Rule 5)

## Non-Compliant Example

-   ✗ "Skip this Backup" mixing styles mid-title (Rule 3)
-   ✗ "What To Do if Your iPhone is Lost" (capitalizing "To," lowercasing "If"/"Is") (Rule 3, Rule 4)
-   ✗ "Restore iPhone From a Backup" capitalizing a 4-letter preposition (Rule 4)
-   ✗ "the Find Command" capitalizing "command" (Rule 5)
-   ✗ "Cut and Paste the selected text." used as plain verbs (Rule 5)

## Dependencies

None.

## References

-   [Apple Style Guide — capitalization (p. 45)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — command names (p. 55)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
