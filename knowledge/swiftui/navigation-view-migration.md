# Navigation View Migration

Status: Draft
Version: 0.1.0

## Metadata

``` yaml
id: knowledge.swiftui.navigation-view-migration
artifact_type: knowledge
title: Navigation View Migration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines how existing deprecated NavigationView code is migrated to NavigationStack and NavigationSplitView -- the platform floor, choosing the replacement from the view's column count rather than preference, the iPhone/iPad adaptive case that must become NavigationSplitView and not NavigationStack, converting isActive: NavigationLinks to a path-driven stack and tag:selection: links to List selection, and the availability-gated wrapper Apple documents for deployment targets below the floor.
domain: SwiftUI
tags:
  - swiftui
  - navigation
  - migration
  - navigationview
  - deprecation
references:
  - https://developer.apple.com/documentation/swiftui/migrating-to-new-navigation-types
  - https://developer.apple.com/documentation/swiftui/navigationview
  - https://developer.apple.com/documentation/swiftui/navigationstack
  - https://developer.apple.com/documentation/swiftui/navigationsplitview
  - https://developer.apple.com/documentation/swiftui/navigationlink
depends_on:
  - knowledge.swiftui.navigation-stack
  - knowledge.swiftui.navigation-split-view
related:
  - knowledge.swiftui.observable-object-migration
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent converts *existing* `NavigationView` code to the containers that replace it. `navigation-stack` and `navigation-split-view` own what the result must look like; this contract owns the choice between them and the mechanical conversion. Its central claim is that the replacement is determined by what the old view actually displayed, not by which container is simpler — and that picking wrong produces code which compiles and looks correct on one device class.

## Scope

### Included

- The platform floor for `NavigationStack`/`NavigationSplitView`, and what to do below it
- Choosing the replacement from the `NavigationView`'s column count and style
- Converting `isActive:` and `tag:selection:` `NavigationLink` forms
- Apple's availability-gated wrapper for pre-floor deployment targets

### Excluded

- How `NavigationStack`, `NavigationPath`, and `.navigationDestination(for:)` are used in new code -- owned by `navigation-stack`
- `NavigationSplitView` column-count, selection, and composition rules -- owned by `navigation-split-view`
- `ObservableObject` migration -- see `observable-object-migration`; different platform floor, separate task

## Rules

### Rule 1

Agents MUST confirm the deployment target reaches the navigation floor before migrating. Per Apple's documentation, transition away from `NavigationView` if the app "has a minimum deployment target of iOS 16, iPadOS 16, macOS 13, tvOS 16, watchOS 9, or visionOS 1, or later." This floor is one major version below the Observation floor in `observable-object-migration` Rule 1, so a target may permit one migration and not the other; agents MUST NOT treat the two as a single upgrade.

### Rule 2

Agents MUST choose the replacement from what the `NavigationView` displayed, not from which container is easier to write. Per Apple's documentation: "How you use these depends on whether you perform navigation in one column or across multiple columns." A `NavigationView` styled `.navigationViewStyle(.stack)` becomes a `NavigationStack`; a two- or three-column `NavigationView` becomes a `NavigationSplitView` built with `init(sidebar:detail:)` or `init(sidebar:content:detail:)` respectively.

### Rule 3

Agents MUST convert a `NavigationView` that shows multiple columns on some devices and one column on others to `NavigationSplitView`, never to `NavigationStack`. Apple names this case directly: "for apps that have multiple columns in some cases and a single column in others — which is typical for apps that run on iPhone and iPad — switch to `NavigationSplitView`." A `NavigationStack` substituted here compiles, and on iPhone it is indistinguishable from correct; what is lost is the iPad layout, on a device the agent is least likely to be running.

### Rule 4

Agents MUST convert `NavigationLink` initializers taking `isActive:` by moving the automation to the enclosing stack, not by preserving one boolean per destination. Per Apple's documentation: "move the automation to the enclosing stack. Do this by changing your navigation links to use the `init(value:label:)` initializer, then use one of the navigation stack initializers that takes a path input." The per-destination `@State` booleans are deleted, and `navigation-stack` Rules 2 and 3 govern the resulting path and `.navigationDestination(for:)` declarations.

### Rule 5

Agents MUST convert `NavigationLink` initializers taking `tag:selection:` by moving selection onto the `List`, not onto each link. Per Apple's documentation, "you can move the selection to the list" — `List(data, id:, selection: $selection)` inside a `NavigationSplitView`, with links reduced to `init(value:label:)`. The single selection state that results is `navigation-split-view` Rule 2's requirement, and the detail column reads it directly.

### Rule 6

Agents MUST NOT report the migration as blocked by a deployment target below Rule 1's floor. Per Apple's documentation, an app that "needs to run on platform versions earlier than iOS 16, iPadOS 16, macOS 13, tvOS 16, watchOS 9, or visionOS 1" can "start migration while continuing to support older clients" through a custom wrapper view that branches on `#available` and uses `NavigationSplitView` on the new path and `NavigationView` on the old. Agents SHOULD offer that wrapper rather than leaving unmigrated `NavigationView` code with no path forward.

## Compliant Example

```swift
// BEFORE: two-column NavigationView, selection driven per link.
// AFTER: NavigationSplitView, selection on the List (Rules 2, 3, 5).
@State private var selection: Color?

var body: some View {
    NavigationSplitView {
        List(colors, id: \.self, selection: $selection) { color in
            NavigationLink(color.description, value: color)
        }
    } detail: {
        if let selection { ColorDetail(color: selection) }
        else { Text("Pick a color") }
    }
}
```

```swift
// BEFORE: NavigationView(.stack) with isActive: booleans.
// AFTER: path-driven NavigationStack; the booleans are deleted (Rule 4).
@State private var path: [Color] = []

var body: some View {
    NavigationStack(path: $path) {
        List { NavigationLink("Purple", value: Color.purple) }
            .navigationDestination(for: Color.self) { ColorDetail(color: $0) }
    }
}
```

## Non-Compliant Example

```swift
// The original was a two-column NavigationView adapting to one column on iPhone.
NavigationStack {
    List(colors, id: \.self) { color in
        NavigationLink(color.description, value: color)
    }
    .navigationDestination(for: Color.self) { ColorDetail(color: $0) }
}
```
Chosen because the app was tested on iPhone, where a `NavigationStack` and a collapsed `NavigationSplitView` look the same. The build is clean and the iPhone behavior is correct; the sidebar–detail layout the app had on iPad is gone, with nothing reporting it (Rules 2, 3).

## Dependencies

- `navigation-stack` -- owns `NavigationStack`, `NavigationPath`, and `.navigationDestination(for:)`, the target shape of a single-column migration.
- `navigation-split-view` -- owns column-count choice, selection binding, and stack composition, the target shape of a multi-column migration.

## References

- [Apple Developer — Migrating to new navigation types](https://developer.apple.com/documentation/swiftui/migrating-to-new-navigation-types)
- [Apple Developer — NavigationView](https://developer.apple.com/documentation/swiftui/navigationview)
- [Apple Developer — NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)
- [Apple Developer — NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)
- [Apple Developer — NavigationLink](https://developer.apple.com/documentation/swiftui/navigationlink)
