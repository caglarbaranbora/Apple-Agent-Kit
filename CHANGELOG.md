# Changelog

Bu dosya projede önemli değişiklikleri kaydeder. Format [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) temel alınmıştır.

Proje tek bir versiyon numarası kullanır (`README.md` ve `npx/package.json` aynı versiyonu paylaşır).

## [Unreleased]

## [0.1.2] - 2026-08-01
### Added
- `networking` Skill (URLSession async/await, Codable decoding, HTTP hata yönetimi, task cancellation, session configuration, App Transport Security, authenticated requests) — 8 Knowledge Contract. `authentication.md`'nin dışarıda bıraktığı "Authentication networking" boşluğunu dolduruyor.
- `sf-symbols` Skill (rendering modes, symbol variants, variable value, weight/scale, color/tinting, custom symbol usage, UIKit SymbolConfiguration; SwiftUI + UIKit) — 8 Knowledge Contract.
- `uikit` Skill (view controller lifecycle/composition, Auto Layout, navigation, diffable table/collection views, cell configuration, modal presentation) — 12 Knowledge Contract.
- `accessibility` Skill (labels/traits/value/hint, custom actions, element grouping, VoiceOver navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access & focus, accessibility audits; SwiftUI + UIKit) — 12 Knowledge Contract.
- `swiftui` Skill (view composition/identity, NavigationStack/NavigationSplitView, layout, state management) — 12 Knowledge Contract.

### Changed
- npm paketi README'si GitHub repo README'si ile senkronize edildi (güncel Skill listesi, kurulum notları eklendi).

## [0.1.1] - 2026-07-31
### Added
- `LICENSE`, `CONTRIBUTING.md`, `CLAUDE.md` eklendi; README zenginleştirildi.
- `app-store-review-guidelines` Skill (App Completeness, Accurate Metadata, In-App Purchase, Minimum Functionality, Spam/Duplicate, Privacy manifest & nutrition label) — 12 Knowledge Contract.
- `human-interface-guidelines` Skill (layout, color, typography, app icons, images, inclusion, accessibility-design, dark mode, materials, motion, icons, branding, privacy-design, SF Symbols usage, RTL) — 15 Knowledge Contract.

### Changed
- Native Skill formatı sertleştirildi (gerçek YAML frontmatter, deterministik keyword routing, Stop Conditions) — tüm Skill'lerde.

## [0.1.0] - 2026-07-31
### Added
- İlk npm installer paketi (`npx apple-agent-kit`) yayınlandı.
- `authentication` Skill (sign-in, sign-up, credentials, biometrics).
- `style-guide` Skill (terminology, capitalization, punctuation, inclusive writing).

[Unreleased]: https://github.com/caglarbaranbora/Apple-Agent-Kit/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/caglarbaranbora/Apple-Agent-Kit/releases/tag/v0.1.2
