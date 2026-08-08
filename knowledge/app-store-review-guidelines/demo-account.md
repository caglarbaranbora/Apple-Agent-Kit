# Demo Account

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.demo-account
artifact_type: knowledge
title: Demo Account
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the requirement to provide App Review with working demo credentials or an Apple-approved built-in demo mode for any app that gates functionality behind login.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - demo-account
  - submission
  - login
references:
  - https://developer.apple.com/app-store/review/guidelines/#2.1
depends_on: []
related:
  - knowledge.app-store-review-guidelines.app-completeness
last_updated: 2026-08-08
```

## Intent

This contract defines how an agent ensures App Review can actually reach
login-gated functionality: working demo credentials, or an
Apple-approved built-in demo mode as a substitute (guideline 2.1(a)).

## Scope

### Included

-   Demo account credentials in App Store Connect review notes
-   Backend/server-side availability of the demo account at submission time
-   Built-in demo mode as an Apple-approved substitute
-   Feature parity requirement for demo mode vs. real account

### Excluded

-   General build-completeness/crash requirements — see `app-completeness`

## Rules

### Rule 1

Agents MUST include demo account credentials in the App Store Connect
review notes if the app requires login to access reviewable
functionality.

### Rule 2

Agents MUST ensure the demo account's backend dependency is active and
reachable at submission time — a demo account that fails to
authenticate is treated as an incomplete submission.

### Rule 3

Agents MAY substitute a built-in demo mode for a demo account only when
a demo account cannot be provided for legal or security reasons, and
only with Apple's prior approval.

### Rule 4

Agents MUST ensure a substitute demo mode exhibits the app's full
features and functionality, not a reduced subset.

## Compliant Example

-   ✓ Review notes include a working username/password; reviewer logs in successfully and reaches gated content. (Rules 1, 2)

## Non-Compliant Example

-   ✗ Review notes contain no demo credentials for a login-gated app. (Rule 1)
-   ✗ The demo account was disabled after internal testing and returns invalid-credentials errors during review. (Rule 2)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 2.1 App Completeness](https://developer.apple.com/app-store/review/guidelines/#2.1)
