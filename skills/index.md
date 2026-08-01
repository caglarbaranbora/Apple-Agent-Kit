# Skills Index

Status: Draft
Version: 0.1.0

## Purpose
Maps implementation tasks to the correct Skill.

## Discovery Rules

| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/SKILL.md |
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/SKILL.md |
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |
| App Store submission, App Review rejection, in-app purchase, IAP, restore purchases, demo account, screenshot requirements, app description accuracy, privacy manifest, PrivacyInfo.xcprivacy, privacy nutrition label, spam app, duplicate app, minimum functionality, permission usage string | skills/app-store-review-guidelines/SKILL.md |
| SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea | skills/swiftui/SKILL.md |
| VoiceOver, accessibilityLabel, accessibilityTraits, accessibilityValue, accessibilityHint, accessibilityAction, UIAccessibilityCustomAction, accessibilityElement, isAccessibilityElement, accessibilitySortPriority, Dynamic Type, ScaledMetric, UIFontMetrics, Reduce Motion, Reduce Transparency, Increase Contrast, Full Keyboard Access, AccessibilityFocusState, accessibilityHidden, performAccessibilityAudit, Accessibility Inspector | skills/accessibility/SKILL.md |
| UIKit, UIViewController, viewDidLoad, viewWillAppear, addChild, NSLayoutConstraint, layout anchors, UIStackView, safeAreaLayoutGuide, UINavigationController, UITabBarController, UITableViewDiffableDataSource, UICollectionViewCompositionalLayout, UICollectionViewDiffableDataSource, CellRegistration, prepareForReuse, present, dismiss, UIModalPresentationStyle | skills/uikit/SKILL.md |

## Resolution Rules

1. Match the most specific task.
2. Load exactly one primary Skill.
3. The Skill routes Knowledge Contracts.
4. If no Skill matches, stop and report a missing Skill.
