# SwiftUI

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/swiftui

## Purpose

Reference index for Apple's SwiftUI framework documentation,
implementation-conventions scope (Views, Navigation, Layout, State
management), targeting iOS 17+ APIs. Visual/UX design guidance for what
a screen should look like is owned by `human-interface-guidelines`, not
this domain — see docs/architecture/domain-map.md Cross-Domain Notes.
Animation, gestures, previews, and custom `Layout` protocol
conformances are out of scope for this pass.

## Primary Topics

- View composition and ViewBuilder
- View identity (ForEach/List, Identifiable)
- Modifier order and view wrapping
- NavigationStack and NavigationPath
- NavigationSplitView
- Stacks and spacing (VStack/HStack/ZStack)
- Safe area (safeAreaInset, ignoresSafeArea)
- Lazy grids and lazy stacks
- GeometryReader
- State and Binding
- The Observable macro
- Environment values

## Used By

- knowledge/swiftui/view-composition.md ([[knowledge/swiftui/view-composition]])
- knowledge/swiftui/view-identity.md ([[knowledge/swiftui/view-identity]])
- knowledge/swiftui/modifier-order.md ([[knowledge/swiftui/modifier-order]])
- knowledge/swiftui/navigation-stack.md ([[knowledge/swiftui/navigation-stack]])
- knowledge/swiftui/navigation-split-view.md ([[knowledge/swiftui/navigation-split-view]])
- knowledge/swiftui/stacks-and-spacing.md ([[knowledge/swiftui/stacks-and-spacing]])
- knowledge/swiftui/safe-area.md ([[knowledge/swiftui/safe-area]])
- knowledge/swiftui/lazy-grids.md ([[knowledge/swiftui/lazy-grids]])
- knowledge/swiftui/geometry-reader-anti-pattern.md ([[knowledge/swiftui/geometry-reader-anti-pattern]])
- knowledge/swiftui/state-and-binding.md ([[knowledge/swiftui/state-and-binding]])
- knowledge/swiftui/observable-macro.md ([[knowledge/swiftui/observable-macro]])
- knowledge/swiftui/environment-values.md ([[knowledge/swiftui/environment-values]])
