# Permission Usage Strings

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.permission-usage-strings
artifact_type: knowledge
title: Permission Usage Strings
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the requirement for accurate, specific Info.plist usage-description strings and informed user consent before collecting user or usage data, per guideline 5.1.1(ii) and 5.1.1(iv).
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - privacy
  - permissions
  - info-plist
references:
  - https://developer.apple.com/app-store/review/guidelines/#5.1.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-manifest
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
last_updated: 2026-08-08
```

## Intent

This contract defines how an agent writes `Info.plist` permission-usage
strings and gates data-dependent functionality: specific, accurate
strings, informed consent, and a fallback path when a permission is
declined (guideline 5.1.1(ii), 5.1.1(iv)).

## Scope

### Included

-   Consent requirement before collecting user/usage data
-   `Info.plist` usage-description string accuracy
-   Prohibition on gating unrelated paid functionality behind a permission
-   Prohibition on bundling unrelated permission requests
-   Fallback-path expectation when a permission is declined
-   Consent-withdrawal accessibility

### Excluded

-   Privacy manifest (`PrivacyInfo.xcprivacy`) declarations — see `privacy-manifest`
-   App Store Connect privacy label accuracy — see `privacy-nutrition-label`

## Rules

### Rule 1

Agents MUST secure user consent before collecting user or usage data,
even data considered anonymous at or immediately after collection.

### Rule 2

Agents MUST write each `Info.plist` usage-description string (e.g.
`NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`) to
clearly and completely describe the actual use of the requested data —
generic or vague strings are a rejection risk.

### Rule 3

Agents MUST NOT make paid functionality dependent on a user granting a
data-access permission that isn't required for that functionality.

### Rule 4

Agents MUST NOT request an unrelated permission as a prerequisite for
an unrelated feature (e.g., requiring microphone access before allowing
a photo upload).

### Rule 5

Agents SHOULD offer an alternative path when a user declines a
permission (e.g., manual address entry when Location is declined)
rather than blocking the feature entirely.

### Rule 6

Agents MUST provide an easily accessible, understandable way for the
user to withdraw previously granted consent.

## Compliant Example

-   ✓ `NSContactsUsageDescription` reads "Used to let you invite friends already in your contacts — we don't upload or store your contacts."; the invite feature still works via manual entry if Contacts is declined. (Rules 2, 5)

## Non-Compliant Example

-   ✗ `NSCameraUsageDescription` reads "This app needs camera access." with no explanation of use. (Rule 2)
-   ✗ App blocks all functionality until Contacts permission is granted, even though contacts aren't used anywhere else in the app. (Rule 4)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 5.1.1 Data Collection and Storage](https://developer.apple.com/app-store/review/guidelines/#5.1.1)
