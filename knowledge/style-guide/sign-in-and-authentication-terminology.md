# Sign-In and Authentication Terminology

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.sign-in-and-authentication-terminology
artifact_type: knowledge
title: Sign-In and Authentication Terminology
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines correct hyphenation, part-of-speech forms, and preposition usage for sign-in, sign-out, sign-on, single sign-on, and login/log-in terminology.
domain: Style Guide
tags:
  - style-guide
  - authentication
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.authentication.sign-in-terminology
  - knowledge.style-guide.authentication-credentials-and-biometrics
  - knowledge.style-guide.general-button-labels
last_updated: 2026-07-30
```

## Intent

This contract defines the correct noun, adjective, and verb forms for
sign-in, sign-out, sign-on, single sign-on, and login/log-in terminology,
including preposition usage, so an AI coding agent writes consistent
authentication-flow copy across UI text and documentation.

## Scope

### Included

-   Hyphenation and part-of-speech forms of sign-in, sign-on, single sign-on
-   Correct verb forms for signing out
-   login (n., adj.) vs. log in (v.), and the deprecated log on / log off
-   Preposition usage: "sign in to," "log in to," never "sign into" / "log into"
-   "into" vs. "in to" as a general grammar rule underlying the above

### Excluded

-   Passkey, password, PIN, and biometric authentication terminology (see `authentication-credentials-and-biometrics`)
-   Generic button-labeling and quotation-mark rules (see `general-button-labels`)

## Rules

### Rule 1

Agents MUST use "sign-in" as a noun or adjective and "sign in" (two words,
no hyphen) as a verb, to refer to creating a session for an internet
account. Users sign in to accounts and services; computers, devices, and
apps do not. Agents MUST use "sign in to," never "sign into."

### Rule 2

Agents MUST describe ending an account session as "sign out of," never
"sign off," "sign off of," or "sign off from."

### Rule 3

Agents MUST use "sign-on" as a noun or adjective (no hyphen removed) and
"sign on" (no hyphen) as a verb.

### Rule 4

Agents MUST hyphenate "single sign-on" in all forms (noun and adjective),
including in compound phrases such as "single sign-on authentication." It
refers to a service that lets a user access multiple apps with one ID and
password.

### Rule 5

Agents MUST use "login" (one word) as a noun or adjective and "log in"
(two words) as a verb, to refer to starting a system account session.
Agents MUST use "log in to," never "log into." Users "log in to" a file
server (not "log on to"); users "log out of" a file server (not "log off,"
"log off of," or "log out from").

### Rule 6

Agents MUST NOT use "log on" or "log off"; agents MUST use "log in" and
"log out" instead.

### Rule 7

Agents MUST use "in to" (two words) when "in" is part of a phrasal verb
(Log in to the computer), and MUST use "into" (one word) only to imply
physical motion to the inside of something (Insert the CD into the
optical drive). Agents MUST NOT write "Log into the computer."

## Compliant Example

-   ✓ "Sign in to your Apple Account to get access to Apple services." (Rule 1)
-   ✓ "Users sign out of accounts and services." (Rule 2)
-   ✓ "single sign-on authentication" (Rule 4)
-   ✓ "You must log in as an administrator." (Rule 5)
-   ✓ "You must log out of the server," not "log off the server." (Rule 5)
-   ✓ "Log in to the computer." (Rule 7)

## Non-Compliant Example

-   ✗ "Your Mac must be signed in to your Apple Account" implying the device signs in (Rule 1)
-   ✗ "Sign into your Apple Account." (Rule 1)
-   ✗ "Users sign off of accounts." (Rule 2)
-   ✗ "single sign on authentication" missing hyphen (Rule 4)
-   ✗ "You must log into the computer." (Rule 5, Rule 7)
-   ✗ "Log on to the server." (Rule 6)

## Dependencies

None.

## References

-   [Apple Style Guide — sign-in (n., adj.), sign in (v.) (p. 185)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — sign-on (n., adj.), sign on (v.); single sign-on (p. 186)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — login (n., adj.), log in (v.); log on, log off (p. 130)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — into, in to (p. 113)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
