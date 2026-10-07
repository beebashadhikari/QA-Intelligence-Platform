# Risk Intelligence Skill

## Purpose

Analyze release and module risk using evidence from the
QA Intelligence Platform.

Risk analysis must be evidence-driven.

---

## Source of Truth

Use:

GET /api/releases/{release_version}/risk

The API is authoritative for:

- module risk
- risk score
- severity
- defect evidence
- change evidence
- affected functionality

Never invent risk scores.

---

## Release Context

Always preserve the release version selected by the user.

Example:

2.4.0

All related evidence must belong to the same release.

---

## Risk Levels

HIGH:

Significant evidence of release risk exists.

MEDIUM:

Meaningful risk exists but is below the high-risk threshold.

LOW:

Current evidence indicates comparatively lower risk.

Do not modify the risk classification returned by the platform.

---

## Evidence

Risk analysis may consider:

- code/module changes
- high-severity defects
- critical defects
- failed tests
- blocked tests
- business-critical functionality
- historical failures

Only claim evidence that is actually available.

---

## Evidence Classification

FACT:
Returned directly by the platform.

INFERENCE:
Reasoning derived from platform evidence.

MISSING EVIDENCE:
Important information that is unavailable.

RECOMMENDATION:
Action suggested from the evidence.

---

## Output

When explaining risk, provide:

- Release
- Module
- Risk level
- Risk score
- Supporting evidence
- Impact
- Recommended QA action

Example:

Payments

Risk: HIGH
Score: 84.75

Evidence:
- High-severity defects exist.
- Relevant tests have failed.
- Payment functionality is affected.

Recommendation:
Prioritize payment-related regression and investigate failing tests.