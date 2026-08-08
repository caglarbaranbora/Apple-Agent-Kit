# Reduce Motion

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.accessibility.reduce-motion
artifact_type: knowledge
title: Reduce Motion
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines checking accessibilityReduceMotion (SwiftUI environment value) / UIAccessibility.isReduceMotionEnabled (UIKit) before playing large-scale motion animations, substituting a simpler alternative instead of disabling feedback entirely.
domain: Accessibility
tags:
  - accessibility
  - motion
  - reduce-motion
references:
  - https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion
  - https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled
depends_on: []
related:
  - knowledge.accessibility.reduce-transparency-increase-contrast
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent checks the user's Reduce
Motion setting (`@Environment(\.accessibilityReduceMotion)` in SwiftUI,
`UIAccessibility.isReduceMotionEnabled` in UIKit) and substitutes a
simpler alternative for large-scale motion, rather than either ignoring
the setting or removing state-communicating feedback entirely.

## Scope

### Included

-   Reading `accessibilityReduceMotion`/`isReduceMotionEnabled`
-   Substituting motion with a crossfade or static alternative
-   Reacting to the setting changing at runtime

### Excluded

-   Transparency/contrast settings — see `reduce-transparency-increase-contrast`

## Rules

### Rule 1

Agents MUST check `@Environment(\.accessibilityReduceMotion)` (SwiftUI)
or `UIAccessibility.isReduceMotionEnabled` (UIKit) before playing
large-scale motion — parallax effects, zoom/scale transitions,
auto-playing motion backgrounds — and substitute a simple crossfade or
static presentation when the setting is on.

### Rule 2

Agents MUST NOT remove state-communicating feedback entirely when Reduce
Motion is on — replace the motion-heavy animation with a reduced-motion
alternative (opacity fade, instant state change) rather than silence.

### Rule 3

Agents SHOULD let the SwiftUI environment value drive recomputation (it
updates automatically when the setting changes) or, in UIKit, observe
`UIAccessibility.reduceMotionStatusDidChangeNotification` so the app
reacts to the user toggling the setting live in Settings without
requiring a relaunch.

### Rule 4

Agents MUST NOT gate accessibility semantics (labels, values, traits)
behind the Reduce Motion check — it governs animation and motion only,
not VoiceOver content.

## Compliant Example

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

var body: some View {
    CardView()
        .transition(reduceMotion ? .opacity : .scale.combined(with: .opacity))
}
```
Falls back to a simple opacity transition when Reduce Motion is enabled. (Rule 1)

## Non-Compliant Example

```swift
var body: some View {
    CardView()
        .transition(.scale.combined(with: .opacity))
        .animation(.spring(response: 0.4, dampingFraction: 0.6), value: isVisible)
}
```
Large-scale spring/scale animation plays unconditionally regardless of the user's Reduce Motion setting. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — accessibilityReduceMotion](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion)
-   [Apple Developer — UIAccessibility isReduceMotionEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled)
