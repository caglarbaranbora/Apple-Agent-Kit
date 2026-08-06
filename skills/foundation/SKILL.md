---
name: foundation
description: Route Swift Foundation framework implementation tasks to the correct Knowledge Contracts -- date/time formatting, measurement and unit formatting, Codable encoding and custom conformance, and FileManager app sandbox directories. Use when working with DateFormatter, ISO8601DateFormatter, Date.FormatStyle, .formatted(), RelativeDateTimeFormatter, Measurement, .converted(to:), MeasurementFormatter, unitStyle, unitOptions, JSONEncoder, Codable, encode(to:), init(from:), CodingKeys, FileManager, Documents directory, Caches directory, Application Support directory, or isExcludedFromBackup. v1 is a curated, highest-usage subset of Foundation -- not an exhaustive API reference.
id: skill.foundation.foundations
title: Foundation — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Foundation
routes: [knowledge.foundation.date-time-formatting, knowledge.foundation.measurement-and-unit-formatting, knowledge.foundation.codable-encoding-and-custom-conformance, knowledge.foundation.filemanager-app-sandbox-directories]
related: []
last_updated: 2026-08-06
---

# Foundation — Foundations Skill

## Purpose

Route Swift Foundation framework implementation tasks to the minimum
required Foundation Knowledge Contracts. v1 scope is a deliberately
curated, highest-usage subset of four topics — not an exhaustive
Foundation API reference.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/foundation/.

-   `DateFormatter`, `ISO8601DateFormatter`, `Date.FormatStyle`,
    `.formatted()`, `RelativeDateTimeFormatter`, or formatter-reuse
    performance -> date-time-formatting.md
-   `Measurement`, `.converted(to:)`, `MeasurementFormatter`, `unitStyle`,
    or `unitOptions` -> measurement-and-unit-formatting.md
-   `JSONEncoder`, custom `encode(to:)`/`init(from:)` conformance, or
    `CodingKeys` for encoding -> codable-encoding-and-custom-conformance.md
-   `FileManager`, `Documents`/`Caches`/`Application Support` directories,
    safe file read/write, or `isExcludedFromBackup` ->
    filemanager-app-sandbox-directories.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/foundation/ — do not guess or fall back to general knowledge.

-   Unit-of-measure copy wording (spelling out vs. abbreviating, spacing,
    capitalization once a value is already display text) is owned by the
    `style-guide` Skill, not this one.
-   Network-response `Codable` decoding (`JSONDecoder`, `DecodingError`
    handling for fetched data) is owned by the `networking` Skill, not
    this one.
-   General String/Unicode text processing, `NotificationCenter`, the
    `Result` type, and GCD/`DispatchQueue` are deferred to a future
    concurrency-focused domain, not yet built — report that explicitly.
-   Locale/Bundle localization and translation workflow mechanics are
    deferred to the future `localization` domain (Tier 2, unbuilt) — report
    that explicitly.
-   Combine is deferred to the future `combine` domain (Tier 2, unbuilt) —
    report that explicitly.
