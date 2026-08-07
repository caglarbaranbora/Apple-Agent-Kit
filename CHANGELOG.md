# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The project uses a single version number (`README.md` and `npx/package.json` share the same version).

## [Unreleased]
### Added
- `localization` domain — 1 Reference, 6 Knowledge Contracts, 1 Skill. **Seventeenth and final Tier 2 domain; Tier 2 is now complete.**
  - `string-catalogs-and-extraction` — `.xcstrings` mechanics, compiler-driven extraction and the string-literal requirement it depends on, translator comments, the New/Needs Review/Translated/Stale states, explicit keys vs. value-as-key, manually-managed entries, and the per-table migration boundary with legacy `.strings`.
  - `localized-string-apis` — `String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey` and SwiftUI's implicit `Text` literal localization, `Text(verbatim:)`, `AttributedString(localized:)`, format specifiers, and `NSLocalizedString`'s remaining role.
  - `plural-and-device-variations` — plural and device variation, the CLDR categories with `other` required and the applicable set language-dependent, substitutions, and legacy `.stringsdict`.
  - `locale-and-language-resolution` — `Locale.current` vs. `autoupdatingCurrent`, `preferredLanguages` vs. `preferredLocalizations`, `Locale.Language`/`Locale.Region`, `CFBundleDevelopmentRegion`, and the `.lproj` fallback chain.
  - `layout-direction-and-rtl-apis` — leading/trailing over left/right, SwiftUI automatic mirroring, `flipsForRightToLeftLayoutDirection(_:)`, UIKit `semanticContentAttribute`/`effectiveUserInterfaceLayoutDirection`, SF Symbols mirroring, `characterDirection`, and the RTL pseudolanguages.
  - `localized-resources-and-infoplist` — `InfoPlist.xcstrings`/`InfoPlist.strings`, `CFBundleDisplayName`/`CFBundleName`, `.lproj` structure, per-asset catalog localization, Swift-package `defaultLocalization`/`Bundle.module`, and `Bundle.localizedString(forKey:value:table:)`.
- Baseline is Xcode 16+ with an iOS 17+ API surface. String Catalogs impose no deployment-target cost — `.xcstrings` compiles to `.strings`/`.stringsdict` at build time — so the real gate is the Xcode version. Xcode 16 specifically because "Don't Translate", stale-string build warnings, format-specifier diagnostics, and the `xcstringstool` replacement for the deprecated `genstrings` do not exist in Xcode 15.
- Four Cross-Domain Notes recorded in `docs/architecture/domain-map.md`: angle-split with `human-interface-guidelines` over RTL (design vs. API), clean handoffs with `foundation` (Locale resolution vs. formatter use) and `style-guide` (source copy vs. extraction/resolution mechanics), and a deferred hand-off to `xcode` for project-language configuration and `.xcloc`/XLIFF export-import.
- Closes the SF Symbols RTL seam `knowledge.human-interface-guidelines.right-to-left` had explicitly left open: mirroring is automatic and driven by the symbol's name, with no API to request it — "forward"/"backward" mirror, "left"/"right" do not.

### Notes
- Corrects several natural-but-wrong assumptions: `String(localized:)`'s `locale:` parameter formats interpolated values but does not change which language is looked up (only `LocalizedStringResource.locale` does); `Text(someVariable)` silently resolves to a non-localizing initializer; `Locale.current` reports the locale the *app* resolved to rather than the user's preference; `Locale.autoupdatingCurrent` never compares equal to a fixed `Locale`; `UISemanticContentAttribute.unspecified` means *mirror*, not "do nothing"; `imageFlippedForRightToLeftLayoutDirection()` sets a flag rather than returning a flipped image; and `^[…](inflect: true)` is a runtime transform, not a pluralization mechanism.
- Sourcing caveats recorded in `localized-resources-and-infoplist`: Info.plist localization is covered by none of the articles in Apple's current Xcode Localization documentation hub, leaving a WWDC23 transcript and the archived Info.plist Key Reference as its only sources; and no Apple source states in those words that permission usage strings must be localized — that rule is written as an inference from their documented user-visibility, not as an Apple mandate.
- Apple publishes no schema for the `.xcstrings` file format, so these contracts describe the String Catalog through its editor affordances and public APIs, never through JSON field names.

