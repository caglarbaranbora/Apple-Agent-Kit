# Accessibility Audits and Testing

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.accessibility.accessibility-audits-testing
artifact_type: knowledge
title: Accessibility Audits and Testing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of Xcode's Accessibility Inspector and XCUIApplication's performAccessibilityAudit() to catch missing labels, low contrast, and undersized hit targets automatically, alongside required manual VoiceOver verification.
domain: Accessibility
tags:
  - accessibility
  - testing
  - audits
references:
  - https://developer.apple.com/documentation/xcuiautomation/xcuiapplication/performaccessibilityaudit(for:_:)
  - https://developer.apple.com/documentation/xcuiautomation/xcuiaccessibilityaudittype
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent verifies accessibility
implementation using Xcode's Accessibility Inspector and
`XCUIApplication`'s `performAccessibilityAudit()` (from the
`XCUIAutomation` module, used inside XCTest UI test targets), and why
automated audits alone are insufficient — reading order and
gesture-alternative correctness still require a manual VoiceOver
walkthrough.

## Scope

### Included

-   `XCUIApplication().performAccessibilityAudit()` in UI tests
-   `XCUIAccessibilityAuditType` scoping
-   Xcode's Accessibility Inspector for manual inspection
-   Limits of automated audits

### Excluded

-   General XCTest/Swift Testing/UI-testing conventions beyond accessibility audits — owned by the future `testing` domain

## Rules

### Rule 1

Agents MUST call `app.performAccessibilityAudit()` in UI test suites for
primary/representative screens, so missing labels, insufficient
contrast, and undersized hit targets are caught automatically in CI
rather than only by manual review.

### Rule 2

Agents MUST inspect an audit failure with Xcode's Accessibility
Inspector before dismissing it as a false positive — the inspector shows
exactly which element and property triggered the issue.

### Rule 3

Agents SHOULD scope audits with `XCUIAccessibilityAuditType` (e.g.
excluding a specific category that's a known, accepted exception for one
screen) rather than disabling `performAccessibilityAudit()` entirely
when one category proves noisy for that screen.

### Rule 4

Agents MUST NOT treat a passing automated audit as sufficient
verification on its own — `performAccessibilityAudit()` does not check
VoiceOver reading order or whether gesture-only interactions have a
custom-action alternative; a manual VoiceOver walkthrough is still
required for those.

## Compliant Example

```swift
func testProfileScreenAccessibility() throws {
    let app = XCUIApplication()
    app.launch()
    app.buttons["Profile"].tap()

    try app.performAccessibilityAudit()
}
```
Automated audit runs against the Profile screen as part of the UI test suite. (Rule 1)

## Non-Compliant Example

```swift
func testProfileScreenLoads() throws {
    let app = XCUIApplication()
    app.launch()
    app.buttons["Profile"].tap()

    XCTAssertTrue(app.staticTexts["Profile"].exists)
}
```
UI test verifies the screen loads but never runs an accessibility audit, so missing labels or low-contrast issues on this screen go undetected until manual review, if ever. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — performAccessibilityAudit(for:_:)](https://developer.apple.com/documentation/xcuiautomation/xcuiapplication/performaccessibilityaudit(for:_:))
-   [Apple Developer — XCUIAccessibilityAuditType](https://developer.apple.com/documentation/xcuiautomation/xcuiaccessibilityaudittype)
