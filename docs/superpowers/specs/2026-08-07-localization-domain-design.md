# Localization Domain — Design Spec

Status: Draft
Version: 0.1.0
Date: 2026-08-07

## Purpose

Build the `localization` Tier 2 domain: extracting, storing, and resolving
an app's user-facing strings and resources across languages and regions,
via String Catalogs and the Foundation/SwiftUI/UIKit localization APIs.

This is the 17th and final Tier 2 domain. Once it ships, Tier 2 is fully
complete and the roadmap advances to Tier 3 (see
`docs/architecture/domain-map.md`).

## Scope

### Domain type

API-implementation, matching all 16 completed Tier 2 domains.

`docs/architecture/domain-map.md`'s current row for this domain reads
`Language, terminology` / `Localization and translation workflow
conventions`. That text is an unrevised placeholder from the original
2026-07-31 27-domain roadmap, written before the API-implementation domain
pattern was established, and before `style-guide` shipped and took
ownership of terminology. It is superseded by this spec, and the row is
rewritten as part of this work.

A translation-workflow/process domain was explicitly considered and
rejected: the repo has no process-domain precedent, and
`scripts/validate_artifact.py`'s Knowledge Contract schema is built around
Rules/Excluded/Examples, not procedure steps.

### Platform

iOS/iPadOS, iOS 17+ / Xcode 15+, matching every prior domain.

String Catalogs (`.xcstrings`) are the primary mechanism. Legacy
`.strings`, `.stringsdict`, and `NSLocalizedString` are covered only to the
extent an agent meets them in an existing codebase — the same
current-conventions-first stance `swiftui` took when it scoped out legacy
`ObservableObject`/`NavigationView` migration guidance.

### Included (v1)

- String Catalog (`.xcstrings`) file mechanics: adding one to a target,
  automatic string extraction from source, the literal-string requirement
  that extraction depends on, translator `comment:` context, translation
  states in the catalog editor, manual keys vs. value-as-key, and marking
  strings as not-for-translation
- The localized-string API surface: `String(localized:)` and its
  `defaultValue:`/`table:`/`bundle:`/`comment:` parameters,
  `LocalizedStringResource` and its deferred-resolution use case,
  `LocalizedStringKey` and SwiftUI's implicit localization of `Text`
  string literals (including exactly when SwiftUI does *not* localize
  automatically), interpolation/format placeholders, and where
  `NSLocalizedString` still applies
- Plural and device variation: plural variation in a String Catalog, the
  CLDR plural categories and their language-dependence, device variation,
  substitutions for strings with more than one varying value, and the
  legacy `.stringsdict` equivalent
- Locale and language resolution: `Locale.current` vs.
  `Locale.autoupdatingCurrent`, `Locale.preferredLanguages` vs.
  `Bundle.preferredLocalizations`, the modern `Locale.Language`/
  `Locale.Region` split, development region and base localization, the
  per-app language setting, and the fallback chain iOS walks to pick a
  localization
- Layout direction and RTL APIs: `\.layoutDirection` in SwiftUI, why
  `leading`/`trailing` are correct and `left`/`right` are not,
  `flipsForRightToLeftLayoutDirection(_:)`, UIKit's
  `semanticContentAttribute`/`effectiveUserInterfaceLayoutDirection`,
  RTL-aware Auto Layout anchors, direction-aware images, SF Symbols RTL
  behavior, and detecting direction via
  `Locale.Language.characterDirection`
- Localized resources and Info.plist: `InfoPlist.xcstrings` (localizing
  permission usage descriptions and `CFBundleDisplayName`), `.lproj`
  structure and bundle resolution, localizing asset-catalog images and
  resource files, framework/Swift-package localization via `Bundle.module`
  and `defaultLocalization`, and `Bundle.localizedString(forKey:value:table:)`

### Excluded (v1, deferred)

