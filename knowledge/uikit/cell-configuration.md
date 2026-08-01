# Cell Configuration

Status: Draft Version: 0.1.0

## Metadata

```yaml
id: knowledge.uikit.cell-configuration
type: knowledge
title: Cell Configuration
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UICollectionView.CellRegistration and UITableView cell registration, reuse identifiers, and prepareForReuse to configure reusable table and collection view cells correctly.
domain: UIKit
tags:
  - uikit
  - cell
  - reuse
references:
  - https://developer.apple.com/documentation/uikit/uicollectionview/cellregistration
  - https://developer.apple.com/documentation/uikit/uitableview/register(_:forcellreuseidentifier:)
  - https://developer.apple.com/documentation/uikit/uitableviewcell/prepareforreuse()
depends_on: []
related:
  - knowledge.uikit.table-view-diffable
  - knowledge.uikit.collection-view-diffable
  - knowledge.accessibility.accessibility-labels
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent registers and configures
reusable table and collection view cells so recycled cells never leak
stale content from a previous item. Accessibility properties on a cell's
content are cross-referenced to the `accessibility` domain, not
duplicated here.

## Scope

### Included

-   `UICollectionView.CellRegistration` typed cell registration
-   `UITableView.register(_:forCellReuseIdentifier:)` and `dequeueReusableCell`
-   Resetting per-item state in `prepareForReuse()`

### Excluded

-   Accessibility labeling of cell content — see `knowledge.accessibility.accessibility-labels`
-   Data binding / snapshot apply — see `table-view-diffable`, `collection-view-diffable`

## Rules

### Rule 1

Agents MUST register cell classes/reuse identifiers before the table or
collection view attempts to dequeue them —
`UICollectionView.CellRegistration` (used with
`dequeueConfiguredReusableCell(using:for:item:)`) or
`UITableView.register(_:forCellReuseIdentifier:)`, done once (typically
in `viewDidLoad`), not per-dequeue.

### Rule 2

Agents SHOULD prefer `UICollectionView.CellRegistration` over a raw
string reuse identifier plus a forced downcast when constructing a
collection view's cell provider — `CellRegistration` is generic over the
concrete cell type, so the compiler catches a mismatched cell type
instead of a runtime crash on `as!`.

### Rule 3

Agents MUST reset any per-item mutable state that isn't overwritten
unconditionally by the next configuration (an image loaded
asynchronously, a highlight/selection flag) in `prepareForReuse()` —
reused cells retain their previous subview state unless explicitly
cleared, so a slow image load for item A can visually appear on a
recycled cell now showing item B.

### Rule 4

Agents MUST configure every visible property of a cell unconditionally
from the current item's data on every dequeue, not just properties that
differ from some assumed default — a cell instance is reused across
arbitrary prior items, so any property set conditionally (only when a
flag is true) can carry over stale state from a previous item when the
condition is now false.

## Compliant Example

```swift
final class PhotoCell: UICollectionViewCell {
    let imageView = UIImageView()
    private var loadTask: Task<Void, Never>?

    func configure(with photo: Photo) {
        loadTask?.cancel()
        imageView.image = nil
        loadTask = Task {
            let image = await ImageLoader.load(photo.url)
            if !Task.isCancelled { imageView.image = image }
        }
    }

    override func prepareForReuse() {
        super.prepareForReuse()
        loadTask?.cancel()
        imageView.image = nil
    }
}

let registration = UICollectionView.CellRegistration<PhotoCell, Photo> { cell, indexPath, photo in
    cell.configure(with: photo)
}
```
Typed `CellRegistration`, unconditional per-item configuration, in-flight async load cancelled and image cleared in `prepareForReuse()`. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
final class PhotoCell: UICollectionViewCell {
    let imageView = UIImageView()

    func configure(with photo: Photo) {
        if photo.hasCustomImage {
            imageView.image = photo.thumbnail
        }
    }
}
```
No `prepareForReuse()` reset and conditional configuration — a recycled cell that previously showed a custom image keeps showing it when the new item's `hasCustomImage` is `false`. (Rules 3, 4)

## Dependencies

None.

## References

-   [Apple Developer — UICollectionView.CellRegistration](https://developer.apple.com/documentation/uikit/uicollectionview/cellregistration)
-   [Apple Developer — register(_:forCellReuseIdentifier:)](https://developer.apple.com/documentation/uikit/uitableview/register(_:forcellreuseidentifier:))
-   [Apple Developer — prepareForReuse()](https://developer.apple.com/documentation/uikit/uitableviewcell/prepareforreuse())
