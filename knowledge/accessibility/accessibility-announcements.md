# Accessibility Announcements

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-announcements
artifact_type: knowledge
title: Accessibility Announcements
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how an app pushes out-of-band information such as a form's validation result to an assistive app -- AccessibilityNotification.Announcement (iOS 17+) versus UIAccessibility.post(notification:.announcement), the events an announcement is and is not for, the three priorities and the fact that equal-priority announcements truncate each other, where the priority attribute lives, and the rule that an announcement is an unverifiable channel that must never be the only route to the information.
domain: Accessibility
tags:
  - accessibility
  - voiceover
  - announcement
  - announcement-priority
references:
  - https://developer.apple.com/documentation/accessibility/accessibilitynotification
  - https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement
  - https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement/post()
  - https://developer.apple.com/documentation/uikit/uiaccessibility/post(notification:argument:)
  - https://developer.apple.com/documentation/uikit/uiaccessibility/notification/announcement
  - https://developer.apple.com/documentation/uikit/uiaccessibilitypriority
  - https://developer.apple.com/videos/play/wwdc2023/10036/
depends_on: []
related:
  - knowledge.accessibility.full-keyboard-access-and-focus
  - knowledge.accessibility.accessibility-value-and-hint
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent conveys an event to an assistive app when no accessibility element carries that information -- the case a form's validation result usually falls into. Its central claim is that an announcement is a fire-and-forget channel: nothing reports whether it was spoken, and the system discards announcements by design.

## Scope

### Included

-   `AccessibilityNotification.Announcement`/`post()` (iOS 17+) and the
    older UIKit `UIAccessibility.post(notification:argument:)`
-   Which events warrant an announcement; announcing validation outcomes
-   The three priorities, their interruption behavior, and where the
    priority attribute lives

### Excluded

-   Moving VoiceOver focus to content that is on screen, including a
    field that failed validation — owned by
    `full-keyboard-access-and-focus`
-   A control's own spoken state — see `accessibility-value-and-hint`
-   Localizing the announcement string — `accessibility-labels` states
    that rule for accessibility text generally

## Rules

### Rule 1

Agents MUST post an announcement only for information no accessibility element carries. Per Apple's documentation for `.announcement`: "Use this notification to provide accessibility information about events that don't update the app's UI, or that update the UI only briefly." A validation failure rendering persistent error text *does* update the UI, so the mechanism there is moving focus to the failing field (`full-keyboard-access-and-focus`, Rule 2); an announcement is right for a result stated only transiently, such as an auto-dismissing banner.

### Rule 2

Agents MUST use `AccessibilityNotification.Announcement(_:).post()` on an iOS 17+ baseline rather than `UIAccessibility.post`. Per Apple's documentation, accessibility notifications "provide a unified, multiplatform way for your app to convey information to someone using an assistive app," and per Apple's WWDC23 session they "can be created for apps running SwiftUI, UIKit, and AppKit." `AccessibilityNotification` is iOS 17.0+; `UIAccessibility.post` remains the form for earlier deployment targets and is UIKit-only.

### Rule 3

Agents MUST NOT post several announcements in sequence without assigning priorities, because equal-priority announcements cut each other off mid-word. Apple's WWDC23 demonstration posts three at one priority and narrates the result: "Notice how the second announcement, 'Camera Loading,' interrupts 'Opening Camera'." The transcribed VoiceOver output is "Open--camera--camera active" -- two of the three were destroyed, and nothing in the app reported it.

### Rule 4

Agents MUST choose a priority from its documented interruption behavior, not from how important the message feels. Per Apple's documentation, `.high` "interrupts other speech and isn't interruptible after it starts"; `.default` "interrupts existing speech, but is interruptible if a new speech utterance starts"; `.low` is "queued and speaks after other speech utterances are complete." Per Apple's WWDC23 session a low-priority announcement is spoken only "if no new announcements have started" -- framed as intended, for "announcements that can be ignored if not spoken in time."

### Rule 5

Agents MUST set the priority on the string, not the notification -- in SwiftUI the `accessibilitySpeechAnnouncementPriority` property of an `AttributedString`, in UIKit the `NSAttributedString.Key` of that name carrying a `UIAccessibilityPriority`. Apple's UIKit form:

```swift
let highPriorityAnnouncement = NSAttributedString(string: "Camera active", attributes:
[NSAttributedString.Key.accessibilitySpeechAnnouncementPriority: UIAccessibilityPriority.high])
```

An announcement built from a plain `String` therefore carries no priority attribute; Apple does not document what the system substitutes, so agents MUST NOT assume `.default`.

### Rule 6

Agents MUST NOT leave an announcement as the only route to the information. `post()` returns `Void` and reports nothing about delivery, Rules 3 and 4 both describe announcements the system discards by design, and an announcement leaves behind no element to navigate back to. The information MUST also be reachable by navigation — as element text, an `accessibilityValue`, or a label.

## Compliant Example

```swift
// The banner auto-dismisses, so no element carries this afterwards --
// Rule 1's case for an announcement.
guard validate() else {
    var message = AttributedString("3 fields need attention")
    message.accessibilitySpeechAnnouncementPriority = .high      // Rules 4, 5
    AccessibilityNotification.Announcement(message).post()       // Rule 2
    firstInvalidFieldFocused = true   // focus: full-keyboard-access-and-focus
    return
}
```
The banner's text is also rendered as an element, so the count survives the speech (Rule 6).

## Non-Compliant Example

```swift
guard validate() else {
    for field in invalidFields {
        AccessibilityNotification.Announcement("\(field.name) is invalid").post()
    }
    return
}
```
One announcement per invalid field, none carrying a priority attribute, so each interrupts the one before it and only fragments of the last survive — the failure Apple demonstrates in WWDC23 (Rules 3, 5). Nothing reports the loss, and because the errors exist nowhere the user can navigate to, anyone who misses the speech has no way to recover them (Rule 6).

## Dependencies

None. `full-keyboard-access-and-focus` covers the complementary move — sending VoiceOver focus to content that *is* on screen.

## References

-   [Apple Developer — AccessibilityNotification](https://developer.apple.com/documentation/accessibility/accessibilitynotification) · [Announcement](https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement) · [post()](https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement/post())
-   [Apple Developer — UIAccessibility.post(notification:argument:)](https://developer.apple.com/documentation/uikit/uiaccessibility/post(notification:argument:)) · [UIAccessibility.Notification.announcement](https://developer.apple.com/documentation/uikit/uiaccessibility/notification/announcement)
-   [Apple Developer — UIAccessibilityPriority](https://developer.apple.com/documentation/uikit/uiaccessibilitypriority)
-   [WWDC23 — Build accessible apps with SwiftUI and UIKit](https://developer.apple.com/videos/play/wwdc2023/10036/)