## [2.0.0] - 2026-08-07
### Changed
- Major version bump marking a repo structure/documentation milestone (16 of 18 Tier 2 domains complete; no new domain content in this release).
- `README.md`'s `## Skills` section condensed from 31 multi-line entries (routing examples, v1-scope caveats) to one bullet per Skill — name, one-line description, link to that Skill's own `SKILL.md`. Routing tables and examples remain the responsibility of each `SKILL.md` and `skills/index.md`.
- `README.md`'s `## What's New` capped at its 3 most recent entries going forward; full history stays exclusively in this file. Both rules codified in `CLAUDE.md`.
- `npx/README.md` re-synced as a byte-identical mirror of `README.md`.

## [1.10.0] - 2026-08-07
### Added
- v1.10.0 release: sixteenth Tier 2 domain, `testing`.
- `testing` Skill (`XCTestCase` structure and assertions, Swift Testing fundamentals, parameterized and async tests, UI testing with `XCUIApplication`, expectations for asynchronous code; curated v1 subset of XCTest/Swift Testing/XCUITest, not exhaustive) — 5 Knowledge Contracts. Covers `XCTestCase` subclassing with `test`-prefixed methods and the per-test instance `setUp()`/`setUpWithError()`/`tearDown()`/`tearDownWithError()` lifecycle and its documented call order (distinct from the once-per-class `class func setUp()`/`tearDown()`), the `XCTAssert*` family, and `XCTSkip`/`XCTSkipIf`/`XCTSkipUnless`; the newer Swift Testing framework's `@Test` (no inheritance required), `#expect(_:)` (continue-on-failure) vs. `#require(_:)` (throw-and-halt), optional `@Suite` grouping (never on an extension), and `Tag`/`.tags(_:)`; `@Test(arguments:)` parameterization (single-collection once-per-element vs. two-bare-collection Cartesian product vs. `zip`-paired) and native `async throws` test functions in both frameworks with no `XCTestExpectation` needed; `XCUIApplication()`/`.launch()`/`XCUIElement` UI testing (now documented under the XCUIAutomation framework, not XCTest), `continueAfterFailure`, identifier-based element lookup, and `.tap()`/`.typeText(_:)`/`.waitForExistence(timeout:)`; and `XCTestExpectation`/`expectation(description:)`/`.fulfill()`/`await fulfillment(of:timeout:)` for callback-based async code with no `async`/`await` entry point. Two clean, proactively-scoped handoffs rather than discovered conflicts: Xcode Test Plans/code coverage config remain `xcode`'s territory, and `performAccessibilityAudit()` remains `accessibility`'s territory. Corrects several natural-but-wrong assumptions found against live Apple docs: the `setUp()`/`tearDown()` naming collision between per-test instance methods and a once-per-class `class func` overload; `XCUIApplication`/`XCUIElement` living under the XCUIAutomation framework rather than XCTest; the `app.buttons["x"]`-style subscript matching any of an element's identifying properties (identifier, title, label, value, placeholderValue), not only `accessibilityIdentifier`; the exact Cartesian-product-vs-`zip`-paired split for two-collection `@Test(arguments:)` overloads; and `wait(for:timeout:)` being guided-away-from in favor of `await fulfillment(of:timeout:)`, not deprecated. Performance testing (`measure { }`/`XCTMetric`), snapshot testing, UI test recording, and mocking/dependency-injection patterns remain out of scope.

