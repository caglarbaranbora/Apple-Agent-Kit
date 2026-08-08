# Combine

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.combine
artifact_type: reference
title: Combine
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's Combine documentation, scoped to this domain's v1.
domain: Combine
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/combine
https://developer.apple.com/documentation/combine/publisher
https://developer.apple.com/documentation/combine/subscriber
https://developer.apple.com/documentation/combine/publisher/sink(receivecompletion:receivevalue:)
https://developer.apple.com/documentation/combine/publisher/sink(receivevalue:)
https://developer.apple.com/documentation/combine/anycancellable
https://developer.apple.com/documentation/combine/anycancellable/store(in:)-3hyxs
https://developer.apple.com/documentation/combine/published
https://developer.apple.com/documentation/combine/observableobject
https://developer.apple.com/documentation/combine/subject
https://developer.apple.com/documentation/combine/passthroughsubject
https://developer.apple.com/documentation/combine/currentvaluesubject
https://developer.apple.com/documentation/combine/publisher/map(_:)-99evh
https://developer.apple.com/documentation/combine/publisher/filter(_:)
https://developer.apple.com/documentation/combine/publisher/removeduplicates()
https://developer.apple.com/documentation/combine/publisher/debounce(for:scheduler:options:)
https://developer.apple.com/documentation/combine/publisher/combinelatest(_:)
https://developer.apple.com/documentation/combine/publishers/merge
https://developer.apple.com/documentation/combine/publisher/zip(_:)
https://developer.apple.com/documentation/combine/publisher/assign(to:on:)
https://developer.apple.com/documentation/combine/publisher/assign(to:)

## Purpose

Reference index for Apple's Combine documentation, scoped to this domain's v1: the `Publisher`/`Subscriber` protocol pair and subscribing via `sink(receiveCompletion:receiveValue:)` (or the `Failure == Never` `sink(receiveValue:)` overload) into a retained `AnyCancellable`; the `@Published` property wrapper and `ObservableObject`'s synthesized `objectWillChange`; `PassthroughSubject` versus `CurrentValueSubject` for imperatively injecting values into a stream; the transforming/combining operators `map`, `filter`, `removeDuplicates`, `debounce(for:scheduler:)`, `combineLatest`, `merge`, and `zip`; and `assign(to:on:)`/`assign(to:)` with their documented retain-cycle risk plus `store(in:)` for cancellable lifetime management. Combine is Apple's declarative, reactive/functional framework for processing values that change over time by composing publishers and subscribers — there is no direct sibling domain the way SwiftData pairs with Core Data.

Out of scope for v1: Combine-to-async/await interop (`Publisher.values`, `AsyncPublisher`); writing custom `Publisher`/`Subscriber` conformances; backpressure and `Subscribers.Demand`; Combine integration with SwiftData/Core Data; and `Timer.publish`/`NotificationCenter.publisher` as dedicated contracts (fine as an example inside another contract, not their own).

## Primary Topics

- `Publisher`/`Subscriber`, `sink(receiveCompletion:receiveValue:)`/`sink(receiveValue:)`, and retaining the returned `AnyCancellable`
- `@Published` and `ObservableObject`'s synthesized `objectWillChange` publisher
- `PassthroughSubject` vs. `CurrentValueSubject`, `send(_:)`, `send(completion:)`
- Transforming (`map`, `filter`, `removeDuplicates`, `debounce`) and combining (`combineLatest`, `merge`, `zip`) operators
- `assign(to:on:)`/`assign(to:)`, their retain-cycle risk, and `store(in:)`

## Used By

- knowledge/combine/publishers-and-subscribers.md ([[knowledge/combine/publishers-and-subscribers]])
- knowledge/combine/published-and-observableobject.md ([[knowledge/combine/published-and-observableobject]])
- knowledge/combine/subjects.md ([[knowledge/combine/subjects]])
- knowledge/combine/operators-transforming-and-combining.md ([[knowledge/combine/operators-transforming-and-combining]])
- knowledge/combine/assign-and-memory-management.md ([[knowledge/combine/assign-and-memory-management]])
- skills/combine/SKILL.md ([[skills/combine/SKILL]])
