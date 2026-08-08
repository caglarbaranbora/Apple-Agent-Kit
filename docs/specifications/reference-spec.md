# Reference Specification

Status: Approved
Version: 1.2.0

## Purpose

Defines the normative specification for every Reference in Apple Agent Kit.

A Reference maps a domain to the official Apple sources that authorize its Knowledge
Contracts. It is an index of authority, not a source of rules.

## Location

    references/apple/<domain>.md

The id is `reference.apple.<domain>`.

One Reference per Skill-scoped domain. A domain whose Knowledge lives in a single
directory may still have several References when its Skills are split — for example
`human-interface-guidelines`, `human-interface-guidelines-components` and
`human-interface-guidelines-patterns` all draw on `knowledge/human-interface-guidelines/`.

**Reference-to-Knowledge is many-to-many.** No tool may derive one from the other by
directory name. A naive directory-derived check reports false positives on exactly the
two cases above and on legitimate cross-domain citations.

## Required Metadata

Common base (see ../../schemas/metadata.schema.md [[metadata.schema]]):
`id`, `artifact_type`, `title`, `version`, `status`, `last_updated`

Reference extension: `domain`, `owner`, `summary`

`artifact_type` is `reference`. Source URLs live in the body, under `## Source`, not in
a metadata field.

## Required Sections

1. Source
2. Purpose
3. Primary Topics
4. Used By

## Rules

- Every URL under `## Source` MUST resolve to an official Apple source: Apple Developer
  documentation, a WWDC session, an Apple archived guide, or help.apple.com. No
  third-party sources.
- A URL MUST be specific enough to authorize a rule. A framework or guideline landing
  page is acceptable when it is itself the cited surface; a bare hub that indexes
  unrelated topics is not. URL shape does not prove specificity — this is a judgment
  made in review, not by a script.
- `## Used By` lists every Knowledge Contract that cites this Reference, as a wiki link
  (`[[knowledge/<domain>/<slug>]]`), per ../architecture/linking-model.md
  [[linking-model]].
- `## Used By` may name Contracts outside this Reference's own domain. A Contract in
  one domain legitimately cites another domain's authoritative source.
- Every URL any Knowledge Contract cites in `references:` MUST be indexed under some
  Reference's `## Source` — not necessarily this one, since indexing is many-to-many
  in both directions. An unindexed citation is outside the `## Used By` check
  entirely, because that check walks indexed URLs and an unindexed one matches
  nothing. It is also an unverified citation: indexing is what makes a URL something
  a human fetches rather than something a Contract asserts, and three consecutive
  domain passes found Apple pages that had begun to redirect the moment indexing
  forced someone to open them.
- Every URL under `## Source` MUST be the address Apple currently serves, not one Apple
  redirects away from. Apple disambiguates a documentation path whenever a name is both
  a type and a member (`xctskip` → `xctskip-swift.struct`) or an overload set
  (`fetch(_:)` → `fetch(_:)-4xeoz`), and the undisambiguated form is a courtesy
  redirect, never the stable one — it is the address that later becomes a 404. A
  redirect is therefore a finding, not a pass. Enforced by `scripts/check_links.py`,
  which is scheduled rather than blocking because it depends on Apple being reachable;
  see ../validation-model.md [[validation-model]].
- A Reference MUST NOT contain implementation rules. Rules live in Knowledge Contracts;
  the Reference records where their authority comes from.
- `## Primary Topics` names the source surface this Reference covers, not the Contracts
  built from it.

## Size Limit

A Reference MUST NOT exceed 98 lines. If a domain's sources do not fit, split the
domain's Skill and give each Skill its own Reference — never raise this limit.

## Validation Checklist

- Metadata complete and valid against the schema
- All four sections present, in order
- Every `## Source` URL is an official Apple source
- Every `## Used By` entry resolves to an existing Knowledge Contract
- No implementation rules present
