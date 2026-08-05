# Domain Map

Status: Draft
Version: 0.5.0

See: ../glossary.md
[[glossary]]

## Purpose

Defines the top-level Apple development domains used to organize References, Knowledge Contracts, Skills, and Workflows, and the Tier (build-order priority, see glossary above) assigned to each.

## Build Order

One domain is fully finished (Reference → Knowledge → Skill → Validation) before the next domain starts. Domains are attempted in Tier order: all of Tier 1, then Tier 2, then Tier 3. Within a tier, order is chosen at build time.

Tiers ranked by real-world usage frequency (2026-07-31 re-rank, cross-checked against the full Apple Developer Documentation technology index): Tier 1 = needed by nearly every iOS app, Tier 2 = common but not universal, Tier 3 = vertical/niche.

Completed: `style-guide` (Tier 1), `authentication` (Existing/Unscheduled — cross-cutting, built ahead of tier order per Phase 5 decision), `human-interface-guidelines` (Tier 1 — Foundations subset only; Patterns/Components/Inputs remain unbuilt), `app-store-review-guidelines` (Tier 1 — critical-subset v1: 2.1, 2.3, 3.1.1, 4.2, 4.3, 5.1.1, 5.1.2; Safety, most of Legal, Design 4.0, and Guideline 4.8 remain unbuilt), `swiftui` (Tier 1 — Views/Navigation/Layout/State v1, iOS 17+ conventions; animation, gestures, previews, custom Layout protocol conformances, and legacy ObservableObject/NavigationView migration guidance remain unbuilt), `accessibility` (Tier 1 — SwiftUI + UIKit accessibility API v1: labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits), `uikit` (Tier 1 — programmatic screen-scaffolding v1: view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, modal presentation; Storyboard/XIB, gesture recognizers, Core Animation, custom transitions, and SwiftUI interop remain unbuilt), `sf-symbols` (Tier 1 — core rendering/variants v1 across SwiftUI + UIKit: symbol basics, rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; symbol effects/animations and Symbol Composer authoring remain unbuilt), `networking` (Tier 1 — async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests; completion-handler APIs, Combine, and URLSessionDelegate-based background/progress/TLS handling remain unbuilt), `xcode` (Tier 1 — Xcode GUI/project-file v1: build configurations & xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; xcodebuild CLI, CI signing automation, and Swift Package Manager build configuration remain unbuilt), `local-authentication` (Tier 1 — iOS/iPadOS LocalAuthentication framework API v1: availability/biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; macOS/watchOS-specific behavior and general Keychain storage remain unbuilt).

