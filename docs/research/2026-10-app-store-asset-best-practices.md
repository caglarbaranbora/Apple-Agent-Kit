# App Store Asset Best Practices Research — October 2026

Status: Research note (not a normative artifact — not a Reference/Knowledge/Skill/Workflow)

## Context

The user found Apple's "App Store asset best practices and resources" page
(https://developer.apple.com/app-store/asset-best-practices/) and reported that it
had recently added "Header and search results" and "App previews and screenshots"
sections. This note records what the page says, dates its changes, follows its
first-party links, and compares it against the repo's current coverage.

Method: every page was fetched live on **2026-10-15** with `curl -L` (raw,
server-rendered HTML; the page is not JS-rendered) and converted to text. WebFetch
returned only a summary, so all quotes below come from the raw HTML. Every URL listed
returned HTTP 200 with **zero redirects** unless noted. To date the changes, Internet
Archive snapshots of the same URL (2026-08-10, 08-25, 09-16, 09-17, 10-06) were
compared. They are used only to establish dates. They are not cited as authority.

## Headline finding

**Part of the premise is wrong, but the content is real and almost none of it is
covered in this repo.**

- The page is **not newly restructured**. The "Product page header", "Search results",
  "Screenshots" and "App previews" sections were all already there in the earliest
  archived capture (2026-08-10). Apple Developer News called the page "new" on
  **2026-08-05** ("Get ready for new creative assets on the App Store",
  https://developer.apple.com/news/?id=kug6m2ea).
- What did change since August is minor:
  1. Between 08-10 and 08-25, "Universal" template links were added to the header and
     search-results template lists.
  2. Between 08-25 and 09-16, Sketch templates were added.
  3. Between 09-17 and 10-06, an **iPhone Duo banner** was added at the top, plus
     "View screenshot specifications" and "View app preview specifications" links
     inside the Screenshots and App previews sections. This matches the
     **2026-10-05** news posts "Showcase your apps with new assets on the App Store"
     (https://developer.apple.com/news/?id=ljpl7kyn) and "Prepare and submit your
     apps for iPhone Duo" (https://developer.apple.com/news/?id=kkphp5qo).
- The page itself has no "updated" or date marker (only "Copyright © 2026").
- The actually new **normative** material is on other pages:
  - a new App Review guideline-reference page for 2.3.3, which carries a quantitative
    "more than half of screenshots" rule;
  - a new App Store Connect "Creative assets specifications" page (header and
    search-result dimensions and durations);
  - new iPhone Duo screenshot and app preview sizes, with an **April 2027**
    screenshot requirement.
- Repo coverage: `screenshots-accuracy.md` covers 2.3.3/2.3.4 at the guideline-text
  level only. Creative assets (header, search results), In-App Event media, every
  asset spec number, guidelines 2.3.2/2.3.8/2.3.9/2.3.10/2.3.13, and all of the
  advisory craft guidance have **zero coverage**.

---

## 1. App Store asset best practices and resources (primary source)

- URL: https://developer.apple.com/app-store/asset-best-practices/ (200, no redirect;
  `http://` → 301 → `https://`, which is the form two news posts link to)
- Top banner (added between 2026-09-17 and 2026-10-06): "Make your apps shine with
  assets optimized for iPhone Duo. View the specifications for app previews and
  screenshots."

### Overview / "Before you begin"

> "App previews and screenshots showcase your app in-use or gameplay, while creative
> assets can be used to highlight your brand, promote seasonal offerings, showcase new
> content, and more. Creative assets appear across the App Store in iOS 27 and iPadOS
> 27 and later including your product page, in search results, and when your app is
> featured."

> "…get familiar with the App Review Guidelines (particularly section 2.3 about
> Accurate Metadata) and the Apple Advertising Policies before you start creating."

### Asset best practices: "Focus on your core experience"

> "While you may depict content outside of your app or game in use, it must still
> relate to its general functionality."
> - "Don't include specific pricing, discounts, website URLs, copyright symbols."
> - "Avoid claims that can't be verified, such as awards or recognition that your app
>   or game hasn't actually received."
> - "Don't include logos or references to other platforms or marketplaces."
> - "Please don't include any Apple-designated recognitions — such as Editor's
>   Choice, App of the Day, Game of the Day, or Apple Design Award winner…"

### "Design with all customers in mind"

> "Build for a global audience. … You can localize your metadata, including images and
> videos…"

> "Create for all ages. … Assets displayed on the App Store must meet a 4+ age rating,
> even if your app's rating is higher… Refrain from showing objectionable content,
> including explicit or harmful imagery, profanity, illegal drugs, self-harm, hate
> speech, stereotypes, sexually suggestive content, inflammatory religious commentary,
> or inaccurate and misleading quotations of religious texts."

> "Keep violent content in check. Games that include violence may use action imagery,
> but must avoid depictions of gore, graphic imagery, or weapons that are pointed
> directly at a person or the audience."

### Format best practices: Image

> - "Choose compelling visuals. … Aim for strong composition and a clear focal point
>   for each asset."
> - "Be intentional with your text. … use a short phrase that enhances your visual
>   rather than describes it. Be sure to localize for all languages your app
>   supports."
> - "Keep it legible. … Design key elements with a safe area in mind to accommodate
>   different devices and orientations. Be sure your focal point artwork is within the
>   center of your composition to prevent any unwanted clipping. You can use the
>   Preview tool in App Store Connect…"

### Format best practices: Videos

> - "Select an impactful poster frame. The poster frame is the first image someone
>   sees before your video plays."
> - "Start strong. Lead with your value proposition or most compelling feature. …
>   Avoid quick cuts and fast-moving visuals, as these can be difficult for people to
>   follow and may not be accessible for everyone."
> - "Loop seamlessly. Videos autoplay and repeat…"
> - "Use audio mindfully. In most cases, audio is muted by default, so your creative
>   must work silently first. … Favor a short music loop over heavy sound effects,
>   avoid sudden loud moments, and ensure the audio loops cleanly…"

### Asset-specific guidelines ("Design for every element")

> "Collectively, you want them to tell a cohesive story and look good together. … consider
> using similar visual style, such as color palette, iconography, fonts, message, and
> tone."

- **App icon:**
  > "Use Icon Composer to create layered icons out of Liquid Glass from a single design
  > for iPhone, iPad, Mac, and Apple Watch."
  >
  > "Ensure your icon is legible at every size across Apple devices…"

  Links to HIG app-icons, and to WWDC26 8012 and WWDC25 220.
- **Product page header:**
  > - "Focus on a single, clear idea. Visually dense or cluttered assets dilute your impact."
  > - "Design with a first-time visitor in mind."
  > - "…you can use a universal creative asset for your header and search results asset…
  >   you can use product page optimization to test alternative header visuals…"

  Templates are offered for Figma (Universal), Photoshop (Header, Universal),
  Pixelmator (Header, Universal) and Sketch (Universal). The links go through
  `/go/?id=…` redirect pages.
- **Search results:**
  > - "State the obvious. … be sure your app or game's purpose is obvious at a glance."
  > - "Showcase the firsthand experience."
  > - "If you choose to not use a search result creative asset, your In-App Events, app
  >   previews, and screenshots will appear."
- **In-App Events:**
  > "You need media for the event card (16:9 landscape) and the event details page (9:16
  > portrait)."
  >
  > "Your chosen badge (Challenge, Competition, Live Event, Major Update, New Season,
  > Premiere, Special Event)… Design your media to complement the badge rather than
  > duplicate it."