## [1.9.0] - 2026-08-07
### Added
- v1.9.0 release: fifteenth Tier 2 domain, `combine`.
- `combine` Skill (publishers and subscribers, `@Published`/`ObservableObject`, subjects, transforming/combining operators, assign and memory management; Combine framework API v1) — 5 Knowledge Contracts. Covers the `Publisher`/`Subscriber` subscription contract (`sink(receiveCompletion:receiveValue:)`/the `Failure == Never` `sink(receiveValue:)` overload, retaining the returned `AnyCancellable`), `@Published`/`ObservableObject` (the `$name` projected-value publisher, synthesized `objectWillChange`, and the `willSet`-timing detail — a subscriber sees the new value before the property itself has changed), `PassthroughSubject`/`CurrentValueSubject` (`send(_:)`/`send(completion:)`), the transforming/combining operators `map`/`filter`/`removeDuplicates`/`debounce(for:scheduler:options:)`/`combineLatest`/`merge`/`zip` (including the tuple-vs-flat-stream distinction between `combineLatest`/`zip` and `merge`), and `assign(to:on:)`/`assign(to:)` with `assign(to:on:)`'s documented same-object retain-cycle risk plus `.store(in:)` for cancellable lifetime management. Resolves the `swiftui`/`combine` state-management boundary this repo had left open pending `combine`'s build (see domain-map.md Cross-Domain Notes) — a clean angle-split, not overlapping content: `swiftui` owns `@Observable` as the modern replacement, `combine` owns `@Published`/`ObservableObject` for code that still uses or interoperates with it. No corrections to the approved scope beyond citation-precision notes: citing the full `debounce(for:scheduler:options:)` three-parameter signature, and citing `Publishers.Merge`'s type page for `merge(with:)` since no distinct single-overload doc page exists. Combine-to-async/await interop (`Publisher.values`/`AsyncPublisher`), custom `Publisher`/`Subscriber` conformances, backpressure/`Subscribers.Demand`, and SwiftData/Core Data interop remain out of scope.

## [1.8.0] - 2026-08-06
### Added
- v1.8.0 release: fourteenth Tier 2 domain, `core-data`.
- `core-data` Skill (model definition, persistent container setup, managed object context CRUD, fetching with `NSFetchRequest`, relationships and delete rules; Core Data framework API v1) — 5 Knowledge Contracts. Covers `NSManagedObject` subclassing and `.xcdatamodeld` Codegen modes (Class Definition/Category+Extension/Manual-None) with `@NSManaged` properties, `NSPersistentContainer(name:)`/`loadPersistentStores(completionHandler:)`/`viewContext`/`NSPersistentStoreDescription` stack setup, `NSManagedObjectContext` CRUD (`insertNewObject(forEntityName:into:)`/`init(context:)`, `delete(_:)`, `save()`, `perform(_:)`/`performAndWait(_:)`, basic parent-child `parent` context), `NSFetchRequest<T>`/`NSPredicate`/`NSSortDescriptor`/`context.fetch(_:)`/`@FetchRequest` fetching, and `NSDeleteRule`'s four cases plus the required `inverseRelationship` for referential integrity. Closes the persistence seam left open by `swiftdata` (see domain-map.md Cross-Domain Notes) — the two frameworks are documented as a clean split, not an angle-split, since they solve the same problem with entirely distinct API surfaces and neither domain's KCs reference the other. Corrects a natural-but-wrong assumption from the drafting brief: `NSDeleteRule`'s case names carry a `DeleteRule` suffix (`.cascadeDeleteRule`/`.nullifyDeleteRule`/`.denyDeleteRule`/`.noActionDeleteRule`), distinct from SwiftData's shorter `.cascade`/`.nullify`/`.deny`/`.noAction` spellings for the same four concepts. `NSPersistentCloudKitContainer`/CloudKit sync, lightweight/mapping-model migration, `NSFetchedResultsController`, multi-context concurrency beyond a basic parent-child relationship, and Core Data↔SwiftData interop remain out of scope.

