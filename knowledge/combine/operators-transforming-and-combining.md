# Operators — Transforming and Combining

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.combine.operators-transforming-and-combining
artifact_type: knowledge
title: Operators — Transforming and Combining
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the transforming operators map, filter, and removeDuplicates, the time-based debounce(for:scheduler:options:), and the multi-publisher combining operators combineLatest, merge, and zip -- what each does and the shape of its output, including the tuple-vs-flat-stream distinction between combineLatest/zip and merge.
domain: Combine
tags:
  - combine
  - operators
  - map
  - filter
  - combinelatest
  - merge
  - zip
references:
  - https://developer.apple.com/documentation/combine/publisher/map(_:)-99evh
  - https://developer.apple.com/documentation/combine/publisher/filter(_:)
  - https://developer.apple.com/documentation/combine/publisher/removeduplicates()
  - https://developer.apple.com/documentation/combine/publisher/debounce(for:scheduler:options:)
  - https://developer.apple.com/documentation/combine/publisher/combinelatest(_:)
  - https://developer.apple.com/documentation/combine/publishers/merge
  - https://developer.apple.com/documentation/combine/publisher/zip(_:)
depends_on:
  - knowledge.combine.publishers-and-subscribers
related: []
last_updated: 2026-08-08
```

## Intent

This contract governs choosing and composing Combine's core transforming operators (`map`, `filter`, `removeDuplicates`, `debounce`) and combining operators (`combineLatest`, `merge`, `zip`), including the output shape each produces. It assumes the `Publisher` vocabulary from `publishers-and-subscribers`.

## Scope

### Included

- `map(_:)` element-to-element transform
- `filter(_:)` predicate-based republishing
- `removeDuplicates()` (`Output: Equatable`) two-element-memory deduplication
- `debounce(for:scheduler:options:)` time-based coalescing
- `combineLatest(_:)`, `merge(with:)`, `zip(_:)` and their output-shape differences

### Excluded

- `tryMap`, `flatMap`, `compactMap`, `throttle` — out of scope for v1
- `removeDuplicates(by:)` predicate overload beyond a one-line mention
- Custom `Scheduler` implementations — only using an existing one (e.g. `RunLoop.main`) is in scope
- Subjects that feed these operators — see `subjects`

## Rules

### Rule 1

Agents MUST use `map(_:)` for a non-throwing, one-to-one transform of each element, and MUST reach for `tryMap(_:)` (out of v1 scope) instead if the transform closure can throw. Per Apple's documentation, `map(_:)` "Transforms all elements from the upstream publisher with a provided closure," and "If your closure can throw an error, use Combine's `tryMap(_:)` operator instead."

### Rule 2

Agents MUST use `filter(_:)` only to republish a subset of elements unchanged, and MUST use `removeDuplicates()` only when `Output` conforms to `Equatable`, being aware it compares solely the current element against the immediately preceding one. Per Apple's documentation, `filter(_:)` "uses a closure to test each element to determine whether to republish" it, and `removeDuplicates()` "has a two-element memory: it uses the current and previously published elements as the basis for its comparison."

### Rule 3

Agents MUST supply an explicit `scheduler:` (e.g. `RunLoop.main`, a `DispatchQueue`) to `debounce(for:scheduler:options:)`, and MUST understand it drops elements that arrive faster than `dueTime` rather than merely delaying them. Per Apple's documentation: "The `debounce` operator controls the number of values and time between delivery of values from the upstream publisher... Elements arriving faster than the debounce interval... are discarded, while elements arriving slower are passed through."

### Rule 4

Agents MUST expect `combineLatest(_:)` and `zip(_:)` to both emit a **tuple** `(Self.Output, P.Output)` and both require `Self.Failure == P.Failure` — but MUST NOT treat their timing as interchangeable: `combineLatest` re-emits on *every* new value from *either* publisher once both have emitted at least once, while `zip` emits only once *both* sides have produced a next unconsumed element, pairing the oldest unconsumed pair. Per Apple's documentation, `combineLatest` "doesn't produce elements until each upstream publisher publishes at least one element... After that, it emits a new tuple whenever any publisher sends a value," while `zip` "waits until both publishers have emitted an event, then delivers the oldest unconsumed event from each publisher together as a tuple."

### Rule 5

Agents MUST expect `merge(with:)` to require `Self.Output == P.Output` **and** `Self.Failure == P.Failure`, and to emit a **flat, interleaved stream of that shared `Output` type** — not a tuple — unlike `combineLatest`/`zip`. Per Apple's documentation, `Publishers.Merge<A, B>` requires `A.Failure == B.Failure, A.Output == B.Output`, and the merge example shows elements printed individually and interleaved (`"1 40 90 2 50 100"`) as they arrive from either side, not paired.

## Compliant Example

```swift
import Combine

let numbers = PassthroughSubject<Int, Never>()
let letters = PassthroughSubject<String, Never>()

var cancellables = Set<AnyCancellable>()

numbers
    .map { $0 * 2 }                    // Rule 1: 1:1 transform
    .filter { $0 > 0 }                 // Rule 2: predicate-based subset
    .removeDuplicates()                // Rule 2: Output (Int) is Equatable
    .debounce(for: .milliseconds(300), scheduler: RunLoop.main) // Rule 3: explicit scheduler
    .sink { print("Value: \($0)") }
    .store(in: &cancellables)

numbers.combineLatest(letters)         // Rule 4: tuple (Int, String), re-emits on either side
    .sink { print("Combined: \($0)") }
    .store(in: &cancellables)

numbers.zip(numbers)                    // Rule 4: tuple, paired oldest-unconsumed elements
    .sink { print("Zipped: \($0)") }
    .store(in: &cancellables)

numbers.merge(with: numbers)            // Rule 5: flat Int stream, not a tuple
    .sink { print("Merged: \($0)") }
    .store(in: &cancellables)
```

## Non-Compliant Example

```swift
import Combine

let numbers = PassthroughSubject<Int, Never>()
let letters = PassthroughSubject<String, Never>()

numbers.combineLatest(letters)
    .sink { (value: Int) in print(value) } // violates Rule 4 -- treats tuple output as a bare Int
```
Assumes `combineLatest`'s output is a bare `Int` and binds it as such, ignoring that `combineLatest` (like `zip`) always emits a tuple of both publishers' outputs (Rule 4).

## Dependencies

Assumes the `Publisher`/subscription contract from `publishers-and-subscribers`: every operator here returns a new `Publisher` subscribed to and retained exactly as described there.

## References

- [Apple Developer — map(_:)](https://developer.apple.com/documentation/combine/publisher/map(_:)-99evh)
- [Apple Developer — filter(_:)](https://developer.apple.com/documentation/combine/publisher/filter(_:))
- [Apple Developer — removeDuplicates()](https://developer.apple.com/documentation/combine/publisher/removeduplicates())
- [Apple Developer — debounce(for:scheduler:options:)](https://developer.apple.com/documentation/combine/publisher/debounce(for:scheduler:options:))
- [Apple Developer — combineLatest(_:)](https://developer.apple.com/documentation/combine/publisher/combinelatest(_:))
- [Apple Developer — Publishers.Merge](https://developer.apple.com/documentation/combine/publishers/merge)
- [Apple Developer — zip(_:)](https://developer.apple.com/documentation/combine/publisher/zip(_:))