- **Screenshots:**
  > "You can have up to 10 screenshots on your product page. Depending on orientation, up
  > to three screenshots can appear in search results."
  >
  > - "Show what people can expect. … avoid using the entire asset to highlight general
  >   accolades or call-to-action statements."
  > - "Lead with your best features. … sequence them so they tell a cohesive story…"
- **App previews:**
  > "You can have up to three app previews on your product page and up to three may appear
  > in search results."
  >
  > - "Use real-UI or gameplay. … Consider compelling visuals in the first few seconds…"
  > - "Tell a complete story. Consider having a beginning, middle, and end…"

### Submit your assets

> "…submit your assets for approval using App Store Connect, either alongside a new app
> version, or in your Asset Library. You can also use the App Store Connect API."

> The product page preview tool shows "how your product page header, app name,
> description, screenshots, and search results creative assets will appear…"

---

## 2. Creative assets specifications (new App Store Connect Help page; normative specs)

- URL: https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
- The asset-best-practices page does **not** link here. It is reached from the
  2026-10-05 news post and from "Manage your App Store assets".

> "Creative assets include product page header, search results, and in-app event cards."
> "Note: Images can't include alpha channels or transparencies."

| Placement | Image | Video |
|---|---|---|
| Product page header | 21:9, 3840 x 1646, .jpeg/.jpg/.png; **or** 16:9, 5244 x 2950, .png | 21:9, 3840 x 1646, 30 or 60 fps, 5–30 s, .mov/.m4v/.mp4 |
| Search results | 3:2, min 1920 x 1280, max 3840 x 2560, .jpeg/.jpg/.png; **or** 16:9, 5244 x 2950, .png | 3:2, same min/max, 30 or 60 fps, 5–30 s |
| In-App Event card | 16:9, 1920 x 1080 – 3840 x 2160, max 500 MB | 16:9, 30 or 60 fps, **15–30 s** |
| In-App Event details page | 9:16, 1080 x 1920 – 2160 x 3840, max 500 MB | 9:16, 30 or 60 fps, 15–30 s |

