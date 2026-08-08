# Connectivity and Media Terminology

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.connectivity-and-media-terminology
artifact_type: knowledge
title: Connectivity and Media Terminology
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the correct vocabulary for connectivity state, device pairing, and media terms that recur in onboarding, settings, and messaging UI text.
domain: Style Guide
tags:
  - style-guide
  - connectivity
  - media
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.capitalization-of-apple-proper-nouns
  - knowledge.style-guide.app-state-and-error-terminology
  - knowledge.style-guide.ui-action-verbs
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent describes connectivity state,
device pairing, and media content — phones, network status, photos, and
messaging — in onboarding, settings, and messaging UI text for Apple
platforms.

## Scope

### Included

-   Connectivity state: online, offline, onboard
-   Device pairing: pair, paired
-   Phone and messaging vocabulary: cell phone/cellular phone, telephone number, text message, predictive text, push notification
-   Media vocabulary: photo, picture, podcast, preinstalled/preloaded, redownload

### Excluded

-   Wi-Fi, Bluetooth, and AirDrop/AirPlay capitalization and verb usage (see `capitalization-of-apple-proper-nouns`)
-   "Error message" and other malfunction/messaging-failure terms (see `app-state-and-error-terminology`)
-   "Sync" and "upload" (see `ui-action-verbs`)

## Rules

Two patterns recur across this table. First, several rows replace a
developer-slang or overly technical synonym with Apple's plain-language
preferred term (mobile phone, download again, help tag-style precision);
agents MUST substitute the listed Correct Form rather than the discouraged
synonym. Second, for connectivity-state terms (online, offline, pair), a
more specific description is preferable to the bare adjective whenever
precision matters, per each row's Notes.

| Term | Correct Form | Notes |
|---|---|---|
| cell phone, cellular phone | Don't use; use "mobile phone" | Don't use "mobile phone" as a synonym for iPhone (Rule 1) |
| offline | Use for a device or account not connected to the internet/network | OK informally for people ("go offline"); prefer "not connected to the internet" when precision matters (Rule 2) |
| onboard (adj., v.) | Use "built in" or "internal" unless specifically about board attachment | Don't use "onboard" as a verb in user materials; OK as a verb only in internal communications (Rule 3) |
| online | One word; describes content/services available on the internet/a network | OK informally for people/devices if context is clear; prefer "connected to the internet" or "signed in" (Rule 4) |
| pair, paired | Pair a device WITH another device, not "to" | Use "paired iPhone"/"paired Apple Watch," not "companion iPhone" (Rule 5) |
| photo | The primary term for photographic images; don't use "photograph" | "image," "picture," or "shots" are OK synonyms depending on context (Rule 6) |
| picture | OK as a synonym for "photo" | Also OK in set phrases: "desktop picture," "profile picture" (Rule 7) |
| podcast, podcasting | Use "podcast" or "show"; don't use "pod" | Italicize a podcast's title; quote an episode's title (Rule 8) |
| predictive text | Use for the iOS/macOS feature that predicts the next word | Use "typing suggestions" or "suggestions" for what users see onscreen (Rule 9) |
| preinstalled, preloaded | Avoid; say "installed," "loaded," or "included" | (Rule 10) |
| push notification | Developer materials only; user materials use "notification" | Lowercase except in proper names, e.g. Apple Push Notification service (Rule 11) |
| redownload | Don't use; use "download again" | (Rule 12) |
| telephone number | Don't use; use "phone number" | (Rule 13) |
| text message | OK to shorten to "message" if context is clear | Avoid "text"/"texts" as nouns; "text" as a verb is OK only informally (Rule 14) |

## Compliant Example

-   ✓ "Connect your mobile phone to continue." (Rule 1)
-   ✓ "You can read your saved articles at any time—even when you're not connected to the internet." (Rule 2)
-   ✓ "Built-in storage" not "onboard storage" (Rule 3)
-   ✓ "To use Siri, you must have an internet connection." (Rule 4)
-   ✓ "To use Apple Watch, pair it with iPhone." (Rule 5)
-   ✓ "You can use Photos to view, edit, and share your photos." (Rule 6)
-   ✓ "Search for any podcast by name." (Rule 8)

## Non-Compliant Example

-   ✗ "Enter your cell phone number." (Rule 1)
-   ✗ "To use Siri, you must be online." stated as a device requirement (Rule 4)
-   ✗ "Pair Apple Watch to iPhone." (Rule 5)
-   ✗ "Search for any pod by name." (Rule 8)
-   ✗ "This app comes preinstalled on your Mac." (Rule 10)
-   ✗ "Your server generates push notifications" in user-facing help text (Rule 11)
-   ✗ "Redownload the app from the App Store." (Rule 12)
-   ✗ "Enter your telephone number." (Rule 13)
-   ✗ "You have 3 unread texts." (Rule 14)

## Dependencies

None.

## References

-   [Apple Style Guide — cell phone, cellular phone (p. 48)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — offline (p. 150); onboard (adj., v.) (p. 151); online (p. 151)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — pair, paired (p. 153)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — photo (p. 157); picture (p. 158)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — podcast, podcasting (p. 162)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — predictive text (p. 165); preinstalled, preloaded (p. 165)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — push notification (p. 171); redownload (p. 175)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — telephone number (p. 202); text message (p. 203)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
