# Widget Interactivity and Deep Links

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.widgetkit.widget-interactivity-and-deep-links
type: knowledge
title: Widget Interactivity and Deep Links
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines whole-widget navigation via widgetURL(_:), per-region navigation via Link, wiring an already-authored AppIntent into Button(intent:)/Toggle(_:isOn:intent:), and routing a deep-link URL's identifying data in the app.
domain: WidgetKit
tags:
  - widgetkit
  - widgeturl
  - link
  - button-intent
  - toggle-intent
references:
  - https://developer.apple.com/documentation/swiftui/view/widgeturl(_:)
  - https://developer.apple.com/documentation/swiftui/link
  - https://developer.apple.com/documentation/swiftui/button/init(_:intent:)
  - https://developer.apple.com/documentation/swiftui/toggle/init(_:ison:intent:)
  - https://developer.apple.com/documentation/widgetkit/linking-to-specific-app-scenes-from-your-widget-or-live-activity
  - https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities
depends_on:
  - knowledge.widgetkit.widget-declaration-and-families
related: []
updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent wires navigation and interaction into a widget's view: whole-widget taps via `widgetURL(_:)`, per-region taps via `Link`, and in-place actions via `Button(intent:)`/`Toggle(_:isOn:intent:)` bound to an already-authored `AppIntent` — the interaction surface of a widget, layered on top of the declaration covered in `widget-declaration-and-families`.

## Scope

### Included

-   Whole-widget navigation via `.widgetURL(_:)` on the root view
-   Per-region navigation via `Link(destination:)` in families with multiple tap targets
-   Wiring an already-authored `AppIntent` into `Button(intent:)`/`Toggle(_:isOn:intent:)`
-   Carrying identifying data in a deep-link URL for the app to route on

### Excluded

-   Authoring the `AppIntent` itself — its parameters, `perform()` body, entities — deferred to the future `app-intents` domain; this contract only covers wiring an already-authored intent into a widget's tap target
-   Declaring the `Widget`/families the interactive view belongs to — see `widget-declaration-and-families`
-   `TimelineProvider`/`TimelineEntry` — see `timeline-provider-and-entries`
-   Handling the deep-link URL inside the app's `onOpenURL`/scene delegate once received — app-side, not this domain

## Rules

### Rule 1

Agents MUST use `.widgetURL(_:)` (`func widgetURL(_ url: URL?) -> some View`) on the widget's root view for whole-widget tap navigation into the app, and MUST apply it at most once per view hierarchy. Per Apple's documentation, "Widgets support one `widgetURL` modifier in their view hierarchy. If multiple views have `widgetURL` modifiers, the behavior is undefined" — agents MUST NOT rely on a second `widgetURL` being safely ignored.

### Rule 2

Agents MUST use one or more `Link(destination:)` controls, in addition to a single `widgetURL`, when a widget needs more than one distinct tappable region — Apple's documentation names `accessoryRectangular`, `systemSmall`, and larger families as having "enough space for more than one interaction target." Per Apple's documentation, "If an interaction targets a `Link` control, the system uses the URL in that control. For interactions anywhere else in the widget, the system uses the URL you specify in the `widgetURL(_:)` view modifier" — agents MUST NOT assume a `Link` inside a widget behaves identically to a plain in-app `Link`; its role is strictly to override the tap target's destination within `widgetURL`'s fallback area.

### Rule 3

Agents MUST use `Button(intent:)` (e.g. `init(_:intent:)`) or `Toggle(_:isOn:intent:)`/`Toggle(isOn:intent:label:)` bound to a type conforming to `AppIntent` (or `AudioPlaybackIntent`, `LiveActivityIntent`, etc., when the action must run in the app's process) for interactive elements inside a widget, and MUST NOT use a plain `Button(action:)` closure. Per Apple's documentation, widget code "runs in an independent process that's separate from your app," and the system "can't run your code or update data bindings at the time it renders your widget" — a `Button(action:)` closure has no running app code to invoke and silently no-ops. Authoring the bound `AppIntent`'s `perform()` itself is out of scope here (see Excluded).

### Rule 4

Agents MUST encode enough identifying data (e.g. an item ID, not just a bare app-root URL) in a `widgetURL`/`Link` destination for the app to route directly to that content on launch, and MUST have the app read that URL in its `onOpenURL`/scene-delegate handling — not inside the widget extension, which has no view of the app's navigation state. Per Apple's documentation, "the system activates the containing app and passes the URL to `onOpenURL(perform:)`" (or the corresponding `UIApplicationDelegate`/`NSApplicationDelegate` callback) — the widget's only job is to produce a URL that identifies the content, not to perform the navigation itself.

## Compliant Example

```swift
struct TodoItemView: View {
    var todo: Todo

    var body: some View {
        Toggle(isOn: todo.isComplete, intent: ToggleTodoIntent(id: todo.id)) {
            Text(todo.title)
        }
    }
}

struct TodoListWidgetView: View {
    var entry: TodoListEntry

    var body: some View {
        VStack(alignment: .leading) {
            ForEach(entry.todos) { todo in
                Link(destination: URL(string: "myapp://todo/\(todo.id)")!) {
                    TodoItemView(todo: todo)
                }
            }
        }
        .widgetURL(URL(string: "myapp://todos")!) // Exactly one, for taps outside any Link.
    }
}
```
Uses `Toggle(isOn:intent:)` bound to an already-authored `ToggleTodoIntent` rather than a plain action closure (Rule 3), gives each row its own `Link` carrying the item's `id` while the container declares exactly one `widgetURL` (Rules 1, 2), and both destinations carry an identifying ID for the app to route on (Rule 4). (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
struct TodoItemView: View {
    var todo: Todo

    var body: some View {
        HStack {
            Text(todo.title)
            Button(action: { todo.isComplete.toggle() }) { // No running app code -- silently no-ops.
                Image(systemName: todo.isComplete ? "checkmark.circle.fill" : "circle")
            }
        }
    }
}

struct TodoListWidgetView: View {
    var entry: TodoListEntry

    var body: some View {
        VStack {
            ForEach(entry.todos) { todo in TodoItemView(todo: todo) }
        }
        .widgetURL(URL(string: "myapp://todos")!)
        .onTapGesture { }
        .widgetURL(URL(string: "myapp://home")!) // A second widgetURL -- behavior is undefined.
    }
}
```
Uses a plain `Button(action:)` closure instead of `Button(intent:)`/`Toggle(_:isOn:intent:)` (Rule 3), and applies two conflicting `widgetURL` modifiers to the same hierarchy instead of exactly one (Rule 1); the row destinations also carry no per-item identifying data (Rule 4).

## Dependencies

-   `knowledge.widgetkit.widget-declaration-and-families` — this contract adds interactivity to the widget view declared there; it does not define the `Widget`/`WidgetConfiguration` itself.

## References

-   [Apple Developer — View.widgetURL(_:)](https://developer.apple.com/documentation/swiftui/view/widgeturl(_:))
-   [Apple Developer — Link](https://developer.apple.com/documentation/swiftui/link)
-   [Apple Developer — Button.init(_:intent:)](https://developer.apple.com/documentation/swiftui/button/init(_:intent:))
-   [Apple Developer — Toggle.init(_:isOn:intent:)](https://developer.apple.com/documentation/swiftui/toggle/init(_:ison:intent:))
-   [Apple Developer — Linking to specific app scenes from your widget or Live Activity](https://developer.apple.com/documentation/widgetkit/linking-to-specific-app-scenes-from-your-widget-or-live-activity)
-   [Apple Developer — Adding interactivity to widgets and Live Activities](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities)
