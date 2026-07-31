---
name: style-guide
description: Route writing and terminology implementation tasks to the minimum required style-guide Knowledge Contracts — capitalization, punctuation, button labels, inclusive writing, date and number formatting. Use when writing or reviewing app UI text, labels, buttons, errors, or onboarding copy. Triggers on writing, terminology, capitalization, punctuation, button label wording, inclusive writing, date and number formatting, style guide, UI copy.
id: skill.style-guide.writing
title: Style Guide Writing
version: 0.2.0
status: Draft
artifact_type: skill
domain: Style Guide
routes: [knowledge.style-guide.ui-action-verbs, knowledge.style-guide.pointer-and-click-terminology, knowledge.style-guide.touch-gesture-verbs, knowledge.style-guide.general-button-labels, knowledge.style-guide.navigation-controls, knowledge.style-guide.presentation-surfaces, knowledge.style-guide.input-controls, knowledge.style-guide.status-and-progress-indicators, knowledge.style-guide.app-chrome-and-window-terminology, knowledge.style-guide.app-state-and-error-terminology, knowledge.style-guide.connectivity-and-media-terminology, knowledge.style-guide.instructional-voice-and-phrasing, knowledge.style-guide.capitalization-style-rules, knowledge.style-guide.capitalization-of-apple-proper-nouns, knowledge.style-guide.punctuation-and-typography-in-text, knowledge.style-guide.abbreviations-and-acronyms, knowledge.style-guide.units-of-measure, knowledge.style-guide.numeric-terminology-supplement, knowledge.style-guide.international-formatting, knowledge.style-guide.international-style, knowledge.style-guide.writing-inclusively, knowledge.style-guide.technical-notation, knowledge.style-guide.copyright-and-trademarks, knowledge.style-guide.sign-in-and-authentication-terminology, knowledge.style-guide.authentication-credentials-and-biometrics]
related:
  - skill.authentication.login
last_updated: 2026-07-31
---

# Style Guide Writing Skill

## Purpose

Route writing/terminology implementation tasks to the minimum required
style-guide Knowledge Contracts.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/style-guide/.

-   UI interaction verbs, clicks, taps, buttons, navigation -> ui-action-verbs.md, pointer-and-click-terminology.md, touch-gesture-verbs.md, general-button-labels.md, navigation-controls.md
-   UI components: dialogs/sheets, inputs, progress, chrome -> presentation-surfaces.md, input-controls.md, status-and-progress-indicators.md, app-chrome-and-window-terminology.md
-   App state, connectivity, instructional voice -> app-state-and-error-terminology.md, connectivity-and-media-terminology.md, instructional-voice-and-phrasing.md
-   Capitalization, punctuation, abbreviations -> capitalization-style-rules.md, capitalization-of-apple-proper-nouns.md, punctuation-and-typography-in-text.md, abbreviations-and-acronyms.md
-   Units, numeric edge cases, locale formatting -> units-of-measure.md, numeric-terminology-supplement.md, international-formatting.md, international-style.md
-   Inclusive writing -> writing-inclusively.md
-   Code font / placeholder-name conventions -> technical-notation.md
-   Copyright/trademark text -> copyright-and-trademarks.md
-   Sign-in, sign-out, login wording -> sign-in-and-authentication-terminology.md
-   Passkey, password, PIN, biometric wording -> authentication-credentials-and-biometrics.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge Contract
in knowledge/style-guide/ — do not guess or fall back to general knowledge.
