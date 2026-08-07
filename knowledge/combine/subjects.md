# Subjects

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.combine.subjects
artifact_type: knowledge
title: Subjects
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines PassthroughSubject<Output, Failure> versus CurrentValueSubject<Output, Failure> -- the latter requires an initial value and exposes .value -- plus send(_:) and send(completion:) for imperatively injecting values and termination into a Combine stream.
domain: Combine
tags:
  - combine
  - subject
  - passthroughsubject
  - currentvaluesubject
references:
  - https://developer.apple.com/documentation/combine/subject
  - https://developer.apple.com/documentation/combine/passthroughsubject
  - https://developer.apple.com/documentation/combine/currentvaluesubject
depends_on:
  - knowledge.combine.publishers-and-subscribers
related: []
last_updated: 2026-08-07
```

## Intent

This contract governs choosing between and using Combine's two concrete `Subject` types for bridging imperative code into a publisher: `PassthroughSubject`, which has no memory of past values, and `CurrentValueSubject`, which always holds a current value. It assumes the `Publisher`/subscription vocabulary from `publishers-and-subscribers`.

## Scope

### Included

- `PassthroughSubject<Output, Failure>` and its lack of an initial value or buffer
- `CurrentValueSubject<Output, Failure>`, its required initial value, and its `.value` property
- `send(_:)` and `send(completion:)`
- Choosing between the two based on whether "current state" semantics are needed

### Excluded

- `@Published`/`ObservableObject` — see `published-and-observableobject`
- Operators applied downstream of a subject — see `operators-transforming-and-combining`
- Custom `Subject`/`Publisher` conformances — out of scope for v1

## Rules

### Rule 1

Agents MUST NOT expect a `PassthroughSubject` to replay a value to a subscriber that subscribes after `send(_:)` was already called, and MUST NOT expect it to hold any value when there is no active subscriber. Per Apple's documentation: "Unlike `CurrentValueSubject`, a `PassthroughSubject` doesn't have an initial value or a buffer of the most recently-published element. A `PassthroughSubject` drops values if there are no subscribers, or its current demand is zero."

### Rule 2

Agents MUST supply an initial value when constructing a `CurrentValueSubject`, since it has no default/empty initializer. Per Apple's documentation, its initializer is `init(_ initialValue: Output)`, described as "Creates a current value subject with the given initial value."

### Rule 3

Agents MAY read a `CurrentValueSubject`'s latest value synchronously via its `.value` property instead of subscribing, and MUST know that calling `send(_:)` also updates that property. Per Apple's documentation: "Calling `send(_:)` on a `CurrentValueSubject` also updates the current value, making it equivalent to updating the `value` property directly."

### Rule 4

Agents MUST call `send(completion:)` (not simply stop calling `send(_:)`) to terminate a subject's stream and trigger downstream `receiveCompletion` handling. Per Apple's documentation, `Subject` requires `func send(completion: Subscribers.Completion<Self.Failure>)`, described as sending "a completion signal to the subscriber."

### Rule 5

Agents SHOULD choose `CurrentValueSubject` when downstream code needs a synchronously-readable "current state" (e.g. backing an `ObservableObject`-like value), and SHOULD choose `PassthroughSubject` for broadcasting discrete one-off events (e.g. a button tap) where there is no meaningful "current value." This is reasoned synthesis from Rules 1–3: only `CurrentValueSubject` documents a readable `.value`, and only `PassthroughSubject` is documented as dropping values with no buffering.

## Compliant Example

```swift
import Combine

final class SearchModel {
    let queryChanged = PassthroughSubject<String, Never>()      // Rule 1/5: discrete event
    let status = CurrentValueSubject<String, Never>("idle")      // Rule 2/5: current state

    func userTyped(_ text: String) {
        queryChanged.send(text)                                  // Rule 1: no replay needed
    }

    func finish() {
        print(status.value)                                      // Rule 3: synchronous read
        status.send("finished")                                   // Rule 3: also updates .value
        queryChanged.send(completion: .finished)                  // Rule 4
    }
}
```

## Non-Compliant Example

```swift
import Combine

final class SearchModel {
    let status = CurrentValueSubject<String, Never>()      // violates Rule 2 -- no initial value supplied
    let queryChanged = PassthroughSubject<String, Never>()

    func finish() {
        // Caller just stops calling send(_:) and never signals completion -- violates Rule 4
    }
}
```
Fails to supply the required initial value to `CurrentValueSubject`'s initializer (Rule 2), and never calls `send(completion:)`, leaving downstream subscribers with no termination signal (Rule 4).

## Dependencies

Assumes the `Publisher`/subscription contract from `publishers-and-subscribers`: both subject types are publishers, subscribed to and retained exactly as described there.

## References

- [Apple Developer — Subject](https://developer.apple.com/documentation/combine/subject)
- [Apple Developer — PassthroughSubject](https://developer.apple.com/documentation/combine/passthroughsubject)
- [Apple Developer — CurrentValueSubject](https://developer.apple.com/documentation/combine/currentvaluesubject)
