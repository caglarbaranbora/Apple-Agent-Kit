# Observable Object Migration

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.observable-object-migration
artifact_type: knowledge
title: Observable Object Migration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how existing ObservableObject code is migrated to the Observable macro -- the platform floor the migration requires, Apple's per-type incremental path, the full property-wrapper mapping (@Published, @StateObject, @ObservedObject, @EnvironmentObject, .environmentObject, @Bindable), the fact that a half-migrated type still compiles and behaves correctly so a green build proves nothing, the tracking default that inverts when @Published is removed, and the invalidation-granularity change that makes the migration not behavior-preserving.
domain: SwiftUI
tags:
  - swiftui
  - observation
  - migration
  - observableobject
  - state
references:
  - https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro
  - https://developer.apple.com/documentation/observation/observable()
  - https://developer.apple.com/documentation/observation/observationignored()
  - https://developer.apple.com/documentation/swiftui/bindable
  - https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app
depends_on:
  - knowledge.swiftui.observable-macro
related:
  - knowledge.swiftui.state-and-binding
  - knowledge.swiftui.environment-values
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent converts *existing* `ObservableObject` code to the `@Observable` macro. `observable-macro` states what new code should look like; this contract is the path from code that already exists to that shape. Its central claim is that this migration has no failure signal: a type left half-converted compiles, runs, and updates its views correctly, so completeness cannot be inferred from a green build.

## Scope

### Included

- The platform floor the migration requires, what to do below it, and Apple's per-type incremental path through mixed-observation-system apps
- The complete property-wrapper and modifier mapping
- `@ObservationIgnored`, the tracking default that inverts on migration, and the invalidation-granularity change the migration introduces

### Excluded

- `@Observable` as the default for newly written code, and its ownership rules -- owned by `observable-macro`
- `@State`/`@Binding` for value-type state (`state-and-binding`) and `@Environment` key definition (`environment-values`)
- `@Published`'s publisher semantics and `objectWillChange` as Combine patterns -- owned by `knowledge.combine.published-and-observableobject`; this contract owns only their removal
- `NavigationView` migration -- see `navigation-view-migration`; different platform floor, separate task

## Rules

### Rule 1

Agents MUST confirm the deployment target reaches the Observation floor before migrating, and MUST leave `ObservableObject` in place below it. Per Apple's documentation, SwiftUI supports Observation "starting with iOS 17, iPadOS 17, macOS 14, tvOS 17, and watchOS 10." Below that floor `ObservableObject` is not legacy code; it is the only available mechanism, and `observable-macro` Rule 1's iOS 17+ default does not apply.

### Rule 2

Agents MUST migrate one data model type at a time rather than converting an app in a single pass, and MUST NOT treat a remaining `ObservableObject` type as a defect. Per Apple's documentation: "You don't need to make a wholesale replacement of the `ObservableObject` protocol throughout your app. Instead, you can make changes incrementally. Start by changing one data model type to use the `@Observable` macro. Your app can mix data model types that use different observation systems."

### Rule 3

Agents MUST complete the whole per-type mapping in Rule 4 and MUST NOT treat a successful build or correct-looking behavior as evidence the type is migrated. A type that has gained `@Observable` but is still held by `@StateObject` and injected with `.environmentObject(_:)` compiles and updates its views — by design. Per Apple's documentation: "data flow property wrappers such as `@StateObject` and `@EnvironmentObject` support types that use the `@Observable` macro. SwiftUI provides this support so apps can make source code changes incrementally." Nothing warns, so the only check is the mapping itself.

### Rule 4

Agents MUST apply the full mapping when converting a type, not the model-side half of it:

| Before | After |
|---|---|
| `: ObservableObject` conformance | `@Observable` macro on the type |
| `@Published var x` | `var x` (no wrapper) |
| `@StateObject private var m = M()` | `@State private var m = M()` |
| `.environmentObject(m)` | `.environment(m)` |
| `@EnvironmentObject var m: M` | `@Environment(M.self) var m` |
| `@ObservedObject var m: M` | `var m: M` (plain stored property) |
| `@ObservedObject` used for a binding | `@Bindable var m: M` |

Per Apple's documentation, the plain-property form works because "SwiftUI automatically tracks any observable properties that a view's `body` reads directly"; `@Bindable` is required only when "a view needs a binding to an observable type."

### Rule 5

Agents MUST mark properties that must not be tracked with `@ObservationIgnored`, because removing `@Published` inverts the tracking default. Under `ObservableObject`, tracking is opt-in per property via `@Published`. Under `@Observable`, per Apple's documentation, "Observation doesn't require a property wrapper to make a property observable. Instead, the accessibility of the property in relationship to an observer, such as a view, determines whether a property is observable" — so every reachable property becomes tracked unless opted out with `@ObservationIgnored`. A property that was deliberately left un-`@Published` is silently promoted by the migration.

### Rule 6

Agents MUST NOT describe this migration as behavior-preserving, because invalidation granularity changes. Per Apple's documentation: "when tracking as `@Observable`, SwiftUI updates a view only when an observable property changes and the view's `body` reads the property directly. The view doesn't update when observable properties not read by `body` changes. In contrast, a view updates when any published property of an `ObservableObject` instance changes, even if the view doesn't read the property that changes." A view that depended on being invalidated by a property it never reads — a cached value, a counter read in a helper — stops updating after migration.

## Compliant Example

```swift
// AFTER — model and every use site converted together (Rules 3, 4).
@Observable final class Library {
    var books: [Book] = []
    @ObservationIgnored var lastSyncToken: String?   // was un-@Published (Rule 5)
}

@main struct BookReaderApp: App {
    @State private var library = Library()           // was @StateObject
    var body: some Scene {
        WindowGroup { LibraryView().environment(library) }   // was .environmentObject
    }
}

struct LibraryView: View {
    @Environment(Library.self) private var library   // was @EnvironmentObject
    var body: some View { BookList(books: library.books) }
}

struct BookEditor: View {
    @Bindable var book: Book                         // was @ObservedObject; needs a binding
    var body: some View { TextField("Title", text: $book.title) }
}
```

## Non-Compliant Example

```swift
@Observable final class Library {
    var books: [Book] = []
    var lastSyncToken: String?
}

@main struct BookReaderApp: App {
    @StateObject private var library = Library()
    var body: some Scene {
        WindowGroup { LibraryView().environmentObject(library) }
    }
}
```
The model side was converted and the use sites were not. This builds and the views update, so nothing reports the state it is in (Rules 3, 4). `lastSyncToken` carried no `@Published` before and is now tracked, so writing it invalidates every view that reads the model (Rule 5).

## Dependencies

- `observable-macro` -- it owns what `@Observable` code must look like, including the `@State` ownership rule and the prohibition on mixing observation mechanisms within one type. This contract owns only the conversion of existing code into that shape.

## References

- [Apple Developer — Migrating from the Observable Object protocol to the Observable macro](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro)
- [Apple Developer — Observable()](https://developer.apple.com/documentation/observation/observable())
- [Apple Developer — ObservationIgnored()](https://developer.apple.com/documentation/observation/observationignored())
- [Apple Developer — Bindable](https://developer.apple.com/documentation/swiftui/bindable)
- [Apple Developer — Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app)
