# FileManager App Sandbox Directories

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.foundation.filemanager-app-sandbox-directories
artifact_type: knowledge
title: FileManager App Sandbox Directories
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of FileManager.urls(for:in:) to locate Documents/Caches/Application Support, safe file read/write, and isExcludedFromBackup for cache-type data.
domain: Foundation
tags:
  - foundation
  - filemanager
  - sandbox
  - backup
references:
  - https://developer.apple.com/documentation/foundation/filemanager
  - https://developer.apple.com/documentation/foundation/using-the-file-system-effectively
  - https://developer.apple.com/documentation/foundation/urlresourcevalues/isexcludedfrombackup
depends_on: []
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent locates the correct app
sandbox directory for a given kind of file (`Documents`, `Caches`,
`Application Support`) via `FileManager.default.urls(for:in:)`, reads and
writes files safely, and marks regenerable cache data as excluded from
backup — avoiding the common correctness mistake of bloating iCloud/iTunes
backups with data the app can simply regenerate.

## Scope

### Included

-   `FileManager.default.urls(for:in:)` to locate `Documents`, `Caches`,
    and `Application Support` directories
-   The semantic and backup-behavior difference between the three
    directories
-   Reading/writing files with `Data(contentsOf:)` / `Data.write(to:)` and
    explicit error handling (not force-try)
-   `isExcludedFromBackup` (`URLResourceValues.isExcludedFromBackup`,
    keyed by `URLResourceKey.isExcludedFromBackupKey`) for excluding
    cache-type data from backup

### Excluded

-   The temporary directory (`FileManager.default.temporaryDirectory`) —
    already excluded from backup by the system, not a decision point
-   Non-sandboxed macOS file-system access outside the app's container
-   Codable encoding/decoding of file contents — see
    `codable-encoding-and-custom-conformance.md` and
    `knowledge.networking.codable-decoding`

## Rules

### Rule 1

Agents MUST use `FileManager.default.urls(for:in:)` (or the
`FileManager`/`URL` common-directory properties it backs) to locate
`Documents`, `Caches`, or `Application Support` rather than hard-coding a
path string — Apple's documentation warns that apps like Finder "may
localize directory names and omit file extensions when presenting them in
the user interface," so a hard-coded path is not guaranteed stable.

### Rule 2

Agents MUST route user-generated or user-facing content through
`Documents` (`.documentDirectory`), app-internal support files (config,
templates, modified bundle defaults) through `Application Support`
(`.applicationSupportDirectory`), and regenerable or discardable data
through `Caches` (`.cachesDirectory`). Per Apple's documentation, "files
in Documents/ and Application Support/ are backed up by default," while
"the system doesn't back up either the temporary directory or the caches
directory" — the system may also purge `Caches` when the app isn't
running, so agents MUST ensure the app can operate without cached files or regenerate them on demand. Only files in `Documents` become visible in the iOS Files app.

### Rule 3

Agents MUST wrap `Data(contentsOf:)` and `Data.write(to:options:)` in
`do`/`catch` (or an equivalent `Result`-based path with explicit error
surfacing) rather than force-try — a missing file, a full disk, or a
sandbox permission failure is a routine occurrence for file I/O, not an
exceptional programmer error.

### Rule 4

Agents MUST set `isExcludedFromBackup = true` on cache-type files stored
outside `Caches` (e.g. large regenerable data an agent chooses to place
elsewhere) to prevent them from bloating iCloud/iTunes backups — per
Apple's documentation, this resource value "is only useful for excluding
cache and other application support files which are not needed in a
backup" and "should not be used on user documents." Agents MUST re-apply this resource value after operations that recreate the file, since Apple's documentation states "some common file operations cause this property to reset to false."

### Rule 5

Agents SHOULD prefer placing regenerable data directly in `Caches` over
storing it elsewhere and manually setting `isExcludedFromBackup` — `Caches`
already carries the correct backup and purge behavior by default, so
Rule 4's per-file exclusion is a fallback for data that can't live in
`Caches` for other reasons, not the default approach.

## Compliant Example

```swift
func cachesDirectoryURL() throws -> URL {
    try FileManager.default.url(
        for: .cachesDirectory, in: .userDomainMask,
        appropriateFor: nil, create: true
    )
}

func writeThumbnail(_ data: Data, named name: String) throws {
    let url = try cachesDirectoryURL().appendingPathComponent(name)
    try data.write(to: url, options: .atomic) // Explicit throws, no force-try (Rule 3).
    // Caches is excluded from backup by default -- no manual flag needed (Rule 2, 5).
}
```
Locates the correct directory via the `FileManager` API rather than a hard-coded path (Rule 1), places regenerable thumbnail data in `Caches` (Rule 2, 5), and propagates write errors instead of force-trying (Rule 3).

## Non-Compliant Example

```swift
func writeThumbnail(_ data: Data, named name: String) {
    let path = "/var/mobile/Containers/Data/Application/.../Documents/" + name // Hard-coded path.
    try! data.write(to: URL(fileURLWithPath: path)) // Force-tried write.
}
```
Hard-codes a container path instead of using `FileManager.urls(for:in:)` (Rule 1), stores regenerable thumbnail data in `Documents` — which is backed up by default — instead of `Caches` (Rule 2), and force-tries the write instead of handling I/O errors (Rule 3).

## Dependencies

None.

## References

-   [Apple Developer — FileManager](https://developer.apple.com/documentation/foundation/filemanager)
-   [Apple Developer — FileManager.urls(for:in:)](https://developer.apple.com/documentation/foundation/filemanager/urls(for:in:))
-   [Apple Developer — Using the file system effectively](https://developer.apple.com/documentation/foundation/using-the-file-system-effectively)
-   [Apple Developer — URLResourceValues.isExcludedFromBackup](https://developer.apple.com/documentation/foundation/urlresourcevalues/isexcludedfrombackup)
-   [Apple Developer — URLResourceKey.isExcludedFromBackupKey](https://developer.apple.com/documentation/foundation/urlresourcekey/isexcludedfrombackupkey)
