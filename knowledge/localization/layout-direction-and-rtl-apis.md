# Layout Direction and RTL APIs

Status: Draft
Version: 0.1.0

## Metadata

```yaml
id: knowledge.localization.layout-direction-and-rtl-apis
artifact_type: knowledge
title: Layout Direction and RTL APIs
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines the API layer of right-to-left support -- leading and trailing over left and right, SwiftUI's automatic mirroring and why reading layoutDirection usually means double-flipping, flipsForRightToLeftLayoutDirection as a contents-mirroring modifier rather than an RTL switch, UIKit semanticContentAttribute whose unspecified default means flip, effectiveUserInterfaceLayoutDirection which does not inherit, SF Symbols name-driven mirroring, and detecting direction through Locale.Language.characterDirection.
domain: Localization
tags:
  - rtl
  - layout-direction
  - semantic-content-attribute
  - character-direction
  - sf-symbols-mirroring
references:
  - https://developer.apple.com/documentation/swiftui/layoutdirection
  - https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:)
  - https://developer.apple.com/documentation/uikit/uiview/semanticcontentattribute
  - https://developer.apple.com/documentation/uikit/uiview/effectiveuserinterfacelayoutdirection
  - https://developer.apple.com/documentation/uikit/uiimage/imageflippedforrighttoleftlayoutdirection()
  - https://developer.apple.com/documentation/uikit/creating-custom-symbol-images-for-your-app
  - https://developer.apple.com/documentation/foundation/locale/language-swift.struct/characterdirection
  - https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization
  - https://developer.apple.com/videos/play/wwdc2022/10107/
depends_on: []
related:
  - knowledge.human-interface-guidelines.right-to-left
  - knowledge.localization.locale-and-language-resolution
  - knowledge.sf-symbols.symbol-variants
last_updated: 2026-08-07
```

## Intent

This contract governs the APIs that make an interface work in right-to-left languages. Its central claim is that RTL support is mostly achieved by *not* writing direction-aware code -- the system mirrors automatically, and most RTL bugs come from either overriding that or from choosing absolutely-directional APIs and assets.

## Scope

### Included

- `leading`/`trailing` over `left`/`right`, in SwiftUI alignment and UIKit Auto Layout
- SwiftUI `LayoutDirection`, `\.layoutDirection`, automatic mirroring, and `flipsForRightToLeftLayoutDirection(_:)`
- UIKit `semanticContentAttribute`, `UISemanticContentAttribute`, `effectiveUserInterfaceLayoutDirection`
- `UIImage.imageFlippedForRightToLeftLayoutDirection()`, asset-catalog direction, and SF Symbols' automatic name-driven mirroring
- `Locale.Language.characterDirection`, `Locale.LanguageDirection`, and the RTL pseudolanguages

### Excluded

- RTL visual-design decisions -- what should mirror, numeral handling, whether an icon reads correctly reversed -- owned by `knowledge.human-interface-guidelines.right-to-left`
- Which localization the app resolved to -- see `locale-and-language-resolution`; localizing the assets themselves -- see `localized-resources-and-infoplist`
- Number and date formatting, including numeral systems -- owned by the `foundation` domain
- General SF Symbols rendering, variants, weight, and scale -- owned by the `sf-symbols` domain; this contract covers only RTL mirroring behavior

## Rules

### Rule 1

Agents MUST use leading/trailing rather than left/right for anything that follows reading order. Per Apple's WWDC22 session "Get it right (to left)": "The 'leading' edge of something is the edge closest to beginning of the line or to the side of the screen or window where the reader would begin reading, left for left to right and right for right to left… Most of the time, you want to use these instead of 'left' and 'right,' saving 'left' and 'right' only for things that are tied to an absolute direction." Per Apple's Internationalization guide: "When you use the Auto Layout `leading` and `trailing` attributes (not the `right` and `left` attributes), most of the user interface appears mirrored in right-to-left languages." Note this behavior is specified in those sources rather than on the `NSLayoutConstraint.Attribute` or `leadingAnchor` reference pages, which describe the anchors without stating their RTL semantics.

