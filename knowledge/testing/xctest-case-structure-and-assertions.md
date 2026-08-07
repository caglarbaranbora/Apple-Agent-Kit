# XCTest Case Structure and Assertions

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.testing.xctest-case-structure-and-assertions
artifact_type: knowledge
title: XCTest Case Structure and Assertions
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines XCTestCase subclassing with test-prefixed methods, the per-test setUp()/tearDown()/setUpWithError()/tearDownWithError() lifecycle and its documented order, the naming collision with the once-per-class setUp()/tearDown() class methods, the XCTAssert family plus XCTFail, and XCTSkip/XCTSkipIf/XCTSkipUnless for conditional skipping.
domain: Testing
tags:
  - xctest
  - xctestcase
  - assertions
  - setup-teardown
  - skip
references:
  - https://developer.apple.com/documentation/xctest/xctestcase
  - https://developer.apple.com/documentation/xctest/defining-test-cases-and-test-methods
  - https://developer.apple.com/documentation/xctest/set-up-and-tear-down-state-in-your-tests
  - https://developer.apple.com/documentation/xctest/unconditional-test-failures
  - https://developer.apple.com/documentation/xctest/methods-for-skipping-tests
depends_on: []
related: []
last_updated: 2026-08-07
```

## Intent

This contract governs the foundational shape of an XCTest-based test: subclassing `XCTestCase`, naming test methods, the per-test setup/teardown lifecycle and its documented ordering, the `XCTAssert*` assertion family, and skipping a test conditionally. It is the vocabulary every other XCTest/XCUITest Knowledge Contract in this domain assumes.

## Scope

### Included

- `XCTestCase` subclassing and the `test`-prefix naming rule for test methods
- Instance-level `setUp()`/`setUpWithError()`/`tearDown()`/`tearDownWithError()`, called once per **test method**, and their documented call order
- The naming collision with `class func setUp()`/`tearDown()`, called once per **test class**
- `XCTAssertEqual`, `XCTAssertTrue`/`XCTAssertFalse`, `XCTAssertNil`/`XCTAssertNotNil`, `XCTAssertThrowsError`/`XCTAssertNoThrow`, `XCTFail(_:)`
- `XCTSkip`, `XCTSkipIf(_:_:)`, `XCTSkipUnless(_:_:)`

### Excluded

- The Swift Testing framework's `@Test`/`#expect`/`#require` — see `swift-testing-fundamentals`
- `async`/`throws` test methods and parameterization — see `parameterized-and-async-tests`
- `XCUIApplication`/`XCUIElement` UI testing — see `ui-testing-with-xcuiapplication`
- `XCTestExpectation` for callback-based async code — see `expectations-for-asynchronous-code`
- Performance testing (`measure { }`, `XCTMetric`) — out of scope for v1 (see reference doc)

## Rules

### Rule 1

Agents MUST subclass `XCTestCase` and name each test method as an instance method with no parameters, no return value, and a name beginning with lowercase `test`. Per Apple's documentation: "A test method is an instance method on an `XCTestCase` subclass, with no parameters, no return value, and a name that begins with the lowercase word *test*."

### Rule 2

Agents MUST override the **instance methods** `setUp()`/`setUpWithError()`/`tearDown()`/`tearDownWithError()` for per-test state, and MUST NOT confuse them with the identically-named `class func setUp()`/`tearDown()`, which run only once for the whole test class. Per Apple's documentation: "XCTest calls the `XCTestCase` `setUp()` class method first... before its first test method is called," whereas "XCTest runs the setup methods once before each test method starts: `setUp() async throws` first, then `setUpWithError()`, then `setUp()`" — and symmetrically, teardown runs "`tearDown()` first, then `tearDownWithError()`, then `tearDown() async throws`" after each test method.

### Rule 3

