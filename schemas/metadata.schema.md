# Metadata Schema

Status: Draft Version: 0.1.0

## Purpose

Define the common metadata contract for every repository artifact.

## Required Fields

  Field        Required   Description
  ------------ ---------- -------------------------------------------------------
  id           Yes        Globally unique artifact identifier
  type         Yes        knowledge, skill, workflow, template, reference, spec
  title        Yes        Human-readable title
  version      Yes        Semantic version
  status       Yes        Draft, Approved, Deprecated, Archived
  owner        Yes        Maintainer or team
  summary      Yes        One-sentence purpose
  tags         Yes        Searchable keywords
  domain       Yes        Apple domain (SwiftUI, StoreKit, etc.)
  references   No         Official source links
  related      No         Related artifacts
  depends_on   No         Required artifacts
  provides     No         Capabilities exposed
  updated      Yes        Last updated date

## Example

``` yaml
id: knowledge.authentication.sign-in
type: knowledge
title: Sign In
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Rules for Sign in terminology.
tags:
  - authentication
domain: Authentication
references:
  - https://developer.apple.com/
depends_on:
  - knowledge.button-labels
related:
  - knowledge.accessibility.forms
provides:
  - sign-in-terminology
updated: 2026-07-29
```

## Rules

-   Every artifact MUST include all required fields.
-   IDs MUST be immutable.
-   Status changes MUST increment version when appropriate.
-   References SHOULD point to official Apple sources.
-   Dependencies MUST remain acyclic.
