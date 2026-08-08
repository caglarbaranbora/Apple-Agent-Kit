# Published and ObservableObject

Status: Approved
Version: 1.0.0

## Metadata

```yaml
id: knowledge.combine.published-and-observableobject
artifact_type: knowledge
title: Published and ObservableObject
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the @Published property wrapper, the ObservableObject protocol, the auto-synthesized objectWillChange publisher, and how @Published's projectedValue (the $name publisher) relates to the wrapped property, including the willSet-timing gotcha where subscribers see the new value before the property itself is updated.
domain: Combine
tags:
  - combine
  - published
  - observableobject
  - objectwillchange
references:
  - https://developer.apple.com/documentation/combine/published
  - https://developer.apple.com/documentation/combine/observableobject
depends_on:
  - knowledge.combine.publishers-and-subscribers
related: []
last_updated: 2026-08-08
```

## Intent

This contract governs declaring an observable model with `@Published` properties and `ObservableObject` conformance: what `@Published` publishes, when it publishes relative to the property's own mutation, and what `ObservableObject`'s synthesized `objectWillChange` publisher does. It assumes the `Publisher`/`sink`/`AnyCancellable` vocabulary from `publishers-and-subscribers`.

## Scope

### Included

- `@Published` and its `projectedValue` (the `$name` publisher)
- The class-only constraint on `@Published`
- `ObservableObject`'s `objectWillChange` requirement and its default synthesis
- The `willSet`-timing detail of when `@Published` emits relative to the property mutation

### Excluded

- `PassthroughSubject`/`CurrentValueSubject` — see `subjects`
- `assign(to:)` writing a publisher's output into a `@Published` property — see `assign-and-memory-management`
- SwiftUI's `@ObservedObject`/`@StateObject` view-side consumption of `ObservableObject` — out of scope for this Combine-only contract

## Rules

### Rule 1

Agents MUST apply `@Published` only to a property of a `class`, never a `struct` or other non-class type. Per Apple's documentation: "The `@Published` attribute is class constrained. Use it with properties of classes, not with non-class types like structures."

### Rule 2

Agents MUST access a `@Published` property's publisher through its `$`-prefixed projected value, not by reading the property itself. Per Apple's documentation: "Publishing a property with the `@Published` attribute creates a publisher of this type. You access the publisher with the `$` operator," e.g. `weather.$temperature`.

### Rule 3

Agents MUST NOT assume a `@Published` property already holds its new value inside a subscriber's `receiveValue` closure at the moment that closure runs. Per Apple's documentation: "publishing occurs in the property's `willSet` block, meaning subscribers receive the new value before it's actually set on the property" — reading the property directly inside that closure still returns the old value.

### Rule 4

Agents MUST NOT hand-implement `objectWillChange` on a class that already declares `@Published` properties and conforms to `ObservableObject`, since it is synthesized automatically. Per Apple's documentation: "By default, an `ObservableObject` synthesizes an `objectWillChange` publisher that emits the changed value before any of its `@Published` properties changes."

### Rule 5

Agents SHOULD subscribe to `objectWillChange` (rather than each individual `@Published` publisher) only when a change to *any* observable property should trigger the same reaction, since it fires once per mutating property change across the whole object. This is reasoned synthesis from the documented default-synthesis behavior in Rule 4: a single `objectWillChange` subscription covers every `@Published` property without wiring one subscriber per property.

## Compliant Example

```swift
import Combine

final class Weather: ObservableObject { // Rule 1: class, not struct
    @Published var temperature: Double
    init(temperature: Double) { self.temperature = temperature }
}

let weather = Weather(temperature: 20)
var cancellables = Set<AnyCancellable>()

weather.$temperature // Rule 2: projected value, not `weather.temperature`
    .sink { newValue in
        print("Incoming: \(newValue)")           // Rule 3: new value arrives here
        // weather.temperature still reads the OLD value inside this closure
    }
    .store(in: &cancellables)

weather.objectWillChange // Rule 4/5: rely on synthesis, one subscription for all properties
    .sink { _ in print("Something on weather will change") }
    .store(in: &cancellables)
```

## Non-Compliant Example

```swift
import Combine

final class Weather: ObservableObject {
    @Published var temperature: Double
    init(temperature: Double) { self.temperature = temperature }

    var objectWillChange: ObservableObjectPublisher { ObservableObjectPublisher() } // violates Rule 4

    func logChange() {
        _ = temperature // caller assumes this already reflects a value just delivered by a subscriber -- violates Rule 3
    }
}
```
Hand-implements `objectWillChange` even though `@Published` properties already trigger the synthesized one (Rule 4), and treats direct property reads as reflecting a value a subscriber just received, ignoring the `willSet`-timing behavior (Rule 3).

## Dependencies

Assumes the `Publisher`/`sink`/`AnyCancellable` contract from `publishers-and-subscribers`: `$name` and `objectWillChange` are ordinary Combine publishers subscribed to and retained exactly as described there.

## References

- [Apple Developer — Published](https://developer.apple.com/documentation/combine/published)
- [Apple Developer — ObservableObject](https://developer.apple.com/documentation/combine/observableobject)
