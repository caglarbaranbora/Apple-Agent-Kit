# Motion

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.human-interface-guidelines.motion
artifact_type: knowledge
title: Motion
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines rules for using animation and motion purposefully in iOS/iPadOS interfaces, including Reduce Motion accessibility support.
domain: Human Interface Guidelines
tags:
  - human-interface-guidelines
  - motion
  - design
references:
  - https://developer.apple.com/design/human-interface-guidelines/motion
depends_on: []
related:
  - knowledge.human-interface-guidelines.accessibility
  - knowledge.human-interface-guidelines.sf-symbols
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent uses motion/animation
purposefully on iOS/iPadOS: pairing motion with non-motion cues,
supporting Reduce Motion, and keeping feedback animations brief,
interruptible, and gesture-consistent.

## Scope

### Included

-   Motion as a non-exclusive information channel
-   Reduce Motion accessibility-setting response
-   Brevity and precision of feedback animation
-   Interruptibility of animation
-   Gesture-consistent motion physics

### Excluded

-   SF Symbol animation implementation — deferred to a future dedicated `sf-symbols` API domain, not covered by any current contract
-   General accessibility rules unrelated to motion — see `accessibility`

## Rules

### Rule 1

Agents MUST NOT use motion as the only way to communicate important
information — pair it with a visual or textual cue.

### Rule 2

Agents MUST respond to the Reduce Motion accessibility setting by
reducing or removing automatic/repetitive animation (zooming, scaling,
peripheral motion) when it's turned on.

### Rule 3

Agents SHOULD keep feedback animations brief and precise rather than
long or elaborate.

### Rule 4

Agents MUST let people cancel or interrupt an animation rather than
blocking interaction until it completes.

### Rule 5

Agents SHOULD make motion follow realistic, gesture-consistent physics
(e.g., a view dismissed by swiping down shouldn't be reopened by
swiping sideways).

## Compliant Example

-   ✓ A card transition responds to Reduce Motion by cross-fading instead of scaling/zooming. (Rule 2)
-   ✓ People can tap through an in-progress animation to proceed immediately. (Rule 4)

## Non-Compliant Example

-   ✗ A decorative parallax animation plays regardless of the Reduce Motion setting. (Rule 2)
-   ✗ An animated onboarding sequence can't be skipped or interrupted. (Rule 4)

## Dependencies

None.

## References

-   [Apple HIG — Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
