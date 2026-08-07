# Model Container Setup

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.swiftdata.model-container-setup
artifact_type: knowledge
title: Model Container Setup
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines creating and injecting a SwiftData ModelContainer -- the SwiftUI .modelContainer(for:) scene/view modifier, ModelConfiguration (in-memory vs. on-disk via isStoredInMemoryOnly), the manual ModelContainer(for:configurations:) initializer for non-SwiftUI contexts or previews, and how .modelContainer makes a ModelContext available via @Environment(\.modelContext).
domain: SwiftData
tags:
  - swiftdata
  - modelcontainer
  - modelconfiguration
  - environment
  - previews
references:
  - https://developer.apple.com/documentation/swiftdata/modelcontainer
  - https://developer.apple.com/documentation/swiftdata/modelconfiguration
  - https://developer.apple.com/documentation/swiftui/view/modelcontainer(_:)
  - https://developer.apple.com/documentation/swiftui/view/modelcontainer(for:inmemory:isautosaveenabled:isundoenabled:onsetup:)
  - https://developer.apple.com/documentation/swiftui/environmentvalues/modelcontext
  - https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches
depends_on:
  - knowledge.swiftdata.model-definition
related:
  - knowledge.swiftdata.model-context-crud
last_updated: 2026-08-06
```

## Intent

This contract governs creating a `ModelContainer` for one or more `@Model` types (see `model-definition`) and making it available to the app: the SwiftUI `.modelContainer` view/scene modifiers, `ModelConfiguration` for controlling in-memory vs. on-disk storage, and the manual `ModelContainer(for:configurations:)` initializer used in non-SwiftUI code or SwiftUI previews. Once a container exists, `model-context-crud` governs using the `ModelContext` it exposes.

## Scope

### Included

- `.modelContainer(for:inMemory:isAutosaveEnabled:isUndoEnabled:onSetup:)` — the primary SwiftUI convenience modifier
- `.modelContainer(_:)` — attaching an already-created `ModelContainer`
- `ModelConfiguration(isStoredInMemoryOnly:)` and related inits for manual storage configuration
- `ModelContainer(for:configurations:)` for creating a container outside SwiftUI (services, tests, previews)
- How `.modelContainer` populates `@Environment(\.modelContext)` for descendant views

### Excluded

- `ModelConfiguration(cloudKitDatabase:)` and CloudKit sync — out of scope for v1
- `SchemaMigrationPlan`/`VersionedSchema` migration — out of scope for v1
- Reading/writing models once the context exists — see `model-context-crud`
- App Group container sharing and widget-extension-specific setup — out of scope for v1

## Rules

### Rule 1

Agents building a SwiftUI app SHOULD attach `.modelContainer(for:)` once, at the top of the view (or scene) hierarchy, rather than constructing a `ModelContainer` manually inside a view. Per Apple's documentation, `modelContainer(for:inMemory:isAutosaveEnabled:isUndoEnabled:onSetup:)` "Sets the model container in this view for storing the provided model type, creating a new container if necessary, and also sets a model context for that container in this view's environment" — its declared signature is `func modelContainer(for modelType: any PersistentModel.Type, inMemory: Bool = false, isAutosaveEnabled: Bool = true, isUndoEnabled: Bool = false, onSetup: @escaping (Result<ModelContainer, any Error>) -> Void = { _ in }) -> some View`.

### Rule 2

Agents who already hold a constructed `ModelContainer` (e.g., one built for a preview or test) MUST attach it with `.modelContainer(_:)` rather than re-deriving it from a model type. Per Apple's documentation, `modelContainer(_:)` "Sets the model container and associated model context in this view's environment" with signature `func modelContainer(_ container: ModelContainer) -> some View`.

### Rule 3

Agents needing in-memory-only storage (previews, unit tests, ephemeral state) MUST use `ModelConfiguration`'s `isStoredInMemoryOnly` parameter/property rather than the `.modelContainer(for:)` modifier's `inMemory:` parameter when they also need other configuration (e.g., `allowsSave`). Per Apple's documentation: `let configuration = ModelConfiguration(isStoredInMemoryOnly: true, allowsSave: false)` followed by `let container = try ModelContainer(for: Trip.self, Accommodation.self, configurations: configuration)`. Agents SHOULD NOT confuse this property name with the SwiftUI modifier's own `inMemory:` parameter (Rule 1) — they configure the same behavior at two different layers and are not interchangeable spellings of one symbol.

### Rule 4

Agents working outside SwiftUI (a service layer, background task, or command-line tool) MUST create a container with `ModelContainer(for:configurations:)`, which throws, and MUST propagate or handle that error rather than force-trying it in production code paths. Per Apple's documentation, the initializer is declared `convenience init(for forTypes: any PersistentModel.Type..., configurations: any DataStoreConfiguration...) throws`.

### Rule 5

Agents MUST NOT read `@Environment(\.modelContext)` in a view that sits outside the subtree `.modelContainer` was attached to, and MUST attach `.modelContainer` above every view that needs that environment value. Per Apple's documentation, `EnvironmentValues.modelContext` is "The SwiftData model context that will be used for queries and other model operations within this environment" — it is populated by `.modelContainer`, so a view outside that subtree finds no matching context.

## Compliant Example

```swift
import SwiftUI
import SwiftData

@main
struct TripsApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Trip.self) // Rule 1
    }
}

#Preview {
    let configuration = ModelConfiguration(isStoredInMemoryOnly: true) // Rule 3
    let container = try! ModelContainer(for: Trip.self, configurations: configuration) // Rule 4
    ContentView()
        .modelContainer(container) // Rule 2
}

struct ContentView: View {
    @Environment(\.modelContext) private var context // Rule 5: inside the .modelContainer subtree

    var body: some View { Text("Trips") }
}
```

## Non-Compliant Example

```swift
import SwiftUI
import SwiftData

struct DetailView: View {
    // No .modelContainer anywhere above this view in the hierarchy -- violates Rule 5.
    @Environment(\.modelContext) private var context

    var body: some View {
        // Force-tries a manual container inside a view body instead of using
        // .modelContainer(for:) or .modelContainer(_:) -- violates Rule 1 and Rule 2.
        let container = try! ModelContainer(for: Trip.self)
        return Text("Trips")
    }
}
```
Builds a `ModelContainer` by hand inside a view body instead of the `.modelContainer` modifiers (Rule 1, Rule 2), and reads `@Environment(\.modelContext)` in a view with no `.modelContainer` above it in the hierarchy to actually populate that value (Rule 5).

## Dependencies

Depends on `model-definition` for the `@Model` types passed to `.modelContainer(for:)`/`ModelContainer(for:configurations:)`.

## References

- [Apple Developer — ModelContainer](https://developer.apple.com/documentation/swiftdata/modelcontainer)
- [Apple Developer — ModelConfiguration](https://developer.apple.com/documentation/swiftdata/modelconfiguration)
- [Apple Developer — modelContainer(_:)](https://developer.apple.com/documentation/swiftui/view/modelcontainer(_:))
- [Apple Developer — modelContainer(for:inMemory:isAutosaveEnabled:isUndoEnabled:onSetup:)](https://developer.apple.com/documentation/swiftui/view/modelcontainer(for:inmemory:isautosaveenabled:isundoenabled:onsetup:))
- [Apple Developer — EnvironmentValues.modelContext](https://developer.apple.com/documentation/swiftui/environmentvalues/modelcontext)
- [Apple Developer — Preserving your app's model data across launches](https://developer.apple.com/documentation/swiftdata/preserving-your-apps-model-data-across-launches)
