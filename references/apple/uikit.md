# UIKit

Status: Draft
Version: 0.2.0

## Metadata

``` yaml
id: reference.apple.uikit
artifact_type: reference
title: UIKit
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Reference index for Apple's UIKit screen-scaffolding documentation behind skill.uikit.foundations -- view controller lifecycle and containment, programmatic Auto Layout (anchors, constraints, stack views, safe area and layout margins), navigation and modal presentation, and the diffable table and collection view data sources with compositional layout and cell registration.
domain: UIKit
last_updated: 2026-08-08
```

## Source

https://developer.apple.com/documentation/uikit/nscollectionlayoutgroup
https://developer.apple.com/documentation/uikit/nscollectionlayoutitem
https://developer.apple.com/documentation/uikit/nscollectionlayoutsection
https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot-swift.struct
https://developer.apple.com/documentation/uikit/nslayoutanchor
https://developer.apple.com/documentation/uikit/nslayoutconstraint
https://developer.apple.com/documentation/uikit/uicollectionview/cellregistration
https://developer.apple.com/documentation/uikit/uicollectionviewcompositionallayout
https://developer.apple.com/documentation/uikit/uicollectionviewdiffabledatasource-9tqpa
https://developer.apple.com/documentation/uikit/uimodalpresentationstyle
https://developer.apple.com/documentation/uikit/uinavigationcontroller
https://developer.apple.com/documentation/uikit/uistackview
https://developer.apple.com/documentation/uikit/uistackview/alignment-swift.property
https://developer.apple.com/documentation/uikit/uistackview/distribution-swift.property
https://developer.apple.com/documentation/uikit/uitabbarcontroller
https://developer.apple.com/documentation/uikit/uitableview/register(_:forcellreuseidentifier:)-3l3ct
https://developer.apple.com/documentation/uikit/uitableviewcell/prepareforreuse()
https://developer.apple.com/documentation/uikit/uitableviewdiffabledatasource-2euir
https://developer.apple.com/documentation/uikit/uiview/layoutmarginsguide
https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide
https://developer.apple.com/documentation/uikit/uiview/translatesautoresizingmaskintoconstraints
https://developer.apple.com/documentation/uikit/uiviewcontroller/addchild(_:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/didmove(toparent:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/dismiss(animated:completion:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/navigationitem
https://developer.apple.com/documentation/uikit/uiviewcontroller/present(_:animated:completion:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/removefromparent()
https://developer.apple.com/documentation/uikit/uiviewcontroller/tabbaritem
https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidappear(_:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdiddisappear(_:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/viewdidload()
https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwillappear(_:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwilldisappear(_:)
https://developer.apple.com/documentation/uikit/uiviewcontroller/willmove(toparent:)

## Purpose

Reference index for the Apple UIKit documentation behind
`skill.uikit.foundations`: how a screen is built. Scope is programmatic UI
(no Storyboard/XIB) and diffable data sources (no classic `cellForRowAt`).
What a built screen then does — gestures, Core Animation, custom and
interactive transitions, SwiftUI interop — is indexed by
`reference.apple.uikit-interaction`; these 34 sources fill this file to its
98-line cap, which is why that surface is a second Skill and a second
Reference rather than an extension of this one. Accessibility API
implementation is owned by `accessibility` and design-level guidance by
`human-interface-guidelines` — see docs/architecture/domain-map.md.

## Primary Topics

- View controller lifecycle callbacks and containment
- Auto Layout: anchors, constraints, autoresizing-mask translation
- Stack views: alignment and distribution
- Safe area and layout margin guides
- Navigation and tab bar containers, and their per-controller items
- Modal presentation and dismissal
- Diffable data sources and snapshots for tables and collections
- Compositional layout, cell registration, and reuse

## Used By

- knowledge/uikit/view-controller-lifecycle.md ([[knowledge/uikit/view-controller-lifecycle]])
- knowledge/uikit/view-controller-composition.md ([[knowledge/uikit/view-controller-composition]])
- knowledge/uikit/auto-layout-constraints.md ([[knowledge/uikit/auto-layout-constraints]])
- knowledge/uikit/auto-layout-stack-views.md ([[knowledge/uikit/auto-layout-stack-views]])
- knowledge/uikit/safe-area-and-layout-guides.md ([[knowledge/uikit/safe-area-and-layout-guides]])
- knowledge/uikit/navigation-controller.md ([[knowledge/uikit/navigation-controller]])
- knowledge/uikit/tab-bar-controller.md ([[knowledge/uikit/tab-bar-controller]])
- knowledge/uikit/table-view-diffable.md ([[knowledge/uikit/table-view-diffable]])
- knowledge/uikit/collection-view-compositional-layout.md ([[knowledge/uikit/collection-view-compositional-layout]])
- knowledge/uikit/collection-view-diffable.md ([[knowledge/uikit/collection-view-diffable]])
- knowledge/uikit/cell-configuration.md ([[knowledge/uikit/cell-configuration]])
- knowledge/uikit/modal-presentation.md ([[knowledge/uikit/modal-presentation]])
- knowledge/uikit/swiftui-hosting-controller.md ([[knowledge/uikit/swiftui-hosting-controller]])
