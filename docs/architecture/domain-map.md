# Domain Map

Status: Draft
Version: 0.3.0

See: ../glossary.md
[[glossary]]

## Purpose

Defines the top-level Apple development domains used to organize References, Knowledge Contracts, Skills, and Workflows, and the Tier (build-order priority, see glossary above) assigned to each.

## Build Order

One domain is fully finished (Reference → Knowledge → Skill → Validation) before the next domain starts. Domains are attempted in Tier order: all of Tier 1, then Tier 2, then Tier 3. Within a tier, order is chosen at build time.

`style-guide` is first.

## Tier 1 — Must-Have

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style | UI copy wording, capitalization rules, punctuation, inclusive writing |
| Human Interface Guidelines | human-interface-guidelines | Visual/UX design patterns, layout, interaction | Layout patterns, interaction conventions, visual design guidance |
| App Store Review Guidelines | app-store-review-guidelines | Review, metadata, distribution rules | App Store submission, metadata, and distribution compliance rules |
| SwiftUI | swiftui | Views, navigation, layout | SwiftUI view/navigation/layout implementation conventions |
| UIKit | uikit | UIKit components | UIKit component implementation conventions |
| AuthenticationServices | authenticationservices | Sign in with Apple API, credential provider | Sign in with Apple API and credential provider implementation |
| StoreKit | storekit | In-App Purchases, subscriptions | In-app purchase and subscription implementation and terminology |
| Accessibility | accessibility | Accessibility APIs and UX | Accessibility API usage and accessible UX requirements |
| SF Symbols | sf-symbols | Iconography | Icon selection and SF Symbols usage rules |
| Xcode | xcode | Build, signing, archives | Build configuration, signing, and archive/export conventions |

## Tier 2

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| App Intents | app-intents | App Intents & Shortcuts | App Intents and Shortcuts implementation and terminology |
| WidgetKit | widgetkit | Widgets | Widget implementation, sizing, and terminology |
| UserNotifications | usernotifications | Push & local notifications | Push and local notification implementation and terminology |
| BackgroundTasks | backgroundtasks | Background execution | Background task scheduling and execution conventions |
| Foundation | foundation | Core Swift/Obj-C data types & utilities | Core Swift/Obj-C data type and utility usage conventions |
| Localization | localization | Language, terminology | Localization and translation workflow conventions |
| Privacy | privacy | Privacy requirements | Privacy manifest and data-use disclosure requirements |
| Sign in with Apple | sign-in-with-apple | Sign in with Apple UX/flow (see Cross-Domain Notes) | Sign in with Apple UX/flow (see Cross-Domain Notes) |

## Tier 3

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| AVFoundation | avfoundation | Audio/video capture & playback | Audio/video capture and playback implementation |
| Vision | vision | Image analysis | Image analysis API usage |
| Core ML | core-ml | On-device ML | On-device ML model integration conventions |
| CloudKit | cloudkit | CloudKit | CloudKit sync and record management conventions |
| Core Data | core-data | Persistence | Core Data persistence conventions |
| HealthKit | healthkit | Health data | Health data access and terminology |
| MapKit | mapkit | Maps | Map display and interaction conventions |
| Photos | photos | Photo library access | Photo library access and permission conventions |
| Core Location | core-location | Location services | Location services access and permission conventions |

## Existing / Unscheduled Domains

Mapped before this Tier list existed. No Tier assigned yet — resolve when reached.

| Domain | Status | Initial Scope | Owns |
|---|---|---|---|
| authentication | Active (Phase 5, in progress) | Sign in, identity, sessions — see Cross-Domain Notes | Sign-in, identity, and session implementation routing (see Cross-Domain Notes) |
| testing | Unscheduled | XCTest, UI testing | XCTest and UI testing conventions |
| networking | Unscheduled | URLSession, ATS | URLSession usage and App Transport Security conventions |
| security | Unscheduled | Keychain, credentials | Keychain and credential storage conventions |

## Cross-Domain Notes

- `authentication`, `authenticationservices`, and `sign-in-with-apple` overlap conceptually (sign-in flows). Boundary not yet resolved — decide when `authenticationservices` or `sign-in-with-apple` is reached, per the rule in ../dependency-graph.md ([[dependency-graph]]) that cross-domain dependencies must be explicit.
- `human-interface-guidelines` and `sf-symbols` were previously merged with `style-guide` under a single `design` domain. Split per ../../rfcs/0001-style-guide-domain-and-domain-roadmap.md ([[0001-style-guide-domain-and-domain-roadmap]]).

## Artifact Layout

references/apple/<domain>/
knowledge/<domain>/
skills/<domain>/
workflows/<domain>/

## Rules

- Every artifact belongs to exactly one primary domain.
- Cross-domain dependencies must be explicit.
- Skills cannot span unrelated domains.
- Knowledge Contracts remain atomic.

## Validation Checklist

- Domain exists
- Artifact mapped
- Cross-domain dependencies declared
- No duplicate ownership
