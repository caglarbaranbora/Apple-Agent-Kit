# Accessibility

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.accessibility
artifact_type: reference
title: Accessibility
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's Accessibility API documentation across SwiftUI, UIKit, and the Accessibility framework -- implementation-conventions scope (labeling, traits, value/hint, custom actions, grouping, navigation order, Dynamic Type, reduce-motion/transparency/contrast, keyboard access and focus, hidden elements, announcements, and audits).
domain: Accessibility
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/accessibility
https://developer.apple.com/documentation/accessibility/accessibilitynotification
https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement
https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement/post()
https://developer.apple.com/documentation/swiftui/accessibilityfocusstate
https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion
https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency
https://developer.apple.com/documentation/swiftui/scaledmetric
https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)
https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:)
https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:)
https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:)
https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:)
https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)
https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:)
https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)
https://developer.apple.com/documentation/uikit/uiaccessibility/isdarkersystemcolorsenabled
https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled
https://developer.apple.com/documentation/uikit/uiaccessibility/isreducetransparencyenabled
https://developer.apple.com/documentation/uikit/uiaccessibility/notification/announcement
https://developer.apple.com/documentation/uikit/uiaccessibility/post(notification:argument:)
https://developer.apple.com/documentation/uikit/uiaccessibilitycontainer
https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction
https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityhint
https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilitylabel
https://developer.apple.com/documentation/uikit/uiaccessibilityelement/accessibilityvalue
https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement
https://developer.apple.com/documentation/uikit/uiaccessibilitypriority
https://developer.apple.com/documentation/uikit/uiaccessibilitytraits
https://developer.apple.com/documentation/uikit/uifocusenvironment
https://developer.apple.com/documentation/uikit/uifontmetrics
https://developer.apple.com/documentation/xcuiautomation/xcuiaccessibilityaudittype
https://developer.apple.com/documentation/xcuiautomation/xcuiapplication/performaccessibilityaudit(for:_:)
https://developer.apple.com/videos/play/wwdc2023/10036/

## Purpose

Reference index for Apple's Accessibility API documentation across SwiftUI, UIKit, and the cross-platform Accessibility framework — implementation-conventions scope (labeling, traits, value/hint, custom actions, element grouping, navigation order, Dynamic Type API, reduce-motion/transparency/increase-contrast, keyboard access and focus, hidden/decorative elements, announcements and announcement priority, accessibility audits). Design-level accessibility guidance (Dynamic Type requirement, contrast ratio, color-alone prohibition, gesture-alternative rule) is owned by `human-interface-guidelines`, not this domain — see docs/architecture/domain-map.md Cross-Domain Notes. General XCTest/UI testing conventions beyond accessibility audits are out of scope for this pass.

Note that `AccessibilityNotification` is published under Apple's **Accessibility** framework (`documentation/accessibility/…`), not under SwiftUI, even though Apple's own example for it is SwiftUI code. It is iOS 17.0+ across SwiftUI, UIKit, and AppKit; `UIAccessibility.post(notification:argument:)` remains the pre-iOS-17, UIKit-only form.

## Primary Topics

- Element description: `accessibilityLabel`, `accessibilityTraits`, `accessibilityValue`/`accessibilityHint`
- Structure and navigation: element grouping, `accessibilitySortPriority`/`accessibilityElements` order, hidden and decorative elements
- Interaction: custom accessibility actions, Full Keyboard Access, and programmatic VoiceOver focus
- Announcements: `AccessibilityNotification.Announcement`, `UIAccessibility.post(notification:argument:)`, and `UIAccessibilityPriority`
- User preferences: Dynamic Type API, Reduce Motion, Reduce Transparency, Increase Contrast
- Verification: `performAccessibilityAudit(for:_:)` and `XCUIAccessibilityAuditType`

## Used By

- knowledge/accessibility/accessibility-labels.md ([[knowledge/accessibility/accessibility-labels]])
- knowledge/accessibility/accessibility-traits.md ([[knowledge/accessibility/accessibility-traits]])
- knowledge/accessibility/accessibility-value-and-hint.md ([[knowledge/accessibility/accessibility-value-and-hint]])
- knowledge/accessibility/custom-accessibility-actions.md ([[knowledge/accessibility/custom-accessibility-actions]])
- knowledge/accessibility/accessibility-element-grouping.md ([[knowledge/accessibility/accessibility-element-grouping]])
- knowledge/accessibility/voiceover-navigation-order.md ([[knowledge/accessibility/voiceover-navigation-order]])
- knowledge/accessibility/dynamic-type-api.md ([[knowledge/accessibility/dynamic-type-api]])
- knowledge/accessibility/reduce-motion.md ([[knowledge/accessibility/reduce-motion]])
- knowledge/accessibility/reduce-transparency-increase-contrast.md ([[knowledge/accessibility/reduce-transparency-increase-contrast]])
- knowledge/accessibility/full-keyboard-access-and-focus.md ([[knowledge/accessibility/full-keyboard-access-and-focus]])
- knowledge/accessibility/accessibility-hidden-decorative.md ([[knowledge/accessibility/accessibility-hidden-decorative]])
- knowledge/accessibility/accessibility-audits-testing.md ([[knowledge/accessibility/accessibility-audits-testing]])
- knowledge/accessibility/accessibility-announcements.md ([[knowledge/accessibility/accessibility-announcements]])