- **Xcode project-configuration side of localization** — adding a language
  to a project, target localization settings, and the `.xcloc`/XLIFF
  export-and-import round trip with translators. This is GUI/project-file
  work, which is `xcode`'s defined territory (build configurations,
  xcconfig, schemes, signing, entitlements, archive/export). Deferred to a
  future `xcode` expansion, the same hand-off precedent already on record
  for `testing` → `xcode` (Test Plans and code coverage).
- **The iOS 18 Translation framework** (`TranslationSession`,
  `.translationTask`, `.translationPresentation`) — a real, documented
  capability, deliberately excluded rather than assumed nonexistent,
  following the `tipkit` / `cloudKitContainer(_:)` precedent. It solves a
  different problem (translating user content at runtime) from this domain
  (shipping the app's own text pre-translated), and requires iOS 18, above
  this domain's iOS 17 baseline.
- Copy wording, capitalization, punctuation, and international
  representation/formatting *rules for the source text itself* — owned by
  `style-guide` (`international-style.md`,
  `international-formatting.md`, `units-of-measure.md`)
- Date, time, number, and measurement formatting mechanics — owned by
  `foundation` (`date-time-formatting.md`,
  `measurement-and-unit-formatting.md`)
- RTL visual-design guidance (what mirrors, numeral handling, icon-flip
  decisions) — owned by `human-interface-guidelines` (`right-to-left.md`)
- App Store Connect localized metadata (app name, description,
  screenshots, keywords) — a submission surface, adjacent to
  `app-store-review-guidelines`, not a runtime API
- Localized remote push payloads (`loc-key`/`loc-args` in an APNs payload)
  — `usernotifications` already scopes out APNs server-side payload
  construction
- Localizing App Shortcuts phrases and `AppEnum` display representations —
  owned by `app-intents`
- macOS/watchOS/tvOS-specific localization behavior
- Machine translation, translation-memory tooling, and translator vendor
  workflow

## Cross-Domain Boundaries

Four boundaries, recorded as new bullets in `docs/architecture/domain-map.md`'s
Cross-Domain Notes.

### 1. vs. `human-interface-guidelines` — angle-split

`knowledge.human-interface-guidelines.right-to-left` already owns
RTL as a design topic: layout mirroring, numeral handling, and icon
flipping. Split follows the established `accessibility` vs.
`human-interface-guidelines` pattern: `human-interface-guidelines` keeps
the design layer (*what* mirrors and *why*), `localization` owns the API
layer (*how* — which property, which modifier, correct syntax).

`layout-direction-and-rtl-apis.md` cross-references
`knowledge.human-interface-guidelines.right-to-left` via `related:` rather
than restating its Rules.

This also closes a seam that document left open: `right-to-left.md`'s own
Excluded section currently states that "SF Symbols' built-in RTL-variant
mechanics specifically is not yet covered by any current contract."
`localization` covers it, to the extent Apple's documentation supports a
factual account of it.

### 2. vs. `foundation` — clean handoff

No overlap. `localization` owns where a `Locale` comes from and how it is
resolved (`Locale.current` vs. `autoupdatingCurrent`, preferred-language
lists, the bundle fallback chain). `foundation` continues to own passing a
`Locale` to a formatter to produce a value
(`date-time-formatting.md`, `measurement-and-unit-formatting.md`).

No correction is needed on `foundation`'s side: its domain-map scope cell
already reads "No … Locale/Bundle localization," written before this
domain existed. Same shape as the existing `foundation` ↔ `networking`
Codable handoff.

### 3. vs. `style-guide` — clean handoff

No overlap. `style-guide` owns what the English source copy says and how it
is written and formatted, including its three international-facing KCs
(`international-style.md` — country/currency/language codes and telephone
numbers; `international-formatting.md` — locale-neutral numeric/date
formatting in copy; `units-of-measure.md`). None of them touch an API.

`localization` owns the mechanics that come after the copy exists: how it
is extracted, stored, varied, and resolved at runtime. Same shape as the
existing `networking` ↔ `authentication` handoff.

`international-style.md`'s guidance to write simple structures so
translators and machine translation have less to fight is adjacent to this
domain in intent, but is a copy-authoring rule, not an API rule — the
handoff holds.

### 4. vs. `xcode` — deferred, not yet resolved

The Xcode-side surface named in Excluded above (adding project languages,
target localization settings, `.xcloc`/XLIFF export-import) belongs to
`xcode` by domain type, but `xcode`'s v1 is complete and does not cover it.
Recorded as an open boundary, to be resolved when `xcode` is next expanded
— the same wording style as the `arkit`/`realitykit` note already on
record.

### Open item to check during execution

`knowledge/accessibility/accessibility-labels.md` contains the substring
"localiz". Verify during execution whether this is only an instruction to
localize the label (in which case a one-way `related:` pointer from this
domain suffices, and no fifth Cross-Domain Note is needed) or genuine
overlapping content requiring an explicit boundary bullet.

## Knowledge Contracts (6)

All under `knowledge/localization/`, IDs `knowledge.localization.<slug>`.

1. **`string-catalogs-and-extraction.md`** — the `.xcstrings` file: what it
   is, adding it to a target, how Xcode extracts strings from source and
   the literal-argument requirement that extraction depends on, the
   `comment:` parameter as translator context, translation states in the
   editor, manual keys vs. value-as-key, marking strings not-for-translation,
   and what happens to a catalog entry when its source call site changes.

2. **`localized-string-apis.md`** — `String(localized:)` and its parameter
   set; `LocalizedStringResource` and when deferred resolution is the right
   choice; `LocalizedStringKey` and SwiftUI's implicit `Text` literal
   localization, including the cases where SwiftUI does not localize;
   interpolation and format placeholders; the remaining role of
   `NSLocalizedString`. Depends on `string-catalogs-and-extraction`.

3. **`plural-and-device-variations.md`** — plural variation in a String
   Catalog, the CLDR plural categories and why the set that applies is
   language-dependent, device variation, substitutions for multi-variable
   strings, the legacy `.stringsdict` equivalent, and why hand-rolling
   singular/plural with a conditional is wrong. Depends on
   `string-catalogs-and-extraction`.

4. **`locale-and-language-resolution.md`** — `Locale.current` vs.
   `Locale.autoupdatingCurrent`; `Locale.preferredLanguages` vs.
   `Bundle.preferredLocalizations` vs. `Bundle.localizations`; the modern
   `Locale.Language`/`Locale.Region` split against the older string
   properties; development region and base localization; the per-app
   language setting; and the fallback chain iOS walks when the user's
   preferred language is not among the app's localizations.
   Cross-references `foundation`'s formatter KCs via `related:`.

5. **`layout-direction-and-rtl-apis.md`** — SwiftUI `\.layoutDirection`
   and `LayoutDirection`; leading/trailing over left/right;
   `flipsForRightToLeftLayoutDirection(_:)`; UIKit
   `semanticContentAttribute`, `effectiveUserInterfaceLayoutDirection`,
   and RTL-aware Auto Layout anchors; direction-aware images; SF Symbols
   RTL behavior; `Locale.Language.characterDirection` for programmatic
   detection; and how to exercise RTL without installing an RTL language.
   Cross-references `knowledge.human-interface-guidelines.right-to-left`
   via `related:`.

6. **`localized-resources-and-infoplist.md`** — `InfoPlist.xcstrings` for
   permission usage descriptions and `CFBundleDisplayName`; `.lproj`
   structure and how the bundle resolves it; localizing asset-catalog
   images and resource files; framework and Swift-package localization
   (`Bundle.module`, `defaultLocalization`);
   `Bundle.localizedString(forKey:value:table:)` for non-main-bundle
   lookup. Cross-references
   `knowledge.app-store-review-guidelines.permission-usage-strings` via
   `related:` — that KC owns the English wording of a usage string, this
   one owns getting it translated.

## Reference

`references/apple/localization.md` — index into Apple's localization
documentation
(https://developer.apple.com/documentation/xcode/localization) and the
related Foundation/SwiftUI/UIKit symbol pages, scoped to the topics above,
carrying the same exclusion note as this spec's Excluded section.

Sourcing: every claim traced to an official Apple page (developer.apple.com
documentation, WWDC session transcripts, or Xcode Help). Research is
delegated to parallel subagents, one per topic pair, and is expected to
surface corrected findings — the documented behavior that contradicts the
common developer assumption — in the same way prior domains surfaced
`@Published`'s `willSet` timing and Core Data's `DeleteRule`-suffixed case
names.

## Skill

`skills/localization/SKILL.md` — one Skill routing all 6 KCs, native Skill
format (real YAML frontmatter, `## Purpose` / `## Routing` /
`## Stop Conditions`), matching every other domain skill.

Trigger keywords: `String Catalog`, `.xcstrings`, `String(localized:)`,
`LocalizedStringResource`, `LocalizedStringKey`, `NSLocalizedString`,
`localization`, `localize`, `translate`, `pluralization`, `stringsdict`,
`Locale`, `preferredLanguages`, `preferredLocalizations`, `lproj`,
`InfoPlist.xcstrings`, `layoutDirection`, `RTL`, `right-to-left`,
`semanticContentAttribute`, `flipsForRightToLeftLayoutDirection`,
`CFBundleDevelopmentRegion`, `CFBundleDisplayName`, `Bundle.module`.

## Documentation Updates

Per `CLAUDE.md`'s "Updating README.md" rule, same PR as the domain:

- `docs/architecture/domain-map.md` — Tier 2 row (line 46) Initial
  Scope/Owns cells rewritten from the `Language, terminology` placeholder
  to detailed v1 scope wording; four new Cross-Domain Notes bullets; the
  "Completed:" paragraph on line 19 gets the `localization` clause
  appended as the seventeenth Tier 2 domain, closing out Tier 2 entirely.
- `README.md` — new `localization` Skills bullet; new top-of-list
  "What's New" line, then the section trimmed back to its 3 most recent
  bullets.
- `CHANGELOG.md` — new entry under `## [Unreleased]`.
- `skills/index.md` — new Discovery Rules row with the trigger keywords
  above.

### Release version

Repo history bumps the shared release version in a separate chore commit
after the domain lands (`2a38eb1` docs → `62c40ad` chore: bump to 2.0.0 →
merge). This domain follows that: the domain PR adds its `[Unreleased]`
CHANGELOG entry only, and a follow-up chore commit bumps all five
release-version files to **2.1.0** together —
`README.md`, `npx/README.md`, `npx/package.json`,
`.claude-plugin/plugin.json`, `CHANGELOG.md`.

No `npm publish`: `npx/bin/install.js` and `npx/package.json`'s installer
behavior are unchanged, and per `CLAUDE.md` content ships to users
directly from `main`.

## Validation

Same as every prior domain:

```bash
python3 scripts/validate_artifact.py references/apple/localization.md --type reference
python3 scripts/validate_artifact.py knowledge/localization/<each>.md --type knowledge
python3 scripts/validate_artifact.py skills/localization/SKILL.md --type skill
python3 -m unittest tests/test_validate_artifact.py -v
claude plugin validate .
```

Plus the five-file release-version consistency check before the version
bump commit.

## Out of Scope for This Spec

- The `xcode` expansion that will absorb project-language configuration
  and the XLIFF export-import round trip.
- The iOS 18 Translation framework, whether as part of this domain or a
  future one.
- Tier 3 sequencing and any Tier 1/Tier 2 completeness backfill — decided
  after this domain ships and Tier 2 closes.