## Tier 1 — Must-Have

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| Apple Style Guide | style-guide | Terminology, capitalization, punctuation, writing style | UI copy wording, capitalization rules, punctuation, inclusive writing |
| Human Interface Guidelines | human-interface-guidelines | Foundations (iOS/iPadOS): layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL. Patterns/Components/Inputs deferred — see Cross-Domain Notes. | Foundations-layer visual/UX design guidance for iOS/iPadOS (layout, color, typography, app icons, images, inclusive-design content, materials, motion, iconography, branding, accessibility-design, privacy-design, RTL) |
| App Store Review Guidelines | app-store-review-guidelines | 2.1 App Completeness, 2.3 Accurate Metadata, 3.1.1 In-App Purchase, 4.2 Minimum Functionality, 4.3 Spam/Duplicate, 5.1.1/5.1.2 Privacy (data collection & sharing). Safety, most of Legal, and Design 4.0 (owned by human-interface-guidelines) out of scope — see Cross-Domain Notes. | App Store submission, metadata, and distribution compliance rules |
| SwiftUI | swiftui | Views (composition, identity, modifier order), Navigation (NavigationStack, NavigationSplitView), Layout (stacks/spacing, safe area, lazy grids, GeometryReader), State management (@State/@Binding, @Observable, @Environment). Targets iOS 17+ conventions; legacy ObservableObject/NavigationView out of scope — see Cross-Domain Notes. | SwiftUI view, navigation, layout, and state-management implementation conventions |
| UIKit | uikit | Programmatic screen-scaffolding v1: view controller lifecycle and composition, Auto Layout (constraints, stack views, safe area), navigation (UINavigationController, UITabBarController, modal presentation), diffable table/collection views. No Storyboard/XIB, no classic data source pattern. Accessibility APIs owned by `accessibility` — see Cross-Domain Notes. | UIKit programmatic screen-scaffolding implementation conventions (view controllers, Auto Layout, navigation, diffable lists/grids) |
| Accessibility | accessibility | SwiftUI + UIKit accessibility API implementation: labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, hidden/decorative elements, accessibility audits. Design-level accessibility guidance owned by human-interface-guidelines — see Cross-Domain Notes. | SwiftUI + UIKit accessibility API implementation, VoiceOver/Dynamic Type/reduce-motion support, and accessibility audit conventions |
| SF Symbols | sf-symbols | SF Symbols API implementation v1: symbol basics (Image(systemName:)/UIImage(systemName:)), rendering modes (monochrome/hierarchical/palette/multicolor), symbol variants (fill/circle/square/slash), variable value symbols, weight/scale configuration, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration. Symbol effects/animations and Symbol Composer authoring deferred — see Cross-Domain Notes. | SF Symbols API implementation across SwiftUI and UIKit (rendering, variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration) |
| Xcode | xcode | Xcode GUI/project-file v1: build configurations & .xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options. No xcodebuild CLI, no CI signing automation, no Swift Package Manager build configuration. | Xcode project-configuration implementation conventions (build settings, xcconfig, schemes, signing, entitlements, archive/export) |
| Networking | networking | Async/await URLSession v1: request construction, data fetching, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests. No completion-handler APIs, no Combine, no URLSessionDelegate-based background/progress/TLS handling. Sign-in UX owned by `authentication` — see Cross-Domain Notes. | URLSession async/await implementation conventions (requests, decoding, error handling, cancellation, session configuration, ATS, authenticated requests) |
| Local Authentication | local-authentication | iOS/iPadOS LocalAuthentication framework API v1: availability and biometry-type detection, policy evaluation (biometrics-only vs. biometrics-or-passcode), reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding (SecAccessControl), fallback UX. No macOS/watchOS-specific behavior, no general Keychain storage. | Biometric and device-passcode authentication API implementation, including the Keychain-biometric binding seam |
| App Tracking Transparency | app-tracking-transparency | ATT prompt, IDFA access | Tracking-permission prompt and IDFA access conventions |

## Tier 2

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| App Intents | app-intents | App Intents, Siri integration, Shortcuts | App Intents, Siri integration, and Shortcuts implementation and terminology |
| WidgetKit | widgetkit | Widgets | Widget implementation, sizing, and terminology |
| UserNotifications | usernotifications | Push & local notifications | Push and local notification implementation and terminology |
| BackgroundTasks | backgroundtasks | Background execution | Background task scheduling and execution conventions |
| Foundation | foundation | Core Swift/Obj-C data types & utilities | Core Swift/Obj-C data type and utility usage conventions |
| Localization | localization | Language, terminology | Localization and translation workflow conventions |
| Privacy | privacy | Privacy requirements | Privacy manifest and data-use disclosure requirements |
| Sign in with Apple | sign-in-with-apple | Sign in with Apple UX/flow (see Cross-Domain Notes) | Sign in with Apple UX/flow (see Cross-Domain Notes) |
| AuthenticationServices | authenticationservices | Sign in with Apple API, credential provider | Sign in with Apple API and credential provider implementation |
| StoreKit | storekit | In-App Purchases, subscriptions | In-app purchase and subscription implementation and terminology |
| Core Data | core-data | Persistence (legacy/established) | Core Data persistence conventions (see Cross-Domain Notes) |
| SwiftData | swiftdata | Persistence (modern) | SwiftData persistence conventions (see Cross-Domain Notes) |
| PassKit | passkit | Apple Pay, Wallet | Apple Pay and Wallet pass implementation and terminology |
| TipKit | tipkit | In-app feature tips | Feature-tip / onboarding-hint implementation conventions |
| Combine | combine | Reactive data flow | Publisher/subscriber usage conventions, SwiftUI interop |
| EventKit | eventkit | Calendar, reminders | Calendar and reminder access and permission conventions |
| Testing | testing | XCTest, Swift Testing, UI testing | XCTest, Swift Testing, and UI testing conventions |
| Security | security | Keychain, credential storage | Keychain and credential storage conventions |

## Tier 3