Agents SHOULD prefer `setUpWithError()`/`tearDownWithError()` over the non-throwing `setUp()`/`tearDown()` when fixture setup or cleanup can fail, since only the throwing variants let that failure mark the test failed (or skipped, via `XCTSkip`) without a manual `XCTFail`. This is reasoned synthesis from the documented per-test call order in Rule 2, which places the throwing variants in the same per-test lifecycle slot as the non-throwing ones.

### Rule 4

Agents MUST use `XCTAssertEqual` only to compare two non-optional `Equatable` values, and MUST choose the assertion that names the actual condition being checked (`XCTAssertTrue`/`XCTAssertFalse` for booleans, `XCTAssertNil`/`XCTAssertNotNil` for optionality, `XCTAssertThrowsError`/`XCTAssertNoThrow` for throwing expressions) rather than reconstructing that check inside `XCTAssertTrue`. Per Apple's documentation, `XCTAssertEqual` is used "to compare two non-optional values of the same type," and `XCTFail(_:)` "generates a failure immediately and unconditionally" for cases with no matching assertion.

### Rule 5

Agents MUST use `XCTSkipIf(_:_:)`/`XCTSkipUnless(_:_:)` for a Boolean skip condition, and MUST `throw XCTSkip(_:)` for any other circumstance requiring a skip. Per Apple's documentation: "Use `XCTSkipIf()` or `XCTSkipUnless()` when you have a Boolean condition that you can use to evaluate when to skip tests. In Swift, throw an `XCTSkip` error when you have other circumstances that result in skipped tests."

## Compliant Example

```swift
import XCTest

final class AccountBalanceTests: XCTestCase {
    private var account: Account!

    override func setUpWithError() throws {          // Rule 2/3: per-test, throwing
        account = try Account(openingBalance: 100)
    }

    override func tearDownWithError() throws {        // Rule 2/3: per-test, throwing
        account = nil
    }

    func testDepositIncreasesBalance() throws {       // Rule 1: test-prefixed
        try XCTSkipUnless(FeatureFlags.deposits, "Deposits disabled")   // Rule 5
        account.deposit(50)
        XCTAssertEqual(account.balance, 150)          // Rule 4: Equatable compare
    }

    func testWithdrawingMoreThanBalanceThrows() {
        XCTAssertThrowsError(try account.withdraw(1000)) { error in    // Rule 4
            XCTAssertEqual(error as? AccountError, .insufficientFunds)
        }
    }
}
```

## Non-Compliant Example

```swift
import XCTest

final class LeakyAccountTests: XCTestCase {
    var account: Account!

    override class func setUp() {                    // violates Rule 2 -- class method
        account = Account(openingBalance: 100)        // runs once for the whole class,
    }                                                  // not before each test

    func checkDeposit() {                             // violates Rule 1 -- no "test" prefix,
        account.deposit(50)                           // XCTest never runs this method
        XCTAssertTrue(account.balance == 150)          // violates Rule 4 -- should be XCTAssertEqual
    }
}
```
Overrides the class-level `setUp()` instead of the per-test instance method (Rule 2), so state leaks across tests; names the method `checkDeposit` without the `test` prefix so XCTest never runs it (Rule 1); and reconstructs an equality check inside `XCTAssertTrue` instead of using `XCTAssertEqual` (Rule 4).

## Dependencies

None within this domain — this is the foundational contract every other XCTest/XCUITest Knowledge Contract assumes when referring to "a test case" or "an assertion."

## References

- [Apple Developer — XCTestCase](https://developer.apple.com/documentation/xctest/xctestcase)
- [Apple Developer — Defining Test Cases and Test Methods](https://developer.apple.com/documentation/xctest/defining-test-cases-and-test-methods)
- [Apple Developer — Set Up and Tear Down State in Your Tests](https://developer.apple.com/documentation/xctest/set-up-and-tear-down-state-in-your-tests)
- [Apple Developer — Unconditional Test Failures](https://developer.apple.com/documentation/xctest/unconditional-test-failures)
- [Apple Developer — Methods for Skipping Tests](https://developer.apple.com/documentation/xctest/methods-for-skipping-tests)
