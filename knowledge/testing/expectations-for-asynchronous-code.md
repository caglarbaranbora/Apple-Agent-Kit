# Expectations for Asynchronous Code

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.testing.expectations-for-asynchronous-code
type: knowledge
title: Expectations for Asynchronous Code
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines XCTestExpectation for testing callback-based (non-async/await) asynchronous code -- expectation(description:), fulfilling it with .fulfill() inside the completion handler under test, and waiting via the concurrency-safe await fulfillment(of:timeout:) in preference to the older synchronous wait(for:timeout:) -- scoped to APIs with no async/await entry point.
domain: Testing
tags:
  - xctestexpectation
  - fulfillment
  - completion-handler
  - async
references:
  - https://developer.apple.com/documentation/xctest/xctestexpectation
  - https://developer.apple.com/documentation/xctest/asynchronous-tests-and-expectations
  - https://developer.apple.com/documentation/xctest/xctestcase/fulfillment(of:timeout:enforceorder:)
  - https://developer.apple.com/documentation/xctest/xctestcase/wait(for:timeout:)
depends_on:
  - knowledge.testing.xctest-case-structure-and-assertions
related:
  - knowledge.testing.parameterized-and-async-tests
updated: 2026-08-07
```

## Intent

This contract governs testing asynchronous code that has **no `async`/`await` entry point to await directly** -- a delegate callback, a completion-handler-based API, or Objective-C code -- via `XCTestExpectation`. For code that already exposes `async`/`await`, use the native `async throws` test methods covered in `parameterized-and-async-tests` instead; do not wrap an awaitable call in an expectation.

## Scope

### Included

- `XCTestExpectation` and creating one with `expectation(description:)`
- Calling `.fulfill()` inside the completion handler under test
- Waiting with `await fulfillment(of:timeout:)`, preferred over the older `wait(for:timeout:)`

### Excluded

- `async`/`await`-native test methods -- see `parameterized-and-async-tests`
- `XCTNSNotificationExpectation`, `XCTKeyPathExpectation`, and other specialized expectation subclasses -- out of scope for v1
- Combine `Future`/`Promise`-based waiting beyond a one-line mention

## Rules

### Rule 1

Agents MUST scope `XCTestExpectation` to code with no `async`/`await` entry point -- a delegate method, a completion-handler closure, or Objective-C code -- and MUST NOT wrap an `async` function's `await` call in an expectation. Per Apple's documentation, XCTest offers expectations for "asynchronous blocks in dispatch queues, delegate methods, asynchronous callbacks, closures, or completion blocks," distinct from the `async`/`await` case covered by native `async throws` test methods (see `parameterized-and-async-tests`).

### Rule 2

Agents MUST create an expectation with `expectation(description:)` before starting the asynchronous work, and MUST call `.fulfill()` on it inside the completion handler once the awaited condition is satisfied. Per Apple's documentation: "If the test doesn't execute the `fulfill()` method before the wait statement's timeout expires, `XCTest` records a test failure."

### Rule 3

Agents MUST wait on the expectation with `await fulfillment(of:timeout:)` rather than the older synchronous `wait(for:timeout:)`, since it is the documented concurrency-safe alternative. Per Apple's documentation on `XCTestCase.fulfillment(of:timeout:enforceOrder:)`: "Use this concurrency-safe alternative to `wait(for:timeout:enforceOrder:)` in your Swift code." The method's `timeout`/`enforceOrder` parameters both have defaults, so `await fulfillment(of: [expectation], timeout: 5)` is a valid call.

### Rule 4

Agents MUST treat `wait(for:timeout:)` as guided-away-from rather than deprecated: it remains valid, particularly for Objective-C interop, but Apple's own reference steers Swift callers elsewhere. Per Apple's documentation on `wait(for:timeout:)`: "Use `XCTWaiter.fulfillment(of:timeout:enforceOrder:)` in Swift code requiring concurrency." Do not report `wait(for:timeout:)` as removed or unavailable -- only as superseded guidance for new Swift code.

### Rule 5

Agents MUST place all assertions on the result inside the completion handler (or immediately after the `await fulfillment(of:timeout:)` call returns), never before it, since the awaited value/state does not exist until the callback fires. This is reasoned synthesis from Rule 2: `.fulfill()` marks completion, so any assertion that must see the callback's result can only run at or after that point.

## Compliant Example

```swift
import XCTest

final class FileManagerTests: XCTestCase {
    func testOpenFileAsync() async throws {
        let expectation = expectation(description: "Open a file asynchronously") // Rule 2
        let fileManager = ExampleFileManager()
        var loadedFile: File?

        fileManager.openFileAsync(with: "example.txt") { file, error in
            loadedFile = file
            XCTAssertNil(error)                              // Rule 5: assert inside the callback
            expectation.fulfill()                             // Rule 2
        }

        await fulfillment(of: [expectation], timeout: 5)      // Rule 3: concurrency-safe wait
        XCTAssertNotNil(loadedFile)                            // Rule 5: assert after fulfillment
    }
}
```

## Non-Compliant Example

```swift
import XCTest

final class LeakyFileManagerTests: XCTestCase {
    func testOpenFileAsync() {
        let expectation = expectation(description: "Open a file asynchronously")
        let fileManager = ExampleFileManager()
        var loadedFile: File?

        fileManager.openFileAsync(with: "example.txt") { file, error in
            loadedFile = file
            expectation.fulfill()
        }

        XCTAssertNotNil(loadedFile)                            // violates Rule 5 -- runs before the
        wait(for: [expectation], timeout: 5)                    // callback fires; loadedFile is
    }                                                             // still nil at this point
}
```
Asserts on `loadedFile` before the asynchronous callback has run, since the assertion is placed above the `wait(for:timeout:)` call instead of after it completes (Rule 5) -- the assertion always fails or passes for the wrong reason.

## Dependencies

Assumes the `XCTestCase` structure from `xctest-case-structure-and-assertions`. Cross-reference `parameterized-and-async-tests` before reaching for an expectation: if the API under test already exposes `async`/`await`, no `XCTestExpectation` is needed.

## References

- [Apple Developer — XCTestExpectation](https://developer.apple.com/documentation/xctest/xctestexpectation)
- [Apple Developer — Asynchronous Tests and Expectations](https://developer.apple.com/documentation/xctest/asynchronous-tests-and-expectations)
- [Apple Developer — fulfillment(of:timeout:enforceOrder:)](https://developer.apple.com/documentation/xctest/xctestcase/fulfillment(of:timeout:enforceorder:))
- [Apple Developer — wait(for:timeout:)](https://developer.apple.com/documentation/xctest/xctestcase/wait(for:timeout:))
