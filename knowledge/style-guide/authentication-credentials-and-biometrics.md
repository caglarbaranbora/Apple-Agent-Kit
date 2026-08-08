# Authentication Credentials and Biometrics

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.authentication-credentials-and-biometrics
artifact_type: knowledge
title: Authentication Credentials and Biometrics
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines correct usage and distinctions among passkey, passphrase, password, PIN, code/passcode, Touch ID, Face ID, two-factor authentication, and two-step verification.
domain: Style Guide
tags:
  - style-guide
  - authentication
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.sign-in-and-authentication-terminology
last_updated: 2026-08-08
```

## Intent

This contract defines the precise, non-interchangeable meanings of
credential and biometric terms — passkey, passphrase, password, PIN,
code/passcode, Touch ID, Face ID, two-factor authentication, and two-step
verification — so an AI coding agent doesn't substitute one for another in
UI text or documentation.

## Scope

### Included

-   Distinguishing passkey, passphrase, password, PIN, and code/passcode
-   Touch ID and Face ID as named biometric technologies
-   Distinguishing two-factor authentication from two-step verification

### Excluded

-   Sign-in/sign-out/login verb and hyphenation forms (see `sign-in-and-authentication-terminology`)
-   Generic button-labeling rules (see `general-button-labels`)

## Rules

### Rule 1

Agents MUST use "passkey" only for the sign-in method for apps and
websites that is more secure than a password, and MUST NOT use it to mean
code, passcode, or password.

### Rule 2

Agents MUST avoid "passphrase" in user materials; agents MUST use
"passcode," "password," or "passkey" instead, depending on context.

### Rule 3

Agents MUST use "password" only for a sequence of characters a user enters
to gain access to a protected resource, and MUST NOT use it to mean code,
passcode, or passkey.

### Rule 4

Agents MUST use "PIN" only to refer to the PIN used to unlock a SIM card
when discussing iOS or iPadOS devices.

### Rule 5

Agents MUST use "code" for the sequence of numbers sent to a device to
verify a user's identity (e.g. a six-digit verification code), and
"passcode" for the unique number/letter combination a user sets to lock or
unlock a device, restrict a device, or authenticate Apple Pay purchases.

### Rule 6

Agents MUST use "Touch ID" for the fingerprint-recognition authentication
technology; it's OK to use "Touch ID" alone or in terms like "Touch ID
sensor." Agents MUST use "Face ID" for the face-recognition authentication
technology available on some iOS and iPadOS devices.

### Rule 7

Agents MUST use "two-factor authentication" only for the security feature
that requires entering a code from a trusted device when signing in to an
Apple Account on a new device, and "two-step verification" only for the
security feature that requires entering a code from a trusted device when
signing in to an app or service. Agents MUST NOT use these two terms
interchangeably.

## Compliant Example

-   ✓ "Use to refer to a sign-in method that's more secure than a password." for passkey (Rule 1)
-   ✓ Rewriting "Enter your passphrase" as "Enter your password." (Rule 2)
-   ✓ "Enter the six-digit code sent to your iPhone." (Rule 5)
-   ✓ "To unlock Apple Watch, enter your passcode." (Rule 5)
-   ✓ "Make sure the Touch ID sensor and your finger are clean and dry." (Rule 6)
-   ✓ Using "two-factor authentication" for new-device Apple Account sign-in (Rule 7)

## Non-Compliant Example

-   ✗ "Enter your passkey" when referring to a typed password (Rule 1, Rule 3)
-   ✗ "Enter your passphrase" left in user-facing text (Rule 2)
-   ✗ Using "PIN" for a device passcode outside the SIM-unlock context (Rule 4)
-   ✗ Using "password" and "passcode" interchangeably for the same field (Rule 3, Rule 5)
-   ✗ "two-step verification" used to describe new-device Apple Account sign-in (Rule 7)

## Dependencies

None.

## References

-   [Apple Style Guide — passkey; passphrase; password (p. 154)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — PIN (p. 159)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — code, passcode (p. 53)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — Touch ID (p. 206); Face ID (p. 83)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — two-factor authentication; two-step verification (p. 208)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
