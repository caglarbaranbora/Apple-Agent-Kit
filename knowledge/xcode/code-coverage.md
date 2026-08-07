# Code Coverage

Status: Draft Version: 0.1.0

## Metadata

``` yaml
id: knowledge.xcode.code-coverage
artifact_type: knowledge
title: Code Coverage
version: 0.1.0
status: Draft
owner: Apple Agent Kit
summary: Defines where code coverage is enabled — the Configurations pane of a test plan, per configuration or under Shared Settings — the target scoping the percentage depends on, and what the resulting number does and does not attest.
domain: Xcode
tags:
  - xcode
  - code-coverage
  - test-plans
references:
  - https://developer.apple.com/documentation/xcode/determining-how-much-code-your-tests-cover
  - https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback
depends_on:
  - knowledge.xcode.test-plans
related:
  - knowledge.xcode.schemes-and-targets
last_updated: 2026-08-07
```

## Intent

This contract defines how an AI coding agent turns on code coverage in an
Xcode project and how it may report the resulting number, so that a
coverage percentage is scoped to a known target set and is not read as
evidence of anything the data does not support.

## Scope

### Included

-   Where coverage is enabled: the Configurations tab of a test plan, per configuration or under Shared Settings
-   Scoping collection to a chosen set of targets
-   Reading the Coverage pane of the Report navigator and the source-editor annotation
-   What a coverage percentage attests, and what it does not

### Excluded

-   Test plan creation, tests selection, and configurations generally — see `test-plans`
-   Writing tests, and the skip/known-issue mechanisms whose interaction with coverage Rule 5 depends on — owned by the `testing` domain
-   `xcodebuild -enableCodeCoverage` and `.xcresult` extraction — CLI usage, Excluded from this domain
-   Coverage thresholds enforced in CI — no Apple-documented mechanism; Excluded

## Rules

### Rule 1

Agents MUST enable coverage in a test plan rather than looking for a
build setting or a scheme option. Per Apple's documentation: "Code
coverage is a testing option you can configure for your test plans." The
documented path is: "Open a test plan… Click the Configurations tab…
Scroll down to the Code Coverage section. Click the value for Code
Coverage and select the 'Gather coverage for' checkbox on the popover."

### Rule 2

Agents MUST enable coverage under Shared Settings when every
configuration in the plan should report it, and MUST NOT assume enabling
it on one configuration covers the plan. Per Apple's documentation:
"Select a specific configuration, or select Shared Settings to enable
testing across all configurations." A plan with several configurations
and coverage set on only one reports a run's worth of data, not the
plan's.

### Rule 3

Agents MUST select the targets coverage is collected from rather than
accepting whatever the popover offers, because the percentage means
nothing without that set. Per Apple's documentation, the last step is:
"Use the options from the pop-up menu to select targets to collect the
information from." A reported number MUST be stated together with the
targets it was gathered for.

### Rule 4

Agents MUST NOT compare a performance measurement taken with coverage
enabled against one taken without it. Per Apple's documentation: "Code
coverage data collection impacts your code's performance. Even if the
impact is significant, it is also linear, so results between two runs
with code coverage enabled remain comparable." The comparability the note
grants is between coverage-enabled runs only.

### Rule 5

Agents MUST NOT read a coverage percentage as evidence that the covered
code passed its tests. Per Apple's documentation: "Code coverage metrics
do not include skipped tests but they do include tests that run marked
with known issues or expected failures." A line exercised only by a test
recorded as an expected failure counts as covered.

### Rule 6

Agents MUST NOT propose raising coverage as a substitute for test
quality, and MUST NOT report a high percentage as adequacy. Per Apple's
documentation: "Although achieving a high level of coverage is an
excellent goal, code coverage alone doesn't ensure that your tests are
doing their job and are robust enough for unexpected behaviors. Be sure
to pair high code coverage with well-written tests."

## Compliant Example

-   ✓ Coverage is enabled under Shared Settings of `Full.xctestplan` and scoped to the app and framework targets only. The agent reports "68% across `AppCore` and `Networking`", then reads the source-editor annotation to name three uncovered error branches — the report highlights what needs coverage rather than what has it. (Rules 2, 3, 6)

## Non-Compliant Example

-   ✗ Coverage is switched on for one configuration of a two-configuration plan, left at whatever target selection the popover offered, and the resulting 91% is reported as "the suite is comprehensive." The figure is scoped to a target set nobody chose, omits the second configuration entirely, and counts a payment path exercised only by a test marked as a known issue. (Rules 2, 3, 5, 6)

## Dependencies

-   knowledge.xcode.test-plans — coverage is a setting inside a test plan configuration; there is nowhere else to enable it.

## References

-   [Apple Developer — Determining how much code your tests cover](https://developer.apple.com/documentation/xcode/determining-how-much-code-your-tests-cover)
-   [Apple Developer — Improving code assessment by organizing tests into test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback)
