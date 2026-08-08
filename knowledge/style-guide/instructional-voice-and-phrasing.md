# Instructional Voice and Phrasing

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.style-guide.instructional-voice-and-phrasing
artifact_type: knowledge
title: Instructional Voice and Phrasing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines sentence-level phrasing and point-of-view rules — avoiding first person, "please," and reader-distancing constructions — that shape the tone of onboarding, instructional, and error copy.
domain: Style Guide
tags:
  - style-guide
  - voice
  - phrasing
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.app-state-and-error-terminology
  - knowledge.style-guide.general-button-labels
  - knowledge.style-guide.ui-action-verbs
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent chooses point of view and
phrasing at the sentence level — addressing the reader as "you" instead of
"the user," avoiding first person, and stating instructions directly rather
than softening or conditionalizing them — when writing onboarding,
instructional, or error copy for Apple platforms.

## Scope

### Included

-   Point-of-view rules: first person, "we," "user," "end user," "capability"
-   Instructional bluntness rules: "please," "if necessary," "optionally," "prompt"
-   Word-choice rules: "and/or," "can/might/may," "desire/desired," "jargon," "once," "shows up," "under"

### Excluded

-   "User name" spelling and general button-label wording (see `general-button-labels`)
-   "Allow" as a verb and permission-prompt phrasing (see `general-button-labels`)
-   "Let" as a verb (see `ui-action-verbs`)
-   Malfunction and app-lifecycle vocabulary such as "error message" (see `app-state-and-error-terminology`)

## Rules

Two patterns recur across this table. First, several rows are point-of-view
rules: agents MUST address the reader as "you" and MUST NOT use first-person
pronouns ("we," "us," "I") or the noun "user" where the reader can instead be
the subject of the sentence. Second, several rows are instructional-bluntness
rules: agents MUST state an instruction or condition directly rather than
softening it with "please," hedging it with "if necessary" or "optionally,"
or narrating the system's role in delivering it with "prompt."

| Term | Correct Form | Notes |
|---|---|---|
| and/or | Rewrite to avoid the construction | "document and app icons," not "document and/or app icons" (Rule 1) |
| can/might/may | can = capacity; might/may = possibility; may = permission | might suggests lower probability than may (Rule 2) |
| capability | Reword in terms of what the user can do with the feature | Avoid if possible when discussing software/hardware features (Rule 3) |
| desire/desired | Don't use "desire"; avoid "desired" | "select the folder," not "select the desired folder" (Rule 4) |
| end user | Avoid in favor of "user" | (Rule 5) |
| first person | Don't use "we," "us," or "I"; rewrite in terms of the reader or the product | (Rule 6) |
| if necessary | Avoid in user materials | Describe the circumstance instead: "If file sharing isn't on, turn it on." (Rule 7) |
| jargon | Avoid whenever possible | Define technical terminology on first occurrence (Rule 8) |
| once | Don't use to mean "after" | (Rule 9) |
| optionally | Avoid in user materials | Describe the reason, or use "If you want to…" (Rule 10) |
| please | Avoid in instructional text and cross-references | (Rule 11) |
| prompt | Avoid as a verb when you can just tell users what to do | OK as noun/adjective for a command-line prompt character; use passive voice if used as a verb (Rule 12) |
| shows up | Don't use; use "appears" | (Rule 13) |
| under | Don't use for an OS environment, a menu location, or an interface location | Use "in," "with," or "below" instead (Rule 14) |
| user | Avoid when addressing the reader directly; address them as "you" | OK when the audience is developers/administrators, to distinguish end users from the reader (Rule 15) |
| we | Don't use first person; rewrite in terms of the reader or the product | (Rule 16) |

## Compliant Example

-   ✓ "document and app icons" (Rule 1)
-   ✓ "You might be able to connect to the internet at a nearby hotspot." (Rule 2)
-   ✓ "With Photos, you can create slideshows." (Rule 3)
-   ✓ "If file sharing isn't on, turn it on." (Rule 7)
-   ✓ "Follow the steps below." (Rule 11)
-   ✓ "Double-click the side button, and then enter your passcode." (Rule 12)
-   ✓ "The Portrait Lighting slider appears below the frame." (Rule 13)
-   ✓ "You can make movies with effects and a soundtrack." (Rule 15)

## Non-Compliant Example

-   ✗ "document and/or app icons" (Rule 1)
-   ✗ "Photos has the capability to create slideshows." (Rule 3)
-   ✗ "select the desired folder" (Rule 4)
-   ✗ "If necessary, turn on file sharing." (Rule 7)
-   ✗ "Please follow the steps below." (Rule 11)
-   ✗ "Enter your passcode when prompted." (Rule 12)
-   ✗ "The Portrait Lighting slider shows up below the frame." (Rule 13)
-   ✗ "Users can make movies with effects and a soundtrack." (Rule 15)
-   ✗ "We recommend that the image be at least 600 x 600 pixels." (Rule 16)

## Dependencies

None.

## References

-   [Apple Style Guide — and/or (p. 19); can, might, may (p. 45); capability (p. 45)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — desire (p. 65); desired (p. 65); end user (n.), end-user (adj.) (p. 81)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — first person (p. 87); if necessary (p. 108); jargon (p. 118)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — once (p. 151); optionally (p. 152); please (p. 161)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — prompt (n., v., adj.) (p. 169); shows up (p. 185)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — under (p. 209); user (p. 212); we (p. 217)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
