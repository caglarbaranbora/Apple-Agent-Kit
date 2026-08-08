# TipKit

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.tipkit
artifact_type: reference
title: TipKit
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's TipKit documentation, scoped to this domain's v1.
domain: TipKit
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/tipkit
https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit
https://developer.apple.com/documentation/tipkit/tip
https://developer.apple.com/documentation/tipkit/tip/action
https://developer.apple.com/documentation/tipkit/tip/actions
https://developer.apple.com/documentation/tipkit/tip/ignoresdisplayfrequency
https://developer.apple.com/documentation/tipkit/tip/image
https://developer.apple.com/documentation/tipkit/tip/invalidate(reason:)
https://developer.apple.com/documentation/tipkit/tip/invalidationreason
https://developer.apple.com/documentation/tipkit/tip/maxdisplaycount
https://developer.apple.com/documentation/tipkit/tip/maxdisplayduration
https://developer.apple.com/documentation/tipkit/tip/message
https://developer.apple.com/documentation/tipkit/tip/option
https://developer.apple.com/documentation/tipkit/tip/options
https://developer.apple.com/documentation/tipkit/tip/rules
https://developer.apple.com/documentation/tipkit/tip/title
https://developer.apple.com/documentation/tipkit/tipgroup
https://developer.apple.com/documentation/tipkit/tipgroup/currenttip
https://developer.apple.com/documentation/tipkit/tipgroup/init(_:_:)
https://developer.apple.com/documentation/tipkit/tipgroup/priority
https://developer.apple.com/documentation/tipkit/tips
https://developer.apple.com/documentation/tipkit/tips/action
https://developer.apple.com/documentation/tipkit/tips/action/init(id:title:perform:)
https://developer.apple.com/documentation/tipkit/tips/configurationoption/cloudkitcontainer(_:)
https://developer.apple.com/documentation/tipkit/tips/configurationoption/datastorelocation(_:)
https://developer.apple.com/documentation/tipkit/tips/configurationoption/displayfrequency(_:)
https://developer.apple.com/documentation/tipkit/tips/configure(_:)
https://developer.apple.com/documentation/tipkit/tips/event
https://developer.apple.com/documentation/tipkit/tips/event/donate()
https://developer.apple.com/documentation/tipkit/tips/event/senddonation(_:)
https://developer.apple.com/documentation/tipkit/tips/invalidationreason
https://developer.apple.com/documentation/tipkit/tips/parameter
https://developer.apple.com/documentation/tipkit/tips/resetdatastore()
https://developer.apple.com/documentation/tipkit/tips/rule
https://developer.apple.com/documentation/tipkit/tips/showalltipsfortesting()
https://developer.apple.com/documentation/tipkit/tips/showtipsfortesting(_:)
https://developer.apple.com/documentation/tipkit/tipuipopoverviewcontroller
https://developer.apple.com/documentation/tipkit/tipuiview
https://developer.apple.com/documentation/tipkit/tipview

## Purpose

Reference index for Apple's TipKit documentation, scoped to this domain's v1: declaring tip content by conforming a `struct` to the `Tip` protocol (`title`, `message`, `image`); controlling when a tip is eligible via the `rules: [Self.Rule]` property built with the `#Rule(_:)` macro over a `Tips.Parameter`-wrapped state variable or a donated `Tips.Event`, noting that all rules on a tip combine with AND logic ("These rules logically AND together in the rules property of the tip structure" — Apple's own TipKit sample-code documentation); configuring the app-wide datastore and display frequency once via `Tips.configure(_:)` before any tip is evaluated ("Call this function during app initialization"); per-tip `Tip.Option`s (`MaxDisplayCount`, `MaxDisplayDuration`, `IgnoresDisplayFrequency`) set via the `options` property; presenting a tip with SwiftUI's `TipView`/`popoverTip(_:arrowEdge:action:)` or UIKit's `TipUIView`/`TipUIPopoverViewController`; grouping tips with `TipGroup` (`.firstAvailable` default vs. `.ordered` priority) so at most one tip in the group displays at a time via `currentTip`; and dismissing a tip programmatically with `invalidate(reason:)` and `Tip.InvalidationReason` (`.actionPerformed`, `.displayCountExceeded`, `.displayDurationExceeded`, `.tipClosed`).

Out of scope for v1: authoring a custom `TipViewStyle` beyond the system default; watchOS-specific TipKit presentation differences; and CloudKit sync of the tip datastore across a person's devices. On that last point specifically — verified directly against Apple's `Tips.ConfigurationOption.cloudKitContainer(_:)` documentation — TipKit's datastore is local-only **only by default**: "By default, TipKit's datastore does not sync with CloudKit," but cross-device sync is a real, documented, opt-in capability ("Use `cloudKitContainer(_:)` to sync TipKit's datastore across devices," requiring the iCloud and Background Modes entitlement capabilities). v1 covers only the default, local-only datastore; `cloudKitContainer(_:)` itself is not covered by any Knowledge Contract in this domain.

## Primary Topics

- Tip declaration: the `Tip` protocol's required `title` and optional `message`/`image`/`actions`
- Display rules and event triggers: `#Rule(_:)`, `Tips.Parameter`, `Tips.Event`, AND-combination
- App configuration: `Tips.configure(_:)` ordering, datastore location, display frequency, per-tip options
- Presentation: `TipView`/`TipUIView`/`TipUIPopoverViewController`, `TipGroup`, invalidation

## Used By

- knowledge/tipkit/tip-declaration-and-content.md ([[knowledge/tipkit/tip-declaration-and-content]])
- knowledge/tipkit/display-rules-and-event-triggers.md ([[knowledge/tipkit/display-rules-and-event-triggers]])
- knowledge/tipkit/tip-options-and-app-configuration.md ([[knowledge/tipkit/tip-options-and-app-configuration]])
- knowledge/tipkit/presenting-tips-and-tip-groups.md ([[knowledge/tipkit/presenting-tips-and-tip-groups]])