### Rule 2

Agents MUST NOT read `\.layoutDirection` in order to reorder content manually, because SwiftUI has already mirrored the layout. Per Apple's documentation for `LayoutDirection`: "in many cases, you don't need to take any action based on this value. SwiftUI horizontally flips the x position of each view within its parent, so layout calculations automatically produce the desired effect for both modes without any changes." Reversing a stack's contents in response to the value applies a second flip and restores left-to-right order.

### Rule 3

Agents MUST treat `flipsForRightToLeftLayoutDirection(_:)` as a way to mirror one view's *contents*, not as a switch that enables RTL layout, and MUST NOT apply it broadly. Per Apple's documentation it "Sets whether this view mirrors its contents horizontally when the layout direction is right-to-left," and its parameter documentation states: "By default, views will adjust their layouts automatically in a right-to-left context and do not need to be mirrored."

### Rule 4

Agents MUST set an explicit `semanticContentAttribute` on UIKit views that must not mirror, because the default value mirrors. Per Apple's WWDC22 session: "The default is 'Unspecified,' which causes the control to reverse its appearance." Per Apple's documentation the opt-outs are semantic: `playback` is "A view representing the playback controls, such as Play, Rewind, or Fast Forward buttons or playhead scrubbers," and `spatial` is "A view representing a directional control, such as a segment control for text alignment, or a D-pad control for a game." Apple's guidance is to pick by meaning: "Instead of thinking about whether or not a view should change its orientation, select the semantic content attribute that best describes your view."

### Rule 5

Agents MUST read `effectiveUserInterfaceLayoutDirection` on the view whose immediate content is being arranged, and MUST NOT cache it for a subtree. Per Apple's documentation: "When a view's immediate content is being arranged or drawn, you should always consult the value of this property. In addition, note that you can't assume that the value propagates through the view's subtree." Apple also directs agents toward this property over the class method: on `userInterfaceLayoutDirection(for:relativeTo:)`, "Although layout and drawing code can use this method to determine how to arrange elements, it might be easier to query the container view's `effectiveUserInterfaceLayoutDirection` property instead."

### Rule 6

Agents MUST choose SF Symbols by directional semantics, because mirroring is automatic and driven by the symbol's name with no API to request it. Per Apple's WWDC22 session: "SF Symbols follows this naming convention throughout with icons that you may or may not want to have flip for right to left. The 'forward' and 'backward' ones flip, and the 'left' and 'right' ones don't," and "remember that 'left' and 'right' always point those directions and 'forward' and 'backward' point in different directions depending on the UI language." Per Apple's documentation on custom symbols: "Image variants adapt automatically according to the user's device language, including right-to-left writing systems." A back button therefore uses `chevron.backward`, not `chevron.left`.

### Rule 7

Agents MUST NOT assume `imageFlippedForRightToLeftLayoutDirection()` returns a mirrored image. Per Apple's documentation: "This method returns the current `UIImage` object with the `flipsForRightToLeftLayoutDirection` property set to `true`; it does not return a flipped image." The mirroring happens at display time, and Apple scopes it to display "in a `UIImageView` object," so custom drawing of that image does not flip. For custom artwork agents MUST opt each asset in explicitly: per Apple's asset catalog reference, with no direction set "The image has a fixed horizontal orientation and will display in the same direction."

### Rule 8

Agents MUST detect writing direction through `Locale.Language.characterDirection` and MUST test for right-to-left explicitly. Per Apple's documentation, `Locale.characterDirection(forLanguage:)` is deprecated as of iOS 16.0 with the replacement note "Use `Locale.Language(identifier:).characterDirection` instead." `Locale.LanguageDirection` has five cases -- `unknown`, `leftToRight`, `rightToLeft`, `topToBottom`, `bottomToTop` -- so a negated comparison against `.leftToRight` also matches unknown languages and vertical scripts.

### Rule 9