| Domain | Slug | Initial Scope | Owns |
|---|---|---|---|
| AVFoundation | avfoundation | Audio/video capture & playback | Audio/video capture and playback implementation |
| Vision | vision | Image analysis | Image analysis API usage |
| Core ML | core-ml | On-device ML | On-device ML model integration conventions |
| CloudKit | cloudkit | CloudKit | CloudKit sync and record management conventions |
| HealthKit | healthkit | Health data | Health data access and terminology |
| MapKit | mapkit | Maps | Map display and interaction conventions |
| Photos | photos | Photo library access | Photo library access and permission conventions |
| Core Location | core-location | Location services | Location services access and permission conventions |
| Apple Ads | apple-ads | Ad attribution: AdAttributionKit, SKAdNetwork | Ad-campaign attribution and measurement implementation |
| HomeKit | homekit | Smart-home accessory control | HomeKit accessory and automation implementation |
| CarPlay | carplay | In-car app UI | CarPlay app template and UI conventions |
| ARKit | arkit | AR session/tracking | AR session setup and tracking conventions |
| RealityKit | realitykit | 3D/AR rendering | RealityKit entity/scene rendering conventions (see Cross-Domain Notes) |
| GameKit | gamekit | Leaderboards, matchmaking | Game Center leaderboard, achievement, and matchmaking conventions |
| MusicKit | musickit | Apple Music playback/catalog | Apple Music catalog and playback integration |
| Contacts | contacts | Contacts access | Contacts framework access and permission conventions |
| MessageUI | messageui | Mail/SMS compose sheets | Mail and message compose-sheet implementation |
| Speech | speech | Speech recognition | Speech-to-text implementation conventions |
| Natural Language | naturallanguage | Text analysis | On-device text analysis (tokenization, language ID, sentiment) conventions |

## Existing / Unscheduled Domains

Mapped before this Tier list existed. No Tier assigned yet — resolve when reached.

| Domain | Status | Initial Scope | Owns |
|---|---|---|---|
| authentication | Active (Phase 5, in progress) | Sign in, identity, sessions — see Cross-Domain Notes | Sign-in, identity, and session implementation routing (see Cross-Domain Notes) |

## Cross-Domain Notes

