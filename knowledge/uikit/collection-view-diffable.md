# Collection View Diffable Data Source

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.uikit.collection-view-diffable
artifact_type: knowledge
title: Collection View Diffable Data Source
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines use of UICollectionViewDiffableDataSource and NSDiffableDataSourceSnapshot to bind data to a collection view built with UICollectionViewCompositionalLayout.
domain: UIKit
tags:
  - uikit
  - collection-view
  - diffable-data-source
references:
  - https://developer.apple.com/documentation/uikit/uicollectionviewdiffabledatasource-9tqpa
  - https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot-swift.struct
depends_on: []
related:
  - knowledge.uikit.collection-view-compositional-layout
  - knowledge.uikit.cell-configuration
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent binds data to a collection
view via `UICollectionViewDiffableDataSource` and an applied snapshot,
mirroring `table-view-diffable`'s split between layout structure
(`collection-view-compositional-layout`) and data binding (this
contract).

## Scope

### Included

-   Constructing `UICollectionViewDiffableDataSource` with a cell provider
-   Building and applying `NSDiffableDataSourceSnapshot` (sections and items)
-   Reloading vs. reconfiguring items on data change

### Excluded

-   Layout structure (item/group/section sizing) — see `collection-view-compositional-layout`
-   Cell registration mechanics — see `cell-configuration`

## Rules

### Rule 1

Agents MUST bind a `UICollectionView`'s content through
`UICollectionViewDiffableDataSource` and `NSDiffableDataSourceSnapshot`,
not `UICollectionViewDataSource`'s `cellForItemAt`/
`numberOfItemsInSection` — same rationale as `table-view-diffable`:
correct insert/delete/move animations computed from snapshot diffs.

### Rule 2

Agents MUST retain a strong reference to the constructed
`UICollectionViewDiffableDataSource` on the owning view controller —
`UICollectionView.dataSource` is a weak reference; an unretained data
source is deallocated immediately and the collection view renders empty.

### Rule 3

Agents MUST use `snapshot.reconfigureItems([...])` (not `reloadItems`)
when only an existing item's *content* changed and its identity is
unchanged — `reconfigureItems` updates the cell in place, while
`reloadItems` triggers a full dequeue/configure cycle and a visible
reload animation even when the item didn't move.

### Rule 4

Agents MUST ensure the item type used as the snapshot's item identifier
conforms to `Hashable` with a stable identity (a model's unique ID, not a
value that changes when unrelated fields update) — the diffable data
source uses this identity to compute which items are the "same" item
across snapshots; an unstable identity produces spurious insert/delete
pairs instead of in-place updates.

## Compliant Example

```swift
enum Section { case main }

final class GalleryViewController: UIViewController {
    private var collectionView: UICollectionView!
    private var dataSource: UICollectionViewDiffableDataSource<Section, Photo>!

    override func viewDidLoad() {
        super.viewDidLoad()
        dataSource = UICollectionViewDiffableDataSource<Section, Photo>(collectionView: collectionView) { collectionView, indexPath, photo in
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "PhotoCell", for: indexPath) as! PhotoCell
            cell.configure(with: photo)
            return cell
        }
        applySnapshot(animatingDifferences: false)
    }

    func applySnapshot(animatingDifferences: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Photo>()
        snapshot.appendSections([.main])
        snapshot.appendItems(photos, toSection: .main)
        dataSource.apply(snapshot, animatingDifferences: animatingDifferences)
    }
}
```
Diffable data source retained as a stored property; `Photo` provides stable `Hashable` identity via its unique ID. (Rules 1, 2, 4)

## Non-Compliant Example

```swift
func updateCaption(for photo: Photo) {
    var snapshot = dataSource.snapshot()
    snapshot.reloadItems([photo])
    dataSource.apply(snapshot)
}
```
Uses `reloadItems` for an in-place content-only change — triggers a full dequeue/configure and reload animation when `reconfigureItems` would update the existing cell in place. (Rule 3)

## Dependencies

None.

## References

-   [Apple Developer — UICollectionViewDiffableDataSource](https://developer.apple.com/documentation/uikit/uicollectionviewdiffabledatasource-9tqpa)
-   [Apple Developer — NSDiffableDataSourceSnapshot](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot-swift.struct)
