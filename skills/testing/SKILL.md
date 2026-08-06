---
name: testing
description: Route Apple-platform testing tasks to the correct Knowledge Contracts -- XCTestCase subclassing with test-prefixed methods and the per-test setUp()/setUpWithError()/tearDown()/tearDownWithError() lifecycle plus the XCTAssert family and XCTSkip/XCTSkipIf/XCTSkipUnless; the Swift Testing framework's @Test/#expect/#require/@Suite/Tag vocabulary; @Test(arguments:) parameterization (single-collection, two-collection Cartesian product, zip-paired) and async throws test functions in both frameworks; XCUIApplication/XCUIElement UI testing with identifier-based lookup; and XCTestExpectation for callback-based async code with no async/await entry point. Use when writing class Foo: XCTestCase, func test..., override func setUp()/setUpWithError()/tearDown()/tearDownWithError(), XCTAssertEqual/XCTAssertTrue/XCTAssertNil/XCTAssertThrowsError, XCTSkip/XCTSkipIf/XCTSkipUnless, import Testing, @Test, @Suite, #expect(_:), #require(_:), .tags(_:), @Test(arguments:), zip(...) inside @Test(arguments:), async throws test methods, XCUIApplication(), .launch(), continueAfterFailure, app.buttons["..."], .tap(), .typeText(_:), .waitForExistence(timeout:), XCTestExpectation, expectation(description:), .fulfill(), or await fulfillment(of:timeout:). v1 covers only XCTest, Swift Testing, and XCUITest as described -- no performance testing (measure { }, XCTMetric, XCTClockMetric), no Xcode Test Plans or code coverage configuration, no third-party snapshot testing, no UI test recording, no mocking/dependency-injection/test-double patterns, and no performAccessibilityAudit(). Triggers on XCTest, XCTestCase, XCTAssert, XCTSkip, Swift Testing, @Test, #expect, #require, @Suite, Tag, parameterized test, XCUITest, XCUIApplication, XCUIElement, accessibilityIdentifier, XCTestExpectation, fulfillment.
id: skill.testing.foundations
title: Testing — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Testing
routes: [knowledge.testing.xctest-case-structure-and-assertions, knowledge.testing.swift-testing-fundamentals, knowledge.testing.parameterized-and-async-tests, knowledge.testing.ui-testing-with-xcuiapplication, knowledge.testing.expectations-for-asynchronous-code]
related: []
last_updated: 2026-08-07
---

# Testing — Foundations Skill

## Purpose

Route Apple-platform testing implementation tasks to the minimum required
Knowledge Contracts. v1 scope is a curated subset of XCTest (case
structure, assertions, skipping), the newer Swift Testing framework
(`@Test`/`#expect`/`#require`/`@Suite`/`Tag`), parameterized and
`async`/`throws` test functions in both frameworks, XCUITest
(`XCUIApplication`/`XCUIElement`), and `XCTestExpectation` for
callback-based asynchronous code -- not performance testing, Test Plans,
snapshot testing, UI test recording, mocking/DI patterns, or accessibility
audits.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/testing/.

-   Subclassing `XCTestCase`; naming a `test`-prefixed method; overriding
    `setUp()`/`setUpWithError()`/`tearDown()`/`tearDownWithError()`; using
    `XCTAssertEqual`/`XCTAssertTrue`/`XCTAssertNil`/`XCTAssertThrowsError`/
    `XCTFail`; or skipping with `XCTSkip`/`XCTSkipIf`/`XCTSkipUnless` ->
    xctest-case-structure-and-assertions.md
-   Writing `import Testing`; declaring `@Test`; choosing between
    `#expect(_:)` and `#require(_:)`; grouping with `@Suite`; or tagging
    with `Tag`/`.tags(_:)` -> swift-testing-fundamentals.md
-   Parameterizing a `@Test` with `arguments:` over one collection, two
    collections, or `zip(...)`; or writing an `async`/`async throws` test
    function in either framework -> parameterized-and-async-tests.md
-   Launching the app under test with `XCUIApplication()`/`.launch()`;
    setting `continueAfterFailure`; querying `XCUIElement`s by
    `accessibilityIdentifier`; or asserting with `.exists`/
    `.waitForExistence(timeout:)` -> ui-testing-with-xcuiapplication.md
-   Testing a delegate callback or completion-handler API with no
    `async`/`await` entry point via `XCTestExpectation`,
    `expectation(description:)`, `.fulfill()`, or
    `await fulfillment(of:timeout:)` -> expectations-for-asynchronous-code.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/testing/ -- do not guess or fall back to general knowledge.
Performance testing (`measure { }`, `XCTMetric`, `XCTClockMetric`) is out
of scope entirely -- do not fabricate performance-testing guidance. Xcode
Test Plans (`.xctestplan`) and code coverage configuration are owned by
the `xcode` domain -- report the boundary rather than answer from this
skill. Snapshot testing (e.g. swift-snapshot-testing) is a third-party
pattern, not an Apple-documented API -- out of scope entirely. Xcode's UI
test recording is an IDE workflow, not an API surface -- out of scope
entirely. Mocking, dependency injection, and test-double patterns are
general software-engineering technique, not Apple-API-specific -- out of
scope entirely. `XCUIApplication().performAccessibilityAudit()` is owned
by the `accessibility` domain -- report the boundary rather than build it
here.
