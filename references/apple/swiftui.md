# SwiftUI

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: reference.apple.swiftui
artifact_type: reference
title: SwiftUI
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for the Apple SwiftUI documentation behind skill.swiftui.foundations -- views and view composition, view identity, modifier order, NavigationStack/NavigationSplitView and migration away from NavigationView, stack and lazy layout, safe area, GeometryReader, State/Binding, the Observable macro and migration away from ObservableObject, and Environment values.
domain: SwiftUI
last_updated: 2026-08-07
```

## Source

https://developer.apple.com/documentation/swiftui
https://developer.apple.com/documentation/observation/observable()
https://developer.apple.com/documentation/observation/observationignored()
https://developer.apple.com/documentation/swift/identifiable
https://developer.apple.com/documentation/swiftui/bindable
https://developer.apple.com/documentation/swiftui/binding
https://developer.apple.com/documentation/swiftui/environment
https://developer.apple.com/documentation/swiftui/environmentkey
https://developer.apple.com/documentation/swiftui/foreach
https://developer.apple.com/documentation/swiftui/geometryreader
https://developer.apple.com/documentation/swiftui/hstack
https://developer.apple.com/documentation/swiftui/lazyvgrid
https://developer.apple.com/documentation/swiftui/lazyvstack
https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app
https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro
https://developer.apple.com/documentation/swiftui/migrating-to-new-navigation-types
https://developer.apple.com/documentation/swiftui/navigationlink
https://developer.apple.com/documentation/swiftui/navigationpath
https://developer.apple.com/documentation/swiftui/navigationsplitview
https://developer.apple.com/documentation/swiftui/navigationstack
https://developer.apple.com/documentation/swiftui/navigationview
https://developer.apple.com/documentation/swiftui/state
https://developer.apple.com/documentation/swiftui/view
https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:)
https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:)
https://developer.apple.com/documentation/swiftui/viewmodifier
https://developer.apple.com/documentation/swiftui/vstack
https://developer.apple.com/documentation/swiftui/zstack

## Purpose

Reference index for the Apple SwiftUI documentation behind `skill.swiftui.foundations` — views, navigation, layout, and state management, targeting iOS 17+ APIs. Animation and gesture sources are indexed by `references/apple/swiftui-interaction.md` ([[references/apple/swiftui-interaction]]), which backs `skill.swiftui.interaction`; the two Skills were split before their References were, and this file's scope was narrowed to match in 2026-08. Visual/UX design guidance for what a screen should look like is owned by `human-interface-guidelines`, not this domain — see docs/architecture/domain-map.md Cross-Domain Notes. Previews and custom `Layout` protocol conformances are out of scope for this pass.

Note that the two legacy-migration paths this Reference indexes have different platform floors: Observation requires iOS 17/iPadOS 17/macOS 14/tvOS 17/watchOS 10, while `NavigationStack`/`NavigationSplitView` require iOS 16/iPadOS 16/macOS 13/tvOS 16/watchOS 9/visionOS 1. A deployment target can permit one and not the other.

## Primary Topics

- Views: composition, `ViewBuilder`, `ViewModifier`, modifier order, and view identity in `ForEach`/`List`
- Navigation: `NavigationStack`, `NavigationPath`, `NavigationSplitView`, `NavigationLink`, and the deprecated `NavigationView` they replace
- Layout: `VStack`/`HStack`/`ZStack`, `LazyVGrid`/`LazyVStack`, safe-area insets, and `GeometryReader`
- State: `@State`, `@Binding`, `@Bindable`, `@Environment`/`EnvironmentKey`
- Observation: the `@Observable` and `@ObservationIgnored` macros, and the `ObservableObject` protocol they replace
- Migration: Apple's two published migration articles for the paths above

## Used By

- knowledge/swiftui/view-composition.md ([[knowledge/swiftui/view-composition]])
- knowledge/swiftui/view-identity.md ([[knowledge/swiftui/view-identity]])
- knowledge/swiftui/modifier-order.md ([[knowledge/swiftui/modifier-order]])
- knowledge/swiftui/navigation-stack.md ([[knowledge/swiftui/navigation-stack]])
- knowledge/swiftui/navigation-split-view.md ([[knowledge/swiftui/navigation-split-view]])
- knowledge/swiftui/navigation-view-migration.md ([[knowledge/swiftui/navigation-view-migration]])
- knowledge/swiftui/stacks-and-spacing.md ([[knowledge/swiftui/stacks-and-spacing]])
- knowledge/swiftui/safe-area.md ([[knowledge/swiftui/safe-area]])
- knowledge/swiftui/lazy-grids.md ([[knowledge/swiftui/lazy-grids]])
- knowledge/swiftui/geometry-reader-anti-pattern.md ([[knowledge/swiftui/geometry-reader-anti-pattern]])
- knowledge/swiftui/state-and-binding.md ([[knowledge/swiftui/state-and-binding]])
- knowledge/swiftui/observable-macro.md ([[knowledge/swiftui/observable-macro]])
- knowledge/swiftui/observable-object-migration.md ([[knowledge/swiftui/observable-object-migration]])
- knowledge/swiftui/environment-values.md ([[knowledge/swiftui/environment-values]])