> "Videos are muted by default in search results and can't currently be unmuted. On
> your product page, videos are also muted by default, but people can unmute them.
> Videos loop continuously in both placements."

**Unverified:** the 16:9 5244 x 2950 .png row appears under both header and search
results. That suggests it is the "universal" asset, but this page never labels it
that way. Do not encode that inference.

## 3. Manage your App Store assets (App Store Connect Help)

- URL: https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets

> "Creative assets are rich images or videos that showcase your app's or game's
> overarching value, brand, or excitement, **distinct from the in-use functionality
> requirement in app previews and screenshots**."

This sentence is the key boundary: creative assets are explicitly outside the 2.3.3
in-use rule.

> "Creative assets are optional and separate from your app's screenshots, app previews,
> In-App Purchase and Subscription images, and any promotional artwork requested by
> editorial teams."

> "If you upload a universal creative asset, you can use it for both your product page
> header and search results placement. … available for iOS and iPadOS apps and games
> running iOS 27 or iPadOS 27 or later."

> "Standalone assets are reviewed against your app's latest version."

> "Poster frames can't be edited after assets have been approved."

> Previews and screenshots "must meet Apple's guidelines and the App Review Guidelines
> (sections 2.3.3 and 2.3.4)."

Required role: "Account Holder, Admin, App Manager, or Marketing."

## 4. Screenshot specifications (App Store Connect Help; updated for iPhone Duo)

- URL: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications

> "You must include at least one screenshot and can upload up to 10 screenshots per
> device size in .jpeg, .jpg, or .png formats…"

> Required: "iPhone: At least one screenshot for iPhone with Dynamic Island (medium
> display)." and "iPad (if your app supports iPadOS): At least one screenshot for iPad
> 13-inch display."

> "If your app's user interface is consistent across multiple device sizes and
> localizations, you only need to provide screenshots for the highest required
> resolution." "Images can't include alpha channels or transparencies."

- **iPhone Duo:** 1398 × 2034 / 2034 × 1398 (outer display) and 2007 × 2853 /
  2853 × 2007 (inner display).
  > "Starting in April 2027, screenshots will be required for any app using the iOS
  > 27.1 SDK or later."
- **iPhone with Dynamic Island (medium):** 1179 x 2556 or 1206 x 2622 (portrait).
- **iPad 13":** 2064 x 2752 or 2048 x 2732.
- **Mac:** 16:10, one of 1280 x 800, 1440 x 900, 2560 x 1600, 2880 x 1800.
- **Apple TV:** 1920 x 1080 or 3840 x 2160.
- **Vision Pro:** 3840 x 2160.
- **Watch:** per-model sizes.
  > "You must use the same screenshot size for Apple Watch consistently across all
  > localizations."

Each size class also has a scaled-fallback chain.

