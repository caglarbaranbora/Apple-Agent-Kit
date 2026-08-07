# Measurement and Unit Formatting

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.foundation.measurement-and-unit-formatting
artifact_type: knowledge
title: Measurement and Unit Formatting
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct construction and conversion of Measurement<UnitType> and locale-aware display via MeasurementFormatter, including unitStyle and unitOptions configuration.
domain: Foundation
tags:
  - foundation
  - measurement
  - measurementformatter
  - unit-conversion
references:
  - https://developer.apple.com/documentation/foundation/measurement
  - https://developer.apple.com/documentation/foundation/measurementformatter
depends_on: []
related:
  - knowledge.style-guide.units-of-measure
last_updated: 2026-08-06
```

## Intent

This contract defines how an AI coding agent constructs and converts
`Measurement<UnitType>` values and produces locale-aware, unit-converted
display strings with `MeasurementFormatter` — producing the correctly
localized value/string in the first place, as distinct from
`knowledge.style-guide.units-of-measure`, which governs how a unit is
*worded* once it already appears as text in UI copy (spelling out vs.
abbreviating, spacing, capitalization). Angle-split, not duplication: this
contract owns the API call that produces the string; style-guide owns the
resulting text's copy-formatting rules.

## Scope

### Included

-   Constructing `Measurement<UnitType>` from a `Unit` subclass and a
    `Double` value
-   `.converted(to:)` for unit conversion between compatible units
-   `MeasurementFormatter.string(from:)` for locale-aware measurement
    display
-   `MeasurementFormatter.unitStyle` (`.short`, `.medium`, `.long`) and
    `MeasurementFormatter.unitOptions` (`.providedUnit`, `.naturalScale`)

### Excluded

-   Spelling-out vs. abbreviating a unit, spacing, hyphenation, and
    capitalization of units already rendered as UI copy text — see
    `knowledge.style-guide.units-of-measure`
-   Currency formatting (`NumberFormatter` currency styles)
-   Date and time formatting — see `date-time-formatting.md`
-   Locale/Bundle translation workflow mechanics — deferred to the future
    `localization` domain (Tier 2, unbuilt)

## Rules

### Rule 1

Agents MUST use `Measurement<UnitType>.converted(to:)` to convert between
compatible units rather than hand-writing conversion arithmetic — Apple's
documentation states the `Measurement` type "provides a programmatic
interface to converting measurements into different units," and
`converted(to:)` "returns a new measurement created by converting to the
specified unit," which is unit-safe (the compiler enforces `UnitType`
compatibility) where manual arithmetic is not.

### Rule 2

Agents MUST use `MeasurementFormatter.string(from:)` to produce a
user-visible string from a `Measurement`, rather than concatenating a
raw `Double` with a hand-written unit symbol — `MeasurementFormatter`
"provides localized representations of units and measurements," so it
selects the locale-appropriate unit system, symbol, and number formatting
automatically (e.g. respecting a user's metric/imperial preference) where
manual string interpolation would not.

### Rule 3

Agents MUST set `MeasurementFormatter.unitOptions = .providedUnit` when
the unit shown must remain exactly the one the `Measurement` was
constructed with (e.g. a recipe app displaying an ingredient in the unit
the user chose). Agents MUST leave the default `.naturalScale` (or set it
explicitly) only when the formatter should be free to pick the
locale-natural unit and scale instead — the two option values are
mutually distinct behaviors, not interchangeable defaults.

### Rule 4

Agents SHOULD choose `MeasurementFormatter.unitStyle` deliberately rather
than accepting the default: `.short` for compact UI (e.g. table cells,
badges), `.medium` (the default) for standard body text, and `.long` for
contexts needing the fully spelled-out unit name — the possible values
are `.short`, `.medium`, and `.long`, with `.medium` as default.

### Rule 5

Agents MUST NOT construct a `MeasurementFormatter` inside a loop or a
frequently-called render path for the same reason `DateFormatter`
instances must be cached (see `date-time-formatting.md` Rule 1) —
`MeasurementFormatter` carries its own `NumberFormatter` and `Locale`
configuration and should be created once and reused.

## Compliant Example

```swift
let formatter = MeasurementFormatter()
formatter.unitOptions = .providedUnit
formatter.unitStyle = .medium

let distance = Measurement(value: 5, unit: UnitLength.kilometers)
let inMiles = distance.converted(to: .miles) // Type-safe conversion (Rule 1).
let label = formatter.string(from: inMiles) // Locale-aware string (Rule 2, 3, 4).
```
Converts with `.converted(to:)` instead of manual arithmetic, and produces the display string via a reused, deliberately-configured `MeasurementFormatter` (Rules 1, 2, 3, 4).

## Non-Compliant Example

```swift
func label(forKilometers km: Double) -> String {
    let miles = km * 0.621371 // Hand-written conversion factor.
    return MeasurementFormatter().string(from: Measurement(value: miles, unit: UnitLength.miles))
    // New MeasurementFormatter allocated on every call.
}
```
Hand-writes the km-to-miles conversion factor instead of using `.converted(to:)` (Rule 1), and allocates a new `MeasurementFormatter` on every call instead of reusing a cached instance (Rule 5).

## Dependencies

None.

## References

-   [Apple Developer — Measurement](https://developer.apple.com/documentation/foundation/measurement)
-   [Apple Developer — Measurement.converted(to:)](https://developer.apple.com/documentation/foundation/measurement/converted(to:))
-   [Apple Developer — MeasurementFormatter](https://developer.apple.com/documentation/foundation/measurementformatter)
-   [Apple Developer — MeasurementFormatter.UnitOptions](https://developer.apple.com/documentation/foundation/measurementformatter/unitoptions-swift.struct)
-   [Apple Developer — MeasurementFormatter.unitStyle](https://developer.apple.com/documentation/foundation/measurementformatter/unitstyle)
