# Publishers and Subscribers

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.combine.publishers-and-subscribers
artifact_type: knowledge
title: Publishers and Subscribers
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the Publisher/Subscriber protocol contract, subscribing via sink(receiveCompletion:receiveValue:) or the Failure == Never sink(receiveValue:) overload, type-erasing the subscription into AnyCancellable, and the requirement to retain that AnyCancellable or the subscription tears down immediately.
domain: Combine
tags:
  - combine
  - publisher
  - subscriber
  - sink
  - anycancellable
references:
  - https://developer.apple.com/documentation/combine/publisher
  - https://developer.apple.com/documentation/combine/subscriber
  - https://developer.apple.com/documentation/combine/publisher/sink(receivecompletion:receivevalue:)
  - https://developer.apple.com/documentation/combine/publisher/sink(receivevalue:)
  - https://developer.apple.com/documentation/combine/anycancellable
depends_on: []
related: []
last_updated: 2026-08-07
```

## Intent

This contract governs the foundational Combine subscription contract: how a `Publisher` and a `Subscriber` must agree on element and error type, how to subscribe with `sink`, and why the resulting `AnyCancellable` must be retained. Every other Combine Knowledge Contract in this domain assumes this vocabulary.

## Scope

### Included

- The `Publisher`/`Subscriber` associated-type contract (`Output`/`Failure` must match `Input`/`Failure`)
- `sink(receiveCompletion:receiveValue:)` and the `sink(receiveValue:)` overload (`Failure == Never` only)
- `AnyCancellable` and its cancel-on-deinit behavior
- The requirement to retain a subscription's `AnyCancellable`

### Excluded

- Writing a custom `Publisher`/`Subscriber` conformance — out of scope for v1
- Backpressure / `Subscribers.Demand` — out of scope for v1
- `.store(in:)` mechanics — see `assign-and-memory-management`
- `@Published`/`ObservableObject`, subjects, and operators — see their own contracts

## Rules

### Rule 1

Agents MUST only pair a `Subscriber` with a `Publisher` whose `Output`/`Failure` match the subscriber's `Input`/`Failure`. Per Apple's documentation: "A given subscriber's `Input` and `Failure` associated types must match the `Output` and `Failure` of its corresponding publisher."

### Rule 2

Agents MUST use `sink(receiveValue:)` only on a publisher whose `Failure` is `Never`, and MUST use `sink(receiveCompletion:receiveValue:)` for any publisher that can fail. Per Apple's documentation, `sink(receiveValue:)` is "Available when `Failure` is `Never`" and "can only be used when the stream doesn't fail," whereas `sink(receiveCompletion:receiveValue:)` carries no such constraint.

### Rule 3

Agents MUST retain the `AnyCancellable` returned by `sink`, typically as a stored property or in a collection, or the subscription is torn down before it can deliver values. Per Apple's documentation on `sink`: "The return value should be held, otherwise the stream will be canceled," and on `AnyCancellable`: "An `AnyCancellable` instance automatically calls `cancel()` when deinitialized."

### Rule 4

Agents MUST expect a subscriber to receive events in a fixed order: a `Subscription` first, then zero or more elements, then at most one completion. Per Apple's documentation on `Subscriber`: "the publisher invokes the subscriber's `receive(subscription:)` method... After the subscriber makes an initial demand, the publisher calls `receive(_:)`... If the publisher stops publishing, it calls `receive(completion:)`."

### Rule 5

Agents SHOULD collect multiple sibling subscriptions on the same owning type into a single `Set<AnyCancellable>` rather than one stored property per subscription, when a type holds more than one active subscription. This is reasoned synthesis: `AnyCancellable` conforms to `Hashable` (enabling set storage) and per-subscription properties do not scale as subscription count grows.

## Compliant Example

```swift
import Combine

final class TemperatureMonitor {
    private var cancellables = Set<AnyCancellable>() // Rule 5

    func observe(_ publisher: AnyPublisher<Double, Never>) {
        publisher
            .sink { value in                 // Rule 2: Failure == Never overload
                print("Temp: \(value)")
            }
            .store(in: &cancellables)         // Rule 3: retained, not dropped
    }

    func observeFallible(_ publisher: AnyPublisher<Double, URLError>) {
        publisher
            .sink(                            // Rule 2: fallible publisher, full overload
                receiveCompletion: { completion in
                    if case .failure(let error) = completion { print(error) }
                },
                receiveValue: { value in print("Temp: \(value)") } // Rule 4: value(s) before completion
            )
            .store(in: &cancellables)
    }
}
```

## Non-Compliant Example

```swift
import Combine

final class LeakyMonitor {
    func observe(_ publisher: AnyPublisher<Double, Never>) {
        publisher.sink { value in print(value) } // violates Rule 3 -- return value discarded
    }

    func observeFallible(_ publisher: AnyPublisher<Double, URLError>) -> AnyCancellable {
        publisher.sink { value in print(value) } // violates Rule 2 -- Failure is URLError, not Never
    }
}
```
Discards the `AnyCancellable` from `sink` so the subscription is canceled almost immediately on return (Rule 3), and calls the `Failure == Never` `sink(receiveValue:)` overload on a publisher whose `Failure` is `URLError` (Rule 2).

## Dependencies

None within this domain — this is the foundational contract every other Combine Knowledge Contract assumes when referring to "a publisher," "a subscription," or "the cancellable."

## References

- [Apple Developer — Publisher](https://developer.apple.com/documentation/combine/publisher)
- [Apple Developer — Subscriber](https://developer.apple.com/documentation/combine/subscriber)
- [Apple Developer — sink(receiveCompletion:receiveValue:)](https://developer.apple.com/documentation/combine/publisher/sink(receivecompletion:receivevalue:))
- [Apple Developer — sink(receiveValue:)](https://developer.apple.com/documentation/combine/publisher/sink(receivevalue:))
- [Apple Developer — AnyCancellable](https://developer.apple.com/documentation/combine/anycancellable)