- `authentication`, `authenticationservices`, and `sign-in-with-apple` overlap conceptually (sign-in flows). Boundary not yet resolved — decide when `authenticationservices` or `sign-in-with-apple` is reached, per the rule in ../dependency-graph.md ([[dependency-graph]]) that cross-domain dependencies must be explicit.
- `human-interface-guidelines` and `sf-symbols` were previously merged with `style-guide` under a single `design` domain. Split per ../../rfcs/0001-style-guide-domain-and-domain-roadmap.md ([[0001-style-guide-domain-and-domain-roadmap]]).
- `core-data` and `swiftdata` overlap (both persistence). Boundary not yet resolved — decide when either is reached; likely resolution is a shared "which framework to recommend" note rather than merging the domains, since `core-data` and `swiftdata` remain separate frameworks with separate APIs.
- `arkit` and `realitykit` overlap (AR/3D rendering, RealityKit often layers on ARKit sessions). Boundary not yet resolved — decide when either is reached.
- `swiftui` and `human-interface-guidelines` overlap on layout (`swiftui`'s `stacks-and-spacing`/`safe-area`/`lazy-grids` vs. `human-interface-guidelines`'s `layout.md`). Resolved via angle-split: `swiftui`'s angle is code-implementation (which API, correct syntax, performance), `human-interface-guidelines`'s angle is visual-design (spacing/alignment as a design decision). Same pattern as the `app-store-review-guidelines` privacy KCs vs. the future `privacy` domain.
- `swiftui` and `combine` (Tier 2, unbuilt) overlap on state management — `combine`'s Owns line already covers "SwiftUI interop." Resolved via angle-split: `swiftui`'s `observable-macro.md` teaches `@Observable` as the modern, non-Combine replacement for `ObservableObject`; `combine`'s angle (when built) is Combine-specific publisher/subscriber patterns. Boundary confirmed when `combine` is reached.
- `app-intents` owns Siri integration; legacy `SiriKit` (donation-based intents) is superseded by App Intents on current OS versions and is not planned as a separate domain unless a legacy-support need is identified.
- `human-interface-guidelines` (`accessibility` Foundations topic) and `accessibility` overlap: HIG's angle is design guidance (Dynamic Type requirement, contrast ratio, not conveying state by color alone, gesture alternatives — the *what* and *why*), `accessibility`'s angle is API implementation (the *how* — `accessibilityLabel`, `accessibilityTraits`, `@ScaledMetric`, `accessibilityReduceMotion`, etc.). Resolved via angle-split, the same pattern as the `swiftui` vs. `human-interface-guidelines` layout overlap.
- `human-interface-guidelines` (`privacy` Foundations topic) and the future `privacy` domain (Tier 2, unbuilt) overlap: HIG's angle is permission-request UI/consent-flow design, the dedicated domain's angle is Privacy Manifest / data-use disclosure implementation. Boundary not yet resolved — decide when `privacy` is built.
- `human-interface-guidelines` (`sf-symbols` Foundations topic) and `sf-symbols` overlap: HIG owns symbol selection/composition as a design decision (which symbol, which color, fill vs. outline as a design choice), `sf-symbols` owns API implementation (rendering modes, variants, variable value, weight/scale, color/tinting mechanics, custom symbol usage, UIKit SymbolConfiguration). Resolved via angle-split — `sf-symbols` KCs cross-reference `human-interface-guidelines`'s `sf-symbols.md` via `related:` rather than restating its Rules.
- `sf-symbols` and `uikit` overlap: `uikit` KCs may display symbols inside their examples but don't own symbol-rendering rules — a future `uikit` KC needing symbol-specific guidance should cross-reference `sf-symbols` via `related:` rather than duplicating rendering-mode/weight/scale content. No existing `uikit` KC required updating for this domain's launch.
- `sf-symbols` and `swiftui` overlap: same pattern as `sf-symbols` vs. `uikit` — `swiftui` owns view composition, not symbol rendering. No existing `swiftui` KC required updating for this domain's launch.
- `app-store-review-guidelines` (`privacy-manifest`/`privacy-nutrition-label` topics) and the future `privacy` domain (Tier 2, unbuilt) overlap: this domain's angle is review consequence (submission gets rejected if the manifest/label is missing or inaccurate), the future `privacy` domain's angle is correct implementation (how to write the manifest and disclosures correctly). Boundary not yet resolved — decide when `privacy` is built.
- `accessibility` (`accessibility-audits-testing` topic) and the future `testing` domain (Tier 2, unbuilt) overlap: this domain's angle is accessibility-specific audit APIs (`performAccessibilityAudit`, Accessibility Inspector), `testing`'s future angle is general XCTest/Swift Testing/UI-testing conventions. Boundary not yet resolved — decide when `testing` is built.
- `uikit` and `accessibility` overlap: `accessibility` owns all UIKit accessibility API implementation (labels, traits, value/hint, custom actions, element grouping/order, Dynamic Type, reduce-motion/transparency, focus, hidden/decorative, audits) across both SwiftUI and UIKit; `uikit` owns non-accessibility screen-scaffolding APIs (lifecycle, layout, navigation, lists/grids). Resolved via angle-split — `uikit` KCs cross-reference `accessibility` KCs via `related:` rather than restating Rules.
- `uikit` and `swiftui` overlap: both cover screen-building but on separate API surfaces (imperative vs. declarative); neither depends on the other for v1. The interop boundary (`UIHostingController`/`UIViewRepresentable`) is future scope for whichever domain builds it — not yet assigned.
- `uikit` and `human-interface-guidelines` overlap: HIG owns design guidance (when to use a tab bar vs. navigation stack, list vs. grid layout choice, modal vs. push presentation), `uikit` owns API implementation (the *how*). Same angle-split pattern as `accessibility` vs. `human-interface-guidelines`.
- `networking` and `authentication` do not overlap — this is a clean handoff, not an angle-split. `authentication`'s own Knowledge Contract (`knowledge.authentication.authentication`) explicitly excludes "Authentication networking" and "Backend architecture" from its scope; `networking`'s `authenticated-requests` topic fills exactly that gap (attaching credentials to a request, 401 refresh-and-retry), while `authentication` continues to own sign-in UX, terminology, and entry points. No content is duplicated between the two domains.
- `local-authentication` and `authentication` do not overlap — this is a clean handoff, not an angle-split, same pattern as `networking`/`authentication`. `knowledge.authentication.authentication`'s Excluded list omits biometrics entirely (its exclusions are StoreKit authentication, passkeys implementation, Sign in with Apple implementation, authentication networking, backend architecture); `authentication` owns sign-in terminology, entry points, and user-facing flow decisions, while `local-authentication` owns the LocalAuthentication framework API surface reached once the decision to use biometrics has already been made. No content is duplicated between the two domains.

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
