# Login Skill

Status: Draft Version: 0.1.0

## Purpose

Route authentication-related implementation tasks to the minimum
required Knowledge Contracts.

## Trigger

Use this skill when the task involves:

-   Sign In
-   Sign Up
-   Authentication UI
-   Apple Account authentication
-   Login terminology
-   Authentication accessibility

## Routing

Load in order:

1.  ../../knowledge/authentication/authentication.md
2.  ../../knowledge/authentication/sign-in-terminology.md
3.  ../../knowledge/authentication/button-labels.md
4.  ../../knowledge/authentication/accessibility-forms.md

## Do Not Load

Do not load unrelated domains (StoreKit, Widgets, Notifications, etc.)
unless explicitly required.

## Output

Return only the routed Knowledge Contracts. This skill must not contain
implementation guidance.

## Dependencies

depends_on: - knowledge.authentication.authentication -
knowledge.authentication.sign-in-terminology -
knowledge.authentication.button-labels -
knowledge.authentication.accessibility-forms