## [1.7.0] - 2026-08-06
### Added
- v1.7.0 release: thirteenth Tier 2 domain, `swiftdata`.
- `swiftdata` Skill (model definition, model container setup, model context CRUD, querying with `@Query`/`FetchDescriptor`, relationships and cascade delete; SwiftData framework API v1) — 5 Knowledge Contracts. Covers `@Model`/`@Attribute`/`@Relationship`/`@Transient` model declaration, `.modelContainer(for:)`/`.modelContainer(_:)`/`ModelConfiguration`/`ModelContainer(for:configurations:)` container setup, `insert(_:)`/`delete(_:)`/`save()`/`autosaveEnabled`/`undoManager` context CRUD, `@Query`/`#Predicate` vs. `FetchDescriptor`/`context.fetch(_:)` fetching, and `@Relationship(deleteRule:)`'s four cases plus the `inverse:` requirement for referential integrity. No cross-domain seam to resolve yet — Core Data remains a separate, unbuilt domain (see domain-map.md Cross-Domain Notes). Corrects two natural-but-wrong assumptions from the drafting brief: `@Model` synthesizes `PersistentModel`/`Observable` (which cover `Hashable`/`Identifiable`) but never `Codable`; and the SwiftUI `.modelContainer(for:)` modifier's `inMemory:` parameter is a distinct name from `ModelConfiguration`'s `isStoredInMemoryOnly` property, not the same symbol at two layers. CloudKit sync, schema migration, Core Data interop, `#Index`/`#Unique` beyond basic `@Attribute(.unique)`, and widget/App-Group container sharing remain out of scope.

## [1.6.0] - 2026-08-06
### Added
- v1.6.0 release: twelfth Tier 2 domain, `passkit`.
- `passkit` Skill (pass library and authorization, pass content and required fields, adding-passes UI, pass updates and push registration, Apple Pay payment request, Apple Pay authorization and result handling; PassKit framework API v1) — 6 Knowledge Contracts. Covers `PKPassLibrary` querying/adding (`isPassLibraryAvailable()`/`containsPass(_:)`/`passes()`/`passes(of:)`/`addPasses(_:withCompletionHandler:)`), `.pkpass`/`pass.json` structure (required keys, style keys, `PassFields`, current `barcodes`/`relevantDates` vs. deprecated singular forms), the `PKAddPassesViewController`/`PKAddPassButton` add-to-Wallet flow, the `webServiceURL`/`authenticationToken` update protocol, and Apple Pay via `PKPaymentRequest`/`PKPaymentAuthorizationController`/`PayWithApplePayButton` through to `PKPaymentAuthorizationControllerDelegate`/`PKPaymentAuthorizationResult`. No existing cross-domain seam to resolve. Corrects a natural-but-wrong assumption that a PassKit-specific `PKPushType` exists for pass-update push registration — it doesn't; the system Wallet component handles push tokens, not the app. Server-side pass signing/certificate management, `PKAddSecureElementPassViewController`/NFC/secure-element passes, `PKPassPersonalization`, and Apple Pay server-side merchant validation/token decryption remain out of scope.

## [1.5.0] - 2026-08-06
### Added
- v1.5.0 release: eleventh Tier 2 domain, `tipkit`.
- `tipkit` Skill (tip declaration and content, display rules and event triggers, tip options and app configuration, presenting tips and tip groups; TipKit framework API v1) — 4 Knowledge Contracts. Covers `Tip` protocol conformance on a `struct` (`title`, optional `message`/`image`, `actions`), the `#Rule(_:)` macro over `Tips.Parameter`/`Tips.Event` (AND-combined), `Tips.configure(_:)` app-launch setup plus per-tip `MaxDisplayCount`/`MaxDisplayDuration`/`IgnoresDisplayFrequency`, and presenting with `TipView`/`TipUIView`/`TipUIPopoverViewController`/`TipGroup` plus `invalidate(reason:)`. No existing cross-domain seam to resolve. Custom `TipViewStyle` authoring, watchOS-specific presentation differences, and `Tips.ConfigurationOption.cloudKitContainer(_:)` cross-device datastore sync (a real, documented TipKit capability, deliberately excluded rather than assumed nonexistent) remain out of scope.

