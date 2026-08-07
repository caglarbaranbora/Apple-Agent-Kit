# Collection View Compositional Layout

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.uikit.collection-view-compositional-layout
artifact_type: knowledge
title: Collection View Compositional Layout
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines composing UICollectionViewCompositionalLayout from NSCollectionLayoutItem, NSCollectionLayoutGroup, and NSCollectionLayoutSection to describe a collection view's visual arrangement.
domain: UIKit
tags:
  - uikit
  - collection-view
  - compositional-layout
references:
  - https://developer.apple.com/documentation/uikit/uicollectionviewcompositionallayout
  - https://developer.apple.com/documentation/uikit/nscollectionlayoutsection
  - https://developer.apple.com/documentation/uikit/nscollectionlayoutgroup
  - https://developer.apple.com/documentation/uikit/nscollectionlayoutitem
depends_on: []
related:
  - knowledge.uikit.cell-configuration
  - knowledge.uikit.collection-view-diffable
last_updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent builds a
`UICollectionViewCompositionalLayout` by composing item, group, and
section, so a collection view's grid/list/multi-column arrangement is
declared structurally instead of via manual `UICollectionViewLayout`
subclassing.

## Scope

### Included

-   `NSCollectionLayoutItem` sizing (estimated/absolute/fractional dimensions)
-   `NSCollectionLayoutGroup` horizontal/vertical composition
-   `NSCollectionLayoutSection` assembly, `interGroupSpacing`, `contentInsets`

### Excluded

-   Binding data to the layout — see `collection-view-diffable`
-   Cell registration — see `cell-configuration`

## Rules

### Rule 1

Agents MUST build collection view layouts with
`UICollectionViewCompositionalLayout` (item → group → section) rather
than subclassing `UICollectionViewLayout` or using the legacy
`UICollectionViewFlowLayout` for any new v1 screen — compositional layout
expresses nested/multi-column arrangements declaratively without manual
`layoutAttributesForElements` overrides.

### Rule 2

Agents MUST use `.fractionalWidth`/`.fractionalHeight` dimensions for
items/groups that should scale with the collection view's own size (for
example, "half the section width") rather than `.absolute` — absolute
dimensions don't adapt across device sizes or size classes.

### Rule 3

Agents MUST set `NSCollectionLayoutSection.contentInsets` and
`interGroupSpacing` explicitly on every section rather than relying on
layout defaults — the system defaults produce zero spacing, which
usually isn't the intended visual result.

### Rule 4

Agents SHOULD compose nested groups (a horizontal group of vertical
groups, or vice versa) for multi-column/grid arrangements rather than
falling back to a single flat group — nesting is how compositional
layout expresses two-dimensional arrangements.

## Compliant Example

```swift
func makeLayout() -> UICollectionViewCompositionalLayout {
    let itemSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .fractionalHeight(1.0))
    let item = NSCollectionLayoutItem(layoutSize: itemSize)

    let groupSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(0.5), heightDimension: .absolute(120))
    let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

    let section = NSCollectionLayoutSection(group: group)
    section.contentInsets = NSDirectionalEdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16)
    section.interGroupSpacing = 12

    return UICollectionViewCompositionalLayout(section: section)
}
```
Fractional item/group sizing for a two-column grid, explicit content insets and inter-group spacing. (Rules 1, 2, 3)

## Non-Compliant Example

```swift
let layout = UICollectionViewFlowLayout()
layout.itemSize = CGSize(width: 160, height: 120)
collectionView.collectionViewLayout = layout
```
Legacy `UICollectionViewFlowLayout` with an absolute item size that won't adapt across device widths, instead of a compositional layout with fractional sizing. (Rules 1, 2)

## Dependencies

None.

## References

-   [Apple Developer — UICollectionViewCompositionalLayout](https://developer.apple.com/documentation/uikit/uicollectionviewcompositionallayout)
-   [Apple Developer — NSCollectionLayoutSection](https://developer.apple.com/documentation/uikit/nscollectionlayoutsection)
-   [Apple Developer — NSCollectionLayoutGroup](https://developer.apple.com/documentation/uikit/nscollectionlayoutgroup)
-   [Apple Developer — NSCollectionLayoutItem](https://developer.apple.com/documentation/uikit/nscollectionlayoutitem)
