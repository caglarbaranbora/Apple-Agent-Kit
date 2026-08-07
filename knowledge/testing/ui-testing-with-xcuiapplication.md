# UI Testing with XCUIApplication

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.testing.ui-testing-with-xcuiapplication
artifact_type: knowledge
title: UI Testing with XCUIApplication
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines launching the app under test with XCUIApplication().launch(), the continueAfterFailure = false convention in setUp() for UI tests, XCUIElement query-type properties and identifier-based element lookup, and asserting UI state with exists/waitForExistence(timeout:) plus basic interaction via tap()/typeText(_:).
domain: Testing
tags:
  - xcuitest
  - xcuiapplication
  - xcuielement
  - accessibility-identifier
  - ui-testing
references:
  - https://developer.apple.com/documentation/xcuiautomation/xcuiapplication
  - https://developer.apple.com/documentation/xcuiautomation/xcuielement
  - https://developer.apple.com/documentation/xcuiautomation/xcuielementquery/subscript(_:)
  - https://developer.apple.com/documentation/xctest/xctestcase/continueafterfailure
  - https://developer.apple.com/documentation/uikit/uiaccessibilityidentification/accessibilityidentifier
depends_on:
  - knowledge.testing.xctest-case-structure-and-assertions
related: []
last_updated: 2026-08-07
```

## Intent

This contract governs driving the app under test end-to-end: launching it with `XCUIApplication`, querying and interacting with `XCUIElement`s, and asserting on UI state -- including why element lookup should key off `accessibilityIdentifier` rather than user-facing text.

## Scope

### Included

- `XCUIApplication()` and `.launch()` to start the app under test
- `continueAfterFailure = false` conventionally set in `setUp()` for UI tests
- `XCUIElement` query-type properties (`.buttons`, `.staticTexts`, `.textFields`, etc.) and subscript lookup
- `accessibilityIdentifier`-based lookup vs. label/title-text-based lookup
- `.tap()`, `.typeText(_:)`, `.exists`, `.waitForExistence(timeout:)`

### Excluded

- `XCUIApplication().performAccessibilityAudit()` -- owned by the `accessibility` domain
- Xcode's UI test recording -- an IDE workflow, not an API surface
- Xcode Test Plans / code coverage -- owned by the `xcode` domain
- `XCTestCase` fundamentals (`setUp`, assertions) beyond `continueAfterFailure` -- see `xctest-case-structure-and-assertions`

## Rules

### Rule 1

Agents MUST construct an `XCUIApplication()` and call `.launch()` to start the app under test before interacting with it. Per Apple's documentation, `XCUIApplication` is "A proxy that can launch, monitor, and terminate a test application," and `launch()` "Launches the application." Note: as of the current documentation, `XCUIApplication`/`XCUIElement` are documented under the **XCUIAutomation** framework, not `XCTest` -- import `XCTest` for the test case itself, but attribute these specific symbols to XCUIAutomation.

### Rule 2

Agents SHOULD set `continueAfterFailure = false` in `setUp()` for UI test classes, so a UI test stops as soon as one step fails rather than cascading into unrelated failures on subsequent, now-meaningless steps. Per Apple's documentation on `continueAfterFailure`: "The default is `true`. Set this property to `false` within a test method to end execution of that method as soon as a failure occurs." This is reasoned synthesis for the UI-testing convention specifically: a failed element lookup mid-flow makes every later assertion in that test unreliable.

### Rule 3

Agents MUST query descendant elements through the typed query properties (`.buttons`, `.staticTexts`, `.textFields`, etc.) rather than untyped traversal, and MUST be aware that the string subscript on the resulting query (e.g. `app.buttons["id"]`) matches against **any** of an element's identifying properties, not only `accessibilityIdentifier`. Per Apple's documentation, the subscript key is "a string to match against any one of each element's identifying properties" (identifier, title, label, value, or placeholderValue) -- so a string that happens to equal a button's title will also match, even if it was never set as that button's identifier.

### Rule 4

Agents MUST set and query by explicit `accessibilityIdentifier` values rather than relying on label or title text matching, because label/title text is user-facing and changes per locale while an identifier is a stable, non-user-facing string set specifically for automation. Per Apple's documentation on `accessibilityIdentifier`: "An identifier can be used to uniquely identify an element in the scripts you write using the UI Automation interfaces. Using an identifier allows you to avoid inappropriately setting or accessing an element's accessibility label." The localization-independence rationale itself is reasoned synthesis (not a literal quote from this page): a hardcoded identifier string is unaffected by the app's active localization, whereas matching on `.buttons["Sign In"]` breaks the moment that string is localized to `.buttons["Se connecter"]`.

### Rule 5

Agents MUST use `.waitForExistence(timeout:)` rather than a bare `.exists` check immediately after an action that changes the UI, since UI updates are asynchronous and a bare `.exists` check races the update. Per Apple's documentation, `exists` "determines if the element exists within the app's current UI hierarchy" at the instant it's read, while `waitForExistence(timeout:)` "Returns `false` if the timeout expires while the element's `exists` property equals `false`" -- i.e. it polls up to the timeout instead of checking once.

## Compliant Example

```swift
import XCTest

final class LoginUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUpWithError() throws {
        continueAfterFailure = false                      // Rule 2
        app.launch()                                       // Rule 1
    }

    func testSuccessfulLogin() throws {
        let usernameField = app.textFields["username_field"]   // Rule 3/4: identifier, not label
        XCTAssertTrue(usernameField.waitForExistence(timeout: 5)) // Rule 5
        usernameField.tap()
        usernameField.typeText("caglar")

        app.buttons["login_button"].tap()                       // Rule 4: identifier lookup

        let welcomeLabel = app.staticTexts["welcome_label"]
        XCTAssertTrue(welcomeLabel.waitForExistence(timeout: 5))  // Rule 5
    }
}
```

## Non-Compliant Example

```swift
import XCTest

final class LeakyLoginUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUpWithError() throws {
        app.launch()                                       // violates Rule 2 -- no continueAfterFailure
    }

    func testSuccessfulLogin() {
        app.textFields["Username"].tap()                   // violates Rule 4 -- matches placeholder
        app.textFields["Username"].typeText("caglar")       // text, breaks under localization
        app.buttons["Log In"].tap()                          // same issue -- matches button title
        XCTAssertTrue(app.staticTexts["Welcome"].exists)     // violates Rule 5 -- races the UI update
    }
}
```
Omits `continueAfterFailure = false` (Rule 2), looks elements up by their placeholder/title text instead of a dedicated `accessibilityIdentifier` (Rule 4), and reads `.exists` immediately instead of polling with `.waitForExistence(timeout:)` (Rule 5), any of which makes the test flaky or locale-fragile.

## Dependencies

Assumes the `XCTestCase` structure from `xctest-case-structure-and-assertions`: a UI test class is still an `XCTestCase` subclass with `test`-prefixed methods and the standard `setUp()` lifecycle.

## References

- [Apple Developer — XCUIApplication](https://developer.apple.com/documentation/xcuiautomation/xcuiapplication)
- [Apple Developer — XCUIElement](https://developer.apple.com/documentation/xcuiautomation/xcuielement)
- [Apple Developer — XCUIElementQuery subscript(_:)](https://developer.apple.com/documentation/xcuiautomation/xcuielementquery/subscript(_:))
- [Apple Developer — continueAfterFailure](https://developer.apple.com/documentation/xctest/xctestcase/continueafterfailure)
- [Apple Developer — accessibilityIdentifier](https://developer.apple.com/documentation/uikit/uiaccessibilityidentification/accessibilityidentifier)