**Conflict to flag.** The two sources state the iPhone Duo requirement differently:
- this page ties it to building with the iOS 27.1 SDK or later;
- the news posts say "Starting April 2027, any apps or games submitted will need to
  include screenshots for iPhone Duo" (https://developer.apple.com/news/?id=kkphp5qo
  and https://developer.apple.com/app-store/whats-new/).

Also, iPhone Duo screenshots trigger a product page badge:
> "When you submit iPhone Duo screenshots in App Store Connect, your App Store product
> page will display a badge…" (kkphp5qo)

## 5. App preview specifications (App Store Connect Help)

- URL: https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications

> "App previews are optional. You can upload up to three app previews per supported
> device size and language for iOS, macOS, tvOS, and visionOS apps."

> "App previews always appear before screenshots on iPhone, iPad, Mac, and Apple TV —
> even if you reorder them… If a preview video uses an aspect ratio different from
> your screenshots, it appears in the 'A Closer Look' section…"

- Max file size **500MB**.
- Length **15–30 seconds**.
- Default poster frame **5 seconds**.
- Max **30 fps**.
- H.264 at 10-12 Mbps, or ProRes 422 (HQ only) at ~220 Mbps VBR.
- Audio: stereo, 256kbps AAC (or PCM for ProRes), 44.1/48kHz.
- Processing time: "Up to 24 hours after upload."
- iMessage: "App previews are not available for apps on the App Store for iMessage."
- Orientation: macOS, tvOS and visionOS are landscape only.
- Accepted resolutions:
  - iPhone (19.5:9 class) and iPhone Duo: 886 x 1920 / 1920 x 886
  - iPad 13": 1200 x 1600 / 1600 x 1200
  - Mac and Apple TV: 1920 x 1080
  - Vision Pro: 3840 x 2160
  - 3.5" iPhone: "App previews aren't supported".

**Possible Apple-side error, unverified:** the iPhone Duo "Device resolutions" (2034 ×
1398, 2853 × 2007) are labeled "(19.5:9 aspect ratio)". Those sizes are about 1.45:1,
and the accepted resolution is identical to every other modern iPhone. This looks
like copy-paste. Don't encode the iPhone Duo preview resolution until Apple confirms
it.

## 6. App Review guideline reference: 2.3.3 (new App Review help page)

