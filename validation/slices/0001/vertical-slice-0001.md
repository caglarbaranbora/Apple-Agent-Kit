# Vertical Slice #0001 --- Login Flow

> **Superseded 2026-08-08 — void, not merely old.** All five artifacts under test
> below were deleted when the `authentication` domain was retired in Phase 4:
> `skills/login.md` and the four `knowledge/authentication/` Contracts. This record
> validates an architecture that no longer exists, and cannot support an approval
> decision. Its own F-001 recommended adding `artifact_type`, which Phases 1–2 did.
> Replaced by slices #0002, #0003, and #0004.
>
> The `Status:`/`Version:` line below carries no meaning. `docs/artifact-lifecycle.md`
> places validation reports under `validation/` outside the lifecycle, so this document
> is not `Draft`, is not promoted, and is not transitioned to `Archived` — a document
> the lifecycle excludes cannot be moved through it. It is superseded, which is a fact
> about the record rather than a state in a machine.

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
