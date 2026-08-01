# Variable Value Symbols

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.sf-symbols.variable-value-symbols
type: knowledge
title: Variable Value Symbols
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct use of the variableValue parameter on Image(systemName:variableValue:) and UIImage(systemName:variableValue:) to represent a continuous quantity, such as signal or battery strength.
domain: SF Symbols
tags:
  - sf-symbols
  - variable-value
  - image
references:
  - https://developer.apple.com/documentation/swiftui/image/init(systemname:variablevalue:)
  - https://developer.apple.com/documentation/uikit/uiimage/init(systemname:variablevalue:configuration:)
depends_on:
  - knowledge.sf-symbols.symbol-basics
related: []
updated: 2026-08-01
```

## Intent

This contract defines how an AI coding agent represents a continuous
quantity (signal strength, battery level, volume) using a variable-value
SF Symbol, so the rendered symbol always reflects the current numeric
state instead of a fixed appearance.

## Scope

### Included

-   `variableValue:` parameter on `Image(systemName:variableValue:)` and
    `UIImage(systemName:variableValue:configuration:)`
-   Clamping and normalizing the input value to the expected `0...1` range
-   Driving the value from state that updates over time

### Excluded

-   Which symbols are semantically appropriate to pair with a variable
    value — see `human-interface-guidelines`'s `sf-symbols.md`
-   Animated transitions between variable-value levels — deferred,
    symbol-effects/animation scope is out of v1

## Rules

### Rule 1

Agents MUST pass a value in the closed range `0...1` to `variableValue:`
— out-of-range values are clamped rather than rejected, which can
silently mask a data bug (e.g. passing an unconverted `0...100`
percentage instead of normalizing it first).

### Rule 2

Agents MUST use `variableValue:` only with a symbol Apple has authored
with a variable-value representation (e.g. `"wifi"`, cellular- and
battery-style indicator symbols) — passing it to a symbol without one is
a silent no-op, not an error, so the symbol renders as if the parameter
were never supplied.

### Rule 3

Agents SHOULD drive `variableValue` from state that updates as the
underlying quantity changes (e.g. a computed property backed by
`@State`/`@Published`), not a value computed once at view construction,
so the rendered symbol always reflects current data.

### Rule 4

Agents MUST NOT use `variableValue` as a substitute for
`.symbolVariant`/`.fill` boolean state toggling — variable value
represents a continuous quantity, not a selected/unselected state; see
`symbol-variants` for boolean state.

## Compliant Example

```swift
struct SignalIndicator: View {
    @State private var rawSignalPercent: Double

    private var normalizedValue: Double {
        min(max(rawSignalPercent / 100, 0), 1)
    }

    var body: some View {
        Image(systemName: "wifi", variableValue: normalizedValue)
    }
}
```
Percentage explicitly normalized into `0...1` and re-derived from live state on every render. (Rules 1, 3)

## Non-Compliant Example

```swift
Image(systemName: "wifi", variableValue: 85)
```
Raw percentage (`85`) passed directly — silently clamped to `1.0`, indistinguishable from a true 100% signal, losing the actual quantity the symbol was meant to represent. (Rule 1)

## Dependencies

- `knowledge.sf-symbols.symbol-basics` — variable value applies to a symbol already resolved by name.

## References

-   [Apple Developer — Image(systemName:variableValue:)](https://developer.apple.com/documentation/swiftui/image/init(systemname:variablevalue:))
-   [Apple Developer — UIImage(systemName:variableValue:configuration:)](https://developer.apple.com/documentation/uikit/uiimage/init(systemname:variablevalue:configuration:))
