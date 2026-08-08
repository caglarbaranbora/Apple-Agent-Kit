# Table View Diffable Data Source

Status: Draft Version: 0.2.0

## Metadata

``` yaml
id: knowledge.uikit.table-view-diffable
artifact_type: knowledge
title: Table View Diffable Data Source
version: 0.2.0
status: Draft
owner: Apple Agent Kit
summary: Defines use of UITableViewDiffableDataSource and NSDiffableDataSourceSnapshot to drive a UITableView's content from applied snapshots instead of manual reloadData or index-path bookkeeping.
domain: UIKit
tags:
  - uikit
  - table-view
  - diffable-data-source
references:
  - https://developer.apple.com/documentation/uikit/uitableviewdiffabledatasource-2euir
  - https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot-swift.struct
depends_on: []
related:
  - knowledge.uikit.cell-configuration
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent drives a `UITableView`'s
rows from a `UITableViewDiffableDataSource` and applied snapshot, so row
insert/delete/reorder animations are computed automatically instead of
hand-managed index paths.

## Scope

### Included

-   Constructing `UITableViewDiffableDataSource` with a cell provider
-   Building and applying `NSDiffableDataSourceSnapshot` (sections and items)
-   `animatingDifferences` on apply

### Excluded

-   Cell dequeue/registration mechanics — see `cell-configuration`
-   Classic `UITableViewDataSource` `cellForRowAt` pattern — permanently out of scope for this domain

## Rules

### Rule 1

Agents MUST drive a `UITableView`'s content through
`UITableViewDiffableDataSource` and `NSDiffableDataSourceSnapshot` rather
than implementing `UITableViewDataSource`'s `cellForRowAt`/
`numberOfRowsInSection` directly — the diffable data source computes
correct insert/delete/move animations from snapshot differences
automatically, which manual `reloadData()` cannot do.

### Rule 2

Agents MUST build a complete `NSDiffableDataSourceSnapshot` (append all
sections, then append all items per section) and apply it via
`dataSource.apply(snapshot, animatingDifferences:)` rather than mutating
the table view's rows directly — the snapshot is the single source of
truth the diffable data source diffs against.

### Rule 3

Agents MUST assign the constructed `UITableViewDiffableDataSource` to the
table view's `dataSource` property and retain a strong reference to it on
the owning view controller — `UITableView.dataSource` is a weak
reference, so a data source with no other owner is deallocated
immediately and rows silently stop appearing.

### Rule 4

Agents SHOULD pass `animatingDifferences: false` only for the first
snapshot applied after the table view loads — animating the initial
population produces an unwanted animation of rows appearing from
nothing; subsequent updates should animate (`true`) so changes are
visible to the user.

## Compliant Example

```swift
enum Section { case main }

final class InboxViewController: UIViewController {
    private let tableView = UITableView()
    private var dataSource: UITableViewDiffableDataSource<Section, Message>!

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(tableView)
        NSLayoutConstraint.activate([
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ])
        dataSource = UITableViewDiffableDataSource<Section, Message>(tableView: tableView) { tableView, indexPath, message in
            let cell = tableView.dequeueReusableCell(withIdentifier: "MessageCell", for: indexPath)
            cell.textLabel?.text = message.subject
            return cell
        }
        applySnapshot(animatingDifferences: false)
    }

    func applySnapshot(animatingDifferences: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Message>()
        snapshot.appendSections([.main])
        snapshot.appendItems(messages, toSection: .main)
        dataSource.apply(snapshot, animatingDifferences: animatingDifferences)
    }
}
```
Diffable data source retained as a stored property, snapshot built and applied, first population unanimated. (Rules 1, 2, 3, 4)

## Non-Compliant Example

```swift
final class InboxViewController: UIViewController, UITableViewDataSource {
    private let tableView = UITableView()

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        messages.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "MessageCell", for: indexPath)
        cell.textLabel?.text = messages[indexPath.row].subject
        return cell
    }
}
```
Classic `UITableViewDataSource` implementation — any row change requires a manual `reloadData()` with no automatic diff-based animation. (Rule 1)

## Dependencies

None.

## References

-   [Apple Developer — UITableViewDiffableDataSource](https://developer.apple.com/documentation/uikit/uitableviewdiffabledatasource-2euir)
-   [Apple Developer — NSDiffableDataSourceSnapshot](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshot-swift.struct)
