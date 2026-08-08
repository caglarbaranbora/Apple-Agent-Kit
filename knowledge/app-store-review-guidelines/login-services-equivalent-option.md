# Login Services Equivalent Option

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.login-services-equivalent-option
artifact_type: knowledge
title: Login Services Equivalent Option
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines guideline 4.8's rule that an app using a third-party or social login service for the user's primary account must also offer an equivalent option with three named properties — data collection limited to name and email, the ability to keep the email address private, and no collection of in-app interactions for advertising without consent — the definition of a primary account that decides whether the rule applies at all, and the five exemptions an agent must be able to name before concluding the option is not required.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - design
  - authentication
  - sign-in
references:
  - https://developer.apple.com/app-store/review/guidelines/#4.8
depends_on: []
related:
  - knowledge.app-store-review-guidelines.privacy-nutrition-label
  - knowledge.app-store-review-guidelines.data-security
last_updated: 2026-08-08
```

## Intent

This contract defines when adding a social login obliges an app to add a
second one. Its central claim is that the trigger is narrow and the
consequence is a screen: 4.8 applies only to the app's **primary account**,
but where it applies the missing option is a shipped-UI change, so an app
that discovers it at review has to rebuild its sign-in screen and resubmit.
An agent building a sign-in flow needs this rule before the flow exists, not
after.

## Scope

### Included

-   What makes 4.8 apply: the primary-account definition
-   The three properties the equivalent option must have
-   The five exemptions, and using them deliberately

### Excluded

-   Implementing Sign in with Apple — owned by `authenticationservices`
-   Sign-in screen layout and button placement — owned by
    `human-interface-guidelines`
-   Sign-in wording — owned by `style-guide`
-   Keychain storage of the resulting credential — owned by `security`

## Rules

### Rule 1

Agents MUST add an equivalent login option whenever a third-party or social
login sets up or authenticates the user's primary account. Per Apple, apps
using such a service "must also offer as an equivalent option another login
service" with the listed features. Apple's examples of the triggering
services are "Facebook Login, Google Sign-In, Log in with X, Sign In with
LinkedIn, Login with Amazon, or WeChat Login".

### Rule 2

Agents MUST decide first whether the account in question is the primary one.
Per Apple, "a user's primary account is the account they establish with your
app for the purposes of identifying themselves, signing in, and accessing
your features and associated services." A social login used only to import a
contact list or share a post is not a primary account and does not trigger
4.8.

### Rule 3

Agents MUST verify the alternative against the three stated properties, not
against a brand. Apple requires that "the login service limits data
collection to the user's name and email address", that it "allows users to
keep their email address private as part of setting up their account", and
that it "does not collect interactions with your app for advertising
purposes without consent." Sign in with Apple satisfies all three, which is
why it is the usual answer — but the guideline specifies properties.

### Rule 4

Agents MUST NOT conclude the option is unnecessary without naming which of
Apple's five exemptions applies. Apple lists them: the app uses only the
company's own account systems; it is an alternative app marketplace or
distributed from one, using a marketplace-specific login; it is an
education, enterprise, or business app requiring an existing education or
enterprise account; it uses a government or industry-backed citizen
identification or electronic ID; or it is a client for a specific
third-party service where users sign in to that service directly to reach
their own content.

### Rule 5

Agents MUST offer the alternative at equal prominence in the same flow.
"Equivalent option" describes the choice presented to the user, so an
alternative reachable only from a secondary screen, or added after account
creation, does not satisfy it — the user must be able to establish the
primary account either way.

## Compliant Example

-   ✓ A sign-in screen offering Google Sign-In also offers Sign in with Apple, both in the initial flow. (Rules 1, 3, 5)
-   ✓ An app that authenticates only against its own email-and-password backend offers no third-party login and records exemption one. (Rules 2, 4)
-   ✓ A mail client where users sign in to their own provider records exemption five before shipping without a second option. (Rule 4)
-   ✓ A social login used solely to post a score to a feed leaves the primary account untouched, so 4.8 does not apply. (Rule 2)

## Non-Compliant Example

-   ✗ Sign-in offers only Facebook Login. (Rule 1)
-   ✗ Sign in with Apple exists but only under "More sign-in options" two taps deep. (Rule 5)
-   ✗ A team concludes 4.8 does not apply because "we are a business app", without checking whether users sign in with an existing enterprise account. (Rule 4)
-   ✗ An alternative is added that returns the user's full profile and friend graph. (Rule 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 4.8 Login Services](https://developer.apple.com/app-store/review/guidelines/#4.8)