- URL: https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
- Announced as "new App Review guidance on how to avoid common screenshot issues"
  (https://developer.apple.com/news/?id=ljpl7kyn, 2026-10-05).

> "App Review takes the set of screenshots submitted for each supported device into
> account, and will approve only those submissions where **more than half of
> screenshots show the app in use**. As long as the majority of the screenshots show
> the app in use, your other screenshots can exhibit the app's main benefits and
> features using marketing materials…"

> "…if an app has three screenshots for each supported device, two … must show the app
> in use… If an app has four…, three must show the app in use…"

Do:
- "Update your screenshots with each new version so they match the current user
  interface."
- "Include screenshots that show your app operating in different configurations,
  such as Dark Mode."
- "Include splash screens or marketing text, as long as the majority of screenshots
  still show the app in use."

Don't:
- "Don't let overlays or marketing visuals crowd out your app."
- "Don't show only the hardware or an overlay with no app interface behind it."

> "Screenshots that reference third-party platforms, such as in a status bar, are
> assessed under App Review Guideline 2.3.10."

FAQ:
> "one screenshot for a device is sufficient as long as it shows your app in use";
> localized screenshots are each "assessed on whether the majority show your app in
> use"; "An image of an app in use can be displayed across multiple screenshots."

The guideline text itself (https://developer.apple.com/app-store/review/guidelines/,
"Last Updated: June 8, 2026") has **no** mention of creative assets or headers. The
2.3.x clauses the asset page relies on are:
- **2.3.2:** IAP must be indicated in "description, screenshots, and previews".
- **2.3.4:** previews "may only use video screen captures of the app itself".
- **2.3.7:** "Metadata such as app names, subtitles, screenshots, and previews should
  not include prices, terms, or descriptions that are not specific to the metadata
  type".
- **2.3.8:** "icons, screenshots, and previews adhere to a 4+ age rating".
- **2.3.9:** rights to materials; "display fictional account information instead of
  data from a real person".
- **2.3.10:** no "names, icons, or imagery of other mobile platforms or alternative app
  marketplaces".
- **2.3.13:** In-App Events metadata.

## 7. News timeline (https://developer.apple.com/news/rss/news.rss)

| Date | Post | Relevance |
|---|---|---|
| 2026-08-05 | "Get ready for new creative assets on the App Store" (?id=kug6m2ea) | Asset best practices page introduced as "new" |
| 2026-09-09 | "App Store submissions now open for the latest OS releases" (?id=k1mtkt1k) | Points to the page for headers and search results; product page preview tool "Coming soon" |
| 2026-10-05 | "Showcase your apps with new assets on the App Store" (?id=ljpl7kyn) | Creative assets, Asset Library and preview tool go live; new creative-assets spec page; new 2.3.3 guidance |
| 2026-10-05 | "Prepare and submit your apps for iPhone Duo" (?id=kkphp5qo) | Updated screenshot and preview specs; April 2027 iPhone Duo screenshot requirement; iPhone Duo badge |
| 2026-10-06 | "Hello Developer: October 2026" (?id=gv788oj6) | "Browse new App Store creative assets" |

## 8. Link and redirect findings (the repo treats redirects as findings)

| Where | Link | Finding |
|---|---|---|
| App preview specs, "Learn how to create videos for app previews" | `/support/app-previews/` | **301** → https://developer.apple.com/app-store/app-previews/ |
| Creating your product page | `/help/app-store-connect/reference/screenshot-specifications/` | **302** → `/help/app-store-connect/reference/app-information/screenshot-specifications` |
| 2.3.3 guideline-reference, "Upload app previews and screenshots" | `/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/` | **Soft 404**: HTTP 200, but the page title is "Page Not Found" |
| Asset page, "Apple Advertising Policies" | `/app-store/marketing/guidelines/` | Lands on "Marketing Resources and Identity Guidelines". The anchor text and the page title disagree. |
| Asset page, "Learn more about App Store search" | `/app-store/discoverability/` | Lands on "Discovery on the App Store and Mac App Store". A separate `/app-store/search/` ("App Store search") also exists. |
| Asset page, "Learn about submitting assets" | `/help/app-store-connect/manage-builds/view-builds-and-metadata` | Lands on "View builds and metadata". The more specific page is https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-assets-from-asset-library |
| News kug6m2ea and ljpl7kyn | `http://developer.apple.com/app-store/asset-best-practices/` | 301 to https |

**Stale first-party page:** https://developer.apple.com/app-store/product-page/ still
says the first screenshots appear in search results "when no app preview is
available". It never mentions creative assets. Follow the newer asset page and
Asset Library page instead.

---

## Gap analysis vs. current repo

What the repo has today:
- `knowledge/app-store-review-guidelines/screenshots-accuracy.md`: 4 rules, 2.3.3 and
  2.3.4 text only.
- `description-accuracy.md`: 2.3, 2.3.1(a), 2.3.7 names and keywords.
- `apple-trademarks-and-product-confusion.md` Rule 2: Editor's Choice badge.
- `knowledge/human-interface-guidelines/app-icons.md`.

A grep for `2.3.2`, `2.3.8`, `2.3.9`, `2.3.10`, `2.3.13`, "product page", "creative
asset", "In-App Event", "Asset Library" and `help/app-review` across `references/`,
`knowledge/` and `skills/` returns no relevant hits.

| Guidance item | Currently covered? (where) | Proposed artifact |
|---|---|---|
| Screenshots show the app in use (2.3.3 text) | Yes: `screenshots-accuracy` Rule 1 | Keep, but **refine**: Rule 1 reads as "all screenshots", while Apple now states "more than half" per device and allows marketing or splash screenshots as the minority |
| Majority-in-use rule, per device and per localization; one screenshot is enough | **No** | Amend `knowledge.app-store-review-guidelines.screenshots-accuracy` (cite the 2-3-3 help page) |
| Overlays must not crowd out the app; no hardware-only or overlay-only screenshots | Partly (Rule 2 allows overlays) | Amend `screenshots-accuracy` |
| Previews are screen captures only; narration and overlays allowed (2.3.4) | Yes: Rules 3–4 | none |
| No prices in screenshots or previews (2.3.7) | Partly: `description-accuracy` Rule 4 covers names and keywords only | Amend `description-accuracy`, or put it in a new asset-content KC |
| No website URLs, copyright symbols, or discounts (advisory, not a guideline) | No | `knowledge.app-store-product-page.asset-content-restrictions` (SHOULD) |
| Unverifiable claims and awards not received | Partly: `description-accuracy` Rule 3 (misleading marketing) | Cross-reference from the asset-content KC |
| Apple-designated recognitions (Editor's Choice, App/Game of the Day, ADA) | Partly: `apple-trademarks…` Rule 2 covers Editor's Choice only | Asset-content KC, `related:` to apple-trademarks |
| Other platforms and marketplaces, including in status bars (2.3.10) | **No** | `knowledge.app-store-review-guidelines.other-platform-references` (MUST) |
| 4+ age rating for icons, screenshots and previews; violence limits (2.3.8) | **No** | `knowledge.app-store-review-guidelines.metadata-age-rating` (MUST) |
| Rights to materials; fictional account data (2.3.9) | No (`third-party-content-licensing` covers 5.2 only) | Optional: `knowledge.app-store-review-guidelines.metadata-rights-and-fictional-data` |
| IAP disclosure in screenshots and previews (2.3.2) | No | Optional: new ASRG KC (Tier decision) |
| In-App Event metadata accuracy (2.3.13) and media 16:9 / 9:16, badges | No | `knowledge.app-store-product-page.in-app-event-media` (+ optional 2.3.13 ASRG KC) |
| Screenshot specs: 1–10 per device size, formats, no alpha, required iPhone and iPad sizes, scaling, iPhone Duo April 2027 | No | `knowledge.app-store-product-page.screenshot-specifications` |
| App preview specs: 0–3, 15–30 s, 500 MB, codecs, 30 fps, previews shown before screenshots, "A Closer Look", poster frame | No | `knowledge.app-store-product-page.app-preview-specifications` |
| Creative assets: header and search-result specs, universal asset, muted and looping, iOS/iPadOS 27+, standalone review, **exempt from the in-use rule** | No | `knowledge.app-store-product-page.creative-assets` |
| Header and search-result messaging (single clear idea, first-time visitor, state the obvious, firsthand experience, fallback order) | No | `knowledge.app-store-product-page.header-and-search-result-messaging` (SHOULD) |
| Image craft (focal point, safe area or center, short localized text, Preview tool) | No | `knowledge.app-store-product-page.image-asset-design` (SHOULD) |
| Video craft (poster frame, start strong, avoid quick cuts for accessibility, seamless loop, silent-first audio) | No | `knowledge.app-store-product-page.video-asset-design` (SHOULD) |
| Storytelling and sequencing (lead with best features, cohesive story, beginning–middle–end, consistent visual style) | No | `knowledge.app-store-product-page.asset-sequencing-and-story` (SHOULD) |
| Localize images and videos | No (the `localization` domain covers code and resources, not App Store metadata) | Rule inside the image and video KCs, or Excluded |
| App icon: Icon Composer, Liquid Glass layers, legible at every size | Mostly: `human-interface-guidelines.app-icons` Rules 1, 3 and its example mention Icon Composer | No new KC. Possibly add the "iPhone, iPad, Mac, and Apple Watch from a single design" scope, after checking it against the HIG app-icons page (not re-verified here: that page is JS-rendered and curl returned no body text) |

## Proposed changes

**A. Normative fixes inside the existing `app-store-review-guidelines` domain (MUST rules)**

1. Amend `knowledge.app-store-review-guidelines.screenshots-accuracy`:
   - majority-in-use per device and per localization;
   - overlays must not crowd out the app;
   - no hardware-only or overlay-only screenshots;
   - update screenshots per version.

   Add the source https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots
   and the 2.3.4 anchor.
2. New `knowledge.app-store-review-guidelines.metadata-age-rating` (2.3.8) and
   `knowledge.app-store-review-guidelines.other-platform-references` (2.3.10).
   Optionally add 2.3.2, 2.3.9 and 2.3.13.
3. **Blocker:** `references/apple/app-store-review-guidelines.md` is already at **98
   lines, the hard cap** (`reference-spec.md`), so it cannot take new `## Source` URLs
   as-is. That forces either a Reference/Skill split or trimming.

**B. New domain `app-store-product-page` (spec facts plus advisory SHOULD rules)**

- Reference: `references/apple/app-store-product-page.md`. Sources:
  - https://developer.apple.com/app-store/asset-best-practices/
  - https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
  - https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
  - https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
  - https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
  - https://developer.apple.com/help/app-store-connect/reference/in-app-events/in-app-event-media-and-audio-specifications
  - https://developer.apple.com/app-store/app-previews/

  Use the post-redirect forms only.
- Knowledge (`knowledge/app-store-product-page/`): `screenshot-specifications`,
  `app-preview-specifications`, `creative-assets`, `in-app-event-media`,
  `asset-content-restrictions`, `header-and-search-result-messaging`,
  `image-asset-design`, `video-asset-design`, `asset-sequencing-and-story`.
  - Use `related:` (not restated rules) to point at `screenshots-accuracy`,
    `description-accuracy`, `apple-trademarks-and-product-confusion` and
    `human-interface-guidelines.app-icons`.
  - Record this as an angle-split in `domain-map.md`, like privacy vs. ASRG: ASRG
    covers what gets rejected; this domain covers specs and how to make assets
    effective.
- Skill: `skills/app-store-product-page/SKILL.md`, id
  `skill.app-store-product-page.foundations` (or `.assets`). Routing groups:
  - Specs → screenshot, preview, creative, IAE
  - Content policy → asset-content-restrictions
  - Craft → image, video, sequence, header/search
  - Hand-offs: compliance is owned by `app-store-review-guidelines`; icon design is
    owned by `human-interface-guidelines`.
- Same-commit obligations from `skill-management.md`: a `skills/index.md` row, plus
  updates to `domain-map.md`, `CHANGELOG.md`, `README.md` (Skills and What's New),
  and `scripts/check_links.py` for the new sources.

## Open questions for the maintainer

1. **Domain shape.** Should this be a new `app-store-product-page` domain (recommended,
   given the 98-line Reference cap and the different concern), or should
   `app-store-review-guidelines` be extended and split into
   `app-store-review-guidelines-metadata`?
2. **Naming.** `app-store-product-page`, `app-store-assets`, or `app-store-marketing`?
   And does v1 also absorb the product-page text fields on
   https://developer.apple.com/app-store/product-page/ (subtitle 30, promotional text
   170, keywords 100 characters), or does it stay assets-only?
3. **Advisory as Knowledge.** SHOULD rules have precedent (about 137 KCs use "Agents
   SHOULD"). But items like "feel current" or "compelling visuals" are not
   deterministic. Which craft items get encoded, and which are Excluded?
4. **MUST vs SHOULD sorting.** The asset page uses "Don't" and "must" for items that are
   not in the Review Guidelines (website URLs, copyright symbols, discounts). Should
   those be encoded as MUST (Apple's wording) or as SHOULD (no rejection authority)?
5. **Spec volatility.** Should the KCs carry full device tables (about 40 sizes; the
   150-line KC cap makes that impossible), or only the required sizes, the scaling
   rule, the limits, and a pointer to the spec page?
6. **iPhone Duo discrepancies.** How should the April 2027 condition be encoded
   (iOS 27.1 SDK per the spec page vs. all submissions per the news posts)? And should
   the preview resolution be held until Apple fixes the "19.5:9" label?
7. **Platform scope for v1.** Creative assets are iOS/iPadOS 27+ only. Should Mac, TV,
   Vision and Watch screenshot and preview specs be in scope?
8. **Workflow.** `workflows/app-store-submission/WORKFLOW.md` currently Excludes "App
   Store Connect metadata … outside this repository". Should the new Skill become a
   step, which means reversing that exclusion?
9. **Source class.** Are developer.apple.com/help/app-review/… and App Store Connect
   Help pages acceptable `## Source` URLs under `reference-spec.md`'s allowed list?
   The repo already cites /app-store/app-privacy-details/, but /help/app-review/ would
   be a first.
10. **Apple-side link issues** (section 8). Should the 2.3.3 page's soft 404 and the
    anchor/title mismatches just be recorded, or reported to Apple?
