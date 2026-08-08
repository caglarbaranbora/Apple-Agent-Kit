# Technical Notation

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.technical-notation
artifact_type: knowledge
title: Technical Notation
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines code-font, syntax-description, and placeholder-naming rules for writing developer-facing code, UI text, and documentation.
domain: Style Guide
tags:
  - style-guide
  - technical-notation
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines the technical-notation rules an AI coding agent must
follow when writing code snippets, syntax descriptions, placeholder names,
and code-related references in developer documentation, UI text, or code
comments for Apple platforms.

## Scope

### Included

-   Code font usage for code, file, volume, directory, and library names
-   Syntax description formatting (literals, placeholders, optional brackets)
-   Placeholder naming and italicization in running text
-   Font boundaries and punctuation spacing around code font

### Excluded

-   General prose style unrelated to code or technical elements
-   API or symbol naming conventions themselves
-   Localization or translation of code samples
-   Accessibility labels for code-related UI elements

## Rules

### Rule 1

Agents MUST use code font for text fragments that represent expressions in
a programming language, and for names of files, volumes, directories, and
libraries.

### Rule 2

When writing code, agents SHOULD adopt one consistent spacing method around
punctuation (for example, "English-style" spacing, one space character
between words) and apply it consistently throughout a document.

### Rule 3

In syntax descriptions, agents MUST use code font for literals, italics for
placeholder names, and regular (non-code) text for brackets that enclose
optional elements.

### Rule 4

Agents MUST use embedded caps to connect words that act as a single
placeholder name, and MUST NOT alternate between different names for the
same placeholder.

### Rule 5

Agents MUST NOT use a function or method name as a verb in running text;
the sentence MUST be phrased in plain English instead.

### Rule 6

Agents MUST NOT mix code font and regular font within a single word, such
as forming the plural of a code-font term by appending a regular-font "s".
Rewrite the sentence instead.

### Rule 7

Agents MUST use regular text font, not code font, for punctuation that
follows a code-font word or phrase, unless that punctuation mark is itself
part of the computer-language element being represented.

### Rule 8

In running text, agents MUST use italics when referring to a placeholder
name, spelled exactly as it appears in the syntax description, and MUST NOT
use `foo`, `bar`, or `baz` for hierarchical or ordered placeholder names;
names that suggest the kind of item MUST be used instead.

## Compliant Example

-   ✓ Rule 1: `MainProg.c` file, `StandardCRuntime.o` library.
-   ✓ Rule 2: `(height, width: extended; quo: integer); PageSize = 1024`
-   ✓ Rule 3: `Read ([file, ] var)` — literals in code font, *file* and
    *var* as italic placeholders, brackets left as regular text.
-   ✓ Rule 4: *sourceFile* used consistently; *commandList* used
    throughout, never swapped for a different name mid-document.
-   ✓ Rule 5: "Run `ls` on both directories."
-   ✓ Rule 6: "values of type `integer`" (rewritten to avoid a mixed-font
    plural).
-   ✓ Rule 7: "`NAN(004)`, `nan(4)`, and NaN are examples of acceptable
    input." — the closing parenthesis is part of the literal, so it stays
    in code font; the following comma is regular text.
-   ✓ Rule 8: "Replace *volumeName* with a name of up to 12 characters."
    `TObject.FirstMethod`, `TObject.SecondMethod`.

## Non-Compliant Example

-   Rule 1: ✗ MainProg.c file (name not set in code font).
-   Rule 2: ✗ `(height,width:extended;quo:integer);PageSize=1024` (no
    consistent spacing).
-   Rule 3: ✗ `Read (file, var)` (no font distinction between literal,
    placeholder, and optional bracket).
-   Rule 4: ✗ Alternates between *commands* and *commandList* for the same
    placeholder.
-   Rule 5: ✗ "`ls` both directories." (function name used as a verb).
-   Rule 6: ✗ "integers" (plural formed by mixing a regular-font "s" onto
    code-font `integer`).
-   Rule 7: ✗ "`NAN(004),`" (trailing comma incorrectly set in code font).
-   Rule 8: ✗ "The volumeName can be up to 12 characters long." Using
    `foo`, `bar`, `baz` as placeholder names.

## Dependencies

None.

## References

-   [Apple Style Guide — Technical notation (p. 237–238)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
