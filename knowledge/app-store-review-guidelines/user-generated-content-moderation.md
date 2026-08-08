# User-Generated Content Moderation

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.app-store-review-guidelines.user-generated-content-moderation
artifact_type: knowledge
title: User-Generated Content Moderation
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the four moderation mechanisms guideline 1.2 requires of any app carrying user-generated content or social networking — a filter for objectionable material, a report mechanism backed by timely response, the ability to block abusive users, and published contact information — plus the default-hidden rule for incidental NSFW content from a web service and the categories Apple removes without notice.
domain: App Store Review Guidelines
tags:
  - app-store-review-guidelines
  - safety
  - user-generated-content
  - moderation
references:
  - https://developer.apple.com/app-store/review/guidelines/#1.2
depends_on: []
related:
  - knowledge.app-store-review-guidelines.developer-contact-information
  - knowledge.app-store-review-guidelines.spam-duplicate-apps
last_updated: 2026-08-08
```

## Intent

This contract defines what an agent must build into any app where one user
can see another user's content. Its central claim is that guideline 1.2
lists four mechanisms and requires all four: three of them are product
features that have to exist in the shipped binary, so they cannot be added
during an appeal. An app that accepts a photo, a comment, a display name, or
a profile bio from one user and shows it to another is in scope, whether or
not it calls itself a social app.

## Scope

### Included

-   The four mechanisms guideline 1.2 requires, and what each must do
-   Incidental mature content from a web-based service
-   The categories removed without notice, and the removal process

### Excluded

-   Objectionable content as a content judgment (guideline 1.1) — Excluded;
    no implementation rule decides whether content is in poor taste
-   Creator-platform age restriction (guideline 1.2.1) — Excluded as vertical
-   Where the contact information itself must appear — see
    `developer-contact-information`
-   Reporting UI design and wording — owned by `human-interface-guidelines`

## Rules

### Rule 1

Agents MUST include a method for filtering objectionable material before it
is posted. Per Apple, apps with user-generated content "must include… a
method for filtering objectionable material from being posted to the app."
The filter runs at post time, not at view time — a moderation queue that
publishes first and reviews later does not satisfy it.

### Rule 2

Agents MUST include a mechanism to report offensive content, and MUST NOT
treat the button as the whole requirement. Apple requires "a mechanism to
report offensive content **and timely responses to concerns**", so a report
that lands nowhere is a partial implementation. The report path needs a
destination that a person reads.

### Rule 3

Agents MUST include the ability to block abusive users from the service. A
mute that only hides content from the reporter is not a block: the guideline
names blocking "from the service", so the blocked user must lose the ability
to reach the person who blocked them.

### Rule 4

Agents MUST publish contact information reachable from the app, as the
fourth required mechanism — "published contact information so users can
easily reach you". This is the same obligation guideline 1.5 imposes on
every app; for a UGC app it is also a 1.2 requirement, so failing it is two
findings rather than one. See `developer-contact-information`.

### Rule 5

Agents MUST hide incidental mature content by default and MUST NOT ship the
categories Apple removes on sight. Per Apple, an app displaying UGC from a
web-based service "may display incidental mature 'NSFW' content, provided
that the content is hidden by default and only displayed when the user turns
it on via your website." Apps used primarily for pornographic content,
Chatroulette-style or anonymous random chat, "hot-or-not" objectification of
real people, physical threats, or bullying "do not belong on the App Store
and may be removed without notice."

## Compliant Example

-   ✓ Comment submission runs through a text filter and an image classifier before the comment becomes visible to anyone. (Rule 1)
-   ✓ Every comment and profile carries a Report action that files a ticket into a queue with a named owner and a response target. (Rule 2)
-   ✓ Blocking a user removes the blocker from that user's reach entirely — no DMs, no comment replies, no profile view. (Rule 3)
-   ✓ A Support entry in Settings shows an email address and links to the same address published on the app's Support URL. (Rule 4)

## Non-Compliant Example

-   ✗ Posts appear immediately and are reviewed only if someone complains. (Rule 1)
-   ✗ A Report button opens a `mailto:` link to an unmonitored address. (Rule 2)
-   ✗ "Block" only hides the blocked user's posts from the blocker's feed, while the blocked user can still send direct messages. (Rule 3)
-   ✗ A photo-sharing app carries user avatars and captions and treats guideline 1.2 as applying only to apps with a chat feature. (Rules 1, 2, 3)

## Dependencies

None.

## References

-   [Apple App Review Guidelines — 1.2 User-Generated Content](https://developer.apple.com/app-store/review/guidelines/#1.2)
