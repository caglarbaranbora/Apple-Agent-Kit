# Swift Testing Fundamentals

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.testing.swift-testing-fundamentals
artifact_type: knowledge
title: Swift Testing Fundamentals
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the Swift Testing framework's core vocabulary -- the @Test macro replacing XCTestCase subclassing, #expect(_:) as the continue-on-failure assertion macro, #require(_:) as the throw-and-halt assertion macro used for safely unwrapping optionals, the optional @Suite grouping macro, and tagging tests with Tag via .tags(_:).
domain: Testing
tags:
  - swift-testing
  - test-macro
  - expect
  - require
  - suite
  - tag
references:
  - https://developer.apple.com/documentation/testing
  - https://developer.apple.com/documentation/testing/definingtests
  - https://developer.apple.com/documentation/testing/expectations
  - https://developer.apple.com/documentation/testing/suite(_:_:)
  - https://developer.apple.com/documentation/testing/tag
depends_on: []
related:
  - knowledge.testing.xctest-case-structure-and-assertions
last_updated: 2026-08-07
```

## Intent

This contract governs the newer Swift Testing framework's core declaration and assertion vocabulary -- `@Test`, `#expect`, `#require`, `@Suite`, and `Tag` -- as a distinct alternative to the `XCTestCase` vocabulary in `xctest-case-structure-and-assertions`, not a superset of it.

## Scope

### Included

- `import Testing` and the `@Test` macro on free functions or methods on any struct/class/actor
- `#expect(_:)` as the general-purpose, continue-on-failure assertion macro
- `#require(_:)` as the halt-on-failure assertion macro, including optional-unwrapping use
- `@Suite` as an optional grouping macro for related `@Test` functions
- `Tag` and `.tags(_:)` for categorizing tests

### Excluded

- `@Test(arguments:)` parameterization and `async`/`throws` test functions -- see `parameterized-and-async-tests`
- `XCTestCase`, `XCTAssert*`, `setUp`/`tearDown` -- see `xctest-case-structure-and-assertions`
- Migrating an existing XCTest suite to Swift Testing -- out of scope for v1

## Rules

### Rule 1

Agents MUST declare a Swift Testing test as a function annotated `@Test`, at file scope or as a method on any struct/class/actor, and MUST NOT subclass anything or conform to any protocol to do so. Per Apple's documentation: "To declare a test function, write a Swift function declaration that doesn't take any arguments, then prefix its name with the `@Test` attribute," and "This test function can be present at file scope or within a type."

### Rule 2

Agents MUST use `#expect(_:)` as the default assertion and MUST expect it to continue the test after a failed expectation, permitting multiple recorded failures per test -- the same continue-on-failure behavior as XCTest's `XCTAssert*` family in `xctest-case-structure-and-assertions`, expressed as a macro instead of a function. Per Apple's documentation: "Your test keeps running after `#expect` fails."

### Rule 3

Agents MUST use `#require(_:)` instead of `#expect(_:)` whenever the test cannot meaningfully continue after a failed check -- most commonly to unwrap an optional -- since `#require` throws and stops the test immediately. Per Apple's documentation: "`#require` throws an instance of `ExpectationFailedError` when your code fails to satisfy the requirement," demonstrated by `let customer = try #require(Customer(id: 123))` where "the test runner doesn't reach [the next] line if the customer is nil."

### Rule 4

Agents MAY omit `@Suite` on a type that contains `@Test` methods, since grouping is implicit, and MUST apply `@Suite` only to a type's primary declaration, never to an extension. Per Apple's documentation: "The use of the `@Suite` attribute is optional. Types are recognized as test suites even if they do not have the `@Suite` attribute applied to them," and "When adding test functions to a type extension, do not use the `@Suite` attribute."

### Rule 5

Agents SHOULD tag related tests with `Tag` values via the `.tags(_:)` trait when tests need to be filtered or organized across suite boundaries (e.g. by feature area or flakiness), rather than encoding that grouping only in file/type structure. Per Apple's documentation, `Tag` is "a tag that can be applied to a test," applied with `static func tags(_ tags: Tag...) -> Self`.

## Compliant Example

```swift
import Testing

extension Tag {
    @Tag static var networking: Self
}

@Suite("Food Truck Ordering")                         // Rule 4: optional, primary type only
struct OrderingTests {
    @Test("Order total reflects item price")           // Rule 1: no inheritance required
    func orderTotalReflectsPrice() throws {
        let order = try #require(Order(items: [.burger]))   // Rule 3: unwrap-or-halt
        #expect(order.total == 8.50)                    // Rule 2: continues even if this fails
        #expect(order.items.count == 1)
    }

    @Test("Refund requires network", .tags(.networking)) // Rule 5: categorize with a Tag
    func refundRequiresNetwork() async throws {
        #expect(try await RefundService.isReachable())
    }
}
```

## Non-Compliant Example

```swift
import Testing

@Suite("Food Truck Ordering")
extension OrderingTests {                              // violates Rule 4 -- @Suite on an extension
    @Test func orderTotalReflectsPrice() {
        let order = Order(items: [.burger])!            // violates Rule 3 -- force-unwrap instead
        #expect(order.total == 8.50)                    // of #require; crashes rather than
    }                                                     // failing the test cleanly
}
```
Applies `@Suite` to a type extension rather than the type's primary declaration (Rule 4), and force-unwraps an optional instead of using `#require(_:)`, so a `nil` result crashes the test process instead of reporting a clean, diagnosable failure (Rule 3).

## Dependencies

None within this domain -- Swift Testing's vocabulary is independent of `XCTestCase`. See `xctest-case-structure-and-assertions` only for contrast (both frameworks continue by default on their primary assertion, `#expect`/`XCTAssert*`).

## References

- [Apple Developer — Swift Testing](https://developer.apple.com/documentation/testing)
- [Apple Developer — Defining Test Functions](https://developer.apple.com/documentation/testing/definingtests)
- [Apple Developer — Expectations and Confirmations](https://developer.apple.com/documentation/testing/expectations)
- [Apple Developer — Suite(_:_:)](https://developer.apple.com/documentation/testing/suite(_:_:))
- [Apple Developer — Tag](https://developer.apple.com/documentation/testing/tag)