## [1.4.0] - 2026-08-06
### Added
- v1.4.0 release: tenth Tier 2 domain, `eventkit`.
- `eventkit` Skill (authorization and access levels, event CRUD and fetch predicates, reminder CRUD and fetch, recurrence rules and EventKitUI hand-off; EventKit framework API v1) — 4 Knowledge Contracts. Covers `EKEventStore` authorization (`EKAuthorizationStatus`, iOS 17+ `requestFullAccessToEvents(completion:)`/`requestWriteOnlyAccessToEvents(completion:)`/`requestFullAccessToReminders(completion:)` vs. legacy `requestAccess(to:completion:)`), `EKEvent`/`EKReminder` CRUD and fetch predicates, and `EKRecurrenceRule`/`EKRecurrenceEnd` with the decision to hand off to EventKitUI's `EKEventEditViewController`/`EKEventViewController` instead of custom UI. No existing cross-domain seam to resolve. `EKSource`/multi-account calendar-source management, CalDAV/Exchange specifics, `EKEventStoreChanged` live-sync, and EventKit inside a widget extension (owned by `widgetkit`) remain out of scope.

## [1.3.0] - 2026-08-06
### Added
- v1.3.0 release: ninth Tier 2 domain, `backgroundtasks`.
- `backgroundtasks` Skill (background task registration and scheduling, task execution and expiration handling, processing task constraints and conditions, background refresh and widget timeline hookup; BackgroundTasks framework API v1) — 4 Knowledge Contracts. Resolves the second seam `widgetkit` had proactively deferred (background-refresh scheduling mechanics): `backgroundtasks` owns registering, submitting, and running the `BGAppRefreshTaskRequest` that produces fresh widget data; `widgetkit` continues to own the `WidgetCenter.reloadTimelines`/`reloadAllTimelines` call site and its refresh-budget reasoning once that data has landed — a clean handoff, not an angle-split. `BGContinuedProcessingTask`, legacy Background Fetch, unrelated background modes (audio/location/VoIP), and `URLSession` background transfer (owned by `networking`) remain out of scope.

## [1.2.0] - 2026-08-06
### Added
- v1.2.0 release: eighth Tier 2 domain, `app-intents`.
- `app-intents` Skill (app intent declaration and parameters, app entities and queries, App Shortcuts and Siri phrases, intent results and widget hookup; App Intents framework API v1) — 4 Knowledge Contracts. Resolves the seam `widgetkit` had proactively deferred (`AppIntent` authoring itself): `app-intents` owns declaring the intent (`perform()`, parameters, entities, result), `widgetkit` continues to own wiring an already-authored intent into a widget's `Button(intent:)`/`Toggle(_:isOn:intent:)` — a clean handoff, not an angle-split. Supersedes legacy SiriKit (donation-based intents) on current OS versions; no separate SiriKit domain planned.

## [1.1.0] - 2026-08-06
### Added
- v1.1.0 release: seventh Tier 2 domain, `widgetkit`.
- `widgetkit` Skill (widget declaration and families, timeline provider and entries, widget interactivity and deep links, timeline reloading and refresh budget; WidgetKit framework API v1) — 4 Knowledge Contracts. No existing cross-domain content to overlap with (no prior widget-design content in `swiftui`/`human-interface-guidelines`); proactively defers `AppIntent` authoring to the future `app-intents` domain and background-refresh scheduling mechanics to the future `backgroundtasks` domain.

