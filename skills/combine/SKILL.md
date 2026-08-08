---
name: combine
description: Route Combine implementation tasks to the correct Knowledge Contracts -- the Publisher/Subscriber protocol pair, sink(receiveCompletion:receiveValue:)/sink(receiveValue:) and retaining the returned AnyCancellable; @Published/ObservableObject and the synthesized objectWillChange publisher; PassthroughSubject vs. CurrentValueSubject with send(_:)/send(completion:); the operators map/filter/removeDuplicates/debounce(for:scheduler:)/combineLatest/merge/zip; and assign(to:on:)/assign(to:) with their retain-cycle risk plus .store(in:). Use when writing publisher.sink { ... }, .sink(receiveCompletion:receiveValue:), var cancellable: AnyCancellable, .store(in: &cancellables), @Published var name: Type, class Foo: ObservableObject, objectWillChange, $propertyName, PassthroughSubject<Output, Failure>(), CurrentValueSubject<Output, Failure>(initialValue), subject.send(_:), subject.send(completion:), .map { }, .filter { }, .removeDuplicates(), .debounce(for:scheduler:), .combineLatest(_:), .merge(with:), .zip(_:), .assign(to:on:), or .assign(to: &$property). v1 is Combine only -- no async/await interop (Publisher.values, AsyncPublisher), no custom Publisher/Subscriber conformances, no backpressure/Subscribers.Demand, no SwiftData/Core Data interop, and Timer.publish/NotificationCenter.publisher are usable only as examples inside other contracts, not their own contract. Triggers on Combine, Publisher, Subscriber, AnyCancellable, @Published, ObservableObject, objectWillChange, PassthroughSubject, CurrentValueSubject, sink, assign, store(in:), combineLatest, debounce, removeDuplicates.
id: skill.combine.foundations
title: Combine — Foundations
version: 1.0.0
status: Approved
artifact_type: skill
domain: Combine
routes: [knowledge.combine.publishers-and-subscribers, knowledge.combine.published-and-observableobject, knowledge.combine.subjects, knowledge.combine.operators-transforming-and-combining, knowledge.combine.assign-and-memory-management]
related: []
last_updated: 2026-08-08
---

# Combine — Foundations Skill

## Purpose

Route Combine implementation tasks to the minimum required Combine
Knowledge Contracts. v1 scope is the `Publisher`/`Subscriber`/`sink`/
`AnyCancellable` subscription contract, `@Published`/`ObservableObject`,
`PassthroughSubject`/`CurrentValueSubject`, the core transforming/
combining operators, and `assign(to:on:)`/`assign(to:)` with cancellable
lifetime management -- not async/await interop, custom conformances,
backpressure, or SwiftData/Core Data interop.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/combine/.

-   Subscribing with `sink(receiveCompletion:receiveValue:)` or
    `sink(receiveValue:)`; asking whether `Failure == Never` applies;
    or reasoning about retaining/discarding an `AnyCancellable` ->
    publishers-and-subscribers.md
-   Declaring `@Published var x`; accessing `$x`; conforming to
    `ObservableObject`; or asking what `objectWillChange` does and when
    it fires -> published-and-observableobject.md
-   Choosing `PassthroughSubject` vs. `CurrentValueSubject`; reading or
    writing `.value`; or calling `send(_:)`/`send(completion:)` ->
    subjects.md
-   Applying `map`/`filter`/`removeDuplicates`/`debounce(for:scheduler:)`;
    or combining multiple publishers with `combineLatest`/`merge`/`zip`
    and asking what shape the output takes -> operators-transforming-and-combining.md
-   Writing a publisher's output into a property with `assign(to:on:)`
    or into a `@Published` property with `assign(to:)`; diagnosing a
    retain-cycle risk; or calling `.store(in:)` -> assign-and-memory-management.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/combine/ — do not guess or fall back to general
knowledge. Combine-to-async/await interop (`Publisher.values`,
`AsyncPublisher`/`AsyncThrowingPublisher`) is out of scope entirely --
do not fabricate a bridging pattern. Writing a custom `Publisher` or
`Subscriber` conformance is out of scope entirely -- route only to the
built-in publishers/operators these contracts cover. Backpressure and
`Subscribers.Demand` reasoning is out of scope entirely -- do not
fabricate demand-management guidance. Combine integration with
SwiftData or Core Data is out of scope entirely -- report the boundary
rather than answer from a persistence domain. `Timer.publish`/
`NotificationCenter.publisher` have no dedicated contract -- they may
appear only as an example inside another contract's Compliant Example,
never as their own routing target.
