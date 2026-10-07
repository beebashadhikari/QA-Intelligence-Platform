# Test Intelligence Skill

## Purpose

Provide evidence-driven recommendations about which software tests
should be executed first for a selected release.

The goal is not to randomly prioritize tests.

The goal is to determine test execution priority using measurable
evidence from the QA Intelligence Platform.

---

## Source of Truth

The QA Intelligence Platform API is the authoritative source for
test intelligence.

Never invent:

- test scores
- risk levels
- test statuses
- defect evidence
- business criticality
- historical failures
- module risk

If the API does not provide the evidence, explicitly state that
the evidence is unavailable.

---

## Required Release Context

Every analysis must use the release selected by the user.

Example:

Release:
2.4.0

Do not silently switch to another release.

The release version must remain consistent across all API calls.

---

## Primary API

Use:

GET /api/releases/{release_version}/recommendations

Example:

GET /api/releases/2.4.0/recommendations

Expected response:

{
  "release_version": "2.4.0",
  "recommendations": [
    {
      "test_case_id": "TC-103",
      "title": "Successful checkout",
      "module": "Payments",
      "score": 85,
      "risk_level": "HIGH",
      "reasons": [
        "Module has a critical/high-severity defect.",
        "Test has failed in the current release.",
        "Test is business-critical."
      ],
      "status": "failed",
      "action": "Investigate the failure and rerun the test after corrective action.",
      "blocking_reason": null
    }
  ]
}

---

## Recommendation Priority

When determining which test should be executed first,
consider the following evidence in order:

1. Risk level
2. Recommendation score
3. Failed status
4. Blocked status
5. Business criticality
6. Recent code/module changes
7. Defect severity
8. Historical execution failures

Higher-risk and higher-scoring tests should generally receive
higher execution priority.

---

## Risk Interpretation

HIGH:

The test represents significant release risk and should receive
early QA attention.

MEDIUM:

The test has meaningful risk but may be executed after higher-risk
tests.

LOW:

The test currently has comparatively lower evidence-based risk.

Do not change the risk level supplied by the API.

---

## Status Interpretation

FAILED:

The test has failed and requires investigation or corrective action.

BLOCKED:

The test cannot currently be executed or completed and requires
resolution of the blocking condition.

PASSED:

The test has passed, but it may still require execution again if
new evidence indicates increased risk.

---

## Reasons

The `reasons` field contains evidence explaining why the test was
recommended.

Do not replace evidence with generic QA statements.

Example:

FACT:
"Test has failed in the current release."

INFERENCE:
"This increases the likelihood that the test should be prioritized."

RECOMMENDATION:
"Investigate the failure and rerun the test."

---

## Evidence Classification

Every conclusion should be classified internally as one of:

FACT
Directly supported by platform data.

INFERENCE
Reasoning derived from available facts.

MISSING EVIDENCE
Information required for a stronger conclusion but unavailable.

RECOMMENDATION
An action proposed based on the available evidence.

Never present an inference as a fact.

---

## Recommended Output

When asked:

"Which tests should QA execute first?"

Return:

1. Test ID
2. Test title
3. Module
4. Score
5. Risk level
6. Current status
7. Evidence/reasons
8. Recommended action

Example:

Priority 1

TC-103 — Successful checkout

Score: 85
Risk: HIGH
Status: FAILED

Why:
- Module has a high-severity defect.
- Test failed in the current release.
- Test is business-critical.

Action:
Investigate the failure and rerun the test after corrective action.

---

## Important Rules

Do not:

- invent test scores
- invent defects
- invent failures
- invent business criticality
- invent historical data
- override API risk levels
- claim a test is safe without evidence
- claim that passing means zero risk

Do:

- retrieve evidence
- preserve release context
- rank tests using platform intelligence
- explain why a test is prioritized
- identify missing evidence
- provide actionable QA recommendations