Agents SHOULD exercise RTL through the scheme's pseudolanguages rather than requiring an RTL localization, and SHOULD use the strings variant to catch bidirectional text problems. Per Apple's documentation, "Right-to-Left Pseudolanguage" "Simulates a right-to-left writing direction to test whether views flip accordingly," while "Right-to-Left Pseudolanguage With Right-to-Left Strings" "Simulates a right-to-left writing direction, using right-to-left strings."

## Compliant Example

```swift
HStack {                                        // Rule 2: no manual reordering
    VStack(alignment: .leading) { Text("Article Title") }   // Rule 1: not .left
    Spacer()
    Image(systemName: "chevron.forward")        // Rule 6: forward mirrors
}
.padding(.leading, 16)                          // Rule 1

// Rule 3: mirror one directional glyph's contents, not the screen.
Image("custom-reply-arrow").flipsForRightToLeftLayoutDirection(true)

let isRTL = Locale.current.language.characterDirection == .rightToLeft  // Rule 8
playbackScrubber.semanticContentAttribute = .playback                  // Rule 4
let direction = containerView.effectiveUserInterfaceLayoutDirection     // Rule 5
```

## Non-Compliant Example

```swift
// violates Rule 2 -- SwiftUI already mirrored the stack, so reversing here
// flips it back to left-to-right in Arabic.
@Environment(\.layoutDirection) private var direction
HStack {
    if direction == .rightToLeft { ForEach(items.reversed()) { ItemView($0) } }
    else { ForEach(items) { ItemView($0) } }
}

Image(systemName: "chevron.left")   // violates Rule 6 -- never mirrors
let scrubber = UISlider()           // violates Rule 4 -- default mirrors, so
                                    // time appears to run backwards in Arabic

// violates Rule 8 -- also true for .unknown and for vertical scripts.
let isRTL = Locale.current.language.characterDirection != .leftToRight
```
Reverses content SwiftUI has already mirrored, producing a double flip (Rule 2); pairs an absolutely-directional symbol with a back action so it points the wrong way under RTL (Rule 6); leaves a playback control at the mirroring default (Rule 4); and treats a five-case enumeration as a boolean, so unknown languages and vertical scripts are misreported as right-to-left (Rule 8).

## Dependencies

None within this domain. Cross-references `knowledge.human-interface-guidelines.right-to-left` via `related:` for the design layer this contract deliberately does not cover, and `knowledge.sf-symbols.symbol-variants` for general symbol usage beyond mirroring behavior.

## References

- [Apple Developer — LayoutDirection](https://developer.apple.com/documentation/swiftui/layoutdirection) · [flipsForRightToLeftLayoutDirection(_:)](https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:))
- [Apple Developer — UIView.semanticContentAttribute](https://developer.apple.com/documentation/uikit/uiview/semanticcontentattribute) · [UISemanticContentAttribute](https://developer.apple.com/documentation/uikit/uisemanticcontentattribute) · [effectiveUserInterfaceLayoutDirection](https://developer.apple.com/documentation/uikit/uiview/effectiveuserinterfacelayoutdirection)
- [Apple Developer — imageFlippedForRightToLeftLayoutDirection()](https://developer.apple.com/documentation/uikit/uiimage/imageflippedforrighttoleftlayoutdirection()) · [Creating custom symbol images](https://developer.apple.com/documentation/uikit/creating-custom-symbol-images-for-your-app)
- [Apple Developer — Locale.Language.characterDirection](https://developer.apple.com/documentation/foundation/locale/language-swift.struct/characterdirection) · [NSLocale.LanguageDirection](https://developer.apple.com/documentation/foundation/nslocale/languagedirection)
- [Apple Developer — Preparing your interface for localization](https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization)
- [Apple Developer — Supporting Right-to-Left Languages (archived)](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/SupportingRight-To-LeftLanguages/SupportingRight-To-LeftLanguages.html)
- [WWDC22 — Get it right (to left)](https://developer.apple.com/videos/play/wwdc2022/10107/)
