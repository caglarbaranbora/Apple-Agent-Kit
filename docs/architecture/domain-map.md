# Domain Map

Status: Draft
Version: 0.2.0

See: ../glossary.md
[[glossary]]

## Purpose

Defines the top-level Apple development domains used to organize References, Knowledge Contracts, Skills, and Workflows, and the Tier (build-order priority, see glossary above) assigned to each.

## Build Order

One domain is fully finished (Reference → Knowledge → Skill → Validation) before the next domain starts. Domains are attempted in Tier order: all of Tier 1, then Tier 2, then Tier 3. Within a tier, order is chosen at build time.

`style-guide` is first.

## Tier 1 — Must-Have

| Domain | Slug | Initial Scope |
|---|---|---|
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style |
| Human Interface Guidelines | human-interface-guidelines | Visual/UX design patterns, layout, interaction |
| App Store Review Guidelines | app-store-review-guidelines | Review, metadata, distribution rules |
| SwiftUI | swiftui | Views, navigation, layout |
| UIKit | uikit | UIKit components |
| AuthenticationServices | authenticationservices | Sign in with Apple API, credential provider |
| StoreKit | storekit | In-App Purchases, subscriptions |
| Accessibility | accessibility | Accessibility APIs and UX |
| SF Symbols | sf-symbols | Iconography |
| Xcode | xcode | Build, signing, archives |

## Tier 2

| Domain | Slug | Initial Scope |
|---|---|---|
| App Intents | app-intents | App Intents & Shortcuts |
| WidgetKit | widgetkit | Widgets |
| UserNotifications | usernotifications | Push & local notifications |
| BackgroundTasks | backgroundtasks | Background execution |
| Foundation | foundation | Core Swift/Obj-C data types & utilities |
| Localization | localization | Language, terminology |
| Privacy | privacy | Privacy requirements |
| Sign in with Apple | sign-in-with-apple | Sign in with Apple UX/flow (see Cross-Domain Notes) |

## Tier 3

| Domain | Slug | Initial Scope |
|---|---|---|
| AVFoundation | avfoundation | Audio/video capture & playback |
| Vision | vision | Image analysis |
| Core ML | core-ml | On-device ML |
| CloudKit | cloudkit | CloudKit |
| Core Data | core-data | Persistence |
| HealthKit | healthkit | Health data |
| MapKit | mapkit | Maps |
| Photos | photos | Photo library access |
| Core Location | core-location | Location services |

## Existing / Unscheduled Domains

Mapped before this Tier list existed. No Tier assigned yet — resolve when reached.

| Domain | Status | Initial Scope |
|---|---|---|
| authentication | Active (Phase 5, in progress) | Sign in, identity, sessions — see Cross-Domain Notes |
| testing | Unscheduled | XCTest, UI testing |
| networking | Unscheduled | URLSession, ATS |
| security | Unscheduled | Keychain, credentials |

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
