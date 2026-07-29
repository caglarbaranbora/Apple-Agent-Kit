# Vertical Slice #0001 --- Login Flow

Status: Draft Version: 0.1.0

## Objective

Validate the Phase 1 architecture using a single end-to-end
implementation chain.

## Scope

Task:

> Implement Sign In for an Apple platform application.

Artifacts under test:

-   skills/login.md
-   knowledge/authentication/authentication.md
-   knowledge/authentication/sign-in-terminology.md
-   knowledge/authentication/button-labels.md
-   knowledge/authentication/accessibility-forms.md

## Expected Routing

login skill

↓

authentication

↓

sign-in-terminology

↓

button-labels

↓

accessibility-forms

## Expected Dependencies

workflow (optional) ↓ login skill ↓ authentication ↓ sign-in-terminology
↓ button-labels ↓ accessibility-forms

No circular dependencies are allowed.

## Validation Checklist

-   Metadata schema is valid.
-   Relative links resolve.
-   Dependencies are acyclic.
-   Routing is deterministic.
-   Context contains only required artifacts.
-   Skills contain no domain knowledge.
-   Knowledge contracts are atomic.

## Success Criteria

-   Architecture requires no structural changes.
-   Routing matches the expected chain.
-   Dependency model behaves as specified.
-   Findings are documented.

## Deliverables

-   Login Skill
-   Four Knowledge Contracts
-   FINDINGS.md

## Exit Criteria

All validation checks pass or every failure is documented in FINDINGS.md
with a proposed architectural action.
