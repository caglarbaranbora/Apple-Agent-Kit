# Assign and Memory Management

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.combine.assign-and-memory-management
artifact_type: knowledge
title: Assign and Memory Management
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines assign(to:on:) and the newer assign(to:) into a @Published property, the documented strong-reference retain-cycle risk of assign(to:on:), and .store(in:) for AnyCancellable lifetime management in a Set<AnyCancellable>.
domain: Combine
tags:
  - combine
  - assign
  - memory-management
  - retain-cycle
  - anycancellable
references:
  - https://developer.apple.com/documentation/combine/publisher/assign(to:on:)
  - https://developer.apple.com/documentation/combine/publisher/assign(to:)
  - https://developer.apple.com/documentation/combine/anycancellable/store(in:)-3hyxs
depends_on:
  - knowledge.combine.publishers-and-subscribers
related:
  - knowledge.combine.published-and-observableobject
last_updated: 2026-08-08
```

## Intent

This contract governs writing a publisher's output directly into a property via `assign(to:on:)` or `assign(to:)`, the documented retain-cycle risk of the former, and using `AnyCancellable.store(in:)` to manage subscription lifetime. It assumes the `Publisher`/`AnyCancellable` vocabulary from `publishers-and-subscribers`.

## Scope

### Included

- `assign(to:on:)` (`Failure == Never`) and its strong-reference behavior toward the target object
- `assign(to:)` into a `@Published` property's projected value (`&$property`)
- Choosing between the two based on retain-cycle risk
- `AnyCancellable.store(in:)` into a `Set<AnyCancellable>`

### Excluded

- Declaring the `@Published` property itself — see `published-and-observableobject`
- `sink`-based subscription and general cancellable retention — see `publishers-and-subscribers`
- Manual `weak`/`unowned` capture inside a `sink` closure — out of scope for v1 (this contract covers only the documented `assign` behavior)

## Rules

### Rule 1

Agents MUST use `assign(to:on:)` only on a publisher whose `Failure` is `Never`. Per Apple's documentation, `assign<Root>(to keyPath:on:) -> AnyCancellable` is available "when `Failure` is `Never`," and is used to "set a given property each time a publisher produces a value."

### Rule 2

Agents MUST treat `assign(to:on:)`'s target object as strongly retained by the subscription itself, and MUST NOT assume that merely dropping the returned `AnyCancellable` releases the object immediately. Per Apple's documentation: "The `Subscribers.Assign` instance created by this operator maintains a strong reference to `object`, and sets it to `nil` when the upstream publisher completes (either normally or with an error)."

### Rule 3

Agents MUST prefer `assign(to:)` over `assign(to:on:)` when the target property is a `@Published` property on the same object that owns the subscription, since `assign(to:)` does not return an `AnyCancellable` to manage and avoids the reference-cycle risk of storing one on `self`. Per Apple's documentation: "This solves a critical problem with `assign(to:on:)`: storing the returned `AnyCancellable` can cause a reference cycle, because the `Subscribers.Assign` subscriber holds a strong reference to `self`. Using `assign(to:)` eliminates this issue," and its signature takes the property via `inout` as `&$property`.

### Rule 4

Agents MUST call `.store(in:)` on any `AnyCancellable` they intend to keep alive rather than assigning it to an ignored local, most commonly into a `Set<AnyCancellable>`. Per Apple's documentation, `AnyCancellable.store(in:)` (the `Set` overload) is declared `final func store(in set: inout Set<AnyCancellable>)`, described as "Stores this type-erasing cancellable instance in the specified set."

### Rule 5

Agents SHOULD choose `assign(to:on:)` only for a *different* target object than the one holding the subscription (e.g. a view updating a separate view model's property), and SHOULD default to `assign(to:)` when writing into the subscribing object's own `@Published` state. This is reasoned synthesis from Rules 2–3: `assign(to:on:)`'s strong-reference risk is specifically a same-object cycle risk, which `assign(to:)` was documented as introduced to eliminate.

## Compliant Example

```swift
import Combine

final class TemperatureViewModel: ObservableObject {
    @Published var displayText: String = ""
    private var cancellables = Set<AnyCancellable>()

    init(sensor: AnyPublisher<Double, Never>) {
        sensor
            .map { "\($0)°" }
            .assign(to: &$displayText) // Rule 3/5: same-object @Published target, no cancellable to manage
    }

    func mirror(into logger: LogModel, from sensor: AnyPublisher<Double, Never>) {
        sensor
            .map { "\($0)°" }
            .assign(to: \.lastReading, on: logger) // Rule 1/5: different target object
            .store(in: &cancellables)              // Rule 4
    }
}
```

## Non-Compliant Example

```swift
import Combine

final class TemperatureViewModel: ObservableObject {
    @Published var displayText: String = ""
    var leak: AnyCancellable? // holds a self-targeting Assign subscriber

    init(sensor: AnyPublisher<Double, Never>) {
        leak = sensor
            .map { "\($0)°" }
            .assign(to: \.displayText, on: self) // violates Rule 3 -- same-object target via assign(to:on:)
        // `leak` is never passed to .store(in:) anywhere else in the type -- violates Rule 4 pattern
    }
}
```
Uses `assign(to:on:)` to write into `self`'s own `@Published` property instead of `assign(to:)` (Rule 3), creating the documented same-object strong-reference risk (Rule 2) that Rule 5 says to avoid by construction.

## Dependencies

Assumes the `Publisher`/`AnyCancellable` retention contract from `publishers-and-subscribers`, and relates to `published-and-observableobject` for the `@Published`/`$property` target that `assign(to:)` writes into.

## References

- [Apple Developer — assign(to:on:)](https://developer.apple.com/documentation/combine/publisher/assign(to:on:))
- [Apple Developer — assign(to:)](https://developer.apple.com/documentation/combine/publisher/assign(to:))
- [Apple Developer — AnyCancellable.store(in:)](https://developer.apple.com/documentation/combine/anycancellable/store(in:)-3hyxs)
