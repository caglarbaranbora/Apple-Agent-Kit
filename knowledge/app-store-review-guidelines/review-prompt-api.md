# Review Prompt API

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.review-prompt-api
artifact_type: knowledge
title: Review Prompt API
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines guideline 5.6.1's requirement to request ratings only through the system API and Apple's statement that custom review prompts are disallowed, the satisfaction gate that is itself a custom prompt, Apple's instruction not to call requestReview from a button because the alert may not appear and the write-review product-page link that is the sanctioned alternative, the rate limits that make an unseen prompt normal rather than broken and the TestFlight build where it never appears at all, and the 5.6.3 prohibition on manipulating reviews.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - legal
  - ratings
  - storekit
references:
  - https://developer.apple.com/app-store/review/guidelines/#5.6.1
  - https://developer.apple.com/app-store/review/guidelines/#5.6.3
  - https://developer.apple.com/documentation/storekit/skstorereviewcontroller
  - https://developer.apple.com/documentation/storekit/skstorereviewcontroller/requestreview(in:)
  - https://developer.apple.com/documentation/swiftui/environmentvalues/requestreview
depends_on: []
related:
  - knowledge.app-store-review-guidelines.spam-duplicate-apps
  - knowledge.app-store-review-guidelines.description-accuracy
last_updated: 2026-08-08
```

## Intent

This contract defines how an app may ask for a rating. Its central claim is
that the system API is not merely the recommended route but the only
permitted one — Apple states it "will disallow custom review prompts" — and
that the two designs teams reach for instead, a satisfaction gate and a
"Rate us" button, are respectively a policy violation and an action Apple
tells developers not to take.

## Scope

### Included

-   The required API, and what counts as a custom prompt
-   Where the call may and may not be triggered from
-   Rate limits, TestFlight behaviour, and review manipulation

### Excluded

-   StoreKit purchases, entitlements, and transactions — owned by `storekit`
-   When in a session to ask, as a design question — owned by
    `human-interface-guidelines`
-   Prompt wording — owned by `style-guide`

## Rules

### Rule 1

Agents MUST request ratings through the system API — SwiftUI's
`@Environment(\.requestReview)` or `SKStoreReviewController.requestReview(in:)`
— and MUST NOT build their own prompt. Per Apple: "Use the provided API to
prompt users to review your app… and we will disallow custom review
prompts." A modal the app draws itself is the violation regardless of how
politely it is worded.

### Rule 2

Agents MUST NOT gate the system prompt behind a satisfaction question. The
"Enjoying the app? → Yes shows the real prompt, No opens a feedback form"
pattern is a custom review prompt under Rule 1, and it filters who reaches
the App Store — which 5.6.3 reaches as "manipulating any element of the App
Store customer experience such as charts, search, reviews, or referrals."

### Rule 3

Agents MUST NOT call the API from a button or other user action. Per Apple's
documentation: "Because this method may not present an alert, don't call
`requestReview()` or `requestReview(in:)` in response to a button tap or
other user action." A "Rate us" button wired to it does nothing on most
taps, which reads as a broken control.

### Rule 4

Agents MUST use a product-page link when a user-initiated path is wanted.
Per Apple: "you may include a persistent link to your App Store product page
in your app's settings or configuration screens. Append the query parameter
`action=write-review` to your product page URL to automatically open the App
Store page where users can write a review." That is the sanctioned form of
Rule 3's button.

### Rule 5

Agents MUST treat an absent prompt as expected, and MUST NOT verify the
feature in TestFlight. StoreKit shows the request "a maximum of three times
within a 365-day period" for someone who has not yet reviewed, and for
someone who has, only on a new version and after 365 days. Apple adds that
the method "has no effect in apps that you distribute for beta testing using
TestFlight" — so a TestFlight build proves nothing, and adding a retry loop
because the alert did not appear is working against the rate limit.

## Compliant Example

-   ✓ `requestReview()` is called from the environment after the user completes a third successful workflow, with no button attached. (Rules 1, 3)
-   ✓ Settings carries a "Write a Review" row opening the product page URL with `?action=write-review`. (Rule 4)
-   ✓ A feedback form exists in Settings and is reachable independently, not as the "No" branch of a rating question. (Rule 2)
-   ✓ Prompt logic is verified in a development build, where StoreKit always displays the view. (Rule 5)

## Non-Compliant Example

-   ✗ A custom alert asks for five stars and links to the App Store on tap. (Rule 1)
-   ✗ "Are you enjoying the app?" routes satisfied users to the system prompt and everyone else to support. (Rules 1, 2)
-   ✗ A "Rate us" button in Settings calls `requestReview(in:)` and usually appears to do nothing. (Rules 3, 4)
-   ✗ The prompt is re-requested on every launch until it appears. (Rule 5)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 5.6.1 App Store Reviews](https://developer.apple.com/app-store/review/guidelines/#5.6.1)
-   [Apple App Review Guidelines — 5.6.3 Discovery Fraud](https://developer.apple.com/app-store/review/guidelines/#5.6.3)
-   [Apple Developer — SKStoreReviewController](https://developer.apple.com/documentation/storekit/skstorereviewcontroller)
-   [Apple Developer — requestReview(in:)](https://developer.apple.com/documentation/storekit/skstorereviewcontroller/requestreview(in:))
-   [Apple Developer — EnvironmentValues.requestReview](https://developer.apple.com/documentation/swiftui/environmentvalues/requestreview)
