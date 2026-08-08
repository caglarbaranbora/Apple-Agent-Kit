# Test Plans

Status: Approved Version: 1.0.0

## Metadata

``` yaml
id: knowledge.xcode.test-plans
artifact_type: knowledge
title: Test Plans
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines how an agent configures an .xctestplan — the default-plan choice a scheme depends on, tag and checkbox inclusion, per-configuration runtime settings, and the multi-scheme sharing that makes one edit reach several schemes.
domain: Xcode
tags:
  - xcode
  - test-plans
  - testing
references:
  - https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback
  - https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project
depends_on:
  - knowledge.xcode.schemes-and-targets
related:
  - knowledge.xcode.build-configurations
  - knowledge.xcode.code-coverage
last_updated: 2026-08-08
```

## Intent

This contract defines how an AI coding agent creates and configures an
Xcode test plan so the scheme's test action runs the intended tests under
the intended runtime environment, and so a change to one plan does not
silently change what another scheme tests.

## Scope

### Included

-   What a test plan is, where it attaches, and the default-plan choice a scheme makes
-   Selecting tests by target, by tag (Xcode 16+), and by the Included checkbox
-   Configurations: what each one sets, and that the plan runs once per configuration
-   Sharing one plan across several schemes

### Excluded

-   Writing the tests themselves — XCTest, Swift Testing, `Tag` declaration, and XCUITest are owned by the `testing` domain
-   Enabling and reading code coverage — see `code-coverage`
-   Scheme structure and the action-to-configuration mapping — see `schemes-and-targets`
-   `xcodebuild -testPlan` and `--only-test-configuration` — CLI usage, Excluded from this domain

## Rules

### Rule 1

Agents MUST set a newly created test plan as the scheme's default before
expecting it to run, because creating one does not select it. Per Apple's
documentation: "You must choose one test plan as the default plan for the
scheme; Xcode uses this plan to run tests when none is explicitly
specified." Xcode has already made this choice — "Xcode creates a default
test plan that includes all of the tests from the test targets built by
your scheme" — so a second plan added and left unselected changes nothing
about what Product > Test runs.

### Rule 2

Agents MUST NOT exclude a test from a plan as a way of handling a test
that fails conditionally. Per Apple's documentation: "If you exclude a
test function or test case from a test plan, Xcode skips over the test
function or test case and doesn't provide feedback on their status. The
only effect an excluded test function has on the outcome of the test
action is if the test contains a build error, in which case the whole
test action fails." Exclusion removes the test from reporting entirely;
the runtime-condition and expected-failure mechanisms in the test
frameworks are what keep a test visible while changing its effect on the
result.

### Rule 3

Agents MUST treat the tag filters as the outer filter and the Included
checkboxes as the inner one, not as two equal switches. Per Apple's
documentation, a test plan's outline view lets you "select or deselect
any item that matches the conditions from the Include Tags and Exclude
Tags fields" — a test the tag fields have already excluded cannot be
restored by its checkbox. To take every test, "leave the Include Tags and
Exclude Tags fields empty."

### Rule 4

Agents MUST NOT add a test plan configuration without accounting for the
run it adds. Per Apple's documentation: "Xcode runs the tests specified
in a test plan once for each of that plan's configurations." A second
configuration doubles the wall-clock cost of every invocation of that
plan, including on CI.

### Rule 5

Agents MUST check which schemes use a test plan before editing it. Per
Apple's documentation: "You can associate a test plan with more than one
scheme, to get the same test suites and functions included with the same
configurations in multiple schemes." Editing a plan to narrow one
scheme's feedback loop narrows every scheme that shares it.

### Rule 6

Agents MUST set a run's language and region in a test plan configuration
rather than by changing the device or simulator, when the test exists to
exercise a localization. Per Apple's documentation, a configuration sets
"The language used for localized strings in the product under test, or
System Language to use the language specified in System Settings" and
"The region used for locale settings in the product under test, or System
Region to use the region specified in System Settings" — which is what
makes the localization under test a property of the plan rather than of
whoever ran it.

## Compliant Example

-   ✓ A `Presubmission.xctestplan` includes only the unit test target and excludes the `.uiTest` tag; a `Full.xctestplan` leaves both tag fields empty and adds a second configuration whose Application Language is Arabic. `Presubmission` is marked Default in Manage Test Plans, so `Product > Test` runs the fast plan and CI names the full one explicitly. (Rules 1, 3, 4, 6)

## Non-Compliant Example

-   ✗ A flaky integration test is unchecked in the shared `Full.xctestplan` to get a green run. The plan is also attached to the release scheme, so the test stops reporting there too, and because exclusion produces no status the next three releases ship with nobody aware the integration path is untested. (Rules 2, 5)

## Dependencies

-   knowledge.xcode.schemes-and-targets — a test plan configures a scheme's test action; the scheme is what selects the targets the plan can draw tests from.

## References

-   [Apple Developer — Improving code assessment by organizing tests into test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback)
-   [Apple Developer — Customizing the build schemes for a project](https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project)
