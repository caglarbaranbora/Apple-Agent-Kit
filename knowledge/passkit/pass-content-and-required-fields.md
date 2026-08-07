# Pass Content and Required Fields

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.passkit.pass-content-and-required-fields
artifact_type: knowledge
title: Pass Content and Required Fields
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the structure of a .pkpass bundle's pass.json -- the required top-level keys, the five pass style keys, the PassFields field groups, the barcodes array, and locations/relevantDates -- and the app-vs-server boundary for authoring, signing, and client-side inspection via PKPass(data:).
domain: PassKit
tags:
  - passkit
  - pass-json
  - pkpass
  - walletpasses
  - pass-fields
references:
  - https://developer.apple.com/documentation/walletpasses/pass
  - https://developer.apple.com/documentation/walletpasses/passfields
  - https://developer.apple.com/documentation/walletpasses/pass/barcode-data.dictionary
  - https://developer.apple.com/documentation/passkit/pkpass
  - https://developer.apple.com/documentation/passkit/pkpass/init(data:)
depends_on: []
related: []
last_updated: 2026-08-06
```

## Intent

This contract defines the structure of a `.pkpass` bundle's `pass.json` that an agent needs to know to build a correct backend contract or to inspect a pass client-side with `PKPass(data:)` — the required top-level keys, the five pass style keys, the front/back field groups, the barcode array, and the relevance keys. It does not cover authoring, signing, or distributing the bundle itself, which is server-side work outside this domain.

## Scope

### Included

-   Required top-level keys: `formatVersion`, `passTypeIdentifier`, `serialNumber`, `teamIdentifier`, `organizationName`, `description`
-   The five mutually exclusive pass style keys: `boardingPass`, `coupon`, `eventTicket`, `storeCard`, `generic`
-   The `PassFields` groups: `headerFields`, `primaryFields`, `secondaryFields`, `auxiliaryFields`, `backFields`
-   The `barcodes` array (current) vs. the deprecated singular `barcode`, and the barcode `format` values
-   `locations`/`maxDistance` and `relevantDates` (current) vs. the deprecated singular `relevantDate`
-   Client-side construction/inspection of a pass with `PKPass(data:)`

### Excluded

-   Signing a `.pkpass` bundle, certificate/Pass Type ID management, and the Apple Developer portal setup process — entirely server-side and Developer-Program work, not app Swift code
-   Querying/adding passes already in the library (`PKPassLibrary`) — see `pass-library-and-authorization`
-   Presenting the add-to-Wallet UI — see `adding-passes-ui`
-   `webServiceURL`/`authenticationToken` and the update push protocol — see `pass-updates-and-push-registration`

## Rules

### Rule 1

Agents specifying or validating a backend's pass-generation contract MUST require `formatVersion`, `passTypeIdentifier`, `serialNumber`, `teamIdentifier`, `organizationName`, and `description` on every pass, since Apple's `Pass` reference marks each as required. Per Apple's documentation: `formatVersion` — "The version of the file format. The value needs to be `1`."; `passTypeIdentifier` — "The pass type identifier that's registered with Apple. The value needs to be the same as the distribution certificate that signs the pass."; `serialNumber` — "An alphanumeric serial number. The combination of the serial number and pass type identifier needs to be unique for each pass."; `teamIdentifier` — "The Team ID for the Apple Developer Program account that registered the pass type identifier."

### Rule 2

Agents MUST set exactly one of the five style keys — `boardingPass`, `coupon`, `eventTicket`, `storeCard`, `generic` — per pass, and MUST NOT treat them as combinable. Apple's reference documents all five as optional, sibling top-level keys (e.g. `boardingPass`: "An object that contains the information for a boarding pass."; `generic`: "An object that contains the information for a generic pass."); a pass's style is which one of these five keys is present, not a separate `style` enum field.

### Rule 3

Agents laying out a pass's visible content MUST place field dictionaries in the correct `PassFields` group rather than inventing new keys: `headerFields` for the top of the pass, `primaryFields` for "the most important information," `secondaryFields`/`auxiliaryFields` for supporting front-of-pass information, and `backFields` for the back. This is Apple's own grouping, taken directly from the `PassFields` reference, which documents `primaryFields`, `secondaryFields`, `auxiliaryFields`, `backFields`, and `headerFields` as the complete set of front/back field groups.

### Rule 4

Agents adding a scannable code MUST use the `barcodes` array, not the deprecated singular `barcode` key, and MUST choose a `format` Apple actually documents. Apple's `Pass.Barcode` reference states the singular object "is deprecated. Use `barcodes` instead," and documents `format`'s allowed values as `PKBarcodeFormatQR`, `PKBarcodeFormatPDF417`, and `PKBarcodeFormatAztec`, further noting "The barcode format PKBarcodeFormatCode128 isn't supported for watchOS" — implying it remains valid on other platforms even though it's absent from the allowed-values list shown for this key.

### Rule 5

Agents adding location- or time-based relevance MUST use `locations`/`maxDistance` and the current `relevantDates` array, and MUST NOT rely on the deprecated singular `relevantDate`. Per Apple's documentation, the singular `relevantDate` entry states "This object is deprecated. Use `relevantDates` instead," while `relevantDates` is documented as "An array of objects that represent date intervals that the system uses to show a relevant pass." Agents inspecting a pass client-side, rather than authoring one, MUST use `PKPass(data:) throws` and handle the thrown error rather than assuming the `Data` is always well-formed.

## Compliant Example

```json
{
  "formatVersion": 1,
  "passTypeIdentifier": "pass.com.example.loyalty",
  "serialNumber": "abc123",
  "teamIdentifier": "ABCDE12345",
  "organizationName": "Example Cafe",
  "description": "Example Cafe loyalty card",
  "storeCard": {
    "primaryFields": [{ "key": "balance", "label": "BALANCE", "value": "$12.50" }]
  },
  "barcodes": [
    { "format": "PKBarcodeFormatQR", "message": "abc123", "messageEncoding": "iso-8859-1" }
  ],
  "relevantDates": [{ "startDate": "2026-08-06T09:00-07:00" }]
}
```

```swift
import PassKit

func inspectPass(from data: Data) -> PKPass? {
    try? PKPass(data: data) // Rule 5: throws, not force-unwrapped
}
```

## Non-Compliant Example

```json
{
  "passTypeIdentifier": "pass.com.example.loyalty",
  "serialNumber": "abc123",
  "storeCard": {},
  "generic": {},
  "barcode": { "format": "PKBarcodeFormatQR", "message": "abc123" },
  "relevantDate": "2026-08-06T09:00-07:00"
}
```
Omits required `formatVersion`/`teamIdentifier`/`organizationName`/`description` (Rule 1), sets two style keys at once (Rule 2), and uses the deprecated singular `barcode`/`relevantDate` instead of `barcodes`/`relevantDates` (Rule 4, Rule 5).

## Dependencies

None within this domain — this contract defines the pass structure other PassKit Knowledge Contracts in this domain reference (`PKPass`, `webServiceURL`/`authenticationToken`) but do not themselves author.

## References

-   [Apple Developer — Pass](https://developer.apple.com/documentation/walletpasses/pass)
-   [Apple Developer — PassFields](https://developer.apple.com/documentation/walletpasses/passfields)
-   [Apple Developer — Pass.Barcode](https://developer.apple.com/documentation/walletpasses/pass/barcode-data.dictionary)
-   [Apple Developer — PKPass](https://developer.apple.com/documentation/passkit/pkpass)
-   [Apple Developer — PKPass.init(data:)](https://developer.apple.com/documentation/passkit/pkpass/init(data:))