## [1.0.9] - 2026-08-06
### Added
- v1.0.9 release: sixth Tier 2 domain, `authenticationservices`.
- `authenticationservices` Skill (Sign in with Apple request-and-credential handling, nonce and identity-token verification, credential-state checks and revocation, session persistence and sign-out; AuthenticationServices framework API v1) — 4 Knowledge Contracts. Resolves the `authentication`/`authenticationservices`/`sign-in-with-apple` three-way boundary domain-map.md had left unresolved, absorbing the former `sign-in-with-apple` placeholder outright (same framework, no distinct content). Clean handoffs with `authentication` (sign-in UX/terminology) and `security` (Keychain storage), resolving two boundaries domain-map.md had flagged proactively.

## [1.0.8] - 2026-08-06
### Added
- v1.0.8 release: fifth Tier 2 domain, `storekit`.
- `storekit` Skill (product loading and purchase, transaction verification and entitlements, transaction updates and restoring purchases, subscription status and renewal info; StoreKit 2 async/await API v1) — 4 Knowledge Contracts. Clean handoff with `app-store-review-guidelines`'s `digital-goods-iap.md`/`restore-purchases.md` (API implementation vs. review compliance), resolving the boundary domain-map.md had flagged proactively.

## [1.0.7] - 2026-08-06
### Added
- v1.0.7 release: fourth Tier 2 domain, `security`.
- `security` Skill (Keychain item CRUD, accessibility levels, access groups and sharing, storing structured/Codable data; general non-biometric-bound Keychain Services API v1) — 4 Knowledge Contracts. Clean handoff with `local-authentication`'s `keychain-biometric-binding.md` (biometric-bound access control vs. general Keychain CRUD), resolving the boundary domain-map.md had flagged proactively.

## [1.0.6] - 2026-08-06
### Added
- v1.0.6 release: third Tier 2 domain, `foundation`.
- `foundation` Skill (date/time formatting, measurement and unit formatting, Codable encoding and custom conformance, FileManager app sandbox directories; curated highest-usage v1 subset, not exhaustive) — 4 Knowledge Contracts. Angle-split with `style-guide`'s `units-of-measure.md` (unit-value production vs. copy wording) and clean handoff with `networking`'s `codable-decoding.md` (encoding vs. network-response decoding).

## [1.0.5] - 2026-08-06
### Added
- v1.0.5 release: second Tier 2 domain, `privacy`.
- `privacy` Skill (manifest file structure/bundling, required-reason API declarations, collected data type declarations, tracking domains and third-party SDK signature requirement; `PrivacyInfo.xcprivacy` implementation/schema v1) — 4 Knowledge Contracts. Angle-split with `human-interface-guidelines`'s `privacy.md` (design vs. implementation) and `app-store-review-guidelines`'s `privacy-manifest.md`/`privacy-nutrition-label.md` (implementation vs. review consequence), resolving two boundaries domain-map.md had flagged proactively.

## [1.0.4] - 2026-08-06
### Added
- v1.0.4 release: first Tier 2 domain, `usernotifications`.
- `usernotifications` Skill (authorization, local notification scheduling, remote push registration, delegate handling, actions/categories, managing pending/delivered requests and badge count; client-side UserNotifications + UIKit push-registration API v1) — 6 Knowledge Contracts. Picked as the tier's highest real-world-usage domain. Angle-split with `human-interface-guidelines`'s `notifications.md` on notification design vs. API implementation, resolving the boundary domain-map.md had flagged proactively.

