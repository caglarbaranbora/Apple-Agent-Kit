# Touch Gesture Verbs

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.style-guide.touch-gesture-verbs
type: knowledge
title: Touch Gesture Verbs
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the correct verbs for touchscreen, trackpad, and Apple Vision Pro gestures, and which gesture terms are user-facing versus developer-only.
domain: Style Guide
tags:
  - style-guide
  - ui-text
  - gestures
references:
  - https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
depends_on: []
related:
  - knowledge.style-guide.input-controls
  - knowledge.style-guide.navigation-controls
  - knowledge.style-guide.presentation-surfaces
updated: 2026-07-30
```

## Intent

This contract defines how an AI coding agent describes touch and trackpad
gestures — tap, swipe, pinch, drag, and related verbs — in UI text and
documentation for Apple platforms, including which gesture terms are
restricted to developer materials.

## Scope

### Included

-   Core gesture verbs: tap, double tap, touch and hold, swipe, pinch, rotate, zoom, drag, scroll, slide, flick
-   Compound/discouraged forms: tap and hold, drag and drop, long press, press and hold, hold down, jiggle, wiggle
-   The umbrella term "gestures" and the term "haptic"/"haptics"

### Excluded

-   Input controls these gestures operate, e.g. slider, switch, stepper (see `input-controls`)
-   Navigation buttons and arrows (see `navigation-controls`)
-   Presentation surfaces gestures act on, e.g. sheet, popover, action sheet (see `presentation-surfaces`)

## Rules

Two rules apply across the whole table. First, agents MUST NOT include the
word "finger" in gesture instructions unless the gesture involves multiple
fingers or needs disambiguation ("Swipe left or right," not "Swipe your
finger left or right"). Second, several terms below (long press, flick)
are developer-materials-only; agents MUST use the listed user-materials
replacement in user-facing text.

| Term | Correct Form | Notes |
|---|---|---|
| gestures | Finger movements on a touchscreen, trackpad, or with Apple Vision Pro | Don't say "finger gestures"; just "gestures" (Rule 1) |
| tap | Quickly touching and releasing the touchscreen/trackpad, or briefly touching thumb and finger on Vision Pro | Don't use "tap on" (Rule 2) |
| tap and hold | Don't use | "Tap" means touch-and-release quickly; use "touch and hold" (Rule 3) |
| touch and hold | Touching a touchscreen and leaving the finger motionless until an action or result occurs | Don't use "tap and hold"; don't use "long press" in user materials (Rule 4) |
| double tap | double tap (n.), double-tap (v.), double-tapping (n., v.) | Note hyphenation of the verb/gerund forms (Rule 5) |
| swipe | Quickly sliding one or more fingers across the touchscreen/trackpad, or pinching thumb and finger while flicking the wrist on Vision Pro | (Rule 6) |
| pinch | Placing two fingers on the touchscreen/trackpad and moving them closer together or farther apart | "pinch open"/"pinch closed" for added detail (Rule 7) |
| rotate | Placing two fingers slightly apart on the touchscreen/trackpad and twisting clockwise/counterclockwise | Don't use for turning the Digital Crown; use "turn" (Rule 8) |
| zoom, Zoom | Lowercase for the zooming action (zoom in, zoom in on, zoom out, zoom out of) | Capitalize only for the Zoom accessibility feature (Rule 9) |
| drag | Moving an onscreen item or control, varies by device (pointer+mouse/trackpad on desktop; one-finger move on touchscreen) | Don't use "click and drag," "drag the mouse/pointer," or "place/put/move" for drag (Rule 10) |
| drag and drop | drag and drop (n., v.), drag-and-drop (adj.) | Don't use as a compound verb taking an object — dragging includes dropping (Rule 11) |
| jiggle | Use for the movement of app icons being rearranged or deleted | Not "wiggle" (Rule 12) |
| wiggle | Don't use for icon movement | Use "jiggle" (Rule 13) |
| long press | Developer materials only, for the gesture recognizer | Don't use in user materials; use "press and hold" or "touch and hold" (Rule 14) |
| press and hold | Pressing a mouse/trackpad, key, or mechanical button until an action or result occurs | Don't use "hold down"; don't confuse with "click and hold" (Rule 15) |
| hold down | Don't use | Use "press and hold" (Rule 16) |
| scroll | Avoid as a transitive verb ("Scroll through a document," not "Scroll a document") | Prefer over specific gestures like drag/swipe when describing moving through content (Rule 17) |
| slide | Avoid as a verb for operating a slider or switch | Use "tap," "click," or "drag" instead (Rule 18) |
| flick | Developer documentation only | In user materials, use "swipe" (Rule 19) |
| haptic, haptics | Technology that uses touch (e.g., a tap) to give feedback | Define "haptics" on first use; prefer describing what the user feels ("you feel a tap") (Rule 20) |

## Compliant Example

-   ✓ "Swipe left or right." (Rule 1)
-   ✓ "Tap Return to move from one field to another." (Rule 2)
-   ✓ "Touch and hold the Mute button to hold a call." (Rule 4)
-   ✓ "A simple double tap lets you zoom in." (Rule 5)
-   ✓ "Pinch the photo to zoom in or out." (Rule 7)
-   ✓ "Drag the Volume slider to change the volume." (Rule 10)
-   ✓ "Scroll through a document." (Rule 17)
-   ✓ "You feel a tap when your message is sent." (Rule 20)

## Non-Compliant Example

-   ✗ "Swipe your finger left or right." (Rule 1)
-   ✗ "Tap on the video you want to play." (Rule 2)
-   ✗ "Tap and hold the Mute button." (Rule 3, Rule 4)
-   ✗ "Long press the icon to open options." in user materials (Rule 14)
-   ✗ "Hold down the power button to restart." (Rule 16)
-   ✗ "Scroll a document." used transitively (Rule 17)
-   ✗ "Slide the switch to turn Airplane Mode on." (Rule 18)
-   ✗ "Flick to the next photo." in user materials (Rule 19)

## Dependencies

None.

## References

-   [Apple Style Guide — gestures (pp. 93–94)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — tap (n., v.); tap and hold (p. 201)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — touch and hold (p. 206)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — double tap (n.) (p. 73)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — swipe (n., v.) (p. 195); pinch (v.) (p. 159); rotate (p. 177)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — zoom, Zoom (p. 222)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — drag (pp. 74–75); drag and drop (n., v.) (p. 75)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — jiggle (p. 118); wiggle (p. 219)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — long press (n.) (p. 130); press and hold (p. 167); hold down (p. 101)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — scroll (p. 179); slide (v.) (p. 188); flick (n., v.) (p. 88)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
-   [Apple Style Guide — haptic (adj.), haptics (n.) (p. 98)](https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf)
