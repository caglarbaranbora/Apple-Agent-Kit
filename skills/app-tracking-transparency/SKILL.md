---
name: app-tracking-transparency
description: Route App Tracking Transparency / IDFA implementation tasks to the correct Knowledge Contracts -- authorization request mechanics, authorization status handling, IDFA access, and the NSUserTrackingUsageDescription Info.plist requirement. Use when calling requestTrackingAuthorization, checking trackingAuthorizationStatus, reading advertisingIdentifier, or writing NSUserTrackingUsageDescription. v1 is iOS/iPadOS AppTrackingTransparency + AdSupport framework API only -- no tvOS-specific behavior, no SKAdNetwork, no AdServices attribution. Triggers on ATTrackingManager, requestTrackingAuthorization, trackingAuthorizationStatus, ATTrackingManagerAuthorizationStatus, ASIdentifierManager, advertisingIdentifier, IDFA, NSUserTrackingUsageDescription, App Tracking Transparency, tracking authorization.
id: skill.app-tracking-transparency.foundations
title: App Tracking Transparency — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: App Tracking Transparency
routes: [knowledge.app-tracking-transparency.authorization-request, knowledge.app-tracking-transparency.status-and-idfa-access, knowledge.app-tracking-transparency.usage-string-and-info-plist]
related: []
last_updated: 2026-08-08
---

# App Tracking Transparency — Foundations Skill

## Purpose

Route App Tracking Transparency / IDFA implementation tasks to the
minimum required App Tracking Transparency Knowledge Contracts. v1 scope
is the iOS/iPadOS AppTrackingTransparency and AdSupport framework API —
no tvOS-specific behavior, no SKAdNetwork, no AdServices attribution.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/app-tracking-transparency/.

-   Calling requestTrackingAuthorization or handling its call mechanics -> authorization-request.md
-   Checking trackingAuthorizationStatus or reading advertisingIdentifier -> status-and-idfa-access.md
-   Writing NSUserTrackingUsageDescription -> usage-string-and-info-plist.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/app-tracking-transparency/ — do not guess or fall
back to general knowledge.

-   tvOS-specific App Tracking Transparency behavior — Deferred
-   SKAdNetwork and AdServices attribution — Deferred
-   Pre-permission screen design, request-timing UX — owned by `human-interface-guidelines`
