---
name: authentication
description: Route authentication-related Apple platform implementation tasks to the correct Knowledge Contracts — sign-in, sign-up, credentials. Use when the task involves login screens, sign-in terminology, or authentication accessibility. Triggers on sign in, sign up, login, authentication, Apple Account, credentials. For Face ID/Touch ID/biometric implementation, see the `local-authentication` Skill instead.
id: skill.authentication.login
title: Login Skill
version: 0.2.0
status: Draft
artifact_type: skill
domain: Authentication
routes:
  - knowledge.authentication.authentication
  - knowledge.authentication.sign-in-terminology
  - knowledge.authentication.button-labels
  - knowledge.authentication.accessibility-forms
related:
  - skill.style-guide.writing
last_updated: 2026-07-31
---

# Login Skill

## Purpose

Route authentication-related implementation tasks to the minimum
required Knowledge Contracts.

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

## Stop Conditions

Stop and report if the requested authentication topic has no matching
Knowledge Contract in knowledge/authentication/ — do not guess or fall
back to general knowledge.