## [1.0.3] - 2026-08-06
### Added
- v1.0.3 release: both named Tier 1 priority gaps closed — `human-interface-guidelines` Patterns/Components/Inputs and `swiftui` Animation/Gestures.
- Expanded `swiftui` with a new Skill, `swiftui-interaction` (implicit/explicit animation, timing curves, transitions, matchedGeometryEffect, the Animatable protocol, PhaseAnimator/KeyframeAnimator, tap/long-press gestures, drag gesture, magnification/rotation gestures, gesture composition, GestureState) — 10 Knowledge Contracts. Closes the second of the two named Tier 1 priority gaps (after HIG Patterns/Components). Second domain with more than one Skill, split by the project's Skill (≤60 lines) size cap.
- Expanded `human-interface-guidelines` with two new Skills, `human-interface-guidelines-components` and `human-interface-guidelines-patterns` (lists and tables, buttons, sheets, alerts, action sheets, navigation bars, tab bars, pickers, toggles, text fields, menus, touchscreen gestures; onboarding, searching, settings, notifications, feedback, undo/redo) — 18 Knowledge Contracts. Closes the highest-priority named Tier 1 gap. First domain with more than one Skill, split by Apple's own Foundations/Patterns/Components information architecture to stay under the project's Reference (≤80 lines) and Skill (≤60 lines) size caps.

## [1.0.2] - 2026-08-05
### Added
- v1.0.2 release: all 11 Tier 1 domains complete (`style-guide`, `human-interface-guidelines`, `app-store-review-guidelines`, `swiftui`, `accessibility`, `uikit`, `sf-symbols`, `networking`, `xcode`, `local-authentication`, `app-tracking-transparency`), plus `authentication` (cross-cutting, built ahead of tier order). See `docs/architecture/domain-map.md` for full per-domain scope and the Cross-Domain Notes documenting every resolved boundary.
- `app-tracking-transparency` Skill (authorization-request mechanics, authorization status handling, IDFA access, NSUserTrackingUsageDescription; iOS/iPadOS AppTrackingTransparency + AdSupport framework API v1) — 3 Knowledge Contracts. Closes out all 11 Tier 1 domains, replaces the prior placeholder scope in domain-map.md.
- `local-authentication` Skill (availability and biometry-type detection, policy evaluation, reason strings & NSFaceIDUsageDescription, LAError handling, LAContext lifecycle, Keychain-biometric binding, fallback UX; iOS/iPadOS LocalAuthentication framework API v1) — 7 Knowledge Contracts. Clean handoff from `authentication`, replaces the prior placeholder scope in domain-map.md.
- `xcode` Skill (build configurations, xcconfig files, schemes/targets, automatic and manual code signing, entitlements/capabilities, archive process, export options; Xcode GUI/project-file v1) — 8 Knowledge Contracts. Replaces the prior placeholder scope in domain-map.md.

## [0.1.2] - 2026-08-01
### Added
- `networking` Skill (URLSession async/await, Codable decoding, HTTP error handling, task cancellation, session configuration, App Transport Security, authenticated requests) — 8 Knowledge Contracts. Fills the "Authentication networking" gap that `authentication.md` explicitly excludes.
- `sf-symbols` Skill (rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contracts.
- `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation) — 12 Knowledge Contracts.
- `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contracts.
- `swiftui` Skill (view composition/identity, NavigationStack/NavigationSplitView, layout, state management) — 12 Knowledge Contracts.

### Changed
- npm package README synced with the GitHub repo README (updated Skill list, installation notes added).

## [0.1.1] - 2026-07-31
### Added
- Added `LICENSE`, `CONTRIBUTING.md`, `CLAUDE.md`; enriched README.
- `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contracts.
- `human-interface-guidelines` Skill (layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL) — 15 Knowledge Contracts.

### Changed
- Hardened native Skill format (real YAML frontmatter, deterministic keyword routing, Stop Conditions) across all Skills.

## [0.1.0] - 2026-07-31
### Added
- Published the initial npm installer package (`npx apple-agent-kit`).
- `authentication` Skill (sign-in, sign-up, credentials, biometrics).
- `style-guide` Skill (terminology, capitalization, punctuation, inclusive writing).

[Unreleased]: https://github.com/caglarbaranbora/Apple-Agent-Kit/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/caglarbaranbora/Apple-Agent-Kit/releases/tag/v0.1.2
