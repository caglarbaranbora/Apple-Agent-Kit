# Naming Conventions

Status: Draft Version: 0.1.0

## Purpose

Define naming rules for repository artifacts to ensure consistency,
discoverability, and deterministic routing.

## General Rules

-   Use lowercase.
-   Use kebab-case for file names.
-   Use singular nouns.
-   Use descriptive names.
-   Avoid abbreviations unless universally recognized.

## Repository Naming

Examples:

docs/ - architecture.md - routing-model.md

knowledge/ - authentication/ - sign-in.md - button-labels.md

skills/ - authentication/SKILL.md - style-guide/SKILL.md

workflows/ - release-ios-app.md

templates/ - knowledge-contract.md

## Artifact IDs

Pattern:

`<type>`{=html}.`<domain>`{=html}.`<name>`{=html}

Examples:

knowledge.authentication.sign-in

skill.authentication.login

workflow.release.app-store

template.knowledge.contract

## Domain Names

Use official Apple terminology whenever possible.

Examples:

-   SwiftUI
-   StoreKit
-   Accessibility
-   App Store
-   WidgetKit

Directory names remain lowercase:

swiftui/ storekit/ accessibility/

## Versioning

Use Semantic Versioning.

-   1.0.0 Initial stable
-   1.1.0 Backward-compatible additions
-   2.0.0 Breaking changes

## Reserved Names

Do not use:

-   temp
-   misc
-   test
-   new
-   final
-   copy

## Validation

A validator MUST verify:

-   File name format
-   ID uniqueness
-   ID/file consistency
-   Domain consistency
-   Version format
