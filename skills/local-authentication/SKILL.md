---
name: local-authentication
description: Route Face ID/Touch ID/device-passcode implementation tasks to the correct Knowledge Contracts -- availability and biometry-type detection, policy evaluation, reason strings and Info.plist, error handling, LAContext lifecycle, Keychain-biometric binding, and fallback UX. Use when checking biometric availability, calling evaluatePolicy, writing an NSFaceIDUsageDescription string, handling an LAError, managing LAContext lifetime, binding a Keychain item to biometrics via SecAccessControl, or deciding on a passcode fallback. v1 is iOS/iPadOS LocalAuthentication framework API only -- no macOS/watchOS-specific behavior, no general Keychain storage (SecItemAdd/Copy/Update for non-biometric-bound items). Triggers on Face ID, Touch ID, LAContext, LABiometryType, canEvaluatePolicy, evaluatePolicy, deviceOwnerAuthentication, deviceOwnerAuthenticationWithBiometrics, LAPolicy, LAError, biometryNotEnrolled, biometryLockout, NSFaceIDUsageDescription, localizedReason, localizedFallbackTitle, SecAccessControl, biometryCurrentSet, biometryAny, biometric Keychain, Enter Passcode fallback, biometric authentication.
id: skill.local-authentication.foundations
title: Local Authentication — Foundations
version: 0.1.0
status: Draft
artifact_type: skill
domain: Local Authentication
routes: [knowledge.local-authentication.availability-and-biometry-type, knowledge.local-authentication.policy-evaluation, knowledge.local-authentication.reason-strings-and-info-plist, knowledge.local-authentication.error-handling, knowledge.local-authentication.context-lifecycle, knowledge.local-authentication.keychain-biometric-binding, knowledge.local-authentication.fallback-ux-and-passcode]
related: []
last_updated: 2026-08-05
---

# Local Authentication — Foundations Skill

## Purpose

Route Face ID/Touch ID/device-passcode implementation tasks to the
minimum required Local Authentication Knowledge Contracts. v1 scope is
the iOS/iPadOS LocalAuthentication framework API plus the
Keychain-biometric binding seam — no macOS/watchOS-specific behavior, no
general Keychain storage.

## Routing

Load only the contracts relevant to the task. All paths relative to
knowledge/local-authentication/.

-   Checking availability or biometry type -> availability-and-biometry-type.md
-   Calling evaluatePolicy / choosing a policy -> policy-evaluation.md
-   Writing localizedReason or NSFaceIDUsageDescription -> reason-strings-and-info-plist.md
-   Handling an LAError -> error-handling.md
-   Managing LAContext lifetime or re-enrollment detection -> context-lifecycle.md
-   Binding a Keychain item to biometrics -> keychain-biometric-binding.md
-   Deciding on or configuring a passcode fallback -> fallback-ux-and-passcode.md

Never load more than the contracts relevant to the specific question.

## Stop Conditions

Stop and report if the requested topic has no matching Knowledge
Contract in knowledge/local-authentication/ — do not guess or fall back
to general knowledge.

-   macOS/watchOS-specific LocalAuthentication behavior — Deferred
-   General Keychain storage (`SecItemAdd`/`SecItemCopyMatching`/
    `SecItemUpdate` for non-biometric-bound items) — owned by `security`
