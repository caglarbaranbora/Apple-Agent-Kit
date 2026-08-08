# Parameterized and Async Tests

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.testing.parameterized-and-async-tests
artifact_type: knowledge
title: Parameterized and Async Tests
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines Swift Testing's @Test(arguments:) parameterization -- single-collection (once per element), two-bare-collection (Cartesian product), and zip-paired overloads -- plus native async/throws-capable test functions in both Swift Testing and XCTest, with no XCTestExpectation needed for pure async/await code.
domain: Testing
tags:
  - swift-testing
  - parameterized-tests
  - arguments
  - async
  - xctest
references:
  - https://developer.apple.com/documentation/testing/parameterizedtesting
  - https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a
  - https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)
  - https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok
  - https://developer.apple.com/documentation/testing/definingtests
  - https://developer.apple.com/documentation/xctest/asynchronous-tests-and-expectations
depends_on:
  - knowledge.testing.swift-testing-fundamentals
  - knowledge.testing.xctest-case-structure-and-assertions
related:
  - knowledge.testing.expectations-for-asynchronous-code
last_updated: 2026-08-08
```

## Intent

This contract governs Swift Testing's `@Test(arguments:)` parameterization overloads -- which of them pairs inputs and which produces every combination -- and the native `async`/`throws` support both Swift Testing and XCTest offer for test functions, without any `XCTestExpectation` involved.

## Scope

### Included

- `@Test(arguments:)` over a single collection: one invocation per element
- `@Test(arguments:_:)` over two bare collections: one invocation per **combination** (Cartesian product)
- `@Test(arguments: zip(a, b))`: one invocation per **paired** element (via `Zip2Sequence`)
- `async`/`async throws` test functions in Swift Testing and in `XCTestCase`

### Excluded

- `XCTestExpectation` for callback-based code with no `async`/`await` entry point -- see `expectations-for-asynchronous-code`
- `CustomTestArgumentEncodable` and custom argument descriptions -- out of scope for v1

## Rules

### Rule 1

Agents MUST expect `@Test(arguments:)` over a single collection to invoke the test function once per element in that collection, evaluated lazily. Per Apple's documentation: "During testing, the testing library calls the associated test function once for each element in `collection`."

### Rule 2

Agents MUST expect passing **two separate collections** to `@Test(_:_:arguments:_:)` to invoke the test once for **every combination** of their elements (a Cartesian product), NOT paired one-to-one -- this is the most common point of confusion in this API. Per Apple's documentation, with five `Food` cases and 100 counts, "this test function will, when run, be invoked 500 times (5 x 100) with every possible combination of food and order size. These combinations are referred to as the collections' Cartesian product."

### Rule 3

Agents MUST wrap two collections in `zip(_:_:)` and pass the single resulting sequence to `@Test(arguments:)` when pairing, not combining, is intended. Per Apple's documentation: "The zipped sequence will be 'destructured' into two arguments automatically, then passed to the test function for evaluation" -- producing one invocation per pair (5 invocations for two 5-element collections), not 25.

### Rule 4

Agents MUST mark a Swift Testing `@Test` function `async` and/or `throws` directly when it needs to await asynchronous work or propagate an error, with no additional ceremony required. Per Apple's documentation, a test function may be declared `@Test @MainActor func foodTruckExists() async throws { ... }`, and the testing library integrates "seamlessly with Swift concurrency."

### Rule 5

Agents MUST mark an `XCTestCase` test method `async throws` to test `async`/`await` code directly, and MUST NOT introduce an `XCTestExpectation` for that case -- expectations are reserved for code with no `async`/`await` entry point (see `expectations-for-asynchronous-code`). Per Apple's documentation: "To test Swift code that uses `async` and `await` for concurrency, mark your test method `async` or `async throws`. `XCTest` executes your test method asynchronously so that your test waits until `async` calls complete."

## Compliant Example

```swift
import Testing
import XCTest

@Test(arguments: Food.allCases)                        // Rule 1: once per element
func eachFoodHasAPrice(_ food: Food) {
    #expect(food.price > 0)
}

@Test(arguments: zip(Food.allCases, [8.50, 6.00, 9.25])) // Rule 3: paired, not combined
func priceMatchesMenu(_ food: Food, expected: Double) {
    #expect(food.price == expected)
}

@Test
func downloadCompletes() async throws {                 // Rule 4: native async throws
    let data = try await MenuService.fetch()
    #expect(!data.isEmpty)
}

final class MenuServiceXCTests: XCTestCase {
    func testDownloadCompletes() async throws {          // Rule 5: async throws, no expectation
        let data = try await MenuService.fetch()
        XCTAssertFalse(data.isEmpty)
    }
}
```

## Non-Compliant Example

```swift
import Testing

@Test(arguments: Food.allCases, [8.50, 6.00, 9.25])      // violates Rule 2/3 -- author intended
func priceMatchesMenu(_ food: Food, expected: Double) {   // pairing but passed two bare collections;
    #expect(food.price == expected)                       // this runs 3x3=9 times, mismatching
}                                                            // most food/price combinations
```
Passes two bare collections expecting them to pair up, but this overload produces every combination (Rule 2) -- the fix is `zip(Food.allCases, [8.50, 6.00, 9.25])` as a single argument (Rule 3).

## Dependencies

Assumes the `@Test` vocabulary from `swift-testing-fundamentals` and the `XCTestCase` vocabulary from `xctest-case-structure-and-assertions`; this contract only adds parameterization and concurrency to those foundations.

## References

- [Apple Developer — Implementing Parameterized Tests](https://developer.apple.com/documentation/testing/parameterizedtesting)
- [Apple Developer — Test(_:_:arguments:_:)](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:))
- [Apple Developer — Test(_:_:arguments:) (zipped overload)](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok)
- [Apple Developer — Defining Test Functions](https://developer.apple.com/documentation/testing/definingtests)
- [Apple Developer — Asynchronous Tests and Expectations](https://developer.apple.com/documentation/xctest/asynchronous-tests-and-expectations)
