# Full Keyboard Access and Accessibility Focus

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.full-keyboard-access-and-focus
type: knowledge
title: Full Keyboard Access and Accessibility Focus
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines making custom controls reachable via .focusable() and UIFocusEnvironment for Full Keyboard Access, and moving VoiceOver focus programmatically with @AccessibilityFocusState / UIAccessibility.post(.screenChanged).
domain: Accessibility
tags:
  - accessibility
  - focus
  - keyboard
references:
  - https://developer.apple.com/documentation/swiftui/accessibilityfocusstate
  - https://developer.apple.com/documentation/uikit/uifocusenvironment
depends_on: []
related:
  - knowledge.accessibility.custom-accessibility-actions
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent makes custom controls
reachable by Full Keyboard Access / external keyboard navigation
(`.focusable()`, `UIFocusEnvironment`), and moves VoiceOver's focus
programmatically (`@AccessibilityFocusState`, UIKit's
`UIAccessibility.post(notification: .screenChanged, argument:)`) when new
content needs the user's immediate attention.

## Scope

### Included

-   `.focusable()` for custom interactive views
-   `@AccessibilityFocusState` for programmatic VoiceOver focus
-   `UIAccessibility.post(notification: .screenChanged, argument:)`
-   Not trapping focus with no way out

### Excluded

-   Providing an activation alternative for gestures — see `custom-accessibility-actions`

## Rules

### Rule 1

Agents MUST mark custom tappable views `.focusable()` (SwiftUI) or
ensure they participate in `UIFocusEnvironment` (UIKit) so Full Keyboard
Access and external-keyboard/switch-control users can reach them by
navigating focus, not only by touch.

### Rule 2

Agents MUST move VoiceOver focus programmatically — bind
`@AccessibilityFocusState` to `true` on the relevant element, or in
UIKit call `UIAccessibility.post(notification: .screenChanged,
argument: view)` — when content appears that the user needs to know
about immediately (a validation error, a newly presented sheet's title).

### Rule 3

Agents MUST NOT trap keyboard or VoiceOver focus inside a subview with
no reachable way out — every modal or focus-scoped view (a sheet, an
alert-like overlay) must expose a focusable/actionable dismiss control.

### Rule 4

Agents SHOULD set an explicit accessibility focus target when presenting
a sheet or full-screen cover so VoiceOver announces its content
immediately, instead of leaving focus on whatever was focused
underneath.

## Compliant Example

```swift
@AccessibilityFocusState private var errorFieldFocused: Bool

TextField("Email", text: $email)
    .accessibilityFocused($errorFieldFocused)

func submit() {
    if !isValidEmail(email) {
        errorFieldFocused = true
    }
}
```
VoiceOver focus moves directly to the invalid field on submission failure. (Rule 2)

## Non-Compliant Example

```swift
func submit() {
    if !isValidEmail(email) {
        showErrorBanner = true
    }
}
```
An error banner appears, but VoiceOver focus stays wherever it was — a VoiceOver user isn't told a validation error occurred unless they happen to swipe past the banner. (Rule 2)

## Dependencies

None.

## References

-   [Apple Developer — AccessibilityFocusState](https://developer.apple.com/documentation/swiftui/accessibilityfocusstate)
-   [Apple Developer — UIFocusEnvironment](https://developer.apple.com/documentation/uikit/uifocusenvironment)
