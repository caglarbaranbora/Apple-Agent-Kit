# Testing

Status: Draft
Version: 0.1.0

## Source

https://developer.apple.com/documentation/xctest
https://developer.apple.com/documentation/xctest/xctestcase
https://developer.apple.com/documentation/xctest/defining-test-cases-and-test-methods
https://developer.apple.com/documentation/xctest/set-up-and-tear-down-state-in-your-tests
https://developer.apple.com/documentation/xctest/xctassertequal(_:_:_:file:line:)
https://developer.apple.com/documentation/xctest/boolean-assertions
https://developer.apple.com/documentation/xctest/nil-and-non-nil-assertions
https://developer.apple.com/documentation/xctest/error-assertions
https://developer.apple.com/documentation/xctest/unconditional-test-failures
https://developer.apple.com/documentation/xctest/methods-for-skipping-tests
https://developer.apple.com/documentation/xctest/xctskip
https://developer.apple.com/documentation/testing
https://developer.apple.com/documentation/testing/definingtests
https://developer.apple.com/documentation/testing/expectations
https://developer.apple.com/documentation/testing/suite(_:_:)
https://developer.apple.com/documentation/testing/tag
https://developer.apple.com/documentation/testing/parameterizedtesting
https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)
https://developer.apple.com/documentation/xctest/asynchronous-tests-and-expectations
https://developer.apple.com/documentation/xctest/xctestexpectation
https://developer.apple.com/documentation/xctest/xctestcase/fulfillment(of:timeout:enforceorder:)
https://developer.apple.com/documentation/xctest/xctestcase/wait(for:timeout:)
https://developer.apple.com/documentation/xcuiautomation
https://developer.apple.com/documentation/xcuiautomation/xcuiapplication
https://developer.apple.com/documentation/xcuiautomation/xcuielement
https://developer.apple.com/documentation/xcuiautomation/xcuielementquery/subscript(_:)
https://developer.apple.com/documentation/xctest/xctestcase/continueafterfailure
https://developer.apple.com/documentation/uikit/uiaccessibilityidentification/accessibilityidentifier

## Purpose

Reference index for Apple's Apple-platform testing documentation, scoped to this domain's v1: `XCTestCase` subclassing with `test`-prefixed methods, the per-test `setUp()`/`tearDown()`/`setUpWithError()`/`tearDownWithError()` lifecycle (distinct from the same-named class-level, once-per-class `setUp()`/`tearDown()` overrides), the `XCTAssert*` family plus `XCTFail`, and `XCTSkip`/`XCTSkipIf`/`XCTSkipUnless`; the newer Swift Testing framework's `@Test`/`#expect`/`#require`/`@Suite`/`Tag` vocabulary as a non-inheriting alternative to `XCTestCase`; parameterized tests via `@Test(arguments:)` (single-collection, two-collection Cartesian product, and `zip`-paired overloads) and native `async throws` test functions in both frameworks; UI testing via `XCUIApplication`/`XCUIElement` (now documented under the XCUIAutomation framework, not XCTest) with identifier-based element lookup; and `XCTestExpectation` for callback-based asynchronous code that has no `async`/`await` entry point to await directly.

Out of scope for v1: performance testing (`measure { }`, `XCTMetric`, `XCTClockMetric`); Xcode Test Plans and code coverage configuration (owned by the existing `xcode` domain); third-party snapshot testing; Xcode's UI test recording (an IDE workflow, not an API); mocking/dependency-injection patterns and test doubles (general technique, not Apple-API-specific); and `XCUIApplication().performAccessibilityAudit()` (owned by the existing `accessibility` domain).

## Primary Topics

- `XCTestCase` subclassing, `test`-prefixed methods, per-test `setUp()`/`tearDown()`/`setUpWithError()`/`tearDownWithError()` vs. the once-per-class class-method overloads of the same names
- `XCTAssertEqual`, `XCTAssertTrue`/`XCTAssertFalse`, `XCTAssertNil`/`XCTAssertNotNil`, `XCTAssertThrowsError`/`XCTAssertNoThrow`, `XCTFail`, and `XCTSkip`/`XCTSkipIf`/`XCTSkipUnless`
- Swift Testing's `@Test`, `#expect`, `#require`, `@Suite`, and `Tag`/`.tags(_:)`
- `@Test(arguments:)` single-collection, two-collection Cartesian-product, and `zip`-paired parameterization; `async throws` test functions in Swift Testing and XCTest
- `XCUIApplication()`/`.launch()`, `continueAfterFailure`, `XCUIElement` query types and interaction/existence APIs, identifier-based lookup
- `XCTestExpectation`, `expectation(description:)`, `.fulfill()`, and `await fulfillment(of:timeout:)` for callback-based async code

## Used By

- knowledge/testing/xctest-case-structure-and-assertions.md ([[knowledge/testing/xctest-case-structure-and-assertions]])
- knowledge/testing/swift-testing-fundamentals.md ([[knowledge/testing/swift-testing-fundamentals]])
- knowledge/testing/parameterized-and-async-tests.md ([[knowledge/testing/parameterized-and-async-tests]])
- knowledge/testing/ui-testing-with-xcuiapplication.md ([[knowledge/testing/ui-testing-with-xcuiapplication]])
- knowledge/testing/expectations-for-asynchronous-code.md ([[knowledge/testing/expectations-for-asynchronous-code]])
- skills/testing/SKILL.md ([[skills/testing/SKILL]])
