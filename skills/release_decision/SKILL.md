---
name: release_decision
description: Explain release readiness (READY / CONDITIONAL / NOT_READY) using deterministic evidence from the QA Intelligence Platform.
---

# Release Decision Skill

## Purpose

Explain release readiness using deterministic evidence from the
QA Intelligence Platform.

The AI may explain the release decision.

The AI must not independently approve or reject a release.

---

## Source of Truth

Use:

GET /api/releases/{release_version}

GET /api/releases/{release_version}/quality

GET /api/releases/{release_version}/risk

GET /api/releases/{release_version}/recommendations

GET /api/releases/{release_version}/defects

GET /api/dashboard/release/{release_version}

---

## Decision States

READY

No known release-blocking condition is present based on available
evidence.

CONDITIONAL

The release has meaningful quality or risk concerns that require
QA review or corrective action.

NOT_READY

A release-blocking condition or critical quality issue prevents
normal approval.

---

## Hard Blocking Evidence

Pay particular attention to:

- release blockers
- critical defects
- blocked tests
- severe unresolved quality issues

Do not invent blockers.

---

## Risk Evidence

Also consider:

- high-severity defects
- high-risk modules
- high-risk failed tests
- high-risk blocked tests
- regression status
- quality health

---

## Output

When asked:

"Why is this release conditional?"

Return:

1. Release
2. Current decision
3. Evidence
4. Risks
5. Required actions
6. Missing evidence
7. Human decision requirement

---

## Human Approval

The AI must never say:

"The release is approved."

Instead say:

"The available evidence indicates READY, but final release approval
belongs to the QA/release owner."

Likewise, the AI must not claim that a release is rejected unless
the platform evidence explicitly supports that conclusion.

---

## Evidence Classification

FACT:
Direct platform evidence.

INFERENCE:
Reasoning derived from evidence.

MISSING EVIDENCE:
Information unavailable from the platform.

RECOMMENDATION:
Suggested next action.